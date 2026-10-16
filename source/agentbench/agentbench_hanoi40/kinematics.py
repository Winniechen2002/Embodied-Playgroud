"""Panda FK from the repository's published rigid kinematic chain (no simulation)."""
import math
import numpy as np
from scipy.spatial.transform import Rotation
from scipy.optimize import least_squares

POS=((0,0,.333),(0,0,0),(0,-.316,0),(.0825,0,0),(-.0825,.384,0),(0,0,0),(.088,0,0))
RX=(0,-math.pi/2,math.pi/2,math.pi/2,-math.pi/2,math.pi/2,math.pi/2)
FIXED=[Rotation.from_euler('x',a).as_matrix() for a in RX]


def fk(q, jacobian=False):
    rot=np.eye(3); pos=np.zeros(3); origins=[]; axes=[]
    for xyz,rx,angle in zip(POS,FIXED,q):
        pos+=rot@np.array(xyz); rot=rot@rx
        origins.append(pos.copy()); axes.append(rot[:,2].copy())
        c=math.cos(angle); s=math.sin(angle)
        rot=rot@np.array([[c,-s,0.],[s,c,0.],[0.,0.,1.]])
    pos+=rot@np.array([0.,0.,.107]); rot=rot@Rotation.from_euler('z',-math.pi/4).as_matrix()
    if jacobian:
        axes=np.array(axes).T; origins=np.array(origins)
        j=np.vstack((np.cross(axes.T,pos-origins).T,axes))
        return pos,rot,j
    return pos,rot


def residual_jacobian(q, position, rotation):
    p,r,j=fk(q,True)
    phi=Rotation.from_matrix(rotation@r.T).as_rotvec(); theta=np.linalg.norm(phi)
    x,y,z=phi; skew=np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]])
    a=1/12 if theta<1e-5 else (1-.5*theta/math.tan(.5*theta))/(theta*theta)
    right_inverse=np.eye(3)+.5*skew+a*(skew@skew)
    return np.r_[p-position,.4*phi],np.vstack((j[:3],-.4*right_inverse@j[3:]))


def ik(position,rotation,seed,bounds):
    def residual(q):
        p,r=fk(q)
        return np.r_[p-position, .4*Rotation.from_matrix(rotation@r.T).as_rotvec()]
    res=least_squares(residual,np.clip(seed,bounds[0]+1e-6,bounds[1]-1e-6),jac=lambda q:residual_jacobian(q,position,rotation)[1],bounds=bounds,max_nfev=160,xtol=1e-9,ftol=1e-9,gtol=1e-9)
    if np.linalg.norm(residual(res.x))>.005:
        candidates=[res]
        rng=np.random.default_rng(47)
        alternatives=[[0.,-.5,0.,-2.,0.,1.5,0.],[-.6,.4,0.,-2.,0.,2.,0.],[.6,.4,0.,-2.,0.,2.,0.]]
        alternatives.extend(rng.uniform(bounds[0],bounds[1],size=(8,7)))
        for other in alternatives:
            candidates.append(least_squares(residual,np.clip(other,bounds[0]+1e-6,bounds[1]-1e-6),jac=lambda q:residual_jacobian(q,position,rotation)[1],bounds=bounds,max_nfev=160))
        valid=[c for c in candidates if np.linalg.norm(c.fun)<.003]
        res=min(valid,key=lambda r:np.linalg.norm(r.x-seed)) if valid else min(candidates,key=lambda r:np.linalg.norm(r.fun))
    if np.linalg.norm(res.fun)>.01: raise RuntimeError('Kinematic goal unresolved')
    return res.x


def link_poses(q, fingers, base_position, base_rotation):
    """All Panda rigid-link transforms in world coordinates, for planning only."""
    def transform(p,r):
        t=np.eye(4);t[:3,:3]=r;t[:3,3]=p;return t
    r=np.asarray(base_rotation).copy();p=np.asarray(base_position).copy()
    result={'robot/panda_link0':transform(p,r)}
    for i,(xyz,rx,angle) in enumerate(zip(POS,FIXED,q)):
        p=p+r@np.array(xyz);c=math.cos(angle);s=math.sin(angle)
        r=r@rx@np.array([[c,-s,0.],[s,c,0.],[0.,0.,1.]])
        result[f'robot/panda_link{i+1}']=transform(p,r)
    p=p+r@np.array([0.,0.,.107]);r=r@Rotation.from_euler('z',-math.pi/4).as_matrix()
    result['robot/panda_hand']=transform(p,r)
    result['robot/panda_leftfinger']=transform(p+r@np.array([0.,fingers[0],.0584]),r)
    result['robot/panda_rightfinger']=transform(p+r@np.array([0.,-fingers[1],.0584]),r)
    return result
