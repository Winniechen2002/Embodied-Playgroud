"""Trusted Isaac adapter. Never import this module into a Level 1/2 planner."""
from __future__ import annotations

import itertools

import numpy as np
from pxr import Usd, UsdGeom, UsdPhysics
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial.transform import Rotation

from .hanoi_rules import RING_SPECS
from .private_evaluator import PrivateHanoiEvaluator, run_physics_substeps
from .scene_fingerprint import SceneFingerprintCache
from .visible_shells import (ConvexShell, VisibleShellAudit,
                            FIXED_INSTALLATION_EXCLUSIONS, PENETRATION_SCOPE)
from .vision_env import HanoiVisionEnv


def pose_matrix(position, quaternion):
    result = np.eye(4)
    result[:3, :3] = Rotation.from_quat(np.asarray(quaternion)[[1, 2, 3, 0]]).as_matrix()
    result[:3, 3] = position
    return result


def _mesh_components(mesh):
    points = np.asarray(mesh.GetPointsAttr().Get(), dtype=np.float64)
    counts = mesh.GetFaceVertexCountsAttr().Get()
    indices = np.asarray(mesh.GetFaceVertexIndicesAttr().Get(), dtype=np.int64)
    # USD exporters often duplicate vertices at normal/material seams. Weld
    # identical positions before finding components, so a closed mesh does not
    # become a collection of zero-volume individual triangles.
    points, welded = np.unique(points, axis=0, return_inverse=True)
    indices = welded[indices]
    edges, offset = [], 0
    for count in counts:
        polygon = indices[offset:offset + count]
        edges.extend(zip(polygon, np.roll(polygon, -1)))
        offset += count
    if offset != len(indices) or not edges:
        raise ValueError('Invalid visible mesh topology')
    edges = np.asarray(edges)
    graph = coo_matrix((np.ones(len(edges)), (edges[:, 0], edges[:, 1])),
                       shape=(len(points), len(points)))
    count, labels = connected_components(graph, directed=False)
    return [points[labels == index] for index in range(count)]


def _primitive_points(prim):
    if prim.IsA(UsdGeom.Mesh):
        return _mesh_components(UsdGeom.Mesh(prim))
    if prim.IsA(UsdGeom.Cube):
        half = float(UsdGeom.Cube(prim).GetSizeAttr().Get()) / 2
        return [np.array(list(itertools.product((-half, half), repeat=3)))]
    if prim.IsA(UsdGeom.Cylinder):
        cylinder = UsdGeom.Cylinder(prim)
        # Declared circumscribed 128-sided envelope, independent of PhysX.
        radius = float(cylinder.GetRadiusAttr().Get()) / np.cos(np.pi / 128)
        half = float(cylinder.GetHeightAttr().Get()) / 2
        angles = (np.arange(128) + 0.5) * (2 * np.pi / 128)
        points = np.array([(radius * np.cos(a), radius * np.sin(a), z)
                           for z in (-half, half) for a in angles])
        axis = str(cylinder.GetAxisAttr().Get())
        if axis == 'X':
            points = points[:, [2, 0, 1]]
        elif axis == 'Y':
            points = points[:, [0, 2, 1]]
        return [points]
    raise ValueError(f'Unsupported visible shell type: {prim.GetTypeName()}')


