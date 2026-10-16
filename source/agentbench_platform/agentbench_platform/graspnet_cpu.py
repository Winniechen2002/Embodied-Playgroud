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
