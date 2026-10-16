"""Procedural visual domains for the marble arena, without physical changes.

Call after ``appearance.workshop`` and scene construction. The default park is
an exact no-op, including RNG consumption. Other domains reuse the existing
world-level cosmetic geom slots, preserving every body/joint/geom ID and count.
Only lighting, sky/floor assets and massless non-contact scenery are modified.
"""
import math
import hashlib
import xml.etree.ElementTree as ET

import numpy as np


BACKGROUNDS = {
    'park': {'title': 'Meadow park', 'title_zh': '草地公园'},
    'desert': {'title': 'Apricot dunes', 'title_zh': '杏色沙丘'},
    'snow': {'title': 'Alpine snow', 'title_zh': '雪松山谷'},
    'studio': {'title': 'Robotics studio', 'title_zh': '机器人摄影棚'},
    'dusk': {'title': 'Moonlit garden', 'title_zh': '暮色月光园'},
}

# Orthogonal to the five palettes. These are visual nuisance conditions, never
# additional simulation bodies or forces. Static preserves the original path.
BACKGROUND_MOTIONS = ('static', 'drift', 'pulse')


def validate_background_motion(motion):
    if motion not in BACKGROUND_MOTIONS:
        raise ValueError(f'Unknown background_motion {motion!r}; choose from {BACKGROUND_MOTIONS}')


def background_motion_metadata(motion='static'):
    """JSON-safe protocol description; realization uses the existing visual seed."""
    validate_background_motion(motion)
    return dict(name=motion, visual_only=True, clock='simulation_time_seconds',
                period_seconds=None if motion == 'static' else 12.,
                translation_amplitude_m=[.12, 0., .018] if motion == 'drift' else [0., 0., 0.],
                rgb_gain_range=[.78, 1.] if motion == 'pulse' else [1., 1.],
                scope='distant_world_cosmetic_geometry_render_copy',
                protects_task_silhouettes=True, changes_physics=False)


def _project_sphere(position, radius, camera):
    """Conservative perspective bounds in normalized camera coordinates.

    A bounding sphere is enclosed by a camera-aligned box. Projecting its eight
    corners encloses its silhouette; this intentionally over-protects the task.
    No rasterization, wall clock, model edits or random draws are needed.
    """
    delta = np.asarray(position) - camera.pos
    depth = float(np.dot(delta, camera.forward))
    if depth <= radius + float(camera.frustum_near):
        return None
    right = np.cross(camera.forward, camera.up)
    xy = np.array([np.dot(delta, right), np.dot(delta, camera.up)])
    corners = np.array([(xy + sign * radius) / z
                        for sign in (-1., 1.) for z in (depth - radius, depth + radius)])
    return np.r_[np.min(corners, axis=0), np.max(corners, axis=0)]


def _scene_sphere_bounds(position, radius, scene):
    # MuJoCo renders a mono view between its two GL cameras. Protect the full
    # union, so this guard also covers their small interpupillary displacement.
    bounds = [_project_sphere(position, radius, camera) for camera in scene.camera]
    if any(item is None for item in bounds):
        return None
    return np.r_[np.minimum(bounds[0][:2], bounds[1][:2]),
                 np.maximum(bounds[0][2:], bounds[1][2:])]


