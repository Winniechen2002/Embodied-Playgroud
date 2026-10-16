"""Future public content audit, without constructing an export directory."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile
from urllib.parse import unquote,urlsplit
from .environment_catalog import ROOT,digest
from .environment_release import source_files,license_inventory,export_content


def public_files(root=ROOT):
    root=Path(root)
    docs=['README.md','README.en.md','README.zh-CN.md','docs/README.en.md','docs/README.zh-CN.md']
    for stem in ('evaluation_protocol','environment_validation','environment_installation','environment_assets'):
        docs += [f'docs/{stem}.{language}.md' for language in ('en','zh-CN')]
    docs += ['docs/evaluation_protocol.md']
    docs += [str(p.relative_to(root)) for pattern in ('rules*.md','Vision_rules*.md') for p in root.glob(pattern)]
    docs += [str(p.relative_to(root)) for p in (root/'docs').glob('*.md')]
    docs += [str(p.relative_to(root)) for p in (root/'docs/tools').rglob('*.md')]
    # Paper-facing definitions contain public task identities, not agent results.
    docs += [str(p.relative_to(root)) for p in (root/'docs/ep_subsets').glob('*') if p.suffix in ('.md','.json')]
    docs += [str(p.relative_to(root)) for p in (root/'docs/evaluation').glob('*') if p.suffix in ('.md','.json')]
    docs += [str(p.relative_to(root)) for p in (root/'env/runtime').glob('*') if p.suffix in ('.json','.txt')]
    return sorted(set(map(str,source_files(root)))|set(docs))


def audit_maniskill_archive(root):
    """Verify embedded assets without extracting or treating integrity as a license."""
    base=Path(root)/'env/maniskill_lgd/agentbench_maniskill/resources'
    manifest=json.loads((base/'asset_manifest.json').read_text())
    bundle=base/manifest['bundle'];expected={r['path']:r for r in manifest['files']}
    failures=[];seen=set();notices=[]
    if len(expected)!=len(manifest['files']) or len(expected)!=444:failures.append('manifest_count_or_duplicates')
    if bundle.stat().st_size!=manifest['bundle_bytes'] or hashlib.sha256(bundle.read_bytes()).hexdigest()!=manifest['bundle_sha256']:
        failures.append('archive_identity')
    with tarfile.open(bundle,'r:gz') as archive:
        for member in archive:
            name=member.name
            if not member.isfile() or Path(name).is_absolute() or '..' in Path(name).parts or name in seen or name not in expected:
                failures.append('unexpected_member:'+name);continue
            seen.add(name);data=archive.extractfile(member).read();record=expected[name]
            if len(data)!=record['bytes'] or hashlib.sha256(data).hexdigest()!=record['sha256']:
                failures.append('member_identity:'+name)
            if name.startswith('notices/'):notices.append(name)
    failures.extend('missing_member:'+name for name in sorted(set(expected)-seen))
    return dict(status='passed_integrity' if not failures else 'failed',file_count=len(seen),
        sha256=manifest['bundle_sha256'],failures=failures,notices=notices,redistribution='unqualified',
        limitation='Archive and file integrity do not establish third-party redistribution rights')


def audit(root=ROOT):
    root=Path(root); names=public_files(root); present=set(names);files={};issues=[];contents={}
    present_dirs={str(parent) for name in present for parent in Path(name).parents}
    pinned_documents=set();upstream_documentation_links=[]
    for name in names:
        if Path(name).name!='UPSTREAM.json':continue
        declaration=json.loads((root/name).read_text())
        for dependency in declaration.get('files',{}):
            candidate=Path(name).parent/dependency
            if candidate.suffix=='.md':pinned_documents.add(str(candidate))
    for name in names:
        path=root/name
        if not path.is_file():issues.append(dict(kind='missing_public_file',path=name));continue
        original=path.read_bytes();content=export_content(name,original);contents[name]=content
        files[name]=dict(sha256=hashlib.sha256(content).hexdigest(),bytes=len(content),
            source_sha256=hashlib.sha256(original).hexdigest(),transformed=content!=original)
        if content.startswith(b'version https://git-lfs.github.com/spec/v1'):
            issues.append(dict(kind='unresolved_lfs_pointer',path=name))
        if path.suffix=='.md':
            for url in re.findall(r'\]\(([^\s)]+)',content.decode()):
                parts=urlsplit(url)
                if parts.scheme or parts.netloc or not parts.path:continue
                target=(path.parent/unquote(parts.path)).resolve()
                try:relative=str(target.relative_to(root.resolve()))
                except ValueError:
                    issues.append(dict(kind='external_filesystem_link',path=name,target=url));continue
                if relative not in present and relative not in present_dirs:
                    record=dict(path=name,target=relative)
                    if name in pinned_documents:
                        upstream_documentation_links.append(dict(**record,status='not_bundled',
                            reason='Unmodified, hash-pinned upstream documentation; referenced upstream document is not redistributed.'))
                    else:issues.append(dict(kind='public_link_outside_allowlist',**record))
    modules={}
    for name in names:
        if name.endswith('.py'):
            path=Path(name)
            if name.startswith('source/'):
                module='.'.join(path.with_suffix('').parts[2:])
            elif name.startswith('env/maniskill_lgd/agentbench_maniskill/'):
                module='.'.join(path.with_suffix('').parts[2:])
            elif name.startswith('scripts/'):
                module=path.stem
            else:continue
            if module.endswith('.__init__'):module=module[:-9]
            modules[module]=name
    missing_imports=[];external=[]
    roots={'agentbench_maniskill','agentbench','agentbench_platform','agentbench_sdk','agentbench_mujoco','agentbench_hanoi40','agentbench_cube20'}
    for module,name in modules.items():
        source=contents[name].decode();tree=ast.parse(source)
        package=module if Path(name).name=='__init__.py' else module.rpartition('.')[0]
        for node in ast.walk(tree):
            targets=[]
            if isinstance(node,ast.Import):targets=[alias.name for alias in node.names]
            elif isinstance(node,ast.ImportFrom):
                if node.level:
                    base=package.split('.')[:len(package.split('.'))-node.level+1]
                    target='.'.join(base+([node.module] if node.module else []))
                    if node.module:targets=[target]
                    else:targets=[target+'.'+alias.name for alias in node.names if target+'.'+alias.name in modules]
                elif node.module:targets=[node.module]
            for target in targets:
                if target.split('.')[0] in roots and target not in modules:
                    missing_imports.append(dict(importer=name,module=target,line=node.lineno))
            if isinstance(node,ast.Constant) and isinstance(node.value,str) and (
                node.value.startswith(('/home/','/workspace/')) or
                re.match(r'https?://.*\.(usd|usda|urdf|zip)(?:$|\?)',node.value)):
                external.append(dict(path=name,line=node.lineno,value=node.value))
    issues += [dict(kind='missing_internal_module',**row) for row in missing_imports]
    licenses=license_inventory(files,root)
    embedded=audit_maniskill_archive(root)
    if embedded['failures']:issues.append(dict(kind='embedded_asset_integrity',details=embedded['failures']))
    groups={}
    for name,record in files.items():
        if Path(name).suffix.lower() in ('.usd','.usda','.usdc','.urdf','.stl','.obj','.dae','.xml','.png','.jpg'):
            prefix=name.split('/assets/')[0]+'/assets' if '/assets/' in name else str(Path(name).parent)
            groups.setdefault(prefix,[]).append(name)
    assets=[]
    for prefix,items in sorted(groups.items()):
        notices=[n for n in licenses['notices'] if any(i.startswith(str(Path(n).parent)+'/') for i in items)]
        provenance=[n for n in files if Path(n).name.upper().startswith('UPSTREAM')
            and any(i.startswith(str(Path(n).parent)+'/') for i in items)]
        assets.append(dict(path=prefix,file_count=len(items),sha256=digest({n:files[n] for n in items}),
            notices=notices,provenance=provenance,redistribution='unverified',
            blocker='Confirm upstream revision, scope of license and redistribution rights; notices alone are insufficient'))
    pins=[]
    for name in files:
        if Path(name).name!='UPSTREAM.json':continue
        declaration=json.loads(contents[name]);failures=[];checked=0
        for relative,record in declaration.get('files',{}).items():
            target=(root/name).parent/relative
            if not target.resolve().is_relative_to(root.resolve()):
                failures.append(relative);continue
            if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest()!=record['sha256']:
                failures.append(relative)
            checked+=1
        pins.append(dict(path=name,checked_files=checked,hash_mismatches=failures,
            declared_source={k:v for k,v in declaration.items() if k!='files'}))
        if failures:issues.append(dict(kind='asset_pin_mismatch',path=name,files=failures))
    git=subprocess.run(['git','-C',str(root),'ls-files','--stage'],capture_output=True,text=True)
    # A source archive need not contain Git history to be auditable.
    submodules=[]
    for line in git.stdout.splitlines():
        if line.startswith('160000 '):
            left,path=line.split('\t',1)
            submodules.append(dict(path=path,revision=left.split()[1],included=path in present,
                required_for_environment=False))
    return dict(version='public-content-audit-v1',files=files,content_digest=digest(files),
        dependency_closure='failed' if missing_imports else 'static_imports_checked',
        issues=issues,upstream_documentation_links=upstream_documentation_links,external_references=external,assets=assets,licenses=licenses,upstream_pins=pins,embedded_assets=dict(maniskill=embedded),
        optional_submodules=submodules,source_release_ready=False,distribution_validation='not_executed',
        limitations=['Static imports do not verify dynamic imports or remote asset resolution',
                    'Asset license scope and provenance require explicit maintainer evidence'])
