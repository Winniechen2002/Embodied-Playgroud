#!/usr/bin/env python3
"""Finite-action environment/gateway probe. No model, solver or completion run."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
ROOT=Path(__file__).resolve().parents[1]
for name in ('agentbench_platform','agentbench_sdk'):
    sys.path.insert(0,str(ROOT/'source'/name))


def hold_action(description,observation):
    spec=description['action_spec'];family=description['task']['family']
    if 'neutral_action' in spec:
        action=spec['neutral_action']
        import math
        if len(action)!=spec['size'] or any(not math.isfinite(v) or lo is not None and v<lo or hi is not None and v>hi for v,lo,hi in zip(action,spec['low'],spec['high'])):
            raise ValueError('Invalid declared neutral action')
        return action
    if family=='marble':
        from agentbench_mujoco.scene import HOME
        return list(HOME)+[1.]+list(HOME)+[1.]
    if description['task'].get('embodiment')=='floating-sharpa':
        robot=description['robots']['floating_sharpa']
        positions=dict(zip(robot['joint_names'],robot['default_joint_positions']))
        return [positions[n.removeprefix('sharpa.')] for n in spec['names']]
    result=[]
    for i,(lo,hi) in enumerate(zip(spec['low'],spec['high'])):
        name=spec.get('names',['']*spec['size'])[i]
        result.append(min(hi,max(lo,1. if name.endswith('gripper') else 0.)))
    return result


def run(args):
    from agentbench_platform.environment_catalog import find_task
    from agentbench_sdk import Client
    from agentbench_sdk.client import ProtocolError
    task=find_task(args.task_id)
    report=dict(schema_version=1,scope='environment_probe_only',task_id=args.task_id,seed=args.seed,
        capability_level=args.capability_level,checks={},runtime=dict(python=sys.version),physics_steps=0)
    with tempfile.TemporaryDirectory(prefix='ab-env-probe-') as tmp:
        output=Path(tmp)/'episode'
        command=[sys.executable,str(ROOT/'scripts/environment_runtime.py'),'--task-id',args.task_id,
            '--capability-level',str(args.capability_level),'--seed',str(args.seed),'--headless',
            '--wall-seconds',str(args.timeout),'--output',str(output),'--initial-mode',args.initial_mode,
            '--spring-stiffness',str(args.spring_stiffness)]
        log=open(Path(tmp)/'runtime.log','w+')
        process=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,cwd=ROOT)
        deadline=time.monotonic()+args.timeout
        client=None
        try:
            while not (output/'session.json').exists() and not (output/'ready.json').exists():
                if process.poll() is not None:raise RuntimeError('Environment startup failed')
                if time.monotonic()>deadline:raise TimeoutError('Environment startup timed out')
                time.sleep(.1)
            if (output/'session.json').exists():session=json.loads((output/'session.json').read_text())
            else:
                ready=json.loads((output/'ready.json').read_text())
                session=dict(socket_path=ready['socket'],native_token=(output/'public/token').read_text().strip())
            client=Client(session['socket_path'],session['native_token'],timeout=60)
            desc=client.describe();before=client.observe()
            assert desc['profile']['capability_level']==args.capability_level
            # Denied methods must never change the clock or state.
            for method in ('reset','set_state','set_seed'):
                try:client._call(method,{})
                except ProtocolError as exc:assert exc.code=='unsupported_method'
                else:raise AssertionError('Forbidden state mutation accepted')
            after=client.observe()
            assert before==after
            assert ('privileged' in before)==(args.capability_level==3)
            if args.capability_level==0:assert client.tools.list()=={'tools':[]}
            for ident in ('../scene.usda','/etc/passwd','unknown-resource'):
                try:client.get_resource(ident)
                except ProtocolError as exc:assert exc.code=='resource_unavailable'
                else:raise AssertionError('Unregistered resource accepted')
            views=list(desc['cameras'])
            assert views,'No public camera'
            obs=client.observe(camera_ids=[views[0]])
            resource=client.get_resource(obs['cameras'][views[0]]['rgb_resource_id'])
            assert resource['byte_length']>0 and resource['sha256']
            assert obs['simulation_time_s']==before['simulation_time_s']
            report['checks']['gateway_l'+str(args.capability_level)]='passed'
            action=hold_action(desc,obs)
            first=client.step(action,request_id='probe-first-step')
            assert client.step(action,request_id='probe-first-step')==first
            snapshot=first['observation']
            assert snapshot['step_index']==before['step_index']+1
            dt=snapshot['simulation_time_s']-before['simulation_time_s']
            assert dt>0
            steps=max(1,int((args.settle+args.hold)/dt+.999))
            for _ in range(1,steps):
                if snapshot['terminated'] or snapshot['truncated']:raise RuntimeError('Unexpected early environment terminal')
                snapshot=client.step(action)['observation']
            report.update(control_steps=snapshot['step_index'],simulation_seconds=snapshot['simulation_time_s'],
                physics_steps=snapshot['physics_step_count'],settle_seconds=args.settle,hold_seconds=args.hold)
            report['checks']['finite_action_clock']='passed'
            if args.mechanism_probe:
                assert task['family'] in ('rubiks_panda','rubiks_sharpa')
                assert desc.get('mechanism'), 'Declared cube mechanism is missing'
                before_mechanism=client.observe()
                try:client.mechanism.command('set_state',{})
                except ProtocolError:pass
                else:raise AssertionError('Undeclared mechanism command accepted')
                assert client.observe()==before_mechanism
                accepted=client.mechanism.command('turn.begin',{'move':'U'},request_id='probe-mechanism')
                assert accepted['accepted'] is True, accepted
                assert client.mechanism.command('turn.begin',{'move':'U'},request_id='probe-mechanism')==accepted
                after_mechanism=client.observe()
                assert after_mechanism['simulation_time_s']==before_mechanism['simulation_time_s']
                assert after_mechanism['physics_step_count']==before_mechanism['physics_step_count']
                try:denied=client.mechanism.command('turn.end',{})
                except ProtocolError:pass
                else:assert denied['accepted'] is False, 'Unmeasured quarter turn accepted'
                assert client.observe()==after_mechanism
                report['checks']['declared_mechanism_boundary']='passed'
            # These probes alone do not certify collision coverage, drift limits,
            # scoring or local manipulation; do not label the full physics gate passed.
            result=client.finish();assert client.finish()==result
            try:client.step(action)
            except ProtocolError as exc:assert exc.code=='episode_closed'
            else:raise AssertionError('Physical action after finish accepted')
            report['checks']['lifecycle']='passed'
            report['status']='passed_probe'
        except Exception as exc:
            report.update(status='failed',error=type(exc).__name__+': '+str(exc))
        finally:
            if client:
                try:client.finish()
                except Exception:pass
                client.close()
            forced_shutdown=False
            try:process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                forced_shutdown=True
                process.terminate()
                try:process.wait(timeout=5)
                except subprocess.TimeoutExpired:process.kill();process.wait()
            if report.get('status')=='passed_probe' and (forced_shutdown or process.returncode!=0):
                report.update(status='failed',error='Runtime did not exit cleanly after finish')
                report['checks']['lifecycle']='failed'
            report['runtime_exit_code']=process.returncode
            report['forced_shutdown']=forced_shutdown
            log.seek(0)
            # Native diagnostics remain outside the distribution and contain no model calls.
            report['diagnostic_tail']=log.read()[-4000:] if report.get('status')=='failed' else ''
            log.close()
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--task-id',required=True);p.add_argument('--seed',type=int,default=0)
    p.add_argument('--capability-level',type=int,choices=range(4),default=0)
    p.add_argument('--initial-mode',choices=['loaded','ground'],default='loaded')
    p.add_argument('--spring-stiffness',type=float,choices=[22,24,26,28],default=22.)
    p.add_argument('--settle',type=float,default=2.);p.add_argument('--hold',type=float,default=3.)
    p.add_argument('--timeout',type=float,default=300.);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--mechanism-probe',action='store_true')
    args=p.parse_args()
    if args.settle<2 or args.hold<3 or args.seed<0 or not 0<args.timeout<float('inf'):p.error('Invalid probe limits')
    result=run(args);args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('task_id','status','checks')}))
    if result['status']=='failed':raise SystemExit(1)


if __name__=='__main__':main()
