"""Standalone ManiSkill extension: L1-L10, P1-P10, D1-D10."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def catalog():
    rows=[]
    for suite in ['long_horizon','geometry_dynamics']:
        for task in json.loads((ROOT/suite/'tasks.json').read_text()):
            rows.append(dict(code=task['code'],category=1 if suite=='long_horizon' else task['category'],title=task['title'],suite=suite,task_id=task['id'],robot=task['robot']['uid']))
    return rows

def specification(code,physics_variant=0):
    row=next((t for t in catalog() if t['code']==code.upper()),None)
    if row is None:raise ValueError(f'Unknown task {code!r}; expected L1-L10, P1-P10 or D1-D10')
    task=json.loads((ROOT/row['suite']/'tasks.json').read_text())[row['task_id']-1]
    if row['suite']=='geometry_dynamics':
        from .geometry_dynamics.variants import resolve
        task=resolve(task,physics_variant)
    elif physics_variant!=0:raise ValueError('Category 1 only has physics_variant=0')
    return row,task

def register_environments():
    from .long_horizon import env as long_horizon
    from .geometry_dynamics import env as geometry_dynamics

def make(code,physics_variant=0,**kwargs):
    """Construct a native simulator; normal dynamics are enabled by default."""
    row,_=specification(code,physics_variant)
    register_environments()
    import gymnasium as gym
    kwargs.setdefault('num_envs',1);kwargs.setdefault('control_mode','pd_joint_pos')
    if row['suite']=='long_horizon':
        if kwargs.pop('freeze_dynamics',False):raise ValueError('freeze_dynamics is a Category 3 diagnostic option')
        return gym.make('GenDexLongHorizon-v1',task_id=row['task_id'],**kwargs)
    return gym.make('GenDexGeometryDynamics-v1',task_id=row['task_id'],physics_variant=physics_variant,**kwargs)
