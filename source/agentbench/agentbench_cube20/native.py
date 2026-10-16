"""Native Isaac adapter. All task variations are authored before physics starts."""
import copy
import math
import tempfile
import numpy as np
import torch
from pxr import Gf, UsdPhysics
import isaaclab.sim as sim_utils
from .catalog import BY_ID, moves, sample
from .geometry import configuration, quaternion
from agentbench.tasks.manager_based.table_top_manipulation.config.pocket_cube.dual_aloha_cfg import DualAlohaPocketCubeEnvCfg
from agentbench.tasks.manager_based.table_top_manipulation.config.pocket_cube.pocket_cube_env import InterlockedPocketCubeEnv
from agentbench.tasks.manager_based.table_top_manipulation.config.pocket_cube.pocket_cube_cfg import CUBIE_CENTER_OFFSET, CUBE_CENTER, _spawn_scanned_cubie, SCANNED_CUBIE_DIAGONAL_INERTIA
from agentbench.tasks.manager_based.table_top_manipulation.config.pocket_cube.pocket_cube_rules import CORNER_NAMES, FACE_NAMES, FACE_CORNER_POSITIONS
from agentbench.tasks.manager_based.table_top_manipulation.config.pocket_cube.pocket_cube_spawners import spawn_switchable_cube_joints

def spawn_cubie(path, cfg, *args, **kwargs):
    prim = _spawn_scanned_cubie(path,cfg,*args,**kwargs)
    mass=UsdPhysics.MassAPI(prim)
    mass.GetDiagonalInertiaAttr().Set(Gf.Vec3f(*([SCANNED_CUBIE_DIAGONAL_INERTIA*cfg.cube20_mass_scale]*3)))
    material=UsdPhysics.MaterialAPI(prim.GetStage().GetPrimAtPath(str(prim.GetPath())+'/PhysicsMaterial'))
    material.GetStaticFrictionAttr().Set(1.4*cfg.cube20_friction_scale)
    material.GetDynamicFrictionAttr().Set(1.1*cfg.cube20_friction_scale)
    return prim

def spawn_joints(path,cfg,*args,**kwargs):
    prim=spawn_switchable_cube_joints(path,cfg,*args,**kwargs)
    stage=prim.GetStage()
    roots=sim_utils.find_matching_prim_paths(path.rsplit('/',1)[0])
    for root in roots:
        for i,name in enumerate(CORNER_NAMES):
            for group in ('CoreLocks','CarrierLocks'):
                joint=UsdPhysics.FixedJoint.Get(stage,f'{root}/Joints/{group}/{name.lower()}')
                joint.GetLocalPos0Attr().Set(Gf.Vec3f(*cfg.cube20_positions[i]))
                q=cfg.cube20_quaternions[i]
                joint.GetLocalRot0Attr().Set(Gf.Quatf(q[0],Gf.Vec3f(*q[1:])))
    return prim