class IsaacHanoiAudit:
    """Read-only private scene snapshot and visible-envelope adapter."""
    def __init__(self, env):
        self.env = env
        self.stage = env.scene.stage
        self.root = '/World/envs/env_0'
        self.robot = env.scene['robot']
        self.body_paths = {}
        self.dynamic = {}
        self.static = {}
        robot_root = self.stage.GetPrimAtPath(self.root + '/Robot')
        for index, name in enumerate(self.robot.body_names):
            matches = [p for p in Usd.PrimRange(robot_root, Usd.TraverseInstanceProxies())
                       if p.GetName() == name and p.HasAPI(UsdPhysics.RigidBodyAPI)]
            if len(matches) != 1:
                raise RuntimeError(f'Cannot uniquely map robot body {name}')
            owner = 'robot/' + name
            self.body_paths[str(matches[0].GetPath())] = owner
            self.dynamic[owner] = ('robot', index)
        for name in ('table', 'hanoi_base', *[spec['asset_name'] for spec in RING_SPECS.values()]):
            asset = env.scene[name]
            path = asset.root_physx_view.prim_paths[0]
            self.body_paths[path] = name
            if name.startswith('ring_'):
                self.dynamic[name] = (name, None)
            else:
                self.static[name] = path
        for name, prim_name in [('peg_left', 'PegLeft'), ('peg_middle', 'PegMiddle'), ('peg_right', 'PegRight')]:
            path = self.root + '/' + prim_name
            self.body_paths[path] = name
            self.static[name] = path

        cache = UsdGeom.XformCache()
        shells, coverage = [], []
        for prim in Usd.PrimRange(self.stage.GetPrimAtPath(self.root), Usd.TraverseInstanceProxies()):
            if not prim.IsA(UsdGeom.Gprim):
                continue
            imageable = UsdGeom.Imageable(prim)
            if imageable.ComputeVisibility() == UsdGeom.Tokens.invisible:
                continue
            if imageable.ComputePurpose() not in (UsdGeom.Tokens.default_, UsdGeom.Tokens.render):
                continue  # Guide/proxy geometry is not a rendered exterior.
            path = str(prim.GetPath())
            parent = prim
            while parent and str(parent.GetPath()) not in self.body_paths:
                parent = parent.GetParent()
            if not parent:
                raise RuntimeError(f'Unmapped visible geometry: {path}')
            owner = self.body_paths[str(parent.GetPath())]
            mesh_world = np.asarray(cache.GetLocalToWorldTransform(prim)).T
            body_world = np.asarray(cache.GetLocalToWorldTransform(parent)).T
            relative = np.linalg.inv(body_world) @ mesh_world
            components = _primitive_points(prim)
            for index, vertices in enumerate(components):
                points = vertices @ relative[:3, :3].T + relative[:3, 3]
                name = f'{path}#component{index}'
                if len(points) < 4 or np.linalg.matrix_rank(points - points.mean(0), tol=1e-10) < 3:
                    # E.g. the authored zero-thickness HandleFlange. Its volume
                    # is zero, so it cannot establish positive penetration.
                    coverage.append({'shell': name, 'owner': owner, 'status': 'zero_volume'})
                    continue
                shells.append(ConvexShell.from_points(owner, name, points))
                coverage.append({'shell': name, 'owner': owner, 'status': 'convex_envelope',
                                 'source': 'visible USD geometry', 'vertex_count': len(points)})

        required = set(self.dynamic) | set(self.static)
        missing = required - {shell.owner for shell in shells}
        if missing:
            raise RuntimeError(f'Visible-shell coverage incomplete: {sorted(missing)}')
        exclusions = FIXED_INSTALLATION_EXCLUSIONS
        self.shells = VisibleShellAudit(shells, exclusions)
        self.manifest = {'shells': coverage, 'excluded_owner_pairs': exclusions,
                         'penetration_scope': PENETRATION_SCOPE,
                         'excluded_pair_categories': ['object_object', 'robot_robot'],
                         'installation_exception_source': 'env/franka_hanoi/task.md#penetration-check-scope',
                         'covered_piece_pairs': len(self.shells.pairs)}
        self._fingerprint_cache = SceneFingerprintCache(
            self.stage, self._prims, self._include_fingerprint_attribute)

    def _prims(self):
        yield from Usd.PrimRange(self.stage.GetPrimAtPath(self.root), Usd.TraverseInstanceProxies())
        camera = self.stage.GetPrimAtPath('/World/HanoiVisionAgentCamera')
        if not camera:
            raise RuntimeError('Declared Vision camera missing')
        yield camera
        for path in ('/World/skyLight', '/World/GroundPlane'):
            prim = self.stage.GetPrimAtPath(path)
            if not prim:
                raise RuntimeError('Fixed background geometry or lighting missing')
            yield from Usd.PrimRange(prim, Usd.TraverseInstanceProxies())
        for prim in self.stage.Traverse():
            if prim.IsA(UsdPhysics.Scene):
                yield prim

    def _include_fingerprint_attribute(self, path, name):
        owner = self.body_paths.get(path)
        dynamic_root = owner in self.dynamic and owner != 'robot/panda_link0'
        if name.startswith('state:') or (name.startswith('drive:') and
                name.endswith((':targetPosition', ':targetVelocity'))):
            return False
        return not (dynamic_root and (name in ('xformOp:translate', 'xformOp:orient',
                    'physics:velocity', 'physics:angularVelocity') or name.startswith('xformOp:rotate')))

    def fingerprint(self, live_fixed_transforms):
        return self._fingerprint_cache.fingerprint(repr(self.env.cfg), self.manifest,
                                                   live_fixed_transforms)

    def snapshot(self):
        transforms = {}
        positions = {}
        robot_positions = self.robot.data.body_link_pos_w[0].detach().cpu().numpy()
        robot_quats = self.robot.data.body_link_quat_w[0].detach().cpu().numpy()
        origin = self.env.scene.env_origins[0].detach().cpu().numpy()
        for owner, (asset_name, index) in self.dynamic.items():
            if asset_name == 'robot':
                pos, quat = robot_positions[index], robot_quats[index]
            else:
                asset = self.env.scene[asset_name]
                pos = asset.data.root_link_pos_w[0].detach().cpu().numpy()
                quat = asset.data.root_link_quat_w[0].detach().cpu().numpy()
                positions[asset_name] = (pos - origin).tolist()
            transforms[owner] = pose_matrix(pos, quat)
        cache = UsdGeom.XformCache()
        for owner, path in self.static.items():
            # Read live transforms so an external edit cannot reuse stale data.
            if owner in ('table', 'hanoi_base'):
                asset = self.env.scene[owner]
                transforms[owner] = pose_matrix(asset.data.root_link_pos_w[0].detach().cpu().numpy(),
                                               asset.data.root_link_quat_w[0].detach().cpu().numpy())
            else:
                transforms[owner] = np.asarray(cache.GetLocalToWorldTransform(self.stage.GetPrimAtPath(path))).T
        fixed = {owner: transforms[owner].tolist() for owner in (*self.static, 'robot/panda_link0')}
        snapshot = positions, self.fingerprint(fixed), self.shells.measure(transforms)
        self.last_snapshot = snapshot
        return snapshot


