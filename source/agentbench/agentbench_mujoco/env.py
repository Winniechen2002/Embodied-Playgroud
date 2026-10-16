"""Panda contact manipulation, passive launcher and substep damage evaluation."""
from collections import deque
import numpy as np
import gymnasium as gym
from gymnasium import spaces
import mujoco as mj
from .scene import make_scene, HOME, LEVELS, MODES, BALL_OFFSET


class FrankaMarbleEnv(gym.Env):
    metadata={'render_modes':['rgb_array'],'render_fps':30}

    def __init__(self,level='direct',initial_mode='loaded',observation_mode='state',
                 render_mode=None,width=640,height=400,physics_dt=.001,decimation=20,
                 max_seconds=45.,damage_mode='impulse',impulse_threshold=.018,
                 pressure_threshold=2e5,contact_area=1e-4,damage_window=.03,dual_arm=False,
                 position_randomization='off',yaw_enabled=None,background_motion='static'):
        from .backgrounds import validate_background_motion
        validate_background_motion(background_motion)
        self.background_motion=background_motion
        from .positions import validate_position_randomization
        validate_position_randomization(position_randomization)
        self.position_randomization=position_randomization
        if level not in LEVELS or initial_mode not in MODES:
            raise ValueError('Invalid level or initial mode')
        if observation_mode not in ('state','vision') or render_mode not in (None,'rgb_array'):
            raise ValueError('Invalid observation/render mode')
        if not 0<physics_dt<=.002 or not isinstance(decimation,int) or decimation<1:
            raise ValueError('Expected physics_dt in (0, .002], positive integer decimation')
        if not 0<max_seconds<=300 or damage_mode not in ('impulse','pressure_proxy'):
            raise ValueError('Invalid duration or damage mode')
        if not 32<=width<=1280 or not 32<=height<=720:
            raise ValueError('Invalid camera resolution')
        damage_parameters=np.asarray([impulse_threshold,pressure_threshold,contact_area,damage_window])
        if not np.all(np.isfinite(damage_parameters)) or np.any(damage_parameters<=0):
            raise ValueError('Damage thresholds, contact area and window must be positive and finite')
        if damage_window>1:
            raise ValueError('Damage window must not exceed one second')
        self.dual_arm=bool(dual_arm)
        if yaw_enabled is not None and not isinstance(yaw_enabled,bool):
            raise ValueError('yaw_enabled must be a boolean or None')
        self.yaw_enabled=bool(yaw_enabled)
        if self.yaw_enabled and not self.dual_arm:
            raise ValueError('Yaw control requires the dual-arm launcher')
        self.arm_count=2 if dual_arm else 1
        self.prefixes=['','aim_'] if dual_arm else ['']
        self.arm_action_indices=np.array([8*a+j for a in range(self.arm_count) for j in range(7)])
        self.grip_action_indices=np.array([8*a+7 for a in range(self.arm_count)])
        self.speed_limits=np.tile([2.175]*4+[2.61]*3,self.arm_count)
        self.impulse_threshold=impulse_threshold
        self.pressure_threshold=pressure_threshold
        self.contact_area=contact_area
        self.damage_window=damage_window
        self.level,self.initial_mode,self.observation_mode=level,initial_mode,observation_mode
        self.render_mode=render_mode
        self.width,self.height=width,height
        self.physics_dt,self.decimation=physics_dt,decimation
        self.max_seconds,self.damage_mode=max_seconds,damage_mode
        self.renderer=None
        self.model=None
        lo=np.array([-2.8973,-1.7628,-2.8973,-3.0718,-2.8973,-.0175,-2.8973,-1],np.float64)
        hi=np.array([2.8973,1.7628,2.8973,-.0698,2.8973,3.7525,2.8973,1],np.float64)
        self.action_space=spaces.Box(np.tile(lo,self.arm_count),np.tile(hi,self.arm_count),dtype=np.float64)
        obs={'joint_pos':spaces.Box(-np.inf,np.inf,(9*self.arm_count,),np.float64),
             'joint_vel':spaces.Box(-np.inf,np.inf,(9*self.arm_count,),np.float64),
             'last_action':self.action_space,'task':spaces.Box(0,1,(6,),np.float64)}
        if observation_mode=='vision':
            obs['rgb']=spaces.Box(0,255,(height,width,3),np.uint8)
        else:
            obs.update(marble=spaces.Box(-np.inf,np.inf,(13,),np.float64),
                       launcher=spaces.Box(-np.inf,np.inf,(6,),np.float64),
                       launcher_anchor=spaces.Box(-np.inf,np.inf,(3,),np.float64),
                       aiming=spaces.Box(-np.inf,np.inf,(4,),np.float64),
                       aiming_locked=spaces.Box(0,1,(2,),np.float64),
                       aiming_ready=spaces.Box(0,1,(2,),np.float64),
                       blocks=spaces.Box(-np.inf,np.inf,(5,13),np.float64),
                       target=spaces.Box(-np.inf,np.inf,(4,),np.float64))
        if self.dual_arm and observation_mode=='state':
            obs['elevation']=spaces.Box(-np.inf,np.inf,(2,),np.float64)
        self.observation_space=spaces.Dict(obs)

    def reset(self,*,seed=None,options=None):
        super().reset(seed=seed)
        if options:
            raise ValueError('Reset options are not supported; choose a registered task')
        self.close()
        xml,self.scene_spec=self._build_scene()
        self.launcher_anchor=np.asarray(self.scene_spec['launcher_anchor'],dtype=float)
        self.model=mj.MjModel.from_xml_string(xml)
        self.data=mj.MjData(self.model)
        m,d=self.model,self.data
        self.robot_q=np.array([m.jnt_qposadr[m.joint(f'{prefix}joint{i}').id] for prefix in self.prefixes for i in range(1,8)])
        self.robot_v=np.array([m.jnt_dofadr[m.joint(f'{prefix}joint{i}').id] for prefix in self.prefixes for i in range(1,8)])
        self.finger_q=np.array([m.jnt_qposadr[m.joint(f'{prefix}finger_joint{i}').id] for prefix in self.prefixes for i in [1,2]])
        self.finger_v=np.array([m.jnt_dofadr[m.joint(f'{prefix}finger_joint{i}').id] for prefix in self.prefixes for i in [1,2]])
        self.draw_q=m.jnt_qposadr[m.joint('draw').id]
        self.draw_v=m.jnt_dofadr[m.joint('draw').id]
        self.ball_body=m.body('marble').id
        self.ball_geom=m.geom('marble').id
        self.carriage=m.body('carriage').id
        self.ball_q=m.jnt_qposadr[m.joint('marble_free').id]
        self.ball_v=m.jnt_dofadr[m.joint('marble_free').id]
        self.latch=m.equality('loaded_latch').id
        self.target_geom=m.geom('target0').id
        self.block_ids=[m.body(b['name']).id for b in self.scene_spec['blocks']]
        self.cup_geoms={m.geom(n).id for n in ['cup_floor','cup_side0','cup_side1','cup_back']}
        self.robot_bodies={m.body(prefix+n).id for prefix in self.prefixes for n in [f'link{i}' for i in range(8)]+['hand','left_finger','right_finger']}
        self.robot_arm={m.body(prefix+n).id:a for a,prefix in enumerate(self.prefixes)
                        for n in [f'link{i}' for i in range(8)]+['hand','left_finger','right_finger']}
        self.base_bodies={m.body(prefix+'link0').id for prefix in self.prefixes}
        self.arm_actuators=np.array([m.actuator(f'{prefix}actuator{i}').id for prefix in self.prefixes for i in range(1,8)])
        self.grip_actuators=np.array([m.actuator(prefix+'actuator8').id for prefix in self.prefixes])
        if self.dual_arm:
            self.elevation_q=m.jnt_qposadr[m.joint('elevation_hinge').id]
            self.elevation_v=m.jnt_dofadr[m.joint('elevation_hinge').id]
        self.yaw_q=self.yaw_v=None
        if self.yaw_enabled:
            self.yaw_q=m.jnt_qposadr[m.joint('yaw_hinge').id]
            self.yaw_v=m.jnt_dofadr[m.joint('yaw_hinge').id]
            self.aim_brakes=np.array([m.equality(n).id for n in ('yaw_brake','elevation_brake')])
            self.aim_handle_geoms=[m.geom(n).id for n in ('yaw_handle','wheel_handle')]
            self.brake_grip_dwell=np.zeros(2)
            self.brake_release_dwell=np.zeros(2)
            self.aim_contact_impulse=np.zeros(2)
            self.aim_cycle_ready=np.zeros(2,dtype=bool)
            self.preloaded_aiming_allowed=self.initial_mode=='loaded'
            self.premature_seat_time=0.
        d.qpos[self.robot_q]=np.tile(HOME,self.arm_count)
        d.qpos[self.finger_q]=.04
        d.ctrl[self.arm_actuators]=np.tile(HOME,self.arm_count);d.ctrl[self.grip_actuators]=255
        self.last_action=np.tile(np.r_[HOME,1.],self.arm_count)
        self.command=np.tile(HOME,self.arm_count)
        self.loaded=self.initial_mode=='loaded'
        self.armed=False;self.launched=False;self.popped=False
        self.finished=False;self.failure=None;self.launch_time=None
        self.events=[];self.max_draw=0.;self.max_pressure=0.
        self.control_steps=0
        self.wheel_contact_impulse=0.
        self.window=deque(maxlen=max(1,round(self.damage_window/self.physics_dt)))
        self.seat_time=0.;self.contact_sources=set()
        self.pop_source=None;self.toppled=set()
        self.max_penetration=0.;self.penetration_pair=None
        self.max_joint_speed=np.zeros(7*self.arm_count)
        self._last_progress=0.
        self._initialize_task()
        mj.mj_forward(m,d)
        # Authored inclines and upside-down compound pieces are valid starts.
        # Measure later tipping relative to their initial local vertical axes.
        self.block_up_reference=d.xmat[self.block_ids].reshape(-1,3,3)[:,:,2].copy()
        # Settle only the authored reset state; this is outside the agent episode.
        for _ in range(round(.25/self.physics_dt)):
            mj.mj_step(m,d)
        d.time=0.
        mj.mj_forward(m,d)
        return self._observation(),self._info()

    def _build_scene(self):
        if self.dual_arm:
            from .dual_scene import make_dual_scene
            return make_dual_scene(self.level,self.initial_mode,self.np_random,self.physics_dt,
                                   position_randomization=self.position_randomization,
                                   yaw_enabled=self.yaw_enabled)
        return make_scene(self.level,self.initial_mode,self.np_random,self.physics_dt,
                          position_randomization=self.position_randomization)

    def _initialize_task(self):
        pass

    def _body_state(self,body):
        j=self.model.body_jntadr[body]
        q=self.model.jnt_qposadr[j];v=self.model.jnt_dofadr[j]
        return np.r_[self.data.qpos[q:q+7],self.data.qvel[v:v+6]]

    def _aiming_state(self):
        """Yaw, yaw speed, absolute elevation and elevation speed, in radians."""
        d=self.data
        return np.array([d.qpos[self.yaw_q] if self.yaw_enabled else 0.,
                         d.qvel[self.yaw_v] if self.yaw_enabled else 0.,
                         np.pi/6+d.qpos[self.elevation_q] if self.dual_arm else np.pi/6,
                         d.qvel[self.elevation_v] if self.dual_arm else 0.],dtype=np.float64)

    def _aiming_locked(self):
        if self.yaw_enabled:
            return self.data.eq_active[self.aim_brakes].astype(np.float64)
        return np.array([1.,float(not self.dual_arm)])

    def _aiming_ready(self):
        return self.aim_cycle_ready.astype(np.float64) if self.yaw_enabled else np.ones(2)

    def _update_aim_brakes(self,contact_forces):
        """Ideal normally-on wheel brakes operated by actual gripper contact.

        A closed, contacting gripper squeezes the brake-release grip. Releasing
        that grip engages the brake at the live joint angle, without changing
        any body's pose or velocity. This is an explicit hybrid latch model;
        it does not simulate cable, lever compliance or brake wear.
        """
        if not self.yaw_enabled:return
        m,d=self.model,self.data
        for axis,(eq,q) in enumerate(zip(self.aim_brakes,(self.yaw_q,self.elevation_q))):
            # Yaw wheel belongs to the power arm; elevation to the other arm.
            held=contact_forces[axis]>.02 and self.last_action[8*axis+7]<0
            self.aim_contact_impulse[axis]+=max(0.,contact_forces[axis])*self.physics_dt
            self.brake_grip_dwell[axis]=self.brake_grip_dwell[axis]+self.physics_dt if held else 0.
            self.brake_release_dwell[axis]=0. if held else self.brake_release_dwell[axis]+self.physics_dt
            if d.eq_active[eq] and self.brake_grip_dwell[axis]>=.04:
                if self.loaded and not self.preloaded_aiming_allowed:
                    self.failure='aim_adjustment_after_loading'
                    return
                d.eq_active[eq]=False
                self.aim_cycle_ready[axis]=False
                self.events.append(dict(kind='aim_unlocked',axis=('yaw','elevation')[axis],time=float(d.time)))
            elif not d.eq_active[eq] and self.brake_release_dwell[axis]>=.06:
                # Joint-equality constant term is relative to qpos0.
                m.eq_data[eq,0]=d.qpos[q]-m.qpos0[q]
                d.eq_active[eq]=True
                self.aim_cycle_ready[axis]=True
                self.events.append(dict(kind='aim_locked',axis=('yaw','elevation')[axis],
                                        angle_deg=float(np.rad2deg(d.qpos[q])+(30. if axis else 0.)),time=float(d.time)))

    def _observation(self):
        d=self.data
        obs=dict(joint_pos=d.qpos[np.r_[self.robot_q,self.finger_q]].copy(),
                 joint_vel=d.qvel[np.r_[self.robot_v,self.finger_v]].copy(),
                 last_action=self.last_action.copy(),task=np.zeros(6))
        obs['task'][LEVELS.index(self.level)]=1
        obs['task'][4+MODES.index(self.initial_mode)]=1
        if self.observation_mode=='vision':
            obs['rgb']=self.render()
        else:
            blocks=np.zeros((5,13))
            for i,b in enumerate(self.block_ids):blocks[i]=self._body_state(b)
            obs.update(marble=self._body_state(self.ball_body),blocks=blocks,
                launcher_anchor=self.launcher_anchor.copy(),
                aiming=self._aiming_state(),
                aiming_locked=self._aiming_locked(),
                aiming_ready=self._aiming_ready(),
                launcher=np.array([d.qpos[self.draw_q],d.qvel[self.draw_v],self.loaded,self.armed,self.launched,self.popped],np.float64),
                target=np.r_[self.scene_spec['target'],float(not self.popped)])
        if self.dual_arm and self.observation_mode=='state':
            obs['elevation']=np.array([np.pi/6+d.qpos[self.elevation_q],d.qvel[self.elevation_v]])
        return obs

    def _info(self):
        basic={'is_success':bool(self.success),'elapsed_seconds':float(self.data.time)}
        if self.observation_mode=='state':
            basic.update(phase=self.phase,toppled=sorted(self.toppled),events=list(self.events),failure=self.failure)
        return basic

    @property
    def phase(self):
        return 'popped' if self.popped else 'flight' if self.launched else 'armed' if self.armed else 'loaded' if self.loaded else 'ground'

    @property
    def success(self):
        if not self.popped or self.failure:return False
        if self.level=='gate':return len(self.toppled)>=1
        if self.level=='bridge':return self.pop_source in {b['name'] for b in self.scene_spec['blocks']}
        if self.level=='domino':return len(self.toppled)>=3
        return True

    def _load_latch(self):
        # The declared launcher catch closes on a physically seated marble.
        # Preserve the live relative pose: never snap, teleport or weld to a finger.
        m,d=self.model,self.data
        inv=np.zeros(4);mj.mju_negQuat(inv,d.xquat[self.carriage])
        rel=np.zeros(3);mj.mju_rotVecQuat(rel,d.xpos[self.ball_body]-d.xpos[self.carriage],inv)
        quat=np.zeros(4);mj.mju_mulQuat(quat,inv,d.xquat[self.ball_body])
        m.eq_data[self.latch,3:6]=rel
        m.eq_data[self.latch,6:10]=quat
        d.eq_active[self.latch]=True
        self.loaded=True
        self.events.append({'kind':'loaded','time':float(d.time)})
        if self.yaw_enabled:
            self.events[-1]['aiming_locked']=self._aiming_locked().tolist()
            self.events[-1]['aiming_ready']=self._aiming_ready().tolist()

    def _after_physics(self):
        m,d=self.model,self.data
        mj.mj_kinematics(m,d)
        draw=float(d.qpos[self.draw_q])
        self.max_draw=max(self.max_draw,draw)
        cup_contact=False
        ball_robot_contact=False
        target_rows=[]
        aim_contact_forces=np.zeros(2)
        for i in range(d.ncon):
            c=d.contact[i];g1,g2=int(c.geom1),int(c.geom2)
            b1,b2=int(m.geom_bodyid[g1]),int(m.geom_bodyid[g2])
            robot_object=(b1 in self.robot_bodies) != (b2 in self.robot_bodies)
            if b1 in self.robot_bodies and b2 in self.robot_bodies:
                robot_object=self.robot_arm[b1]!=self.robot_arm[b2]
            base_floor=(bool(self.base_bodies.intersection((b1,b2))) and m.geom('floor').id in (g1,g2))
            if robot_object and not base_floor and -c.dist>self.max_penetration:
                self.max_penetration=float(-c.dist)
                self.penetration_pair=[m.body(b1).name,m.body(b2).name]
            if self.ball_geom in (g1,g2) and (g1 in self.cup_geoms or g2 in self.cup_geoms):
                cup_contact=True
            if self.ball_geom in (g1,g2) and (b1 in self.robot_bodies or b2 in self.robot_bodies):
                ball_robot_contact=True
            if self.dual_arm and m.geom('wheel_handle').id in (g1,g2):
                if self.robot_arm.get(b1)==1 or self.robot_arm.get(b2)==1:
                    f=np.zeros(6);mj.mj_contactForce(m,d,i,f)
                    self.wheel_contact_impulse+=max(0.,float(f[0]))*self.physics_dt
            if self.yaw_enabled:
                for axis,handle in enumerate(self.aim_handle_geoms):
                    other=b2 if g1==handle else b1 if g2==handle else None
                    if other is not None and self.robot_arm.get(other)==axis and 'finger' in m.body(other).name:
                        f=np.zeros(6);mj.mj_contactForce(m,d,i,f)
                        aim_contact_forces[axis]+=max(0.,float(f[0]))
            if self.target_geom in (g1,g2) and not self.popped:
                f=np.zeros(6);mj.mj_contactForce(m,d,i,f)
                other=g2 if g1==self.target_geom else g1
                if f[0]>0:
                    target_rows.append((float(f[0]),m.geom(other).name))
        self._update_aim_brakes(aim_contact_forces)
        if not self.loaded and not self.launched:
            delta=d.xpos[self.ball_body]-d.site('load_site').xpos
            seated=(cup_contact and np.linalg.norm(delta)<.025 and
                    np.linalg.norm(d.qvel[self.ball_v:self.ball_v+3])<.12 and
                    np.min(d.qpos[self.finger_q[:2]])>.027 and abs(draw)<(.015 if self.dual_arm else .006))
            if self.yaw_enabled:
                ready=bool(np.all(self._aiming_locked()) and np.all(self.aim_cycle_ready))
                # Detect a physically deposited projectile even if a policy
                # keeps an unrelated gripper closed to postpone catch closure.
                deposited=(cup_contact and not ball_robot_contact and np.linalg.norm(delta)<.025
                           and np.linalg.norm(d.qvel[self.ball_v:self.ball_v+3])<.12)
                self.premature_seat_time=self.premature_seat_time+self.physics_dt if deposited and not ready else 0.
                if self.premature_seat_time>=.06:
                    self.failure='loading_before_aim_cycle_complete'
                seated=seated and ready
            self.seat_time=self.seat_time+self.physics_dt if seated else 0.
            if self.seat_time>=.06:self._load_latch()
        if self.loaded and not self.launched:
            if draw>.04:self.armed=True
            if self.armed and draw<.008 and d.qvel[self.draw_v]<-.15:
                if self.yaw_enabled:
                    if not np.all(self._aiming_locked()):
                        self.failure='launch_before_aim_locked'
                        return
                    if not np.all(self.aim_cycle_ready):
                        self.failure='launch_before_aim_cycle_complete'
                        return
                d.eq_active[self.latch]=False
                self.loaded=False;self.launched=True;self.launch_time=float(d.time)
                self.events.append({'kind':'launched','time':self.launch_time,'speed':float(np.linalg.norm(d.qvel[self.ball_v:self.ball_v+3])),
                                    'yaw_deg':float(np.rad2deg(d.qpos[self.yaw_q])) if self.yaw_enabled else 0.,
                                    'elevation_deg':float(30+np.rad2deg(d.qpos[self.elevation_q])) if self.dual_arm else 30.})
                if self.yaw_enabled:
                    self.events[-1]['aiming_locked']=self._aiming_locked().tolist()
                    self.events[-1]['aiming_ready']=self._aiming_ready().tolist()
                    self.events[-1]['brake_error_deg']=[float(np.rad2deg(d.qpos[q]-m.qpos0[q]-m.eq_data[eq,0]))
                                                        for q,eq in zip((self.yaw_q,self.elevation_q),self.aim_brakes)]
                    self.aim_cycle_ready[:]=False
                    self.preloaded_aiming_allowed=False
                    self.premature_seat_time=0.
        self._update_targets(target_rows)
        for i,(b,spec) in enumerate(zip(self.block_ids,self.scene_spec['blocks'])):
            # More than 35 degrees from the authored orientation, or an 8 cm fall.
            up=d.xmat[b].reshape(3,3)[:,2]
            if np.dot(up,self.block_up_reference[i])<np.cos(np.deg2rad(35)) or d.xpos[b,2]<spec['pos'][2]-.08:
                self.toppled.add(spec['name'])
        if not np.all(np.isfinite(d.qpos)) or not np.all(np.isfinite(d.qvel)):
            self.failure='nonfinite_physics'
        self.max_joint_speed=np.maximum(self.max_joint_speed,np.abs(d.qvel[self.robot_v]))
        if self.max_penetration>.005:self.failure='robot_object_penetration_over_5mm'
        if self.dual_arm and not -.005<=draw<=.195:
            self.failure='launcher_slide_limit_violation'
        if self.dual_arm and not np.deg2rad(-17)<=d.qpos[self.elevation_q]<=np.deg2rad(27):
            self.failure='elevation_limit_violation'
        if self.yaw_enabled and not np.deg2rad(-27)<=d.qpos[self.yaw_q]<=np.deg2rad(27):
            self.failure='yaw_limit_violation'
        if np.any(self.max_joint_speed>1.1*self.speed_limits):
            self.failure='joint_overspeed_over_10pct_margin'
        if any(d.warning[int(w)].number for w in (mj.mjtWarning.mjWARN_BADQPOS,
                                                   mj.mjtWarning.mjWARN_BADQVEL,
                                                   mj.mjtWarning.mjWARN_BADQACC)):
            self.failure='physics_instability'

    def _update_targets(self,target_rows):
        m,d=self.model,self.data
        # Ignore static setup/pre-shot loads. Damage cannot accumulate indefinitely.
        force=sum(f for f,_ in target_rows) if self.launched else 0.
        self.window.append(force*self.physics_dt)
        self.max_pressure=max(self.max_pressure,force/self.contact_area)
        damage=(sum(self.window)>self.impulse_threshold if self.damage_mode=='impulse'
                else force/self.contact_area>self.pressure_threshold)
        if not self.popped and damage:
            self.popped=True
            self.pop_source=max(target_rows,key=lambda row:row[0],default=(0,None))[1]
            m.geom_contype[self.target_geom]=0;m.geom_conaffinity[self.target_geom]=0
            for g in range(m.ngeom):
                if m.geom_bodyid[g]==m.body('target0').id:m.geom_rgba[g,3]=0
            self.events.append({'kind':'popped','time':float(d.time),'source':self.pop_source,
                                'window_impulse':sum(self.window),'pressure_proxy':force/self.contact_area})

    def _shot_spent(self):
        return self.launched and self.data.time-self.launch_time>=5.

    def _progress(self):
        return float(self.popped)+.1*len(self.toppled)

    def step(self,action):
        if self.model is None:raise RuntimeError('Call reset first')
        if self.finished:raise RuntimeError('Episode finished; call reset')
        action=np.asarray(action,dtype=np.float64)
        if action.shape!=self.action_space.shape or not np.all(np.isfinite(action)) or not self.action_space.contains(action):
            raise ValueError(f'Expected {self.arm_count} blocks of 7 bounded joint targets in radians and a gripper command in [-1,1]')
        self.last_action=action.copy()
        self.control_steps+=1
        limits=self.speed_limits
        for _ in range(self.decimation):
            self.command+=np.clip(action[self.arm_action_indices]-self.command,-limits*self.physics_dt,limits*self.physics_dt)
            self.data.ctrl[self.arm_actuators]=self.command
            self.data.ctrl[self.grip_actuators]=np.where(action[self.grip_action_indices]>=0,255,0)
            mj.mj_step(self.model,self.data)
            self._after_physics()
            if self.success or self.failure:break
        terminal=bool(self.success or self.failure)
        timed_out=self.data.time>=self.max_seconds
        spent=self._shot_spent()
        truncated=bool(not terminal and (timed_out or spent))
        self.finished=terminal or truncated
        progress=self._progress()
        reward=progress-self._last_progress+(1. if self.success else 0.)
        self._last_progress=progress
        # Vision observations never expose per-step privileged damage rewards.
        if self.observation_mode=='vision':reward=float(self.success) if self.finished else 0.
        return self._observation(),reward,terminal,truncated,self._info()

    def render(self):
        if self.model is None:raise RuntimeError('Call reset first')
        if self.renderer is None:
            self.renderer=mj.Renderer(self.model,height=self.height,width=self.width)
        cam=mj.MjvCamera();cam.lookat[:]=[.98,.12,.28]
        cam.azimuth=110;cam.elevation=-22;cam.distance=3.20 if self.dual_arm else 2.8
        opt=mj.MjvOption();opt.geomgroup[3]=False;opt.geomgroup[4]=True
        mj.mj_kinematics(self.model,self.data)
        self.renderer.update_scene(self.data,cam,opt)
        if self.background_motion!='static':
            from .backgrounds import apply_background_motion
            visual_seed=self.scene_spec.get('variant',{}).get('realized',{}).get('visual_seed',0)
            apply_background_motion(self.renderer.scene,self.model,self.data.time,
                                    self.background_motion,visual_seed,getattr(self,'background',None))
        return self.renderer.render().copy()

    def private_result(self):
        return dict(level=self.level,initial_mode=self.initial_mode,dual_arm=self.dual_arm,success=bool(self.success),
                    yaw_enabled=self.yaw_enabled,
                    yaw_deg=float(np.rad2deg(self.data.qpos[self.yaw_q])) if self.yaw_enabled else 0.,
                    aiming_locked=self._aiming_locked().tolist(),
                    aiming_ready=self._aiming_ready().tolist(),
                    aim_contact_impulse_Ns=self.aim_contact_impulse.tolist() if self.yaw_enabled else [0.,self.wheel_contact_impulse],
                    position_randomization=self.scene_spec['position_randomization'],
                    elevation_deg=float(30+np.rad2deg(self.data.qpos[self.elevation_q])) if self.dual_arm else 30.,
                    wheel_contact_impulse_Ns=self.wheel_contact_impulse,
                    phase=self.phase,elapsed_seconds=float(self.data.time),events=list(self.events),
                    control_steps=self.control_steps,
                    toppled=sorted(self.toppled),max_draw_m=self.max_draw,
                    max_pressure_proxy_Pa=self.max_pressure,failure=self.failure,
                    max_robot_object_penetration_m=self.max_penetration,
                    penetration_pair=self.penetration_pair,max_joint_speed_radps=self.max_joint_speed.tolist())

    def close(self):
        if self.renderer is not None:
            self.renderer.close();self.renderer=None
