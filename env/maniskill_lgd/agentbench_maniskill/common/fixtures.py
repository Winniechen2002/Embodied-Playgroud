"""Collision-bearing furniture and functional storage fixtures in SI units."""
import numpy as np,sapien
from .asset_loader import axis_quat

WOOD=(.43,.25,.12); LIGHT=(.76,.66,.48); METAL=(.15,.18,.19)
def box(e,b,half,p,color=LIGHT,collision=True,roughness=.65):
 if collision:b.add_box_collision(half_size=half,pose=sapien.Pose(p),material=e.material,density=450)
 if e.scene.can_render():b.add_box_visual(half_size=half,pose=sapien.Pose(p),material=sapien.render.RenderMaterial(base_color=[*color,1],roughness=roughness))
def cylinder(e,b,r,h,p,color=METAL,collision=True,axis=(0,0,1)):
 pose=sapien.Pose(p,axis_quat(axis))
 if collision:b.add_cylinder_collision(radius=r,half_length=h/2,pose=pose,material=e.material,density=500)
 if e.scene.can_render():b.add_cylinder_visual(radius=r,half_length=h/2,pose=pose,material=sapien.render.RenderMaterial(base_color=[*color,1],roughness=.45))
def build_static(e,name,position,shapes):
 b=e.scene.create_actor_builder()
 for half,p,color in shapes:box(e,b,half,p,color)
 b.initial_pose=sapien.Pose(position);a=b.build_static(name);e.builders.append(b);e.supports[name]=a;return a

def table(e,s):
 w,d,z=s['size'];name=s['name'];color=s.get('color',WOOD);sh=[([w/2,d/2,.025],[0,0,z-.025],color)]
 for x in [-w/2+.06,w/2-.06]:
  for y in [-d/2+.06,d/2-.06]:sh.append(([.035,.035,(z-.05)/2],[x,y,(z-.05)/2],s.get('legs',METAL)))
 return build_static(e,name,[*s['xy'],0],sh)

def open_container(e,s):
 w,d,h=s['size'];th=s.get('thickness',.008);name=s['name'];color=s.get('color',LIGHT);sh=[([w/2,d/2,th/2],[0,0,th/2],color)]
 for x in [-w/2+th/2,w/2-th/2]:sh.append(([th/2,d/2,h/2],[x,0,h/2],color))
 for y in [-d/2+th/2,d/2-th/2]:sh.append(([w/2,th/2,h/2],[0,y,h/2],color))
 for x in s.get('dividers',[]):sh.append(([th/2,d/2,h/2],[x,0,h/2],color))
 if s.get('rails'):
  for x in [-w/2+.015,w/2-.015]:sh.append(([.015,d/2-.010,.012],[x,0,.061],color))
 a=build_static(e,name,s['position'],sh)
 # Handles are visual furniture details; the basket itself is anchored to the surface.
 if s.get('handles') and e.scene.can_render():
  b=e.scene.create_actor_builder()
  for x in [-w/2,w/2]:
   for y in [-.08,.08]:cylinder(e,b,.007,.10,[x,y,h+.04],color,False)
   cylinder(e,b,.007,.16,[x,0,h+.09],color,False,axis=(0,1,0))
  b.initial_pose=sapien.Pose(s['position']);e.builders.append(b);b.build_static(name+'_handles')
 return a

