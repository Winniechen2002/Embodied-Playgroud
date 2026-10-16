"""Original toy-park art direction; every decoration is massless and non-contact.

Group 4 holds cosmetic geometry. Hiding that group changes rendering only; the
floor, robots, projectiles, obstacle colliders and green damage spheres remain.
"""
import math
import xml.etree.ElementTree as ET
from pathlib import Path

ASSET_DIR = Path(__file__).parent / 'assets'


def geom(parent, **attrs):
    return ET.SubElement(parent, 'geom', {k: str(v) for k, v in attrs.items()})


def decor(parent, **attrs):
    attrs.update(contype=0, conaffinity=0, mass=0, group=4)
    return geom(parent, **attrs)


def pig(body, name, radius, size_name='standard'):
    """One radius-matched damage sphere; facial features are cosmetic."""
    geom(body, name=name, type='sphere', size=radius, rgba='.47 .78 .20 1',
         material='pig_mat')

    def detail(suffix, xyz, size, color, kind='sphere'):
        decor(body, name=f'{name}_{suffix}', type=kind,
              pos=' '.join(str(v*radius) for v in xyz),
              size=' '.join(str(v*radius) for v in size), rgba=color)

    for i, x in enumerate((-.48, .48)):
        detail(f'ear{i}', [x, 0, .87], [.25, .20, .32], '.38 .69 .17 1', 'ellipsoid')
        detail(f'ear_inner{i}', [x, -.17, .91], [.12, .035, .17], '.75 .88 .40 1', 'ellipsoid')
        detail(f'eye{i}', [x*.78, -.84, .32], [.22], '1 .995 .92 1')
        detail(f'pupil{i}', [x*.78+.025, -1.035, .30], [.095], '.08 .15 .055 1')
        detail(f'glint{i}', [x*.78+.005, -1.11, .33], [.025], '1 1 1 1')
    detail('snout', [0, -.92, -.13], [.47, .20, .32], '.70 .87 .37 1', 'ellipsoid')
    for i,x in enumerate((-.18,.18)):
        detail(f'nostril{i}', [x, -1.105, -.11], [.078, .035, .11], '.26 .44 .13 1', 'ellipsoid')
    for i,x in enumerate((-.67,.67)):
        detail(f'cheek{i}', [x, -.73, -.12], [.14,.03,.08], '.91 .61 .30 1', 'ellipsoid')
    if size_name=='large':
        for i,x in enumerate((-.39,.39)):
            detail(f'brow{i}',[x,-.97,.57],[.24,.045,.06],'.20 .38 .08 1','ellipsoid')
        for i,x in enumerate((-.21,.21)):
            detail(f'tooth{i}',[x,-.97,-.46],[.095,.05,.12],'.99 .97 .84 1','ellipsoid')


def target_rule_marker(body, name, radius, protected=False, rank=None):
    """Visible non-colliding shield/cross or ordinal, for task-rule grounding."""
    y=-radius*.95; z=radius*1.60
    if protected:
        main=body.find(f"geom[@name='{name}']")
        if main is not None:main.set('rgba','.18 .55 .95 1')
    decor(body,name=f'art_rule_{name}_sign',type='box',pos=f'0 {y} {z}',
          size=f'{radius*.43} .001 {radius*.46}',rgba='.10 .40 .75 1' if protected else '.97 .88 .45 1')
    front=y-.0018
    if protected:
        for dx,dz in ((.27,.07),(.07,.27)):
            decor(body,type='box',pos=f'0 {front} {z}',size=f'{radius*dx} .0005 {radius*dz}',rgba='1 1 1 1')
    elif rank is not None:
        # Seven-segment numerals 1–3; no text renderer or hidden ID needed.
        points={'a':((-.23,.31),(.23,.31)),'b':((.23,.31),(.23,0)),
                'c':((.23,0),(.23,-.31)),'d':((-.23,-.31),(.23,-.31)),
                'e':((-.23,0),(-.23,-.31)),'f':((-.23,.31),(-.23,0)),
                'g':((-.23,0),(.23,0))}
        for segment in {1:'bc',2:'abged',3:'abgcd'}[rank]:
            a,b=points[segment]
            decor(body,type='capsule',fromto=f'{a[0]*radius} {front} {z+a[1]*radius} {b[0]*radius} {front} {z+b[1]*radius}',
                  size=radius*.035,rgba='.13 .20 .19 1')


