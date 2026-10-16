"""Trusted offline builds own one disposable container; never an ambient name."""
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace

import pytest


@pytest.mark.parametrize('failure', [None, 'cp', 'start', 'timeout', 'ownership'])
def test_proc_less_build_seals_output_and_cleans_only_verified_container(tmp_path, monkeypatch, failure):
    from agentbench_platform.image_build import build_image
    from agentbench_platform.container_engine import ContainerEngine
    engine=ContainerEngine('podman',cgroups=False,proc_mode='empty')
    context=tmp_path/'context';context.mkdir();(context/'build.py').write_text('print("setup")')
    output=tmp_path/'output';output.mkdir()
    cid='a'*64;image='sha256:'+'b'*64;name=None;removed=False;calls=[]

    def external(command, **kwargs):
        nonlocal name,removed
        verb,*args=command[len(engine.command()):];calls.append((verb,args))
        stdout='';code=0
        if verb=='create':
            name=args[args.index('--name')+1]
            Path(args[args.index('--cidfile')+1]).write_text(cid)
            assert '--network=none' in args and '--pid=private' in args
            assert '--cap-drop=ALL' in args and '--security-opt=no-new-privileges' in args
            assert '/proc:ro,nosuid,nodev,noexec,size=4k' in args
            assert not any(a in args for a in ('--privileged','--pid=host','--network=host','--mount'))
            assert args[-3:]==['-I','-B','/build/build.py']
            stdout=cid+'\n'
        elif verb=='inspect':
            assert args==[cid]
            if removed:code=1
            else:stdout=json.dumps([dict(Id=cid,Name='unrelated' if failure=='ownership' else name,State=dict(Running=False))])
        elif verb=='container':
            assert args==['ls','--all','--no-trunc','--quiet','--filter','id='+cid]
        elif verb=='cp':
            assert args==[str(context),cid+':/build']
            if failure=='cp':code=1
        elif verb=='start':
            assert args==['--attach',cid]
            if failure=='start':code=1
            if failure=='timeout':raise subprocess.TimeoutExpired(command,600,output=b'partial setup log',stderr=b'partial setup error')
        elif verb=='commit':
            assert args[-1]==cid and 'USER 65532:65532' in args
            assert 'ENTRYPOINT ["/usr/local/bin/python3", "-I", "/opt/worker.py"]' in args
            stdout=image.removeprefix('sha256:')+'\n'
        elif verb=='image':
            assert args==['inspect',image]
            stdout=json.dumps([dict(Id=image,Config=dict(User='65532:65532',WorkingDir='/tmp',Entrypoint=['/usr/local/bin/python3','-I','/opt/worker.py']))])
        else:
            assert verb in ('stop','rm') and args[-1]==cid
            if verb=='rm':removed=True
        return SimpleNamespace(returncode=code,stdout=stdout,stderr='build-progress-stderr')

    monkeypatch.setattr(subprocess,'run',external)
    kwargs=dict(engine=engine,context=context,output=output,base_image='python@sha256:'+'c'*64,
                entrypoint=['/usr/local/bin/python3','-I','/opt/worker.py'])
    if failure:
        with pytest.raises((RuntimeError,subprocess.CalledProcessError,subprocess.TimeoutExpired)):
            build_image(**kwargs)
        assert not (output/'image.id').exists()
    else:
        assert build_image(**kwargs)==image
        assert (output/'image.id').read_text().strip()==image
    assert removed == (failure!='ownership')
    if failure=='ownership':assert not any(v in ('cp','start','commit','stop','rm') for v,_ in calls)
    report=json.loads((output/'build-report.json').read_text())
    assert report['complete'] == (failure is None)
    assert report['engine']['proc_mode']=='empty'
    assert report['files']['build.py']['bytes']==len('print("setup")')
    if failure=='timeout':
        assert (output/'prepare.stdout').read_text()=='partial setup log'
        assert (output/'prepare.stderr').read_text()=='partial setup error'


def test_builder_refuses_symlink_context_before_creating_container(tmp_path, monkeypatch):
    from agentbench_platform.image_build import build_image
    from agentbench_platform.container_engine import ContainerEngine
    context=tmp_path/'context';context.mkdir()
    private=tmp_path/'private';private.write_text('not an image input')
    (context/'build.py').symlink_to(private)
    monkeypatch.setattr(subprocess,'run',lambda *a,**k:pytest.fail('Unsafe context reached engine'))
    with pytest.raises(ValueError):
        build_image(engine=ContainerEngine('podman',proc_mode='empty'),context=context,output=tmp_path,
                    base_image='python@sha256:'+'c'*64,entrypoint=['/usr/local/bin/python3'])
