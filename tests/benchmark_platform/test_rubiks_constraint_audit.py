"""Raw joint transactions must match the declared graph and measured frames."""
from copy import deepcopy
from dataclasses import asdict

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from test_rubiks_measured_events import Trace, module


def row(trace):
    return dict(native=asdict(trace.sample()), robot=dict(
        hand_position=[.7, 0., .75], hand_quaternion=[1., 0., 0., 0.]))


def initial_joints(trace):
    joints = {}
    def add(name, a, b, enabled, axis=None):
        poses = {n: np.asarray(p) for n, p in zip(trace.names, trace.poses)}
        poses['panda_hand'] = np.array([.7, 0., .75, 0., 0., 0., 1.])
        joints[name] = dict(enabled=enabled, body0=a, body1=b,
            position0=(poses[b][:3]-poses[a][:3]).tolist(), quaternion0=[1.,0.,0.,0.],
            position1=[0.,0.,0.], quaternion1=[1.,0.,0.,0.],
            type='PhysicsRevoluteJoint' if axis else 'PhysicsFixedJoint',
            axis=axis, lower_limit='-inf' if axis else None,
            upper_limit='inf' if axis else None, drive_schemas=[],
            collision_enabled=False, exclude_from_articulation=True)
    add('world_core_anchor', 'world_anchor', 'core', True)
    add('robot_hand_core_attachment', 'panda_hand', 'core', False)
    for axis in 'xyz':
        add('carrier_hinge_'+axis, 'core', 'carrier_'+axis, True, axis.upper())
        add('carrier_transport_lock_'+axis, 'core', 'carrier_'+axis, False)
    for name in trace.names[:26]:
        add('core_anchor_'+name, 'core', name, True)
        for axis in 'xyz':
            add('carrier_attachment_'+axis+'_'+name, 'carrier_'+axis, name, False)
    return joints


def ledger():
    trace = Trace()
    return trace, module('rubiks_cube_constraint_audit').ConstraintAudit(initial_joints(trace))


def test_declared_joint_graph_and_each_atomic_exchange():
    trace, audit = ledger()
    assert len(audit.joints)==112
    before = deepcopy(audit.joints)
    after = audit.expected_transaction('turn.begin', {'move':'U'}, row(trace))
    selected = trace.state.active_cubie_ids('U')
    assert sum(j['enabled'] for n,j in after.items() if n.startswith('carrier_attachment_'))==9
    assert all(not after['core_anchor_'+n]['enabled'] for n in selected)
    audit.accept('turn.begin', {'move':'U'}, row(trace), after)
    assert audit.state=='turning' and audit.epoch==1 and audit.joints==after
    end = audit.expected_transaction('turn.end', {}, row(trace))
    audit.accept('turn.end', {}, row(trace), end)
    assert audit.state=='idle' and audit.epoch==2
    assert all(j['enabled']==before[n]['enabled'] for n,j in end.items())
    for name, arguments, state in [
        ('transport.begin', {'target_frame':np.eye(3).tolist()}, 'transporting'),
        ('transport.attach', {}, 'attached'),
        ('transport.capture_support', {}, 'supported'),
        ('transport.release', {}, 'settling'),
        ('transport.end', {}, 'idle'),
        ('detent.begin', {'axis':'x'}, 'settling'),
        ('detent.end', {}, 'idle'),
    ]:
        after = audit.expected_transaction(name, arguments, row(trace))
        audit.accept(name, arguments, row(trace), after)
        assert audit.state==state


@pytest.mark.parametrize('defect', ['extra', 'missing', 'drive', 'limited_hinge', 'wrong_body', 'enabled_hand'])
def test_initial_graph_rejects_undeclared_constraints(defect):
    trace=Trace(); joints=initial_joints(trace)
    if defect=='extra': joints['hidden_weld']=deepcopy(joints['world_core_anchor'])
    if defect=='missing': del joints['world_core_anchor']
    if defect=='drive': joints['carrier_hinge_x']['drive_schemas']=['PhysicsDriveAPI:angular']
    if defect=='limited_hinge': joints['carrier_hinge_x']['upper_limit']=90.
    if defect=='wrong_body': joints['world_core_anchor']['body0']='panda_hand'
    if defect=='enabled_hand': joints['robot_hand_core_attachment']['enabled']=True
    with pytest.raises(ValueError):
        module('rubiks_cube_constraint_audit').ConstraintAudit(joints)


@pytest.mark.parametrize('defect', ['unrecorded', 'wrong_layer', 'snap_frame', 'body_rewrite', 'joint_type', 'partial'])
def test_transactions_reject_changes_outside_exact_measured_exchange(defect):
    trace,audit=ledger(); saved=deepcopy(audit.joints)
    after=audit.expected_transaction('turn.begin', {'move':'U'}, row(trace))
    active=trace.state.active_cubie_ids('U')[0]
    if defect=='unrecorded': after['carrier_hinge_x']['enabled']=False
    if defect=='wrong_layer': after['core_anchor_'+next(n for n in trace.names[:26] if n not in trace.state.active_cubie_ids('U'))]['enabled']=False
    if defect=='snap_frame': after['carrier_attachment_z_'+active]['position0'][0]+=.002
    if defect=='body_rewrite': after['carrier_attachment_z_'+active]['body0']='panda_hand'
    if defect=='joint_type': after['carrier_hinge_z']['type']='PhysicsFixedJoint'
    if defect=='partial': after['core_anchor_'+active]['enabled']=True
    with pytest.raises(ValueError): audit.accept('turn.begin', {'move':'U'}, row(trace), after)
    assert audit.joints==saved and audit.epoch==0


def test_frames_are_captured_from_current_native_pose_and_hand():
    trace,audit=ledger()
    data=row(trace); data['robot']['hand_position'][0]+=.012
    unchanged=deepcopy(data)
    prepared=audit.expected_transaction('transport.begin', {'target_frame':np.eye(3).tolist()}, data)
    audit.accept('transport.begin', {'target_frame':np.eye(3).tolist()}, data, prepared)
    after=audit.expected_transaction('transport.attach', {}, data)
    assert after['robot_hand_core_attachment']['position0']==pytest.approx([-.012,0.,-.1145])
    assert after['robot_hand_core_attachment']['enabled'] and not after['world_core_anchor']['enabled']
    assert data==unchanged


@pytest.mark.parametrize('frame', [np.zeros((3,3)).tolist(), np.diag([1.,1.,-1.]).tolist()])
def test_transport_target_rejects_singular_or_reflected_frame(frame):
    trace,audit=ledger()
    with pytest.raises(ValueError): audit.expected_transaction('transport.begin', {'target_frame':frame}, row(trace))


@pytest.mark.parametrize('yaw',[30.,75.])
def test_transport_accepts_world_rotation_for_existing_yawed_regressions(yaw):
    trace,audit=ledger()
    frame=Rotation.from_euler('z',yaw,degrees=True).as_matrix().tolist()
    after=audit.expected_transaction('transport.begin',{'target_frame':frame},row(trace))
    assert all(after['carrier_transport_lock_'+axis]['enabled'] for axis in 'xyz')


def test_runtime_joint_readback_detects_out_of_band_edits_and_copies_inputs():
    trace,audit=ledger(); readback=deepcopy(audit.joints)
    audit.verify_current(readback)
    readback['world_core_anchor']['position0'][0]=1.
    with pytest.raises(ValueError): audit.verify_current(readback)
    assert audit.joints['world_core_anchor']['position0'][0]==0.
    with pytest.raises(ValueError): audit.expected_transaction('transport.attach', {}, row(trace))
