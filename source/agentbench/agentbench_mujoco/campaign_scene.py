"""Physical environment definitions for the independent distribution."""
import xml.etree.ElementTree as ET
import numpy as np
from .dual_scene import make_dual_scene
from .scene import add, vec
from .appearance import pig, block_detail, shot_detail, fixed_detail
from .structures import build_structure
from .projectiles import NEW_AMMO, build_projectile_geometry
from .redesigned_levels import redesigned_scenarios
from .benchmark_levels import benchmark_scenarios
from .multilevel_levels import multilevel_scenarios
from .defense_levels import defense_scenarios
from .atlas_levels_a import atlas_scenarios_a
from .atlas_levels_b import atlas_scenarios_b
from .fracture import build_fracturable
from .variants import sample_variant, scale_structure_contacts, TARGET_TYPES
(MAX_AMMO, MAX_TARGETS, MAX_BLOCKS, MAX_FIXED) = (4, 3, 8, 6)
MAX_FRAGMENTS = 64
OBSERVATION_SCHEMA_VERSION = 8
AMMO = {'sphere': dict(type='sphere', size=[0.02], mass=0.025, z=0.0205, color=[0.95, 0.15, 0.12, 1]), 'cube': dict(type='box', size=[0.017, 0.017, 0.017], mass=0.035, z=0.0175, color=[1, 0.68, 0.12, 1]), 'heavy': dict(type='sphere', size=[0.02], mass=0.045, z=0.0205, color=[0.2, 0.4, 0.85, 1]), 'capsule': dict(type='capsule', size=[0.014, 0.01], mass=0.025, z=0.0245, color=[0.7, 0.3, 0.85, 1])}
AMMO.update(NEW_AMMO)

def obstacle(name, xyz, halfsize, mass=0.06, fixed=False, material=None, shape='box', angle=0.0, condim=None, breakable=False, fracture_threshold=0.025, anchored=False, load_bearing=False, yaw=0.0):
    if fixed and breakable:
        raise ValueError('Breakable glass is a dynamic object; use anchored=True for a releasable anchor')
    if load_bearing and (not breakable):
        raise ValueError('load_bearing specifies a fracture-strength floor and requires breakable=True')
    if not np.isfinite(yaw):
        raise ValueError('Structure yaw must be finite')
    if breakable and yaw:
        raise ValueError('Rotated breakable panes are not supported')
    result = dict(name=name, pos=xyz, size=halfsize, mass=mass, fixed=fixed, material=material or ('stone' if fixed else 'wood'), shape=shape, angle=angle, condim=condim, breakable=breakable, fracture_threshold=fracture_threshold, anchored=anchored, load_bearing=load_bearing)
    if yaw:
        result['yaw'] = float(yaw)
    return result
