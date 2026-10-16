"""Native Isaac Lab runtime with measured, read-only task evidence."""
from __future__ import annotations
import copy
from itertools import combinations
import gymnasium as gym
import numpy as np
import torch
from isaaclab.envs import ManagerBasedEnv
from .shapes import (CANONICAL_SPEC, GRID_CELL_M, TABLE_TOP_Z, LOCK_CENTER_XY,
    LockPhase, PuzzleState, TaskMode, collision_boxes)
from .evaluation import quaternion_matrix, box_pair_clearance, goal_predicates, lattice_motion_diagnostics, FORBIDDEN_CONTACT_LABELS


class KongmingLockEnv(ManagerBasedEnv, gym.Env):
    lock_piece_names=CANONICAL_SPEC.piece_names

    def __init__(self,cfg,*,task_mode=TaskMode.DISASSEMBLE,case_spec=None,**kwargs):
        task_mode = TaskMode(task_mode)
        # Keep caller-owned config reusable across assembly/disassembly.
        cfg = copy.deepcopy(cfg)
        if cfg.scene.num_envs != 1:
            raise ValueError('v0 evidence evaluator supports num_envs=1')
        self.task_mode=task_mode
        self.case_spec=copy.deepcopy(case_spec) if case_spec is not None else None
        self.case_id=self.case_spec.get('case_id') if self.case_spec else None
        self.case_subtask=self.case_spec.get('subtask','complete') if self.case_spec else 'complete'
        self.case_target_pieces=tuple(self.case_spec.get('target_pieces',())) if self.case_spec else ()
        self.puzzle_state=PuzzleState(mode=task_mode)
        for piece in CANONICAL_SPEC.pieces:
            cfg_piece = getattr(cfg.scene, 'piece_' + piece.name)
            if self.case_spec is None:
                position = piece.target_position if task_mode is TaskMode.ASSEMBLE else piece.assembly_position
                quaternion = piece.target_quat_wxyz if task_mode is TaskMode.ASSEMBLE else piece.assembly_quat_wxyz
            else:
                position, quaternion = self.case_spec['initial'][piece.name]
            cfg_piece.init_state.pos = tuple(position)
            cfg_piece.init_state.rot = tuple(quaternion)
        self._privileged_events=[]
        self._max_penetration_m=0.
        self._step_count=0;self._stable_steps=0;self._last_audit={};self._max_arm_contact_n=0.
        self._max_finger_unfiltered_n=0.
        super().__init__(cfg=cfg,**kwargs)
        self.lock_removed_mask=torch.zeros((1,6),device=self.device)
        self.lock_placed_mask=torch.zeros((1,6),device=self.device)
        self.lock_assembled_mask=torch.zeros((1,6),device=self.device)
        self.lock_phase_one_hot=torch.zeros((1,len(LockPhase)),device=self.device)
        self.lock_max_penetration_m=torch.zeros(1,device=self.device)
        self._set_phase(LockPhase.DISASSEMBLED if self.task_mode is TaskMode.ASSEMBLE else LockPhase.ASSEMBLED)
        self._local_cells={}
        self._collision_boxes={p.name:collision_boxes(p) for p in CANONICAL_SPEC.pieces}
        for p in CANONICAL_SPEC.pieces:
            points=np.asarray(p.cells)*GRID_CELL_M+np.array([*LOCK_CENTER_XY,TABLE_TOP_Z])+GRID_CELL_M*.5
            points[:,2]+=4*GRID_CELL_M
            self._local_cells[p.name]=(points-p.assembly_position)@quaternion_matrix(p.assembly_quat_wxyz)

    def _set_phase(self,phase):
        self.puzzle_state.phase=phase
        if hasattr(self,'lock_phase_one_hot'):
            self.lock_phase_one_hot.zero_();self.lock_phase_one_hot[:,list(LockPhase).index(phase)]=1.

    def reset(self,*args,**kwargs):
        self.puzzle_state=PuzzleState(mode=self.task_mode)
        self._privileged_events=[];self._max_penetration_m=0.;self._stable_steps=0;self._step_count=0;self._max_arm_contact_n=0.
        self._max_finger_unfiltered_n=0.
        self.lock_removed_mask.zero_();self.lock_placed_mask.zero_();self.lock_assembled_mask.zero_();self.lock_max_penetration_m.zero_()
        self._set_phase(LockPhase.DISASSEMBLED if self.task_mode is TaskMode.ASSEMBLE else LockPhase.ASSEMBLED)
        result=super().reset(*args,**kwargs)
        # Reset teleports the initial robot joints but does not solve a new
        # physics step. PhysX force buffers still describe the preceding pose.
        # Audit geometry now; start force history with the first real step.
        self._audit(contacts_fresh=False)
        return result

    def step(self,action):
        hook = getattr(self, 'benchmark_substep_hook', None)
        if hook is not None:
            # Same installed ManagerBasedEnv CPU PhysX loop, with explicit
            # observation-only rendering and fresh post-update substep evidence.
            self.action_manager.process_action(action.to(self.device))
            self.recorder_manager.record_pre_step()
            for _ in range(self.cfg.decimation):
                self._sim_step_counter += 1
                self.action_manager.apply_action()
                self.scene.write_data_to_sim()
                self.sim.step(render=False)
                self.scene.update(dt=self.physics_dt)
                hook()
            if 'interval' in self.event_manager.available_modes:
                self.event_manager.apply(mode='interval', dt=self.step_dt)
            self.obs_buf = self.observation_manager.compute(update_history=True)
            self.recorder_manager.record_post_step()
            self._step_count += 1
            return self.obs_buf, self.extras
        result=super().step(action)
        self._step_count+=1
        self._audit()
        return result

    def lock_piece(self,name):return CANONICAL_SPEC.piece(name)

    def _goal_pose(self, name):
        if self.case_spec is not None:
            return self.case_spec['goal_state'][name]
        piece = self.lock_piece(name)
        return ((piece.assembly_position, piece.assembly_quat_wxyz)
                if self.task_mode is TaskMode.ASSEMBLE else (piece.target_position, piece.target_quat_wxyz))

    def lock_target_tensor(self,name):
        position, _ = self._goal_pose(name)
        return torch.tensor(position,device=self.device).view(1,3)+self.scene.env_origins

    def record_privileged_event(self,kind,payload=None):
        self._privileged_events.append(dict(kind=kind,time_s=self._step_count*self.step_dt,
            source='native_state_and_frozen_spec',payload=payload or {}))

    def set_phase(self,phase,*,piece=None):
        self._set_phase(phase);self.puzzle_state.active_piece=piece
        self.record_privileged_event('phase',dict(phase=phase.value,piece=piece))

    def mark_failed(self,reason):
        self.puzzle_state.failure_reason=str(reason)
        self._set_phase(LockPhase.FAILED)
        self.record_privileged_event('failure',dict(reason=str(reason)))

    def _snapshot(self):
        pieces={};robots={}
        for p in CANONICAL_SPEC.pieces:
            d=self.scene['piece_'+p.name].data
            target_position, target_quaternion = self._goal_pose(p.name)
            if self.task_mode is TaskMode.DISASSEMBLE and self.case_spec is None:
                target_position = self.lock_target_tensor(p.name)[0].cpu().numpy()
            pieces[p.name]=dict(position=d.root_pos_w[0].cpu().numpy().copy(),quaternion=d.root_quat_w[0].cpu().numpy().copy(),
                linear_velocity=d.root_lin_vel_w[0].cpu().numpy().copy(),angular_velocity=d.root_ang_vel_w[0].cpu().numpy().copy(),
                target=np.asarray(target_position, dtype=np.float64), target_quaternion=target_quaternion)
        for side in ('left','right'):
            r=self.scene[side+'_robot'];d=r.data;i=r.find_bodies('panda_hand')[0][0]
            hand=d.body_pos_w[0,i].cpu().numpy();q=d.body_quat_w[0,i].cpu().numpy()
            fingers=r.find_joints('panda_finger_joint.*')[0]
            robots[side]=dict(joints=d.joint_pos[0].cpu().numpy().copy(),joint_velocities=d.joint_vel[0].cpu().numpy().copy(),
                tcp=hand+quaternion_matrix(q)@np.array([0,0,.1034]),hand=hand,quaternion=q,fingers=d.joint_pos[0,fingers].cpu().numpy())
            if self.task_mode is TaskMode.ASSEMBLE:
                robots[side]['link_com_positions'] = {
                    name: d.body_com_pos_w[0, r.find_bodies(name)[0][0]].cpu().numpy().tolist()
                    for name in ('panda_link3', 'panda_link5', 'panda_link6')}
        return pieces,robots

    def _audit(self,*,contacts_fresh=True):
        pieces,robots=self._snapshot();depth=0.;pairs={};clearances={}
        if self.task_mode is TaskMode.ASSEMBLE:
            for piece in CANONICAL_SPEC.pieces:
                pieces[piece.name]['target'] = np.asarray(self._goal_pose(piece.name)[0], dtype=np.float64)
                pieces[piece.name]['target_quaternion'] = self._goal_pose(piece.name)[1]
        cubes={n:(p['position']+self._local_cells[n]@quaternion_matrix(p['quaternion']).T,
                  quaternion_matrix(p['quaternion'])) for n,p in pieces.items()}
        boxes={n:(p['position']+self._collision_boxes[n][0]@quaternion_matrix(p['quaternion']).T,
                  quaternion_matrix(p['quaternion']),self._collision_boxes[n][1]) for n,p in pieces.items()}
        for a,b in combinations(pieces,2):
            ca,ra,ha=boxes[a];cb,rb,hb=boxes[b]
            gap=box_pair_clearance(ca,ra,ha,cb,rb,hb);clearances[a+'/'+b]=gap
            d=max(0.,-gap);pairs[a+'/'+b]=d;depth=max(depth,d)
        for n,(centers,rotation,half) in boxes.items():
            d=max(0.,TABLE_TOP_Z-float(np.min(centers[:,2]-half@np.abs(rotation[2]))))
            pairs[n+'/table']=d;depth=max(depth,d)
        self._max_penetration_m=max(depth,self._max_penetration_m)
        self.lock_max_penetration_m[:]=self._max_penetration_m
        predicates=goal_predicates(pieces,robots,self._max_penetration_m)
        if self.task_mode is TaskMode.ASSEMBLE:
            # Assembly uses a tighter final pose gate than the common
            # disassembly parking predicate.  Keep the same measured fields
            # and only replace the position/orientation zone used for the
            # stable-window counter.
            for name, row in predicates['pieces'].items():
                row['in_zone'] = (row['position_error_m'] <= .0075
                                  and row['angle_error_rad'] <= .08)
            predicates['all_in_zones'] = all(row['in_zone'] for row in predicates['pieces'].values())
            # Every pair in this six-piece variant has nominal mating faces
            # 2 mm apart. Bound actual pair gaps as well as individual poses.
            predicates['mating_clearance_ok'] = all(gap <= .0075 for gap in clearances.values())
            if self.case_subtask == 'complete':
                predicates['all_outside_parking'] = all(
                    np.linalg.norm(pieces[p.name]['position'] - np.asarray(
                        self.case_spec['pieces'][p.name]['parking_position'] if self.case_spec else p.target_position)) > .025
                    for p in CANONICAL_SPEC.pieces)
            else:
                predicates['all_outside_parking'] = True
            predicates['instantaneous_goal'] = bool(
                predicates['all_in_zones'] and predicates['all_stable']
                and predicates['grippers_open'] and predicates['arms_clear']
                and predicates['penetration_ok'] and predicates['mating_clearance_ok']
                and predicates['all_outside_parking'])
        arm_forces={}
        for side in ('left','right'):
            sensor=self.scene[side+'_arm_contacts']
            arm_forces[side]=dict(zip(sensor.body_names,
                torch.linalg.vector_norm(sensor.data.net_forces_w[0],dim=-1).cpu().numpy().tolist()))
        arm_force=max(force for arm in arm_forces.values() for force in arm.values())
        if contacts_fresh:self._max_arm_contact_n=max(self._max_arm_contact_n,arm_force)
        # Filtered matrices account for permitted finger/wood contacts. The
        # residual of the total force exposes table, other-finger and robot
        # contacts, which are absent from the six-piece filter matrix.
        finger_unfiltered={};finger_vectors={}
        for side in ('left','right'):
            finger_unfiltered[side]={};finger_vectors[side]={}
            for finger,suffix in (('left','finger_piece_contact'),('right','other_finger_piece_contact')):
                data=self.scene[side+'_'+suffix].data
                net=data.net_forces_w[0].sum(0)
                filtered=data.force_matrix_w[0].sum(0)
                if filtered.shape != (6+len(FORBIDDEN_CONTACT_LABELS),3):
                    raise RuntimeError('incomplete finger contact filter coverage')
                allowed=filtered[:6].sum(0)
                residual=net-allowed
                pair_vectors=dict(zip(FORBIDDEN_CONTACT_LABELS,filtered[6:].cpu().numpy().tolist()))
                pair_force=float(torch.linalg.vector_norm(filtered[6:],dim=-1).max())
                finger_unfiltered[side][finger]=max(float(torch.linalg.vector_norm(residual)),pair_force)
                finger_vectors[side][finger]=dict(net_w=net.cpu().numpy().tolist(),
                    allowed_piece_sum_w=allowed.cpu().numpy().tolist(),residual_w=residual.cpu().numpy().tolist(),
                    forbidden_pairs_w=pair_vectors)
        residual_force=max(v for fingers in finger_unfiltered.values() for v in fingers.values())
        if contacts_fresh:self._max_finger_unfiltered_n=max(self._max_finger_unfiltered_n,residual_force)
        predicates['arm_collision_free']=max(self._max_arm_contact_n,self._max_finger_unfiltered_n) < .5
        predicates['max_nonfinger_contact_n']=self._max_arm_contact_n
        predicates['max_finger_unfiltered_contact_n']=self._max_finger_unfiltered_n
        predicates['instantaneous_goal']=predicates['instantaneous_goal'] and predicates['arm_collision_free'] and contacts_fresh
        self._stable_steps=self._stable_steps+1 if predicates['instantaneous_goal'] else 0
        self._last_audit=dict(**predicates,pair_penetration_m=pairs,pair_signed_sat_clearance_m=clearances,stable_steps=self._stable_steps,
            nonfinger_contact_n=arm_forces,contacts_fresh=contacts_fresh,
            required_stable_steps=(60 if self.task_mode is TaskMode.ASSEMBLE else 30),
            finger_unfiltered_contact_n=finger_unfiltered,finger_contact_vectors=finger_vectors,
            penetration_scope='oriented maximal-cuboid compounds vs pieces and tabletop')
        self._motion_diagnostics=lattice_motion_diagnostics(cubes,GRID_CELL_M,
            np.array([*LOCK_CENTER_XY,TABLE_TOP_Z])+GRID_CELL_M*np.array([.5,.5,4.5]))

    def contact_forces(self):
        result={}
        for side in ('left','right'):
            result[side]={}
            for finger,suffix in (('left','finger_piece_contact'),('right','other_finger_piece_contact')):
                data=self.scene[side+'_'+suffix].data
                matrix=data.force_matrix_w
                result[side][finger]=matrix[0].sum(0)[:6].cpu().numpy().tolist()
        return result

    def has_bilateral_contact(self,side,piece):
        i=self.lock_piece_names.index(piece);forces=self.contact_forces()[side]
        return all(np.linalg.norm(f[i])>.1 for f in forces.values())


    def get_privileged_state(self):
        """Legacy physical snapshot only. New protocol uses its own explicit schema."""
        pieces, robots = self._snapshot()
        def plain(rows):
            return {n: {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in p.items()} for n, p in rows.items()}
        return dict(pieces=plain(pieces), robots=plain(robots), contacts=self.contact_forces(),
                    max_penetration_m=self._max_penetration_m, audit=self._last_audit)

    def assembly_success(self):
        return self.task_mode is TaskMode.ASSEMBLE and self._stable_steps >= 60

    def success_summary(self):
        return dict(success=self.assembly_success() if self.task_mode is TaskMode.ASSEMBLE else self.disassembly_success(),
                    task_mode=self.task_mode.value, max_penetration_m=self._max_penetration_m, audit=self._last_audit)

    def disassembly_success(self):return self.task_mode is TaskMode.DISASSEMBLE and self._stable_steps>=30


