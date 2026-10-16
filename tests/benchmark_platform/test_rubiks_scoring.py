"""Episode-level native evidence, rather than controller claims, decides success."""
from copy import deepcopy
from dataclasses import asdict
import sys

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from test_rubiks_constraint_audit import initial_joints
from test_rubiks_measured_events import Trace
from test_rubiks_state import ROOT

sys.path.insert(0, str(ROOT/'source/agentbench'))


def snapshot(trace, physics, joints, *, forces=(0.,0.), epoch=0, state='idle'):
    contacts=[]
    for side,force in zip(('left','right'),forces):
        vectors=np.zeros((26,3)); vectors[0,0]=force
        contacts.append(dict(finger=side,cubie_names=list(trace.names[:26]),
                             forces_w=vectors.tolist(),net_w=[force,0.,0.]))
    return dict(control_step=(physics+3)//4,physics_step=physics,native=asdict(trace.sample()),
        robot=dict(joint_positions=[0.]*7+[.04,.04], joint_velocities=[0.]*9,
            arm_joint_ids=list(range(7)),finger_joint_ids=[7,8],
            hand_position=[.7,0.,.75],hand_quaternion=trace.hand.tolist()),
        finger_contacts=contacts,mechanism=dict(version='hybrid_fixture_v1',state=state,epoch=epoch,joints=deepcopy(joints)),
        submitted_targets=dict(arm=[0.]*7,fingers=[.04,.04]))


def setup(mode='solve', sequence=None):
    from agentbench_platform.rubiks_scoring import RubiksScorer
    trace=Trace(); joints=initial_joints(trace); initialization=[]
    for i in range(1,62):
        trace.step=i; initialization.append(snapshot(trace,0,joints))
    spec=dict(table_height_m=.6,home_joint_positions=[0.]*7,arm_joint_ids=list(range(7)),finger_joint_ids=[7,8])
    scorer=RubiksScorer(mode,spec,initialization,initialization_after_step=0,target_sequence=sequence)
    return trace,joints,scorer


def controls(trace,joints,scorer,count=16, mutate=None):
    for control in range(1,count+1):
        samples=[]
        for substep in range(4):
            trace.step+=1; step=(control-1)*4+substep+1
            sample=snapshot(trace,step,joints)
            if mutate: mutate(sample)
            samples.append(sample);scorer.audit_substep(sample)
        scorer.update(samples[-1],samples)
    return scorer.result()


def test_already_solved_requires_fresh_full_endpoint_and_complete_substeps():
    trace,joints,scorer=setup()
    assert not scorer.result()['success']
    result=controls(trace,joints,scorer)
    assert result['success'] and result['coverage_complete'] and result['observed_substeps']==64
    assert result['measured_quarters']==[]


@pytest.mark.parametrize('defect',['force','missing','duplicate','native_gap','joint_edit','labels','fingers'])
def test_episode_rejects_prior_hard_violation_or_incomplete_evidence(defect):
    trace,joints,scorer=setup()
    def corrupt(s):
        if defect=='labels': s.update(move_index=999,phase='DONE',success=True)
        if s['physics_step']==1:
            if defect=='force': s['finger_contacts'][0]['forces_w'][0][0]=20.1
            if defect=='native_gap': s['native']['native_step']+=1
            if defect=='joint_edit': s['mechanism']['joints']['world_core_anchor']['enabled']=False
        if defect=='fingers': s['robot']['joint_positions'][7]=.01
    if defect in ('missing','duplicate'):
        trace.step+=1
        first=snapshot(trace,1,joints)
        if defect=='duplicate': scorer.audit_substep(first);scorer.audit_substep(first)
        result=controls(trace,joints,scorer)
    else: result=controls(trace,joints,scorer,mutate=corrupt)
    assert result['success'] is (defect=='labels')
    if defect not in ('labels','fingers'): assert result['hard_failure']


def test_sequence_cancellation_gets_no_credit_for_idle_solved_cube():
    trace,joints,scorer=setup('execute_sequence',['U',"U'"])
    result=controls(trace,joints,scorer)
    assert result['terminal']['passed'] and not result['success']
    assert result['sequence']['matched_prefix_quarters']==0


def test_initialization_must_be_full_raw_stable_evidence():
    from agentbench_platform.rubiks_scoring import RubiksScorer
    trace,joints,scorer=setup()
    with pytest.raises(ValueError):
        RubiksScorer('solve',scorer.spec,[snapshot(trace,0,joints)],initialization_after_step=0)


def test_mechanism_epoch_cannot_change_without_audited_transaction():
    trace,joints,scorer=setup()
    result=controls(trace,joints,scorer,mutate=lambda s:s['mechanism'].update(epoch=1))
    assert result['hard_failure'] and not result['success']


