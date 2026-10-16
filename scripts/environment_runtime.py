#!/usr/bin/env python3
"""Launch one environment-only permission gateway; no model service is used."""
import argparse
import json
import os
from pathlib import Path
import secrets
import sys
import tempfile
import time
ROOT=Path(__file__).resolve().parents[1]
for package in ('agentbench','agentbench_platform','agentbench_sdk'):
    sys.path.insert(0,str(ROOT/'source'/package))


def main(argv=None):
    from agentbench_platform.environment_catalog import find_task
    from agentbench_platform.profiles import RunProfile,CAPABILITY_VERSION
    p=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    p.add_argument('--task-id',required=True)
    p.add_argument('--capability-level',type=int,choices=range(4),required=True)
    p.add_argument('--profile',choices=['rgb','rgbd','privileged'])
    p.add_argument('--tool',action='append',default=[])
    p.add_argument('--tool-setup')
    p.add_argument('--cube-solver-setup')
    p.add_argument('--seed',type=int,default=0)
    p.add_argument('--split',choices=['nominal','train','heldout'],default='nominal')
    p.add_argument('--initial-mode',choices=['loaded','ground'],default='loaded')
    p.add_argument('--spring-stiffness',type=float,choices=[22,24,26,28],default=22.)
    p.add_argument('--evaluation-protocol',choices=['environment-four-trial-v1','environment-four-trial-v2'])
    p.add_argument('--trial-index',type=int,choices=range(1,5))
    p.add_argument('--output',type=Path)
    p.add_argument('--max-steps',type=int)
    p.add_argument('--wall-seconds',type=float)
    p.add_argument('--headless',action='store_true')
    p.add_argument('--device',default='cuda:0')
    args=p.parse_args(argv)
    task=find_task(args.task_id)
    from agentbench_platform.evaluation_protocol import budgets
    defaults=budgets(task)
    if args.wall_seconds is None:args.wall_seconds=defaults['wall_seconds']
    if args.max_steps is None:args.max_steps=defaults['max_steps']
    if args.seed<0 or not 0<args.wall_seconds<float('inf') or args.max_steps is not None and args.max_steps<1:
        p.error('Invalid seed or limits')
    trial=None
    if args.evaluation_protocol:
        if args.evaluation_protocol=='environment-four-trial-v1' and (task['backend']=='maniskill' or task['embodiment']=='dual-floating-sharpa'):
            p.error('New tasks require environment-four-trial-v2')
        from agentbench_platform.evaluation_protocol import select_trial,budgets
        raw=sys.argv[1:] if argv is None else argv
        if any(v.split('=')[0] in ('--split','--spring-stiffness','--max-steps','--wall-seconds') for v in raw):
            p.error('Registered evaluation controls split, spring and budgets; omit their overrides')
        if args.trial_index is None:p.error('Evaluation requires an explicit --trial-index 1..4')
        try:trial=select_trial(task,args.seed,args.trial_index,initial_mode=args.initial_mode)
        except ValueError as exc:p.error(str(exc))
        args.base_seed=args.seed
        args.seed=trial['reset_seed'];args.split=trial['split']
        limits=budgets(task);args.max_steps=limits['max_steps'];args.wall_seconds=limits['wall_seconds']
        if task['family']=='marble':args.spring_stiffness=trial['environment_parameters']['spring_stiffness']
    elif args.trial_index is not None:p.error('--trial-index requires --evaluation-protocol')
    profile=RunProfile(observation=args.profile or ('privileged' if args.capability_level==3 else 'rgb'),tools=tuple(args.tool),
        capability_level=args.capability_level,capability_profile_version=CAPABILITY_VERSION)
    if task['family']=='marble' and profile.observation=='rgbd':
        p.error('Marble declares RGB only; native depth is not a public sensor')
    output=args.output or Path(tempfile.mkdtemp(prefix='agentbench-environment-parent-'))/'episode'
    if os.environ.get('AGENTBENCH_EPISODE_CHILD')!='1':
        from agentbench_platform.environment_supervisor import supervise
        raw=list(sys.argv[1:] if argv is None else argv)
        if args.output is None:raw+=['--output',str(output)]
        environment=dict(os.environ,AGENTBENCH_EPISODE_CHILD='1')
        raise SystemExit(supervise([sys.executable,str(Path(__file__).resolve()),*raw],
            seconds=args.wall_seconds,output=output,environment=environment))
    if task['family'] in ('rubiks_panda','rubiks_sharpa','kongming_lock'):
        command=[sys.executable,str(ROOT/'scripts/agentbench_platform_runtime.py'),
            '--task-family','kongming_lock' if task['family']=='kongming_lock' else 'rubiks_cube',
            '--mode',task.get('mode','solve'),'--case-id',task['case_id'],
            '--capability-level',str(args.capability_level),'--profile',profile.observation,
            '--disable-cube-solver','--output',str(output),'--wall-seconds',str(args.wall_seconds),
            '--result-grace-seconds','2',
            '--environment-seed',str(args.seed)]
        if trial:
            command+=['--evaluation-protocol-version',args.evaluation_protocol,'--evaluation-light-scale',str(trial['environment_parameters']['authored_sky_light_scale']),
                '--evaluation-base-seed',str(args.base_seed),'--evaluation-trial-index',str(args.trial_index)]
        if task['family']=='rubiks_sharpa':command+=['--embodiment','floating-sharpa']
        if task['embodiment']=='dual-floating-sharpa':command+=['--embodiment','dual-floating-sharpa']
        if args.max_steps:command+=['--max-steps',str(args.max_steps)]
        if args.headless:command+=['--headless']
        for tool in args.tool:command+=['--tool',tool]
        if args.tool_setup:command+=['--tool-setup',args.tool_setup]
        if args.cube_solver_setup:command+=['--cube-solver-setup',args.cube_solver_setup]
        if 'cube_solver' in args.tool:command.remove('--disable-cube-solver')
        # Preserve catalog case projections; case seeds are maintainer identities,
        # not silently remapped to a different public case.
        os.execv(sys.executable,command)
    output.mkdir(parents=True,exist_ok=False,mode=0o700)
    if trial:
        (output/'evaluation-trial.private.json').write_text(json.dumps(dict(
            version=args.evaluation_protocol,task_id=task['id'],base_seed=args.base_seed,
            trial=trial,budgets=limits,configuration_sha256=task['configuration_sha256']),indent=2)+'\n')
    from agentbench_platform.environment_backend import MarbleBackend,IsaacEnvironmentBackend
    from agentbench_platform.resources import ResourceStore
    resources=ResourceStore();app=None;backend=None;env=None;server=None;service=None;dispatcher=None
    try:
        from agentbench_platform.plugins import configured_registry
        args.profile=profile.observation
        registry=configured_registry(args,resources=resources,private_directory=output/'tools-private')
        if task['backend']=='mujoco':
            from agentbench_mujoco.rendering import configure_headless
            if args.headless:configure_headless()
            backend=MarbleBackend(task,seed=args.seed,initial_mode=args.initial_mode,
                spring_stiffness=args.spring_stiffness,resources=resources,max_steps=args.max_steps,
                environment_parameters=trial['environment_parameters'] if trial else None)
        elif task['backend']=='maniskill':
            sys.path.insert(0,str(ROOT/'env/maniskill_lgd'))
            from agentbench_platform.maniskill_backend import ManiSkillBackend
            backend=ManiSkillBackend(task,resources=resources,seed=args.seed,max_steps=args.max_steps,
                parameters=trial['environment_parameters'] if trial else None)
        else:
            from isaaclab.app import AppLauncher
            app=AppLauncher(headless=args.headless,enable_cameras=True,device=args.device).app
            from agentbench_platform.environment_backend import create_isaac_backend
            backend=create_isaac_backend(task,seed=args.seed,split=args.split,device=args.device,
                asset_dir=output/'assets',resources=resources,max_steps=args.max_steps)
            env=backend.env
        from agentbench_platform.protocol import ProtocolService,ProtocolServer
        from agentbench_platform.native_backend import MainThreadDispatcher,DispatchedBackend
        dispatcher=MainThreadDispatcher();token=secrets.token_urlsafe(32)
        # A short, owned directory avoids AF_UNIX path length limits.
        socket_dir=tempfile.TemporaryDirectory(prefix='ab-env-')
        socket_path=Path(socket_dir.name)/'native.sock'
        service=ProtocolService(DispatchedBackend(backend,dispatcher),token=token,profile=profile,
            journal_path=output/'requests.sqlite',resources=resources,tools=registry,finalize_on_terminal=True)
        server=ProtocolServer(socket_path,service);server.start()
        session=dict(socket_path=str(socket_path),native_token=token,profile=profile.public_record())
        session_path=output/'session.json'
        temporary=session_path.with_suffix('.tmp')
        temporary.write_text(json.dumps(session,indent=2)+'\n');temporary.chmod(0o600);temporary.replace(session_path)
        print('Session: '+str(session_path),flush=True)
        deadline=time.monotonic()+args.wall_seconds
        while time.monotonic()<deadline and not service.terminal_response_complete.is_set() and (app is None or app.is_running()):
            if not service.poll_storage():break
            dispatcher.pump(timeout=.05)
        backend.finish()
        # Finish retries are served from the protocol journal, not a new episode.
        end=time.monotonic()+2.
        while time.monotonic()<end:dispatcher.pump(timeout=.05)
    finally:
        if dispatcher:dispatcher.close()
        if server:server.close()
        if service:service.close()
        if backend:backend.close()
        elif env:env.close()
        if app:app.close()
        if 'socket_dir' in locals():socket_dir.cleanup()


if __name__=='__main__':main()