def apply_background_motion(scene, model, simulation_time, motion='static', visual_seed=0,
                            background=None):
    """Animate distant scenery in an already updated ``MjvScene`` only.

    Call immediately after ``Renderer.update_scene``: each frame starts from
    authored geometry, so repeated rendering at the same simulation time is
    exactly deterministic. ``MjModel`` and ``MjData`` are never written. The
    legacy static path returns before reading the seed or scene and consumes no
    RNG. A conservative camera-space guard leaves scenery unchanged wherever
    its complete motion envelope overlaps any visible task/robot silhouette.
    Attached group-4 decorations (pig faces, rule signs, projectile decals) are
    task objects and are expressly excluded from animation.
    """
    validate_background_motion(motion)
    if motion == 'static':
        return 0
    import mujoco as mj
    if not math.isfinite(float(simulation_time)):
        raise ValueError('simulation_time must be finite')
    if isinstance(visual_seed, bool) or not isinstance(visual_seed, (int, np.integer)) or not 0 <= int(visual_seed) < 2**64:
        raise ValueError('visual_seed must be a nonnegative integer below 2**64')
    digest = hashlib.sha256(f'background-motion-v1:{int(visual_seed)}'.encode()).digest()
    phase = 2 * math.pi * int.from_bytes(digest[:8], 'little') / 2**64
    angle = 2 * math.pi * (float(simulation_time) % 12.) / 12. + phase
    shift = np.array([.12 * math.sin(angle), 0., .018 * math.sin(angle)])
    gain = .89 + .11 * math.sin(angle)
    protected = []
    candidates = []
    for geom in scene.geoms[:scene.ngeom]:
        if geom.objtype != mj.mjtObj.mjOBJ_GEOM or geom.objid < 0 or geom.rgba[3] <= 0:
            continue
        gid = int(geom.objid)
        world = model.geom_bodyid[gid] == 0
        cosmetic = (world and model.geom_group[gid] == 4 and
                    model.geom_contype[gid] == 0 and model.geom_conaffinity[gid] == 0)
        if cosmetic:
            if geom.pos[1] >= 1.6 and geom.pos[2] >= .5 and model.geom_rbound[gid] <= .42:
                candidates.append((geom, float(model.geom_rbound[gid])))
        elif not world or model.geom_type[gid] != mj.mjtGeom.mjGEOM_PLANE:
            bounds = _scene_sphere_bounds(geom.pos, float(model.geom_rbound[gid]), scene)
            if bounds is not None:
                protected.append(bounds)
    protected = np.asarray(protected).reshape(-1, 4)
    # Snow's low, connected mountain/tree meshes are deliberately not moved as
    # separate rigid pieces. Reuse otherwise hidden existing cosmetic IDs for
    # a few small distant snow motes in the render scene only. update_scene
    # omits alpha-zero geoms, so these visual copies must be appended explicitly.
    # No mesh, geom, body or joint is added to MjModel, and static is unchanged.
    if background == 'snow':
        dormant = np.flatnonzero((model.geom_bodyid == 0) & (model.geom_group == 4) &
                                 (model.geom_contype == 0) & (model.geom_conaffinity == 0) &
                                 (model.geom_rgba[:, 3] == 0))
        for index, gid in enumerate(dormant[:6]):
            if scene.ngeom >= scene.maxgeom:
                break
            position = np.array([-.52 + .57 * index, 2.7, 1.40 + .065 * (index % 3)])
            radius = .017
            bounds = _scene_sphere_bounds(position, radius + .139, scene)
            if bounds is None:
                continue
            overlap = ((protected[:, 0] <= bounds[2]) & (protected[:, 2] >= bounds[0]) &
                       (protected[:, 1] <= bounds[3]) & (protected[:, 3] >= bounds[1]))
            if np.any(overlap):
                continue
            geom = scene.geoms[scene.ngeom]
            mj.mjv_initGeom(geom, mj.mjtGeom.mjGEOM_SPHERE, np.full(3, radius),
                           position, np.eye(3).ravel(), np.array([.86, .95, 1., 1.]))
            geom.objtype = mj.mjtObj.mjOBJ_GEOM
            geom.objid = int(gid)
            geom.category = mj.mjtCatBit.mjCAT_DECOR
            geom.segid = scene.ngeom
            geom.modelrbound = radius
            scene.ngeom += 1
            candidates.append((geom, radius))
    changed = 0
    for geom, radius in candidates:
        # Both motion types preserve current task silhouettes. Drift protects
        # its entire bounded envelope, not just a particular sampled frame.
        envelope = radius + (.139 if motion == 'drift' else 0.)
        bounds = _scene_sphere_bounds(geom.pos, envelope, scene)
        if bounds is None:
            continue
        overlap = ((protected[:, 0] <= bounds[2]) & (protected[:, 2] >= bounds[0]) &
                   (protected[:, 1] <= bounds[3]) & (protected[:, 3] >= bounds[1]))
        if np.any(overlap):
            continue
        if motion == 'drift':
            geom.pos[:] += shift
        else:
            geom.rgba[:3] *= gain
        changed += 1
    return changed


def _vec(values):
    return ' '.join(format(float(x), '.10g') for x in values)


def _element(parent, tag, name=None, **attrs):
    item = parent.find(f"{tag}[@name='{name}']") if name else parent.find(tag)
    if item is None:
        item = ET.SubElement(parent, tag)
    if name:
        item.set('name', name)
    item.attrib.update({k: str(v) for k, v in attrs.items()})
    return item


