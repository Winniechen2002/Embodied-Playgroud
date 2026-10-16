#!/usr/bin/env python3
"""Normal passive dynamics diagnostics. Does not certify a full environment condition."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'env/maniskill_lgd'))


def check(code,variant,seed,light):
    import numpy as np
    from agentbench_maniskill import make
    env=make(code,physics_variant=variant,light_scale=light,obs_mode='none',render_backend='none')
    try:
        env.reset(seed=seed);e=env.unwrapped
        assert not e.freeze_dynamics
        d=e.task.get('dynamics',{})
        deadline=max(r['seconds'] for r in e.task['history_rules'] if r['type']=='deadline')
        duration=max(5.,deadline+.05)
        measurements=dict(substeps=0,maximum_penetration_m=0.,maximum_linear_speed_m_s=0.,maximum_angular_speed_rad_s=0.)
        original=e._after_simulation_step
        def audit():
            original();measurements['substeps']+=1
            state=e.snapshot()
            for o in state['objects'].values():
                assert np.isfinite([*o['p'],*o['q'],*o['v'],*o['w']]).all(),'Nonfinite physics'
                measurements['maximum_linear_speed_m_s']=max(measurements['maximum_linear_speed_m_s'],float(np.linalg.norm(o['v'])))
                measurements['maximum_angular_speed_rad_s']=max(measurements['maximum_angular_speed_rad_s'],float(np.linalg.norm(o['w'])))
            for contact in e.scene.px.get_contacts():
                for point in contact.points:
                    assert math.isfinite(point.separation)
                    measurements['maximum_penetration_m']=max(measurements['maximum_penetration_m'],float(-point.separation))
        e._after_simulation_step=audit
        for _ in range(math.ceil(duration*e.control_freq)):env.step(e.hold_action())
        expected=math.ceil(d.get('start_after',.5)*e.control_freq)/e.control_freq if d else None
        assert getattr(e,'motion_started_at',None)==expected,'Incorrect trigger time'
        initial=getattr(e,'motion_initial_readback',{})
        for n,velocity in d.get('velocities',{}).items():
            expected_v=e.task.get('active_physics',{}).get('velocities',{}).get(n,velocity)
            assert np.allclose(initial[n]['linear_velocity'],expected_v,atol=1e-7)
        for n,velocity in d.get('angular_velocities',{}).items():
            assert np.allclose(initial[n]['angular_velocity'],velocity,atol=1e-7)
        spring=None
        if d.get('spring'):
            spec=d['spring'];art,joint=spec['joint'].split('/')
            native=next(j for j in e.articulations[art].get_active_joints() if j.name==joint)._objs[0]
            spring=dict(stiffness=native.stiffness,damping=native.damping,target=np.asarray(native.drive_target).tolist())
            params=e.task.get('active_physics',{}).get('spring',spec)
            assert np.isclose(spring['stiffness'],params['stiffness']) and np.isclose(spring['damping'],params['damping'])
            assert np.allclose(spring['target'],0)
        assert e.oracle.violations and getattr(e.oracle,'first_violation',None),'Unfinished no-action episode omitted its deadline'
        assert measurements['substeps']==e.physics_steps and e.physics_steps>=1200
        return dict(code=code,physics_variant=variant,seed=seed,light_scale=light,status='passed_diagnostic',
            task_spec_sha256=hashlib.sha256(json.dumps(e.task,sort_keys=True).encode()).hexdigest(),
            duration_s=e.physics_steps/e.sim_freq,physics_steps=e.physics_steps,measurements=measurements,
            trigger=dict(expected_seconds=expected,actual_seconds=getattr(e,'motion_started_at',None),velocities=initial,spring=spring),
            first_violation=e.oracle.first_violation,violations=e.oracle.violations,
            scope='Separate maintainer instance, normal passive dynamics; no client episode advanced after termination',
            qualification='Per-task admissible motion and penetration envelopes still require review; not a formal pass')
    finally:env.close()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--task',action='append');p.add_argument('--variant',type=int,action='append')
    p.add_argument('--seed',type=int,default=0);p.add_argument('--light-scale',type=float,default=1.)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    rows=[];a.output.parent.mkdir(parents=True,exist_ok=True)
    for code in a.task or [f'D{i}' for i in range(1,11)]:
        for variant in a.variant or [0,1,2]:
            try:r=check(code,variant,a.seed,a.light_scale)
            except Exception as exc:r=dict(code=code,physics_variant=variant,status='failed',error=repr(exc))
            rows.append(r);a.output.write_text(json.dumps(dict(scope='normal_dynamics_diagnostic',cases=rows),indent=2)+'\n')
            print(code,variant,r['status'],r.get('error',''),flush=True)
    return int(any(r['status']=='failed' for r in rows))


if __name__=='__main__':raise SystemExit(main())
