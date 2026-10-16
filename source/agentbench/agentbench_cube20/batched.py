"""Seven isolated native instances per task, with USD randomization before physics."""
import math
import numpy as np
import torch
from pxr import Gf, UsdPhysics, UsdLux, Sdf
import isaaclab.sim as sim_utils
from isaaclab.managers import EventTermCfg
from .native import Cube20Env,build_cfg
from .catalog import sample
from .geometry import quaternion

def pose_records(cfg):
    result=[]
    for params in cfg.cube20_batch_parameters:
        a=math.radians(params['yaw_deg']);c=math.cos(a);s=math.sin(a)
        yaw=np.array([[c,-s,0],[s,c,0],[0,0,1.]])
        root=np.array([params['x'],params['y'],.6505])
        # Local scramble quaternions are independent of the world yaw.
        from scipy.spatial.transform import Rotation
        rs=Rotation.from_quat(np.array(cfg.cube20_local_quaternions)[:,[1,2,3,0]]).as_matrix()
        result.append(dict(root=[*root,*quaternion(yaw)],rest=[params['x'],params['y'],.6125,*quaternion(yaw)],
             cubies=[[*list(root+yaw@np.array(p)),*quaternion(yaw@r)] for p,r in zip(cfg.cube20_local_positions,rs)]))
    return result

def prestartup(env,env_ids=None):
    """Authored before sim.reset; there are no scored-time object writes."""
    stage=sim_utils.get_current_stage()
    for i,(params,poses) in enumerate(zip(env.cfg.cube20_batch_parameters,pose_records(env.cfg))):
        prefix=f'/World/envs/env_{i}'
        def set_pose(path,values):
            prim=stage.GetPrimAtPath(path)
            prim.GetAttribute('xformOp:translate').Set(Gf.Vec3d(*values[:3]))
            q=values[3:];attr=prim.GetAttribute('xformOp:orient');qtype=Gf.Quatf if isinstance(attr.Get(),Gf.Quatf) else Gf.Quatd
            attr.Set(qtype(q[0],Gf.Vec3f(*q[1:]) if qtype==Gf.Quatf else Gf.Vec3d(*q[1:])))
            return prim
        for name,mass in (('Core',.008),('Carrier',.002)):
            prim=set_pose(prefix+'/PocketCube/'+name,poses['root'])
            UsdPhysics.MassAPI(prim).GetMassAttr().Set(mass*params['mass_scale'])
        set_pose(prefix+'/CubeRest',poses['rest'])
        from .catalog import rules
        for j,name in enumerate(rules.CORNER_NAMES):
            if i:
                # The original scan spawner authors its controlled mass,
                # material and collider overrides after cloning. Copy that
                # fully authored source spec before per-instance overrides.
                source=f'/World/envs/env_0/PocketCube/Cubies/Cubie_{name.lower()}'
                target=prefix+'/PocketCube/Cubies/Cubie_'+name.lower()
                if not Sdf.CopySpec(stage.GetRootLayer(),source,stage.GetRootLayer(),target):
                    raise RuntimeError('Could not clone controlled cubie spec')
            prim=set_pose(prefix+'/PocketCube/Cubies/Cubie_'+name.lower(),poses['cubies'][j])
            mass=UsdPhysics.MassAPI(prim);mass.GetMassAttr().Set(.0075*params['mass_scale'])
            mass.GetDiagonalInertiaAttr().Set(Gf.Vec3f(*([7.320500117202755e-7*params['mass_scale']]*3)))
            material=UsdPhysics.MaterialAPI(stage.GetPrimAtPath(str(prim.GetPath())+'/PhysicsMaterial'))
            material.GetStaticFrictionAttr().Set(1.4*params['friction_scale'])
            material.GetDynamicFrictionAttr().Set(1.1*params['friction_scale'])
        # Per-instance light linking prevents light randomization leaking across instances.
        light=UsdLux.DomeLight.Define(stage,f'/World/Cube20Light_{i}')
        light.CreateIntensityAttr(params['light']);light.CreateColorAttr(Gf.Vec3f(.88,.91,1.))
        links=UsdLux.LightAPI(light.GetPrim()).GetLightLinkCollectionAPI();links.CreateIncludeRootAttr().Set(False)
        links.CreateIncludesRel().SetTargets([Sdf.Path(prefix)])
    stage.GetPrimAtPath('/World/skyLight').GetAttribute('inputs:intensity').Set(0.)

class BatchCube20Env(Cube20Env):
    def load_managers(self):
        # Config-level defaults are shared; replace only reset defaults to match
        # the already-authored per-instance USD poses before any scored reset.
        poses=pose_records(self.cfg)
        for name,key in (('pocket_cube','root'),('pocket_cube_carrier','root'),('cube_rest','rest')):
            self.scene[name].data.default_root_state[:,:7]=torch.tensor([p[key] for p in poses],device=self.device)
        self.scene['pocket_cubies'].data.default_object_state[:,:,:7]=torch.tensor([p['cubies'] for p in poses],device=self.device)
        super().load_managers()

def make_batch(task_id,device='cuda:0',robot='aloha'):
    cases=[('nominal',0)]+[(s,n) for s in ('train','heldout') for n in range(3)]
    cfg=build_cfg(task_id,0,'nominal',device,robot)
    cfg.scene.num_envs=len(cases);cfg.scene.env_spacing=3.
    cfg.cube20_batch_parameters=[sample(task_id,n,s) for s,n in cases]
    cfg.events.cube20_batch_prestartup=EventTermCfg(func=prestartup,mode='prestartup')
    return BatchCube20Env(cfg),cases
