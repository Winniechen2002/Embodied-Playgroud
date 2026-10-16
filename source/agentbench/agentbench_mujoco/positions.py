"""Reset-only position distributions, independent of appearance and materials.

Assemblies move before compilation so joints, spring reference positions and
world-anchored fracture bonds retain their physical meaning. No success-based
rejection, runtime teleportation, or changes to robot bases are used.
"""
import numpy as np
from .variants import derived_seed

POSITION_RANDOMIZATIONS = ('off', 'train', 'heldout')
POSITION_DISTRIBUTION_VERSION = 1


def validate_position_randomization(mode):
    if mode not in POSITION_RANDOMIZATIONS:
        raise ValueError('Unknown position_randomization; expected off/train/heldout')


def sample_positions(rng, mode, target_count, target_x_directions=None):
    validate_position_randomization(mode)
    directions = [0] * target_count if target_x_directions is None else list(target_x_directions)
    if len(directions) != target_count or any(value not in (-1, 0, 1) for value in directions):
        raise ValueError('Each target needs an authored X direction: -1, 0, or 1')
    seed = derived_seed(rng, 'scene-positions-v1:')
    component_seeds = {}
    # Separate streams mean adding pigs cannot move the launcher or ammo rack.
    def stream(name):
        component_seeds[name] = derived_seed(rng, 'scene-positions-v1:' + name)
        return np.random.default_rng(component_seeds[name])

    launcher_rng, layout_rng = stream('launcher'), stream('target-layout')
    pig_rng, ammo_rng = stream('individual-pigs'), stream('ammunition')

    def offset(random, train, heldout):
        if mode == 'off':
            return np.zeros(3)
        if mode == 'train':
            return np.array([random.uniform(-bound, bound) if bound else 0.
                             for bound in train])
        return np.array([float(random.uniform(*bounds)) * (1 if random.integers(2) else -1)
                         if bounds[1] else 0. for bounds in heldout])

    launcher = offset(launcher_rng, (.025, .015, 0), ((.035, .050), (.025, .035), (0, 0)))
    layout = offset(layout_rng, (.040, .006, 0), ((.060, .090), (.008, .012), (0, 0)))
    # There is elevation control but no yaw. Keep the stage in the launcher's
    # lateral corridor, while retaining a separately sampled lateral residual.
    layout[1] += launcher[1]
    individual = [offset(pig_rng, (.008, 0, 0), ((.012, .020), (0, 0), (0, 0))).tolist()
                  for _ in range(target_count)]
    # Authored clearance constraints are applied to the distribution itself,
    # never by testing a sampled policy or moving objects after simulation.
    for delta, direction in zip(individual, directions):
        if direction:
            delta[0] = abs(delta[0]) * direction
    ammo = offset(ammo_rng, (.010, .008, 0), ((.015, .022), (.012, .018), (0, 0)))
    return dict(requested=mode, distribution_version=POSITION_DISTRIBUTION_VERSION,
                realized=dict(seed=seed, component_seeds=component_seeds, launcher_offset_m=launcher.tolist(),
                              target_layout_offset_m=layout.tolist(),
                              target_individual_offsets_m=individual,
                              target_x_directions=directions,
                              ammunition_offset_m=ammo.tolist()))


def _vec(values):
    return ' '.join(str(float(v)) for v in values)


def _translate(element, delta):
    if element is None:
        raise ValueError('Position randomization references a missing scene element')
    if not np.any(delta):
        return
    if 'fromto' in element.attrib:
        points = np.fromstring(element.get('fromto'), sep=' ').reshape(2, 3)
        element.set('fromto', _vec((points + delta).ravel()))
    else:
        element.set('pos', _vec(np.fromstring(element.get('pos', '0 0 0'), sep=' ') + delta))


def apply_positions(root, spec, sampled, initial_mode):
    """Move explicit scene objects once; synchronize evaluator metadata."""
    from .scene import LAUNCH_ORIGIN
    world = root.find('worldbody')
    values = sampled['realized']
    launcher = np.asarray(values['launcher_offset_m'])
    layout = np.asarray(values['target_layout_offset_m'])
    ammunition = np.asarray(values['ammunition_offset_m'])
    pivot = world.find("body[@name='yaw_turntable']")
    if pivot is None:
        pivot = world.find("body[@name='elevation']")
    if pivot is None:
        pivot = world.find("body[@name='carriage']")
    _translate(pivot, launcher)
    for geom in world.findall('geom'):
        if geom.get('name', '').startswith('launcher_') or geom.get('name') == 'axle_stand':
            _translate(geom, launcher)

    # Every shard is a world child, including anchored panels. Move all pieces
    # before MuJoCo compiles the new default relative poses for their welds.
    moved = set()
    for pane in spec.get('fractures', []):
        for fragment in pane['fragments']:
            name = fragment['name']
            _translate(world.find(f"body[@name='{name}']"), layout)
            moved.add(name)
        pane['pos'] = (np.asarray(pane['pos']) + layout).tolist()
    for entry in spec.get('blocks', []) + spec.get('fixed', []):
        delta = ammunition if entry.get('role') == 'ammo_holder' else layout
        if entry['name'] not in moved:
            _translate(world.find(f"body[@name='{entry['name']}']"), delta)
        entry['pos'] = (np.asarray(entry['pos']) + delta).tolist()

    targets = spec.get('targets', [dict(name='target0', pos=spec['target'])])
    for target, individual in zip(targets, values['target_individual_offsets_m']):
        delta = layout + individual
        _translate(world.find(f"body[@name='{target['name']}']"), delta)
        target['pos'] = (np.asarray(target['pos']) + delta).tolist()
    spec['target'] = list(targets[0]['pos'])
    for index, ammo in enumerate(spec.get('ammo', [dict(name='marble')])):
        delta = launcher if index == 0 and initial_mode == 'loaded' else ammunition
        _translate(world.find(f"body[@name='{ammo['name']}']"), delta)
    spec['ball_spawn'] = np.fromstring(world.find("body[@name='marble']").get('pos'), sep=' ').tolist()
    spec['launcher_anchor'] = (LAUNCH_ORIGIN + launcher).tolist()
    values['launcher_anchor_m'] = list(spec['launcher_anchor'])
    values['target_positions_m'] = [list(t['pos']) for t in targets]
    values['ammunition_positions_m'] = {
        ammo['name']: np.fromstring(world.find(f"body[@name='{ammo['name']}']").get('pos'), sep=' ').tolist()
        for ammo in spec.get('ammo', [dict(name='marble')])}
    spec['position_randomization'] = sampled
