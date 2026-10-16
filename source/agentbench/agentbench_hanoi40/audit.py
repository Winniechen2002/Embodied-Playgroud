"""Native visible-geometry audit including all added supports and obstacles."""
import numpy as np
from pxr import Usd, UsdGeom, UsdPhysics
from .isaac_cfg import NAMES
from agentbench.tasks.manager_based.table_top_manipulation.config.hanoi.isaac_evaluator import _primitive_points, pose_matrix
from agentbench.tasks.manager_based.table_top_manipulation.config.hanoi.visible_shells import ConvexShell, VisibleShellAudit, FIXED_INSTALLATION_EXCLUSIONS
from agentbench.tasks.manager_based.table_top_manipulation.config.hanoi.scene_fingerprint import SceneFingerprintCache


class Audit:
    def __init__(self,env):
        self.env=env; self.stage=env.scene.stage; self.root='/World/envs/env_0'
        self.fixed_robot_owner='robot/'+getattr(env.cfg,'hanoi40_fixed_robot_body','panda_link0')
        robot=env.scene['robot']; self.dynamic={}; self.static={}; self.paths={}; self.coverage=[]
        for idx,name in enumerate(robot.body_names):
            prims=[p for p in Usd.PrimRange(self.stage.GetPrimAtPath(self.root+'/Robot'),Usd.TraverseInstanceProxies()) if p.GetName()==name and p.HasAPI(UsdPhysics.RigidBodyAPI)]
            if len(prims)!=1: raise ValueError('Robot mapping: '+name)
            path=str(prims[0].GetPath()); owner='robot/'+name
            self.paths[path]=owner; self.dynamic[owner]=('robot',idx)
        for name in NAMES:
            owner='ring_'+name; path=env.scene[owner].root_physx_view.prim_paths[0]
            self.paths[path]=owner; self.dynamic[owner]=(owner,None)
        for prim in self.stage.GetPrimAtPath(self.root).GetChildren():
            path=str(prim.GetPath())
            if path in self.paths or prim.GetName()=='Robot': continue
            # Static roots are not permitted to hide unsupported visible pieces.
            owner={'Table':'table','HanoiBase':'hanoi_base'}.get(prim.GetName(),prim.GetName())
            self.paths[path]=owner; self.static[owner]=path
        cache=UsdGeom.XformCache(); shells=[]
        for prim in Usd.PrimRange(self.stage.GetPrimAtPath(self.root),Usd.TraverseInstanceProxies()):
            if not prim.IsA(UsdGeom.Gprim): continue
            image=UsdGeom.Imageable(prim)
            if image.ComputeVisibility()==UsdGeom.Tokens.invisible or image.ComputePurpose() not in (UsdGeom.Tokens.default_,UsdGeom.Tokens.render): continue
            parent=prim
            while parent and str(parent.GetPath()) not in self.paths: parent=parent.GetParent()
            if not parent: raise ValueError('Unmapped geometry '+str(prim.GetPath()))
            owner=self.paths[str(parent.GetPath())]
            rel=np.linalg.inv(np.asarray(cache.GetLocalToWorldTransform(parent)).T)@np.asarray(cache.GetLocalToWorldTransform(prim)).T
            for index,vertices in enumerate(_primitive_points(prim)):
                pts=vertices@rel[:3,:3].T+rel[:3,3]; name=str(prim.GetPath())+f'#{index}'
                if len(pts)<4 or np.linalg.matrix_rank(pts-pts.mean(0),tol=1e-10)<3:
                    self.coverage.append(dict(name=name,owner=owner,status='zero_volume')); continue
                shells.append(ConvexShell.from_points(owner,name,pts)); self.coverage.append(dict(name=name,owner=owner,status='covered'))
        required=set(self.dynamic)|set(self.static)
        # Empty transform/sensor roots have no visible collision role.
        self.static={k:v for k,v in self.static.items() if k in {s.owner for s in shells}}
        missing=set(self.dynamic)-{s.owner for s in shells}
        # The original Sharpa asset has five geometry-free fingertip frames.
        # Actual elastomer pads are separate rigid bodies and MUST be covered.
        virtual_tips={f'robot/right_{finger}_fingertip' for finger in ('thumb','index','middle','ring','pinky')} if getattr(env.cfg,'hanoi40_robot','franka') in ('sharpa','sharpa_no_arm') else set()
        if getattr(env.cfg,'hanoi40_robot','franka')=='sharpa_no_arm':
            from .sharpa_no_arm import VIRTUAL_BODY_NAMES
            virtual_tips.update('robot/'+name for name in VIRTUAL_BODY_NAMES)
        if missing-virtual_tips: raise ValueError('Incomplete dynamic shell coverage: '+repr(sorted(missing-virtual_tips)))
        empty_frames=[{'owner':owner,'path':next(path for path,value in self.paths.items() if value==owner),
                       'reason':'geometry-free coordinate frame; physical hand meshes separately covered'} for owner in sorted(missing)]
        exclusions=() if getattr(env.cfg,'hanoi40_robot','franka')=='sharpa_no_arm' else FIXED_INSTALLATION_EXCLUSIONS
        self.shells=VisibleShellAudit(shells,exclusions)
        self.manifest=dict(coverage=self.coverage,covered_pairs=len(self.shells.pairs),exclusions=exclusions,geometry_free_frames=empty_frames)
        cache_type=SceneFingerprintCache
        if getattr(env.cfg,'hanoi40_robot','franka') in ('sharpa','sharpa_no_arm'):
            from .fingerprint import cache_class
            cache_type=cache_class()
        self.cache=cache_type(self.stage,self.prims,self.include_attribute)
        self.initial_fingerprint=None

    def prims(self):
        yield from Usd.PrimRange(self.stage.GetPrimAtPath(self.root),Usd.TraverseInstanceProxies())
        for prim in self.stage.Traverse():
            if prim.IsA(UsdPhysics.Scene): yield prim

    def include_attribute(self,path,name):
        dynamic=self.paths.get(path) in self.dynamic and self.paths.get(path)!=self.fixed_robot_owner
        if name.startswith('state:') or (name.startswith('drive:') and name.endswith((':targetPosition',':targetVelocity'))): return False
        return not (dynamic and (name in ('xformOp:translate','xformOp:orient','physics:velocity','physics:angularVelocity') or name.startswith('xformOp:rotate')))

    def snapshot(self):
        transforms={}; positions={}; robot=self.env.scene['robot']
        rp=robot.data.body_link_pos_w[0].detach().cpu().numpy(); rq=robot.data.body_link_quat_w[0].detach().cpu().numpy()
        for owner,(asset,idx) in self.dynamic.items():
            if asset=='robot': p,q=rp[idx],rq[idx]
            else:
                data=self.env.scene[asset].data; p=data.root_link_pos_w[0].detach().cpu().numpy(); q=data.root_link_quat_w[0].detach().cpu().numpy(); positions[asset]=p.tolist()
            transforms[owner]=pose_matrix(p,q)
        cache=UsdGeom.XformCache()
        for owner,path in self.static.items():
            if owner in ('table','hanoi_base'):
                data=self.env.scene[owner].data
                transforms[owner]=pose_matrix(data.root_link_pos_w[0].detach().cpu().numpy(),data.root_link_quat_w[0].detach().cpu().numpy())
            else: transforms[owner]=np.asarray(cache.GetLocalToWorldTransform(self.stage.GetPrimAtPath(path))).T
        fixed={k:transforms[k].tolist() for k in (*self.static,self.fixed_robot_owner)}
        fingerprint=self.cache.fingerprint(repr(self.env.cfg),self.manifest,fixed)
        if self.initial_fingerprint is None: self.initial_fingerprint=fingerprint
        if fingerprint!=self.initial_fingerprint: raise RuntimeError('Environment fingerprint changed')
        self.last_transforms=transforms
        return [positions['ring_'+n] for n in NAMES],self.shells.measure(transforms)
