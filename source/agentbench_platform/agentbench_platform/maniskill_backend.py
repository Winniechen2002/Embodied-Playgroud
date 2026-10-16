"""Trusted single-instance SAPIEN adapter. Never hand its environment to a client."""
import io
import math
import numpy as np


def plain(value):
    if hasattr(value,'detach'):value=value.detach().cpu().numpy()
    return np.asarray(value).tolist()


class ManiSkillBackend:
    def __init__(self,task,*,resources,seed=0,parameters=None,max_steps=None,render=True):
        import agentbench_maniskill as bench
        self.task,self.resources=task,resources
        parameters=dict(parameters or {'authored_light_scale':1.,'physics_variant':0})
        if set(parameters)!={'authored_light_scale','physics_variant'}:raise ValueError('Unknown initialization parameters')
        self.parameters=parameters;self.seed=seed
        self.env=bench.make(task['case_id'],physics_variant=parameters['physics_variant'],
            light_scale=parameters['authored_light_scale'],obs_mode='rgbd' if render else 'none',
            render_backend='gpu' if render else 'none',reward_mode='sparse',control_mode='pd_joint_pos')
        try:self.env.reset(seed=seed)
        except BaseException:self.env.close();raise
        self.e=self.env.unwrapped
        self.steps=0;self.finished=False;self.terminated=False;self.truncated=False;self._result=None
        self.max_steps=max_steps or (6000 if task['family']=='maniskill_long_horizon' else 2400)
        self.render_enabled=render;self._capture=None;self._resource_ids=[]
        self.previous_action=np.asarray(plain(self.e.hold_action()),dtype=float).reshape(-1).tolist()
        self.action_spec=self._action_spec()

    def _action_spec(self):
        space=self.env.unwrapped.single_action_space
        low=np.asarray(space.low,dtype=float).reshape(-1);high=np.asarray(space.high,dtype=float).reshape(-1)
        names=[];semantics=[]
        for name,c in self.e.agent.controller.controllers.items():
            count=int(np.prod(c.action_space.shape));cfg=c.config
            joints=list(getattr(cfg,'joint_names',()))
            normalized=bool(getattr(cfg,'normalize_action',False))
            relative=bool(getattr(cfg,'use_delta',False))
            original=getattr(c,'_original_single_action_space',c.single_action_space)
            mapping=(f'{name}: {type(c).__name__}; joint order={joints}; normalize_action={normalized}; use_delta={relative}; '
                f'native_low={np.asarray(original.low).tolist()}; native_high={np.asarray(original.high).tolist()}; '
                'rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.')
            names.extend([f'{name}.{joints[i]}' if len(joints)==count else f'{name}[{i}]' for i in range(count)])
            semantics.extend([mapping]*count)
        if len(names)!=len(low) or np.isnan([low,high]).any() or np.isposinf(low).any() or np.isneginf(high).any():raise ValueError('Unbounded or unmapped native action contract')
        return dict(size=len(low),low=[float(v) if np.isfinite(v) else None for v in low],high=[float(v) if np.isfinite(v) else None for v in high],names=names,semantics=semantics,
            neutral_action=self.previous_action,control_period_s=1/self.e.control_freq,physics_period_s=1/self.e.sim_freq)

    def describe(self):
        robot=self.e.agent.robot
        return dict(task=dict(id=self.task['id'],family=self.task['family'],case_id=self.task['case_id'],
            embodiment=self.task['embodiment'],name=self.e.task['title'],description=self.e.task.get('instruction',self.e.task['title']),max_steps=self.max_steps),
            action_spec=self.action_spec,robots={self.task['embodiment']:dict(model=self.task['embodiment'],
                joint_names=[j.name for j in robot.get_active_joints()],joint_limits=[
                    [float(v) if math.isfinite(v) else None for v in pair] for pair in plain(robot.get_qlimits())[0]],
                default_joint_positions=plain(self.e.initial_qpos))},
            cameras={'scene':dict(width=640,height=480)} if self.render_enabled else {},
            goal=dict(description=str(self.task['goal']),stable_seconds=1.))

    def initialization_readback(self):
        import sapien
        lighting=None
        if self.render_enabled:
            scene=self.e.scene.sub_scenes[0]
            lights=[component for entity in scene.entities for component in entity.components
                if isinstance(component,sapien.render.RenderDirectionalLightComponent)]
            lighting=dict(ambient=plain(scene.render_system.ambient_light),directional=[plain(light.color) for light in lights])
        return dict(seed=int(np.asarray(self.e._episode_seed).reshape(-1)[0]),
            physics_variant=self.e.task.get('physics_variant',0),light_scale=self.e.light_scale,
            lighting=lighting,physics_hz=self.e.sim_freq,control_hz=self.e.control_freq)

    def _physical_arrays(self):
        s=self.e.snapshot()
        return [np.asarray([*o['p'],*o['q'],*o['v'],*o['w']]) for o in s['objects'].values()]+[
            np.asarray(plain(self.e.agent.robot.get_qpos())),np.asarray(plain(self.e.agent.robot.get_qvel()))]

    def _camera(self):
        if self._capture is not None and self._capture[0]==self.steps:return self._capture[1]
        from PIL import Image
        before=self.e.physics_steps
        obs=self.e.get_obs()
        data=obs['sensor_data']['scene'];params=obs['sensor_param']['scene']
        rgb=data['rgb'].detach().cpu().numpy()[0].astype(np.uint8)
        source_height,source_width=rgb.shape[:2]
        rgb=np.asarray(Image.fromarray(rgb).resize((640,480),Image.Resampling.BILINEAR),dtype=np.uint8)
        intrinsic=np.asarray(plain(params['intrinsic_cv']),dtype=float)[0]
        intrinsic[0]*=640/source_width;intrinsic[1]*=480/source_height
        extrinsic=np.asarray(plain(params['extrinsic_cv']),dtype=float)[0]
        if extrinsic.shape==(3,4):extrinsic=np.vstack([extrinsic,[0.,0.,0.,1.]])
        if extrinsic.shape!=(4,4):raise ValueError('Invalid native camera extrinsics')
        world_from_camera=np.linalg.inv(extrinsic)
        calibration=dict(intrinsics=intrinsic.tolist(),world_from_camera=world_from_camera.tolist(),
            convention='opencv_x_right_y_down_z_forward',near_m=.01,far_m=30.,pixel_center_offset=[.5,.5])
        depth=data['depth'].detach().cpu().numpy()[0].astype(np.float32).squeeze()/1000.
        depth=np.asarray(Image.fromarray(depth).resize((640,480),Image.Resampling.NEAREST),dtype='<f4')
        validity=(np.isfinite(depth)&(depth>0)&(depth<=30)).astype(np.uint8)
        depth=np.where(validity,depth,0).astype('<f4')
        camera=self.resources.register_capture(camera_id='scene',capture_step=self.steps,rgb=rgb.tobytes(),
            depth=depth.tobytes(),validity=validity.tobytes(),calibration=calibration)
        if self.e.physics_steps!=before:raise RuntimeError('Observation advanced physics')
        self._capture=(self.steps,camera);return camera

    def snapshot(self,camera_ids=()):
        if any(x!='scene' for x in camera_ids) or camera_ids and not self.render_enabled:raise ValueError('Unknown camera')
        state=self.e.snapshot();robot=self.e.agent.robot
        return dict(step_index=self.steps,physics_step_count=self.e.physics_steps,simulation_time_s=self.e.physics_steps/self.e.sim_freq,
            terminated=self.terminated,truncated=self.truncated,
            robots={self.task['embodiment']:dict(joint_positions=plain(robot.get_qpos())[0],joint_velocities=plain(robot.get_qvel())[0],previous_action=self.previous_action)},
            cameras={'scene':self._camera()} if camera_ids else {},
            privileged=dict(pieces={name:dict(position=o['p'],quaternion=o['q'],linear_velocity=o['v'],angular_velocity=o['w']) for name,o in state['objects'].items()},
                physics=dict(physics_hz=self.e.sim_freq,control_hz=self.e.control_freq)))

    def step(self,action):
        if self.finished or self.terminated or self.truncated:raise RuntimeError('Episode closed')
        a=np.asarray(action,dtype=float)
        if a.shape!=(self.action_spec['size'],) or not np.isfinite(a).all() or any(lo is not None and v<lo or hi is not None and v>hi for v,lo,hi in zip(a,self.action_spec['low'],self.action_spec['high'])):raise ValueError('Invalid action')
        import torch
        _,_,terminal,truncated,_=self.env.step(torch.as_tensor(a[None],dtype=torch.float32,device=self.e.device))
        self.steps+=1;self.previous_action=a.tolist();r=self.e.report
        self.terminated=bool(r['success'] or r['violations'] or np.asarray(plain(terminal)).any())
        self.truncated=bool(np.asarray(plain(truncated)).any() or self.steps>=self.max_steps) and not self.terminated
        return self.snapshot()

    def finish(self):
        if self._result is None:
            self.finished=True;r=self.e.report
            self._result=dict(success=bool(r['success'] and not r['violations']),score=float(bool(r['success'] and not r['violations'])),
                step_count=self.steps,terminated=self.terminated,truncated=self.truncated,
                reason='violation' if r['violations'] else 'success' if r['success'] else 'timeout' if self.truncated else 'owner_finish')
        return dict(self._result)

    abort=finish
    def close(self):self.env.close()
