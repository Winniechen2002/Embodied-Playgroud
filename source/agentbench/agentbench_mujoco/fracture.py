"""Prefragmented rigid glass with an explicitly authored impulse break rule.

This is not a continuum stress/fracture solver. Six convex triangular prisms
exactly partition each rectangular pane. Weld equalities make the pieces move
together until permitted external contact exceeds an impulse threshold. At
failure its welds deactivate and its fragments' mutual collisions activate.
No bodies spawn and no poses, velocities, masses or applied forces are changed.
"""
from collections import deque
import xml.etree.ElementTree as ET

import numpy as np

from .structures import MATERIALS


def _vec(values):
    return ' '.join(str(float(v)) for v in np.asarray(values).ravel())


def build_fracturable(root, world, spec):
    """Append a six-piece glass box and return serializable fracture metadata.

    ``size`` is the unbroken pane's local bounding half-extents, ``angle`` is
    rotation about local/world Y in degrees (the scene compiler uses radians).
    The first fragment keeps ``spec['name']`` and every fragment keeps the same
    authored body frame. Mesh centering is left to MuJoCo's compiler; mass and
    inertia are inferred from each actual convex collision mesh.

    ``anchored`` means an initially world-welded, breakable pane. It is distinct
    from ordinary immutable fixed terrain. Its world weld breaks with the pane.
    """
    name = spec['name']
    if spec.get('shape', 'box') != 'box':
        raise ValueError('Fracturable glass currently supports box panes only')
    if spec.get('material', 'glass') != 'glass':
        raise ValueError('Fracturable panes must use the glass material')
    half = np.asarray(spec['size'], dtype=float)
    position = np.asarray(spec['pos'], dtype=float)
    mass = float(spec['mass'])
    threshold = float(spec.get('fracture_threshold', .025))
    window = float(spec.get('fracture_window', .03))
    angle = float(spec.get('angle', 0.))
    if (half.shape != (3,) or position.shape != (3,) or
            not np.isfinite(np.r_[half, position, mass, threshold, window, angle]).all()
            or min(half) <= 0 or mass <= 0 or threshold <= 0 or window <= 0):
        raise ValueError('Pane geometry, mass, threshold and window must be finite and positive')
    # Flat convex mesh faces need a distributed contact patch to support a roof.
    # The default single mesh contact lets narrow panes rock/slip under load.
    # Only scenes that actually contain fracture geometry opt into multi-CCD.
    option = root.find('option')
    if option is None:
        option = ET.SubElement(root, 'option')
    flag = option.find('flag')
    if flag is None:
        flag = ET.SubElement(option, 'flag')
    flag.set('multiccd', 'enable')
    assets = root.find('asset')
    if assets is None:
        assets = ET.SubElement(root, 'asset')
    equality = root.find('equality')
    if equality is None:
        equality = ET.SubElement(root, 'equality')
    # Distinct pane bits suppress only bonded siblings' internal contacts, whose
    # numerical compliance would otherwise fight welds under a heavy roof. The
    # base scene uses bit 1; cross-pane collisions retain all other pane bits.
    pane_index = sum(mesh.get('name', '').endswith('_fracture_mesh')
                     for mesh in assets.findall('mesh')) // 6
    if pane_index >= 30:
        raise ValueError('At most 30 collision-distinct fracture panes are supported')
    collision_bit = 1 << (pane_index + 1)
    collision_mask = (1 << 31) - 1
    hx, hy, hz = half
    fragments, bonds = [], []
    # Alternate diagonals avoid six visually identical slivers. Triangles have
    # equal area, so equal masses preserve uniform density exactly.
    for row in range(3):
        lo, hi = -hz + 2 * hz * row / 3, -hz + 2 * hz * (row + 1) / 3
        a, b, c, d = (-hy, lo), (hy, lo), (hy, hi), (-hy, hi)
        triangles = ((a, b, c), (a, c, d)) if row % 2 == 0 else ((a, b, d), (b, c, d))
        for triangle in triangles:
            index = len(fragments)
            fragment_name = name if index == 0 else f'{name}_frag{index}'
            vertices = [[x, y, z] for x in (-hx, hx) for y, z in triangle]
            mesh_name = f'{fragment_name}_fracture_mesh'
            ET.SubElement(assets, 'mesh', name=mesh_name, vertex=_vec(vertices))
            body = ET.SubElement(world, 'body', name=fragment_name,
                                 pos=_vec(position), euler=_vec([0, np.deg2rad(angle), 0]))
            ET.SubElement(body, 'freejoint', name=fragment_name + '_free')
            attrs = dict(MATERIALS['glass'])
            # Always use actual glass collision parameters. Use the project's
            # artwork only if its material has already been installed.
            if any(m.get('name') == 'glass_mat' for m in assets.findall('material')):
                attrs.update(material='glass_mat', rgba='1 1 1 1')
            ET.SubElement(body, 'geom', name=fragment_name, type='mesh',
                          mesh=mesh_name, mass=str(mass / 6), margin='0', gap='0',
                          contype=str(collision_bit),
                          conaffinity=str(collision_mask & ~collision_bit), **attrs)
            fragments.append(dict(name=fragment_name, parent=name, mass=mass / 6,
                                  local_vertices=vertices))
            if index:
                bond_name = f'{name}_bond{index}'
                ET.SubElement(equality, 'weld', name=bond_name, body1=name,
                              body2=fragment_name, solref='.002 1', solimp='.9999 .99999 .0001')
                bonds.append(bond_name)
    anchored = bool(spec.get('anchored', False))
    if anchored:
        bond_name = name + '_anchor'
        ET.SubElement(equality, 'weld', name=bond_name, body1=name,
                      solref='.002 1', solimp='.9999 .99999 .0001')
        bonds.append(bond_name)
    return dict(parent=name, fragments=fragments, bonds=bonds,
                threshold_Ns=threshold, window_s=window, anchored=anchored,
                collision_bit=collision_bit, collision_mask=collision_mask,
                mass=mass, size=half.tolist(), pos=position.tolist(), angle=angle)


