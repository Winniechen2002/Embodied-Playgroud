"""Manifest-bound third-party source snapshots; no fetching or installation."""
import hashlib
import json
from pathlib import Path, PurePosixPath


def embedded_manifest(root):
    path=Path(root)/'third_party/manifest.json'
    if not path.is_file():raise ValueError('Missing embedded third-party source manifest')
    data=json.loads(path.read_text())
    if data.get('version')!=1 or not isinstance(data.get('files'),dict):
        raise ValueError('Invalid embedded source manifest')
    for name in data['files']:
        parts=PurePosixPath(name).parts
        if not name.startswith('third_party/') or '..' in parts or '.git' in parts or '\\' in name:
            raise ValueError('Unsafe embedded source path')
    return data


def embedded_files(root):
    data=embedded_manifest(root)
    return sorted([*data['files'],'third_party/manifest.json','third_party/.gitattributes',
                   'third_party/README.md'])


def verify_embedded_sources(root, *, files=None):
    root=Path(root).resolve();data=embedded_manifest(root);issues=[]
    for name,record in data['files'].items():
        path=root/name
        if not path.resolve().is_relative_to(root) or path.is_symlink() or not path.is_file():
            issues.append(dict(path=name,error='missing_or_linked'));continue
        if files is None:
            content=path.read_bytes()
            actual=dict(sha256=hashlib.sha256(content).hexdigest(),bytes=len(content))
        else:actual=files.get(name,{})
        if any(actual.get(k)!=record[k] for k in ('sha256','bytes')):
            issues.append(dict(path=name,error='content_mismatch'))
    return dict(status='failed' if issues else 'passed',file_count=len(data['files']),
        project_count=sum(len(p['path'].split('/'))==2 for p in data['projects']),
        nested_project_count=sum(len(p['path'].split('/'))>2 for p in data['projects']),
        issues=issues,unavailable_lfs=data.get('unavailable_lfs',[]))
