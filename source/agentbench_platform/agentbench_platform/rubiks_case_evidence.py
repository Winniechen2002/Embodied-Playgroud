"""Bind maintainer case metadata to the requested reset during trace replay."""
import importlib

from .rubiks_cases import case_evidence, public_reset_data
from .rubiks_physics import load_physics


def verify_case_binding(config):
    """Reject a public-case trace with another scramble, pose, hash or fixture.

    Native measurement validation still belongs to RubiksScorer. This check
    prevents a correctly scored episode from being attributed to another case.
    Legacy engineering episodes have no case binding and remain supported.
    """
    case_id = config.get('case_id')
    if case_id is None:
        if config.get('case') is not None:
            raise ValueError('case metadata requires a case_id')
        return None
    expected = case_evidence(case_id)
    if config.get('mode') != 'solve' or config.get('case') != expected:
        raise ValueError('public case journal identity mismatch')
    spec = config['physical_spec']
    physics = load_physics()
    initialization = importlib.import_module(physics.native.__package__+'.rubiks_cube_initialization')
    _, reset = initialization.prepare_initial_reset(public_reset_data(case_id),
        baseline_xy_m=(.7, 0.), table_height_m=spec['table_height_m'])
    # Recompute support Z and orientation with the same geometry source that
    # owns reset. No stored physical or symbolic trajectory is consulted.
    recorded = config['initialization']
    for key in ('requested_initial_config', 'support_geometry', 'target_core_position_xyz_m',
                'target_core_quaternion_wxyz', 'expected_facelets_urfdlb', 'expected_permutation_checksum'):
        if recorded.get(key) != reset[key]:
            raise ValueError('public case reset metadata mismatch: '+key)
    target = dict(position=reset['target_core_position_xyz_m'],
        quaternion=reset['target_core_quaternion_wxyz'],facelets_urfdlb=expected['expected_facelets_urfdlb'],
        permutation_checksum=expected['permutation_checksum'])
    if spec.get('initial_target') != target:
        raise ValueError('public case requested physical target mismatch')
    return expected