def build_cfg(task_id, seed=0, split='nominal', device='cuda:0', robot='aloha'):
    t=BY_ID[task_id]; params=sample(task_id,seed,split)
    if robot == 'aloha':
        cfg=DualAlohaPocketCubeEnvCfg()
    elif robot == 'sharpa':
        from agentbench.tasks.manager_based.table_top_manipulation.config.pocket_cube.dual_sharpa_cfg import DualSharpaPocketCubeEnvCfg
        cfg=DualSharpaPocketCubeEnvCfg()
    else:
        raise ValueError(f'Unknown embodiment: {robot}')
    cfg.cube20_robot=robot
    cfg.scene.num_envs=1; cfg.sim.device=device; cfg.sim.use_fabric=False; cfg.seed=seed
    # Isaac's default converter directory includes a seeded random suffix.
    # Two processes with the same seed and second can otherwise share a USD.
    if robot == 'aloha':
        for side in ('left','right'):
            getattr(cfg.scene,side+'_robot').spawn.usd_dir=tempfile.mkdtemp(prefix=f'cube20_{side}_')
    cfg.cube20_task_id=task_id; cfg.cube20_parameters=params
    cfg.target_moves=moves(t.transition)
    cfg.preconfigure_single_target_face=len(cfg.target_moves)==1
    cfg.enforce_target_face_order=True
    # Static screenshots render explicitly; no RTX cost on every physics substep.
    cfg.sim.render_interval=1000000
    positions,rotations=configuration(moves(t.start_moves))
    positions=positions*CUBIE_CENTER_OFFSET
    cfg.cube20_local_positions=positions.tolist()
    cfg.cube20_local_quaternions=[quaternion(r) for r in rotations]
    angle=math.radians(params['yaw_deg']); c=math.cos(angle); s=math.sin(angle)
    yaw=np.array([[c,-s,0],[s,c,0],[0,0,1.]])
    root=np.array([params['x'],params['y'],CUBE_CENTER[2]])
    root_q=quaternion(yaw)
    for name in ('pocket_cube','pocket_cube_carrier'):
        asset=getattr(cfg.scene,name)
        asset.init_state.pos=tuple(root); asset.init_state.rot=root_q
        asset.spawn.mass_props.mass*=params['mass_scale']
    for i,asset in enumerate(cfg.scene.pocket_cubies.rigid_objects.values()):
        asset.init_state.pos=tuple(root+yaw@positions[i]); asset.init_state.rot=quaternion(yaw@rotations[i])
        asset.spawn.func=spawn_cubie
        asset.spawn.mass_props.mass*=params['mass_scale']
        asset.spawn.cube20_mass_scale=params['mass_scale']
        asset.spawn.cube20_friction_scale=params['friction_scale']
    joint_cfg=cfg.scene.pocket_cube_joints.spawn
    joint_cfg.func=spawn_joints
    joint_cfg.cube20_positions=cfg.cube20_local_positions
    joint_cfg.cube20_quaternions=cfg.cube20_local_quaternions
    rest=cfg.scene.cube_rest
    rest.init_state.pos=(params['x'],params['y'],rest.init_state.pos[2])
    rest.init_state.rot=root_q
    cfg.scene.sky_light.spawn.intensity=params['light']
    cfg.validate()
    return cfg

