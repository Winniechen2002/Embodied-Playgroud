#!/usr/bin/env python3
"""One trusted native PhysX episode. Agent clients never import this entry point."""
import argparse
import json
import math
import os
from pathlib import Path
import secrets
import sys

# This entry point can be exec'd by environment_runtime.py. exec starts a new
# interpreter, so the parent process's in-memory sys.path is not inherited.
ROOT = Path(__file__).resolve().parents[1]
for package in ('agentbench', 'agentbench_platform', 'agentbench_sdk'):
    sys.path.insert(0, str(ROOT / 'source' / package))


def parse_runtime_args(launcher, argv=None):
    from agentbench_platform.tasks import add_task_arguments, normalize_embodiment, validate_task
    from agentbench_platform.profile_cli import add_profile_arguments
    from agentbench_platform.container_engine import add_container_arguments
    parser = argparse.ArgumentParser(description=__doc__)
    add_task_arguments(parser)
    add_profile_arguments(parser)
    add_container_arguments(parser)
    parser.add_argument('--target-sequence', help='Space-separated public goal moves for execute_sequence')
    initial = parser.add_mutually_exclusive_group()
    initial.add_argument('--case-id', help='Public case: Rubik C01..C30 or Kongming A01..A15/D01..D15')
    initial.add_argument('--initial-config', type=Path, help='Private maintainer reset JSON')
    initial.add_argument('--scramble', help='Private maintainer reset moves')
    parser.add_argument('--local-state-root', type=Path, help='Owned local filesystem for socket and request SQLite')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-steps', type=int)
    parser.add_argument('--environment-seed',type=int,default=None,
                        help='Maintainer RNG seed; public case geometry remains fixed')
    parser.add_argument('--evaluation-protocol-version',choices=['environment-four-trial-v1','environment-four-trial-v2'],default='environment-four-trial-v2')
    parser.add_argument('--evaluation-light-scale', type=float, choices=[.85,.95,1.05,1.15])
    parser.add_argument('--evaluation-base-seed',type=int)
    parser.add_argument('--evaluation-trial-index',type=int,choices=range(1,5))
    parser.add_argument('--wall-seconds', type=float)
    parser.add_argument('--result-grace-seconds', type=float, default=30.)
    parser.add_argument('--native-smoke', action='store_true')
    parser.add_argument('--native-smoke-profile', choices=('privileged', 'rgb', 'rgbd'),
        help='Observation profile used by the maintainer native smoke')
    parser.add_argument('--case-reset-only', action='store_true',
        help='Maintainer acceptance: settle one public case, preserve private evidence, then stop')
    parser.add_argument('--goal-reference', action='store_true', help='Separate maintainer reset-only goal stills')
    launcher.add_app_launcher_args(parser)
    parser.set_defaults(device=None)
    args = parser.parse_args(argv)
    if args.environment_seed is not None and args.environment_seed < 0:
        parser.error('Environment seed must be nonnegative')
    rubik = args.task_family == 'rubiks_cube'
    from agentbench_platform.evaluation_protocol import budgets
    limits=budgets(dict(family='rubiks_panda' if rubik else 'kongming_lock'))
    args.max_steps = args.max_steps if args.max_steps is not None else limits['max_steps']
    args.wall_seconds = args.wall_seconds if args.wall_seconds is not None else limits['wall_seconds']
    try:
        args.case_metadata = None
        args.embodiment = normalize_embodiment(args.embodiment)
        args.device = args.device or ('cuda:0' if rubik or args.embodiment == 'dual-floating-sharpa' else 'cpu')
        if args.embodiment == 'dual-floating-sharpa' and args.case_id is None:
            raise ValueError('Dual Floating Sharpa requires a public --case-id')
        args.target_sequence = validate_task(args.task_family, args.mode,
            args.target_sequence.split() if args.target_sequence is not None else None,
            embodiment=args.embodiment)
        if not rubik and (args.initial_config is not None or args.scramble is not None):
            raise ValueError('Private cube initialization is only valid for rubiks_cube')
        from agentbench_platform.evaluation_protocol import LIGHT_SCALES
        evaluation_fields=(args.evaluation_light_scale,args.evaluation_base_seed,args.evaluation_trial_index)
        if any(v is not None for v in evaluation_fields):
            if any(v is None for v in evaluation_fields) or args.case_id is None:
                raise ValueError('Evaluation requires case, scale, base seed and trial index')
            if (args.evaluation_light_scale!=LIGHT_SCALES[args.evaluation_trial_index-1]
                    or args.evaluation_base_seed!=args.environment_seed or args.environment_seed<0):
                raise ValueError('Evaluation trial mapping mismatch')
            if (args.max_steps!=limits['max_steps']
                    or args.wall_seconds!=limits['wall_seconds']
                    or args.case_reset_only or args.goal_reference or args.native_smoke):
                raise ValueError('Registered evaluation requires standard episode budgets and mode')
        args.case_spec = None
        if args.case_id is not None:
            if rubik:
                if args.mode != 'solve':
                    raise ValueError('--case-id is only valid for rubiks_cube solve')
                from agentbench_platform.rubiks_cases import case_evidence, public_reset_data
                # Resolve and validate before any output directory or simulator is
                # created.  The trusted runner keeps the full case in maintainer
                # memory; only case_id is inserted into the public description.
                args.case_metadata = case_evidence(args.case_id)
                args.initial_data = public_reset_data(args.case_id)
            else:
                if args.mode not in ('assemble', 'disassemble'):
                    raise ValueError('--case-id requires assemble or disassemble for Kongming')
                from agentbench_platform.kongming_cases import case_evidence, trusted_case_spec
                args.case_metadata = case_evidence(args.case_id)
                args.case_spec = trusted_case_spec(args.case_id)
                if args.case_spec['task'] != args.mode:
                    raise ValueError('Kongming case task and --mode do not match')
                args.initial_data = {}
        else:
            args.initial_data = json.loads(args.initial_config.read_text()) if args.initial_config else (
                {'scramble': args.scramble} if args.scramble is not None else {})
        cuda_native = rubik or args.embodiment == 'dual-floating-sharpa'
        if cuda_native and not args.device.startswith('cuda') or not cuda_native and args.device != 'cpu':
            raise ValueError('Rubik and dual Floating Sharpa require CUDA PhysX; DualFranka Kongming requires CPU PhysX')
        if not isinstance(args.initial_data, dict):
            raise ValueError('Initial config must be a JSON object')
        if args.case_reset_only:
            if args.case_id is None or args.goal_reference or args.native_smoke or args.tool:
                raise ValueError('--case-reset-only requires a public case and no goal/smoke/tool operation')
            args.disable_cube_solver = True
        if rubik and args.native_smoke and args.case_id is not None and args.embodiment != 'floating-sharpa':
            raise ValueError('The solved-cube native smoke is separate from public scrambled cases')
        if (args.max_steps < 1 or not math.isfinite(args.wall_seconds) or args.wall_seconds <= 0
                or not 0 <= args.result_grace_seconds <= 300):
            raise ValueError('Positive finite run limits and result grace 0..300 seconds required')
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    args.enable_cameras = not (args.embodiment == 'dual-floating-sharpa' and args.case_reset_only)
    if args.native_smoke:
        args.profile = args.native_smoke_profile or 'rgbd'
    return args


