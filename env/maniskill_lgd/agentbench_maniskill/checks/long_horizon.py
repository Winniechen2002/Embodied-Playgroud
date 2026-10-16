"""Evaluator unit tests using synthetic histories; not physically executed robot trajectories."""
import json,copy,hashlib
import numpy as np
from pathlib import Path
from ..long_horizon.oracle import TaskOracle,rot

def settled(s):
 s=copy.deepcopy(s)
 for o in s['objects'].values():o['v']=[0,0,0];o['w']=[0,0,0];o['robot_force']=0
 for j in s['joints'].values():j['v']=0
 s['art_robot_force']=0
 return s

def satisfy(c,s,goal):
 ty=c['type']
 if ty=='joint':s['joints'][c['key']]['q']=(c['min']+c['max'])/2;return
 if ty=='region':
  n=c['object'];o=s['objects'][n];g=goal['objects'][n];o.update(copy.deepcopy(g));v=np.array(g['vertices']);frame=c.get('frame');R=np.eye(3);p=np.zeros(3)
  if frame and frame!='world':f=s['frames'][frame];R=rot(f['q']);p=np.array(f['p'])
  lv=(v-p)@R;delta=np.array([c['xy'][0]-(lv[:,0].min()+lv[:,0].max())/2,c['xy'][1]-(lv[:,1].min()+lv[:,1].max())/2,c['bottom']-lv[:,2].min()]);world=R@delta;o['vertices']=(v+world).tolist();o['p']=(np.array(g['p'])+world).tolist();o['contacts']={c['support']:True} if c.get('support') else g['contacts'];return
 if ty in ['clear','preserved','orientation']:
  if ty=='clear':
   for n,g in goal['objects'].items():s['objects'][n]=copy.deepcopy(g)
  elif ty=='orientation':s['objects'][c['object']]=copy.deepcopy(goal['objects'][c['object']])
  return
 raise ValueError(ty)

def run(task,initial,goal):
 checks=[]
 def check(name,value):checks.append(dict(name=name,passed=bool(value)))
 ref=settled(initial);goal=settled(goal);o=TaskOracle(task,ref);s=copy.deepcopy(ref)
 check('initial_does_not_succeed',not o.assess(s)['success'])
 # State finalization is distinct from action history: a teleported final scene cannot pass.
 finalonly=TaskOracle(task,ref)
 for _ in range(60):finalonly.advance(goal)
 check('final_state_without_access_history_rejected',not finalonly.assess(goal)['success'])
 for m in task['milestones']:
  for c in m['conditions']:satisfy(c,s,goal)
  for _ in range(m.get('hold_steps',2)+1):o.advance(s)
  check('milestone_'+m['id'],m['id'] in o.done)
 # Use the physically settled goal fixture, not artificially centered condition states.
 for _ in range(25):r=o.advance(goal)
 check('complete_history_then_stable_goal_accepted',r['success'])
 for c in task['final']:
  if c['type']!='region':continue
  n=c['object'];bad=copy.deepcopy(goal);bad['objects'][n]['p'][0]+=1.;v=np.array(bad['objects'][n]['vertices']);v[:,0]+=1;bad['objects'][n]['vertices']=v.tolist();bad['objects'][n]['contacts']={};oo=copy.deepcopy(o);check('missing_or_wrong_location_'+n,not oo.advance(bad)['success'])
 for n in task['protected']:
  oo=copy.deepcopy(o);bad=copy.deepcopy(goal);bad['objects'][n]['p'][0]+=.06;oo.advance(bad)
  for _ in range(25):oo.advance(goal)
  check('protected_moved_then_returned_'+n,not oo.assess(goal)['success'] and 'protected:'+n in oo.violations)
 for rule in task.get('forbidden',[]):
  oo=copy.deepcopy(o);bad=copy.deepcopy(goal)
  for c in rule['conditions']:satisfy(c,bad,goal)
  oo.advance(bad)
  for _ in range(25):oo.advance(goal)
  check('forbidden_history_'+rule['name'],not oo.assess(goal)['success'] and rule['name'] in oo.violations)
 # Goal must be released, stable, and held for one second; observations alone do not advance time.
 for name,mut in [('unreleased',lambda s:s['objects'][next(iter(s['objects']))].update(robot_force=1.)),('moving',lambda s:s['objects'][next(iter(s['objects']))].update(v=[.12,0,0]))]:
  oo=copy.deepcopy(o);bad=copy.deepcopy(goal);mut(bad);check(name+'_rejected',not oo.advance(bad)['success'])
 oo=copy.deepcopy(o);oo.dwell=0
 check('dwell_required',not oo.assess(goal)['success']);before=json.dumps(oo.__dict__,sort_keys=True,default=lambda x:sorted(x) if isinstance(x,set) else str(x));ss=json.dumps(goal,sort_keys=True)
 for _ in range(10):oo.assess(goal)
 check('read_only_evaluator',before==json.dumps(oo.__dict__,sort_keys=True,default=lambda x:sorted(x) if isinstance(x,set) else str(x)) and ss==json.dumps(goal,sort_keys=True))
 return dict(task=task['id'],passed=all(c['passed'] for c in checks),checks=checks,scope='Synthetic evaluator unit tests. No claim of robot execution or collision-free motion planning.')
