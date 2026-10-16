"""Exact primitive compounds, including open rings and explicit surface normals."""
import numpy as np
import sapien
from .asset_loader import quaternion, rot, axis_quat


def add_shape(e, builder, s):
    p = np.array(s.get('p', [0, 0, 0]), float)
    q = quaternion(s.get('rpy', [0, 0, 0]))
    R = rot(q)
    pose = sapien.Pose(p, q)
    mat = sapien.render.RenderMaterial(base_color=[*s.get('color', [.6, .6, .6]), 1],
                                       roughness=s.get('roughness', .6)) if e.scene.can_render() else None
    collision = s.get('collision', True)
    typ = s['type']
    if typ == 'box':
        half = np.array(s['half'])
        if collision: builder.add_box_collision(half_size=half, pose=pose, material=e.material)
        if mat: builder.add_box_visual(half_size=half, pose=pose, material=mat)
        v = np.array([[x, y, z] for x in [-1, 1] for y in [-1, 1] for z in [-1, 1]]) * half
    elif typ == 'sphere':
        r = s['radius']
        if collision: builder.add_sphere_collision(radius=r, pose=pose, material=e.material)
        if mat: builder.add_sphere_visual(radius=r, pose=pose, material=mat)
        v = np.array([[np.sin(a)*np.cos(b), np.sin(a)*np.sin(b), np.cos(a)]
                      for a in np.linspace(0, np.pi, 17) for b in np.linspace(0, 2*np.pi, 32, endpoint=False)])*r
    elif typ == 'cylinder':
        r, h = s['radius'], s['height']
        cp = pose * sapien.Pose(q=axis_quat([0, 0, 1]))
        if collision: builder.add_cylinder_collision(radius=r, half_length=h/2, pose=cp, material=e.material)
        if mat: builder.add_cylinder_visual(radius=r, half_length=h/2, pose=cp, material=mat)
        v = np.array([[r*np.cos(a), r*np.sin(a), z] for a in np.linspace(0, 2*np.pi, 49)
                      for z in [-h/2, h/2]])
    else:
        raise ValueError(typ)
    return v @ R.T + p
