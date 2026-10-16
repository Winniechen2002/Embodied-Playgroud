"""Explicit nested public schemas; unspecified keys are discarded at every level."""
import math
from dataclasses import dataclass

CAPABILITY_VERSION = '2026-10-09-environment-l0-l3'
TOOL_MIN_LEVEL = {
    'cube_solver': 1, 'graspnet': 2, 'graspnet_cpu': 2,
    'depth_pro': 1, 'depth_anything_3': 1, 'sam_3d_objects': 1,
    'stream3d': 1, 'pyroki': 1, 'curobo': 1, 'ompl': 1,
    'pinocchio': 1, 'proxy_dynamics': 1,
}


@dataclass(frozen=True)
class RunProfile:
    observation: str = 'privileged'
    tools: tuple[str, ...] = ()
    experience: str = 'none'
    capability_level: int | None = None
    capability_profile_version: str | None = None

    def __post_init__(self):
        if self.observation not in ('privileged', 'rgb', 'rgbd'):
            raise ValueError('Unknown observation profile')
        if self.experience not in ('none', 'reference'):
            raise ValueError('Unknown experience profile')
        if not isinstance(self.tools, tuple) or any(not isinstance(n, str) or not n for n in self.tools):
            raise ValueError('Tools must be a tuple of names')
        if len(set(self.tools)) != len(self.tools):
            raise ValueError('Duplicate tool name')
        if self.capability_level is None:
            if self.capability_profile_version is not None:
                raise ValueError('A capability version requires an explicit level')
            return
        if type(self.capability_level) is not int or self.capability_level not in range(4):
            raise ValueError('Capability level must be an integer from 0 through 3')
        if self.capability_profile_version != CAPABILITY_VERSION:
            raise ValueError('Unsupported capability profile version')
        if self.observation == 'privileged' and self.capability_level != 3:
            raise ValueError('Privileged observations require Level 3')
        if self.capability_level == 0 and self.observation != 'rgb':
            raise ValueError('Level 0 exposes RGB and proprioception only')
        if self.experience != 'none':
            raise ValueError('Environment release profiles do not import reference experience')
        for name in self.tools:
            if name not in TOOL_MIN_LEVEL or TOOL_MIN_LEVEL[name] > self.capability_level:
                raise ValueError('Tool is not authorized at this capability level')

    def public_record(self):
        record = dict(observation=self.observation, tools=list(self.tools), experience=self.experience)
        if self.capability_level is not None:
            record.update(capability_level=self.capability_level,
                          capability_profile_version=self.capability_profile_version)
        return record


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def numeric(value):
    return number(value) or isinstance(value, (list, tuple)) and all(numeric(v) for v in value)


def _fields(data, numeric_keys=(), text_keys=(), bool_keys=(), text_lists=()):
    if not isinstance(data, dict):
        return {}
    out = {k: data[k] for k in numeric_keys if k in data and numeric(data[k])}
    out.update({k: data[k] for k in text_keys if isinstance(data.get(k), str)})
    out.update({k: data[k] for k in bool_keys if type(data.get(k)) is bool})
    out.update({k: list(data[k]) for k in text_lists if isinstance(data.get(k), (list, tuple))
                and all(isinstance(v, str) for v in data[k])})
    return out


POSE = ('position', 'quaternion', 'linear_velocity', 'angular_velocity', 'mass_kg', 'dimensions_m')
CALIBRATION = ('intrinsics', 'extrinsics', 'position', 'quaternion', 'world_from_camera', 'near_m', 'far_m', 'pixel_center_offset')
ROBOT = ('joint_positions', 'joint_velocities', 'measured_finger_positions', 'previous_action')


def _named(data, cleaner):
    return {name: cleaner(value) for name, value in data.items() if isinstance(name, str)} if isinstance(data, dict) else {}


def camera(data, profile):
    out = _fields(data, ('width', 'height', 'capture_step'), ('rgb_resource_id', 'capture_id'))
    out['calibration'] = _fields(data.get('calibration'), CALIBRATION, ('convention',))
    if profile != 'rgb':
        out.update(_fields(data, (), ('depth_resource_id', 'validity_resource_id', 'depth_units')))
    return out


