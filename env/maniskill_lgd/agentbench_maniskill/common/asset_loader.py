"""Native SAPIEN articulations from existing MJCF/URDF meshes and joint topology.
Source box/cylinder collisions are retained; MuJoCo motors are not used.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np, sapien, trimesh
from scipy.spatial.transform import Rotation

def numbers(s,default):return np.array([float(v) for v in s.split()]) if s else np.array(default,dtype=float)
def quaternion(rpy):return np.roll(Rotation.from_euler('xyz',rpy).as_quat(),1)
def rot(q):return Rotation.from_quat(np.roll(q,-1)).as_matrix()
def pose_of(e,urdf=False,degrees=False):
 if e is None:return sapien.Pose()
 p=numbers(e.get('xyz' if urdf else 'pos'),[0,0,0]);q=numbers(e.get('quat'),[1,0,0,0])
 if 'rpy' in e.attrib or 'euler' in e.attrib:q=quaternion(numbers(e.get('rpy',e.get('euler')),[0,0,0])*(np.pi/180 if degrees else 1))
 return sapien.Pose(p,q)
def axis_quat(axis):
 x=np.array(axis,dtype=float);x/=np.linalg.norm(x);v=np.array([0,0,1]) if abs(x[2])<.9 else np.array([0,1,0]);y=np.cross(v,x);y/=np.linalg.norm(y);z=np.cross(x,y)
 return np.roll(Rotation.from_matrix(np.stack([x,y,z],axis=1)).as_quat(),1)
def corners(half):return np.array([[x,y,z] for x in [-half[0],half[0]] for y in [-half[1],half[1]] for z in [-half[2],half[2]]])

def parse_model(path):
 path=Path(path);root=ET.parse(path).getroot();links=[];materials={}
 def geometry(el,attr,urdf=False):
  if urdf:
   shape=list(el.find('geometry'))[0];kind=shape.tag;at=shape.attrib;po=pose_of(el.find('origin'),True)
   v=dict(type=kind,p=po.p.tolist(),q=po.q.tolist())
   if kind=='mesh':v.update(file=str(path.parent/at['filename']),scale=numbers(at.get('scale'),[1,1,1]).tolist())
   elif kind=='box':v['half']=(numbers(at['size'],[])/2).tolist()
   elif kind in ['cylinder','capsule']:v.update(radius=float(at['radius']),length=float(at['length']))
   elif kind=='sphere':v['radius']=float(at['radius'])
   return v
  po=pose_of(ET.Element('geom',attr),degrees=degrees);kind=attr.get('type','sphere');v=dict(type=kind,p=po.p.tolist(),q=po.q.tolist())
  sz=numbers(attr.get('size'),[.01,.01,.01])
  if kind=='mesh':v.update(meshes[attr['mesh']])
  elif kind=='box':v['half']=sz.tolist()
  elif kind in ['cylinder','capsule']:v.update(radius=float(sz[0]),length=float(sz[1]*2))
  elif kind=='sphere':v['radius']=float(sz[0])
  v['material']=materials.get(attr.get('material'),dict(rgba=numbers(attr.get('rgba'),[.65,.65,.65,1]).tolist()))
  return v
 if root.tag=='robot':
  children={j.find('child').get('link'):j for j in root.findall('joint')};ls={l.get('name'):l for l in root.findall('link')}
  def visit(name,parent=None):
   l=ls[name];j=children.get(name);po=pose_of(j.find('origin'),True) if j is not None else sapien.Pose()
   d=dict(name=name,parent=parent,p=po.p.tolist(),q=po.q.tolist(),visuals=[geometry(v,None,True) for v in l.findall('visual')],collisions=[geometry(v,None,True) for v in l.findall('collision')])
   if j is not None and j.get('type')!='fixed':
    lim=j.find('limit');d['joint']=dict(name=j.get('name'),type='prismatic' if j.get('type')=='prismatic' else 'revolute',axis=numbers(j.find('axis').get('xyz'),[1,0,0]).tolist(),pivot=[0,0,0],limits=[float(lim.get('lower',-3.14)),float(lim.get('upper',3.14))])
   links.append(d)
   for child,cj in children.items():
    if cj.find('parent').get('link')==name:visit(child,name)
  for name in ls:
   if name not in children:visit(name)
 else:
  compiler=root.find('compiler');degrees=compiler is None or compiler.get('angle','degree')=='degree';meshes={};defaults={}
  for m in root.findall('./asset/mesh'):meshes[m.get('name')]=dict(file=str(path.parent/m.get('file')),scale=numbers(m.get('scale'),[1,1,1]).tolist())
  textures={t.get('name'):str(path.parent/t.get('file')) for t in root.findall('./asset/texture') if t.get('file')}
  for m in root.findall('./asset/material'):materials[m.get('name')]=dict(rgba=numbers(m.get('rgba'),[1,1,1,1]).tolist(),texture=textures.get(m.get('texture')))
  def defs(el,base={}):
   a=dict(base);g=el.find('geom')
   if g is not None:a.update(g.attrib)
   defaults[el.get('class','')]=a
   for sub in el.findall('default'):defs(sub,a)
  for d in root.findall('default'):defs(d)
  def visit(body,parent=None):
   name=body.get('name',f'body_{len(links)}');po=pose_of(body,degrees=degrees)
   d=dict(name=name,parent=parent,p=po.p.tolist(),q=po.q.tolist(),visuals=[],collisions=[])
   js=body.findall('joint')
   if len(js)>1:
    for ji,j in enumerate(js[:-1]):
     kind='prismatic' if j.get('type','hinge')=='slide' else 'revolute';lim=numbers(j.get('range'),[-np.pi,np.pi])
     if kind=='revolute' and degrees:lim*=np.pi/180
     dn=name+'_axis_'+str(ji)
     links.append(dict(name=dn,parent=parent,p=po.p.tolist(),q=po.q.tolist(),visuals=[],collisions=[],joint=dict(name=j.get('name'),type=kind,axis=numbers(j.get('axis'),[0,0,1]).tolist(),pivot=numbers(j.get('pos'),[0,0,0]).tolist(),limits=lim.tolist())))
     parent=dn;po=sapien.Pose()
    d.update(parent=parent,p=po.p.tolist(),q=po.q.tolist());js=js[-1:]
   if js:
    j=js[0];kind='prismatic' if j.get('type','hinge')=='slide' else 'revolute';lim=numbers(j.get('range'),[-np.pi,np.pi])
    if kind=='revolute' and degrees:lim*=np.pi/180
    if j.get('limited')=='false' or not j.get('range'):lim=np.array([-6.283,6.283])
    d['joint']=dict(name=j.get('name'),type=kind,axis=numbers(j.get('axis'),[0,0,1]).tolist(),pivot=numbers(j.get('pos'),[0,0,0]).tolist(),limits=lim.tolist())
   for g in body.findall('geom'):
    a=dict(defaults.get(g.get('class',''),defaults.get('',{})));a.update(g.attrib);cls=a.get('class','');v=geometry(g,a)
    collidable=int(a.get('contype','1'))!=0
    visual=('visual' in cls or (a.get('material') and 'collision' not in cls)) and float(v['material']['rgba'][-1])>0
    if collidable:d['collisions'].append(v)
    if visual:d['visuals'].append(v)
   links.append(d)
   for child in body.findall('body'):visit(child,name)
  for body in root.findall('./worldbody/body'):visit(body)
 return links

def geom_vertices(g):
 if g['type']=='mesh':
  s=trimesh.load(g['file'],force='scene',process=False);v=np.concatenate([m.vertices for m in s.dump()])*g.get('scale',[1,1,1])
 elif g['type']=='box':v=corners(g['half'])
 else:
  radius=g['radius'];h=g.get('length',2*radius)/2;v=corners([radius,radius,h])
 return v@rot(g['q']).T+g['p']

def rest_geometry(links,rotation=[0,0,0]):
 poses={};vertices=[];joint_info={};R=sapien.Pose(q=quaternion(rotation))
 for l in links:
  parent=poses.get(l['parent'],R);p=parent*sapien.Pose(l['p'],l['q']);poses[l['name']]=p
  vv=[geom_vertices(g) for g in l['collisions'] or l['visuals']]
  if vv:
   v=np.concatenate(vv)@rot(p.q).T+p.p;vertices.append(v)
  if 'joint' in l:
   j=l['joint'];joint_info[j['name']]=dict(**j,link=l['name'],anchor=(rot(p.q)@j['pivot']+p.p).tolist(),world_axis=(rot(p.q)@j['axis']).tolist())
 v=np.concatenate(vertices);return [v.min(0).tolist(),v.max(0).tolist()],joint_info

def build_asset(scene,path,name,scale,position,rotation,render=True,extras=None):
 links=parse_model(path);ab=scene.create_articulation_builder();built={};poses={};joint_info={};material=sapien.physx.PhysxMaterial(.65,.5,0)
 for l in links:
  b=ab.create_link_builder(built.get(l['parent']));b.set_name(name+'__'+l['name']);built[l['name']]=b
  po=sapien.Pose(np.array(l['p'])*scale,l['q']);parent_pose=poses.get(l['parent'],sapien.Pose());poses[l['name']]=parent_pose*po
  if 'joint' in l:
   j=l['joint'];ax=axis_quat(j['axis']);pivot=sapien.Pose(np.array(j['pivot'])*scale,ax);limits=np.array(j['limits'])*(scale if j['type']=='prismatic' else 1)
   b.set_joint_name(j['name']);b.set_joint_properties(j['type'],[limits],po*pivot,pivot,friction=.12 if 'button' in j['name'].lower() else 1.5,damping=3 if j['type']=='prismatic' else 1)
   joint_info[j['name']]=dict(j,limits=limits.tolist(),link=l['name'])
  elif l['parent'] is not None:b.set_joint_properties('fixed',[],po,sapien.Pose())
  for g in l['collisions']:
   pose=sapien.Pose(np.array(g['p'])*scale,g['q']);kw=dict(pose=pose,material=material,density=300)
   if g['type']=='box':b.add_box_collision(half_size=np.array(g['half'])*scale,**kw)
   elif g['type']=='mesh':b.add_convex_collision_from_file(g['file'],scale=np.array(g.get('scale',[1,1,1]))*scale,**kw)
   elif g['type']=='sphere':b.add_sphere_collision(radius=g['radius']*scale,**kw)
   elif g['type'] in ['cylinder','capsule']:
    # SAPIEN's primitive axis is X; MJCF/URDF use Z.
    kw['pose']=pose*sapien.Pose(q=axis_quat([0,0,1]));getattr(b,'add_'+g['type']+'_collision')(radius=g['radius']*scale,half_length=g['length']*scale/2,**kw)
  if render:
   for g in l['visuals']:
    pose=sapien.Pose(np.array(g['p'])*scale,g['q']);m=g.get('material');mat=None
    if m:
     mat=sapien.render.RenderMaterial(base_color=m['rgba'],roughness=.55,metallic=.15)
     if m.get('texture'):mat.base_color_texture=sapien.render.RenderTexture2D(filename=m['texture'])
    if g['type']=='mesh':b.add_visual_from_file(g['file'],pose=pose,scale=np.array(g.get('scale',[1,1,1]))*scale,material=mat)
    elif g['type']=='box':b.add_box_visual(pose=pose,half_size=np.array(g['half'])*scale,material=mat)
  for g in (extras or {}).get(l['name'],[]):
   pp=sapien.Pose(np.array(g['p'])*scale);hh=np.array(g['half'])*scale
   b.add_box_collision(half_size=hh,pose=pp,material=material,density=250)
   if render:b.add_box_visual(half_size=hh,pose=pp,material=sapien.render.RenderMaterial(base_color=[.38,.41,.43,1],roughness=.55))
  # Source dummy URDF inertias are intentionally replaced with collision-density inertias.
 ab.initial_pose=sapien.Pose(position,quaternion(rotation));art=ab.build(name=name,fix_root_link=True)
 art._source_builder=ab
 art._visual_vertices={l['name']:np.concatenate([geom_vertices(g) for g in l['visuals']])*scale for l in links if l['visuals']} if render else {}
 return art,joint_info,poses