def storage(e,s):
 """Real prismatic drawer / hinged cupboard / hinged case with sliding latch."""
 w,d,h=s['size'];th=.016 if s['kind']!='case' else .009;name=s['name'];color=s.get('color',LIGHT);ab=e.scene.create_articulation_builder();root=ab.create_link_builder();root.set_name(name+'__body')
 if s['kind']=='drawer':
  for x in [-w/2,w/2]:box(e,root,[th/2,d/2,h/2],[x,0,h/2],color)
  box(e,root,[w/2,th/2,h/2],[0,d/2,h/2],color);box(e,root,[w/2,d/2,th/2],[0,0,h],color)
  mov=ab.create_link_builder(root);mov.set_name(name+'__tray');mov.set_joint_name('slide');ax=axis_quat([0,-1,0]);mov.set_joint_properties('prismatic',[[0,s.get('travel',.30)]],sapien.Pose(q=ax),sapien.Pose(q=ax),friction=5,damping=5)
  box(e,mov,[w/2-th,d/2-th,th/2],[0,0,th/2],color)
  for x in [-w/2+th/2,w/2-th/2]:box(e,mov,[th/2,d/2-th,h*.32],[x,0,th+h*.32],color)
  for y in [-d/2+th/2,d/2-th/2]:box(e,mov,[w/2,th/2,h*.42],[0,y,th+h*.42],color)
  box(e,mov,[.09,.015,.012],[0,-d/2-.025,h*.5],METAL)
 elif s['kind']=='cupboard':
  for x in [-w/2,w/2]:box(e,root,[th/2,d/2,h/2],[x,0,h/2],color)
  box(e,root,[w/2,th/2,h/2],[0,d/2,h/2],color)
  for z in [th/2,h,*s.get('shelves',[])]:box(e,root,[w/2,d/2,th/2],[0,0,z],color)
  door=ab.create_link_builder(root);door.set_name(name+'__door');door.set_joint_name('door');ax=axis_quat([0,0,1]);door.set_joint_properties('revolute',[[-1.60,0]],sapien.Pose([-w/2,-d/2-th/2,0],ax),sapien.Pose(q=ax),friction=2,damping=2)
  box(e,door,[w/2,th/2,h/2],[w/2,0,h/2],s.get('front',color));box(e,door,[.012,.025,.07],[w-.07,-.025,h*.5],METAL)
 elif s['kind']=='case':
  box(e,root,[w/2,d/2,th/2],[0,0,th/2],color)
  for x in [-w/2,w/2]:box(e,root,[th/2,d/2,h/2],[x,0,h/2],color)
  for y in [-d/2,d/2]:box(e,root,[w/2,th/2,h/2],[0,y,h/2],color)
  for x in s.get('dividers',[]):box(e,root,[.006,d/2-.01,h*.42],[x,0,h*.42],(.13,.14,.14))
  lid=ab.create_link_builder(root);lid.set_name(name+'__lid');lid.set_joint_name('lid');lid.set_joint_properties('revolute',[[-1.65,0]],sapien.Pose([0,d/2,h]),sapien.Pose(),friction=1.5,damping=1.5)
  box(e,lid,[w/2+.008,d/2+.010,.007],[0,-d/2,.009],color);box(e,lid,[.07,.015,.018],[0,-d/2,.025],METAL)
  latch=ab.create_link_builder(root);latch.set_name(name+'__latch');latch.set_joint_name('latch');ax=axis_quat([1,0,0]);latch.set_joint_properties('prismatic',[[0,.045]],sapien.Pose([0,-d/2-.018,h+.040],ax),sapien.Pose(q=ax),friction=4,damping=12)
  box(e,latch,[.022,.008,.012],[0,-.003,0],(.72,.73,.72))
  box(e,lid,[.018,.009,.005],[0,-d-.020,.017],(.44,.46,.46))
  for x in s.get('divider_slots',[]):
   for dx in [-.020,.020]:box(e,root,[.004,d/2-.013,.016],[x+dx,0,.024],(.17,.18,.18))
 ab.initial_pose=sapien.Pose(s['position']);a=ab.build(name=name,fix_root_link=True);e.builders.append(ab);e.register_art(name,a,None,s)
 return a

def room(e):
 t=e.task;pal=t['palette'];wall=pal['wall'];floor=pal['floor']
 build_static(e,'floor',[0,0,0],[([2.4,2.6,.05],[0,0,-.05],floor)])
 from .collision_filters import configure_fetch_floor
 configure_fetch_floor(e)
 build_static(e,'architecture',[0,0,0],[([2.4,.06,1.4],[0,1.7,1.4],wall),([.06,2.1,1.4],[-2.4,-.4,1.4],wall),([2.4,.022,.055],[0,1.61,.055],(.9,.89,.85)),([.023,2.1,.055],[-2.31,-.4,.055],(.9,.89,.85))])
 if not e.scene.can_render():return
 # Window, trim, timber floor boards, framed art, and shelves stay outside manipulation volumes.
 b=e.scene.create_actor_builder();box(e,b,[.58,.012,.45],[-.55,1.625,1.80],(.54,.70,.72),False)
 for x in [-1.15,.05]:box(e,b,[.025,.045,.48],[x,1.60,1.80],(.92,.90,.84),False)
 for z in [1.32,2.28]:box(e,b,[.62,.045,.026],[-.55,1.60,z],(.92,.90,.84),False)
 box(e,b,[.016,.036,.44],[-.55,1.59,1.80],(.92,.90,.84),False);box(e,b,[.62,.08,.02],[-.55,1.54,1.31],WOOD,False)
 box(e,b,[.29,.018,.38],[.88,1.61,1.92],WOOD,False);box(e,b,[.26,.021,.35],[.88,1.58,1.92],(.89,.85,.74),False)
 for i in range(5):box(e,b,[.025,.003,.15+i*.022],[.73+i*.07,1.553,1.86],pal['accent'],False)
 for i in range(17):box(e,b,[.001,2.45,.0002],[-2.3+i*.28,-.6,.0004],tuple(float(v*.77) for v in floor),False)
 for y in [-2,-.8,.4,1.6]:box(e,b,[2.3,.001,.0002],[0,y,.0004],tuple(float(v*.77) for v in floor),False)
 b.initial_pose=sapien.Pose();e.builders.append(b);b.build_static('room_visual_details')
