"""Two physical Pandas and a handwheel rigidly coupled to launcher elevation."""
from copy import deepcopy
import xml.etree.ElementTree as ET
import numpy as np
from .scene import make_scene, add, vec, LAUNCH_ORIGIN


def make_dual_scene(level, mode, rng, timestep, *, position_randomization='off', yaw_enabled=False):
    from .positions import sample_positions, apply_positions
    positions = sample_positions(rng, position_randomization, 1)
    xml, spec = make_scene(level, mode, rng, timestep)
    root = ET.fromstring(xml)
    world = root.find('worldbody')

    def prefixed(element):
        out = deepcopy(element)
        for node in out.iter():
            for key in ('name', 'joint', 'joint1', 'joint2', 'body1', 'body2', 'tendon'):
                if key in node.attrib:
                    node.set(key, 'aim_' + node.get(key))
        return out

    robot = prefixed(world.find("body[@name='link0']"))
    robot.set('pos', '.15 .60 0')
    world.append(robot)
    for section in ('tendon', 'actuator', 'contact'):
        for element in list(root.find(section)):
            root.find(section).append(prefixed(element))
    # Firmer position servo on the wheel gripper; the existing 100 N limit remains.
    grip = root.find("actuator/general[@name='aim_actuator8']")
    grip.set('gainprm', '.04705882353 0 0')
    grip.set('biasprm', '0 -300 -20')
    # Only duplicate the Panda finger coupling, not the launcher latch.
    finger_coupling = root.find('equality').find('joint')
    root.find('equality').append(prefixed(finger_coupling))

    pivot = add(world, 'body', name='elevation', pos=vec(LAUNCH_ORIGIN))
    # Positive angle increases elevation from the single-arm 30-degree datum.
    add(pivot, 'joint', name='elevation_hinge', type='hinge', axis='0 -1 0',
        range=vec(np.deg2rad([-15, 25])), damping='.05', frictionloss='.08')
    add(pivot, 'inertial', pos='0 0 0', mass='.15', diaginertia='.003 .004 .003')
    carriage = world.find("body[@name='carriage']")
    world.remove(carriage)
    carriage.set('pos', '0 0 0')
    pivot.append(carriage)
    # Low loading lip retains a rolling marble; an upward shot clears it.
    add(carriage, 'geom', name='cup_lip', type='box', pos='.041 0 .007',
        size='.003 .035 .007', rgba='.2 .3 .42 1')
    # Move the existing rails into the rotating assembly, keeping their reset pose.
    for geom in list(world.findall('geom')):
        if geom.get('name','').startswith('launcher_rail'):
            endpoints = np.fromstring(geom.get('fromto'), sep=' ').reshape(2, 3)
            geom.set('fromto', vec((endpoints - LAUNCH_ORIGIN).ravel()))
            world.remove(geom)
            pivot.append(geom)
    add(world, 'geom', name='axle_stand', type='box', pos='.55 .115 .15',
        size='.025 .025 .15', rgba='.18 .28 .38 1')
    add(pivot, 'geom', name='wheel_axle', type='capsule', fromto='0 .075 0 0 .19 0',
        size='.012', rgba='.25 .35 .45 1')
    # A vertical handwheel: segmented collision rim and four spokes.
    for i in range(24):
        a, b = 2*np.pi*np.array([i, i+1])/24
        add(pivot, 'geom', name=f'wheel_rim{i}', type='capsule',
            fromto=vec([.10*np.sin(a), .19, .10*np.cos(a),
                        .10*np.sin(b), .19, .10*np.cos(b)]),
            size='.008', rgba='.12 .60 .80 1')
    for i in range(4):
        a = i*np.pi/2
        add(pivot, 'geom', type='capsule',
            fromto=vec([0, .19, 0, .10*np.sin(a), .19, .10*np.cos(a)]),
            size='.005', rgba='.20 .35 .45 1')
    add(pivot, 'geom', name='wheel_crank', type='capsule',
        fromto='0 .19 .10 0 .27 .105', size='.006', rgba='.96 .57 .13 1')
    add(pivot, 'geom', name='wheel_handle', type='box', pos='0 .27 .13',
        size='.015 .019 .020', friction='1.5 .01 .001', rgba='.96 .57 .13 1')
    add(pivot, 'site', name='wheel_grasp', pos='0 .27 .13', rgba='0 0 0 0')
    spec['dual_arm'] = True
    if yaw_enabled:
        # The entire elevation assembly slews around the pillar. Both joints
        # remain passive: only hand contact can turn or brace this turret.
        turntable = add(world, 'body', name='yaw_turntable', pos=vec(LAUNCH_ORIGIN))
        add(turntable, 'joint', name='yaw_hinge', type='hinge', axis='0 0 1',
            range=vec(np.deg2rad([-25, 25])), damping='.10', frictionloss='.08')
        add(turntable, 'inertial', pos='0 0 -.015', mass='.15',
            diaginertia='.003 .003 .004')
        add(turntable, 'geom', name='yaw_bearing', type='cylinder',
            pos='0 0 -.076', size='.014 .012', rgba='.12 .60 .80 1')
        add(world, 'geom', name='launcher_yaw_column', type='cylinder',
            pos=vec(LAUNCH_ORIGIN+[0,0,-.20]), size='.013 .11', rgba='.18 .28 .38 1')
        world.remove(pivot)
        pivot.set('pos', '0 0 0')
        turntable.append(pivot)
        stand = world.find("geom[@name='axle_stand']")
        world.remove(stand)
        # A slewing yoke clears the fixed plinth; the old floor-reaching stand
        # would intersect that plinth once made dynamic.
        stand.set('pos', '0 .115 -.13')
        stand.set('size', '.025 .025 .11')
        turntable.append(stand)
        # The power arm turns this separate, horizontal handwheel. Its brake
        # release grip belongs only to yaw; the other arm owns the pitch grip.
        for i in range(24):
            a,b=2*np.pi*np.array([i,i+1])/24
            add(turntable,'geom',name=f'yaw_wheel_rim{i}',type='capsule',
                fromto=vec([.21*np.cos(a),.21*np.sin(a),-.19,
                            .21*np.cos(b),.21*np.sin(b),-.19]),
                size='.006',rgba='.88 .38 .12 1')
        for i in range(4):
            a=i*np.pi/2
            add(turntable,'geom',name=f'yaw_wheel_spoke{i}',type='capsule',
                fromto=vec([.09*np.cos(a),.09*np.sin(a),-.19,.21*np.cos(a),.21*np.sin(a),-.19]),
                size='.004',rgba='.40 .28 .19 1')
        add(turntable,'geom',name='yaw_crank',type='capsule',
            fromto='0 -.21 -.19 0 -.24 .065',size='.006',rgba='.96 .57 .13 1')
        add(turntable,'geom',name='yaw_handle',type='box',pos='0 -.24 .09',
            size='.015 .019 .020',friction='1.5 .01 .001',rgba='.96 .57 .13 1')
        add(turntable,'site',name='yaw_grasp',pos='0 -.24 .09',rgba='0 0 0 0')
        for joint,brake in [('yaw_hinge','yaw_brake'),('elevation_hinge','elevation_brake')]:
            add(root.find('equality'),'joint',name=brake,joint1=joint,
                polycoef='0 0 0 0 0',active='true',solref='.002 1',solimp='.99 .999 .001')
        spec['yaw_enabled'] = True
        spec['aiming_mechanism'] = 'separate_yaw_and_elevation_wheels_with_contact_released_brakes'
    apply_positions(root,spec,positions,mode)
    return ET.tostring(root, encoding='unicode'), spec