def _scenery(background, offset):
    """Return original procedural scenery, always outside manipulation space."""
    geoms = []
    meshes = {}

    def add(kind, pos=None, size=None, color=None, **attrs):
        attrs['type'] = kind
        if pos is not None:
            attrs['pos'] = _vec(pos)
        if size is not None:
            attrs['size'] = _vec(size if isinstance(size, (list, tuple)) else [size])
        if color is not None:
            attrs['rgba'] = _vec(color)
        geoms.append(attrs)

    def line(a, b, radius, color):
        add('capsule', size=radius, color=color, fromto=_vec([*a, *b]))

    def pyramid(name, pos, radius, height, color):
        meshes[name] = [[-radius, -radius, 0], [radius, -radius, 0],
                        [radius, radius, 0], [-radius, radius, 0], [0, 0, height]]
        add('mesh', pos, color=color, mesh=name)

    # The painted landing strip is cosmetic, at the unchanged physical plane.
    add('box', [1.48, 0, .00015], [.66, .225, .0001],
        material=f'bg_{background}_lane')
    border = {'desert': [.95, .87, .61, 1], 'snow': [.34, .65, .77, 1],
              'studio': [.24, .82, .91, 1], 'dusk': [.92, .72, .39, 1]}[background]
    for y in (-.26, .26):
        for x in (1., 1.15, 1.3, 1.45, 1.6, 1.75, 1.9, 2.05):
            add('box', [x, y, .00035], [.029, .002, .0001], border)

    if background == 'desert':
        # Rounded sand ridges and terracotta mesas behind the firing corridor.
        for i, (x, y, sx, sy, sz) in enumerate((
                (-.55, 1.5, .62, .38, .18), (.34, 1.9, .72, .46, .24),
                (1.28, 1.8, .58, .42, .18), (2.22, 1.48, .66, .40, .22))):
            add('ellipsoid', [x + offset, y, .015], [sx, sy, sz],
                [.83 + .02 * (i % 2), .59 + .035 * (i % 3), .34, 1])
        for x, y, h in ((-.48, 1.1, .53), (2.36, .97, .62)):
            x += offset
            green = [.29, .48, .28, 1]
            line([x, y, 0], [x, y, h], .036, green)
            for sign, z in ((-1, h * .45), (1, h * .64)):
                line([x, y, z], [x + sign * .105, y, z], .024, green)
                line([x + sign * .105, y, z],
                     [x + sign * .105, y, z + .14], .024, green)
        for i, (x, y) in enumerate(((2.45, .35), (2.30, 1.50), (-.49, .95))):
            for j in range(2):
                add('box', [x + offset + j * .025, y, .07 + j * .12],
                    [.13 - j * .03, .105 - j * .025, .07 - j * .015],
                    [.67 + i * .02, .39 + j * .045, .25, 1])
        add('sphere', [2.42, 2.2, 1.18], .14, [.99, .82, .39, 1],
            material='bg_desert_glow')
        # Dry flowering shrubs never overlap the ground pickup or landing lane.
        for x, y in ((-.36, -.86), (.83, -.60), (1.80, -.57), (2.18, .70)):
            for j in (-1, 0, 1):
                line([x, y, 0], [x + j * .024, y, .065 - abs(j) * .012],
                     .003, [.61, .42, .22, 1])
            add('sphere', [x, y, .070], .012, [.96, .66, .42, 1])

    elif background == 'snow':
        for i, (x, y, r, h) in enumerate(((-.56, 1.82, .56, .65),
                (.41, 2.15, .67, .86), (1.47, 2.04, .62, .68),
                (2.43, 1.79, .57, .72))):
            pyramid(f'bg_snow_peak{i}', [x + offset, y, -.02], r, h,
                    [.69 + .025 * i, .81 + .018 * i, .89 + .012 * i, 1])
            pyramid(f'bg_snow_cap{i}', [x + offset, y, h * .44], r * .52,
                    h * .54, [.97, .985, .99, 1])
        for i, (x, y) in enumerate(((-.48, 1.10), (.27, 1.70), (2.35, .98))):
            x += offset
            add('cylinder', [x, y, .17], [.018, .17], [.39, .32, .29, 1])
            for j, (r, z, h) in enumerate(((.18, .16, .25), (.145, .30, .23),
                                          (.10, .44, .22))):
                pyramid(f'bg_snow_tree{i}_{j}', [x, y, z], r, h,
                        [.22 + j * .035, .42 + j * .03, .41 + j * .03, 1])
                pyramid(f'bg_snow_treecap{i}_{j}', [x, y, z + h * .3],
                        r * .72, h * .72, [.95, .98, .98, 1])
        for i, (x, y) in enumerate(((-.36, -.86), (.81, -.62), (1.86, -.60),
                                    (2.30, .46), (-.48, .80))):
            add('ellipsoid', [x, y, .018], [.11, .075, .039], [.96, .98, 1, 1])
            add('sphere', [x + .023, y, .041], .013, [.73, .84, .91, 1])

    elif background == 'studio':
        # A photographic cyclorama, with geometric panels and light bars.
        for i, x in enumerate((-.64, -.05, .54, 1.13, 1.72, 2.31)):
            add('box', [x, 2.08, .61], [.285, .025, .63],
                [.15 + .009 * i, .20 + .008 * i, .28 + .009 * i, 1])
            add('box', [x + .274, 2.049, .61], [.006, .002, .56],
                [.26, .70, .79, 1], material='bg_studio_glow')
        for x, y in ((-.46, 1.04), (2.35, 1.02)):
            add('cylinder', [x, y, .16], [.055, .16], [.19, .25, .33, 1])
            add('box', [x, y, .36], [.105, .048, .040],
                [.85, .92, .95, 1], material='bg_studio_glow')
        # Offset-resistant visual floor markings outside the manipulation area.
        for x in (-.45, .0, .45, .90, 1.35, 1.80, 2.25):
            add('box', [x, 1.15, .0003], [.003, .54, .0001], [.30, .40, .48, 1])
        for y in (.62, 1.05, 1.48):
            add('box', [.90, y, .0003], [1.36, .003, .0001], [.30, .40, .48, 1])
        # A restrained amber/cyan backboard palette distinguishes it from snow.
        for i, x in enumerate((-.18, .98, 2.10)):
            add('box', [x + offset, 2.044, .82], [.17, .002, .075],
                [.93, .65, .32, 1] if i == 1 else [.36, .68, .76, 1])

    elif background == 'dusk':
        for i, (x, y, r, h) in enumerate(((-.52, 1.82, .57, .41),
                (.45, 2.00, .71, .55), (1.49, 1.93, .61, .43),
                (2.39, 1.67, .58, .48))):
            pyramid(f'bg_dusk_ridge{i}', [x + offset, y, -.025], r, h,
                    [.20 + i * .012, .23 + i * .010, .34 + i * .018, 1])
        add('sphere', [2.34, 2.18, 1.23], .145, [.99, .92, .69, 1],
            material='bg_dusk_glow')
        for i in range(19):
            # Authored quasiperiodic placements, no hidden/global random state.
            x = -.65 + (i * .437 % 3.2)
            z = .82 + (i * .173 % .73)
            add('sphere', [x, 2.35 + .13 * math.sin(i), z],
                .007 + .002 * (i % 3), [.90, .92, 1, 1], material='bg_dusk_glow')
        for x, y in ((-.48, 1.06), (2.37, .98)):
            add('cylinder', [x, y, .24], [.012, .24], [.19, .22, .27, 1])
            add('box', [x, y, .465], [.052, .052, .008], [.29, .29, .36, 1])
            add('sphere', [x, y, .50], .043, [1, .81, .47, 1],
                material='bg_dusk_glow')
            add('ellipsoid', [x, y, .003], [.13, .10, .001], [.56, .43, .28, 1])
        for x, y in ((.82, -.61), (1.87, -.57), (2.18, .45), (-.36, -.86)):
            for j in range(3):
                add('sphere', [x + .024 * math.cos(j * 2), y + .014 * math.sin(j * 2),
                               .025 + .009 * j], .006, [1, .78, .42, 1],
                    material='bg_dusk_glow')
    return geoms, meshes