def shot_detail(body, kind, size=None):
    """Apply stripes to the real collider, with a tiny face on regular shapes.

Convex wedges and shards get texture only, preserving their readable silhouette.
Repeated calls replace prior decorations, for the first shared scene projectile.
"""
    for child in list(body):
        if child.tag=='geom' and child.get('name','').startswith('art_shot_'):
            body.remove(child)
    main=next((g for g in body.findall('geom') if g.get('contype','1')!='0'),None)
    if main is None:return
    styles={'sphere':'red','cube':'cube','heavy':'heavy','capsule':'irregular',
            'wedge':'irregular','shard':'irregular'}
    main.set('material',f'shot_{styles.get(kind,"irregular")}_mat')
    main.set('rgba','1 1 1 1')
    if kind not in ('sphere','cube','heavy','capsule'):return
    name=body.get('name','ammo')
    r=.017 if kind=='cube' else (.014 if kind=='capsule' else .02)
    for i,x in enumerate((-.27*r,.27*r)):
        # Eyes are flat decals expressed as ellipsoids, at most 1.2 mm proud.
        y=-r if kind=='cube' else -r*.93
        decor(body,name=f'art_shot_{name}_eye{i}',type='ellipsoid',
              pos=f'{x} {y} {r*.23}',size=f'{r*.17} .0008 {r*.21}',rgba='1 .995 .91 1')
        decor(body,name=f'art_shot_{name}_pupil{i}',type='ellipsoid',
              pos=f'{x} {y-.00065} {r*.21}',size=f'{r*.08} .0005 {r*.10}',rgba='.11 .12 .17 1')


def block_detail(body, size, fixed=False, material=None, shape='box'):
    """Texture the real solid and add restrained joinery only on box obstacles."""
    main=body.find('geom')
    if main is not None:
        # Colored PNGs own their palette rather than multiplying a dark tint.
        main.set('rgba','1 1 1 1')
        if material:main.set('material',material if material.endswith('_mat') else material+'_mat')
        shape=main.get('type',shape)
    if shape!='box' or len(size)<3:return
    x,y,z=size
    mat=main.get('material','') if main is not None else ''
    if 'glass' in mat:
        for sign in (-1,1):
            decor(body,type='box',pos=f'{sign*x*.93} {-y-.0003} 0',
                  size=f'{min(.0016,x*.035)} .0003 {z*.92}',rgba='.48 .90 .94 1')
        return
    if fixed or 'stone' in mat or 'rubber' in mat:return
    # Joint bands make beams readable even at small gallery scale.
    for fraction in (-.73,.73):
        decor(body,type='box',pos=f'0 {-y-.00035} {z*fraction}',
              size=f'{x*.93} .0003 {min(.0018,z*.045)}',rgba='.60 .35 .13 1')
    if z>.09 and x<.06:
        for fraction in (-.80,.80):
            decor(body,type='sphere',pos=f'0 {-y-.001} {z*fraction}',size='.003',rgba='.94 .75 .42 1')



def fixed_detail(body, size):
    """A small gold padlock badge identifies an immovable structural body.

Material color denotes wood/stone/glass/rubber, never whether it can move.
The badge is a cosmetic annotation and contributes neither mass nor contacts.
"""
    if len(size)<3:return
    x,y,z=size
    scale=min(1.,x/.018,z/.024)
    r=.0015*scale;front=-y-.001;cz=0.
    decor(body,name='art_fixed_badge_'+body.get('name','body'),type='box',
          pos=f'0 {front} {cz}',size=f'{.010*scale} .0006 {.009*scale}',rgba='1 .77 .20 1')
    for a,b in (((-.006,.009),(-.006,.016)),((-.006,.016),(.006,.016)),((.006,.016),(.006,.009))):
        decor(body,type='capsule',fromto=f'{a[0]*scale} {front} {a[1]*scale} {b[0]*scale} {front} {b[1]*scale}',
              size=r,rgba='.99 .88 .46 1')
    decor(body,type='ellipsoid',pos=f'0 {front-.0008} {.001*scale}',
          size=f'{.0024*scale} .0003 {.0024*scale}',rgba='.32 .30 .18 1')
    decor(body,type='box',pos=f'0 {front-.0008} {-.002*scale}',
          size=f'{.0009*scale} .0003 {.0022*scale}',rgba='.32 .30 .18 1')


