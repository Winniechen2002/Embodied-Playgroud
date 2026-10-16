"""Reconstruct physical quarter turns without tokens, controller stages or caches.

This module is a component of the independent judge. It is not an episode
success predicate: support, return pose, release, robot home and constraint
audits are separate gates. Every call consumes one consecutive 120 Hz sample.
"""
from collections import deque
import math

import numpy as np
from scipy.spatial.transform import Rotation

from .rubiks_cube_native_observation import NativeCubeSample, evaluate_native_cube_window
from .rubiks_cube_observer import classify_native_snapshot
from .rubiks_cube_rules import FACE_AXIS_SIGN, evaluate_quarter_turn


def local_poses(sample):
    poses = np.asarray(sample.native_link_transforms_xyzw)
    core = sample.body_names.index('core')
    rotations = Rotation.from_quat(poses[:,3:]).as_matrix()
    return ((poses[:,:3]-poses[core,:3]) @ rotations[core],
            rotations[core].T @ rotations, rotations[core])


def hand_rotation(quaternion):
    q = np.asarray(quaternion,dtype=float)
    if q.shape!=(4,) or not np.isfinite(q).all() or abs(np.linalg.norm(q)-1)>1e-3:
        raise ValueError('Invalid measured hand quaternion')
    return Rotation.from_quat(q[[1,2,3,0]]).as_matrix()


