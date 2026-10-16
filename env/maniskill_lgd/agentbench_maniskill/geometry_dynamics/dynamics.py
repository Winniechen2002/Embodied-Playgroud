"""Passive episode physics. Task success never drives target objects toward goals."""
import numpy as np


def advance(e):
    d=e.task.get('dynamics',{})
    if not d or e.freeze_dynamics:return
    if not e.motion_started and e.elapsed>=d.get('start_after',.5):
        e.motion_started=True
        e.motion_started_at=e.elapsed
        e.motion_initial_readback={}
        for n,v in d.get('velocities',{}).items():
            v=e.task.get('active_physics',{}).get('velocities',{}).get(n,v)
            e.objects[n].set_linear_velocity(v)
            e.motion_initial_readback.setdefault(n,{})['linear_velocity']=np.asarray(e.objects[n]._bodies[0].linear_velocity).tolist()
        for n,w in d.get('angular_velocities',{}).items():
            e.objects[n].set_angular_velocity(w)
            e.motion_initial_readback.setdefault(n,{})['angular_velocity']=np.asarray(e.objects[n]._bodies[0].angular_velocity).tolist()
    if d.get('spring') and e.motion_started:
        spec=d['spring'];art,jname=spec['joint'].split('/')
        j=next(j for j in e.articulations[art].get_active_joints() if j.name==jname)
        params=e.task.get('active_physics',{}).get('spring',spec)
        j.set_drive_properties(stiffness=params['stiffness'],damping=params['damping'],force_limit=8)
        j.set_drive_target(0)
