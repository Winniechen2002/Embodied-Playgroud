#!/usr/bin/env python3
"""Maintainer-only native ManiSkill measurements; missing checks never qualify."""
import argparse
import importlib.metadata
import json
import math
import platform
from pathlib import Path
import sys
import tempfile
import time
ROOT=Path(__file__).resolve().parents[1]
for path in ('source/agentbench_platform','source/agentbench_sdk','env/maniskill_lgd'):
    sys.path.insert(0,str(ROOT/path))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task-id',action='append')
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--capture-contracts',action='store_true')
    parser.add_argument('--default-configurations',action='store_true',help='Seed 0, nominal lighting and physics for each selected task')
    parser.add_argument('--probe-only',action='store_true',help='Explicit five-second diagnostic; never full-horizon qualification')
    parser.add_argument('--list-conditions',action='store_true')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--no-render',action='store_true',help='Physics diagnostic only; cannot satisfy observation/render checks')
    args=parser.parse_args()
    import numpy as np
    from agentbench_platform.environment_catalog import catalog
    from agentbench_platform.environment_conditions import condition_case
    from agentbench_platform.environment_release import inventory,evidence_identity
    from agentbench_platform.maniskill_backend import ManiSkillBackend
    from agentbench_platform.resources import ResourceStore
    from agentbench_platform.environment_qa import gateway_probe,lifecycle_probe,repeat_measurement,structure_displacement,contract_probe,local_action_probe
    manifest=catalog(_native_records={} if args.capture_contracts else None)
    tasks={t['id']:t for t in manifest['tasks'] if t['backend']=='maniskill' and (not args.task_id or t['id'] in args.task_id)}
    if not tasks or args.task_id and set(args.task_id)!=set(tasks):parser.error('Unknown ManiSkill task')
    rows=[condition_case(task) for task in tasks.values()]
    if args.list_conditions:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(rows,indent=2)+'\n');return 0
    sources=inventory();identity=evidence_identity(manifest,sources)
    report=dict(scope='maniskill_native_engineering',run_status='running',expected_cases=len(rows),source_manifest=sources,
        **identity,execution=dict(capture_contracts=args.capture_contracts,no_render=args.no_render,
            probe_only=args.probe_only,default_configurations=True,selected_keys=[r['key'] for r in rows]),
        runtime=dict(python=sys.version,platform=platform.platform(),packages={name:importlib.metadata.version(name)
            for name in ('mani-skill-nightly','sapien','torch','numpy','scipy','gymnasium','trimesh','Pillow')}),cases=[])
    if args.resume and args.output.exists():
        old=json.loads(args.output.read_text())
        if any(old.get(k)!=v for k,v in identity.items()) or old.get('execution')!=report['execution']:parser.error('Stale resume evidence')
        keys=[r['key'] for r in old['cases']]
        if len(keys)!=len(set(keys)) or set(keys)-set(report['execution']['selected_keys']):parser.error('Duplicate or unknown evidence')
        report['attempt_history']=old.get('attempt_history',[])+[r for r in old['cases'] if r['status']=='failed']
        report['cases']=[r for r in old['cases'] if r['status']!='failed']
    done={r['key'] for r in report['cases']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    def save():
        temp=args.output.with_suffix('.tmp');temp.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');temp.replace(args.output)
    save()
    try:
        for required in rows:
            if required['key'] in done:continue
            task=tasks[required['task_id']];condition=required['condition'];backend=None
            row=dict(required,status='failed',versions=identity,measurements={},checks={},physics_steps=0)
            try:
                with tempfile.TemporaryDirectory(prefix='ab-maniskill-qa-') as temp:
                    def create():return ManiSkillBackend(task,resources=ResourceStore(),seed=condition['seed'],
                        parameters=condition['environment_parameters'],render=not args.no_render)
                    backend=create();initial=backend.snapshot()
                    row['native_description']=backend.describe()
                    from agentbench_maniskill.common.evaluation import lighting_parameters
                    row['actual_initialization']=dict(condition,environment_parameters=dict(
                        authored_light_scale=backend.e.light_scale,physics_variant=backend.e.task.get('physics_variant',0)))
                    readback=backend.initialization_readback()
                    assert readback['seed']==condition['seed']
                    assert readback['physics_variant']==condition['environment_parameters']['physics_variant']
                    if not args.no_render:
                        expected=lighting_parameters(condition['environment_parameters']['authored_light_scale'])
                        assert np.allclose(readback['lighting']['ambient'],expected['ambient'],rtol=1e-6,atol=1e-7)
                        assert np.allclose(readback['lighting']['directional'],expected['directional'],rtol=1e-6,atol=1e-7)
                        camera=backend.snapshot(('scene',))['cameras']['scene']
                        row['measurements']['camera']=camera
                    row['measurements']['initialization']=readback
                    if not args.capture_contracts:
                        row['measurements']['contract']=contract_probe(backend,task);row['checks']['contract']='passed'
                        if not args.no_render:
                            row['measurements'].update(gateway_probe(backend,Path(temp)/'gateway'))
                            for level in range(4):row['checks']['gateway_l'+str(level)]='passed'
                        if required['physics_acceptance']=='static_stability':
                            row['measurements']['action_observation']=local_action_probe(backend)
                            row['checks']['action_observation']='passed'
                            backend.close();backend=create()
                        row['measurements']['lifecycle']=lifecycle_probe(backend,Path(temp)/'lifecycle');row['checks']['lifecycle']='passed'
                        backend.close();backend=create()
                        row['measurements']['repeat_initialization']=repeat_measurement(initial,backend.snapshot());row['checks']['repeat_initialization']='passed'
                    duration=5. if args.capture_contracts or args.probe_only or required['physics_acceptance']=='expected_dynamics' else required['episode_time_limit_seconds']
                    initial_positions={n:v['position'] for n,v in backend.snapshot()['privileged']['pieces'].items()}
                    baseline=None;peak=0.;initial_drift=0.;terminal=None
                    for i in range(math.ceil(duration*20)):
                        if backend.terminated or backend.truncated:
                            terminal=dict(step=backend.steps,result=backend.finish());break
                        observed=backend.step(backend.action_spec['neutral_action'])
                        assert all(np.isfinite(v).all() for v in backend._physical_arrays()),'Nonfinite physical state'
                        if required['physics_acceptance']=='static_stability':
                            positions={n:v['position'] for n,v in observed['privileged']['pieces'].items()}
                            if i+1==40:
                                baseline=positions;initial_drift=structure_displacement(initial_positions,positions) if positions else 0.
                                assert initial_drift<=.003,'Initial structure drift exceeds 3 mm'
                            if baseline is not None:
                                peak=max(peak,structure_displacement(baseline,positions) if positions else 0.)
                                assert peak<=.003,'Support structure drift exceeds 3 mm'
                    observed=backend.snapshot();row['physics_steps']=observed['physics_step_count']
                    if args.capture_contracts:
                        assert row['physics_steps']>0,'No physics measured'
                    elif required['physics_acceptance']=='expected_dynamics':
                        # A separate developer instance validates passive physics after early task termination.
                        # It is not a client episode and does not contribute success/stability credit.
                        from agentbench_maniskill import make
                        raw=make(task['case_id'],physics_variant=condition['environment_parameters']['physics_variant'],
                            light_scale=condition['environment_parameters']['authored_light_scale'],obs_mode='none',render_backend='none')
                        try:
                            raw.reset(seed=condition['seed']);e=raw.unwrapped
                            for _ in range(100):
                                raw.step(e.hold_action())
                                state=e.snapshot()
                                assert all(np.isfinite(np.asarray(o['vertices'])).all() for o in state['objects'].values())
                            row['measurements']['passive_dynamics']=dict(physics_steps=e.physics_steps,simulation_seconds=e.physics_steps/e.sim_freq,
                                first_violation=getattr(e.oracle,'first_violation',None),motion_started=getattr(e,'motion_started',False),
                                frozen=e.freeze_dynamics,qualification='trigger/contact envelope checks still required')
                        finally:raw.close()
                    elif observed['simulation_time_s']+1e-6<duration or observed['terminated']:
                        raise AssertionError('Unexpected early termination during static hold')
                    row.update(simulation_seconds=observed['simulation_time_s'],settle_seconds=min(2.,observed['simulation_time_s']),
                        hold_seconds=max(0.,observed['simulation_time_s']-2),runtime=report['runtime'],terminal=terminal)
                    row['measurements']['physics']=dict(maximum_initial_displacement_m=initial_drift,maximum_hold_displacement_m=peak,
                        finite=True,acceptance=required['physics_acceptance'])
                    # Geometry, complete native scoring and contact/trigger qualification remain separate gates.
                    row['status']='passed_probe'
            except Exception as exc:
                import traceback
                row.update(error=type(exc).__name__+': '+str(exc),failure_traceback=traceback.format_exc())
            finally:
                if backend is not None:
                    if row['status']=='failed':
                        try:
                            row['physics_steps']=backend.e.physics_steps
                            row['measurements']['failure_state']=backend.e.snapshot()
                            row['measurements']['first_violation']=getattr(backend.e.oracle,'first_violation',None)
                        except Exception as diagnostic_error:
                            row['measurement_error']=type(diagnostic_error).__name__+': '+str(diagnostic_error)
                    backend.close()
            report['cases'].append(row);save();print(task['id'],row['status'],row.get('error',''),flush=True)
        report['run_status']='failed' if any(r['status']=='failed' for r in report['cases']) else 'completed'
    except BaseException:
        report['run_status']='interrupted';save();raise
    save();return int(report['run_status']!='completed')

if __name__=='__main__':raise SystemExit(main())
