"""Public initialization input and requested-versus-native diagnostics.

Keep this module in the same import namespace as its reset/rules dependencies.
Controller input crosses into the runtime package as plain JSON data only.
"""
from __future__ import annotations

from copy import deepcopy
import math
from numbers import Real

try:
    from .rubiks_cube_reset import CubeResetSpec, build_reset_core_transform, reset_support_center_z
    from .rubiks_cube_rules import CubeFrame, CubeState, parse_sequence
except ImportError:  # Dependency-light standalone tools.
    from rubiks_cube_reset import CubeResetSpec, build_reset_core_transform, reset_support_center_z
    from rubiks_cube_rules import CubeFrame, CubeState, parse_sequence


_INITIAL_KEYS = {'center_xy_m', 'logical_orientation', 'yaw_rad', 'tilt_xy_rad', 'scramble'}


def _finite(value, label):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f'{label} must be a finite real')
    try:
        converted = float(value)
    except OverflowError as error:
        raise ValueError(f'{label} must be a finite real') from error
    if not math.isfinite(converted):
        raise ValueError(f'{label} must be a finite real')
    return converted


def _vector(value, length, label):
    if not isinstance(value, (list, tuple)) or len(value) != length:
        raise ValueError(f'{label} must contain {length} finite reals')
    return tuple(_finite(item, label) for item in value)


def prepare_initial_reset(data, *, baseline_xy_m, table_height_m):
    """Validate and snapshot JSON input; compute support from configured table."""
    if not isinstance(data, dict):
        raise ValueError('initial config must be a JSON object')
    if set(data) - _INITIAL_KEYS:
        raise ValueError(f'unknown initial config keys: {sorted(set(data) - _INITIAL_KEYS)}')
    baseline = _vector(baseline_xy_m, 2, 'baseline_xy_m')
    xy = _vector(data.get('center_xy_m', baseline), 2, 'center_xy_m')
    if any(abs(value - origin) > .05 + 2 * math.ulp(origin) for value, origin in zip(xy, baseline)):
        raise ValueError('center_xy_m must be within configured baseline +/- 0.05 m')
    matrix = data.get('logical_orientation', CubeFrame.identity().logical_to_world)
    if (not isinstance(matrix, (tuple, list)) or len(matrix) != 3
            or any(not isinstance(row, (tuple, list)) or len(row) != 3 for row in matrix)
            or any(type(value) is not int for row in matrix for value in row)):
        raise ValueError('logical_orientation must be a proper 3x3 integer cube frame')
    frame = CubeFrame(tuple(tuple(row) for row in matrix))
    if frame not in CubeFrame.all():
        raise ValueError('logical_orientation must be a proper cube frame')
    yaw = _finite(data.get('yaw_rad', 0.), 'yaw_rad')
    tilt = _vector(data.get('tilt_xy_rad', (0., 0.)), 2, 'tilt_xy_rad')
    scramble = data.get('scramble', '')
    if not isinstance(scramble, str):
        raise ValueError('scramble must be a legal move string')
    moves = parse_sequence(scramble)
    state = CubeState.solved().apply_sequence(moves)
    provisional = CubeResetSpec(state, frame, (*xy, 0.), yaw, tilt)
    table_height = _finite(table_height_m, 'table_height_m')
    z = reset_support_center_z(provisional, table_height_m=table_height, include_stickers=True)
    spec = CubeResetSpec(state, frame, (*xy, z), yaw, tilt)
    return spec, {
        'requested_initial_config': {
            'center_xy_m': list(xy), 'logical_orientation': [list(row) for row in matrix],
            'yaw_rad': yaw, 'tilt_xy_rad': list(tilt), 'scramble': ' '.join(moves),
        },
        'support_geometry': {'include_stickers': True, 'table_height_m': table_height,
                             'convention': 'lowest_cubie_or_sticker_box_on_configured_table'},
        'target_core_position_xyz_m': list(spec.center_position),
        'target_core_quaternion_wxyz': list(build_reset_core_transform(spec).quaternion),
        'expected_facelets_urfdlb': state.facelet_string(),
        'expected_permutation_checksum': state.permutation_checksum(),
    }


def initial_scene_parameters(cfg):
    """Read the baseline and horizontal cuboid table surface from task config."""
    core = cfg.scene.cube_parts.rigid_objects['core'].init_state
    table = cfg.scene.table
    rotation = _vector(table.init_state.rot, 4, 'table rotation')
    if rotation not in ((1., 0., 0., 0.), (-1., 0., 0., 0.)):
        raise ValueError('configured initial pose requires a horizontal unrotated cuboid table')
    size = _vector(table.spawn.size, 3, 'table size')
    if any(value <= 0 for value in size):
        raise ValueError('table size must be positive')
    position = _vector(table.init_state.pos, 3, 'table position')
    return _vector(core.pos, 3, 'configured core position')[:2], position[2] + .5 * size[2]


def evaluate_configured_initial_reset(spec, native_result):
    """Compare independent native results to the fixed requested state and pose."""
    target = build_reset_core_transform(spec)
    observation = native_result.get('native_observation') or {}
    measured = native_result.get('measured_state')
    state_matches = measured is not None and measured == spec.cube_state
    position_error = rotation_error = None
    try:
        position = _vector(observation.get('final_core_world_position_xyz_m'), 3, 'native core position')
        quaternion = _vector(observation.get('final_core_world_quaternion_wxyz'), 4, 'native core quaternion')
        norm = math.hypot(*quaternion)
        if abs(norm - 1.) > 1e-5:
            raise ValueError('native core quaternion must be normalized')
        position_error = math.dist(position, target.position)
        alignment = abs(sum(a * b / norm for a, b in zip(quaternion, target.quaternion)))
        rotation_error = 2. * math.acos(min(1., alignment))
    except ValueError:
        pass
    pose_matches = (position_error is not None and rotation_error is not None
                    and position_error <= .001 + 1e-12
                    and rotation_error <= math.radians(2.) + 1e-12)
    required_bodies = set(spec.cube_state.pieces) | {'core', 'world_anchor', 'carrier_x', 'carrier_y', 'carrier_z'}
    native_valid = (
        native_result.get('success') is True
        and observation.get('source') == 'native_physx_link_transforms'
        and observation.get('status') == 'valid'
        and observation.get('ready') is True
        and observation.get('stable') is True
        and observation.get('duration_s', 0.) >= .5 - 1e-12
        and observation.get('first_native_step', -1) > observation.get('after_native_step', math.inf)
        and set(observation.get('body_diameter_reports', {})) == required_bodies
    )
    reason = native_result.get('abort_reason')
    if reason is None:
        if not native_valid:
            reason = 'initial_native_window_invalid'
        elif not state_matches:
            reason = 'initial_state_mismatch'
        elif not pose_matches:
            reason = 'initial_core_pose_mismatch'
    return {
        'success_tolerance_met': reason is None,
        'abort_reason': reason,
        'initial_state_matches_requested': state_matches,
        'initial_core_pose_matches_requested': pose_matches,
        'initial_core_position_error_m': position_error,
        'initial_core_orientation_error_rad': rotation_error,
        'initial_core_position_tolerance_m': .001,
        'initial_core_orientation_tolerance_rad': math.radians(2.),
        'target_core_position_xyz_m': list(target.position),
        'target_core_quaternion_wxyz': list(target.quaternion),
        'expected_facelets_urfdlb': spec.cube_state.facelet_string(),
        'expected_permutation_checksum': spec.cube_state.permutation_checksum(),
        'actual_raw_initial_reference': deepcopy(observation),
    }
