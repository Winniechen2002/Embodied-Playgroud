"""Developer diagnostics. Only normal env.step() may advance an evaluated episode."""
import copy,gc,json,platform
from pathlib import Path
import numpy as np
from . import ROOT,make,catalog,specification

def create(code,variant=0,render_backend='none',width=1800,freeze_dynamics=True):
    row,_=specification(code,variant)
    kwargs=dict(obs_mode='none',render_backend=render_backend,reward_mode='sparse',image_width=width)
    if render_backend!='none':kwargs['render_mode']='rgb_array'
    if row['category'] in [2,3]:kwargs['freeze_dynamics']=freeze_dynamics
    env=make(code,physics_variant=variant,**kwargs);env.reset(seed=8000+row['task_id'])
    return env

def initial_steps(e):
    return 0 if e.task['code']=='D2' else 120 if e.task['code'].startswith('L') else 90

def settle_goal(env):
    e=env.unwrapped;e.set_fixture('goal');held=e.task.get('goal_fixture_kind')=='held_pose_only';count=0;stable=0
    limit=0 if held else 1200 if e.task['code']=='P5' else 160 if e.task['code'].startswith('L') else 140
    for _ in range(limit):
        env.step(e.hold_action());count+=1
        if e.task['code']=='P5':
            stable=stable+1 if e.oracle.assess(e.snapshot())['final_state_valid'] else 0
            if stable>=20:break
    return held,count

def validate(code,variant,output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True);env=create(code,variant);e=env.unwrapped
    try:
        for _ in range(initial_steps(e)):env.step(e.hold_action())
        initial=e.snapshot();ir=copy.deepcopy(e.report);held,steps=settle_goal(env);goal=e.snapshot();gr=e.oracle.assess(goal)
        for name,state in [('initial',initial),('goal_fixture',goal)]:
            (output/(name+'_state.json')).write_text(json.dumps(state)+'\n')
        initial_ok=all(ir[k] for k in ['stable','no_fall','protected_ok','released']) and not ir['success']
        report=dict(code=code,physics_variant=variant,initial_passed=initial_ok,goal_passed=None if held else gr['final_state_valid'],passed=initial_ok and not held and gr['final_state_valid'],goal_steps=steps,initial=ir,goal=gr,platform=platform.platform(),robot_execution=False,scope='Initialized reference fixture; unvalidated held pose' if held else 'Initialized and physically settled reference fixtures, not a robot demonstration')
        (output/'validation.json').write_text(json.dumps(report,indent=2)+'\n');return report
    finally:env.close()

def smoke(code,output):
    import torch
    torch.set_num_threads(1)
    rows=[]
    selected=catalog() if code=='all' else [specification(code)[0]]
    for task in selected:
        env=None
        try:
            env=create(task['code'],freeze_dynamics=False);e=env.unwrapped
            for _ in range(12):obs,reward,terminated,truncated,info=env.step(e.hold_action())
            s=e.snapshot()
            assert all(np.isfinite(np.array(o['vertices'])).all() for o in s['objects'].values())
            assert 'success' in info and not bool(info['success'][0])
            for object_ in e.objects.values():assert len(object_._bodies[0].get_collision_shapes())>0
            rows.append(dict(code=task['code'],passed=True,dynamic_objects=len(e.objects),articulations=len(e.articulations),success_exposed=True,robot_dof=len(e.agent.robot.get_active_joints())))
            print(task['code'],'load/step/collision checks passed',flush=True)
        except Exception as exc:
            rows.append(dict(code=task['code'],passed=False,error=str(exc)));print(task['code'],'FAILED',str(exc),flush=True)
        finally:
            if env is not None:env.close()
            gc.collect()
    report=dict(passed=all(r['passed'] for r in rows),tasks=len(rows),rows=rows,scope='Native load, twelve hold steps with passive dynamics enabled, finite state, collision shapes and success signal; no task execution or solvability claim')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2)+'\n');return report

def render(code,variant,stage,output,backend,width):
    from PIL import Image
    from mani_skill.utils import sapien_utils
    row,_=specification(code,variant);env=create(code,variant,backend,width);e=env.unwrapped
    try:
        for _ in range(initial_steps(e)):env.step(e.hold_action())
        if stage=='goal':settle_goal(env)
        overrides=json.loads((ROOT/row['suite']/'camera_views.json').read_text()).get(str(row['task_id']),{})
        camera=overrides.get('overview',e.task['camera']);e._human_render_cameras['overview'].camera.set_local_pose(sapien_utils.look_at(camera['eye'],camera['target']).sp)
        for _ in range(3):rgb=env.render().cpu().numpy()[0]
        output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(rgb).save(output)
        report=dict(task=code,stage=stage,physics_variant=variant,image=output.name,robot_execution=False,scope='Initialized native simulator reference view; not a demonstration')
        output.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');return report
    finally:env.close()
