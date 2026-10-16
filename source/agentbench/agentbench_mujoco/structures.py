"""Rigid construction pieces: physical materials and primitive/convex shapes.

The material parameters are authored benchmark values, not measurements of
real wood/glass/stone. Glass stays a rigid body: no implicit fracture/removal.
"""
import xml.etree.ElementTree as ET
import numpy as np
from .appearance import block_detail, fixed_detail

MATERIALS = {
    'wood': dict(rgba='.70 .46 .24 1', friction='.55 .005 .0001', solref='.006 1'),
    'glass': dict(rgba='.48 .86 .96 .80', friction='.24 .003 .0001', solref='.004 .8'),
    'stone': dict(rgba='.55 .61 .67 1', friction='.72 .008 .0002', solref='.008 1'),
    'rubber': dict(rgba='.85 .40 .25 1', friction='1.1 .012 .0005', solref='.01 .45'),
}


def _vec(values):
    return ' '.join(str(float(v)) for v in values)


def build_structure(root, world, spec):
    """size always stores LOCAL bounding half-extents, including compound arches."""
    s=spec;name=s['name'];shape=s.get('shape','box')
    mat=s.get('material','stone' if s['fixed'] else 'wood')
    if mat not in MATERIALS:raise ValueError(f'Unknown material: {mat}')
    body=ET.SubElement(world,'body',name=name,pos=_vec(s['pos']))
    # Arch legs lie on local +/-X. A 90-degree yaw makes their opening face
    # the launcher along world X. Keep the legacy XML identical for yaw=0.
    yaw = s.get('yaw', 0.)
    if not np.isfinite(yaw):raise ValueError('Structure yaw must be finite')
    if s.get('angle') or yaw:
        body.set('euler',_vec([0,np.deg2rad(s.get('angle',0.)),np.deg2rad(yaw)]))
    if not s['fixed']:ET.SubElement(body,'freejoint',name=name+'_free')
    attrs=dict(MATERIALS[mat],material=mat+'_mat')
    attrs['rgba']='1 1 1 1'
    if s.get('condim') is not None:
        if s['condim'] not in (1,3,4,6):raise ValueError('Contact dimension must be 1, 3, 4 or 6')
        attrs['condim']=str(s['condim'])
    hx,hy,hz=s['size']
    if shape=='sphere' and not np.allclose([hx,hy,hz],hx):
        raise ValueError('Sphere half-extents must all equal its radius')
    if shape=='cylinder' and not np.isclose(hx,hy):
        raise ValueError('Cylinder x/y half-extents must equal its radius')
    def part(suffix,typ,size,pos=(0,0,0),mass=None,**kw):
        return ET.SubElement(body,'geom',name=name+suffix,type=typ,size=_vec(size),
              pos=_vec(pos),mass=str(s['mass'] if mass is None else mass),**attrs,**kw)
    if shape=='box':
        part('', 'box',s['size']);block_detail(body,s['size'],mat=='stone')
    elif shape=='sphere':
        part('','sphere',[hx])
    elif shape=='cylinder':
        part('','cylinder',[hx,hz])
    elif shape in ('wedge','gable'):
        # Six vertices define a triangular prism, a convex collision mesh.
        if shape=='wedge':xz=[(-hx,-hz),(hx,-hz),(-hx,hz)]
        else:xz=[(-hx,-hz),(hx,-hz),(0,hz)]
        vertices=[[x,y,z] for y in (-hy,hy) for x,z in xz]
        ET.SubElement(root.find('asset'),'mesh',name=name+'_mesh',vertex=_vec(np.array(vertices).ravel()))
        part('','mesh',[1,1,1],mesh=name+'_mesh')
    elif shape=='arch':
        t=min(.025,hx/4,hz/4)
        volumes=np.array([(2*hx)*(2*hy)*(2*t),2*t*2*hy*(2*hz-2*t),2*t*2*hy*(2*hz-2*t)])
        masses=s['mass']*volumes/volumes.sum()
        part('','box',[hx,hy,t],[0,0,hz-t],masses[0])
        for i,sign in enumerate((-1,1)):
            part(f'_leg{i}','box',[t,hy,hz-t],[sign*(hx-t),0,-t],masses[i+1])
    else:raise ValueError(f'Unknown structure shape: {shape}')
    if s['fixed']:fixed_detail(body,s['size'])
    s.update(shape=shape,material=mat,angle=s.get('angle',0.))
    return body
