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
  if typ=='center':return bool(np.all(np.array(s['objects'][c['object']]['p'])>=c['low']) and np.all(np.array(s['objects'][c['object']]['p'])<=c['high']))
  if typ=='lugs_engaged':
   o=s['objects'][c['object']];pts=np.array(c['points'])@rot(o['q']).T+o['p'];return bool(np.all(np.abs(pts-c['centers'])<=c['half']))
  if typ=='contact':return bool(s['objects'][c['object']]['contacts'].get(c['support'],False))
  if typ=='handle_on_hook':
   o=s['objects'][c['object']];p=np.array([c['hook'][0],o['p'][1],c['hook'][1]]);local=(p-o['p'])@rot(o['q']);return bool(np.linalg.norm((local-c['handle_center'])[[0,2]])<c['radius'])
  if typ=='speed':return c.get('min',0)<=np.linalg.norm(s['objects'][c['object']]['v'])<=c.get('max',1e9)
  if typ=='height':
   v=np.array(s['objects'][c['object']]['vertices']);return c.get('min',-1e9)<=v[:,2].min()<=c.get('max',1e9)
  if typ=='held':
   o=s['objects'][c['object']];return o['robot_force']>c.get('force',.05) and np.min(np.array(o['vertices'])[:,2])>c['min_height']
  if typ=='robot_contact':return c.get('min_force',0)<=s['objects'][c['object']]['robot_force']<=c.get('max_force',1e9)
  if typ=='joint_speed':return c.get('min',0)<=abs(s['joints'][c['key']]['v'])<=c.get('max',1e9)
  if typ=='airborne':
   o=s['objects'][c['object']];return not o['contacts'] and np.linalg.norm(o['v'])>c.get('min_speed',.08) and o['p'][0]>=c.get('min_x',-1e9)
  if typ=='bead_count':
   volume={k:v for k,v in c.items() if k in ['frame','low','high']}
   return sum(self.predicate(dict(type='inside',object=n,**volume),s) for n in c['names'])==c['count']
  if typ=='inside':
   v=np.array(s['objects'][c['object']]['vertices']);f=s['frames'].get(c.get('frame'))
   if f:v=(v-f['p'])@rot(f['q'])
   return bool(np.all(v>=c['low']) and np.all(v<=c['high']))
  if typ=='frame_orientation':
   f=s['frames'][c['frame']];return bool(np.dot(rot(f['q'])@c['axis'],c['world'])>=np.cos(np.radians(c.get('tolerance',5)))) and np.linalg.norm(f.get('w',[0,0,0]))<.03
  if typ=='frame_region':
   f=s['frames'][c['frame']];return np.linalg.norm(np.array(f['p'])[:2]-c['xy'])<c.get('tolerance',.04) and np.linalg.norm(f.get('v',[0,0,0]))<.03
  if typ=='semantic_count':
   hits=0
   for n,word in self.t['label_mapping'].items():
    if word==c['label'] and self.predicate(dict(type='inside',object=n,**c['volume']),s):hits+=1
   return hits==c['count']
  if typ=='stock_or_order':
   return all(any(self.predicate(dict(type='inside',object=n,**v),s) for v in c['volumes']) for n in self.t['label_mapping'])
  if typ=='rim_seated':
   o=s['objects'][c['object']];R=rot(o['q']);pts=np.array(c['points'])@R.T+o['p'];return bool(np.max(np.abs(pts[:,2]-c['height']))<c.get('gap',.006))
  raise ValueError(typ)
 def preserved(self,n,s,pt=.025,at=20):
  o=s['objects'][n];ref=self.reference['objects'][n];return np.linalg.norm(np.array(o['p'])-ref['p'])<pt and angle(o['q'],ref['q'])<at
 def assess(self,s):
  rows=[dict(condition=c,ok=bool(self.predicate(c,s))) for c in self.t['final']]
  protected=all(self.preserved(n,s) for n in self.t['protected'])
  for k in self.t.get('protected_joints',[]):protected &= abs(s['joints'][k]['q']-self.reference['joints'][k]['q'])<(.008 if s['joints'][k]['type']=='prismatic' else .045)
  stable=all(np.linalg.norm(o['v'])<.025 and np.linalg.norm(o['w'])<.15 for o in s['objects'].values()) and all(abs(v['v'])<(.008 if v['type']=='prismatic' else .03) for v in s['joints'].values())
  released=all(o['robot_force']<.05 for n,o in s['objects'].items() if n not in self.t.get('held_goal_objects',[])) and s['art_robot_force']<.05
  nofall=all(np.array(o['vertices'])[:,2].min()>.035 for o in s['objects'].values())
  final_ok=all(r['ok'] for r in rows) and protected and stable and released and nofall
  instant=final_ok and len(self.done)==len(self.t['milestones']) and not self.violations
  return dict(success=bool(instant and self.dwell>=20),final_state_valid=bool(final_ok),instantaneous=bool(instant),conditions=rows,protected_ok=bool(protected),stable=bool(stable),released=bool(released),no_fall=bool(nofall),milestones=sorted(self.done),milestones_required=len(self.t['milestones']),dwell=self.dwell,violations=list(self.violations))
 def audit(self,s,*,physics_step=None,simulation_time=None):
  """Latch physical history without advancing control milestones or dwell."""
  previous_violations=len(self.violations)
  def violate(name):
   if name not in self.violations:self.violations.append(name)
  for rule in self.t.get('history_rules',[]):
   kind=rule['type'];name=rule['name']
   if kind=='upright':
    for n in rule['objects']:
     if (rot(s['objects'][n]['q'])@rule.get('axis',[0,0,1]))[2]<np.cos(np.radians(rule.get('degrees',15))):violate(name)
   elif kind=='retain':
    for n in rule['objects']:
     if not self.predicate(dict(type='inside',object=n,**rule['volume']),s):violate(name)
   elif kind=='no_contact':
    if any(s['objects'][n]['robot_force']>.05 for n in rule['objects']):violate(name)
   elif kind=='no_lift':
    n=rule['object']
    if np.min(np.array(s['objects'][n]['vertices'])[:,2])>rule['max_bottom']:violate(name)
   elif kind=='single_push':
    touch=s['objects'][rule['object']]['robot_force']>.05
    previous=getattr(self,'touching',{});bouts=getattr(self,'contact_bouts',{})
    if touch and not previous.get(name,False):bouts[name]=bouts.get(name,0)+1
    previous[name]=touch;self.touching=previous;self.contact_bouts=bouts
    if bouts.get(name,0)>1:violate(name)
   elif kind=='soft_close':
    j=s['joints'][rule['joint']]
    if j['q']<.12 and abs(j['v'])>rule.get('max_speed',.45):violate(name)
   elif kind=='no_rebound':
    q=s['joints'][rule['joint']]['q'];closed=getattr(self,'closed_once',{})
    if closed.get(name,False) and q>rule['reopened']:violate(name)
    if q<rule['closed']:closed[name]=True
    self.closed_once=closed
   elif kind=='force_limit':
    if (s['objects'][rule['object']].get('contact_forces',{}).get(rule['support'],0) if rule.get('support') else s['objects'][rule['object']]['robot_force'])>rule['max_force']:violate(name)
   elif kind=='low_push':
    if any(z>rule['max_height'] for z in s['objects'][rule['object']].get('robot_contact_heights',[])):violate(name)
   elif kind=='deadline':
    if s.get('elapsed',self.steps*.05)>rule['seconds'] and not self.assess(s)['success']:violate(name)
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
