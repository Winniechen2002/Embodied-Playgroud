"""Inference-only NumPy kernels for the pinned GraspNet PointNet++ extension.

Implements its ordered/open-boundary query semantics and fixed FPS start, without
CUDA or gradients. The network and weights remain the official pinned model.
Derived from the documented operations of graspnet-baseline 280c215; its upstream
PointNet++ kernels carry the MIT license (Facebook, Inc. and affiliates).
"""
import numpy as np


def _points(value):
    value=np.asarray(value,dtype=np.float32)
    if value.ndim!=3 or value.shape[2]!=3 or not value.shape[1] or not np.isfinite(value).all():
        raise ValueError('Expected finite batched XYZ')
    return value


def _neighbors(mask,nsample):
    out=np.zeros((len(mask),nsample),dtype=np.int32)
    for i,row in enumerate(mask):
        hits=np.flatnonzero(row)[:nsample]
        if len(hits):out[i].fill(hits[0]);out[i,:len(hits)]=hits
    return out


def _query(new_xyz,xyz,nsample,predicate):
    xyz=_points(xyz);new_xyz=_points(new_xyz)
    if xyz.shape[0]!=new_xyz.shape[0] or type(nsample) is not int or nsample<=0:
        raise ValueError('Invalid query shape/count')
    out=np.zeros((*new_xyz.shape[:2],nsample),dtype=np.int32)
    for b in range(len(xyz)):
        for start in range(0,new_xyz.shape[1],64):
            delta=xyz[b,None,:,:]-new_xyz[b,start:start+64,None,:]
            out[b,start:start+64]=_neighbors(predicate(delta,b,start),nsample)
    return out


def ball_query(new_xyz,xyz,radius,nsample):
    radius=np.float32(radius)
    return _query(new_xyz,xyz,nsample,lambda d,b,s:(d[...,0]**2+d[...,1]**2+d[...,2]**2)<radius*radius)


def cylinder_query(new_xyz,xyz,rot,radius,hmin,hmax,nsample):
    rot=np.asarray(rot,dtype=np.float32).reshape(*np.shape(new_xyz)[:2],3,3)
    radius,hmin,hmax=map(np.float32,(radius,hmin,hmax))
    def predicate(delta,b,start):
        r=rot[b,start:start+len(delta)]
        x,y,z=(sum(delta[...,j]*r[:,None,j,k] for j in range(3)) for k in range(3))
        return (y*y+z*z<radius*radius)&(x>hmin)&(x<hmax)
    return _query(new_xyz,xyz,nsample,predicate)


def furthest_point_sampling(xyz,npoint):
    xyz=_points(xyz)
    if type(npoint) is not int or not 0<npoint<=xyz.shape[1]:raise ValueError('Invalid FPS count')
    out=np.zeros((len(xyz),npoint),dtype=np.int32)
    n=xyz.shape[1];threads=min(512,1<<(n.bit_length()-1))
    # The CUDA reduction breaks equal maxima by thread index, then by the first
    # point visited by that thread, not always by global input index.
    order=np.lexsort((np.arange(n),np.arange(n)%threads))
    for b,points in enumerate(xyz):
        minimum=np.full(n,np.float32(1e10));old=0
        eligible=(points[:,0]**2+points[:,1]**2+points[:,2]**2)>np.float32(1e-3)
        for i in range(1,npoint):
            d=points-points[old];dist=d[:,0]**2+d[:,1]**2+d[:,2]**2
            np.minimum(minimum,dist,out=minimum)
            values=np.where(eligible,minimum,np.float32(-1))
            old=int(order[np.argmax(values[order])]) if eligible.any() else 0
            out[b,i]=old
    return out


def gather_points(features,idx):
    features=np.asarray(features,dtype=np.float32);idx=np.asarray(idx,dtype=np.int64)
    return np.take_along_axis(features,idx[:,None,:],axis=2)


def group_points(features,idx):
    idx=np.asarray(idx,dtype=np.int64)
    return gather_points(features,idx.reshape(len(idx),-1)).reshape(len(idx),np.shape(features)[1],*idx.shape[1:])


def three_nn(unknown,known):
    unknown=_points(unknown);known=_points(known)
    if len(unknown)!=len(known) or known.shape[1]<3:raise ValueError('Three reference neighbors required')
    dist=np.empty((*unknown.shape[:2],3),dtype=np.float32);idx=np.empty(dist.shape,dtype=np.int32)
    for b in range(len(known)):
        for start in range(0,unknown.shape[1],64):
            d=unknown[b,start:start+64,None,:]-known[b,None,:,:]
            squared=d[...,0]**2+d[...,1]**2+d[...,2]**2
            nearest=np.argsort(squared,axis=-1,kind='stable')[:,:3]
            idx[b,start:start+64]=nearest
            dist[b,start:start+64]=np.take_along_axis(squared,nearest,axis=1)
    return dist,idx


def three_interpolate(features,idx,weight):
    v=group_points(features,idx);w=np.asarray(weight,dtype=np.float32)[:,None,:,:]
    return v[...,0]*w[...,0]+v[...,1]*w[...,1]+v[...,2]*w[...,2]


def install_extension():
    """Bind official torch Function wrappers to CPU kernels in this worker only."""
    import sys
    from types import ModuleType
    import torch
    name='pointnet2._ext'
    if name in sys.modules:raise RuntimeError('PointNet extension was already loaded')
    module=ModuleType(name)
    def convert(value):
        if isinstance(value,torch.Tensor):
            if value.device.type!='cpu' or value.requires_grad:raise ValueError('CPU inference tensors only')
            return value.detach().numpy()
        return value
    def wrap(function):
        def execute(*args):
            value=function(*(convert(v) for v in args))
            tensor=lambda array:torch.from_numpy(np.ascontiguousarray(array))
            return tuple(tensor(v) for v in value) if isinstance(value,tuple) else tensor(value)
        return execute
    for function in (ball_query,cylinder_query,furthest_point_sampling,gather_points,group_points,three_nn,three_interpolate):
        setattr(module,function.__name__,wrap(function))
    sys.modules[name]=module
    # Official label_generation imports KNN eagerly although inference never
    # calls it. Reject any accidental training path explicitly, without loading
    # its unrelated CUDA training extension or modifying official source files.
    training=ModuleType('knn_modules')
    def unavailable(*args,**kwargs):raise RuntimeError('Training KNN unavailable in inference-only worker')
    training.knn=unavailable
    if 'knn_modules' in sys.modules:raise RuntimeError('Training extension already loaded')
    sys.modules['knn_modules']=training
