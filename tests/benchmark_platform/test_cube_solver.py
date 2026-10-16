"""Symbolic tools receive submitted facelets only and independently verify output."""
import pytest


def test_symbolic_tool_never_resolves_environment_capture():
    from agentbench_platform.cube_solver import descriptor
    from agentbench_platform.plugins import ToolRegistry
    class NoResources:
        def resolve_capture(self,*a):raise AssertionError('Symbolic tool read camera state')
    seen=[]
    def worker(payload):
        seen.append(payload)
        return dict(solution=[],version='1.1.4',search_timed_out=False,search_wall_s=0.)
    registry=ToolRegistry(resources=NoResources(),observation='rgb',granted=('cube_solver',))
    registry.register(descriptor('1'*64,'2'*64),worker)
    facelets=''.join(f*9 for f in 'URFDLB')
    assert registry.call('cube_solver',{'facelets_urfdlb':facelets})['solution']==[]
    assert seen==[{'arguments':{'facelets_urfdlb':facelets}}]
    with pytest.raises(ValueError):registry.call('cube_solver',{'capture_id':'secret'})
    assert len(seen)==1


def test_symbolic_output_replays_without_solver_or_native_state():
    from agentbench_platform.cube_solver import validate_solution,check_facelets
    from agentbench_platform.rubiks_physics import load_physics
    rules=load_physics().rules
    facelets=rules.CubeState.solved().apply_sequence(('R','U',"F'")).facelet_string()
    answer=dict(solution=['F',"U'","R'"],version='1.1.4',search_timed_out=False,search_wall_s=.01)
    validate_solution(answer,{'arguments':{'facelets_urfdlb':facelets}})
    with pytest.raises(ValueError):validate_solution(dict(answer,solution=['F','U','R']),{'arguments':{'facelets_urfdlb':facelets}})
    with pytest.raises(ValueError):check_facelets('U'*54)
    with pytest.raises(ValueError):check_facelets(facelets[:-1])


def test_offline_table_loader_refuses_missing_tables_without_generation(tmp_path):
    from types import SimpleNamespace
    from agentbench_platform.cube_solver import frozen_table_loader
    import numpy as np
    import hashlib
    directory=tmp_path/'tables';directory.mkdir()
    np.savez(directory/'example.npz',present=np.ones((2,3)))
    digest=hashlib.sha256((directory/'example.npz').read_bytes()).hexdigest()
    loader=frozen_table_loader(tmp_path,{'example.npz':digest})
    generate=lambda **kw:(_ for _ in ()).throw(AssertionError('Generated during episode'))
    assert loader('example.npz',[SimpleNamespace(name='present')],generate)['present'].shape==(2,3)
    with pytest.raises(ValueError):loader('example.npz',[SimpleNamespace(name='missing')],generate)
    with pytest.raises(ValueError):loader('../example.npz',[SimpleNamespace(name='present')],generate)
    (directory/'example.npz').write_bytes(b'changed')
    with pytest.raises(ValueError):loader('example.npz',[SimpleNamespace(name='present')],generate)


def test_explicit_solver_grant_can_be_disabled():
    from argparse import ArgumentParser
    from agentbench_platform.profile_cli import add_profile_arguments, profile_from_args
    from agentbench_platform.tasks import add_task_arguments
    parser=ArgumentParser();add_task_arguments(parser);add_profile_arguments(parser)
    args=parser.parse_args(['--task-family','rubiks_cube','--mode','solve','--profile','rgb','--tool','cube_solver'])
    assert profile_from_args(args,available_tools=['cube_solver'])['tools']==['cube_solver']
    with pytest.raises(ValueError,match='unavailable'):profile_from_args(args)
    args=parser.parse_args(['--task-family','rubiks_cube','--mode','solve','--disable-cube-solver'])
    assert profile_from_args(args)['tools']==[]
    args=parser.parse_args(['--mode','assemble'])
    assert profile_from_args(args)['tools']==[]
    args=parser.parse_args(['--task-family','rubiks_cube','--mode','solve','--tool','cube_solver','--disable-cube-solver'])
    with pytest.raises(ValueError):profile_from_args(args,available_tools=['cube_solver'])


@pytest.mark.parametrize('proc_mode', ['standard', 'empty'])
def test_container_solver_has_only_readonly_cache_and_explicit_engine(tmp_path, proc_mode):
    from agentbench_platform.cube_solver import container_create_command
    from agentbench_platform.container_engine import ContainerEngine
    conf=tmp_path/'storage.conf';conf.write_text('[storage]\ndriver="vfs"\n')
    engine=ContainerEngine('podman',storage_conf=conf,cgroups=False,proc_mode=proc_mode)
    manifest=dict(image='sha256:'+'3'*64,cache=str(tmp_path/'cache'))
    command=container_create_command(manifest,engine=engine)
    assert command[:len(engine.command('create'))]==engine.command('create')
    assert '--userns=keep-id' in command and '--cgroups=disabled' in command
    assert '--read-only' in command and command[command.index('--network')+1]=='none'
    assert command[command.index('--cap-drop')+1]=='ALL'
    assert command[command.index('--user')+1]!='0:0'
    mounts=[command[i+1] for i,v in enumerate(command) if v=='--mount']
    assert mounts==[f'type=bind,src={tmp_path}/cache,dst=/cache,readonly']
    assert not any('gpu' in item or '/dev/nvidia' in item for item in command)
    assert '--memory' not in command
    assert ('/proc:ro,nosuid,nodev,noexec,size=4k' in command) == (proc_mode == 'empty')
    assert command[-3:]==['/opt/worker/scripts/agentbench_cube_solver.py','--cache','/cache']


