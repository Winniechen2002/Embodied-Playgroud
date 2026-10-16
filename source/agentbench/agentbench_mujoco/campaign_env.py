"""Finite-ammunition, multiple-target extension of the contact-only dual suite."""
from collections import deque
import numpy as np
import mujoco as mj
from gymnasium import spaces
from .env import FrankaMarbleEnv
from .scene import MODES
from .structures import MATERIALS
from .fracture import FractureSystem

SHAPES=('box','sphere','cylinder','wedge','gable','arch')
from .campaign_scene import (SCENARIOS, AMMO, MAX_AMMO, MAX_TARGETS, MAX_BLOCKS,
                             MAX_FIXED, MAX_FRAGMENTS, OBSERVATION_SCHEMA_VERSION, make_campaign_scene)


class FrankaCampaignEnv(FrankaMarbleEnv):
    def __init__(self, scenario='twins', initial_mode='loaded', max_seconds=150.,target_thresholds=None,
                 target_profile='authored', variation='nominal', background='park', visual_seed=None,
                 yaw_enabled=None, spring_stiffness=25., launcher_offset_m=(0.,0.,0.),
                 ammunition_offset_m=(0.,0.,0.), **kwargs):
        if scenario not in SCENARIOS:
            raise ValueError(f'Unknown scenario: {scenario}')
        self.scenario=scenario
        from .variants import validate_variant
        validate_variant(target_profile,variation,background,visual_seed)
        self.target_profile,self.variation,self.background=target_profile,variation,background
        self.visual_seed=None if visual_seed is None else int(visual_seed)
        from .launcher_variants import validate_launcher_configuration
        self.spring_stiffness,self.launcher_offset_m,self.ammunition_offset_m=validate_launcher_configuration(
            spring_stiffness,launcher_offset_m,ammunition_offset_m)
        self.threshold_overrides=None
        if target_thresholds is not None:
            values=np.asarray(target_thresholds,dtype=float)
            if values.shape!=(len(SCENARIOS[scenario]['targets']),) or not np.all(np.isfinite(values)) or np.any(values<=0):
                raise ValueError('Provide one positive finite impulse threshold per target')
            self.threshold_overrides=values.copy()
        if 'dual_arm' in kwargs or 'level' in kwargs:
            raise ValueError('Campaigns always use the dual-arm launcher')
        if yaw_enabled is None:
            yaw_enabled=SCENARIOS[scenario].get('yaw_enabled',False)
        super().__init__(level='direct',initial_mode=initial_mode,dual_arm=True,
                         max_seconds=max_seconds,yaw_enabled=yaw_enabled,**kwargs)
        obs={k:v for k,v in self.observation_space.spaces.items()
             if k in ('joint_pos','joint_vel','last_action','rgb')}
        obs['task']=spaces.Box(0,1,(len(SCENARIOS)+2,),np.float64)
        if self.observation_mode=='state':
            for name,shape in [('ammo',(MAX_AMMO,15)),('targets',(MAX_TARGETS,5)),
                               ('blocks',(MAX_BLOCKS,13)),('fixed',(MAX_FIXED,6)),
                               ('block_properties',(MAX_BLOCKS,6)),('fixed_properties',(MAX_FIXED,6)),
                               ('fragments',(MAX_FRAGMENTS,15)),('fragment_vertices',(MAX_FRAGMENTS,6,3)),
                               ('fracture_state',(MAX_BLOCKS,3)),('target_rules',(MAX_TARGETS,3)),
                               ('target_properties',(MAX_TARGETS,4)),
                               ('launcher',(6,)),('launcher_anchor',(3,)),('elevation',(2,)),('aiming',(4,))]:
                obs[name]=spaces.Box(-np.inf,np.inf,shape,np.float64)
            obs['aiming_locked']=spaces.Box(0,1,(2,),np.float64)
            obs['aiming_ready']=spaces.Box(0,1,(2,),np.float64)
            for name,size in [('ammo_mask',MAX_AMMO),('target_mask',MAX_TARGETS),
                              ('block_mask',MAX_BLOCKS),('fixed_mask',MAX_FIXED),('fragment_mask',MAX_FRAGMENTS)]:
                obs[name]=spaces.Box(0,1,(size,),np.float64)
        self.observation_space=spaces.Dict(obs)

    def _build_scene(self):
        xml,spec=make_campaign_scene(self.scenario,self.initial_mode,self.np_random,self.physics_dt,
                                   target_profile=self.target_profile,variation=self.variation,
                                   background=self.background,visual_seed=self.visual_seed,
                                   position_randomization=self.position_randomization,yaw_enabled=self.yaw_enabled,
                                   background_motion=self.background_motion,spring_stiffness=self.spring_stiffness,
                                   launcher_offset_m=self.launcher_offset_m,ammunition_offset_m=self.ammunition_offset_m)
        if self.threshold_overrides is not None:
            for target,value in zip(spec['targets'],self.threshold_overrides):target['impulse_threshold']=float(value)
            spec['variant']['threshold_override']=self.threshold_overrides.tolist()
        return xml,spec

    def _initialize_task(self):
        m=self.model
        self.ammo_ids=[m.body(a['name']).id for a in self.scene_spec['ammo']]
        self.ammo_geoms=[m.geom(a['name']).id for a in self.scene_spec['ammo']]
        self.ammo_q=[m.jnt_qposadr[m.joint(a['joint']).id] for a in self.scene_spec['ammo']]
        self.ammo_v=[m.jnt_dofadr[m.joint(a['joint']).id] for a in self.scene_spec['ammo']]
        self.latches=[m.equality(a['latch']).id for a in self.scene_spec['ammo']]
        self.ammo_status=np.zeros(len(self.ammo_ids),dtype=int)  # 0 unused, 1 retained, 2 fired
        self.ammo_status[0]=int(self.loaded)
        self.active_ammo=0
        self.shots=[]
        self.shot_peak_draw=0.
        self.target_ids=[m.body(t['name']).id for t in self.scene_spec['targets']]
        self.target_geoms=[m.geom(t['name']).id for t in self.scene_spec['targets']]
        self.target_alive=np.ones(len(self.target_ids),dtype=bool)
        cfg=SCENARIOS[self.scenario]
        self.protected_indices=set(cfg.get('protected',[]))
        if not self.protected_indices.issubset(range(len(self.target_ids))):
            raise ValueError('Protected target index out of range')
        self.required_indices=[i for i in range(len(self.target_ids)) if i not in self.protected_indices]
        if not self.required_indices:raise ValueError('A scenario requires at least one non-protected target')
        self.target_order=list(cfg.get('target_order',[]))
        if self.target_order and (len(set(self.target_order))!=len(self.target_order) or set(self.target_order)!=set(self.required_indices)):
            raise ValueError('Target order must list every required target exactly once')
        self.protected_hits=[]
        self.damage_windows=[deque(maxlen=max(1,round(self.damage_window/self.physics_dt)))
                             for _ in self.target_ids]
        self.target_hits=[]
        self.bank_hits=set()
        self.fixed_ids=[m.body(f['name']).id for f in self.scene_spec['fixed']]
        self.fixed_reference=np.array([f['pos'] for f in self.scene_spec['fixed']]).reshape(-1,3)
        self.fracture=FractureSystem(self)
        self.fragment_specs=[fragment for pane in self.scene_spec.get('fractures',[]) for fragment in pane['fragments']]
        self.logical_block_index={s['name']:i for i,s in enumerate(self.scene_spec['blocks'])}
        self._activate(0)

    def _activate(self,index):
        self.active_ammo=index
        self.ball_body=self.ammo_ids[index];self.ball_geom=self.ammo_geoms[index]
        self.ball_q=self.ammo_q[index];self.ball_v=self.ammo_v[index]
        self.latch=self.latches[index]
        self.seat_time=0.

    @property
    def success(self):
        return (hasattr(self,'target_alive') and not np.any(self.target_alive[self.required_indices])
                and len(self.toppled)>=SCENARIOS[self.scenario].get('min_toppled',0)
                and set(SCENARIOS[self.scenario].get('fracture_required',[])).issubset(self.fracture.broken)
                # Preserve a post-hit observation window for delayed collateral.
                and self._protected_observation_complete()
                and not self.failure)

    def _protected_observation_complete(self):
        if not self.protected_indices:return True
        hits=[hit['time'] for hit in self.target_hits if not hit.get('protected')]
        return bool(hits and self.data.time+1e-9>=max(hits)+3.)

    @property
    def phase(self):
        if self.success:return 'cleared'
        if self.launched:return 'flight'
        if self.armed:return 'armed'
        if self.loaded:return 'loaded'
        return 'reload' if self.shots else 'ground'

    def _load_latch(self):
        # Use the parent's physical seating gate and preserve this piece's pose.
        super()._load_latch()
        self.ammo_status[self.active_ammo]=1
        self.events[-1].update(ammo=self.active_ammo,kind_name=self.scene_spec['ammo'][self.active_ammo]['kind'])

    def _after_physics(self):
        d=self.data
        mj.mj_kinematics(self.model,d)
        if not self.loaded and not self.launched:
            available=np.flatnonzero(self.ammo_status==0)
            if len(available):
                near=min(available,key=lambda i:np.linalg.norm(d.xpos[self.ammo_ids[i]]-d.site('load_site').xpos))
                if near!=self.active_ammo and np.linalg.norm(d.xpos[self.ammo_ids[near]]-d.site('load_site').xpos)<.07:
                    self._activate(int(near))
        before=self.launched
        self.shot_peak_draw=max(self.shot_peak_draw,float(d.qpos[self.draw_q]))
        super()._after_physics()
        if self.launched and not before:
            self.ammo_status[self.active_ammo]=2
            event=next(event for event in reversed(self.events) if event['kind']=='launched')
            event.update(ammo=self.active_ammo,kind_name=self.scene_spec['ammo'][self.active_ammo]['kind'],
                         draw_m=self.shot_peak_draw)
            self.shots.append(dict(event))
        # Release authored bonds and enable sibling collisions after qualified
        # impacts. No pose, velocity, mass or projectile state is changed.
        sources=({self.ammo_ids[s['ammo']] for s in self.shots}|set(self.block_ids)|set(self.fracture.fragment_ids)) if self.shots else set()
        self.fracture.update(sources)
        # A shattered logical pane counts once, regardless of fragment count.
        self.toppled.update(self.fracture.broken)
        # Only re-arm the empty apparatus. No projectile is spawned or moved.
        if self.launched and d.time-self.launch_time>=3.:
            available=np.flatnonzero(self.ammo_status==0)
            if len(available):
                self.launched=False;self.loaded=False;self.armed=False
                self.shot_peak_draw=0.
                self._activate(int(available[0]))
                self.events.append(dict(kind='ready_for_reload',time=float(d.time),remaining=len(available)))

    def _update_targets(self,ignored_rows):
        m,d=self.model,self.data
        rows=[[] for _ in self.target_ids]
        # Only shots already released by the launcher, or movable structures,
        # can damage targets. Contacts from robot arms/unfired ammo do not score.
        fired={self.ammo_ids[s['ammo']] for s in self.shots}
        structures=set(self.block_ids)|set(self.fracture.fragment_ids)
        damaging=fired|structures
        allowed=damaging
        cfg=SCENARIOS[self.scenario]
        if cfg.get('indirect'):allowed=structures
        if cfg.get('damage_sources'):
            allowed={m.body(name).id for name in cfg['damage_sources']}
            allowed.update(b for b,parent in self.fracture.parent_by_body.items() if parent in cfg['damage_sources'])
        if cfg.get('required_bank'):
            bank=m.body(cfg['required_bank']).id
            for i in range(d.ncon):
                c=d.contact[i];b1=int(m.geom_bodyid[c.geom1]);b2=int(m.geom_bodyid[c.geom2])
                other=b2 if b1==bank else b1 if b2==bank else None
                if other in fired:
                    force=np.zeros(6);mj.mj_contactForce(m,d,i,force)
                    index=self.ammo_ids.index(other)
                    if force[0]>.01 and index not in self.bank_hits:
                        self.bank_hits.add(index)
                        self.events.append(dict(kind='bank_hit',ammo=index,bank=cfg['required_bank'],time=float(d.time)))
            allowed={self.ammo_ids[i] for i in self.bank_hits}
        for i in range(d.ncon):
            c=d.contact[i];g1,g2=int(c.geom1),int(c.geom2)
            for j,g in enumerate(self.target_geoms):
                if not self.target_alive[j] or g not in (g1,g2):continue
                other=g2 if g1==g else g1
                # Goal-source restrictions apply to required targets only.
                # Protected targets must not become immune to direct shots,
                # unqualified bank shots or other movable debris.
                target_sources=damaging if j in self.protected_indices else allowed
                if self.shots and int(m.geom_bodyid[other]) in target_sources:
                    force=np.zeros(6);mj.mj_contactForce(m,d,i,force)
                    if force[0]>0:rows[j].append((float(force[0]),m.geom(other).name))
        candidates=[]
        measurements={}
        for j,contacts in enumerate(rows):
            if not self.target_alive[j]:continue
            force=sum(f for f,_ in contacts)
            self.damage_windows[j].append(force*self.physics_dt)
            pressure=force/self.contact_area
            self.max_pressure=max(self.max_pressure,pressure)
            threshold=self.scene_spec['targets'][j]['impulse_threshold']
            popped=(sum(self.damage_windows[j])>threshold if self.damage_mode=='impulse'
                    else pressure>self.pressure_threshold)
            if not popped:continue
            candidates.append(j)
            measurements[j]=(pressure,sum(self.damage_windows[j]))
        # Simultaneous threshold crossings are one event batch, not an arbitrary
        # ordering induced by target array indices. Only the next target may pop.
        expected=next((j for j in self.target_order if self.target_alive[j]),None)
        wrong_order=bool(self.target_order and any(j!=expected for j in candidates if j not in self.protected_indices))
        for j in candidates:
            contacts=rows[j];pressure,impulse=measurements[j]
            self.target_alive[j]=False
            geom=self.target_geoms[j]
            m.geom_contype[geom]=0;m.geom_conaffinity[geom]=0
            for k in range(m.ngeom):
                if m.geom_bodyid[k]==self.target_ids[j]:m.geom_rgba[k,3]=0
            event=dict(kind='popped',target=j,time=float(d.time),
                       source=max(contacts,key=lambda x:x[0])[1],
                       window_impulse=impulse,pressure_proxy=pressure,
                       target_type=self.scene_spec['targets'][j]['size_name'])
            source_body=int(m.geom_bodyid[m.geom(event['source']).id])
            event['source_parent']=self.fracture.parent_by_body.get(source_body,m.body(source_body).name)
            event['protected']=j in self.protected_indices
            if j in self.protected_indices:
                self.protected_hits.append(j)
                self.failure='protected_target_hit'
            self.target_hits.append(event);self.events.append(event)
        if wrong_order and not self.failure:
            self.failure='target_order_violation'
            self.events.append(dict(kind='order_violation',time=float(d.time),expected=expected,hit=candidates))
        self.popped=not bool(np.any(self.target_alive[self.required_indices]))

    def _shot_spent(self):
        if len(self.shots)!=len(self.ammo_ids):return False
        deadline=self.shots[-1]['time']+5.
        if self.protected_indices and not np.any(self.target_alive[self.required_indices]):
            hits=[hit['time'] for hit in self.target_hits if not hit.get('protected')]
            if hits:deadline=max(deadline,max(hits)+3.)
        return self.data.time+1e-9>=deadline

    def _progress(self):
        return float(np.mean(~self.target_alive[self.required_indices]))+.1*len(self.toppled)

    def _observation(self):
        d=self.data
        obs=dict(joint_pos=d.qpos[np.r_[self.robot_q,self.finger_q]].copy(),
                 joint_vel=d.qvel[np.r_[self.robot_v,self.finger_v]].copy(),
                 last_action=self.last_action.copy(),task=np.zeros(len(SCENARIOS)+2))
        obs['task'][list(SCENARIOS).index(self.scenario)]=1
        obs['task'][len(SCENARIOS)+MODES.index(self.initial_mode)]=1
        if self.observation_mode=='vision':
            obs['rgb']=self.render()
            return obs
        for name,size,count in [('ammo',MAX_AMMO,len(self.ammo_ids)),('target',MAX_TARGETS,len(self.target_ids)),
                                ('block',MAX_BLOCKS,len(self.block_ids)),('fixed',MAX_FIXED,len(self.fixed_ids))]:
            mask=np.zeros(size);mask[:count]=1;obs[name+'_mask']=mask
        obs['ammo']=np.zeros((MAX_AMMO,15))
        for i,b in enumerate(self.ammo_ids):
            obs['ammo'][i]=np.r_[self._body_state(b),list(AMMO).index(self.scene_spec['ammo'][i]['kind']),self.ammo_status[i]]
        obs['targets']=np.zeros((MAX_TARGETS,5))
        obs['target_properties']=np.zeros((MAX_TARGETS,4))
        obs['launcher_anchor']=self.launcher_anchor.copy()
        obs['aiming']=self._aiming_state()
        obs['aiming_locked']=self._aiming_locked()
        obs['aiming_ready']=self._aiming_ready()
        for i,t in enumerate(self.scene_spec['targets']):
            obs['targets'][i]=[*t['pos'],self.target_alive[i],t['impulse_threshold']]
            obs['target_properties'][i]=[t['radius'],t['impulse_threshold'],t['size_code'],i in self.protected_indices]
        obs['block_properties']=np.zeros((MAX_BLOCKS,6))
        for i,spec in enumerate(self.scene_spec['blocks']):
            obs['block_properties'][i]=[SHAPES.index(spec.get('shape','box')),list(MATERIALS).index(spec.get('material','wood')),spec['mass'],*spec['size']]
        obs['fixed_properties']=np.zeros((MAX_FIXED,6))
        for i,spec in enumerate(self.scene_spec['fixed']):
            b=self.fixed_ids[i]
            obs['fixed_properties'][i]=[SHAPES.index(spec.get('shape','box')),list(MATERIALS).index(spec.get('material','stone')),*d.xquat[b]]
        obs['blocks']=np.zeros((MAX_BLOCKS,13))
        for i,b in enumerate(self.block_ids):obs['blocks'][i]=self._body_state(b)
        obs['fragments']=np.zeros((MAX_FRAGMENTS,15))
        obs['fragment_vertices']=np.zeros((MAX_FRAGMENTS,6,3))
        obs['fragment_mask']=np.zeros(MAX_FRAGMENTS)
        obs['fracture_state']=np.zeros((MAX_BLOCKS,3))
        for pane in self.scene_spec.get('fractures',[]):
            obs['fracture_state'][self.logical_block_index[pane['parent']]]=[1,pane['parent'] in self.fracture.broken,pane['anchored']]
        for i,spec in enumerate(self.fragment_specs):
            body=self.model.body(spec['name']).id
            obs['fragments'][i]=np.r_[self._body_state(body),self.logical_block_index[spec['parent']],spec['mass']]
            obs['fragment_vertices'][i]=spec['local_vertices']
            obs['fragment_mask'][i]=1
        obs['target_rules']=np.zeros((MAX_TARGETS,3))
        for i in range(len(self.target_ids)):
            rank=self.target_order.index(i)+1 if i in self.target_order else 0
            obs['target_rules'][i]=[i in self.required_indices,i in self.protected_indices,rank]
        obs['fixed']=np.zeros((MAX_FIXED,6))
        for i,f in enumerate(self.scene_spec['fixed']):obs['fixed'][i]=f['pos']+f['size']
        obs['launcher']=np.array([d.qpos[self.draw_q],d.qvel[self.draw_v],self.loaded,self.armed,self.launched,self.active_ammo],float)
        obs['elevation']=np.array([np.pi/6+d.qpos[self.elevation_q],d.qvel[self.elevation_v]])
        return obs

    def private_result(self):
        result=super().private_result()
        drift=max((float(np.linalg.norm(self.data.xpos[b]-p)) for b,p in zip(self.fixed_ids,self.fixed_reference)),default=0.)
        result.update(scenario=self.scenario,difficulty_tier=SCENARIOS[self.scenario]['tier'],
                      stage=SCENARIOS[self.scenario]['stage'],targets_total=len(self.target_ids),
                      targets_popped=int(np.count_nonzero(~self.target_alive)),
                      target_alive=self.target_alive.tolist(),ammo_total=len(self.ammo_ids),
                      shots_fired=len(self.shots),ammo_status=self.ammo_status.tolist(),
                      max_fixed_displacement_m=drift,shots=list(self.shots),bank_hits=sorted(self.bank_hits),
                      design_reference=SCENARIOS[self.scenario].get('reference'),
                      observation_schema_version=OBSERVATION_SCHEMA_VERSION,
                      variant=self.scene_spec['variant'],
                      launcher_configuration=self.scene_spec['launcher_configuration'],
                      target_properties=[dict(t,alive=bool(self.target_alive[i]),protected=i in self.protected_indices)
                                         for i,t in enumerate(self.scene_spec['targets'])],
                      capabilities=list(SCENARIOS[self.scenario]['capabilities']),split=SCENARIOS[self.scenario]['split'],
                      required_targets_total=len(self.required_indices),
                      required_targets_popped=int(np.count_nonzero(~self.target_alive[self.required_indices])),
                      protected_targets_total=len(self.protected_indices),protected_hits=list(self.protected_hits),
                      post_goal_observation_seconds=3. if self.protected_indices else 0.,
                      target_order=list(self.target_order),fractured=sorted(self.fracture.broken),
                      fracture_count=len(self.fracture.broken),
                      fracture_events=[event for event in self.events if event['kind']=='fracture'],
                      fracture_status=self.fracture.snapshot(),
                      fragment_count=len(self.fragment_specs),
                      materials=sorted({s.get('material','wood') for s in self.scene_spec['blocks']+self.scene_spec['fixed']}))
        return result
