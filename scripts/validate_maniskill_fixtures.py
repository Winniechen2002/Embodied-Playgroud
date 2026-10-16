#!/usr/bin/env python3
"""Private physical scoring fixtures, not client actions or task-solving trajectories."""
import argparse
import json
from pathlib import Path
import platform
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'env/maniskill_lgd'))


def held_washer(output):
    import numpy as np
    import sapien
    import torch
    from agentbench_maniskill import make
    from agentbench_maniskill.common.asset_loader import quaternion
    # Measured native Panda posture. No constraint, gravity override or object drive.
    q=np.array([-.11749618,.23326475,.26507071,-1.99043117,-.07577869,2.21444638,-.59905462,.002,.002],np.float32)
    env=make('P10',obs_mode='none',render_backend='none')
    try:
        env.reset(seed=0);e=env.unwrapped;initial=e.snapshot()
        e.agent.reset(q)
        tcp=e.agent.tcp.pose.p[0].cpu().numpy()
        assert np.linalg.norm(tcp-[.18,.03,1.087])<.001, 'Fixture robot geometry changed'
        obj=e.objects['washer']
        obj.set_pose(sapien.Pose([.1605,.03,1.087],quaternion([np.pi/2,0,0])))
        obj.set_linear_velocity([0,0,0]);obj.set_angular_velocity([0,0,0])
        action=e.hold_action();action[0,:7]=torch.as_tensor(q[:7]);action[0,-1]=-.7
        for _ in range(100):env.step(action)
        goal=e.snapshot();o=goal['objects']['washer'];r=e.report
        assert not e.freeze_dynamics and r['success'] and r['dwell']>=20 and not r['violations'],r
        assert o['robot_force']>.03 and np.linalg.norm(o['v'])<.025 and np.linalg.norm(o['w'])<.15
        output.mkdir(parents=True,exist_ok=True)
        for name,state in [('initial',initial),('goal_fixture',goal)]:
            (output/(name+'_state.json')).write_text(json.dumps(state)+'\n')
        result=dict(code='P10',physics_variant=0,passed=True,goal_passed=True,initial_passed=not e.oracle.assess(initial)['success'],
            platform=platform.platform(),physics_steps=e.physics_steps,
            contact_force_n=o['robot_force'],linear_speed_m_s=float(np.linalg.norm(o['v'])),
            angular_speed_rad_s=float(np.linalg.norm(o['w'])),stable_control_intervals=r['dwell'],
            scope='Private initialized physical hold fixture; no solution trajectory; normal gravity and contacts',
            full_environment_qualified=False,goal=r)
        (output/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
        return result
    finally:env.close()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--task',action='append',required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    from agentbench_maniskill import specification
    from agentbench_maniskill.runtime import validate
    rows=[]
    for code in a.task:
        meta,_=specification(code)
        key=f"{meta['task_id']:02}"
        destination=a.output/meta['suite']/key
        try:
            result=held_washer(destination) if code=='P10' else validate(code,0,destination)
        except Exception as exc:
            result=dict(code=code,passed=False,error=repr(exc))
        rows.append(result);print(code,result['passed'],result.get('error',''),flush=True)
    a.output.mkdir(parents=True,exist_ok=True)
    (a.output/'summary.json').write_text(json.dumps(dict(passed=all(r['passed'] for r in rows),rows=rows),indent=2)+'\n')
    return int(not all(r['passed'] for r in rows))


if __name__=='__main__':raise SystemExit(main())