SCENARIOS = {'twins': dict(title='Two distances', description='Two targets, finite mixed ammunition; choose shot order and draw.', targets=[[1.24, 0, 0.085], [1.7, 0, 0.085]], thresholds=[0.018, 0.025], obstacles=[], ammo=['sphere', 'cube', 'heavy']), 'bunker': dict(title='Fixed bunker', description='A fixed low wall and roof restrict the firing corridor.', targets=[[1.4, 0, 0.075], [1.7, 0, 0.075]], ammo=['sphere', 'cube', 'heavy'], obstacles=[obstacle('fixed_wall', [1.1, 0, 0.095], [0.035, 0.16, 0.095], fixed=True), obstacle('fixed_roof', [1.48, 0, 0.43], [0.31, 0.18, 0.025], fixed=True), obstacle('fixed_rear_post', [1.82, 0.14, 0.2], [0.025, 0.025, 0.2], fixed=True)]), 'perches': dict(title='Three elevations', description='Three elevated targets on immovable platforms.', targets=[[1.2, 0, 0.275], [1.51, 0, 0.195], [1.82, 0, 0.075]], ammo=['sphere', 'cube', 'capsule', 'heavy'], obstacles=[obstacle('fixed_high', [1.2, 0, 0.1], [0.055, 0.12, 0.1], fixed=True), obstacle('fixed_mid', [1.51, 0, 0.06], [0.055, 0.12, 0.06], fixed=True)]), 'twin_bridge': dict(title='Bridge rescue', description='Collapse the bridge onto two sheltered targets.', targets=[[1.36, 0, 0.075], [1.51, 0, 0.075]], ammo=['sphere', 'cube', 'heavy'], obstacles=[obstacle('left_support', [1.2, 0, 0.2], [0.025, 0.12, 0.2], 0.045), obstacle('right_support', [1.67, 0, 0.2], [0.025, 0.12, 0.2], 0.045), obstacle('roof', [1.435, 0, 0.426], [0.265, 0.12, 0.026], 0.08)], indirect=True), 'fortress': dict(title='Wall and tower', description='Arc over a fixed wall, then knock down the wooden tower.', targets=[[1.43, 0, 0.075], [1.69, 0, 0.275]], ammo=['sphere', 'cube', 'heavy'], obstacles=[obstacle('fixed_front', [1.05, 0, 0.11], [0.03, 0.18, 0.11], fixed=True), obstacle('fixed_perch', [1.69, 0, 0.1], [0.055, 0.12, 0.1], fixed=True), obstacle('tower_left', [1.3, 0, 0.22], [0.022, 0.12, 0.22], 0.045), obstacle('tower_right', [1.57, 0, 0.22], [0.022, 0.12, 0.22], 0.045), obstacle('tower_beam', [1.435, 0, 0.468], [0.18, 0.12, 0.028], 0.07)], min_toppled=1), 'domino_fork': dict(title='Domino fork', description='A chain reaction must reach both targets beside a fixed arch.', targets=[[1.77, -0.067, 0.065], [1.77, 0.067, 0.065]], ammo=['sphere', 'cube', 'heavy'], obstacles=[obstacle(f'domino{i}', [1.05 + i * 0.13, 0, 0.17], [0.018, 0.09, 0.17], 0.04) for i in range(5)] + [obstacle('fixed_arch_roof', [1.41, 0, 0.46], [0.31, 0.18, 0.025], fixed=True), obstacle('fixed_arch_side', [1.69, 0.16, 0.215], [0.025, 0.025, 0.215], fixed=True)], min_toppled=3)}
SCENARIOS.update({'warmup': dict(title='First flight', description='One near target with a spare shot to learn draw control.', targets=[[1.3, 0, 0.075]], obstacles=[], ammo=['sphere', 'cube']), 'long_shot': dict(title='Across the lane', description='One distant target needs more spring energy.', targets=[[1.83, 0, 0.075]], obstacles=[], ammo=['sphere', 'heavy']), 'high_stand': dict(title='On a pedestal', description='Aim at a single elevated target on a fixed pedestal.', targets=[[1.35, 0, 0.275]], ammo=['sphere', 'cube'], obstacles=[obstacle('fixed_pedestal', [1.35, 0, 0.1], [0.075, 0.12, 0.1], fixed=True)]), 'wooden_gate': dict(title='Timber gate', description='Knock over the movable shield and reach the target behind it.', targets=[[1.6, 0, 0.075]], ammo=['sphere', 'heavy'], min_toppled=1, obstacles=[obstacle('shield', [1.28, 0, 0.18], [0.028, 0.15, 0.18], 0.065)]), 'low_wall': dict(title='Over the wall', description='Clear an immovable front wall to hit the target.', targets=[[1.5, 0, 0.075]], ammo=['sphere', 'cube'], obstacles=[obstacle('fixed_front', [1.1, 0, 0.08], [0.035, 0.17, 0.08], fixed=True)]), 'staircase': dict(title='Step by step', description='Two targets at different elevations require trajectory selection.', targets=[[1.25, 0, 0.235], [1.7, 0, 0.075]], ammo=['sphere', 'cube', 'heavy'], obstacles=[obstacle('fixed_step', [1.25, 0, 0.08], [0.075, 0.12, 0.08], fixed=True)]), 'window': dict(title='Through the window', description='Thread a shot between a fixed sill and lintel.', targets=[[1.55, 0, 0.075]], ammo=['sphere', 'cube', 'heavy'], obstacles=[obstacle('fixed_sill', [1.12, 0, 0.065], [0.025, 0.16, 0.065], fixed=True), obstacle('fixed_lintel', [1.12, 0, 0.4], [0.025, 0.16, 0.025], fixed=True), obstacle('fixed_jamb', [1.12, 0.185, 0.225], [0.025, 0.025, 0.225], fixed=True)]), 'triple_line': dict(title='Three little targets', description='Three separated targets with different impulse thresholds.', targets=[[1.19, 0, 0.075], [1.51, 0, 0.075], [1.84, 0, 0.075]], thresholds=[0.012, 0.018, 0.025], obstacles=[], ammo=['sphere', 'cube', 'heavy']), 'double_bridge': dict(title='Twin timber halls', description='Collapse two separate bridges; only falling wood can pop targets.', targets=[[1.255, 0, 0.075], [1.775, 0, 0.075]], ammo=['sphere', 'cube', 'capsule', 'heavy'], obstacles=[obstacle('west_left', [1.08, 0, 0.17], [0.022, 0.11, 0.17], 0.04), obstacle('west_right', [1.43, 0, 0.17], [0.022, 0.11, 0.17], 0.04), obstacle('west_beam', [1.255, 0, 0.364], [0.215, 0.11, 0.024], 0.065), obstacle('east_left', [1.6, 0, 0.22], [0.022, 0.11, 0.22], 0.045), obstacle('east_right', [1.95, 0, 0.22], [0.022, 0.11, 0.22], 0.045), obstacle('east_beam', [1.775, 0, 0.464], [0.215, 0.11, 0.024], 0.075)], indirect=True, min_toppled=2), 'one_chance': dict(title='One chance', description='A single projectile must pass the fixed bunker and hit a small target.', targets=[[1.48, 0, 0.075]], ammo=['sphere'], obstacles=[obstacle('fixed_front', [1.08, 0, 0.09], [0.03, 0.16, 0.09], fixed=True), obstacle('fixed_ceiling', [1.4, 0, 0.43], [0.3, 0.16, 0.025], fixed=True)])})
REDESIGNED = redesigned_scenarios(obstacle)
SCENARIOS.update(REDESIGNED)
BENCHMARK_SCENARIOS = benchmark_scenarios(obstacle)
SCENARIOS.update(BENCHMARK_SCENARIOS)
MULTILEVEL_SCENARIOS = multilevel_scenarios(obstacle)
SCENARIOS.update(MULTILEVEL_SCENARIOS)
DEFENSE_SCENARIOS = defense_scenarios(obstacle)
SCENARIOS.update(DEFENSE_SCENARIOS)
(_atlas_a, _atlas_b) = (atlas_scenarios_a(obstacle), atlas_scenarios_b(obstacle))
if set(_atlas_a) & set(_atlas_b) or (set(_atlas_a) | set(_atlas_b)) & set(SCENARIOS):
    raise ValueError('Atlas scenario names must be unique across the whole campaign')
