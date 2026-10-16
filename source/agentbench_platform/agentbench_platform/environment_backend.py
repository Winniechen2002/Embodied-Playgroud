"""Trusted environment adapters. No model clients, controller or public reset."""
import io
import math
import numpy as np
from .resources import ResourceStore


class MarbleBackend:
    def __init__(self, task, *, seed=0, initial_mode='loaded', spring_stiffness=22., resources=None,max_steps=None,environment_parameters=None):
        from agentbench_mujoco.campaign_env import FrankaCampaignEnv
        self.task=task
        self.resources=resources if resources is not None else ResourceStore()
        parameters=dict(environment_parameters or {})
        allowed={'spring_stiffness','launcher_offset_m','ammunition_offset_m','background','background_motion'}
        if set(parameters)-allowed:raise ValueError('Unknown environment trial parameters')
        parameters.setdefault('spring_stiffness',spring_stiffness)
        self.env=FrankaCampaignEnv(scenario=task['scenario'],initial_mode=initial_mode,
            observation_mode='state',**parameters)
        if max_steps is not None:
            self.env.max_seconds=min(self.env.max_seconds,max_steps*self.env.physics_dt*self.env.decimation)
        try: self.env.reset(seed=seed)
        except BaseException:
            self.env.close(); raise
        self.finished=False; self.terminated=False; self.truncated=False; self._result=None
        self._capture=None
        self.physics_steps=0
        original=self.env._after_physics
        def after_physics():
            self.physics_steps+=1
            original()
        self.env._after_physics=after_physics

    def describe(self):
        e=self.env
        # Calibrated render is read-only and cached at this physical step.
        camera=self.snapshot(('front_left',))['cameras']['front_left']
        return dict(task=dict(id=self.task['id'],family='marble',name='Marble manipulation',
            description=self.task['goal'], max_steps=math.ceil(e.max_seconds/(e.physics_dt*e.decimation)),
            task_metadata_version='public-spring-v1',variation_request=dict(
                spring_stiffness=e.spring_stiffness,spring_stiffness_unit='N/m')),
            action_spec=dict(size=16,low=e.action_space.low.tolist(),high=e.action_space.high.tolist(),neutral_action=e.last_action.tolist(),
                control_period_s=e.physics_dt*e.decimation,physics_period_s=e.physics_dt,
                names=[f'{side}_{j}' for side in ('left','right') for j in (*range(7),'gripper')],
                semantics=['Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm.']),
            cameras={'front_left':dict(width=e.width,height=e.height,model='mujoco',calibration=camera['calibration'])},
            robots={prefix or 'left':dict(model='Franka Panda',joint_names=[f'{prefix}joint{i}' for i in range(1,8)],
                joint_limits=e.model.jnt_range[[e.model.joint(f'{prefix}joint{i}').id for i in range(1,8)]].tolist(),
                default_joint_positions=e.last_action[8*arm:8*arm+7].tolist()) for arm,prefix in enumerate(e.prefixes)},
            goal=dict(description=self.task['goal']))

    def snapshot(self,camera_ids=()):
        e=self.env; d=e.data
        cameras={}
        if camera_ids:
            if tuple(camera_ids)!=('front_left',): raise ValueError('Unknown cameras')
            if self._capture is None or self._capture[0]!=e.control_steps:
                from PIL import Image
                before=(d.time,d.qpos.copy(),d.qvel.copy())
                pixels=e.render(); out=io.BytesIO(); Image.fromarray(pixels).save(out,format='PNG')
                import mujoco
                camera=mujoco.mjv_averageCamera(e.renderer.scene.camera[0],e.renderer.scene.camera[1])
                forward=np.asarray(camera.forward);up=np.asarray(camera.up)
                right=np.cross(forward,up)
                transform=np.eye(4);transform[:3,:3]=np.column_stack((right,-up,forward));transform[:3,3]=camera.pos
                fy=e.height*camera.frustum_near/(camera.frustum_top-camera.frustum_bottom)
                calibration=dict(intrinsics=[[float(fy),0,e.width/2],[0,float(fy),e.height/2],[0,0,1]],
                    world_from_camera=transform.tolist(),convention='opencv_x_right_y_down_z_forward',
                    near_m=float(camera.frustum_near),far_m=float(camera.frustum_far),pixel_center_offset=[.5,.5])
                if d.time!=before[0] or not np.array_equal(d.qpos,before[1]) or not np.array_equal(d.qvel,before[2]):
                    raise RuntimeError('Camera changed simulation')
                # A store is per episode. Do not let expired camera frames fill it.
                previous=getattr(self,'_capture_id',None)
                if previous is not None: self.resources.discard(previous)
                ident=self.resources.register(out.getvalue(),modality='rgb',profiles=('rgb','rgbd','privileged'),
                    capture_step=e.control_steps,metadata=dict(width=e.width,height=e.height,encoding='png',content_type='image/png'))
                self._capture_id=ident
                self._capture=(e.control_steps,dict(rgb_resource_id=ident,width=e.width,height=e.height,
                    capture_step=e.control_steps,calibration=calibration))
            cameras['front_left']=self._capture[1]
        ids=np.r_[e.robot_q,e.finger_q]; velocities=np.r_[e.robot_v,e.finger_v]
        pieces={e.model.body(i).name:dict(position=d.xpos[i].tolist(),quaternion=d.xquat[i].tolist())
                for i in range(1,e.model.nbody) if i not in e.robot_bodies}
        return dict(step_index=e.control_steps,physics_step_count=self.physics_steps,simulation_time_s=float(d.time),
            terminated=self.terminated,truncated=self.truncated,cameras=cameras,
            robots={'dual_panda':dict(joint_positions=d.qpos[ids].tolist(),joint_velocities=d.qvel[velocities].tolist(),
                previous_action=e.last_action.tolist())},privileged=dict(pieces=pieces))

    def step(self,action):
        if self.finished or self.terminated or self.truncated:raise RuntimeError('Episode closed')
        _,_,self.terminated,self.truncated,_=self.env.step(np.asarray(action,dtype=np.float64))
        return self.snapshot()

    def finish(self):
        if self._result is None:
            self.finished=True
            self._result=dict(success=bool(self.env.success),score=float(bool(self.env.success)),
                step_count=self.env.control_steps,terminated=self.terminated,truncated=self.truncated)
        return dict(self._result)

    abort=finish
    def close(self): self.env.close()


