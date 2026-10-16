"""Shared maintainer construction for the native journal-backed environments.

Importing this module does not initialize Isaac. Call only after AppLauncher.
"""


def create_native_environment(args, resources, *, goal_reset_data):
    if args.task_family == 'kongming_lock' and args.embodiment == 'dual-floating-sharpa':
        return create_dual_sharpa_environment(args, resources)
    import gymnasium as gym
    import isaaclab_tasks
    import agentbench.tasks
    from agentbench.tasks.utils import parse_env_cfg
    from .native_cameras import add_cameras, add_target_outlines, NativeCameras
    from .native_state import plain
    from .evaluation_protocol import apply_visual_trial
    rubik=args.task_family=='rubiks_cube'
    sharpa=rubik and args.embodiment=='floating-sharpa'
    fixture=None
    initial_metadata=None
    if rubik:
        from agentbench.tasks.manager_based.table_top_manipulation.config.rubiks_cube.rubiks_cube_env import RubiksCubeEnv
        if sharpa:
            from agentbench.tasks.manager_based.table_top_manipulation.config.rubiks_cube.rubiks_cube_sharpa_benchmark import SharpaState,VIEWS
        else:
            from agentbench.tasks.manager_based.table_top_manipulation.config.rubiks_cube.rubiks_cube_benchmark import RubiksState,VIEWS
        from agentbench.tasks.manager_based.table_top_manipulation.config.rubiks_cube.rubiks_cube_fixture import NativeFixture
        from agentbench.tasks.manager_based.table_top_manipulation.config.rubiks_cube.rubiks_cube_initialization import prepare_initial_reset,initial_scene_parameters
        task_id = ('Agentbench-RubiksCube-FloatingSharpaRight-Play-v0' if sharpa
                   else 'Agentbench-RubiksCube-FrankaPanda-Play-v0')
        cfg=parse_env_cfg(task_id,device=args.device,num_envs=1)
        if args.environment_seed is not None: cfg.seed=args.environment_seed
        if args.case_metadata is not None and args.environment_seed is None:
            cfg.seed = args.case_metadata['seed']
        xy,table_height=initial_scene_parameters(cfg)
        initial_data=goal_reset_data(args.initial_data,args.mode,args.target_sequence) if args.goal_reference else args.initial_data
        reset_spec,initial_metadata=prepare_initial_reset(initial_data,baseline_xy_m=xy,table_height_m=table_height)
        apply_visual_trial(cfg,getattr(args,'evaluation_light_scale',None))
        add_cameras(cfg,views=VIEWS)
        env=RubiksCubeEnv(cfg,initial_reset_spec=reset_spec)
        fixture = (None if sharpa and args.case_reset_only else NativeFixture(env,
            hand_body_name='right_hand_C_MC' if sharpa else 'panda_hand'))
        state = (SharpaState(env,mode=args.mode,target_sequence=args.target_sequence,case_id=args.case_id,mechanism=fixture)
                 if sharpa else RubiksState(env,mode=args.mode,target_sequence=args.target_sequence,
                                            mechanism=fixture,case_id=args.case_id))
        state.reset()
        if sharpa:
            spec=dict(embodiment='floating-sharpa', table_height_m=table_height,
                home_joint_positions=plain(state.robot.data.default_joint_pos[0,state.joint_ids]),
                joint_ids=list(state.joint_ids), motion_joint_ids=list(state.motion_ids),
                finger_joint_ids=list(state.finger_ids),
                initial_target=dict(position=initial_metadata['target_core_position_xyz_m'],
                    quaternion=initial_metadata['target_core_quaternion_wxyz'],
                    facelets_urfdlb=initial_metadata['expected_facelets_urfdlb'],
                    permutation_checksum=initial_metadata['expected_permutation_checksum']))
        else:
            spec=dict(embodiment='franka-panda',table_height_m=table_height,home_joint_positions=plain(state.robot.data.default_joint_pos[0,state.arm_ids]),
                arm_joint_ids=list(state.arm_ids),finger_joint_ids=list(state.finger_ids),
                initial_target=dict(position=initial_metadata['target_core_position_xyz_m'],
                    quaternion=initial_metadata['target_core_quaternion_wxyz'],facelets_urfdlb=initial_metadata['expected_facelets_urfdlb']))
        if args.case_metadata is not None and not args.goal_reference:
            if (initial_metadata['expected_facelets_urfdlb'] != args.case_metadata['expected_facelets_urfdlb']
                    or initial_metadata['expected_permutation_checksum'] != args.case_metadata['permutation_checksum']):
                raise ValueError('Catalog/reset symbolic state mismatch')
            spec['initial_target']['permutation_checksum'] = args.case_metadata['permutation_checksum']
        cameras=NativeCameras(env,resources,views=VIEWS,physical_arrays=state.physical_arrays)
        robots={('floating_sharpa' if sharpa else 'panda'):('/World/envs/env_0/Robot','robot')}
    else:
        from agentbench.tasks.manager_based.table_top_manipulation.config.kongming_lock.shapes import CANONICAL_SPEC,collision_boxes,TABLE_TOP_Z
        from agentbench_platform.native_state import IsaacState,scorer_spec
        from agentbench_platform.native_cameras import VIEWS
        from agentbench_platform.kongming_scoring import KongmingScorer
        mode=('disassemble' if args.mode=='assemble' else 'assemble') if args.goal_reference else args.mode
        task='Agentbench-KongmingLock-DualFranka-'+mode.capitalize()+'-Play-v0'
        cfg=parse_env_cfg(task,device='cpu',num_envs=1)
        if args.environment_seed is not None: cfg.seed=args.environment_seed
        apply_visual_trial(cfg,getattr(args,'evaluation_light_scale',None))
        add_cameras(cfg)
        from agentbench_platform.kongming_cases import goal_reference_spec
        reset_spec = (goal_reference_spec(args.case_spec)
                      if args.goal_reference and args.case_spec is not None else args.case_spec)
        env=gym.make(task,cfg=cfg,case_spec=reset_spec).unwrapped
        spec=scorer_spec(CANONICAL_SPEC,collision_boxes,TABLE_TOP_Z,case_spec=args.case_spec)
        cameras=NativeCameras(env,resources)
        robots=None
        state=IsaacState(env,spec)
        add_target_outlines(env,CANONICAL_SPEC,mode=args.mode if args.goal_reference else None)
    return env,cfg,state,spec,cameras,robots,fixture,initial_metadata,VIEWS


