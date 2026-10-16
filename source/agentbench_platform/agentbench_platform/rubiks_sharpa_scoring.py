"""Measured task scorer for the declared floating-Sharpa hybrid cube mechanism.

The historical reset-only scorer remains available for historical trace replay.
This scorer requires fresh native motion, contact, constraint and terminal evidence.
"""
import math
import numpy as np
from scipy.spatial.transform import Rotation

from .rubiks_scoring import RubiksScorer
from .rubiks_sharpa_reset import SharpaResetScorer, _array

FINGERS=('right_thumb_elastomer','right_index_elastomer','right_middle_elastomer',
         'right_ring_elastomer','right_pinky_elastomer')


class SharpaRubiksScorer(RubiksScorer):
    def __init__(self,mode,spec,initialization,*,initialization_after_step,target_sequence=None):
        SharpaResetScorer.__init__(self,mode,spec,initialization,
            initialization_after_step=initialization_after_step,target_sequence=target_sequence)
        self.target_sequence=None
        self.fixture=self.physics.constraints.ConstraintAudit(self.initial['mechanism']['joints'])
        for row in initialization:
            self.fixture.verify_current(row['mechanism']['joints'])
            if row['mechanism']['state']!='idle' or row['mechanism']['epoch']!=0:
                raise ValueError('Sharpa initialization mechanism is not idle')
        self.turns=self.physics.events.MeasuredTurns(self.initial_native,
            hand_quaternion_wxyz=self.initial['robot']['hand_quaternion'])
        self.terminal=dict(passed=False,reason='insufficient_stable_window')
        self.peak_contact_force_n=0.
        self.turn_request=None;self.turn_event_count=0;self.transport=None

    def _validate_row(self,row):
        native=SharpaResetScorer._validate_row(self,row)
        robot=row['robot']
        if (robot['joint_ids']!=list(self.joint_ids) or robot['finger_joint_ids']!=list(self.finger_ids)
                or robot['motion_joint_ids']!=self.spec['motion_joint_ids']):
            raise ValueError('Sharpa joint identity changed')
        if row['mechanism']['version']!='hybrid_fixture_v1':
            raise ValueError('Sharpa fixture version mismatch')
        self._contact_vectors(row)
        return native

    def _contact_vectors(self,row):
        names=sorted(n for n in self.initial_native.body_names if n.startswith('cubie_'))
        contacts=row['finger_contacts']
        if len(contacts)!=5:raise ValueError('Five native fingertip sensors required')
        for name,contact in zip(FINGERS,contacts):
            if contact['finger']!=name or contact['cubie_names']!=names:
                raise ValueError('Sharpa contact identity changed')
        return np.stack([_array(c['forces_w'],(26,3),'contact forces') for c in contacts])

    def _contact_pair(self,row):
        # Keep all five sensors in the audit. The turn detector uses the two
        # opposed groups: thumb and the other fingertips, never Panda joints.
        forces=np.linalg.norm(self._contact_vectors(row),axis=2).sum(axis=1)
        return [float(forces[0]),float(forces[1:].max())]

    def _grasp_ready(self,row):
        forces=self._contact_vectors(row).sum(axis=1)
        thumb,others=forces[0],forces[1:].sum(axis=0)
        a,b=np.linalg.norm(thumb),np.linalg.norm(others)
        return bool(a>.5 and b>.5 and np.dot(thumb,others)/(a*b)<-.5)

    def _released(self,row):
        q=_array(row['robot']['joint_positions'],(28,),'joint positions')
        home=_array(self.spec['home_joint_positions'],(28,),'home joints')
        home_by_id=dict(zip(self.joint_ids,home))
        return bool(max(self._contact_pair(row))<=.1 and
                    max(abs(q[i]-home_by_id[i]) for i in self.finger_ids)<=.05)

    def _terminal_window(self):
        rows=list(self.rows)
        samples=[self.physics.native.NativeCubeSample(**r['native']) for r in rows]
        state,window=self.physics.native.evaluate_native_cube_window(samples,
            physics_dt_s=1/120,after_step=self.after_step,ignore_center_twist=True)
        core=self.initial_native.body_names.index('core')
        initial=np.asarray(self.initial_native.native_link_transforms_xyzw[core])
        poses=np.asarray([s.native_link_transforms_xyzw[core] for s in samples])
        position=np.linalg.norm(poses[:,:3]-initial[:3],axis=1)
        angle=(Rotation.from_quat(poses[:,3:])*Rotation.from_quat(initial[3:]).inv()).magnitude()
        joints=np.asarray([r['robot']['joint_positions'] for r in rows])[:,self.joint_ids]
        home=np.asarray(self.spec['home_joint_positions'])
        support=self.physics.native.measure_native_support_geometry(samples[-1],
            table_height_m=self.spec['table_height_m'],include_stickers=True)
        gates=dict(native_configuration=state is not None,stable=bool(window['stable']),
            returned_position=bool(position.max()<=.005+1e-12),
            returned_orientation=bool(angle.max()<=math.radians(2)+1e-12),
            fingers_released=all(self._released(r) for r in rows),
            robot_home=bool(np.max(np.abs(joints-home))<=.05+1e-12),
            supported=abs(support['table_gap_m'])<=.002)
        return dict(passed=all(gates.values()),gates=gates,stable_window=window,support=support,
            cube=dict(valid=state is not None,solved=state is not None and
                state.facelet_string()==self.physics.rules.CubeState.solved().facelet_string()))

    def result(self):
        result=super().result()
        result['detection_scope']='31 native bodies, 28 Sharpa joints, five fingertip sensors, declared cube USD joints'
        return result
