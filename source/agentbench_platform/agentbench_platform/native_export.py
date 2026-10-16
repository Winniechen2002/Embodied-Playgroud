"""Public legal robot kinematics and separate maintainer goal still export."""
import base64
import hashlib
import json
from pathlib import Path


def export_robot_models(env,directory,*,robots=None):
    """Joint frames and axes suffice for FK/IK; task object assets are excluded."""
    from pxr import Usd,UsdGeom,UsdPhysics
    stage=env.sim.stage
    output={}
    robots = robots if robots is not None else {
        side:('/World/envs/env_0/'+side.title()+'Panda',side+'_robot') for side in ('left','right')}
    for side,(prim_path,scene_name) in robots.items():
        root=stage.GetPrimAtPath(prim_path)
        if not root.IsValid():raise RuntimeError('Robot root missing')
        rows=[]
        for prim in Usd.PrimRange(root):
            if not prim.IsA(UsdPhysics.Joint):continue
            joint=UsdPhysics.Joint(prim)
            row=dict(name=prim.GetName(),joint_type=prim.GetTypeName(),
                limit_units='degrees' if prim.IsA(UsdPhysics.RevoluteJoint) else 'm' if prim.IsA(UsdPhysics.PrismaticJoint) else None,body0=[str(p).split('/')[-1] for p in joint.GetBody0Rel().GetTargets()],
                body1=[str(p).split('/')[-1] for p in joint.GetBody1Rel().GetTargets()],
                local_pos0=list(joint.GetLocalPos0Attr().Get()),local_pos1=list(joint.GetLocalPos1Attr().Get()))
            for key,attr in (('local_quat0',joint.GetLocalRot0Attr()),('local_quat1',joint.GetLocalRot1Attr())):
                q=attr.Get();row[key]=[float(q.GetReal()),*map(float,q.GetImaginary())]
            for key in ('physics:axis','physics:lowerLimit','physics:upperLimit'):
                value=prim.GetAttribute(key).Get()
                if value is not None:row[key.split(':')[-1]]=value
            rows.append(row)
        if not rows:raise RuntimeError('Robot joint model missing')
        body_names = list(env.scene[scene_name].body_names)
        is_sharpa = 'right_hand_C_MC' in body_names
        if is_sharpa:
            output[side] = dict(
                model='Floating Sharpa Wave right hand', length_units='m',
                revolute_limit_units='degrees', action_revolute_units='radians', quaternion_order='wxyz',
                joints=rows, root_link=body_names[0],
                palm_body='right_hand_C_MC',
                fingertip_bodies=[
                    'right_thumb_elastomer', 'right_index_elastomer',
                    'right_middle_elastomer', 'right_ring_elastomer',
                    'right_pinky_elastomer',
                ],
                tool_frames=dict(
                    palm=dict(parent='right_hand_C_MC', position=[0., 0., 0.],
                              quaternion=[1., 0., 0., 0.]),
                ),
                world_from_base=[list(r) for r in UsdGeom.Xformable(root).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).GetTranspose()],
            )
        else:
            output[side]=dict(model='Franka Panda',length_units='m',revolute_limit_units='degrees',quaternion_order='wxyz',
                joints=rows,root_link=body_names[0],
                tool_frames=dict(tcp=dict(parent='panda_hand',position=[0.,0.,.1034],quaternion=[1.,0.,0.,0.])),
                world_from_base=[list(r) for r in UsdGeom.Xformable(root).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).GetTranspose()])
    path=Path(directory)/'robot_model.json';path.write_text(json.dumps(output,indent=2)+'\n')
    return path


def export_goal_stills(directory,cameras,resources,mode):
    """A separate reset-only goal scene; never move pieces in an active attempt."""
    from PIL import Image
    import numpy as np
    captures=cameras.capture(tuple(cameras.description()),0)
    manifest=dict(mode=mode,kind='goal_reference_reset_only',images={})
    for name,capture in captures.items():
        data=base64.b64decode(resources.get(capture['rgb_resource_id'],'rgb')['data_base64'])
        path=Path(directory)/(name+'.png')
        Image.fromarray(np.frombuffer(data,np.uint8).reshape(480,640,3)).save(path)
        manifest['images'][name]=dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),calibration=capture['calibration'])
    (Path(directory)/'goal_reference.json').write_text(json.dumps(manifest,indent=2)+'\n')