def test_cube_solver_setup_detects_changed_tables_before_worker(tmp_path):
    import hashlib,json
    from agentbench_platform.cube_solver import freeze_container_setup,verify_container_setup
    cache=tmp_path/'cache';(cache/'tables').mkdir(parents=True)
    tables={}
    for name in ('transition.npz','pruning_kociemba.npz'):
        path=cache/'tables'/name;path.write_bytes(name.encode());tables[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    frozen=dict(version=1,solver_version='1.1.4',source={'worker':'a'*64,'adapter':'b'*64},tables=tables)
    (cache/'setup.json').write_text(json.dumps(frozen))
    manifest=tmp_path/'tool.json'
    freeze_container_setup(cache,'sha256:'+'c'*64,manifest)
    verified=verify_container_setup(manifest)
    assert verified['cache']==str(cache) and verified['image']=='sha256:'+'c'*64
    (cache/'tables/transition.npz').write_bytes(b'changed')
    with pytest.raises(ValueError):verify_container_setup(manifest)


def test_configured_solver_uses_isolated_worker_and_independent_replay(tmp_path,monkeypatch):
    from argparse import Namespace
    import hashlib,json
    from agentbench_platform import cube_solver,plugins
    from agentbench_platform.container_engine import ContainerEngine
    cache=tmp_path/'cache';(cache/'tables').mkdir(parents=True)
    tables={}
    for name in ('transition.npz','pruning_kociemba.npz'):
        path=cache/'tables'/name;path.write_bytes(name.encode());tables[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    (cache/'setup.json').write_text(json.dumps(dict(version=1,solver_version='1.1.4',source={'worker':'a'*64,'adapter':'b'*64},tables=tables)))
    manifest=tmp_path/'tool.json'
    cube_solver.freeze_container_setup(cache,'sha256:'+'c'*64,manifest)
    seen=[]
    # Replace only the unavailable OS/container boundary. Registry validation,
    # source verification, schemas and independent replay remain real.
    class Boundary:
        def __init__(self,command,**kwargs):
            assert command[0]=='docker';assert isinstance(kwargs['engine'],ContainerEngine)
        def __call__(self,payload):
            seen.append(payload)
            return dict(solution=[],version='1.1.4',search_timed_out=False,search_wall_s=0.)
    monkeypatch.setattr(plugins,'DockerWorker',Boundary)
    args=Namespace(task_family='rubiks_cube',tool=['cube_solver'],disable_cube_solver=False,profile='rgb',cube_solver_setup=manifest,tool_setup=None)
    registry=plugins.configured_registry(args,resources=None,private_directory=tmp_path/'private')
    assert [x['name'] for x in registry.list()]==['cube_solver']
    assert registry.list()[0]['execution_contract']['isolation']=='docker'
    assert registry.call('cube_solver',{'facelets_urfdlb':cube_solver.SOLVED})['solution']==[]
    from agentbench_platform.rubiks_physics import load_physics
    unsolved=load_physics().rules.CubeState.solved().apply_sequence(('U',)).facelet_string()
    with pytest.raises(plugins.ToolFailure):registry.call('cube_solver',{'facelets_urfdlb':unsolved})
    assert all(set(p)=={'arguments'} for p in seen)


def test_symbolic_replay_does_not_import_native_physics_modules():
    import os,subprocess,sys
    from pathlib import Path
    code="""
import sys
from agentbench_platform.cube_solver import validate_solution,SOLVED
validate_solution(dict(version='1.1.4',solution=[]),{'arguments':{'facelets_urfdlb':SOLVED}})
assert not any('native_observation' in name or name.startswith(('isaac','omni','baselines')) for name in sys.modules)
"""
    result=subprocess.run([sys.executable,'-c',code],capture_output=True,text=True,env=dict(os.environ,PYTHONPATH=os.pathsep.join(str(Path(__file__).resolve().parents[2]/'source'/name) for name in ('agentbench_platform','agentbench'))))
    assert result.returncode==0,result.stderr


def test_solver_image_context_contains_only_worker_math_and_explicit_wheels(tmp_path):
    from pathlib import Path
    from agentbench_platform.cube_solver import export_container_context
    root=Path(__file__).resolve().parents[2]
    wheels=tmp_path/'wheels';wheels.mkdir();(wheels/'dependency.whl').write_bytes(b'pinned wheel')
    (wheels/'private-trajectory.json').write_text('secret')
    lock=tmp_path/'requirements.lock';lock.write_text('cube-solver==1.1.4 --hash=sha256:'+'a'*64+'\n')
    context=tmp_path/'context'
    files=export_container_context(root,context,wheels,lock)
    assert 'runtime/scripts/agentbench_cube_solver.py' in files
    assert 'wheels/dependency.whl' in files
    assert not any('trajectory' in name or 'baselines' in name or 'native_observation' in name for name in files)
    # The shipped subset must actually perform trusted symbolic replay, without
    # reaching back to this test's source checkout or importing Isaac.
    import subprocess,sys,os
    env=dict(os.environ,PYTHONPATH=os.pathsep.join(str(context/'runtime/source'/name) for name in ('agentbench_platform','agentbench')))
    code="from agentbench_platform.cube_solver import validate_solution,SOLVED; validate_solution(dict(version='1.1.4',solution=[]),{'arguments':{'facelets_urfdlb':SOLVED}})"
    result=subprocess.run([sys.executable,'-c',code],cwd=tmp_path,env=env,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
