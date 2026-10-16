"""Read-only, contact-aware long-horizon success evaluator with dependency milestones."""
import numpy as np
from scipy.spatial.transform import Rotation

def rot(q):return Rotation.from_quat(np.roll(q,-1)).as_matrix()
def angle(a,b):return np.degrees(2*np.arccos(np.clip(abs(np.dot(a,b)),0,1)))
class TaskOracle:
 def __init__(self,task,reference):
  self.t=task;self.reference=reference;self.done=set();self.counts={};self.dwell=0;self.steps=0;self.violations=[]
 def predicate(self,c,s):
  typ=c['type']
  if typ=='joint':return c['min']<=s['joints'][c['key']]['q']<=c['max']
  if typ=='region':
   o=s['objects'][c['object']];v=np.array(o['vertices']);frame=c.get('frame')
   if frame and frame!='world':
    f=s['frames'][frame];v=(v-f['p'])@rot(f['q'])
   xy=np.array(c['xy']);half=np.array(c['half']);support=c.get('support')
   return bool(np.all(v[:,:2]>=xy-half) and np.all(v[:,:2]<=xy+half) and abs(v[:,2].min()-c['bottom'])<c.get('tolerance',.014) and (not support or o['contacts'].get(support,False)))
  if typ=='clear':
   lo=np.array(c['xy'])-c['half'];hi=np.array(c['xy'])+c['half']
   for n,o in s['objects'].items():
    if n in c.get('exclude',[]):continue
    v=np.array(o['vertices']);overlap=np.all(v[:,:2].max(0)>lo)&np.all(v[:,:2].min(0)<hi)
    if overlap and v[:,2].min()<c['z']+.20 and v[:,2].max()>c['z']-.015:return False
   return True
  if typ=='preserved':return self.preserved(c['object'],s,c.get('position_tolerance',.025),c.get('angle_tolerance',20))
  if typ=='orientation':return bool(np.dot(rot(s['objects'][c['object']]['q'])@c['axis'],c['world'])>=np.cos(np.radians(c.get('tolerance',15))))
  raise ValueError(typ)
 def preserved(self,n,s,pt=.025,at=20):
  o=s['objects'][n];ref=self.reference['objects'][n];return np.linalg.norm(np.array(o['p'])-ref['p'])<pt and angle(o['q'],ref['q'])<at
 def assess(self,s):
  rows=[dict(condition=c,ok=bool(self.predicate(c,s))) for c in self.t['final']]
  protected=all(self.preserved(n,s) for n in self.t['protected'])
  for k in self.t.get('protected_joints',[]):protected &= abs(s['joints'][k]['q']-self.reference['joints'][k]['q'])<(.008 if s['joints'][k]['type']=='prismatic' else .045)
  stable=all(np.linalg.norm(o['v'])<.025 and np.linalg.norm(o['w'])<.15 for o in s['objects'].values()) and all(abs(v['v'])<(.008 if v['type']=='prismatic' else .03) for v in s['joints'].values())
  released=all(o['robot_force']<.05 for o in s['objects'].values()) and s['art_robot_force']<.05
  nofall=all(np.array(o['vertices'])[:,2].min()>.035 for o in s['objects'].values())
  final_ok=all(r['ok'] for r in rows) and protected and stable and released and nofall
  instant=final_ok and len(self.done)==len(self.t['milestones']) and not self.violations
  return dict(success=bool(instant and self.dwell>=20),final_state_valid=bool(final_ok),instantaneous=bool(instant),conditions=rows,protected_ok=bool(protected),stable=bool(stable),released=bool(released),no_fall=bool(nofall),milestones=sorted(self.done),milestones_required=len(self.t['milestones']),dwell=self.dwell,violations=list(self.violations))
 def audit(self,s,*,physics_step=None,simulation_time=None):
  """Latch physical history without advancing control milestones or dwell."""
  previous_violations=len(self.violations)
  for n in self.t['protected']:
   if not self.preserved(n,s) and 'protected:'+n not in self.violations:self.violations.append('protected:'+n)
  for k in self.t.get('protected_joints',[]):
   tol=.008 if s['joints'][k]['type']=='prismatic' else .045
   if abs(s['joints'][k]['q']-self.reference['joints'][k]['q'])>tol and 'joint:'+k not in self.violations:self.violations.append('joint:'+k)
  if any(np.array(o['vertices'])[:,2].min()<.025 for o in s['objects'].values()) and 'dropped_object' not in self.violations:self.violations.append('dropped_object')
  for c in self.t.get('forbidden',[]):
   if all(self.predicate(p,s) for p in c['conditions']) and c['name'] not in self.violations:self.violations.append(c['name'])
  if len(self.violations)>previous_violations and getattr(self,"first_violation",None) is None:
   self.first_violation=dict(reason=self.violations[previous_violations],physics_step=physics_step,simulation_time_s=simulation_time)
  if not self.assess(s)["instantaneous"]:
   self.dwell=0
   if physics_step is not None:self._unstable_control_interval=True
  return list(self.violations)

 def advance(self,s):
  self.steps+=1
  self.audit(s)
  before=set(self.done)
  for m in self.t['milestones']:
   if m['id'] in before:continue
   good=all(x in before for x in m.get('requires',[])) and all(self.predicate(c,s) for c in m['conditions'])
   self.counts[m['id']]=self.counts.get(m['id'],0)+1 if good else 0
   if self.counts[m['id']]>=m.get('hold_steps',2):self.done.add(m['id'])
  r=self.assess(s);self.dwell=self.dwell+1 if r['instantaneous'] and not getattr(self,'_unstable_control_interval',False) else 0
  self._unstable_control_interval=False
  return self.assess(s)