def workshop(root):
    """Install all texture materials and a decorative park outside the work area."""
    asset=root.find('asset')
    ET.SubElement(asset,'material',name='pig_mat',specular='.18',shininess='.32')
    specs=[('wood_mat','wood_grain','1 2','.10','.16'),
           ('stone_mat','park_stone','1 1','.07','.10'),
           ('glass_mat','park_glass','1 1','.32','.60'),
           ('rubber_mat','park_rubber','1 1','.04','.08'),
           ('grass_mat','park_grass','2 2','.01','.05'),
           ('dirt_mat','park_dirt','2 1','.01','.05'),
           ('shot_red_mat','shot_red','1 1','.25','.38'),
           ('shot_cube_mat','shot_cube','1 1','.20','.32'),
           ('shot_heavy_mat','shot_heavy','1 1','.26','.42'),
           ('shot_irregular_mat','shot_irregular','1 1','.22','.34')]
    for material,texture,repeat,specular,shine in specs:
        ET.SubElement(asset,'texture',name=texture,type='2d' if texture=='park_grass' else 'cube',file=str((ASSET_DIR/f'{texture}.png').resolve()))
        ET.SubElement(asset,'material',name=material,texture=texture,texrepeat=repeat,
                      specular=specular,shininess=shine,rgba='1 1 1 1')
    # This changes the physical plane's visible material only, not its collision.
    floor=asset.find("material[@name='floor_mat']")
    if floor is not None:floor.attrib.update(texture='park_grass',texrepeat='2 2',texuniform='true',rgba='1 1 1 1')
    sky=asset.find("texture[@name='sky']")
    if sky is not None:sky.attrib.update(rgb1='.39 .72 .88',rgb2='.85 .95 .95')
    visual=root.find('visual')
    ET.SubElement(visual,'headlight',ambient='.40 .40 .38',diffuse='.24 .24 .22',specular='.08 .08 .08')
    ET.SubElement(visual,'rgba',haze='.80 .91 .88 1')
    ET.SubElement(visual,'map',fogstart='.8',fogend='2.8',shadowclip='.40')
    world=root.find('worldbody')
    top=world.find("light[@name='top']")
    if top is not None:top.attrib.update(diffuse='.12 .14 .12',specular='.05 .05 .05',castshadow='false')
    # The landing area is a painted dirt strip at the same physical floor level.
    decor(world,name='art_landing_lane',type='box',pos='1.48 0 .00015',
          size='.66 .225 .0001',material='dirt_mat',rgba='1 1 1 1')
    # Cream border pips mark the safe arena without adding raised collision edges.
    for y in (-.26,.26):
        for x in (1.,1.15,1.3,1.45,1.6,1.75,1.9,2.05):
            decor(world,type='box',pos=f'{x} {y} .00035',size='.029 .002 .0001',rgba='.99 .91 .58 1')
    # Backdrop foliage is beyond both robot workspaces and the projectile lane.
    for i,(x,y,s) in enumerate(((-.58,1.35,.43),(.25,1.65,.60),(1.12,1.65,.51),(2.08,1.40,.48))):
        decor(world,name=f'art_hill{i}',type='ellipsoid',pos=f'{x} {y} {s*.10}',
              size=f'{s} {s*.60} {s*.48}',rgba='.40 .65 .35 .999')

    # Flat-topped soil beds, entirely out of reach, expose the playful dirt strata.
    for i,(x,y) in enumerate(((2.43,.12),(2.24,1.05),(-.48,.97))):
        decor(world,name=f'art_soil_bed{i}',type='box',pos=f'{x} {y} .027',
              size='.14 .115 .028',material='dirt_mat',rgba='1 1 1 1')
        decor(world,type='box',pos=f'{x} {y} .058',size='.145 .119 .009',material='grass_mat',rgba='1 1 1 1')
    # Sparse cloud clusters are scenic geometry; they never interact with shots.
    for i,(x,y,z) in enumerate(((-.45,2.15,1.03),(.92,2.55,1.20),(2.50,2.0,1.04))):
        for j,(dx,dz,s) in enumerate(((-.16,0,.13),(0,.055,.18),(.17,0,.13))):
            decor(world,name=f'art_cloud{i}_{j}',type='ellipsoid',pos=f'{x+dx} {y} {z+dz}',
                  size=f'{s} {s*.43} {s*.62}',rgba='.98 .985 .94 .999')
    # Rounded trees retain a low visual horizon behind the target structures.
    for i,(x,y) in enumerate(((-.54,1.12),(2.38,.97))):
        decor(world,name=f'art_tree_trunk{i}',type='cylinder',pos=f'{x} {y} .20',size='.027 .20',rgba='.57 .34 .16 1')
        for j,(dx,dz,s) in enumerate(((-.10,.41,.14),(.10,.43,.15),(0,.57,.16))):
            decor(world,name=f'art_tree_crown{i}_{j}',type='sphere',pos=f'{x+dx} {y} {dz}',size=s,rgba='.39 .65 .33 .999')
    # The flags carry our own simple striped palette, not any franchise artwork.
    for i,(x,y) in enumerate(((.78,.72),(2.15,-.43))):
        decor(world,name=f'art_flagpole{i}',type='cylinder',pos=f'{x} {y} .15',size='.005 .15',rgba='.95 .91 .74 1')
        decor(world,type='box',pos=f'{x+.045} {y} .258',size='.045 .003 .024',rgba='.99 .66 .21 1')
        decor(world,type='box',pos=f'{x+.045} {y-.0035} .263',size='.032 .0003 .003',rgba='1 .94 .72 1')
    # A few clusters frame the arena; no plants occupy pickup or reload positions.
    for i,(x,y) in enumerate(((-.34,-.88),(.80,-.64),(1.30,-.58),(1.87,-.57),(2.24,.48),(.48,1.04))):
        for j,dx in enumerate((-.025,.014,.037)):
            h=.025+j*.006
            decor(world,name=f'art_grass{i}_{j}',type='capsule',fromto=f'{x+dx} {y} .001 {x+dx+.01} {y+.009} {h}',
                  size='.003',rgba='.28 .56 .22 1')
        cx=x+.012;cy=y-.005;cz=.041
        for j in range(5):
            a=j*2*math.pi/5
            decor(world,name=f'art_flower{i}_{j}',type='sphere',pos=f'{cx+.008*math.cos(a)} {cy+.008*math.sin(a)} {cz}',
                  size='.006',rgba='.99 .97 .84 1')
        decor(world,name=f'art_flower_center{i}',type='sphere',pos=f'{cx} {cy} {cz+.004}',size='.0045',rgba='1 .66 .10 1')
