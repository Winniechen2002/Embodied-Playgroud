"""Optional CPU GraspNet adapter for externally prepared, pinned worker images."""
import hashlib
import json
import os
from pathlib import Path
import re

from . import graspnet


def digest(path):
    path=Path(path)
    if path.is_symlink() or not path.is_file():raise ValueError('Expected regular pinned file')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def worker_digest():
    files={name:digest(Path(__file__).with_name(name)) for name in ('graspnet.py','graspnet_cpu_ops.py','graspnet_cpu.py')}
    return hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()



def verify_container_setup(path):
    digest(path);manifest=json.loads(Path(path).read_text())
    expected={'version','kind','isolation','image','checkpoint','checkpoint_sha256','revision','source_sha256','worker_sha256','image_manifest_sha256'}
    if (set(manifest)!=expected or manifest['version']!=1 or manifest['kind']!='graspnet_cpu_container'
            or manifest['isolation']!='docker' or not re.fullmatch('sha256:[0-9a-f]{64}',manifest['image'])
            or not re.fullmatch('[0-9a-f]{64}',manifest['image_manifest_sha256'])
            or manifest['checkpoint_sha256']!=graspnet.CHECKPOINT_SHA256
            or manifest['revision']!=graspnet.REVISION or manifest['source_sha256']!=graspnet.SOURCE_SHA256
            or manifest['worker_sha256']!=worker_digest() or digest(manifest['checkpoint'])!=graspnet.CHECKPOINT_SHA256):
        raise ValueError('Frozen CPU GraspNet setup changed')
    return manifest


def container_create_command(manifest,*,engine,preflight=False):
    checkpoint=manifest['checkpoint']
    if not Path(checkpoint).is_absolute() or any(c in checkpoint for c in (',','\n','\r','\0')):raise ValueError('Invalid checkpoint mount')
    uid=os.getuid() or 65532;gid=os.getgid() or 65532
    return engine.command('create','--interactive',*engine.create_options(),'--network','none','--read-only',
        '--user',f'{uid}:{gid}','--cap-drop','ALL','--security-opt','no-new-privileges',
        *engine.resource_options(memory='3g'),'--tmpfs','/tmp:rw,nosuid,nodev,size=268435456,mode=1777',
        '--env','HOME=/tmp','--env','OMP_NUM_THREADS=2','--env','OPENBLAS_NUM_THREADS=2',
        '--workdir','/tmp','--entrypoint','/usr/local/bin/python3',
        '--mount',f'type=bind,src={checkpoint},dst=/weights.tar,readonly',
        manifest['image'],'-I','-B','/opt/worker/worker.py','--preflight' if preflight else '--worker')


def freeze_container_setup(checkpoint,image,context,output):
    if not re.fullmatch('sha256:[0-9a-f]{64}',image):raise ValueError('Immutable image required')
    checkpoint=Path(checkpoint).absolute()
    if digest(checkpoint)!=graspnet.CHECKPOINT_SHA256:raise ValueError('Checkpoint mismatch')
    context=Path(context);image_manifest=context/'runtime/image-manifest.json'
    metadata=json.loads(image_manifest.read_text())
    if metadata['source_sha256']!=graspnet.SOURCE_SHA256 or metadata['worker_sha256']!=worker_digest():
        raise ValueError('Image source changed')
    for name,sha in metadata['files'].items():
        if digest(context/'runtime'/name)!=sha:raise ValueError('Image member changed')
    manifest=dict(version=1,kind='graspnet_cpu_container',isolation='docker',image=image,
        checkpoint=str(checkpoint),checkpoint_sha256=graspnet.CHECKPOINT_SHA256,
        revision=graspnet.REVISION,source_sha256=graspnet.SOURCE_SHA256,
        worker_sha256=worker_digest(),image_manifest_sha256=digest(image_manifest))
    with Path(output).open('x') as stream:json.dump(manifest,stream,indent=2,sort_keys=True);stream.write('\n')
    return manifest


def export_container_context(repository,output,archive,wheelhouse,requirements):
    """Copy only the pinned official inference source, adapter and offline wheels."""
    import shutil
    import zipfile
    if digest(archive)!=graspnet.SOURCE_SHA256:raise ValueError('Official source archive mismatch')
    repository=Path(repository);output=Path(output)
    output.mkdir(mode=0o700,parents=True,exist_ok=False);runtime=output/'runtime';runtime.mkdir()
    package=runtime/'agentbench_platform';package.mkdir()
    for name in ('__init__.py','graspnet.py','graspnet_cpu_ops.py','graspnet_cpu.py'):
        source=repository/'source/agentbench_platform/agentbench_platform'/name
        digest(source);shutil.copyfile(source,package/name)
    shutil.copyfile(repository/'scripts/agentbench_graspnet_cpu_worker.py',runtime/'worker.py')
    shutil.copyfile(repository/'tools/graspnet_cpu/THIRD_PARTY_NOTICES.txt',runtime/'THIRD_PARTY_NOTICES.txt')
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            rel=Path(*Path(member.filename).parts[1:])
            if member.is_dir() or not rel.parts:continue
            if rel.parts[0] not in ('models','utils','pointnet2') and rel!=Path('LICENSE'):continue
            if '..' in rel.parts or rel.is_absolute():raise ValueError('Unsafe archive member')
            if (rel.suffix!='.py' or rel.name=='setup.py') and rel.name!='LICENSE':continue
            target=runtime/'source'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(member))
    metadata=dict(version=1,source_sha256=graspnet.SOURCE_SHA256,worker_sha256=worker_digest(),
        files={str(p.relative_to(runtime)):digest(p) for p in sorted(runtime.rglob('*')) if p.is_file()})
    (runtime/'image-manifest.json').write_text(json.dumps(metadata,sort_keys=True,indent=2)+'\n')
    # The image runs as a non-root UID. A maintainer's private umask must not
    # turn the public, minimal payload into root-only files after COPY.
    for path in [runtime, *runtime.rglob('*')]:
        path.chmod(0o755 if path.is_dir() else 0o644)
    wheels=sorted(Path(wheelhouse).glob('*.whl'))
    if not wheels:raise ValueError('Prepare pinned offline CPU wheels first')
    (output/'wheels').mkdir()
    for source in wheels:digest(source);shutil.copyfile(source,output/'wheels'/source.name)
    digest(requirements);shutil.copyfile(requirements,output/'requirements.lock')
    shutil.copyfile(repository/'tools/graspnet_cpu/Dockerfile',output/'Dockerfile')
    shutil.copyfile(repository/'tools/graspnet_cpu/build.py',output/'build.py')
    return {str(p.relative_to(output)):dict(sha256=digest(p),bytes=p.stat().st_size)
        for p in sorted(output.rglob('*')) if p.is_file()}
