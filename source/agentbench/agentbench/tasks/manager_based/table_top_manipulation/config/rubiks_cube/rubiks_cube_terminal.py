"""Independent physical terminal and sequence predicates, not episode authorization.

The trusted episode judge must also verify complete substep/constraint coverage
and absence of earlier hard failures. These functions never consume controller
phases, requested move indices or self-reported completion.
"""
import math

import numpy as np
from scipy.spatial.transform import Rotation

from .rubiks_cube_native_observation import (
    NativeCubeSample, evaluate_native_cube_window, measure_native_support_geometry,
)
from .rubiks_cube_rules import CubeState, parse_sequence


def sequence_goal(target_sequence, measured_events):
    """Compare events produced by MeasuredTurns, including cancelling quarters."""
    expected = [move.replace('-prime',"'") for move in parse_sequence(target_sequence)]
    if not expected:
        raise ValueError('Execution task needs a target sequence')
    actual = [event['move'] for event in measured_events]
    if any(move not in [f+s for f in 'URFDLB' for s in ('',"'")] for move in actual):
        raise ValueError('Measured event must be a quarter turn')
    matched = 0
    for a,b in zip(expected,actual):
        if a!=b:
            break
        matched += 1
    return dict(passed=actual==expected,expected_quarters=expected,actual_quarters=actual,
                matched_prefix_quarters=matched)


def evaluate_terminal_window(rows, *, initial_native, home_joint_positions,
                             arm_joint_ids, finger_joint_ids, table_height_m,
                             after_step=None):
    """Check measured pose, support, 31-body stationarity, release and robot home.

    ``initial_native`` is the runtime's accepted initialization reference.
    ``after_step`` is the most recent trusted constraint-transition boundary;
    no pre-transition sample may contribute to its 0.5 second stable window.
    """
    if not isinstance(initial_native,NativeCubeSample):
        raise TypeError('Accepted initial NativeCubeSample required')
    if not isinstance(rows,(list,tuple)) or len(rows)<2:
        raise ValueError('A native terminal window needs at least two samples')
    arm_ids,finger_ids = list(arm_joint_ids),list(finger_joint_ids)
    ids = arm_ids+finger_ids
    if (len(arm_ids)!=7 or len(finger_ids)!=2 or any(type(i) is not int for i in ids)
            or sorted(ids)!=list(range(9))):
        raise ValueError('Invalid frozen Panda joint indices')
    home = np.asarray(home_joint_positions,dtype=float)
    if home.shape!=(7,) or not np.isfinite(home).all():
        raise ValueError('Invalid public home joints')
    samples = [NativeCubeSample(**row['native']) for row in rows]
    if any(s.body_names!=initial_native.body_names for s in samples):
        raise ValueError('Native body ordering changed')
    boundary = initial_native.native_step if after_step is None else after_step
    if type(boundary) is not int or boundary<initial_native.native_step:
        raise ValueError('Invalid fresh-window boundary')
    if len(samples)<61:
        return dict(passed=False,reason='insufficient_stable_window',sample_count=len(samples))
    state, window = evaluate_native_cube_window(samples,physics_dt_s=1/120,after_step=boundary,
                                                ignore_center_twist=True)
    joints = []
    for row in rows:
        robot = row['robot']
        if robot['arm_joint_ids']!=arm_ids or robot['finger_joint_ids']!=finger_ids:
            raise ValueError('Native joint ordering changed')
        q = np.asarray(robot['joint_positions'],dtype=float)
        if q.shape!=(9,) or not np.isfinite(q).all():
            raise ValueError('Invalid measured robot joint vector')
        joints.append(q)
    joints = np.stack(joints)
    core = initial_native.body_names.index('core')
    initial = np.asarray(initial_native.native_link_transforms_xyzw)[core]
    cores = np.asarray([s.native_link_transforms_xyzw[core] for s in samples])
    position_error = np.linalg.norm(cores[:,:3]-initial[:3],axis=1)
    angle_error = (Rotation.from_quat(cores[:,3:])*Rotation.from_quat(initial[3:]).inv()).magnitude()
    support = measure_native_support_geometry(samples[-1],table_height_m=table_height_m,include_stickers=True)
    gates = dict(native_configuration=state is not None,stable=bool(window['stable']),
        returned_position=bool(np.max(position_error)<=.005+1e-12),
        returned_orientation=bool(np.max(angle_error)<=math.radians(2)+1e-12),
        fingers_open=bool(np.min(joints[:,finger_ids])>=.035-1e-12),
        arm_home=bool(np.max(np.abs(joints[:,arm_ids]-home))<=.05+1e-12),
        supported=abs(support['table_gap_m'])<=.002)
    return dict(passed=all(gates.values()),gates=gates,stable_window=window,support=support,
        max_return_position_error_m=float(np.max(position_error)),max_return_angle_error_rad=float(np.max(angle_error)),
        minimum_finger_position_m=float(np.min(joints[:,finger_ids])),
        maximum_home_joint_error_rad=float(np.max(np.abs(joints[:,arm_ids]-home))),
        cube=dict(valid=state is not None,solved=state is not None and state.facelet_string()==CubeState.solved().facelet_string(),
                  facelets_urfdlb=state.facelet_string() if state is not None else None))