class IsaacEnvironmentBackend:
    """Adapter for a single, maintainer-created Hanoi, pocket cube or bookshelf instance."""
    def __init__(self,task,env,*,resources,max_steps=18000):
        self.task,self.env,self.resources=task,env,resources
        self.steps=0;self.finished=False;self.terminated=False;self.truncated=False;self._result=None
        self.max_steps=max_steps;self.success=False;self.failure=None
        env.benchmark_disable_auto_reset=True
        from .native_cameras import NativeCameras
        self.robot_keys=list(env.scene.articulations)
        self.cameras=NativeCameras(env,resources,physical_arrays=self._physical_arrays)
        self.low,self.high,self.names,self.semantics=self._action_spec()
        self.previous_action=[0.]*len(self.low)
        self.monitor=None;self.audit=None
        if task['family'].startswith('hanoi_'):
            from agentbench_hanoi40.catalog import BY_ID
            from agentbench_hanoi40.rules import ObservedMonitor
            from agentbench_hanoi40.audit import Audit
            self.monitor=ObservedMonitor(BY_ID[task['case_id']],env.cfg.hanoi40_parameters)
            self.audit=Audit(env)
        env.benchmark_substep_hook=self._audit
        self.start_time=float(env.sim.current_time)
        self.start_physics=int(env._sim_step_counter)

    def _physical_arrays(self):
        arrays=[]
        for item in self.env.scene.articulations.values():
            arrays.extend([item.data.joint_pos.detach().cpu().numpy(),item.data.joint_vel.detach().cpu().numpy()])
        for item in self.env.scene.rigid_objects.values():arrays.append(item.data.root_state_w.detach().cpu().numpy())
        for item in self.env.scene.rigid_object_collections.values():arrays.append(item.data.object_link_state_w.detach().cpu().numpy())
        return arrays

    def _action_spec(self):
        low=[];high=[];names=[];semantics=[]
        for name in self.env.action_manager.active_terms:
            term=self.env.action_manager.get_term(name)
            if term.action_dim==1 and 'gripper' in name:
                low.append(-1.);high.append(1.);names.append(name)
                semantics.append(name+': negative closes, nonnegative opens')
                continue
            asset=term._asset; ids=term._joint_ids
            bounds=asset.data.joint_pos_limits[0,ids].detach().cpu().numpy()
            scale=np.broadcast_to(np.asarray(term._scale.detach().cpu() if hasattr(term._scale,'detach') else term._scale), (1,term.action_dim))[0]
            offset=np.broadcast_to(np.asarray(term._offset.detach().cpu() if hasattr(term._offset,'detach') else term._offset), (1,term.action_dim))[0]
            relative='Relative' in type(term).__name__
            if relative:
                lo=np.full(term.action_dim,-1.);hi=np.full(term.action_dim,1.)
                semantics.append(name+': current joint position + scale * action; scale='+str(scale.tolist()))
            else:
                if np.any(scale==0):raise ValueError('Zero action scale')
                pair=(bounds-offset[:,None])/scale[:,None]
                lo=pair.min(1);hi=pair.max(1)
                semantics.append(name+': joint target = offset + scale * action; offset='+str(offset.tolist())+'; scale='+str(scale.tolist()))
            low.extend(lo.tolist());high.extend(hi.tolist())
            indices=list(range(len(asset.joint_names)))[ids] if isinstance(ids,slice) else ids
            names.extend(name+'.'+asset.joint_names[i] for i in indices)
        return low,high,names,semantics

    def _neutral_action(self):
        values=[]
        for name in self.env.action_manager.active_terms:
            term=self.env.action_manager.get_term(name)
            if term.action_dim==1 and 'gripper' in name:
                values.append(1.)
            elif 'Relative' in type(term).__name__:
                values.extend([0.]*term.action_dim)
            else:
                value=(term._asset.data.joint_pos[:,term._joint_ids]-term._offset)/term._scale
                values.extend(value[0].detach().cpu().tolist())
        return values

    def describe(self):
        task=dict(id=self.task['id'],family=self.task['family'],name=self.task['family'],
            description=self.task['goal'] if isinstance(self.task['goal'],str) else 'Reach the declared goal.',max_steps=self.max_steps)
        goal=self.task['goal']
        if isinstance(goal,dict) and 'state' in goal:
            task['description']='Reach pocket-cube corner permutation/orientation '+str(goal['state'])+' and hold for one second.'
        if self.task['family']=='bookshelf':
            # Catalog IDs encode misplaced objects; the client sees only the public instruction.
            task.update(id='bookshelf-v1',description=self.env.cfg.task_instruction)
        if self.monitor is not None:task['description']='Move the rings to peg assignments '+str(list(self.monitor.task.goal))+' using top-only, smaller-on-larger moves.'
        return dict(task=task,goal=dict(description=task['description']),
            action_spec=dict(size=len(self.low),low=self.low,high=self.high,names=self.names,semantics=self.semantics,
                control_period_s=self.env.physics_dt*self.env.cfg.decimation,physics_period_s=self.env.physics_dt,
                neutral_action=self._neutral_action()),
            cameras=self.cameras.description(),robots={key:dict(model=key,joint_names=list(self.env.scene[key].joint_names),
                joint_limits=self.env.scene[key].data.joint_pos_limits[0].tolist(),
                default_joint_positions=self.env.scene[key].data.default_joint_pos[0].tolist()) for key in self.robot_keys})

    def _audit(self):
        if self.monitor is not None:
            from agentbench_hanoi40.rules import RuleFailure
            poses,shell=self.audit.snapshot()
            try:self.monitor.observe(poses,shell['penetration_depth_m'],shell['covered_pairs'],dt=self.env.physics_dt)
            except RuleFailure:self.failure=self.monitor.failure
            self.success=self.monitor.result(poses)['task_success']
        elif self.task['family']=='pocket_cube':
            self.failure=self.env.terminal_guard.first_failure
            self.success=bool(self.env.pocket_cube_success[0])
        else:
            from agentbench.tasks.manager_based.table_top_manipulation.config.organize_bookshelf.mdp import _runtime
            if bool(_runtime(self.env)['violations'].any()):self.failure='physical_violation'
        self.terminated=bool(self.success or self.failure)
        self.env.benchmark_stop_requested=self.terminated

    def snapshot(self,camera_ids=()):
        robots={key:dict(joint_positions=self.env.scene[key].data.joint_pos[0].tolist(),
            joint_velocities=self.env.scene[key].data.joint_vel[0].tolist(),previous_action=self.previous_action)
            for key in self.robot_keys}
        pieces={key:dict(position=item.data.root_pos_w[0].tolist(),quaternion=item.data.root_quat_w[0].tolist())
            for key,item in self.env.scene.rigid_objects.items()}
        return dict(step_index=self.steps,physics_step_count=int(self.env._sim_step_counter)-self.start_physics,
            simulation_time_s=max(0.,float(self.env.sim.current_time)-self.start_time),
            terminated=self.terminated,truncated=self.truncated,robots=robots,
            cameras=self.cameras.capture(camera_ids,self.steps),privileged=dict(pieces=pieces))

    def step(self,action):
        import torch
        if self.finished or self.terminated or self.truncated:raise RuntimeError('Episode closed')
        a=np.asarray(action,dtype=float)
        if a.shape!=(len(self.low),) or not np.isfinite(a).all() or np.any(a<self.low) or np.any(a>self.high):
            raise ValueError('Invalid action')
        tensor=torch.tensor([action],device=self.env.device,dtype=torch.float32)
        # Validate processed relative/absolute targets before advancing physics.
        self.env.action_manager.process_action(tensor)
        for name in self.env.action_manager.active_terms:
            term=self.env.action_manager.get_term(name)
            if term.action_dim==1 and 'gripper' in name:continue
            limits=term._asset.data.joint_pos_limits[:,term._joint_ids]
            target=term.processed_actions
            from isaaclab.envs.mdp.actions.joint_actions import RelativeJointPositionAction
            if isinstance(term,RelativeJointPositionAction):
                target=target+term._asset.data.joint_pos[:,term._joint_ids]
            if ((target<limits[:,:,0])|(target>limits[:,:,1])).any():
                raise ValueError('Action target outside joint limits')
        if self.monitor is not None:
            for _ in range(self.env.cfg.decimation):
                self.env._sim_step_counter+=1;self.env.action_manager.apply_action();self.env.scene.write_data_to_sim()
                self.env.sim.step(render=False);self.env.scene.update(dt=self.env.physics_dt);self._audit()
                if self.terminated:break
        else:
            self.env.step(tensor)
            if self.task['family']=='bookshelf':
                report=self.env.report();self.success=bool(report['success'])
                if report['terminations']['object_lost']:self.failure='object_lost'
                self.terminated=bool(self.success or self.failure)
        self.steps+=1;self.previous_action=list(action)
        self.truncated=not self.terminated and self.steps>=self.max_steps
        return self.snapshot()

    def finish(self):
        if self._result is None:
            self.finished=True
            self._result=dict(success=bool(self.success and not self.failure),score=float(bool(self.success and not self.failure)),
                step_count=self.steps,terminated=self.terminated,truncated=self.truncated)
        return dict(self._result)
    abort=finish
    def close(self):
        try:
            if self.audit is not None:self.audit.cache.close()
        finally:self.env.close()