class MeasuredTurns:
    """Measured motion plus fresh stable endpoints; ordinary center roll is free.

    Only motion is used to identify face and direction. Contact and wrist
    evidence end at the last entry into the quarter-turn tolerance band. The
    independent all-body rest window may occur after release/carrier settling;
    controller-provided rotation/release phase labels are never consumed.
    """
    def __init__(self, initial, *, hand_quaternion_wxyz):
        if not isinstance(initial,NativeCubeSample):
            raise TypeError('NativeCubeSample required')
        state, diagnostics = classify_native_snapshot(initial.body_names,initial.native_link_transforms_xyzw,
                                                       ignore_center_twist=True)
        if state is None:
            raise ValueError('Initial native cube state is invalid')
        self.names = initial.body_names
        self.indices = {name:i for i,name in enumerate(self.names)}
        self.last = initial
        self.measured_state = state
        self.reference = initial
        self.reference_positions,self.reference_rotations,core_rotation = local_poses(initial)
        self.quiet_hand = core_rotation.T @ hand_rotation(hand_quaternion_wxyz)
        self.previous_hand = self.quiet_hand
        self.quiet_sample = initial
        self.events = []
        self.window = deque(maxlen=61)
        self.active = None
        self.pending_motion = []
        self.failure = None
        self.after_step = initial.native_step
        self.non_centers = [self.indices[n] for n,p in state.pieces.items() if len(p.stickers)>1]

    def invalidate_window(self, native_step):
        """Trusted owner calls this after an audited constraint change, never the agent."""
        if type(native_step) is not int or native_step != self.last.native_step:
            raise ValueError('Constraint window invalidation must use the current native step')
        self.after_step = native_step
        self.window.clear()

    def _fail(self, reason):
        self.failure = reason
        raise ValueError(reason)

    def _stable(self):
        if len(self.window)<61:
            return None
        poses = np.asarray([s.native_link_transforms_xyzw for s in self.window])
        # Cheap necessary conditions; the exact all-pairs window check below
        # retains the existing 1 mm / 1 degree criteria for all 31 bodies.
        if np.any(np.ptp(poses[:,:,:3],axis=0)> .001+1e-12):
            return None
        q = poses[:,:,3:]; q = q/np.linalg.norm(q,axis=2,keepdims=True)
        angles = 2*np.arccos(np.clip(np.abs(np.sum(q*q[0],axis=2)),-1.,1.))
        if np.max(angles)>math.radians(1)+1e-10:
            return None
        state, report = evaluate_native_cube_window(list(self.window),physics_dt_s=1/120,
            after_step=self.after_step,ignore_center_twist=True)
        return (state,report) if state is not None and report['stable'] else None

    def observe(self, sample, *, hand_quaternion_wxyz, finger_contact_forces_n):
        if self.failure is not None:
            raise ValueError(self.failure)
        if (not isinstance(sample,NativeCubeSample) or sample.body_names!=self.names
                or sample.native_step!=self.last.native_step+1
                or abs(sample.native_time_s-self.last.native_time_s-1/120)>2e-6):
            self._fail('Noncontiguous native turn evidence')
        forces = np.asarray(finger_contact_forces_n,dtype=float)
        if forces.shape!=(2,) or not np.isfinite(forces).all() or np.min(forces)<0:
            self._fail('Invalid measured contact pair')
        if np.max(forces)>20.:
            self._fail('excessive_contact_force')
        positions, rotations, core_rotation = local_poses(sample)
        hand = core_rotation.T @ hand_rotation(hand_quaternion_wxyz)
        delta = rotations @ np.swapaxes(self.reference_rotations,1,2)
        vectors = Rotation.from_matrix(delta).as_rotvec()
        self.window.append(sample)
        self.last = sample
        if self.active is None:
            if np.max(np.linalg.norm(vectors[self.non_centers],axis=1))<=math.radians(1)+1e-10:
                self.quiet_hand = hand
                self.previous_hand = hand
                self.quiet_sample = sample
                self.pending_motion.clear()
                return None
            candidates = []
            for face,(axis,sign) in FACE_AXIS_SIGN.items():
                active = [self.indices[n] for n in self.measured_state.active_cubie_ids(face)
                          if len(self.measured_state.pieces[n].stickers)>1]
                rest = [i for i in self.non_centers if i not in active]
                column = 'XYZ'.index(axis)
                angle = float(np.median(vectors[active,column]))
                residual = vectors[active].copy(); residual[:,column] -= angle
                if (abs(angle)>math.radians(1) and np.max(np.linalg.norm(residual,axis=1))<math.radians(3)
                        and np.max(np.linalg.norm(vectors[rest],axis=1))<math.radians(3)):
                    candidates.append((face,column,active,angle))
            if not candidates and np.max(np.linalg.norm(vectors[self.non_centers],axis=1))<math.radians(3):
                # One cubie can cross 1 degree before its layer median does.
                # Within the existing layer-residual tolerance this is not yet
                # a classifiable turn. Retain every contact/wrist increment;
                # waiting must not erase evidence used by eventual scoring.
                increment = Rotation.from_matrix(hand @ self.previous_hand.T).as_rotvec()
                self.pending_motion.append((sample.native_step,forces.tolist(),increment))
                self.previous_hand = hand
                return None
            if len(candidates)!=1:
                self._fail('Native motion does not identify one face layer')
            face,axis,indices,angle = candidates[0]
            self.active = dict(face=face,axis=axis,indices=indices,angle=0.,wrapped=0.,
                wrist=0.,start=self.quiet_sample,history=[],intermediate=False,near_step=None)
            for step,contact,increment in self.pending_motion:
                self.active['wrist'] += float(increment[axis])
                self.active['history'].append((step,contact,self.active['wrist']))
            self.pending_motion.clear()
        turn = self.active
        axis = turn['axis']
        # Project the measured active-layer rotation onto its intrinsic axis.
        a,b = (axis+1)%3,(axis+2)%3
        matrices = delta[turn['indices']]
        wrapped = float(np.median(np.arctan2(matrices[:,b,a]-matrices[:,a,b],
                                            matrices[:,a,a]+matrices[:,b,b])))
        increment = math.atan2(math.sin(wrapped-turn['wrapped']),math.cos(wrapped-turn['wrapped']))
        turn['angle'] += increment; turn['wrapped'] = wrapped
        wrist_increment = Rotation.from_matrix(hand @ self.previous_hand.T).as_rotvec()[axis]
        turn['wrist'] += float(wrist_increment); self.previous_hand = hand
        turn['history'].append((sample.native_step,forces.tolist(),turn['wrist']))
        turn['intermediate'] |= math.radians(3)<abs(turn['angle'])<math.radians(87)
        if abs(abs(turn['angle'])-math.pi/2)<=math.radians(3)+1e-12:
            if turn['near_step'] is None:
                turn['near_step'] = sample.native_step
        else:
            turn['near_step'] = None
        if abs(turn['angle'])>math.radians(120):
            self._fail('quarter_turn_safety_guard')
        stable = self._stable()
        if stable is None:
            return None
        state, window = stable
        if abs(turn['angle'])<=math.radians(3) and state.facelet_string()==self.measured_state.facelet_string():
            self._accept_reference(sample,state,positions,rotations,hand)
            return None  # A cancelled partial turn supplies no quarter-turn credit.
        move = turn['face'] + ("'" if turn['angle']*FACE_AXIS_SIGN[turn['face']][1]>0 else '')
        if not turn['intermediate']:
            self._fail('Missing intermediate quarter-turn motion')
        expected = self.measured_state.apply_move(move)
        cutoff = min(window['first_native_step'],turn['near_step'] or window['first_native_step'])
        history = [row for row in turn['history'] if row[0]<=cutoff]
        if not history:
            self._fail('Missing pre-stability contact and wrist history')
        core = self.indices['core']; carrier = self.indices['carrier_'+'xyz'[axis]]
        start = np.asarray(turn['start'].native_link_transforms_xyzw)
        poses = np.asarray(sample.native_link_transforms_xyzw)
        start_r = Rotation.from_quat(start[core,3:]).as_matrix()
        rest = [self.indices[n] for n in self.measured_state.pieces
                if n not in self.measured_state.active_cubie_ids(turn['face'])]
        angular_velocity = np.asarray(sample.raw_com_velocities)[carrier,3:]-np.asarray(sample.raw_com_velocities)[core,3:]
        metrics = evaluate_quarter_turn(move=move,initial_angle_rad=0.,final_angle_rad=turn['angle'],
            final_angular_velocity_rad_s=float(angular_velocity @ core_rotation[:,axis]),
            left_contact_forces_n=[row[1][0] for row in history],right_contact_forces_n=[row[1][1] for row in history],
            wrist_axis_delta_rad=history[-1][2],core_pose_error_m=float(np.linalg.norm(poses[core,:3]-start[core,:3])),
            active_cubie_alignment_error_m=window['classifier_diagnostics']['max_position_residual_m'],
            non_active_cubie_displacement_m=float(np.max(np.linalg.norm(positions[rest]-self.reference_positions[rest],axis=1))),
            permutation_matches=state.facelet_string()==expected.facelet_string(),native_pose_window_valid=True,
            core_orientation_error_rad=float(Rotation.from_matrix(core_rotation @ start_r.T).magnitude()),
            max_contact_force_n=float(np.max([row[1] for row in turn['history']])),contact_force_limit_n=20.)
        if not metrics['success_tolerance_met']:
            self._fail(metrics['abort_reason'])
        event = dict(move=move,start_native_step=turn['start'].native_step,end_native_step=sample.native_step,
            motion_end_native_step=cutoff,motion_cutoff_rule='last_entry_quarter_tolerance_band',
            before_facelets=self.measured_state.facelet_string(),after_facelets=state.facelet_string(),
            metrics=metrics,stable_window=window)
        self.events.append(event)
        self._accept_reference(sample,state,positions,rotations,hand)
        return event

    def _accept_reference(self,sample,state,positions,rotations,hand):
        self.measured_state = state
        self.reference = sample
        self.reference_positions,self.reference_rotations = positions,rotations
        self.quiet_hand = self.previous_hand = hand
        self.quiet_sample = sample
        self.active = None
        self.pending_motion.clear()