class KongmingDualSharpaLockEnv(KongmingLockEnv):
    """Kongming state machine with native dual-Sharpa reset semantics.

    The native bridge owns measured physical auditing.  This subclass keeps
    the puzzle state reset bookkeeping but avoids the Panda-specific legacy
    contact audit in ``KongmingLockEnv.reset``.
    """

    def step(self, action):
        # Direct gym callers still use the standard native action loop. The
        # platform bridge supplies its own fresh 120 Hz scorer audit hook.
        if getattr(self, 'benchmark_substep_hook', None) is not None:
            return super().step(action)
        return ManagerBasedEnv.step(self, action)

    def reset(self, *args, **kwargs):
        self.puzzle_state = PuzzleState(mode=self.task_mode)
        self._privileged_events = []
        self._max_penetration_m = 0.0
        self._stable_steps = 0
        self._step_count = 0
        self._max_arm_contact_n = 0.0
        self._max_finger_unfiltered_n = 0.0
        self.lock_removed_mask.zero_()
        self.lock_placed_mask.zero_()
        self.lock_assembled_mask.zero_()
        self.lock_max_penetration_m.zero_()
        self._set_phase(LockPhase.DISASSEMBLED if self.task_mode is TaskMode.ASSEMBLE else LockPhase.ASSEMBLED)
        return ManagerBasedEnv.reset(self, *args, **kwargs)


def make_kongming_lock_env(*,cfg=None,env_cfg_entry_point=None,**kwargs):
    if cfg is None:
        if not env_cfg_entry_point:raise ValueError('missing env cfg')
        module_name,attr=env_cfg_entry_point.split(':');cfg=getattr(__import__(module_name,fromlist=[attr]),attr)()
    env_cls = KongmingDualSharpaLockEnv if getattr(cfg, 'embodiment', None) == 'dual-floating-sharpa' else KongmingLockEnv
    return env_cls(cfg,**kwargs)