def apply_background(root, background='park', rng=None):
    """Apply a named visual domain and return JSON-safe realization metadata.

    ``rng`` must be an independent visual ``numpy.random.Generator`` (or another
    object with ``uniform``). Its three bounded draws affect scenery/color/light
    only. ``None`` selects the exact authored palette. The function must not be
    given the RNG used for target, obstacle, ammunition or robot initialization.
    Call once on an XML tree built with ``appearance.workshop``. Park leaves the
    tree byte-for-byte unchanged and does not inspect or draw from ``rng``.
    """
    if background not in BACKGROUNDS:
        raise ValueError(f'Unknown background {background!r}; choose from {tuple(BACKGROUNDS)}')
    metadata = dict(name=background, title=BACKGROUNDS[background]['title'],
                    visual_only=True, randomized=False, variation={}, decorated_geoms=0)
    if background == 'park':
        return metadata
    world, asset, visual = root.find('worldbody'), root.find('asset'), root.find('visual')
    if world is None or asset is None or visual is None:
        raise ValueError('Backgrounds require a complete workshop scene')
    slots = [g for g in world.findall('geom') if g.get('group') == '4'
             and g.get('mass') == '0' and g.get('contype') == '0'
             and g.get('conaffinity') == '0']
    if not slots or asset.find("material[@name='floor_mat']") is None:
        raise ValueError('Backgrounds require appearance.workshop cosmetic slots and floor material')
    hue = offset = light_gain = 0.
    if rng is not None:
        hue = float(rng.uniform(-.025, .025))
        offset = float(rng.uniform(-.035, .035))
        light_gain = float(rng.uniform(-.04, .04))
        metadata['randomized'] = True
    metadata['variation'] = dict(palette_shift=hue, scenery_offset_x=offset,
                                 light_gain=light_gain)
    geoms, meshes = _scenery(background, offset)
    if len(geoms) > len(slots):
        raise ValueError(f'Background needs {len(geoms)} existing cosmetic slots; found {len(slots)}')

    palettes = {
        'desert': dict(floor=[.78, .61, .39], alternate=[.82, .65, .43], lane=[.67, .48, .30, 1],
                       sky1=[.58, .77, .83], sky2=[.95, .85, .65], haze=[.89, .77, .60, 1],
                       ambient=[.43, .40, .34], diffuse=[.29, .27, .22]),
        'snow': dict(floor=[.87, .92, .95], alternate=[.93, .965, .98], lane=[.62, .77, .85, 1],
                     sky1=[.40, .64, .81], sky2=[.86, .94, .98], haze=[.85, .93, .98, 1],
                     ambient=[.39, .43, .47], diffuse=[.25, .28, .32]),
        'studio': dict(floor=[.24, .30, .37], alternate=[.26, .32, .39], lane=[.39, .47, .55, 1],
                       sky1=[.14, .19, .27], sky2=[.30, .39, .48], haze=[.29, .36, .45, 1],
                       ambient=[.41, .43, .46], diffuse=[.30, .32, .35]),
        'dusk': dict(floor=[.25, .28, .34], alternate=[.28, .31, .37], lane=[.44, .39, .39, 1],
                     sky1=[.11, .12, .27], sky2=[.65, .38, .42], haze=[.43, .35, .48, 1],
                     ambient=[.38, .36, .44], diffuse=[.29, .28, .35]),
    }
    palette = palettes[background]
    def color(values):
        return _vec([min(1., max(0., v + hue)) for v in values])
    texture_name = f'bg_{background}_floor_tex'
    _element(asset, 'texture', texture_name, type='2d', builtin='checker',
             rgb1=color(palette['floor']), rgb2=color(palette['alternate']),
             width='512', height='512')
    floor = asset.find("material[@name='floor_mat']")
    floor.attrib.update(texture=texture_name, texrepeat='9 9', texuniform='true',
                        rgba='1 1 1 1', reflectance='0', specular='.03', shininess='.1')
    _element(asset, 'material', f'bg_{background}_lane', rgba=_vec(palette['lane']),
             specular='.04', shininess='.1')
    _element(asset, 'material', f'bg_{background}_glow', emission='.6',
             specular='.08', shininess='.1')
    for name, vertices in meshes.items():
        _element(asset, 'mesh', name, vertex=_vec([v for xyz in vertices for v in xyz]))
    sky = asset.find("texture[@name='sky']")
    if sky is not None:
        sky.attrib.update(rgb1=color(palette['sky1']), rgb2=color(palette['sky2']))
    _element(visual, 'headlight', ambient=_vec([v + light_gain for v in palette['ambient']]),
             diffuse=_vec([v + light_gain for v in palette['diffuse']]), specular='.08 .08 .08')
    _element(visual, 'rgba', haze=_vec(palette['haze']))
    # Existing lights keep their IDs, position, direction and shadow setup.
    for light in world.findall('light'):
        diffuse = [float(v) for v in light.get('diffuse', '.7 .7 .7').split()]
        tint = (1., .93, .81) if background == 'desert' else (
               (.80, .90, 1.) if background in ('snow', 'studio') else (.95, .79, 1.))
        light.set('diffuse', _vec([v * t * (1 + light_gain) for v, t in zip(diffuse, tint)]))

    for index, slot in enumerate(slots):
        if index >= len(geoms):
            rgba = slot.get('rgba', '1 1 1 1').split()
            slot.set('rgba', ' '.join([*rgba[:3], '0']))
            continue
        name = slot.get('name')
        slot.attrib.clear()
        if name:
            slot.set('name', name)
        slot.attrib.update(geoms[index])
        slot.attrib.update(contype='0', conaffinity='0', mass='0', group='4')
    metadata['decorated_geoms'] = len(geoms)
    metadata['retained_cosmetic_slots'] = len(slots)
    return metadata
