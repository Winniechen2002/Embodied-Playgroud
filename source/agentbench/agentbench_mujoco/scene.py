"""Standalone Panda marble-launching scenes; no Isaac imports."""
from pathlib import Path
from .appearance import pig, block_detail, workshop, shot_detail
import xml.etree.ElementTree as ET
import numpy as np

ASSETS = Path(__file__).parent / 'assets' / 'panda'
LEVELS = ('direct', 'gate', 'bridge', 'domino')
MODES = ('ground', 'loaded')
HOME = np.array([0., -.4, 0., -2.2, 0., 1.9, .7854])
LAUNCH_ORIGIN = np.array([.55, 0., .32])
LAUNCH_AXIS = np.array([-np.cos(np.pi/6), 0., -np.sin(np.pi/6)])
HANDLE_OFFSET = np.array([-.08, 0., .03])
BALL_OFFSET = np.array([0., 0., .025])


def add(parent, tag, **attrs):
    return ET.SubElement(parent, tag, {k:str(v) for k,v in attrs.items()})


def vec(x):
    return ' '.join(str(float(v)) for v in x)


def make_scene(level, mode, rng, timestep=.001, *, position_randomization='off'):
    if level not in LEVELS or mode not in MODES:
        raise ValueError(f'Unknown scene {level}/{mode}')
    from .positions import sample_positions, apply_positions
    positions = sample_positions(rng, position_randomization, 1)
    root = ET.parse(ASSETS/'panda.xml').getroot()
    root.remove(root.find('keyframe'))
    root.find('compiler').set('meshdir', str((ASSETS/'assets').resolve()))
    root.find('option').attrib.update(timestep=str(timestep), gravity='0 0 -9.81',
                                     iterations='80', tolerance='1e-9', cone='elliptic')
    add(root.find('default'), 'geom', solref='.006 1', solimp='.95 .99 .001', friction='.7 .005 .0001')
    visual = add(root, 'visual')
    add(visual,'global',offwidth='1280',offheight='720')
    add(visual,'quality',shadowsize='4096',offsamples='4')
    asset=root.find('asset')
    add(asset,'texture',name='sky',type='skybox',builtin='gradient',rgb1='.70 .80 .84',rgb2='.92 .94 .91',width='512',height='3072')
    add(asset,'texture',name='floor_tex',type='2d',builtin='flat',rgb1='.54 .61 .61',rgb2='.54 .61 .61',width='512',height='512')
    add(asset,'material',name='floor_mat',texture='floor_tex',texrepeat='1 1',reflectance='0',specular='.05',shininess='.1')
    workshop(root)
    world=root.find('worldbody')
    world.find("body[@name='link0']").set('pos','0 -.45 0')
    hand=world.find(".//body[@name='hand']")
    add(hand,'site',name='grasp',pos='0 0 .1034',size='.005',rgba='0 0 0 0')
    # Rubber pads remain ordinary frictional contact, never a grasp constraint.
    for name in ['left_finger','right_finger']:
        for g in world.find(f".//body[@name='{name}']").findall('geom'):
            if g.get('class','').startswith('fingertip'):
                g.set('friction','1.5 .01 .001')
    add(world,'light',pos='-.5 -3 5',dir='.3 .3 -1',diffuse='.50 .51 .52',specular='.15 .15 .15',directional='true')
    add(world,'light',pos='2 3 4',dir='-.2 -.4 -1',diffuse='.16 .19 .22',castshadow='false')
    add(world,'geom',name='floor',type='plane',size='20 20 .1',material='floor_mat')
    add(world,'geom',name='launcher_foot',type='box',pos='.48 0 .025',size='.19 .12 .025',rgba='.16 .22 .3 1')
    add(world,'geom',name='launcher_pillar',type='box',pos='.59 0 .15',size='.025 .045 .10',rgba='.95 .55 .13 1')
    # Rails are explicit fixed geometry; their top is below the moving tray.
    for y in [-.075,.075]:
        add(world,'geom',name=f'launcher_rail{y}',type='capsule',fromto=vec(np.r_[LAUNCH_ORIGIN[:1]-.20,y,.18])+ ' '+vec([.55,y,.295]),size='.009',rgba='.22 .3 .4 1')
    carriage=add(world,'body',name='carriage',pos=vec(LAUNCH_ORIGIN))
    add(carriage,'joint',name='draw',type='slide',axis=vec(LAUNCH_AXIS),range='0 .19',
        stiffness='25',springref='0',damping='.015',armature='.0001',solreflimit='.002 1')
    add(carriage,'inertial',pos='0 0 0',mass='.015',diaginertia='.00002 .00002 .00002')
    add(carriage,'geom',name='cup_floor',type='box',size='.038 .035 .004',rgba='.2 .3 .42 1',friction='.4 .005 .0001')
    for i,y in enumerate([-.04,.04]):
        add(carriage,'geom',name=f'cup_side{i}',type='box',pos=f'0 {y} .019',size='.035 .005 .023',rgba='.2 .3 .42 1')
    add(carriage,'geom',name='cup_back',type='box',pos='-.038 0 .019',size='.004 .035 .023',rgba='.2 .3 .42 1')
    add(carriage,'geom',name='handle_stem',type='capsule',fromto='-.035 0 .012 -.08 0 .012',size='.006',rgba='.95 .55 .13 1')
    add(carriage,'geom',name='handle',type='box',pos=vec(HANDLE_OFFSET),size='.014 .017 .015',rgba='.95 .55 .13 1',friction='1.5 .01 .001')
    add(carriage,'site',name='handle_site',pos=vec(HANDLE_OFFSET),rgba='0 0 0 0')
    add(carriage,'site',name='load_site',pos=vec(BALL_OFFSET),rgba='0 0 0 0')
    ball_pos=LAUNCH_ORIGIN+BALL_OFFSET if mode=='loaded' else np.array([.37+rng.uniform(-.01,.01),-.23+rng.uniform(-.01,.01),.0205])
    ball=add(world,'body',name='marble',pos=vec(ball_pos))
    add(ball,'freejoint',name='marble_free')
    add(ball,'geom',name='marble',type='sphere',size='.02',mass='.025',rgba='.95 .15 .12 1',friction='1.2 .005 .001')
    shot_detail(ball,'sphere')
    add(root.find('equality'),'weld',name='loaded_latch',body1='carriage',body2='marble',
        relpose='0 0 .025 1 0 0 0',active=str(mode=='loaded').lower(),solref='.002 1')
    blocks=[]
    shift=float(rng.uniform(-.025,.025))

    def block(name,pos,size,mass=.07):
        pos=np.array(pos,dtype=float);pos[0]+=shift
        b=add(world,'body',name=name,pos=vec(pos))
        add(b,'freejoint',name=name+'_free')
        add(b,'geom',name=name,type='box',size=vec(size),mass=mass,
            rgba='.70 .46 .24 1',material='wood_mat',friction='.55 .005 .0001')
        block_detail(b,size)
        blocks.append(dict(name=name,pos=pos.tolist(),size=list(size)))

    target=[1.65+shift,0,.095]
    if level=='gate':
        block('shield',[1.28,0,.18],[.028,.18,.18],.065)
        target=[1.60+shift,0,.095]
    elif level=='bridge':
        block('left_support',[1.22,0,.20],[.025,.12,.20],.045)
        block('right_support',[1.64,0,.20],[.025,.12,.20],.045)
        block('roof',[1.43,0,.426],[.24,.12,.026],.08)
        target=[1.43+shift,0,.09]
    elif level=='domino':
        for i in range(5):
            block(f'domino{i}',[1.05+i*.13,0,.17],[.018,.085,.17],.04)
        target=[1.77+shift,0,.07]
    old_radius=.065 if level=='domino' else .085
    radius=old_radius*.8
    target[2]-=old_radius-radius
    b=add(world,'body',name='target0',pos=vec(target))
    pig(b,'target0',radius)
    spec=dict(blocks=blocks,target=target,ball_spawn=ball_pos.tolist())
    apply_positions(root,spec,positions,mode)
    return ET.tostring(root,encoding='unicode'),spec