def sanitize_snapshot(raw, profile, camera_ids=()):
    if (not isinstance(raw, dict) or type(raw.get('step_index')) is not int
            or raw['step_index'] < 0 or not number(raw.get('simulation_time_s'))
            or raw['simulation_time_s'] < 0 or type(raw.get('terminated')) is not bool
            or type(raw.get('truncated')) is not bool):
        raise ValueError('Backend snapshot lacks valid clock or termination fields')
    out = _fields(raw, ('step_index', 'simulation_time_s'), bool_keys=('terminated', 'truncated'))
    if 'physics_step_count' in raw:
        if type(raw['physics_step_count']) is not int or raw['physics_step_count']<0:
            raise ValueError('Invalid physics step counter')
        out['physics_step_count']=raw['physics_step_count']
    out['robots'] = _named(raw.get('robots'), lambda r: _fields(r, ROBOT, text_lists=('joint_names',)))
    cameras = raw.get('cameras', {})
    out['cameras'] = {name: camera(cameras[name], profile.observation) for name in camera_ids
                      if name in cameras and isinstance(cameras[name], dict)}
    if 'mechanism' in raw:
        from .mechanisms import public_state
        out['mechanism'] = public_state(raw['mechanism'])
    if profile.observation == 'privileged':
        physical = raw.get('privileged', {})
        physics = physical.get('physics')
        physics = physics if isinstance(physics,dict) else {}
        out['privileged'] = {
            'pieces': _named(physical.get('pieces'), lambda p: _fields(p, POSE)),
            'robot_bodies': _named(physical.get('robot_bodies'), lambda p: _fields(p, POSE + ('com_position',))),
            'jacobians': _named(physical.get('jacobians'), lambda j: j if numeric(j) else []),
            'contacts': [_fields(c, ('position', 'normal', 'force_n', 'force_vector_n', 'impulse_ns', 'penetration_m'),
                                  ('body_a', 'body_b')) for c in physical.get('contacts', []) if isinstance(c, dict)],
            'geometry': _named(physical.get('geometry'), lambda g: _fields(g, ('vertices', 'faces', 'half_extents', 'center', 'collision_boxes', 'voxel_size_m'))),
            'physics': {**_fields(physical.get('physics'), ('physics_hz', 'control_hz', 'gravity', 'friction', 'restitution', 'timestep_s')),
                'rigid_bodies': _named(physics.get('rigid_bodies'),lambda p: _fields(p,
                    ('mass_kg','inertia_kg_m2','material_static_dynamic_restitution','contact_offset_m','rest_offset_m','shape_indices'),text_lists=('body_names',)))},
            'diagnostics': _fields(physical.get('diagnostics'), ('clearance_m', 'penetration_m', 'max_penetration_m')),
        }
        if 'cube' in physical:
            out['privileged']['cube'] = _fields(physical['cube'], text_keys=('facelets_urfdlb', 'source'), bool_keys=('valid',))
    return out


def action_bounds(values):
    """JSON null denotes a native continuous joint's unbounded endpoint."""
    if not isinstance(values,(list,tuple)) or not all(v is None or number(v) for v in values):
        raise ValueError('Invalid action bound')
    return list(values)


def sanitize_description(raw, profile):
    out = {'version': 1, 'profile': profile.public_record(),
           'task': _fields(raw.get('task'), ('max_steps',), ('id', 'task_id', 'name', 'family', 'mode', 'description', 'case_id', 'subtask', 'embodiment'), text_lists=('target_pieces',)),
           'action_spec': _fields(raw.get('action_spec'), ('size', 'low', 'high', 'neutral_action',
                'control_period_s','physics_period_s'), text_lists=('names', 'semantics')),
           'goal': _fields(raw.get('goal'), ('position_tolerance_m', 'angular_tolerance_rad', 'penetration_ceiling_m', 'stable_controls',
               'return_position_tolerance_m', 'return_angle_tolerance_rad', 'stable_seconds',
               'finger_open_min_m', 'home_joint_tolerance_rad'), ('description', 'mode'))}
    for name in ('low','high'):
        out['action_spec'][name]=action_bounds(raw.get('action_spec',{}).get(name))
    if out['task'].get('family') == 'rubiks_cube' and out['task'].get('mode') == 'execute_sequence':
        from .tasks import validate_task
        out['task']['target_sequence'] = validate_task('rubiks_cube', 'execute_sequence', raw['task'].get('target_sequence'))
    if out['task'].get('family') == 'marble':
        task = raw['task']
        variation = task.get('variation_request', {})
        if (task.get('task_metadata_version') != 'public-spring-v1'
                or not number(variation.get('spring_stiffness')) or variation['spring_stiffness'] <= 0
                or variation.get('spring_stiffness_unit') != 'N/m'):
            raise ValueError('Missing public spring metadata')
        out['task'].update(task_metadata_version='public-spring-v1',variation_request={
            'spring_stiffness':variation['spring_stiffness'],'spring_stiffness_unit':'N/m'})
    def robot(r):
        out = _fields(r, ('joint_limits', 'base_position', 'base_quaternion', 'default_joint_positions', 'joint_action_scale', 'soft_joint_limits'), ('model',), text_lists=('joint_names',))
        if 'joint_limits' in r:
            limits=r['joint_limits']
            if not isinstance(limits,(list,tuple)) or any(not isinstance(pair,(list,tuple)) or len(pair)!=2 for pair in limits):
                raise ValueError('Invalid joint limits')
            out['joint_limits']=[action_bounds(pair) for pair in limits]
        out['kinematics'] = _fields(r.get('kinematics'), ('dh_parameters', 'joint_axes', 'joint_origins', 'link_transforms', 'base_transform'), text_lists=('link_names',))
        out['calibration'] = _fields(r.get('calibration'), CALIBRATION)
        return out
    out['robots'] = _named(raw.get('robots'), robot)
    out['cameras'] = _named(raw.get('cameras'), lambda c: {**_fields(c, ('width', 'height'), ('model',)), 'calibration': _fields(c.get('calibration'), CALIBRATION, ('convention',))})
    if 'mechanism' in raw:
        from .mechanisms import description
        if out['task'].get('family') != 'rubiks_cube':
            raise ValueError('Mechanism requires a declared Rubik task')
        out['mechanism'] = description(raw['mechanism'])
    return out


def sanitize_result(raw):
    if (not isinstance(raw, dict)
            or any(type(raw.get(k)) is not bool for k in ('success', 'terminated', 'truncated'))
            or not number(raw.get('score')) or type(raw.get('step_count')) is not int
            or raw['step_count'] < 0):
        raise ValueError('Backend finish result lacks valid required summary fields')
    # No free-form reason/detail strings: score summary cannot expose host state.
    return {'version': 1, **{k: raw[k] for k in ('success', 'score', 'step_count', 'terminated', 'truncated')}}
