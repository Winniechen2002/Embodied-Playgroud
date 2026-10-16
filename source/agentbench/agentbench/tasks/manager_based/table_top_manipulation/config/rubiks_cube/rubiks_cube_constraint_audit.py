"""Independent audit of the declared hybrid fixture's USD joint transactions.

This verifies the entire 112-joint graph, exact membership exchanges, and frames
captured from current native measurements. It is NOT permission to grasp, turn,
or capture support: fresh motion/contact/stability guards must also pass before
the trusted runtime applies any proposed transaction. Joint readback is USD
authoring evidence; physical effectiveness is checked using subsequent PhysX
samples, not inferred from authoring or controller caches.
"""
from copy import deepcopy
import json

import numpy as np
from scipy.spatial.transform import Rotation

from .rubiks_cube_native_observation import NativeCubeSample
from .rubiks_cube_observer import classify_native_snapshot
from .rubiks_cube_rules import CubeState, FACE_AXIS_SIGN


def joint_graph():
    """Frozen relationship/type declarations, independent of mutable USD state."""
    result = {
        'world_core_anchor': ('world_anchor', 'core', None, True),
        'robot_hand_core_attachment': ('panda_hand', 'core', None, False),
    }
    for axis in 'xyz':
        result['carrier_hinge_'+axis] = ('core', 'carrier_'+axis, axis.upper(), True)
        result['carrier_transport_lock_'+axis] = ('core', 'carrier_'+axis, None, False)
    for name in CubeState.solved().pieces:
        result['core_anchor_'+name] = ('core', name, None, True)
        for axis in 'xyz':
            result['carrier_attachment_'+axis+'_'+name] = ('carrier_'+axis, name, None, False)
    return result


def _vector(value, size):
    array = np.asarray(value, dtype=float)
    if array.shape != (size,) or not np.isfinite(array).all():
        raise ValueError('Invalid joint frame')
    if size == 4 and abs(np.linalg.norm(array)-1.) > 1e-5:
        raise ValueError('Invalid joint quaternion')
    return array


def validate_joints(joints, *, initial=False):
    graph = joint_graph()
    if not isinstance(joints, dict) or set(joints) != set(graph):
        raise ValueError('Incomplete or undeclared cube joint graph')
    keys = {'enabled', 'body0', 'body1', 'position0', 'position1', 'quaternion0', 'quaternion1',
            'type', 'axis', 'lower_limit', 'upper_limit', 'drive_schemas',
            'collision_enabled', 'exclude_from_articulation'}
    for name, (body0, body1, axis, enabled) in graph.items():
        joint = joints[name]
        if not isinstance(joint, dict) or set(joint) != keys:
            raise ValueError('Incomplete joint readback: '+name)
        if (type(joint['enabled']) is not bool or joint['body0'] != body0 or joint['body1'] != body1
                or joint['type'] != ('PhysicsRevoluteJoint' if axis else 'PhysicsFixedJoint')
                or joint['axis'] != axis or joint['drive_schemas'] != []
                or joint['collision_enabled'] is not False or joint['exclude_from_articulation'] is not True
                or joint['lower_limit'] != ('-inf' if axis else None)
                or joint['upper_limit'] != ('inf' if axis else None)):
            raise ValueError('Undeclared joint configuration: '+name)
        if initial and joint['enabled'] != enabled:
            raise ValueError('Initial fixture is not anchored: '+name)
        for side in (0, 1):
            _vector(joint['position'+str(side)], 3)
            _vector(joint['quaternion'+str(side)], 4)
        # The implementation captures only frame 0; frame 1 is fixed identity.
        if (not np.allclose(joint['position1'], 0., atol=1e-8, rtol=0.)
                or abs(abs(float(joint['quaternion1'][0]))-1.) > 1e-8
                or not np.allclose(joint['quaternion1'][1:], 0., atol=1e-8, rtol=0.)):
            raise ValueError('Unexpected body-1 constraint frame: '+name)


def compare_joints(expected, measured):
    validate_joints(measured)
    frames = {'position0', 'position1', 'quaternion0', 'quaternion1'}
    for name, joint in expected.items():
        for key, value in joint.items():
            actual = measured[name][key]
            if key in frames:
                a, b = np.asarray(value), np.asarray(actual)
                if key.startswith('quaternion') and np.dot(a, b) < 0:
                    b = -b
                # USD stores single-precision joint frames. This allowance only
                # covers serialization roundoff, not the 1 mm physics tolerance.
                if not np.allclose(a, b, atol=2e-7, rtol=0.):
                    raise ValueError('Constraint frame does not match native capture: '+name)
            elif value != actual:
                raise ValueError('Unexpected constraint mutation: '+name+'.'+key)


def _poses(row):
    sample = NativeCubeSample(**row['native'])
    poses = dict(zip(sample.body_names, sample.native_link_transforms_xyzw))
    hand = row['robot']
    q = _vector(hand['hand_quaternion'], 4)
    poses['panda_hand'] = [*_vector(hand['hand_position'], 3), *q[1:], q[0]]
    return sample, poses