class Episode:
    def __init__(self, sequence=('U',)):
        self.trace,self.joints,self.scorer=setup('execute_sequence',list(sequence))
        self.steps=0; self.pending=[]
        self.fingers=[.04,.04]
        self.hand_position=[.7,0.,.75]

    def tick(self, forces=(0.,0.)):
        self.trace.step+=1; self.steps+=1
        s=snapshot(self.trace,self.steps,self.joints,forces=forces,
                   epoch=self.scorer.fixture.epoch,state=self.scorer.fixture.state)
        s['robot']['joint_positions'][7:]=self.fingers
        s['robot']['hand_position']=self.hand_position
        self.pending.append(s); self.scorer.audit_substep(s)
        if self.steps%4==0:
            self.scorer.update(s,self.pending); self.pending=[]
        assert not self.scorer.hard_failure,self.scorer.result()['failure_reasons']

    def settle(self, count=64, forces=(0.,0.)):
        for _ in range(count): self.tick(forces)
        while self.steps%4: self.tick(forces)

    def command(self, name, arguments=None):
        arguments=arguments or {}
        before=deepcopy(self.scorer.last_row)
        proposed=self.scorer.mechanism_plan(name,arguments)
        _,state,_=self.scorer.fixture._transaction(name,arguments,before)
        after=deepcopy(before)
        after['mechanism'].update(joints=proposed,state=state,epoch=self.scorer.fixture.epoch+1)
        event=dict(name=name,arguments=arguments,before=before,after=after,
            result=dict(accepted=True,state=state,epoch=self.scorer.fixture.epoch+1),
            control_step=self.scorer.last_control,physics_step=self.scorer.observed_substeps)
        self.scorer.mechanism_event(event)
        assert not self.scorer.hard_failure,self.scorer.result()['failure_reasons']
        self.joints=proposed

    def turn(self, move):
        self.command('turn.begin',{'move':move})
        axis='XYZ'.index(self.trace.rules.FACE_AXIS_SIGN[move[0]][0])
        delta=(-1 if len(move)==1 else 1)*self.trace.rules.FACE_AXIS_SIGN[move[0]][1]*np.pi/2
        for angle in np.linspace(0.,delta,91)[1:]:
            self.trace.poses=self.trace._poses(move[0],angle)
            vector=np.zeros(3);vector[axis]=angle
            self.trace.hand=Rotation.from_rotvec(vector).as_quat()[[3,0,1,2]]
            self.tick((2.,2.))
        self.settle(forces=(2.,2.))
        self.trace.state=self.trace.state.apply_move(move)
        self.command('turn.end')
        self.settle()


def test_full_measured_quarter_commits_only_after_motion_and_fresh_windows():
    episode=Episode();episode.settle()
    episode.turn('U')
    result=episode.scorer.result()
    assert result['success'] and result['measured_quarters']==['U']
    assert result['fixture_epoch']==2


def test_public_inverse_command_matches_measured_event():
    episode=Episode(("U'",));episode.settle()
    episode.turn("U'")
    result=episode.scorer.result()
    assert result['success'] and result['measured_quarters']==["U'"]
    assert result['fixture_epoch']==2


def test_turn_end_without_motion_and_attach_without_contacts_are_rejected():
    episode=Episode();episode.settle();episode.command('turn.begin',{'move':'U'})
    episode.settle()
    with pytest.raises(ValueError,match='measured requested quarter'):
        episode.scorer.mechanism_plan('turn.end',{})
    other=Episode();other.settle()
    other.command('transport.begin',{'target_frame':np.eye(3).tolist()});other.settle()
    with pytest.raises(ValueError,match='bilateral grasp'):
        other.scorer.mechanism_plan('transport.attach',{})


def test_each_constraint_switch_invalidates_previously_stable_endpoint():
    episode=Episode();episode.settle()
    episode.command('detent.begin',{'axis':'x'})
    with pytest.raises(ValueError,match='Fresh stable window'):
        episode.scorer.mechanism_plan('detent.end',{})
    episode.settle();episode.command('detent.end')
    assert not episode.scorer.result()['terminal']['passed']


def test_transport_needs_real_grasp_lift_support_and_release_without_turn_credit():
    e=Episode();e.settle()
    target=Rotation.from_euler('z',90,degrees=True)
    e.command('transport.begin',{'target_frame':np.rint(target.as_matrix()).tolist()})
    e.fingers=[.032,.032];e.settle(forces=(2.,2.));e.command('transport.attach')
    e.settle(forces=(2.,2.))
    with pytest.raises(ValueError,match='4 cm lift'):
        e.scorer.mechanism_plan('transport.capture_support',{})
    anchor=e.trace.poses[e.trace.names.index('world_anchor')].copy()
    center=e.trace.core_position.copy()
    def move(z,angle):
        e.trace.core_position=center+[0.,0.,z]
        r=Rotation.from_euler('z',angle,degrees=True)
        e.trace.core_rotation=r.as_matrix(); e.trace.poses=e.trace._poses()
        e.trace.poses[e.trace.names.index('world_anchor')]=anchor
        e.trace.hand=r.as_quat()[[3,0,1,2]]
        e.hand_position=(e.trace.core_position+r.apply([0.,0.,.1145])).tolist()
        e.tick((2.,2.))
    for z in np.linspace(0,.045,61)[1:]: move(z,0.)
    for angle in np.linspace(0,90,91)[1:]: move(.045,angle)
    for z in np.linspace(.045,0,61)[1:]: move(z,90.)
    e.settle(forces=(2.,2.)); e.command('transport.capture_support')
    e.fingers=[.04,.04];e.settle();e.command('transport.release')
    e.settle();e.command('transport.end')
    assert e.scorer.fixture.state=='idle' and not e.scorer.hard_failure
    assert e.scorer.turns.events==[]


def test_accepted_receipt_cannot_bypass_measurement_gate():
    e=Episode();e.settle();e.command('transport.begin',{'target_frame':np.eye(3).tolist()});e.settle()
    before=deepcopy(e.scorer.last_row);after=deepcopy(before)
    after['mechanism'].update(joints=e.scorer.fixture.expected_transaction('transport.attach',{},before),
                             state='attached',epoch=2)
    e.scorer.mechanism_event(dict(name='transport.attach',arguments={},before=before,after=after,
        result=dict(accepted=True,state='attached',epoch=2),control_step=e.scorer.last_control,
        physics_step=e.scorer.observed_substeps))
    assert e.scorer.hard_failure and not e.scorer.coverage_complete
