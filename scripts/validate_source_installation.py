#!/usr/bin/env python3
"""Verify a clean source checkout in an isolated backend interpreter; no distribution build."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
for name in ('agentbench','agentbench_platform','agentbench_sdk'):
    sys.path.insert(0,str(ROOT/'source'/name))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--backend',choices=['mujoco','maniskill'],default='mujoco')
    args=parser.parse_args()
    from agentbench_platform.environment_catalog import catalog
    from agentbench_platform.environment_backend import MarbleBackend
    from agentbench_platform.environment_release import inventory,evidence_identity
    import agentbench_platform,agentbench_sdk
    modules=[agentbench_platform,agentbench_sdk]
    if args.backend=='mujoco':
        import agentbench_mujoco
        modules.append(agentbench_mujoco)
    else:
        import agentbench_maniskill
        modules.append(agentbench_maniskill)
    manifest=catalog()
    report=dict(scope='clean_source_'+args.backend+'_installation',**evidence_identity(manifest,inventory()),
        run_status='running',status='failed',task_discovery_count=manifest['count'],tasks=[],
        native_backend_installation='not_executed',distribution_validation='not_executed')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    def save():
        temporary=args.output.with_suffix('.tmp');temporary.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');temporary.replace(args.output)
    try:
        opts=['git','-c','filter.lfs.process=','-c','filter.lfs.required=false','-C',str(ROOT)]
        state=subprocess.run(opts+['status','--porcelain'],capture_output=True,text=True,check=True).stdout
        assert not state,'Source checkout is not clean'
        report['checkout']=dict(path=str(ROOT),revision=subprocess.check_output(opts+['rev-parse','HEAD'],text=True).strip(),clean=True)
        assert sys.prefix!=sys.base_prefix,'Separate virtual environment required'
        configuration=Path(sys.prefix,'pyvenv.cfg').read_text().lower()
        assert 'include-system-site-packages = false' in configuration,'System packages are inherited'
        assert not list(Path(sys.prefix).glob('lib/python*/site-packages/*.egg-link')),'External editable dependency'
        report['runtime']=dict(python=sys.version,executable=sys.executable,packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()})
        pins=ROOT/('env/runtime/mujoco-constraints.txt' if args.backend=='mujoco' else 'env/maniskill_lgd/requirements-simulator.txt')
        for line in pins.read_text().splitlines():
            if not line or line.startswith('#'):continue
            name,version=line.split('==')
            assert importlib.metadata.version(name)==version, 'Dependency pin mismatch: '+name
        for module in modules:
            assert Path(module.__file__).resolve().is_relative_to(ROOT),'Module imported from another checkout'
        assert manifest['count']==410 and len({t['id'] for t in manifest['tasks']})==410
        for task in manifest['tasks']:
            if task['backend']!=args.backend:continue
            backend=None;row=dict(task_id=task['id'],configuration_sha256=task['configuration_sha256'],status='failed')
            try:
                if args.backend=='mujoco':backend=MarbleBackend(task)
                else:
                    from agentbench_platform.maniskill_backend import ManiSkillBackend
                    from agentbench_platform.resources import ResourceStore
                    backend=ManiSkillBackend(task,resources=ResourceStore(),render=False)
                description=backend.describe();before=backend.snapshot()
                after=backend.step(description['action_spec']['neutral_action'])
                assert after['physics_step_count']>before['physics_step_count']
                assert not after['terminated'] and not after['truncated']
                row.update(status='loaded_and_stepped',physics_steps=after['physics_step_count'])
                if not report['tasks'] and args.backend=='mujoco':
                    image=backend.env.render()
                    from OpenGL import GL
                    report['rendering']=dict(shape=list(image.shape),
                        vendor=GL.glGetString(GL.GL_VENDOR).decode(),
                        renderer=GL.glGetString(GL.GL_RENDERER).decode(),
                        version=GL.glGetString(GL.GL_VERSION).decode())
                assert not backend.finish().get('success',False)
            except Exception as exc:row.update(error=type(exc).__name__+': '+str(exc))
            finally:
                if backend is not None:backend.close()
            report['tasks'].append(row);save()
        assert len(report['tasks'])==(100 if args.backend=='mujoco' else 30) and all(r['status']=='loaded_and_stepped' for r in report['tasks'])
        # A separate process exercises rendering, the socket SDK and clean exit.
        representatives={}
        for task in manifest['tasks']:
            if task['backend']==args.backend:representatives.setdefault(task['embodiment'],task['id'])
        report['render_gateway']=[]
        for robot,task_id in representatives.items():
            smoke=args.output.with_name(args.output.stem+'-'+robot+'-render-gateway.json')
            command=[sys.executable,str(ROOT/'scripts/environment_smoke.py'),'--task-id',task_id,'--output',str(smoke)]
            run=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=360)
            record=dict(command=command,returncode=run.returncode,report=str(smoke))
            if run.returncode:record['diagnostic_tail']=(run.stdout+run.stderr)[-6000:]
            report['render_gateway'].append(record);save()
            assert run.returncode==0,'Rendering/gateway/clean-exit probe failed: '+robot
        report.update(status='passed_installation_probe',run_status='completed')
    except Exception as exc:
        import traceback
        report.update(run_status='failed',error=type(exc).__name__+': '+str(exc),failure_traceback=traceback.format_exc())
    save();print(args.output)
    return int(report['status']=='failed')


if __name__=='__main__':raise SystemExit(main())
