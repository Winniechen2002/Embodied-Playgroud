"""Evaluator unit tests. Synthetic contact/history flags are not executed trajectories."""
import copy,json,hashlib
from pathlib import Path
import numpy as np
from ..geometry_dynamics.oracle import TaskOracle

def test(t,initial,goal):
 checks=[]
 def check(name,value):checks.append(dict(name=name,passed=bool(value)))
 goal=copy.deepcopy(goal);goal['elapsed']=0
 if t.get('held_goal_objects'):
  for n in t['held_goal_objects']:goal['objects'][n]['robot_force']=.15
 def ready():
  o=TaskOracle(t,initial);o.done={m['id'] for m in t['milestones']};return o
 o=TaskOracle(t,initial);check('initial_rejected',not o.assess(initial)['success'])
 o=ready();check('valid_goal_predicates',o.assess(goal)['final_state_valid'])
 for _ in range(21):r=o.advance(goal)
 check('goal_after_synthetic_completed_history_and_dwell',r['success'])
 if any(m.get('requires') for m in t['milestones']):
  o0=TaskOracle(t,initial)
  for _ in range(22):o0.advance(goal)
  check('missing_required_events_rejected',not o0.assess(goal)['success'])
 for n in {c.get('object') for c in t['final'] if c.get('object')}:
  bad=copy.deepcopy(goal);bad['objects'][n]['p'][0]+=1;bad['objects'][n]['vertices']=(np.array(bad['objects'][n]['vertices'])+[1,0,0]).tolist();bad['objects'][n]['contacts']={};bad['objects'][n]['robot_force']=0
  oo=ready();check('wrong_target_'+n,not oo.assess(bad)['final_state_valid'])
 for c in t['final']:
  if c['type']=='bead_count':
   n=next(n for n in c['names'] if ready().predicate(dict(type='inside',object=n,**{k:c[k] for k in ['frame','low','high']}),goal));bad=copy.deepcopy(goal);bad['objects'][n]['vertices']=(np.array(bad['objects'][n]['vertices'])+[1,0,0]).tolist();check('incorrect_bead_count_'+c['frame'],not ready().predicate(c,bad))
 for n in t['protected']:
  oo=ready();bad=copy.deepcopy(goal);bad['objects'][n]['p'][0]+=.1;oo.advance(bad)
  for _ in range(22):oo.advance(goal)
  check('protected_moved_then_returned_'+n,not oo.assess(goal)['success'] and 'protected:'+n in oo.violations)
 for k in t.get('protected_joints',[]):
  oo=ready();bad=copy.deepcopy(goal);bad['joints'][k]['q']+=.20;oo.advance(bad)
  for _ in range(22):oo.advance(goal)
  check('neighbor_control_moved_'+k,not oo.assess(goal)['success'])
 for rule in t.get('history_rules',[]):
  oo=ready();bad=copy.deepcopy(goal);kind=rule['type']
  if kind=='upright':bad['objects'][rule['objects'][0]]['q']=[.70710678,.70710678,0,0]
  elif kind=='retain':
   n=rule['objects'][0];bad['objects'][n]['vertices']=(np.array(bad['objects'][n]['vertices'])+[2,0,0]).tolist()
  elif kind=='no_contact':bad['objects'][rule['objects'][0]]['robot_force']=1
  elif kind=='no_lift':bad['objects'][rule['object']]['vertices']=(np.array(bad['objects'][rule['object']]['vertices'])+[0,0,1]).tolist()
  elif kind=='soft_close':bad['joints'][rule['joint']].update(q=.01,v=-2.)
  elif kind=='no_rebound':
   bad['joints'][rule['joint']]['q']=0;oo.advance(bad);bad['joints'][rule['joint']]['q']=rule['reopened']+.05
  elif kind=='deadline':bad['elapsed']=rule['seconds']+1;oo.done=set()
  elif kind=='force_limit':bad['objects'][rule['object']].setdefault('contact_forces',{})[rule.get('support')]=rule['max_force']*2
  elif kind=='low_push':bad['objects'][rule['object']]['robot_contact_heights']=[rule['max_height']+.2]
  elif kind=='single_push':
   n=rule['object'];bad['objects'][n]['robot_force']=1;oo.advance(bad);bad['objects'][n]['robot_force']=0;oo.advance(bad);bad['objects'][n]['robot_force']=1
  else:raise ValueError(kind)
  oo.advance(bad)
  for _ in range(22):oo.advance(goal)
  check('latched_history_'+rule['name'],rule['name'] in oo.violations and not oo.assess(goal)['success'])
 # Generic stable hold and release checks; P10 intentionally requires contact.
 for what in ['moving','held']:
  bad=copy.deepcopy(goal);n=next(iter(bad['objects']),None)
  if n is None:
   if what=='moving':bad['joints'][next(iter(bad['joints']))]['v']=1
   else:bad['art_robot_force']=1
   check(what+'_invalid',not ready().assess(bad)['final_state_valid']);continue
  if what=='moving':bad['objects'][n]['v']=[.1,0,0]
  elif n in t.get('held_goal_objects',[]):bad['objects'][n]['robot_force']=0
  else:bad['objects'][n]['robot_force']=1
  check(what+'_invalid',not ready().assess(bad)['final_state_valid'])
 oo=ready();check('dwell_required',not oo.assess(goal)['success'])
 before=repr(oo.__dict__);state=json.dumps(goal,sort_keys=True)
 for _ in range(10):oo.assess(goal)
 check('read_only_assessment',before==repr(oo.__dict__) and state==json.dumps(goal,sort_keys=True))
 return dict(passed=all(c['passed'] for c in checks),checks=checks,scope='Unit tests with synthetic completed-milestone flags and contact perturbations; no robot execution.')
