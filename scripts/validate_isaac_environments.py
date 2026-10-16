#!/usr/bin/env python3
"""Batch native initialization/hold and actual four-level gateway probes.

This scoped engineering report does not certify full-horizon stability, local
contact reachability or scorer fixture coverage. No model or solution controller.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
for package in ('agentbench', 'agentbench_platform', 'agentbench_sdk'):
    sys.path.insert(0, str(ROOT / 'source' / package))


def create_journal_backend(task, seed, directory, resources, launcher, *, light_scale=1.):
    from types import MethodType, SimpleNamespace
    from agentbench_platform.environment_backend import IsaacEnvironmentBackend
    from agentbench_platform.native_environment import create_native_environment
    from agentbench_platform.native_recording import EvidenceJournal
    from agentbench_platform.native_backend import NativeBackend
    from agentbench_platform.rubiks_initialization import initialize_rubiks
    from agentbench_platform.rubiks_sharpa_scoring import SharpaRubiksScorer
    from agentbench_platform.kongming_scoring import KongmingScorer
    from agentbench_platform_runtime import goal_reset_data
    from agentbench_platform.evaluation_protocol import budgets
    limits=budgets(task)
    rubik=task['family'].startswith('rubiks_')
    args=SimpleNamespace(task_family='rubiks_cube' if rubik else 'kongming_lock',
        mode=task.get('mode','solve'),case_id=task['case_id'],environment_seed=seed,
        embodiment=('dual-floating-sharpa' if task['embodiment']=='dual-floating-sharpa' else
            'floating-sharpa' if task['family']=='rubiks_sharpa' else 'franka-panda'),
        device='cuda:0' if rubik or task['embodiment']=='dual-floating-sharpa' else 'cpu',goal_reference=False,case_reset_only=False,
        target_sequence=None,max_steps=limits['max_steps'],case_spec=None,
        evaluation_light_scale=None if light_scale==1. else light_scale)
    if rubik:
        from agentbench_platform.rubiks_cases import case_evidence,public_reset_data
        args.case_metadata=case_evidence(args.case_id)
        args.initial_data=public_reset_data(args.case_id)
    else:
        from agentbench_platform.kongming_cases import case_evidence,trusted_case_spec
        args.case_metadata=case_evidence(args.case_id)
        args.case_spec=trusted_case_spec(args.case_id)
        args.initial_data={}
    env,cfg,state,spec,cameras,robots,fixture,metadata,views=create_native_environment(
        args,resources,goal_reset_data=goal_reset_data)
    journal=None
    try:
        journal=EvidenceJournal(directory/'journal',source_paths=[Path(__file__)],
            config=dict(scope='private_environment_probe',task_id=task['id'],seed=seed))
        if rubik:
            scorer=initialize_rubiks(state,spec,journal,mode=args.mode,
                scorer_factory=SharpaRubiksScorer if task['family']=='rubiks_sharpa' else None)
            fixture.bind(scorer)
        else:scorer=KongmingScorer(args.mode,spec,case_spec=args.case_spec,embodiment=args.embodiment)
        backend=NativeBackend(state,scorer,journal,cameras=cameras,max_steps=args.max_steps,prepared=rubik)
        backend.env=env
        backend.resources=resources
        backend._physical_arrays=MethodType(IsaacEnvironmentBackend._physical_arrays,backend)
        backend.close=env.close
        return backend
    except BaseException:
        if journal is not None:journal.finish(dict(status='initialization_failed'))
        env.close()
        raise


def main():
    from isaaclab.app import AppLauncher
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--family', action='append', required=True,
        choices=['hanoi_panda', 'hanoi_sharpa', 'hanoi_floating', 'pocket_cube', 'bookshelf',
                 'rubiks_panda','rubiks_sharpa','kongming_lock'])
    parser.add_argument('--task-id', action='append')
    parser.add_argument('--seeds', nargs='+', type=int, default=[0, 1, 2])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seconds', type=float, default=5.)
    parser.add_argument('--matrix', action='store_true', help='Execute the selected complete condition matrix')
    parser.add_argument('--matrix-kind', choices=['legacy','protocol','union'],default='union')
    parser.add_argument('--condition-key',action='append')
    parser.add_argument('--probe-only',action='store_true',help='Explicit short diagnostic; cannot qualify full-horizon conditions')
    parser.add_argument('--list-conditions',action='store_true')
    parser.add_argument('--capture-contracts', action='store_true', help='Record native action contracts in this scoped probe')
    parser.add_argument('--resume', action='store_true', help='Resume only the same source and exact selected schedule; preserve failed attempts')
    parser.add_argument('--full-horizon', action='store_true', help='Hold for the declared complete episode limit')
    AppLauncher.add_app_launcher_args(parser)
    args = parser.parse_args()
    if args.seconds < 5 or not math.isfinite(args.seconds): parser.error('At least five seconds required')
    from agentbench_platform.environment_catalog import catalog, digest
    # Only the maintainer capture path may bootstrap stale projection records.
    # It measures native actions and never qualifies a condition. Client discovery
    # continues to require validated source hashes.
    bootstrap = None
    if args.capture_contracts:
        bootstrap = {}
    manifest = catalog(_native_records=bootstrap)
    tasks = [t for t in manifest['tasks'] if t['family'] in args.family and
        (args.task_id is None or t['id'] in args.task_id)]
    if not tasks or any(s < 0 for s in args.seeds): parser.error('Invalid tasks or seeds')
    if args.task_id and set(args.task_id) != {t['id'] for t in tasks}: parser.error('Unknown task ID')
    from agentbench_platform.environment_release import matrix
    conditions={task['id']:[] for task in tasks}
    if args.matrix:
        for required in matrix(dict(tasks=tasks),args.matrix_kind):
            conditions[required['task_id']].append(required)
    else:
        for task in tasks:
            from agentbench_platform.environment_matrix import effective_condition, VERSION
            conditions[task['id']]=[]
            for seed in args.seeds:
                condition=effective_condition(task,seed=seed)
                conditions[task['id']].append(dict(condition=condition,
                    key=digest([VERSION,task['id'],task['configuration_sha256'],condition]),memberships=[]))
    if args.condition_key:
        known={r['key'] for rows in conditions.values() for r in rows}
        if set(args.condition_key)-known:parser.error('Unknown condition key')
        conditions={task:[r for r in rows if r['key'] in args.condition_key] for task,rows in conditions.items()}
    if args.list_conditions:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(conditions,indent=2)+'\n');return 0
    args.enable_cameras = True
    app = AppLauncher(args).app
    import numpy as np
    import torch
    import omni.usd
    from agentbench_platform.environment_backend import create_isaac_backend
    from agentbench_platform.resources import ResourceStore
    from agentbench_platform.protocol import ProtocolService
    from agentbench_platform.profiles import RunProfile, CAPABILITY_VERSION
    from agentbench_platform.environment_release import inventory,evidence_identity
    from agentbench_platform.environment_qa import isaac_readback,gateway_probe,lifecycle_probe,repeat_measurement,contract_probe,local_action_probe,structure_displacement
    source_manifest=inventory();identity=evidence_identity(manifest,source_manifest)
    report = dict(scope='native_initialization_hold_gateway_probe', **identity, source_manifest=source_manifest,
        run_status='running',expected_cases=sum(map(len,conditions.values())),
        runtime=dict(python=sys.version, torch=torch.__version__, gpu=torch.cuda.get_device_name()), cases=[])
    selected_keys={r['key'] for rows in conditions.values() for r in rows}
    execution=dict(seconds=args.seconds,full_horizon=args.full_horizon,probe_only=args.probe_only,
        capture_contracts=args.capture_contracts,selected_keys=sorted(selected_keys))
    report['execution']=execution
    completed=set()
    if args.resume and args.output.exists():
        previous=json.loads(args.output.read_text())
        if any(previous.get(k)!=v for k,v in identity.items()) or previous.get('execution')!=execution:
            app.close();parser.error('Cannot resume changed source, protocol or execution conditions')
        rows=previous.get('cases',[]);keys=[r.get('key') for r in rows]
        if len(keys)!=len(set(keys)) or set(keys)-selected_keys:
            app.close();parser.error('Duplicate or unknown condition in resume evidence')
        report['attempt_history']=previous.get('attempt_history',[])+[r for r in rows if r.get('status')!='passed_probe']
        report['cases']=[r for r in rows if r.get('status')=='passed_probe']
        completed={r['key'] for r in report['cases']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    def save():
        temp = args.output.with_suffix('.tmp')
        temp.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n'); temp.replace(args.output)
    save()
    try:
        for task in tasks:
            for required in conditions[task['id']]:
                if required['key'] in completed:continue
                condition=required['condition'];seed=condition['seed']
                row = dict(task_id=task['id'], seed=seed,condition=condition,
                    key=required['key'],memberships=required['memberships'],
                    configuration_sha256=task['configuration_sha256'],versions=identity,status='failed', checks={}, measurements={},physics_steps=0)
                start = time.monotonic(); backend = None; services = []
                with tempfile.TemporaryDirectory(prefix='ab-native-batch-') as temporary:
                    directory = Path(temporary)
                    try:
                        omni.usd.get_context().new_stage()
                        resources = ResourceStore()
                        foreign_resources = ResourceStore()
                        foreign_id = foreign_resources.register(b'foreign-instance',modality='rgb',
                            profiles=('rgb','rgbd','privileged'),capture_step=0)
                        def construct(directory,resources):
                            directory.mkdir(parents=True,exist_ok=True)
                            if task['family'] in ('rubiks_panda','rubiks_sharpa','kongming_lock'):
                                return create_journal_backend(task,seed,directory,resources,AppLauncher,
                                    light_scale=condition['environment_parameters']['authored_sky_light_scale'])
                            return create_isaac_backend(task,seed=seed,split=condition['split'],device=args.device,
                                asset_dir=directory/'assets',resources=resources)
                        backend=construct(directory/'first',resources)
                        if not args.capture_contracts:
                            first=backend.snapshot()
                            row['measurements']['action_observation']=local_action_probe(backend)
                            row['checks']['action_observation']='passed'
                            row['measurements']['lifecycle']=lifecycle_probe(backend,directory/'lifecycle')
                            row['checks']['lifecycle']='passed'
                            backend.close();backend=None
                            omni.usd.get_context().new_stage()
                            resources=ResourceStore()
                            backend=construct(directory/'second',resources)
                            row['measurements']['repeat_initialization']=repeat_measurement(first,backend.snapshot())
                            row['checks']['repeat_initialization']='passed'
                            row['measurements']['contract']=contract_probe(backend,task)
                            row['checks']['contract']='passed'
                        row['native_description']=backend.describe()
                        if not args.capture_contracts:
                            row['actual_initialization'],row['measurements']['initialization']=isaac_readback(backend,task,condition)
                            row['measurements'].update(gateway_probe(backend,directory/'authorization'))
                            if task['family'].startswith('hanoi_') or task['family']=='pocket_cube':
                                from agentbench_platform.scorer_fixtures import symbolic_fixture
                                row['measurements']['scorer_endpoint']=symbolic_fixture(task,condition)
                            elif task['family']=='kongming_lock':
                                from agentbench_platform.scorer_fixtures import kongming_fixture
                                row['measurements']['scorer_endpoint']=kongming_fixture(task['case_id'],
                                    'dual-floating-sharpa' if task['embodiment']=='dual-floating-sharpa' else 'franka-panda')
                            elif task['family'].startswith('rubiks_'):
                                from agentbench_platform.rubiks_endpoint_fixture import check as rubiks_fixture
                                row['measurements']['scorer_endpoint']=rubiks_fixture(task)
                            elif task['family']=='bookshelf':
                                from agentbench_platform.scorer_fixtures import bookshelf_fixture
                                row['measurements']['scorer_endpoint']=bookshelf_fixture(task)
                        initial = backend.snapshot()
                        row['initial_robots'] = initial['robots']
                        row['initial_pieces'] = initial['privileged']['pieces']
                        for level in range(4):
                            profile = RunProfile(observation='privileged' if level == 3 else 'rgb',
                                capability_level=level, capability_profile_version=CAPABILITY_VERSION)
                            private = directory / str(level); private.mkdir()
                            service = ProtocolService(backend, token='engineering-fixture', profile=profile,
                                journal_path=private/'requests.sqlite', resources=resources)
                            services.append(service)
                            counter = 0
                            def call(method, params=None):
                                nonlocal counter
                                counter += 1
                                return service.handle(dict(version=1, id=str(counter), token='engineering-fixture',
                                    method=method, params=params or {}))
                            before = backend.snapshot()
                            observed = call('observe')
                            assert observed['ok'], observed
                            assert ('privileged' in observed['result']) == (level == 3)
                            for method in ('reset', 'set_state', 'set_seed'):
                                response = call(method)
                                assert not response['ok'] and response['error']['code'] == 'unsupported_method'
                            for resource_id in (foreign_id,'/etc/passwd','../scene.usda'):
                                response=call('get_resource',dict(resource_id=resource_id))
                                assert not response['ok'] and response['error']['code']=='resource_unavailable'
                            response=call('observe',dict(fields=['undeclared_hidden_state']))
                            assert not response['ok'] and response['error']['code']=='invalid_request'
                            assert call('tools.list')['result'] == {'tools': []}
                            for tool in ('pyroki', 'graspnet', 'unknown'):
                                response = call('tools.call', dict(name=tool, arguments={}))
                                assert not response['ok'] and response['error']['code'] == 'tool_unavailable', response
                            assert backend.snapshot() == before
                            description = call('describe')['result']
                            camera = next(iter(description['cameras']))
                            image = call('observe', dict(camera_ids=[camera]))
                            assert image['ok'], image
                            ident = image['result']['cameras'][camera]['rgb_resource_id']
                            resource = call('get_resource', dict(resource_id=ident))
                            assert resource['ok'] and resource['result']['byte_length'] > 0, resource
                            assert backend.snapshot()['physics_step_count'] == before['physics_step_count']
                            row['checks']['gateway_l' + str(level)] = 'passed'
                        action = description['action_spec']['neutral_action']
                        dt = description['action_spec']['control_period_s']
                        episode_limit=description['task']['max_steps']*dt
                        seconds=max(args.seconds,episode_limit) if args.full_horizon or (args.matrix and not args.probe_only and task.get('full_horizon_stability')) else args.seconds
                        control_count=math.ceil(seconds / dt-1e-8)
                        initial_positions={name:piece['position'] for name,piece in initial['privileged']['pieces'].items()}
                        baseline=None;peak_drift=0.;settling_drift=0.
                        for index in range(control_count):
                            observation = backend.step(action)
                            assert all(np.isfinite(a).all() for a in backend._physical_arrays()), 'Nonfinite native state'
                            assert not observation['terminated'], 'Unexpected no-action terminal'
                            assert not observation['truncated'] or index+1==control_count, 'Unexpected early timeout'
                            positions={name:np.asarray(piece['position']) for name,piece in observation['privileged']['pieces'].items()}
                            if index+1==round(2/dt):
                                baseline=positions
                                settling_drift=structure_displacement(initial_positions,baseline)
                                row['measurements']['settling']=dict(maximum_initial_displacement_m=settling_drift,limit_m=.003)
                                assert settling_drift<=.003, 'Initial structure changed by more than 3 mm during settling'
                            if baseline is not None:
                                peak_drift=max(peak_drift,structure_displacement(baseline,positions))
                            assert peak_drift<=.003, 'Native support structure drift exceeds 3 mm'
                        row.update(physics_steps=observation['physics_step_count'],
                            settle_seconds=2.,hold_seconds=max(0.,observation['simulation_time_s']-2),
                            runtime=report['runtime'],simulation_seconds=observation['simulation_time_s'],
                            no_operation_seconds=observation['simulation_time_s'],
                            episode_time_limit_seconds=episode_limit,
                            final_pieces=observation['privileged']['pieces'])
                        row['checks']['finite_hold'] = 'passed'
                        row['measurements']['physics']=dict(maximum_structure_drift_m=peak_drift,maximum_initial_displacement_m=settling_drift,drift_limit_m=.003,finite=True,
                            observed_timeout=bool(observation['truncated']),required_episode_seconds=condition['budgets']['simulation_seconds'])
                        if seconds>=condition['budgets']['simulation_seconds']:
                            assert observation['truncated'], 'Full-horizon idle did not time out'
                            row['checks']['physics']='passed'
                        row['status'] = 'passed_probe'
                    except Exception as exc:
                        row['error'] = type(exc).__name__ + ': ' + str(exc)
                        import traceback
                        row['failure_traceback']=traceback.format_exc()
                    finally:
                        for service in services: service.close()
                        if backend is not None:
                            try: backend.finish(); backend.close()
                            except Exception as exc:
                                row.update(status='failed', error='Cleanup: ' + repr(exc))
                    row['elapsed_seconds'] = time.monotonic() - start
                    report['cases'].append(row); save()
                    print('CASE', row['task_id'], seed, row['status'], row.get('error', ''), flush=True)
    finally:
        if len(report['cases'])==report['expected_cases']:
            report['run_status']='failed' if any(r['status']=='failed' for r in report['cases']) else 'completed'
        else:report['run_status']='interrupted'
        save()
        app.close()
    return int(any(row['status'] != 'passed_probe' for row in report['cases']))


if __name__ == '__main__': raise SystemExit(main())