ATLAS_SCENARIOS = {**_atlas_a, **_atlas_b}
SCENARIOS.update(ATLAS_SCENARIOS)
TIERS = {1: dict(title='Foundations', title_zh='基础操作', color='#59A88B', scenes=['warmup', 'long_shot', 'high_stand', 'wooden_gate'], focus='One target; learn range, elevation and movable obstacles.'), 2: dict(title='Trajectory', title_zh='弹道与遮挡', color='#4E91C2', scenes=['twins', 'low_wall', 'staircase', 'window'], focus='Choose trajectories across distances, heights and fixed openings.'), 3: dict(title='Planning', title_zh='多目标规划', color='#C6994A', scenes=['bunker', 'perches', 'twin_bridge', 'triple_line'], focus='Coordinate reloads, multiple targets and indirect damage.'), 4: dict(title='Challenge', title_zh='组合挑战', color='#BE7064', scenes=['fortress', 'domino_fork', 'double_bridge', 'one_chance'], focus='Combine structures and chain reactions, or remove the spare-shot margin.'), 5: dict(title='Spatial structures', title_zh='方位与多层结构', color='#8872B5', scenes=[], focus='Aim in azimuth and elevation; reason about several structural levels and lateral targets.')}
for (_name, _cfg) in {**REDESIGNED, **BENCHMARK_SCENARIOS, **MULTILEVEL_SCENARIOS, **DEFENSE_SCENARIOS, **ATLAS_SCENARIOS}.items():
    TIERS[_cfg['tier']]['scenes'].append(_name)
for (_tier, _cfg) in TIERS.items():
    for (_order, _name) in enumerate(_cfg['scenes'], 1):
        SCENARIOS[_name].update(tier=_tier, stage=f'{_tier}-{_order}')
for (_name, _cfg) in SCENARIOS.items():
    _tags = ['bimanual_coordination', 'trajectory_control']
    if len(_cfg['ammo']) > 1:
        _tags.append('physical_reload')
    if len(_cfg['targets']) > 1:
        _tags.append('multi_target_planning')
    if _cfg.get('indirect') or _cfg.get('damage_sources'):
        _tags.append('causal_reasoning')
    if any((x['fixed'] for x in _cfg['obstacles'])):
        _tags.append('fixed_obstacle_reasoning')
    _aliases = {'reload': 'physical_reload', 'causal_chain': 'causal_reasoning', 'trajectory_selection': 'trajectory_control', 'aim_force_coordination': 'bimanual_coordination'}
    _cfg['capabilities'] = list(dict.fromkeys(_tags + [_aliases.get(tag, tag) for tag in _cfg.get('capabilities', [])]))
    _cfg.setdefault('split', 'train')

