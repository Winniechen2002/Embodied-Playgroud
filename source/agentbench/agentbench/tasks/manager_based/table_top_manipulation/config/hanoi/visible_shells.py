"""Evaluator-only convex visible-envelope penetration checks (no Isaac imports).

Unlike a whole-ring bounding box, one convex piece per visible ring sector
preserves the hole. SAT includes edge/edge axes, so crossed thin parts are
detected even when neither mesh has a vertex inside the other.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np
from scipy.spatial import ConvexHull


def _hpp_geometry(shell):
    # hpp-fcl is the locally installed collision dependency of Pinocchio.
    import hppfcl
    points = hppfcl.StdVec_Vec3f()
    for point in shell.vertices:
        points.append(point)
    return hppfcl.Convex.convexHull(points, True, 'Qt')


def _hpp_penetration(a, transform_a, b, transform_b):
    import hppfcl
    request = hppfcl.CollisionRequest(hppfcl.CONTACT, 1)
    request.gjk_tolerance = 1e-10
    request.gjk_max_iterations = 1000
    result = hppfcl.CollisionResult()
    hppfcl.collide(a, hppfcl.Transform3f(transform_a[:3, :3], transform_a[:3, 3]),
                  b, hppfcl.Transform3f(transform_b[:3, :3], transform_b[:3, 3]), request, result)
    if not result.isCollision():
        return 0.0
    if not result.numContacts():
        raise RuntimeError('Convex collision solver returned no penetration witness')
    depth = float(result.getContact(0).penetration_depth)
    # hpp-fcl 2.x uses DBL_MAX for EPA non-convergence, not a valid depth.
    if not np.isfinite(depth) or abs(depth) > 1e100:
        raise RuntimeError('Convex penetration solver did not converge')
    return max(0.0, depth)


# Task policy, deliberately independent of PhysX contact/rest offsets.
# Source: Pocket Cube Hard Task Rule 9 originally specified 0.25 mm.
# User raised Hanoi to 2 mm on 2026-09-16, then 5 mm on 2026-09-23.
# Shared robot policy: env/hanoi_task.md#penetration-scoring.
MAX_VISIBLE_SHELL_PENETRATION = 0.005

# User-authorized scoring scope and fixed installation exceptions (2026-09-16).
# These exclusions do not alter physical collisions or fixed-pose fingerprints.
PENETRATION_SCOPE = 'robot_object_only'
FIXED_INSTALLATION_EXCLUSIONS = (
    ('robot/panda_link0', 'table'),
    ('robot/panda_link0', 'hanoi_base'),
)


def _directions(vectors: np.ndarray) -> np.ndarray:
    lengths = np.linalg.norm(vectors, axis=1)
    vectors = vectors[lengths > 1e-10] / lengths[lengths > 1e-10, None]
    if not len(vectors):
        return vectors.reshape(0, 3)
    # Parallel and antiparallel axes are equivalent in SAT.
    pivot = np.argmax(np.abs(vectors), axis=1)
    vectors *= np.where(vectors[np.arange(len(vectors)), pivot] < 0, -1, 1)[:, None]
    _, indices = np.unique(np.round(vectors, 10), axis=0, return_index=True)
    return vectors[np.sort(indices)]


def _rigid_transform(transform):
    transform = np.asarray(transform, dtype=np.float64)
    if transform.shape != (4, 4) or not np.isfinite(transform).all():
        raise ValueError('Invalid body transform')
    rotation = transform[:3, :3]
    if not np.allclose(rotation.T @ rotation, np.eye(3), atol=1e-5):
        raise ValueError('Body transforms must be rigid; bake mesh scale into vertices')
    return transform


@dataclass(frozen=True)
class ConvexShell:
    owner: str
    name: str
    vertices: np.ndarray
    normals: np.ndarray
    edges: np.ndarray

    @classmethod
    def from_points(cls, owner: str, name: str, points) -> 'ConvexShell':
        points = np.unique(np.asarray(points, dtype=np.float64), axis=0)
        if points.ndim != 2 or points.shape[1] != 3 or not np.isfinite(points).all():
            raise ValueError('Invalid visible-shell vertices')
        hull = ConvexHull(points)
        edges = np.concatenate([hull.simplices[:, [0, 1]], hull.simplices[:, [1, 2]],
                                hull.simplices[:, [2, 0]]])
        return cls(owner, name, points[hull.vertices], _directions(hull.equations[:, :3]),
                   _directions(points[edges[:, 1]] - points[edges[:, 0]]))

    def at(self, transform: np.ndarray) -> 'ConvexShell':
        return self._at_rigid(_rigid_transform(transform))

    def _at_rigid(self, transform):
        """Internal path: the owner transform has already been validated."""
        rotation = transform[:3, :3]
        return ConvexShell(self.owner, self.name, self.vertices @ rotation.T + transform[:3, 3],
                           self.normals @ rotation.T, self.edges @ rotation.T)


def convex_penetration(a: ConvexShell, b: ConvexShell) -> float:
    """Minimum separating translation along polytope SAT axes, in metres.

    Uses directed interval separation, including containment (an inner body
    cannot be separated by moving only its own width).
    """
    if len(a.edges) * len(b.edges) > 4096:
        return _hpp_penetration(_hpp_geometry(a), np.eye(4), _hpp_geometry(b), np.eye(4))
    axes = _directions(np.concatenate([a.normals, b.normals,
        np.cross(a.edges[:, None, :], b.edges[None, :, :]).reshape(-1, 3)]))
    left = a.vertices @ axes.T
    right = b.vertices @ axes.T
    overlap = np.minimum(left.max(0) - right.min(0), right.max(0) - left.min(0))
    return max(0.0, float(overlap.min()))


def visible_vertex_intrusion(a: ConvexShell, b: ConvexShell) -> float:
    """Diagnostic witness: original visible vertices of A inside B's envelope.

    Hull vertices are a subset of source mesh vertices. This is supplementary
    evidence, never a replacement for SAT/GJK (crossed edges may have none).
    """
    planes = ConvexHull(b.vertices).equations
    inward = -(a.vertices @ planes[:, :3].T + planes[:, 3])
    return max(0.0, float(inward.min(axis=1).max()))


class VisibleShellAudit:
    def __init__(self, shells: list[ConvexShell], excluded_owner_pairs=FIXED_INSTALLATION_EXCLUSIONS):
        if not shells:
            raise ValueError('Cannot evaluate an empty visible-shell manifest')
        self.shells = tuple(shells)
        self.owners = frozenset(shell.owner for shell in shells)
        exclusions = {frozenset(pair) for pair in excluded_owner_pairs}
        self.pairs = tuple((i, j) for i, j in combinations(range(len(shells)), 2)
                           if shells[i].owner.startswith('robot/') != shells[j].owner.startswith('robot/')
                           and frozenset((shells[i].owner, shells[j].owner)) not in exclusions)
        if not self.pairs:
            raise ValueError('No robot-object shell pairs are covered')
        self._hpp = {}
        self._pair_indices = np.asarray(self.pairs)
        self._owner_indices = {owner: tuple(i for i, shell in enumerate(self.shells)
                                            if shell.owner == owner) for owner in self.owners}
        self._transforms = {}
        self._world = [None] * len(self.shells)
        self._mins = np.empty((len(self.shells), 3))
        self._maxs = np.empty((len(self.shells), 3))

    def measure(self, transforms: dict[str, np.ndarray]) -> dict:
        if not self.owners.issubset(transforms):
            raise ValueError('Missing evaluator body transforms')
        for owner, indices in self._owner_indices.items():
            transform = np.asarray(transforms[owner], dtype=np.float64)
            if owner in self._transforms and np.array_equal(transform, self._transforms[owner]):
                continue
            transform = _rigid_transform(transform)
            for index in indices:
                shell = self.shells[index]._at_rigid(transform)
                self._world[index] = shell
                self._mins[index] = shell.vertices.min(0)
                self._maxs[index] = shell.vertices.max(0)
            # Copy: simulator callers may update an existing matrix in place.
            self._transforms[owner] = transform.copy()
        world, mins, maxs = self._world, self._mins, self._maxs
        pairs = self._pair_indices
        i, j = pairs.T
        bounds = np.minimum(maxs[i] - mins[j], maxs[j] - mins[i]).min(1)
        candidates = pairs[bounds > 0]
        max_depth, deepest_indices = 0.0, None
        for i, j in candidates:
            if len(world[i].edges) * len(world[j].edges) > 4096:
                for index in (i, j):
                    if index not in self._hpp:
                        self._hpp[index] = _hpp_geometry(self.shells[index])
                depth = _hpp_penetration(self._hpp[i], transforms[world[i].owner],
                                        self._hpp[j], transforms[world[j].owner])
            else:
                depth = convex_penetration(world[i], world[j])
            if depth > max_depth:
                max_depth = depth
                deepest_indices = (i, j)
        deepest = None
        if deepest_indices is not None:
            i, j = deepest_indices
            deepest = {'object_a': world[i].owner, 'object_b': world[j].owner,
                       'shell_a': world[i].name, 'shell_b': world[j].name,
                       'source_visible_vertex_intrusion_m': visible_vertex_intrusion(world[i], world[j])}
        return {'penetration_depth_m': max_depth, 'pair': deepest,
                'covered_pairs': len(self.pairs), 'narrow_phase_pairs': len(candidates)}