def goal_reset_data(initial_data, mode, target_sequence):
    """Build a separate reset-only exemplar; no mutation of the active scene."""
    from copy import deepcopy
    from agentbench_platform.tasks import validate_task
    validate_task('rubiks_cube', mode, target_sequence)
    data = deepcopy(initial_data)
    data['scramble'] = '' if mode == 'solve' else ' '.join(
        [*data.get('scramble', '').split(), *target_sequence])
    return data




def main():
    from isaaclab.app import AppLauncher
    from agentbench_platform.profile_cli import profile_from_args
    args = parse_runtime_args(AppLauncher)
    from agentbench_platform.resources import ResourceStore
    from agentbench_platform.plugins import configured_registry
    args.output.mkdir(parents=True,exist_ok=False)
    os.chmod(args.output,0o700)
    resources=ResourceStore()
    try:
        tools=configured_registry(args,resources=resources,private_directory=args.output/'tool-private')
        run_profile=profile_from_args(args,available_tools=[d['name'] for d in tools.list()] if tools else ())
    except ValueError as exc:
        print(str(exc), file=sys.stderr); raise SystemExit(2)
    (args.output/'run_profile.json').write_text(json.dumps(dict(version=1,profile=run_profile,
        baseline={'name':args.task_family+'_reference'} if args.experience_profile=='reference' else None),indent=2)+'\n')
    app=AppLauncher(args).app
    env=None;backend=None;server=None;service=None;dispatcher=None;storage=None;journal=None
    try:
        import gymnasium as gym
        import isaaclab_tasks
        import agentbench.tasks
        from agentbench.tasks.utils import parse_env_cfg
        from agentbench_platform.native_cameras import add_cameras,add_target_outlines,NativeCameras
        from agentbench_platform.native_backend import NativeBackend,MainThreadDispatcher,DispatchedBackend,run_native_service
        from agentbench_platform.native_storage import RuntimeStorage
        from agentbench_platform.native_recording import EvidenceJournal
        from agentbench_platform.native_state import plain
        from agentbench_platform.profiles import RunProfile
        from agentbench_platform.protocol import ProtocolService,ProtocolServer
        from agentbench_platform.native_export import export_robot_models,export_goal_stills
        assert not any(n=='baselines' or n.startswith('baselines.') for n in sys.modules)
        root=Path(__file__).resolve().parents[1]
        import agentbench, agentbench_platform, agentbench_sdk
        imports={m.__name__:str(Path(m.__file__).resolve()) for m in (agentbench,agentbench_platform,agentbench_sdk)}
        if any(not Path(p).is_relative_to(root/'source') for p in imports.values()):
            raise RuntimeError('Imported code is outside the selected development snapshot')
        rubik=args.task_family=='rubiks_cube'
        sharpa = rubik and args.embodiment == 'floating-sharpa'
        dual_sharpa = args.task_family == 'kongming_lock' and args.embodiment == 'dual-floating-sharpa'
        from agentbench_platform.native_environment import create_native_environment
        env,cfg,state,spec,cameras,robots,fixture,initial_metadata,VIEWS = create_native_environment(
            args,resources,goal_reset_data=goal_reset_data)
        if args.goal_reference:
            if not rubik:state.reset()
            export_robot_models(env,args.output,robots=robots)
            export_goal_stills(args.output,cameras,resources,args.mode)
            return
        storage=RuntimeStorage(root,args.output,local_root=args.local_state_root)
        socket_path=storage.socket_path
        sources=[Path(__file__)]+[p for folder in (
            root/'source/agentbench_platform',root/'source/agentbench_sdk',
            root/'source/agentbench/agentbench/tasks/manager_based/table_top_manipulation/config'/args.task_family,
            root/'source/agentbench/agentbench/assets/assets'/args.task_family,
            root/'source/agentbench/agentbench/assets/articulations'/args.task_family)
            for p in folder.rglob('*') if p.is_file() and p.suffix in ('.py','.json','.usda','.toml')
            and not any(part in ('build','dist','__pycache__') or part.endswith('.egg-info') for part in p.parts)]
        sources += list((root/'source/agentbench/agentbench/tasks/manager_based/table_top_manipulation/config').glob('tabletop_background*.py'))
        if sharpa or dual_sharpa:
            # The official robot asset and its loader are part of the immutable
            # native identity.  Hash them alongside the task and gateway code.
            sharpa_root = root/'source/agentbench/agentbench/robot_usds/Sharpa_hand/Floating_Sharpa_right'
            asset_suffixes = {'.py', '.json', '.usda', '.usd', '.urdf', '.yaml', '.yml', '.md', '.txt'}
            sources += [p for p in sharpa_root.rglob('*') if p.is_file() and p.suffix in asset_suffixes]
            sources += [root/'source/agentbench/agentbench/sharpa_joint_names.py',
                        root/'source/agentbench/agentbench/robot_agents/franka_sharpa_right.py']
        # Include actual runtime loop and sensor implementation, not just package versions.
        import inspect
        from isaaclab.envs import ManagerBasedEnv
        from isaaclab.sensors import Camera,ContactSensor
        sources += [Path(inspect.getfile(x)) for x in (ManagerBasedEnv,Camera,ContactSensor)]
        journal=EvidenceJournal(args.output/'private',source_paths=sorted(set(sources)),
            config=dict(task_family=args.task_family,embodiment=args.embodiment,mode=args.mode,target_sequence=args.target_sequence,
                        environment_seed=args.environment_seed,
                        evaluation_protocol=(args.evaluation_protocol_version if args.evaluation_trial_index else None),
                        evaluation_base_seed=args.evaluation_base_seed,evaluation_trial_index=args.evaluation_trial_index,
                        evaluation_light_scale=args.evaluation_light_scale,
                        case_id=args.case_id,
                        case=args.case_metadata,
                        profile=args.profile,run_profile=run_profile,imports=imports,initialization=initial_metadata,
                        action_spec=state.describe()['action_spec'],wall_seconds=args.wall_seconds,
                        baseline=({'name':args.task_family+'_reference'} if args.experience_profile=='reference' else None),physics_hz=120,control_hz=30,max_steps=args.max_steps,
                        result_grace_seconds=args.result_grace_seconds,
                        cameras=VIEWS,physical_spec=spec,environment=json.loads(json.dumps(cfg.to_dict(),default=str))))
        if rubik:
            from agentbench_platform.rubiks_initialization import initialize_rubiks
            if sharpa:
                from agentbench_platform.rubiks_sharpa_reset import SharpaResetScorer
                from agentbench_platform.rubiks_sharpa_scoring import SharpaRubiksScorer
                scorer=initialize_rubiks(state,spec,journal,mode=args.mode,
                    target_sequence=args.target_sequence,
                    scorer_factory=SharpaResetScorer if args.case_reset_only else SharpaRubiksScorer)
                if fixture is not None:fixture.bind(scorer)
            else:
                scorer=initialize_rubiks(state,spec,journal,mode=args.mode,target_sequence=args.target_sequence)
                fixture.bind(scorer)
        elif dual_sharpa:
            from agentbench_platform.kongming_scoring import KongmingScorer
            scorer=KongmingScorer(args.mode, spec, case_spec=args.case_spec,
                embodiment='dual-floating-sharpa')
        else:
            from agentbench_platform.kongming_scoring import KongmingScorer
            scorer=KongmingScorer(args.mode,spec,case_spec=args.case_spec)
        backend=NativeBackend(state,scorer,journal,cameras=cameras,max_steps=args.max_steps,prepared=rubik,
            control_observer=None)
        if args.case_reset_only:
            backend.finish(reason='runtime_shutdown')
            if rubik:
                initialization = scorer.initialization
                passed = initialization['passed']
            else:
                initialization = state.reset_acceptance()
                passed = initialization['passed']
            (args.output/'reset_acceptance.json').write_text(json.dumps(dict(
                case=args.case_metadata, passed=passed,
                initialization=initialization, task_success=False), indent=2)+'\n')
            return
        public=args.output/'public';public.mkdir(mode=0o700)
        export_robot_models(env,public,robots=robots)
        (public/'cameras.json').write_text(json.dumps(cameras.description(),indent=2)+'\n')
        if args.native_smoke:
            if rubik:
                from agentbench_platform.rubiks_native_smoke import run_smoke
            else:
                from agentbench_platform.native_smoke import run_smoke
            run_smoke(backend,env,resources,args.output,socket_path,journal_path=storage.sqlite_path,
                      storage_guard=storage.guard,profile=args.profile)
            return
        token=secrets.token_urlsafe(32)
        (public/'token').write_text(token+'\n');os.chmod(public/'token',0o600)
        dispatcher=MainThreadDispatcher()
        service=ProtocolService(DispatchedBackend(backend,dispatcher),token=token,profile=RunProfile(**{**run_profile,'tools':tuple(run_profile['tools'])}),
            journal_path=storage.sqlite_path,resources=resources,tools=tools,finalize_on_terminal=True,storage_guard=storage.guard)
        server=ProtocolServer(socket_path,service);server.start()
        session=args.output/'session.json'
        temporary=session.with_suffix('.tmp')
        temporary.write_text(json.dumps(dict(socket_path=str(socket_path),native_token=token,profile=run_profile))+'\n')
        temporary.chmod(0o600);temporary.replace(session)
        print('Session: '+str(session),flush=True)
        (args.output/'ready.json').write_text(json.dumps(dict(socket=str(socket_path),pid=os.getpid(),profile=run_profile))+'\n')
        def close_native():
            nonlocal env
            env.close();env=None
            # Kit shutdown may terminate Python before its finally clauses run.
            # Keep the app until protocol grace and durable SQLite archival end.
        run_native_service(backend,dispatcher,service,is_running=app.is_running,
            wall_seconds=args.wall_seconds,close_native=close_native,replay_seconds=args.result_grace_seconds)
    except BaseException:
        import traceback
        detail=traceback.format_exc()
        (args.output/'exception.txt').write_text(detail)
        print(detail,flush=True)
        raise
    finally:
        if dispatcher:dispatcher.close()
        if server:server.close()
        if service:service.close()
        if backend:
            if storage and storage.guard.loss: backend.abort()
            else: backend.finish()
        elif journal and not journal.closed:journal.finish(dict(incomplete=True,termination_reason='initialization_or_setup_failure'))
        if storage:storage.archive()
        if env:env.close()
        if app:app.close()


if __name__=='__main__':main()
