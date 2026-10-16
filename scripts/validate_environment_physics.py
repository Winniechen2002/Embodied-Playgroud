#!/usr/bin/env python3
"""MuJoCo finite-action stability checks; no model or task completion run."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
ROOT=Path(__file__).resolve().parents[1]
for name in ('agentbench','agentbench_platform'):sys.path.insert(0,str(ROOT/'source'/name))


def check(task,seed,mode,stiffness,hold,required=None):
    import numpy as np
    import mujoco
    from agentbench_platform.environment_backend import MarbleBackend
    from agentbench_platform.environment_conditions import effective_condition
    from agentbench_platform.environment_qa import marble_readback, gateway_probe, lifecycle_probe, contract_probe, local_action_probe
    import tempfile
    condition=required['condition'] if required else effective_condition(task,seed=seed,initial_mode=mode,parameters=dict(spring_stiffness=stiffness))
    backend=MarbleBackend(task,seed=seed,initial_mode=mode,environment_parameters=condition['environment_parameters'])
    e=backend.env;action=e.last_action.tolist();baseline=None;peak=0.;depth=0.;error=None
    start=time.monotonic();tracked=sorted(set(e.block_ids))
    initial=e.data.xpos[tracked].copy();checks={};measurements={};actual=None
    try:
        actual,measurements['initialization']=marble_readback(backend,condition)
        measurements['contract']=contract_probe(backend,task);checks['contract']='passed'
        from agentbench_platform.scorer_fixtures import marble_fixture
        measurements['scorer_endpoint']=marble_fixture(e,task)
        with tempfile.TemporaryDirectory(prefix='ab-gateway-qa-') as directory:
            measurements.update(gateway_probe(backend,directory))
        checks.update({k:'passed' for k in measurements if k.startswith('gateway_')})
        twin=MarbleBackend(task,seed=seed,initial_mode=mode,environment_parameters=condition['environment_parameters'])
        try:
            repeat_error=float(np.max(np.abs(twin.env.data.qpos-e.data.qpos)))
            assert repeat_error<=1e-10, 'Repeated initialization outside declared 1e-10 tolerance'
            measurements['repeat_initialization']=dict(maximum_qpos_error=repeat_error,tolerance=1e-10)
            checks['repeat_initialization']='passed'
            measurements['action_observation']=local_action_probe(twin)
            checks['action_observation']='passed'
            with tempfile.TemporaryDirectory(prefix='ab-lifecycle-qa-') as directory:
                measurements['lifecycle']=lifecycle_probe(twin,directory)
            checks['lifecycle']='passed'
        finally:twin.close()
        seconds=max(hold+2,e.max_seconds if task.get('full_horizon_stability') else hold+2)
        count=round(seconds/(e.physics_dt*e.decimation))
        for step in range(count):
            snapshot=backend.step(action)
            if step+1==round(2/(e.physics_dt*e.decimation)):
                baseline=e.data.xpos[tracked].copy()
                if float(np.linalg.norm(baseline-initial,axis=1).max(initial=0))>.003:
                    raise ValueError('Initial structure changed by more than 3 mm during settling')
            if baseline is not None:
                peak=max(peak,float(np.linalg.norm(e.data.xpos[tracked]-baseline,axis=1).max(initial=0)))
            if not np.isfinite(e.data.qpos).all() or not np.isfinite(e.data.qvel).all():raise ValueError('Nonfinite physics')
            for contact in e.data.contact:
                bodies={int(e.model.geom_bodyid[contact.geom1]),int(e.model.geom_bodyid[contact.geom2])}
                if bodies&set(tracked):depth=max(depth,max(0.,-float(contact.dist)))
            if snapshot['terminated']:raise ValueError('Unexpected no-action termination')
            if snapshot['truncated'] and step+1<count:raise ValueError('Unexpected early truncation')
        if peak>.003:raise ValueError('Structure drift exceeds 3 mm')
        if depth>.002:raise ValueError('Structure contact depth exceeds 2 mm')
        checks['physics']='passed'
        measurements['physics']=dict(maximum_structure_drift_m=peak,maximum_structure_contact_depth_m=depth,
            drift_limit_m=.003,contact_limit_m=.002)
    except Exception as exc:error=type(exc).__name__+': '+str(exc)
    finally:
        row=dict(task_id=task['id'],seed=seed,initial_mode=mode,spring_stiffness=stiffness,
            status='failed' if error else 'passed_probe',scope='structure_stability_gateway_repeat_initialization',
            condition=condition,actual_initialization=actual,checks=checks,measurements=measurements,hold_seconds=max(0.,float(e.data.time)-2),
            configuration_sha256=task['configuration_sha256'],
            physics_steps=backend.physics_steps,settle_seconds=2.,simulation_seconds=float(e.data.time),
            no_operation_seconds=float(e.data.time),episode_time_limit_seconds=e.max_seconds,
            initial_structure_positions_m=initial.tolist(),
            final_structure_positions_m=e.data.xpos[tracked].tolist(),
            maximum_structure_drift_m=peak,maximum_structure_contact_depth_m=depth,
            runtime=dict(python=sys.version,mujoco=mujoco.__version__,numpy=np.__version__),
            elapsed_seconds=time.monotonic()-start,error=error)
        backend.close()
    return row


def checked(arguments):
    task,*rest=arguments
    try:return check(task,*rest)
    except Exception as exc:return dict(task_id=task['id'],status='failed',error=type(exc).__name__+': '+str(exc))


def main():
    from agentbench_platform.environment_catalog import catalog
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--task-id',action='append');p.add_argument('--seed',type=int,default=0)
    p.add_argument('--initial-mode',choices=['loaded','ground'],default='loaded')
    p.add_argument('--spring-stiffness',type=float,choices=[22,24,26,28],default=22.)
    p.add_argument('--hold',type=float,default=3.);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--workers',type=int,default=1)
    p.add_argument('--list-conditions',action='store_true',help='Write the selected schedule without running physics')
    p.add_argument('--resume',action='store_true',help='Resume only when source and catalog digests exactly match')
    args=p.parse_args()
    if not 3<=args.hold< float('inf') or args.seed<0 or not 1<=args.workers<=16:
        p.error('hold >= 3, seed >= 0, and workers in 1..16 required')
    tasks=[t for t in catalog()['tasks'] if t['backend']=='mujoco' and (not args.task_id or t['id'] in args.task_id)]
    if args.task_id and {t['id'] for t in tasks}!=set(args.task_id):p.error('This checker requires MuJoCo task IDs')
    from agentbench_platform.environment_release import inventory
    from agentbench_platform.environment_catalog import digest
    rows=[];args.output.parent.mkdir(parents=True,exist_ok=True)
    from agentbench_platform.environment_conditions import condition_case
    from agentbench_platform.environment_release import evidence_identity
    identity=evidence_identity(catalog(),inventory())
    by_id={t['id']:t for t in tasks}
    required=[condition_case(task,seed=args.seed,initial_mode=args.initial_mode,
        parameters=dict(spring_stiffness=args.spring_stiffness)) for task in tasks]
    if args.list_conditions:
        args.output.write_text(json.dumps(dict(**identity,conditions=required),indent=2)+'\n')
        return
    work=[(by_id[r['task_id']],r['condition']['seed'],r['condition']['initial_mode'],
        r['condition']['environment_parameters']['spring_stiffness'],args.hold,r) for r in required]
    history=[]
    execution=dict(hold_seconds=args.hold,selected_keys=sorted(r['key'] for r in required))
    if args.resume and args.output.exists():
        previous=json.loads(args.output.read_text())
        if any(previous.get(k)!=v for k,v in identity.items()) or previous.get('execution')!=execution:
            p.error('Cannot resume changed source, catalog or execution conditions; use a new report path')
        if len({r['key'] for r in previous['cases']})!=len(previous['cases']):
            p.error('Duplicate condition evidence')
        if {r['key'] for r in previous['cases']}-{r['key'] for r in required}:
            p.error('Unknown condition evidence')
        history=previous.get('attempt_history',[])+[r for r in previous['cases'] if r['status']=='failed']
        rows=[r for r in previous['cases'] if r['status']=='passed_probe']
        complete={r['key'] for r in rows}
        work=[w for w in work if w[-1]['key'] not in complete]
    expected_cases=len(rows)+len(work)
    report=dict(scope='environment_physics_only',**identity,expected_cases=expected_cases,
        cases=rows,attempt_history=history,execution=execution,run_status='running')
    def save():
        temp=args.output.with_suffix('.tmp')
        temp.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
        temp.replace(args.output)
    save()
    pool=ProcessPoolExecutor(max_workers=args.workers)
    try:
        pending={pool.submit(checked,w):w for w in work}
        for future in as_completed(pending):
            row=future.result()
            _,seed,mode,stiffness,_,required=pending[future]
            row.update(key=required['key'],versions=identity,
                seed=seed,initial_mode=mode,spring_stiffness=stiffness)
            rows.append(row)
            save()
            print(row['task_id'],row['status'],row.get('error') or '',flush=True)
    except BaseException:
        report['run_status']='interrupted';save()
        pool.shutdown(wait=False,cancel_futures=True)
        raise
    else:
        pool.shutdown()
        report['run_status']='failed' if any(r['status']!='passed_probe' for r in rows) else 'completed'
        save()
    raise SystemExit(any(r['status']!='passed_probe' for r in rows))


if __name__=='__main__':main()