def create_dual_sharpa_environment(args, resources):
    """One shared construction path for runtime and engineering checks."""
    import gymnasium as gym
    import isaaclab_tasks
    import agentbench.tasks
    from agentbench.tasks.utils import parse_env_cfg
    from .native_cameras import add_cameras, add_target_outlines, NativeCameras
    from agentbench.tasks.manager_based.table_top_manipulation.config.kongming_lock.shapes import CANONICAL_SPEC, collision_boxes, TABLE_TOP_Z
    from agentbench.tasks.manager_based.table_top_manipulation.config.kongming_lock.kongming_sharpa_benchmark import KongmingDualSharpaState, VIEWS
    from agentbench.tasks.manager_based.table_top_manipulation.config.kongming_lock.sharpa_calibration import PRESET_SHA256
    from agentbench_platform.native_state import scorer_spec
    task_mode = ('disassemble' if args.mode == 'assemble' else 'assemble') if args.goal_reference else args.mode
    task = 'Agentbench-KongmingLock-DualSharpa-'+task_mode.capitalize()+'-Play-v0'
    cfg = parse_env_cfg(task, device=args.device, num_envs=1)
    from .evaluation_protocol import apply_visual_trial
    if args.environment_seed is not None:
        cfg.seed = args.environment_seed
    apply_visual_trial(cfg, getattr(args, 'evaluation_light_scale', None))
    if not args.case_reset_only:
        add_cameras(cfg, views=VIEWS)
    scene_case = args.case_spec
    if args.goal_reference:
        from copy import deepcopy
        scene_case = deepcopy(args.case_spec)
        scene_case['initial'] = deepcopy(scene_case['goal_state'])
    env = gym.make(task, cfg=cfg, case_spec=scene_case).unwrapped
    spec = scorer_spec(CANONICAL_SPEC, collision_boxes, TABLE_TOP_Z, case_spec=args.case_spec)
    spec.update(state_hash=args.case_spec['state_hash'], manifest_sha256=args.case_spec['manifest_sha256'],
                fixture_version='shape_v1.5', mount_calibration_sha256=PRESET_SHA256)
    state = KongmingDualSharpaState(env, mode=args.mode, spec=spec, case_id=args.case_id)
    cameras = (None if args.case_reset_only else
        NativeCameras(env, resources, views=VIEWS, physical_arrays=state.physical_arrays))
    robots = {'left_floating_sharpa': ('/World/envs/env_0/LeftSharpa', 'left_robot'),
              'right_floating_sharpa': ('/World/envs/env_0/RightSharpa', 'right_robot')}
    fixture = None
    initial_metadata = None
    add_target_outlines(env, CANONICAL_SPEC, mode=args.mode if args.goal_reference else None)
    return env,cfg,state,spec,cameras,robots,fixture,initial_metadata,VIEWS