def scenario_names(tier=None):
    return [name for (number, cfg) in TIERS.items() if tier is None or tier == number for name in cfg['scenes']]

def make_campaign_scene(scenario, mode, rng, timestep, *, target_profile='authored', variation='nominal', background='park', visual_seed=None, position_randomization='off', yaw_enabled=None, background_motion='static', spring_stiffness=25.0, launcher_offset_m=(0.0, 0.0, 0.0), ammunition_offset_m=(0.0, 0.0, 0.0)):
    cfg = SCENARIOS[scenario]
    if yaw_enabled is None:
        yaw_enabled = cfg.get('yaw_enabled', False)
    if not isinstance(yaw_enabled, bool):
        raise ValueError('yaw_enabled must be a boolean or None')
    from .positions import sample_positions, apply_positions
    positions = sample_positions(rng, position_randomization, len(cfg['targets']), cfg.get('target_position_x_directions'))
    from .backgrounds import apply_background, BACKGROUND_MOTIONS
    if background_motion not in BACKGROUND_MOTIONS:
        raise ValueError('Unknown background_motion')
    from .launcher_variants import validate_launcher_configuration, configure_launcher
    validate_launcher_configuration(spring_stiffness, launcher_offset_m, ammunition_offset_m)
    from .variants import validate_variant
    validate_variant(target_profile, variation, background, visual_seed)
    variant = sample_variant(rng, target_profile, variation, background, visual_seed, len(cfg['targets']))
    realized = variant['realized']
    (xml, spec) = make_dual_scene('direct', mode, rng, timestep, yaw_enabled=yaw_enabled)
    root = ET.fromstring(xml)
    world = root.find('worldbody')
    if cfg.get('multiccd', False):
        option = root.find('option')
        if option is None:
            option = ET.SubElement(root, 'option')
        flag = option.find('flag')
        if flag is None:
            flag = ET.SubElement(option, 'flag')
        flag.set('multiccd', 'enable')
        spec['contact_solver'] = {'multiccd': True}
    if 'impratio' in cfg:
        impratio = float(cfg['impratio'])
        if not np.isfinite(impratio) or impratio <= 0:
            raise ValueError('impratio must be finite and positive')
        option = root.find('option')
        if option is None:
            option = ET.SubElement(root, 'option')
        option.set('impratio', format(impratio, '.15g'))
        spec.setdefault('contact_solver', {})['impratio'] = impratio
    if 'noslip_iterations' in cfg:
        iterations = cfg['noslip_iterations']
        if type(iterations) is not int or not 0 <= iterations <= 100:
            raise ValueError('noslip_iterations must be an integer in 0..100')
        option = root.find('option')
        if option is None:
            option = ET.SubElement(root, 'option')
        option.set('noslip_iterations', str(iterations))
        spec.setdefault('contact_solver', {})['noslip_iterations'] = iterations
    world.remove(world.find("body[@name='target0']"))
    shift = float(rng.uniform(-0.012, 0.012))
    offset = np.array(realized['layout_offset_m']) + [shift, 0, 0]
    realized['legacy_shift_m'] = shift
    realized['total_layout_offset_m'] = offset.tolist()
    blocks = []
    fixed = []
    fractures = []
    for entry in cfg['obstacles']:
        s = dict(entry)
        s['pos'] = np.array(entry['pos']) + offset
        if not s['fixed']:
            s['mass'] *= realized['structure_mass_scale']
        if s.get('breakable'):
            scale = realized['strength_scale']
            if s.get('load_bearing'):
                scale = max(scale, realized['structure_mass_scale'])
            s['fracture_threshold'] *= scale
        if s.get('breakable'):
            pane = build_fracturable(root, world, s)
            fractures.append(pane)
            names = [part['name'] for part in pane['fragments']]
        else:
            build_structure(root, world, s)
            names = [s['name']]
        scale_structure_contacts(world, names, realized['structure_friction_scale'])
        s['pos'] = s['pos'].tolist()
        (fixed if s['fixed'] else blocks).append(s)
    targets = []
    for (i, xyz) in enumerate(cfg['targets']):
        pos = (np.array(xyz) + offset).tolist()
        name = f'target{i}'
        old_radius = 0.058 if scenario == 'domino_fork' else 0.065
        size_name = realized['target_types'][i]
        radius = old_radius * 0.8 if size_name == 'standard' else TARGET_TYPES[size_name]['radius'] * (old_radius / 0.065)
        pos[2] -= old_radius - radius
        body = add(world, 'body', name=name, pos=vec(pos))
        pig(body, name, radius, size_name=size_name)
        if i in cfg.get('protected', []) or cfg.get('target_order'):
            from .appearance import target_rule_marker
            rank = cfg.get('target_order', []).index(i) + 1 if i in cfg.get('target_order', []) else None
            target_rule_marker(body, name, radius, protected=i in cfg.get('protected', []), rank=rank)
        threshold = cfg.get('thresholds', [0.018] * len(cfg['targets']))[i] if size_name == 'standard' else TARGET_TYPES[size_name]['impulse_threshold']
        threshold *= realized['strength_scale']
        targets.append(dict(name=name, pos=pos, radius=radius, impulse_threshold=threshold, size_name=size_name, size_code=TARGET_TYPES[size_name]['code']))
    rack_positions = [[0.37, -0.23], [0.29, -0.29], [0.44, -0.3], [0.31, -0.47]]
    ammo = []
    for (i, kind) in enumerate(cfg['ammo']):
        a = AMMO[kind]
        name = 'marble' if i == 0 else f'ammo{i}'
        joint = 'marble_free' if i == 0 else name + '_free'
        latch = 'loaded_latch' if i == 0 else name + '_latch'
        if i == 0:
            body = world.find("body[@name='marble']")
            if mode == 'ground':
                body.set('pos', vec([0.37 + rng.uniform(-0.003, 0.003), -0.65 + rng.uniform(-0.003, 0.003), a['z']]))
            geom = body.find('geom')
        else:
            xy = np.array(rack_positions[i]) + rng.uniform(-0.003, 0.003, 2)
            holder_name = f'fixed_ammo_holder{i}'
            holder = add(world, 'body', name=holder_name, pos=vec([*xy, 0]))
            add(holder, 'geom', name=holder_name, type='box', size='.057 .057 .004', pos='0 0 .004', rgba='.29 .37 .48 1')
            for axis in (0, 1):
                for sign in (-1, 1):
                    pos = [0, 0, 0.014]
                    pos[axis] = sign * 0.061
                    size = [0.065, 0.065, 0.006]
                    size[axis] = 0.004
                    add(holder, 'geom', type='box', pos=vec(pos), size=vec(size), rgba='.29 .37 .48 1')
            fixed_detail(holder, [0.065, 0.065, 0.02])
            fixed.append(dict(name=holder_name, pos=[*xy, 0], size=[0.065, 0.065, 0.02], fixed=True, role='ammo_holder', material='stone', shape='box', angle=0.0))
            body = add(world, 'body', name=name, pos=vec([*xy, a['z'] + 0.008]))
            add(body, 'freejoint', name=joint)
            geom = add(body, 'geom', name=name)
            add(root.find('equality'), 'weld', name=latch, body1='carriage', body2=name, relpose='0 0 .025 1 0 0 0', active='false', solref='.002 1')
        geom.attrib.update(type=a['type'], size=vec(a['size']), mass=str(a['mass']), rgba=vec(a['color']), friction='1.2 .005 .001')
        if kind == 'capsule':
            geom.set('condim', '6')
            geom.set('friction', '1.2 .005 .002')
        build_projectile_geometry(root, body, geom, kind, name)
        shot_detail(body, kind)
        ammo.append(dict(name=name, joint=joint, latch=latch, kind=kind, mass=a['mass']))
    realized['background'] = apply_background(root, background, np.random.default_rng(realized['visual_seed']))
    realized['background']['motion'] = background_motion
    spec.update(blocks=blocks, fixed=fixed, targets=targets, target=targets[0]['pos'], variant=variant, ammo=ammo, scenario=scenario, description=cfg['description'], tier=cfg['tier'], stage=cfg['stage'], fractures=fractures, observation_schema_version=OBSERVATION_SCHEMA_VERSION)
    if sum((len(f['fragments']) for f in fractures)) > MAX_FRAGMENTS:
        raise ValueError('Scene exceeds fragment observation capacity')
    if len(targets) > MAX_TARGETS or len(ammo) > MAX_AMMO or len(blocks) > MAX_BLOCKS or (len(fixed) > MAX_FIXED):
        raise ValueError('Scene exceeds logical-object observation capacity')
    configuration = configure_launcher(root, positions, spring_stiffness=spring_stiffness, launcher_offset_m=launcher_offset_m, ammunition_offset_m=ammunition_offset_m)
    apply_positions(root, spec, positions, mode)
    configuration['realized'].update(launcher_anchor_m=list(spec['launcher_anchor']), ammunition_positions_m=dict(positions['realized']['ammunition_positions_m']))
    spec['launcher_configuration'] = configuration
    return (ET.tostring(root, encoding='unicode'), spec)
