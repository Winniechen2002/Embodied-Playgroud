"""Private stationary native-sample fixtures; no move sequence or solution trace."""
from copy import deepcopy
from dataclasses import asdict
import numpy as np
from scipy.spatial.transform import Rotation
from .rubiks_physics import load_physics
from .rubiks_cases import get_case
from .rubiks_scoring import RubiksScorer
from .rubiks_sharpa_scoring import SharpaRubiksScorer,FINGERS


def _setup(task, wrong=False):
    physics=load_physics();case=get_case(task['case_id'])
    state=physics.rules.CubeState.solved()
    if wrong:state=state.apply_sequence(case['scramble'].split())
    names=tuple(sorted(state.pieces))+('world_anchor','core','carrier_x','carrier_y','carrier_z')
    center=np.array([*case['center_xy_m'],.6355])
    rotation=Rotation.from_euler('z',case['yaw_rad']).as_matrix() @ np.array(case['logical_orientation'])
    poses=np.zeros((31,7));poses[:,:3]=center;poses[:,3:]=Rotation.from_matrix(rotation).as_quat()
    for i,name in enumerate(names[:26]):
        piece=state.pieces[name]
        poses[i,:3]+=rotation @ (np.array(piece.position)*.024)
        poses[i,3:]=Rotation.from_matrix(rotation @ np.array(piece.orientation)).as_quat()
    pose_by_name=dict(zip(names,poses));pose_by_name['panda_hand']=np.array([.7,0,.75,0,0,0,1.])
    joints={}
    def add(name,a,b,enabled,axis=None):
        pa,pb=pose_by_name[a],pose_by_name[b]
        ra,rb=Rotation.from_quat(pa[3:]).as_matrix(),Rotation.from_quat(pb[3:]).as_matrix()
        q=Rotation.from_matrix(ra.T @ rb).as_quat()[[3,0,1,2]].tolist()
        joints[name]=dict(enabled=enabled,body0=a,body1=b,position0=(ra.T @ (pb[:3]-pa[:3])).tolist(),
            quaternion0=q,position1=[0.,0.,0.],quaternion1=[1.,0.,0.,0.],
            type='PhysicsRevoluteJoint' if axis else 'PhysicsFixedJoint',axis=axis,
            lower_limit='-inf' if axis else None,upper_limit='inf' if axis else None,
            drive_schemas=[],collision_enabled=False,exclude_from_articulation=True)
    add('world_core_anchor','world_anchor','core',True)
    add('robot_hand_core_attachment','panda_hand','core',False)
    for axis in 'xyz':
        add('carrier_hinge_'+axis,'core','carrier_'+axis,True,axis.upper())
        add('carrier_transport_lock_'+axis,'core','carrier_'+axis,False)
    for name in names[:26]:
        add('core_anchor_'+name,'core',name,True)
        for axis in 'xyz':add('carrier_attachment_'+axis+'_'+name,'carrier_'+axis,name,False)
    sharpa=task['family']=='rubiks_sharpa'
    def row(native_step,episode_step):
        sample=physics.native.NativeCubeSample(native_step,native_step/120,names,poses.copy(),np.zeros((31,6)))
        robot=dict(joint_positions=[0.]*28 if sharpa else [0.]*7+[.04,.04],
            joint_velocities=[0.]*(28 if sharpa else 9),hand_position=[.7,0.,.75],hand_quaternion=[1.,0.,0.,0.])
        robot.update(dict(joint_ids=list(range(28)),motion_joint_ids=list(range(6)),finger_joint_ids=list(range(6,28)))
            if sharpa else dict(arm_joint_ids=list(range(7)),finger_joint_ids=[7,8]))
        return dict(control_step=(episode_step+3)//4,physics_step=episode_step,native=asdict(sample),
            robot=robot,finger_contacts=[dict(finger=n,cubie_names=list(names[:26]),forces_w=np.zeros((26,3)).tolist(),
                net_w=[0.,0.,0.]) for n in (FINGERS if sharpa else ('left','right'))],
            mechanism=dict(version='hybrid_fixture_v1',state='idle',epoch=0,joints=deepcopy(joints)),
            submitted_targets=dict(arm=[0.]*7,fingers=[.04,.04]))
    spec=dict(table_height_m=.6,home_joint_positions=[0.]*(28 if sharpa else 7),
        initial_target=dict(position=center.tolist(),quaternion=Rotation.from_matrix(rotation).as_quat()[[3,0,1,2]].tolist(),
            facelets_urfdlb=state.facelet_string(),permutation_checksum=state.permutation_checksum()))
    spec.update(dict(embodiment='floating-sharpa',joint_ids=list(range(28)),motion_joint_ids=list(range(6)),finger_joint_ids=list(range(6,28)))
        if sharpa else dict(embodiment='franka-panda',arm_joint_ids=list(range(7)),finger_joint_ids=[7,8]))
    scorer=(SharpaRubiksScorer if sharpa else RubiksScorer)('solve',spec,
        [row(i,0) for i in range(1,62)],initialization_after_step=0)
    return scorer,row


def check(task):
    def feed(scorer,row,start,count,violation=False):
        for control in range(start,start+count):
            samples=[]
            for step in range(4*control-3,4*control+1):
                sample=row(61+step,step)
                if violation and step==1:sample['finger_contacts'][0]['forces_w'][0][0]=20.1
                scorer.audit_substep(sample);samples.append(sample)
            scorer.update(samples[-1],samples)
        return scorer.result()
    scorer,row=_setup(task)
    assert not scorer.result()['success']
    assert not feed(scorer,row,1,15)['success']
    assert feed(scorer,row,16,1)['success']
    scorer,row=_setup(task,wrong=True)
    assert not feed(scorer,row,1,16)['success']
    scorer,row=_setup(task)
    result=feed(scorer,row,1,16,violation=True)
    assert result['hard_failure'] and not result['success']
    return dict(case_id=task['case_id'],pose_checked=True,legal_goal=True,wrong_goal_rejected=True,
        stable_short_rejected=True,first_violation_latched=True,scope='scorer_endpoint_only')