def create_isaac_backend(task, *, seed=0, split='nominal', device='cuda:0', asset_dir,
                         resources=None, max_steps=None):
    """Maintainer factory; call only after AppLauncher starts the native runtime."""
    from .native_cameras import add_cameras
    resources=resources if resources is not None else ResourceStore()
    env=None
    try:
        if task['family'].startswith('hanoi_'):
            from isaaclab.envs import ManagerBasedEnv
            from agentbench_hanoi40.isaac_cfg import build_cfg
            robot={'hanoi_panda':'franka','hanoi_sharpa':'sharpa','hanoi_floating':'sharpa_no_arm'}[task['family']]
            cfg=build_cfg(task['case_id'],seed,split,asset_dir=asset_dir,robot=robot)
            cfg.sim.device=device;add_cameras(cfg);env=ManagerBasedEnv(cfg)
        elif task['family']=='pocket_cube':
            from agentbench_cube20.native import Cube20Env,build_cfg
            robot='aloha' if task['embodiment']=='aloha' else 'sharpa'
            cfg=build_cfg(task['case_id'],seed,split,device,robot)
            add_cameras(cfg);env=Cube20Env(cfg)
        elif task['family']=='bookshelf':
            import gymnasium as gym
            import isaaclab_tasks
            import agentbench.tasks
            from agentbench.tasks.utils import parse_env_cfg
            cfg=parse_env_cfg(task['gym_id'],device=device,num_envs=1)
            cfg.seed=seed;add_cameras(cfg);env=gym.make(task['gym_id'],cfg=cfg).unwrapped
        else:raise ValueError('Family uses the native journal backend')
        env.reset()
        return IsaacEnvironmentBackend(task,env,resources=resources,
            max_steps=max_steps or getattr(env,'max_episode_length',18000))
    except BaseException:
        if env is not None:env.close()
        raise