def _capture(joint, poses):
    a, b = np.asarray(poses[joint['body0']]), np.asarray(poses[joint['body1']])
    ra, rb = Rotation.from_quat(a[3:]), Rotation.from_quat(b[3:])
    q = (ra.inv()*rb).as_quat()
    joint['position0'] = ra.inv().apply(b[:3]-a[:3]).tolist()
    joint['quaternion0'] = q[[3,0,1,2]].tolist()


class ConstraintAudit:
    """Track only audited changes; neither agent phase labels nor backend caches."""
    def __init__(self, initial_joints):
        validate_joints(initial_joints, initial=True)
        self.joints = deepcopy(initial_joints)
        self._serialized = json.dumps(self.joints, sort_keys=True, allow_nan=False)
        self.state = 'idle'
        self.epoch = 0
        self.operation = None

    def verify_current(self, joints):
        # Consecutive USD reads serialize identically until an authored edit.
        # Avoid repeating 448 numerical frame comparisons at every substep.
        # The full validator still explains any mismatch, including tiny edits.
        if json.dumps(joints, sort_keys=True, allow_nan=False) != self._serialized:
            compare_joints(self.joints, joints)

    def _transaction(self, name, arguments, row):
        from agentbench_platform.mechanisms import validate_command
        validate_command(name, arguments)
        sample, poses = _poses(row)
        after = deepcopy(self.joints)
        state, operation = self.state, self.operation
        def require(condition):
            if not condition:
                raise ValueError('Constraint transition is out of order: '+name)
        def set_joint(key, enabled, capture=False):
            after[key]['enabled'] = enabled
            if capture:
                _capture(after[key], poses)
        if name == 'turn.begin':
            require(state == 'idle')
            measured, _ = classify_native_snapshot(sample.body_names, sample.native_link_transforms_xyzw,
                                                     ignore_center_twist=True)
            if measured is None:
                raise ValueError('Cannot select layer from invalid native geometry')
            face = arguments['move'][0]
            axis = FACE_AXIS_SIGN[face][0].lower()
            for cubie in measured.active_cubie_ids(face):
                set_joint('core_anchor_'+cubie, False)
                set_joint('carrier_attachment_'+axis+'_'+cubie, True, True)
            state, operation = 'turning', 'turn'
        elif name == 'turn.end':
            require(state == 'turning' and operation == 'turn')
            for key in after:
                if key.startswith('carrier_attachment_'):
                    set_joint(key, False)
                elif key.startswith('core_anchor_'):
                    set_joint(key, True, True)
            state, operation = 'idle', None
        elif name == 'transport.begin':
            require(state == 'idle')
            # World-from-core orientation includes the scene's continuous yaw;
            # the frozen short03/04 cases use 30 and 75 degrees respectively.
            target = np.asarray(arguments['target_frame'], dtype=float)
            if (not np.allclose(target.T @ target, np.eye(3), atol=1e-6, rtol=0.)
                    or abs(np.linalg.det(target)-1.) > 1e-6):
                raise ValueError('Transport target must be a proper world-from-core rotation')
            for axis in 'xyz':
                set_joint('carrier_hinge_'+axis, False)
                set_joint('carrier_transport_lock_'+axis, True, True)
            state, operation = 'transporting', 'transport'
        elif name == 'transport.attach':
            require(state == 'transporting' and operation == 'transport')
            set_joint('robot_hand_core_attachment', True, True)
            set_joint('world_core_anchor', False)
            state = 'attached'
        elif name == 'transport.capture_support':
            require(state == 'attached' and operation == 'transport')
            set_joint('world_core_anchor', True, True)
            set_joint('robot_hand_core_attachment', False)
            state = 'supported'
        elif name == 'transport.release':
            require(state == 'supported' and operation == 'transport')
            state = 'settling'
        elif name == 'transport.end':
            require(state == 'settling' and operation == 'transport')
            for axis in 'xyz':
                set_joint('carrier_transport_lock_'+axis, False)
                set_joint('carrier_hinge_'+axis, True)
            state, operation = 'idle', None
        elif name == 'detent.begin':
            require(state == 'idle')
            state, operation = 'settling', 'detent'
        elif name == 'detent.end':
            require(state == 'settling' and operation == 'detent')
            state, operation = 'idle', None
        else:
            raise ValueError('Unsupported joint transaction')
        return after, state, operation

    def expected_transaction(self, name, arguments, row):
        return self._transaction(name, arguments, row)[0]

    def accept(self, name, arguments, row, actual_joints):
        expected, state, operation = self._transaction(name, arguments, row)
        compare_joints(expected, actual_joints)
        self.joints = deepcopy(actual_joints)
        self._serialized = json.dumps(self.joints, sort_keys=True, allow_nan=False)
        self.state, self.operation = state, operation
        self.epoch += 1