class Cube20Env(InterlockedPocketCubeEnv):
    def _physics_fingerprint(self):
        from .fingerprint import FixedPhysicsFingerprintCache
        if not hasattr(self,'_fixed_physics_cache'):
            self._fixed_physics_cache=FixedPhysicsFingerprintCache(sim_utils.get_current_stage())
        return self._fixed_physics_cache.fingerprint(physics_dt=self.physics_dt,
            decimation=self.cfg.decimation, gravity=self.cfg.sim.gravity)

    def close(self):
        try:
            if hasattr(self,'_fixed_physics_cache'):self._fixed_physics_cache.close()
        finally:super().close()

    def _reset_terminal_guard(self):
        from .evaluation import TerminalGuard
        self.terminal_guard = TerminalGuard(self.cfg.cube20_task_id, self._physics_fingerprint())
        self.pocket_cube_success[:] = False

    def _physical_goal_matches(self):
        from isaaclab.utils.math import quat_apply, quat_inv, quat_mul
        task=BY_ID[self.cfg.cube20_task_id]
        pos, rot = configuration(moves(task.start_moves)+moves(task.transition))
        core=self.scene['pocket_cube'].data
        cubies=self.scene['pocket_cubies'].data
        inv=quat_inv(core.root_quat_w)[:,None].expand(-1,8,-1).reshape(-1,4)
        local=quat_apply(inv,(cubies.object_link_pos_w[:,self._cube_cubie_ids]-core.root_pos_w[:,None]).reshape(-1,3))
        actual=quat_mul(inv,cubies.object_link_quat_w[:,self._cube_cubie_ids].reshape(-1,4))
        target=torch.tensor([quaternion(r) for r in rot],device=self.device,dtype=actual.dtype)
        distance=torch.linalg.norm(local-torch.tensor(pos*CUBIE_CENTER_OFFSET,device=self.device),dim=-1)
        angle=2*torch.acos((actual*target).sum(-1).abs().clamp(0,1))
        return bool((distance <= CUBIE_CENTER_OFFSET*math.sin(math.radians(1))).all()
                    and (angle <= math.radians(1)).all())

    def _update_pocket_cube_interlock(self):
        super()._update_pocket_cube_interlock()
        angles,speeds=self.get_pocket_cube_face_joint_state()
        success=self.terminal_guard.update(
            state=self.pocket_cube_state_tensor[0].tolist(),angles=angles[0].tolist(),speeds=speeds[0].tolist(),
            active_face=int(self.pocket_cube_active_face[0]),committed_turns=int(self._cube_committed_turns[0]),
            native_failed=bool(self.pocket_cube_rule_failed[0]),
            penetration_m=float(self._cube_max_shell_penetration[0]),
            fingerprint=self._physics_fingerprint(),dt=self.physics_dt,
            physical_goal_matches=self._physical_goal_matches())
        self.pocket_cube_success[0]=success
        if self.terminal_guard.first_failure is not None:
            self.pocket_cube_rule_failed[0]=True
        hook=getattr(self,'benchmark_substep_hook',None)
        if hook is not None: hook()

    def _set_start(self,ids):
        t=BY_ID[self.cfg.cube20_task_id]
        self._cube_permutation[ids]=torch.tensor(t.start.permutation,device=self.device)
        self._cube_orientation[ids]=torch.tensor(t.start.orientation,device=self.device)
        self._cube_cubie_quat[ids]=torch.tensor(self.cfg.cube20_local_quaternions,device=self.device)
        self.pocket_cube_target_tensor[:]=torch.tensor(t.goal.as_vector(),device=self.device)
        self._refresh_state_observation()

    def _initialize_pocket_cube(self):
        super()._initialize_pocket_cube()
        self._set_start(slice(None))
        self._reset_terminal_guard()

    def _reset_joint_switches(self,env_id):
        # Author the correct permutation's locks directly, never a transient
        # solved lock graph for scrambled physical bodies.
        handles=self._cube_joint_handles[env_id]
        t=BY_ID[self.cfg.cube20_task_id]
        face=FACE_NAMES.index(self.cfg.target_moves[0][0])
        selected={t.start.permutation[p] for p in FACE_CORNER_POSITIONS[face]}
        for joint in self._cube_suction_joints[env_id].values(): self._enable(joint,False)
        for hinge in handles['hinges'].values():
            self._enable(hinge,False); self._set_hinge_limits(hinge,0.,95.)
        for i,name in enumerate(CORNER_NAMES):
            for group in ('core','carrier'):
                self._set_fixed_frame(handles[group][name.lower()],self.cfg.cube20_local_positions[i],self.cfg.cube20_local_quaternions[i])
                self._enable(handles[group][name.lower()],(i in selected)==(group=='carrier'))
        self._enable(handles['core_carrier'],False)
        hinge=handles['hinges'][self.FACE_HINGE_AXIS[face]]
        self._enable(hinge,True); self._set_hinge_limits(hinge,0.,.05)

    def _reset_idx(self,env_ids):
        super()._reset_idx(env_ids)
        if hasattr(self,'_cube_joint_handles'): self._set_start(env_ids)
        if hasattr(self,'terminal_guard'): self._reset_terminal_guard()

def hold_action(env):
    action=torch.zeros((env.num_envs,env.action_manager.total_action_dim),device=env.device)
    if env.cfg.cube20_robot == 'aloha':
        assert action.shape[1] == 16
        for side,offset in (('left',6),('right',14)):
            term=env.action_manager.get_term(side+'_gripper')
            action[:,offset:offset+2]=env.scene[side+'_robot'].data.joint_pos[:,term._joint_ids]
    else:
        assert env.cfg.cube20_robot == 'sharpa' and action.shape[1] == 56
    return action

def make(task_id,seed=0,split='nominal',device='cuda:0',robot='aloha',**kwargs):
    return Cube20Env(build_cfg(task_id,seed,split,device,robot))
