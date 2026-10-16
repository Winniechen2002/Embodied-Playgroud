"""Collision-bearing native SAPIEN joints; no animation or goal-following controller."""
import numpy as np
import sapien
from .shapes import add_shape
from .asset_loader import axis_quat, quaternion


def build(e, spec):
    ab = e.scene.create_articulation_builder()
    links = {}
    for index, item in enumerate(spec['links']):
        parent = links.get(item.get('parent'))
        link = ab.create_link_builder(parent)
        link.set_name(spec['name']+'__'+item['name'])
        links[item['name']] = link
        for s in item.get('shapes', []): add_shape(e, link, s)
        if parent is not None:
            joint = item['joint']
            link.set_joint_name(joint['name'])
            ax = axis_quat(joint.get('axis', [0, 0, 1]))
            link.set_joint_properties(joint['type'], [joint['limits']],
                                      sapien.Pose(joint.get('origin', [0,0,0]), ax),
                                      sapien.Pose(q=ax), friction=joint.get('friction', .15),
                                      damping=joint.get('damping', .05))
        if 'mass' in item:
            link.set_mass_and_inertia(item['mass'], sapien.Pose(item.get('com',[0,0,0])), item.get('inertia', [.001]*3))
    ab.initial_pose = sapien.Pose(spec['position'], quaternion(spec.get('rpy', [0,0,0])))
    art = ab.build(name=spec['name'], fix_root_link=not spec.get('free_root', False))
    e.builders.append(ab)
    e.register_art(spec['name'], art, None, spec)
    return art
