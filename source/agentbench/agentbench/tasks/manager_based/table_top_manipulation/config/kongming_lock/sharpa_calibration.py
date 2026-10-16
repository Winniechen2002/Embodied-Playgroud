"""Private, versioned mount geometry and read-only native preflight."""
import hashlib
import json
from itertools import product
from pathlib import Path

import numpy as np

PRESET_PATH = Path(__file__).with_name('dual_sharpa_mount_v1.json')
PRESET = json.loads(PRESET_PATH.read_text())
PRESET_SHA256 = hashlib.sha256(PRESET_PATH.read_bytes()).hexdigest()
NON_PAD_BODIES = tuple(PRESET['non_pad_collision_bodies'])
_URDF = Path(__file__).resolve().parents[5] / 'robot_usds/Sharpa_hand/Floating_Sharpa_right/official_wave_01/right_sharpa_wave/right_sharpa_wave_with_float_base.urdf'
if hashlib.sha256(_URDF.read_bytes()).hexdigest() != PRESET['urdf_sha256']:
    raise ValueError('Sharpa mount calibration does not match the official URDF')


def rotation(q):
    w, x, y, z = np.asarray(q) / np.linalg.norm(q)
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
        [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
        [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])


def preflight(robots, pieces, table_z, joint_limits):
    """Conservative home collision bounds plus bounded palm travel paths.

    The travel check proves actuator reach, not contact-rich manipulation;
    native grasp and insertion acceptance remain separate requirements.
    """
    bounds = {}
    for side, bodies in robots.items():
        bounds[side] = {}
        for name, box in PRESET['body_local_bounds'].items():
            pose = bodies[name]
            corners = np.array(list(product(*zip(box['min'], box['max']))))
            points = corners @ rotation(pose[3:7]).T + pose[:3]
            bounds[side][name] = (points.min(axis=0), points.max(axis=0))
    table_clearance = min(lo[2]-table_z for row in bounds.values() for lo, _ in row.values())
    separation = min(float(np.max(np.maximum(a[0]-b[1], b[0]-a[1])))
        for a in bounds['left'].values() for b in bounds['right'].values())
    paths = {}
    for name, piece in pieces.items():
        reachable = []
        for side, mount in PRESET['mounts'].items():
            limits = joint_limits[side][:3]
            local = np.array(piece['position']) + [0, .057, .202] - mount['position']
            above = local.copy(); above[2] = 1.15-mount['position'][2]
            if all(np.all(q >= limits[:, 0]) and np.all(q <= limits[:, 1]) for q in (local, above)):
                reachable.append(side)
        paths[name] = reachable
    return dict(passed=bool(table_clearance > .02 and separation > .02 and all(paths.values())),
        calibration_sha256=PRESET_SHA256, calibration_version=PRESET['version'],
        min_collision_table_clearance_m=float(table_clearance), interhand_aabb_separation_m=separation,
        reachable_hands=paths, collisionless_support_bodies=PRESET['collisionless_support_bodies'],
        scope='conservative home collision geometry and joint-bound palm paths; native manipulation checked separately')
