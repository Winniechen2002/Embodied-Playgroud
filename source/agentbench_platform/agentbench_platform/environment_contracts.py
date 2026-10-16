"""Source-bound native action projection and concrete scoring contracts."""
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from .environment_catalog import ROOT,CONFIG,digest

VERSION='environment-contract-v3'


@lru_cache(maxsize=1)
def action_contracts():
    data=json.loads(Path(__file__).with_name('action_contracts.json').read_text())
    for name,expected in data['sources'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('Native action projection needs revalidation: '+name)
    return data['records']


def contract(task, configuration, *, _native_records=None):
    from .evaluation_protocol import budgets
    family=task['family']
    key=family+'/'+task['embodiment']+('/'+task['case_id'] if family.startswith('maniskill_') else '')
    native=deepcopy((action_contracts() if _native_records is None else _native_records)[key])
    action=native['action_spec']
    if task['action_spec']['size'] is not None and action['size']!=task['action_spec']['size']:raise ValueError('Native action dimension mismatch')
    action['units']='Per-component target mappings in semantics; rotational joint targets use radians, prismatic targets use metres.'
    if family=='marble':
        scoring=dict(required_targets='all except protected indices',order=configuration.get('target_order',[]),
            protected_indices=configuration.get('protected',[]),minimum_toppled=configuration.get('min_toppled',0),
            required_fractures=configuration.get('fracture_required',[]),damage_sources=configuration.get('damage_sources',{}),
            damage_window_s=.03,protected_observation_seconds=3. if configuration.get('protected') else 0.,
            impulse_thresholds_N_s=configuration.get('thresholds',[.018]*len(configuration['targets'])),
            target_threshold_comparison='strict accumulated impulse > threshold',
            stability_seconds=3. if configuration.get('protected') else 0.)
        source='source/agentbench/agentbench_mujoco/campaign_env.py'
    elif family.startswith('hanoi_'):
        scoring=dict(goal_ring_pegs=list(configuration['goal']),initial_ring_pegs=list(configuration['start']),
            stable_seconds=1.,seat_xy_tolerance_m=.022,seat_z_tolerance_m=.016,penetration_limit_m=.005,
            rules=['top_ring_only','smaller_on_larger','finite_state','workspace_bounds'],first_violation_sticky=True,
            gripper_closed_half_width_m=configuration['gripper_closed_half_width'] if family=='hanoi_panda' else None)
        source='source/agentbench/agentbench_hanoi40/rules.py'
    elif family=='pocket_cube':
        from .environment_catalog import source_module
        cube=source_module('_contract_cube',ROOT/'source/agentbench/agentbench_cube20','catalog')
        authored=cube.BY_ID[task['case_id']]
        scoring=dict(goal=list(authored.goal.as_vector()),initial=list(authored.start.as_vector()),
            expected_committed_quarter_turns=len(cube.moves(authored.transition)),stable_seconds=1.,
            detent_tolerance_degrees=1.,angular_speed_limit_rad_s=.05,active_face=-1,
            penetration_limit_m=.00025,immutable_scene_fingerprint=True,physical_goal_required=True,first_violation_sticky=True)
        source='source/agentbench/agentbench_cube20/evaluation.py'
    elif family.startswith('rubiks_'):
        scoring=dict(goal='uniform face colors',stable_seconds=.5,core_home_position_tolerance_m=.005,
            core_home_rotation_tolerance_degrees=2.,arm_home_tolerance_rad=.05,support_gap_m=.002,
            maximum_contact_force_n=20.,
            release=({'contact_force_max_n':.1,'finger_home_tolerance_rad':.05} if family=='rubiks_sharpa'
                else {'finger_open_min_m':.035}),
            mechanism='hybrid_fixture_v1',physical_cube_measurement_required=True,first_violation_sticky=True)
        source='source/agentbench_platform/agentbench_platform/'+('rubiks_sharpa_scoring.py' if family=='rubiks_sharpa' else 'rubiks_scoring.py')
    elif family=='kongming_lock':
        assembly=task['mode']=='assemble'
        scoring=dict(goal_state=configuration['goal_state'],target_pieces=configuration['target_pieces'],
            initial_state=configuration['initial'],stable_seconds=2. if assembly else 1.,
            position_tolerance_m=.0075 if assembly else .025,angle_tolerance_rad=.08 if assembly else .25,
            linear_speed_limit_m_s=.01,angular_speed_limit_rad_s=.1,penetration_limit_m=.002,
            support_tolerance_m=.002,finger_open_min_m=.035,tcp_clearance_min_m=.13,
            forbidden_contact_force_limit_n=.5,complete_substep_coverage=True,first_violation_sticky=True)
        if task['embodiment']=='dual-floating-sharpa':
            scoring.pop('finger_open_min_m')
            scoring.update(finger_home_tolerance_rad=.05)
        source='source/agentbench_platform/agentbench_platform/kongming_scoring.py'
    elif family.startswith('maniskill_'):
        scoring=dict(final=deepcopy(configuration['final']),milestones=deepcopy(configuration['milestones']),
            protected=configuration['protected'],protected_joints=configuration.get('protected_joints',[]),
            forbidden=configuration.get('forbidden',[]),history_rules=configuration.get('history_rules',[]),
            stable_seconds=1.,linear_speed_limit_m_s=.025,angular_speed_limit_rad_s=.15,
            prismatic_speed_limit_m_s=.008,revolute_speed_limit_rad_s=.03,
            release_force_n=.05,protected_position_tolerance_m=.025,protected_angle_tolerance_degrees=20.,
            protected_prismatic_tolerance_m=.008,protected_revolute_tolerance_rad=.045,
            no_fall_min_height_m=.035,dropped_object_latch_height_m=.025,
            held_goal_objects=configuration.get('held_goal_objects',[]),complete_substep_coverage=True,
            first_violation_sticky=True)
        source='env/maniskill_lgd/agentbench_maniskill/'+task['suite']+'/oracle.py'
    elif family=='bookshelf':
        scoring=dict(stable_seconds=.5,containment_tolerance_m=.002,support_tolerance_m=.004,
            upright_tolerance_degrees=10.,still_linear_m_s=.03,still_angular_rad_s=.15,
            book_pack_max_gap_m=.006,book_pack_alignment_degrees=3.,display_min_gap_m=.05,
            display_wall_margin_m=.02,frame_facing_degrees=20.,release_distance_m=.05,release_force_n=.1,
            arm_speed_limit_rad_s=[2.175]*4+[2.61]*3,arm_speed_factor_limit=1.1,
            penetration_limit_m=.005,wall_anchor=configuration['wall_anchor'],layer_rules=configuration['layer_rules'],
            first_violation_sticky=True)
        source=str((CONFIG/'organize_bookshelf/mdp.py').relative_to(ROOT))
    else:raise ValueError('Unregistered scoring contract')
    # Keep environment definitions; omit historical runner command strings.
    initial={k:deepcopy(v) for k,v in configuration.items() if not k.endswith('_command') and k not in ('plan','yaw_plan','reference')}
    result=dict(version=VERSION,action_spec=action,robots=native['robots'],budgets=budgets(task),
        observation_spec=dict(
            clock=dict(step_index='integer control steps',physics_step_count='integer physics substeps',simulation_time_s='seconds'),
            proprioception=['robots.<id>.joint_positions','robots.<id>.joint_velocities','robots.<id>.previous_action'],
            proprioception_units='radians and radians/second for revolute joints; metres and metres/second for prismatic joints',
            rgb=dict(encoding='PNG' if family=='marble' else 'raw uint8 RGB',width=640,height=400 if family=='marble' else 480,minimum_level=0),
            depth=(dict(available=False) if family=='marble' else dict(available=True,
                encoding='little-endian float32 metres with uint8 validity mask',width=640,height=480,minimum_level=1)),
            calibration=['intrinsics','world_from_camera','convention','near_m','far_m','pixel_center_offset'],
            calibration_values='Measured for each initialization and attached to every authorized camera capture',
            privileged_fields=(['pieces.<name>.position','pieces.<name>.quaternion','pieces.<name>.linear_velocity',
                'pieces.<name>.angular_velocity','physics.physics_hz','physics.control_hz'] if family.startswith('maniskill_')
                else ['pieces','robot_bodies','jacobians','contacts','geometry','physics','diagnostics']),
            privileged_minimum_level=3,unknown_fields='denied',read_only=True),
        initial_definition=initial,goal=deepcopy(task['goal']),scoring=scoring,
        termination=dict(success='goal and required continuous stability with no prior violation',
            violation='first violation terminates and denies success',timeout='budget exhausted without qualified success',
            finish='owner/client submission evaluates existing evidence; no extra physics or stability credit'),
        scorer_source=source,scorer_sha256=hashlib.sha256((ROOT/source).read_bytes()).hexdigest())
    result['sha256']=digest(result)
    return result