class EvaluatedHanoiVisionEnv(HanoiVisionEnv):
    """Single-use evaluation, private substep checks, unchanged action dynamics."""
    def __init__(self, *args, **kwargs):
        self._evaluation = None
        self._audit = None
        self._label = 'idle'
        self._reset_done = False
        super().__init__(*args, **kwargs)

    def reset(self, *args, **kwargs):
        if self._reset_done:
            raise RuntimeError('A new process and authorized attempt are required for reset')
        result = super().reset(*args, **kwargs)
        self._reset_done = True
        return result

    def reset_to(self, *args, **kwargs):
        raise RuntimeError('Direct state resets are not evaluation actions')

    def start_evaluation(self, target=None):
        if not self._reset_done or self._evaluation is not None:
            raise RuntimeError('Evaluation must start once, after reset and setup settling')
        self._audit = IsaacHanoiAudit(self)
        self._evaluation = PrivateHanoiEvaluator(*self._audit.snapshot(), target=target)
        self._evaluation.ensure_running()

    def step(self, action):
        if self._evaluation is None:
            return super().step(action)  # Trusted setup settling only.
        self._evaluation.ensure_running()
        self.action_manager.process_action(action.to(self.device))
        arm = self.action_manager.get_term('arm_action')
        targets = arm.processed_actions.detach().cpu().numpy()
        bounds = self.scene['robot'].data.joint_pos_limits[:, arm._joint_ids].detach().cpu().numpy()
        if (not np.isfinite(targets).all() or (targets < bounds[..., 0]).any()
                or (targets > bounds[..., 1]).any()):
            self._evaluation.abort('robot_joint_limit_command')
            self._evaluation.ensure_running()
        self.recorder_manager.record_pre_step()
        is_rendering = self.sim.has_gui() or self.sim.has_rtx_sensors()

        def substep():
            self._sim_step_counter += 1
            self.action_manager.apply_action()
            self.scene.write_data_to_sim()
            self.sim.step(render=False)
            self.scene.update(dt=self.physics_dt)

        def audit():
            self._evaluation.after_physics_step(*self._audit.snapshot(), label=self._label)
            if self._sim_step_counter % self.cfg.sim.render_interval == 0 and is_rendering:
                self.sim.render()

        run_physics_substeps(self.cfg.decimation, substep, audit)
        if 'interval' in self.event_manager.available_modes:
            self.event_manager.apply(mode='interval', dt=self.step_dt)
            # Interval events also cannot alter the fixed scene outside audit.
            self._evaluation._check(*self._audit.snapshot(), self._label + ':interval')
            self._evaluation.ensure_running()
        self.obs_buf = self.observation_manager.compute(update_history=True)
        self.recorder_manager.record_post_step()
        return self._add_rgb(self.obs_buf), {}  # Never export simulator extras.

    def finish_evaluation(self):
        if self._evaluation is None:
            raise RuntimeError('Evaluation was not initialized')
        snapshot_error = None
        try:
            snapshot = self._audit.snapshot()
        except Exception as error:
            # A later adapter error must not discard an earlier hard violation.
            self._evaluation.abort('terminal_snapshot_unavailable')
            snapshot = self._audit.last_snapshot
            snapshot_error = type(error).__name__
        result = self._evaluation.end_trajectory_and_disclose(*snapshot)
        if snapshot_error:
            result['terminal_snapshot_error'] = snapshot_error
        result['visible_shell_manifest'] = self._audit.manifest
        return result
