"""Ten native ManiSkill long-horizon environments. Units: meters, radians, kilograms."""
import sys,json,copy,os
import numpy as np, torch, sapien,trimesh
from scipy.spatial import ConvexHull
from .paths import ROOT
from ..common.paths import PREVIOUS,LEGACY,YCB,PREPARED
from ..common.robots import SUPPORTED_ROBOTS, register_robots
register_robots()
from mani_skill.envs.sapien_env import BaseEnv
from mani_skill.sensors.camera import CameraConfig
from mani_skill.utils import sapien_utils
from mani_skill.utils.registration import register_env
from mani_skill.utils.structs.types import SimConfig,SceneConfig
from ..common.asset_loader import build_asset,rot,quaternion
from ..common import fixtures as F
from .oracle import TaskOracle
TASKS=json.loads((ROOT/'tasks.json').read_text())
ASSETS=json.loads((PREVIOUS/'articulated/metadata.json').read_text())

@register_env('GenDexLongHorizon-v1',max_episode_steps=6000)
class LongHorizonEnv(BaseEnv):
 SUPPORTED_ROBOTS=SUPPORTED_ROBOTS
 def __init__(self,*args,task_id=1,image_width=1600,light_scale=1.,**kwargs):
  from ..common.evaluation import validate_light_scale
  self.light_scale=validate_light_scale(light_scale);self.physics_steps=0
  if int(task_id) not in range(1,len(TASKS)+1):raise ValueError('task_id must be 1..10')
  self.task=copy.deepcopy(TASKS[int(task_id)-1]);self.image_width=image_width
  if kwargs.get('num_envs',1)!=1:raise ValueError('Validated configuration is num_envs=1')
  kwargs['sim_backend']='cpu';super().__init__(*args,robot_uids=self.task['robot']['uid'],**kwargs)
 @property
 def _default_sim_config(self):return SimConfig(sim_freq=240,control_freq=20,scene_config=SceneConfig(contact_offset=.001,solver_position_iterations=40,solver_velocity_iterations=10,enable_tgs=True))
 @property
 def _default_sensor_configs(self):
  c=self.task['camera'];return [CameraConfig('scene',sapien_utils.look_at(c['eye'],c['target']),960,720,.70,.01,30,shader_pack=os.getenv('GENDEX_SHADER','default'))]
 @property
 def _default_human_render_camera_configs(self):
  c=self.task['camera'];return CameraConfig('overview',sapien_utils.look_at(c['eye'],c['target']),self.image_width,int(self.image_width*.70),.70,.01,30,shader_pack=os.getenv('GENDEX_SHADER','default'))
 def _load_lighting(self,options):
  if self.scene.can_render():
   self.scene.set_ambient_light((np.array([.32,.35,.39])*self.light_scale).tolist());self.scene.add_directional_light([-.7,.3,-1.3],(np.array([2.0,1.89,1.75])*self.light_scale).tolist(),shadow=True,shadow_scale=4,shadow_map_size=4096);self.scene.add_directional_light([.6,-1,-.7],(np.array([.43,.49,.58])*self.light_scale).tolist(),shadow=False)
 def _load_agent(self,options):
  r=self.task['robot'];p=np.array(r['position'],float);q=quaternion([0,0,r.get('yaw',0)])
  if r['uid'].startswith('everyday_robot'):
   ix=int(r['uid'].split('_')[-1]);folder=next((LEGACY/'robots').glob(f'{ix:02d}_*'));original=json.loads((folder/'physical_model.json').read_text())['base_position'];p-=rot(q)@np.array(original)
  self.robot_root_pose=sapien.Pose(p,q);super()._load_agent(options,self.robot_root_pose)
  from ..common.collision_filters import restore_native_self_collision_filters
  restore_native_self_collision_filters(self.agent)
 def register_art(self,name,a,meta,s):
  self.articulations[name]=a;self.art_specs[name]=s;self.builders.append(getattr(a,'_source_builder',None));self.joint_names[name]=[j.name for j in a.get_active_joints()]
  for l in a.get_links():self.supports[name+'/'+l.name.split('__',1)[-1]]=l
  for j in a.get_active_joints():
   k=name+'/'+j.name;limits=np.array(j.get_limits()).flatten().tolist();self.joint_meta[k]={'type':'prismatic' if j.type[0]=='prismatic' else 'revolute','limits':limits}
   # Counterbalanced appliance doors retain hand-set poses; no goal-following drives.
   if s['kind']=='source':
    if 'door' in j.name.lower():j.set_drive_properties(stiffness=0,damping=12,force_limit=20);j.set_friction(8)
    if 'knob' in j.name.lower():
     body=j.child_link._bodies[0];ratio=.04/max(float(body.mass),1e-8);body.inertia=np.maximum(np.array(body.inertia)*ratio,1e-7);body.mass=.04
  if s['kind']=='case':
   j=next(j for j in a.get_active_joints() if j.name=='latch');j.set_drive_properties(stiffness=0,damping=2,force_limit=.5);j.set_drive_target(s.get('initial_latch',.045))
  a.set_qpos(np.zeros(len(self.joint_names[name])))
 def _load_scene(self,options):
  self.builders=[];self.objects={};self.vertices={};self.meta={};self.supports={};self.articulations={};self.art_specs={};self.joint_names={};self.joint_meta={};self.material=sapien.physx.PhysxMaterial(.7,.55,.01)
  F.room(self)
  for s in self.task['furniture']:
   if s['kind']=='table':F.table(self,s)
   elif s['kind']=='container':F.open_container(self,s)
   elif s['kind']=='static':F.build_static(self,s['name'],s['position'],s['shapes'])
   elif s['kind'] in ['drawer','cupboard','case']:F.storage(self,s)
   elif s['kind']=='source':
    c=ASSETS[s['asset']];a,m,_=build_asset(self.scene,PREVIOUS/c['model'],s['name'],s['scale'],s['position'],s.get('rotation',[0,0,0]),self.scene.can_render(),s.get('extras'));self.register_art(s['name'],a,m,s)
  self.set_joint_state(self.task['initial_joints'])
  for o in self.task['objects']:self.build_object(o)
  r=self.task['robot']
  if r['uid'].startswith('everyday_robot'):
   ix=int(r['uid'].split('_')[-1]);pose=json.loads((PREVIOUS/'robot_poses'/f'{ix:02d}.json').read_text());pose.update(json.loads((ROOT/'stowed_poses.json').read_text()).get(str(self.task['id']),{}));self.initial_qpos=np.array([pose[j.name] for j in self.agent.robot.get_active_joints()],np.float32)
  else:self.initial_qpos=self.agent.keyframes['rest'].qpos.copy()
 def build_object(self,o):
  b=self.scene.create_actor_builder();vs=[]
  if 'asset' in o:
   folder=(PREPARED if o.get('source')=='prepared' else YCB/'objects')/o['asset'];d=json.loads((folder/'physics.json').read_text());sc=o.get('scale',1)
   if self.scene.can_render():b.add_visual_from_file(str(folder/d['visual']),scale=[sc]*3)
   for f in d['collisions']:
    b.add_convex_collision_from_file(str(folder/f),scale=[sc]*3,material=self.material);vs.append(np.array(trimesh.load_mesh(folder/f,process=False).vertices)*sc)
   b.set_mass_and_inertia(d['mass_kg']*sc**3,sapien.Pose(np.array(d['center_of_mass_m'])*sc,d['principal_frame_quaternion_wxyz']),np.array(d['principal_inertia_kg_m2'])*sc**5)
   self.meta[o['name']]=d
  else:
   for sh in o['shapes']:
    if sh['type']=='box':
     F.box(self,b,sh['half'],sh.get('p',[0,0,0]),sh['color']);v=np.array([[x,y,z] for x in [-1,1] for y in [-1,1] for z in [-1,1]])*sh['half']+sh.get('p',[0,0,0])
    else:
     F.cylinder(self,b,sh['radius'],sh['height'],sh.get('p',[0,0,0]),sh['color']);v=np.array([[sh['radius']*np.cos(t),sh['radius']*np.sin(t),z] for t in np.linspace(0,2*np.pi,25) for z in [-sh['height']/2,sh['height']/2]])+sh.get('p',[0,0,0])
    vs.append(v)
   v=np.concatenate(vs);dim=np.ptp(v,axis=0);mass=o.get('mass',.12);I=mass/12*np.array([dim[1]**2+dim[2]**2,dim[0]**2+dim[2]**2,dim[0]**2+dim[1]**2]);b.set_mass_and_inertia(mass,sapien.Pose((v.min(0)+v.max(0))/2),I);self.meta[o['name']]={'mass_kg':mass,'mass_provenance':'Engineering estimate; rigid prop','collision_provenance':'Exact primitive compound'}
  from ..common.foliage import add as add_foliage
  add_foliage(self,b,vs,o['name'])
  v=np.concatenate(vs);self.vertices[o['name']]=v[ConvexHull(v).vertices];b.initial_pose=self.placement_pose(o['name'],o['initial']);self.objects[o['name']]=b.build(name=o['name']);self.builders.append(b)
 def frame_pose(self,frame):return sapien.Pose() if frame in [None,'world'] else self.supports[frame].pose.sp
 def placement_pose(self,name,c):
  q=quaternion(c.get('rpy',[0,0,0]));v=self.vertices[name]@rot(q).T;p=[*c['xy'],c['bottom']-v[:,2].min()+c.get('gap',.002)]
  return self.frame_pose(c.get('frame'))*sapien.Pose(p,q)
 def set_joint_state(self,values):
  for n,a in self.articulations.items():
   a.set_qpos([values.get(n+'/'+k,0.) for k in self.joint_names[n]]);a.set_qvel(np.zeros(len(self.joint_names[n])))
 def _initialize_episode(self,env_idx,options):
  self.agent.robot.set_pose(self.robot_root_pose);self.agent.reset(self.initial_qpos);self.set_joint_state(self.task['initial_joints'])
  for o in self.task['objects']:
   a=self.objects[o['name']];a.set_pose(self.placement_pose(o['name'],o['initial']));a.set_linear_velocity([0,0,0]);a.set_angular_velocity([0,0,0])
  self.physics_steps=0
  self.oracle=TaskOracle(self.task,self.snapshot());self.report=self.oracle.assess(self.snapshot())
 def hold_action(self):
  names=[j.name for j in self.agent.robot.get_active_joints()];uid=self.task['robot']['uid'];d={'arm':torch.tensor([[float(self.initial_qpos[names.index(n)]) for n in self.agent.arm_joint_names]],device=self.device)}
  if uid.startswith('everyday'):d['hand']=torch.tensor([[float(self.initial_qpos[names.index(n)]) for n in self.agent.hand_joint_names]],device=self.device)
  else:
   d['gripper']=torch.ones((1,1),device=self.device)
   if uid=='fetch':d.update(body=torch.zeros((1,3),device=self.device),base=torch.zeros((1,2),device=self.device))
  return self.agent.controller.from_action_dict(d)
 def snapshot(self):
  force={}
  for c in self.scene.get_contacts():
   bs=c.bodies if hasattr(c,'bodies') else [c.body0,c.body1];key=frozenset([b.entity.name for b in bs]);force[key]=force.get(key,0)+sum(float(np.linalg.norm(p.impulse)) for p in c.points)*self.sim_freq
  rn={l._bodies[0].entity.name for l in self.agent.robot.get_links()};names={k:a._bodies[0].entity.name for k,a in {**self.supports,**self.objects}.items()};out={}
  for n,a in self.objects.items():
   p=a.pose.p[0].cpu().numpy();q=a.pose.q[0].cpu().numpy();b=a._bodies[0];native=b.entity.name
   out[n]=dict(p=p.tolist(),q=q.tolist(),v=np.asarray(b.linear_velocity).tolist(),w=np.asarray(b.angular_velocity).tolist(),vertices=(self.vertices[n]@rot(q).T+p).tolist(),contacts={k:force.get(frozenset([native,v]),0)>1e-4 for k,v in names.items() if k!=n and force.get(frozenset([native,v]),0)>1e-4},robot_force=sum(force.get(frozenset([native,r]),0) for r in rn))
  js={};af=0
  for n,a in self.articulations.items():
   q=a.get_qpos()[0].cpu().numpy();v=a.get_qvel()[0].cpu().numpy()
   for i,k in enumerate(self.joint_names[n]):js[n+'/'+k]=dict(q=float(q[i]),v=float(v[i]),type=self.joint_meta[n+'/'+k]['type'])
   af+=sum(force.get(frozenset([l._bodies[0].entity.name,r]),0) for l in a.get_links() for r in rn)
  frames={k:dict(p=a.pose.p[0].cpu().tolist(),q=a.pose.q[0].cpu().tolist()) for k,a in self.supports.items()}
  return dict(objects=out,joints=js,frames=frames,art_robot_force=af,robot_qpos=self.agent.robot.get_qpos()[0].cpu().tolist())
 def set_fixture(self,stage='goal'):
  """Validation only: set a reference state. This is NOT a robot demonstration."""
  self.set_joint_state(self.task['goal_joints'] if stage=='goal' else self.task['initial_joints'])
  for o in self.task['objects']:
   a=self.objects[o['name']];a.set_pose(self.placement_pose(o['name'],o.get('goal',o['initial']) if stage=='goal' else o['initial']));a.set_linear_velocity([0,0,0]);a.set_angular_velocity([0,0,0])
 def _after_simulation_step(self):
  self.physics_steps+=1
  if hasattr(self,'oracle'):
   snapshot=self.snapshot();snapshot['elapsed']=self.physics_steps/self.sim_freq
   self.oracle.audit(snapshot,physics_step=self.physics_steps,simulation_time=self.physics_steps/self.sim_freq)
 def _after_control_step(self):self.report=self.oracle.advance(self.snapshot())
 def evaluate(self):return {k:torch.tensor([v],device=self.device) for k,v in getattr(self,'report',{}).items() if isinstance(v,(bool,int,float))}
 def _get_obs_extra(self,info):return {}
 def compute_dense_reward(self,obs,action,info):return torch.tensor([sum(r['ok'] for r in self.report['conditions'])/max(1,len(self.report['conditions']))],device=self.device)
 def compute_normalized_dense_reward(self,obs,action,info):return self.compute_dense_reward(obs,action,info)
