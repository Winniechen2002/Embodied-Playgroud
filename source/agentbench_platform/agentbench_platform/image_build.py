"""Offline maintainer builds; never callable by an episode or untrusted agent.

Both paths execute the context's build.py. The explicit empty-proc deployment
uses one private build container because older Buildah mounts procfs before RUN.
Only this disposable image root is writable/root-owned during preparation.
Final images have a non-root default user; runtime isolation is unchanged.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
import uuid

from .owned_container import OwnedContainer


def build_image(*, engine, context, output, base_image, entrypoint, workdir='/tmp'):
    context=Path(context).absolute();output=Path(output).absolute()
    if not re.fullmatch(r'python@sha256:[0-9a-f]{64}',base_image):
        raise ValueError('Immutable official Python base required')
    if (context.is_symlink() or not context.is_dir() or not isinstance(entrypoint,list)
            or not entrypoint or any(not isinstance(x,str) or not x or '\0' in x for x in entrypoint)
            or not isinstance(workdir,str) or not workdir.startswith('/') or '\n' in workdir):
        raise ValueError('Invalid build inputs')
    files={}
    for path in sorted(context.rglob('*')):
        if path.is_symlink() or not (path.is_dir() or path.is_file()):
            raise ValueError('Only regular image inputs are allowed')
        if path.is_file():
            files[str(path.relative_to(context))]=dict(bytes=path.stat().st_size,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    if 'build.py' not in files:raise ValueError('Missing image preparation script')
    base=('docker.io/library/' if engine.kind=='podman' else '')+base_image
    report=dict(complete=False,engine=engine.manifest(),base_image=base,files=files,
                method='private_build_container' if engine.proc_mode=='empty' else 'dockerfile',commands=[])
    started=time.monotonic();owner=None;image=None
    name='agentbench-build-'+uuid.uuid4().hex;cidfile=output/'build-container.id'

    def record(component,code,**details):
        report.setdefault('cleanup_errors',[]).append(dict(component=component,code=code,**details))

    def command(stage,args,timeout=600):
        argv=engine.command(*args);report['commands'].append(dict(stage=stage,argv=argv))
        try:
            result=subprocess.run(argv,capture_output=True,text=True,timeout=timeout,check=False)
        except subprocess.TimeoutExpired as error:
            for suffix,data in (('stdout',error.stdout),('stderr',error.stderr)):
                text=data.decode(errors='replace') if isinstance(data,bytes) else (data or '')
                (output/(stage+'.'+suffix)).write_text(text)
            raise
        (output/(stage+'.stdout')).write_text(result.stdout)
        (output/(stage+'.stderr')).write_text(result.stderr)
        if result.returncode:
            raise subprocess.CalledProcessError(result.returncode,argv,result.stdout,result.stderr)
        return result.stdout.strip()

    def get_owner():
        if not cidfile.exists():return None
        return OwnedContainer(cidfile.read_text().strip(),name,engine=engine,record=record,
                              inspection_path=output/'build-container-inspect.json')

    try:
        if engine.proc_mode=='standard':
            with (output/'build.log').open('w') as log:
                argv=engine.command('build','--network=none','--build-arg','BASE_IMAGE='+base,
                                    '--iidfile',str(output/'image.id'),str(context))
                report['commands'].append(dict(stage='dockerfile',argv=argv))
                subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,timeout=600,check=True)
            image=(output/'image.id').read_text().strip()
        else:
            command('create',['create',*engine.create_options(),'--name',name,'--cidfile',str(cidfile),
                '--network=none','--pid=private','--ipc=private','--user','0:0',
                '--cap-drop=ALL','--security-opt=no-new-privileges',*engine.resource_options(),
                '--env','OMP_NUM_THREADS=2','--env','OPENBLAS_NUM_THREADS=2',
                '--entrypoint','/usr/local/bin/python3',base,'-I','-B','/build/build.py'])
            owner=get_owner()
            if owner is None or owner._inspect()!='owned':raise RuntimeError('Build container ownership unverified')
            command('copy',['cp',str(context),owner.cid+':/build'])
            command('prepare',['start','--attach',owner.cid])
            raw=command('commit',['commit','--change','USER 65532:65532','--change','WORKDIR '+workdir,
                        '--change','ENTRYPOINT '+json.dumps(entrypoint),owner.cid])
            image=raw if raw.startswith('sha256:') else 'sha256:'+raw
            if not re.fullmatch(r'sha256:[0-9a-f]{64}',image):raise RuntimeError('Invalid committed image ID')
            rows=json.loads(command('image-inspect',['image','inspect',image]))
            if (len(rows)!=1 or rows[0].get('Id','').removeprefix('sha256:')!=image.removeprefix('sha256:')
                    or rows[0].get('Config',{}).get('User')!='65532:65532'
                    or rows[0]['Config'].get('WorkingDir')!=workdir
                    or rows[0]['Config'].get('Entrypoint')!=entrypoint):
                raise RuntimeError('Committed image configuration mismatch')
        if not re.fullmatch(r'sha256:[0-9a-f]{64}',image):raise RuntimeError('Invalid image ID')
        report['image']=image
    except BaseException as error:
        report['error']=dict(type=type(error).__name__,message=str(error))
        raise
    finally:
        if engine.proc_mode=='empty':
            try:
                owner=owner or get_owner()
                if owner is not None:
                    owner.stop()
                    report['cleanup']=owner.remove()
                else:report['cleanup']='no_container_id'
            except Exception as error:
                record('build_cleanup','exception',type=type(error).__name__)
        report['complete']=('image' in report and 'error' not in report and not report.get('cleanup_errors')
                            and (engine.proc_mode=='standard' or report.get('cleanup') in ('removed','absent')))
        report['elapsed_seconds']=time.monotonic()-started
        (output/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
    if not report['complete']:raise RuntimeError('Image built but owned-container cleanup is unresolved')
    (output/'image.id').write_text(image+'\n')
    return image