class FractureSystem:
    """One environment's reset-local pane state and contact impulse windows.

    Call ``update`` once after each physics step. Caller selects permitted
    sources, such as fired ammunition and dynamic structures/fragments, by body
    ID. Floor, robot and stationary launcher forces need not damage the panes.
    The environment must own its MjModel (campaign resets compile a fresh one).
    Release changes only its shard geoms' conaffinity and the corresponding body
    broad-phase cache, in addition to equality states. Reset restores these
    owned masks; sharing one model between asynchronous episodes is unsupported.
    """

    def __init__(self, env):
        self.env, self.model, self.data = env, env.model, env.data
        self.specs = tuple(env.scene_spec.get('fractures', ()))
        self.by_parent = {s['parent']: s for s in self.specs}
        if len(self.by_parent) != len(self.specs):
            raise ValueError('Fracture parent names must be unique')
        self.parent_by_body = {}
        self.bond_ids = {}
        self.geom_ids = {}
        for spec in self.specs:
            parent = spec['parent']
            for fragment in spec['fragments']:
                body_id = int(self.model.body(fragment['name']).id)
                if body_id in self.parent_by_body:
                    raise ValueError('A fragment cannot belong to multiple panes')
                self.parent_by_body[body_id] = parent
            self.bond_ids[parent] = np.array(
                [self.model.equality(name).id for name in spec['bonds']], dtype=int)
            self.geom_ids[parent] = np.array(
                [self.model.geom(fragment['name']).id for fragment in spec['fragments']], dtype=int)
        self.fragment_ids = tuple(self.parent_by_body)
        self.reset()

    def reset(self):
        """Clear local records and restore owned bonds, without moving bodies.

        This belongs after ``mj_resetData`` or scene reconstruction, not midway
        through an episode: re-welding scattered fragments is not a repair tool.
        """
        self.broken = set()
        self.events = []
        self.windows = {p: deque() for p in self.by_parent}
        self.peak_impulse = {p: 0. for p in self.by_parent}
        self.last_impulse = {p: 0. for p in self.by_parent}
        self.last_update_time = None
        for ids in self.bond_ids.values():
            self.data.eq_active[ids] = self.model.eq_active0[ids]
        for parent, spec in self.by_parent.items():
            self.model.geom_conaffinity[self.geom_ids[parent]] = spec['collision_mask'] & ~spec['collision_bit']
        self._refresh_body_collision_masks()

    def _refresh_body_collision_masks(self):
        # MuJoCo's broad phase reads the per-body OR cache, not only geom masks.
        for body in self.fragment_ids:
            geoms = self.model.geom_bodyid == body
            self.model.body_conaffinity[body] = np.bitwise_or.reduce(self.model.geom_conaffinity[geoms])

    def update(self, allowed_bodies):
        """Accumulate real external contact impulse and return new break events."""
        if not self.specs:
            return []
        import mujoco as mj
        m, d = self.model, self.data
        now = float(d.time)
        # An accidental duplicate call must not count the same solver impulse
        # twice. A backwards clock requires an explicit environment reset.
        if self.last_update_time is not None:
            if now < self.last_update_time:
                raise RuntimeError('FractureSystem must be reset with the environment')
            if now == self.last_update_time:
                return []
        self.last_update_time = now
        allowed = set(int(b) for b in allowed_bodies)
        impulse = {p: 0. for p in self.by_parent if p not in self.broken}
        sources = {p: set() for p in impulse}
        force = np.zeros(6)
        dt = float(self.env.physics_dt)
        for index in range(d.ncon):
            contact = d.contact[index]
            a, b = int(m.geom_bodyid[contact.geom1]), int(m.geom_bodyid[contact.geom2])
            pa, pb = self.parent_by_body.get(a), self.parent_by_body.get(b)
            if pa == pb:  # Also cheaply ignores contacts involving no pane.
                continue
            affected = []
            if pa in impulse and b in allowed:
                affected.append((pa, b))
            if pb in impulse and a in allowed:
                affected.append((pb, a))
            if not affected:
                continue
            mj.mj_contactForce(m, d, index, force)
            normal_impulse = max(0., float(force[0])) * dt
            if normal_impulse <= 0:
                continue
            for parent, source in affected:
                impulse[parent] += normal_impulse
                sources[parent].add(source)
        new_events = []
        for parent, value in impulse.items():
            spec, window = self.by_parent[parent], self.windows[parent]
            window.append((now, value, sources[parent]))
            # Half-open integration interval prevents an extra dt at the edge.
            while window and window[0][0] <= now - spec['window_s'] + 1e-12:
                window.popleft()
            total = sum(sample[1] for sample in window)
            self.last_impulse[parent] = total
            self.peak_impulse[parent] = max(self.peak_impulse[parent], total)
            if total < spec['threshold_Ns']:
                continue
            self.data.eq_active[self.bond_ids[parent]] = False
            self.model.geom_conaffinity[self.geom_ids[parent]] |= spec['collision_bit']
            self._refresh_body_collision_masks()
            self.broken.add(parent)
            source_ids = sorted(set().union(*(sample[2] for sample in window)))
            event = dict(kind='fracture', time=now, parent=parent,
                         impulse_Ns=float(total), threshold_Ns=spec['threshold_Ns'],
                         fragments=len(spec['fragments']), anchored=spec['anchored'],
                         sources=[mj.mj_id2name(m, mj.mjtObj.mjOBJ_BODY, b) for b in source_ids])
            self.events.append(event)
            if hasattr(self.env, 'events'):
                self.env.events.append(event)
            new_events.append(event)
        return new_events

    def snapshot(self):
        """JSON-safe logical-pane status; no hidden fragment poses are exposed."""
        return [dict(parent=p, broken=p in self.broken,
                     threshold_Ns=s['threshold_Ns'], window_s=s['window_s'],
                     window_impulse_Ns=float(self.last_impulse[p]),
                     peak_impulse_Ns=float(self.peak_impulse[p]),
                     fragment_count=len(s['fragments']), anchored=s['anchored'])
                for p, s in self.by_parent.items()]
