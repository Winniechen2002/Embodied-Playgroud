"""Versioned Kongming-lock public cases and trusted reset projections.

The catalog is dependency-light and deliberately keeps the complete reset
projection on the maintainer side.  Agents receive only the selected case
identity through the protocol description.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


CATALOG_VERSION = "kongming-public-cases-v1"
FIXTURE_VERSION = "shape_v1.5"
LOCK_CENTER = (0.70, 0.0, 0.70)
BAR_CASE_PIECE = "frame_y1"

POSE_TEMPLATES = (
    ("P01", "easy", 0.000, 0.000, 0.0),
    ("P02", "easy", -0.015, -0.020, 5.0),
    ("P03", "medium", 0.015, 0.020, -5.0),
    ("P04", "hard", -0.025, 0.030, 10.0),
    ("P05", "hard", 0.025, -0.030, -10.0),
)

_TASK_BLOCKS = (
    ("full", "assemble", "A", "complete", ()),
    ("key", "assemble", "A", "key_only", ("key",)),
    ("key_bar", "assemble", "A", "key_plus_bar", ("key", BAR_CASE_PIECE)),
    ("full", "disassemble", "D", "complete", ()),
    ("key", "disassemble", "D", "key_only", ("key",)),
    ("key_bar", "disassemble", "D", "key_plus_bar", ("key", BAR_CASE_PIECE)),
)


def _shape_module():
    path = Path(__file__).resolve().parents[2] / "agentbench" / "agentbench" / "tasks" / "manager_based" / "table_top_manipulation" / "config" / "kongming_lock" / "shapes.py"
    spec = importlib.util.spec_from_file_location("_agentbench_kongming_shapes", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Kongming shapes unavailable: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def _quat_mul(a, b):
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return (aw * bw - ax * bx - ay * by - az * bz,
            aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw)


def _yaw_quaternion(degrees):
    import math
    half = math.radians(degrees) / 2.0
    return (math.cos(half), 0.0, 0.0, math.sin(half))


def _rotate_z(vector, degrees):
    import math
    angle = math.radians(degrees)
    c, s = math.cos(angle), math.sin(angle)
    x, y, z = vector
    return (c * x - s * y, s * x + c * y, z)


def _transform_pose(position, quaternion, dx, dy, yaw):
    relative = tuple(float(a - b) for a, b in zip(position, LOCK_CENTER))
    rotated = _rotate_z(relative, yaw)
    result_position = (rotated[0] + LOCK_CENTER[0] + dx,
                       rotated[1] + LOCK_CENTER[1] + dy,
                       rotated[2] + LOCK_CENTER[2])
    result_quaternion = _quat_mul(_yaw_quaternion(yaw), quaternion)
    return list(result_position), list(result_quaternion)


def _base_piece_rows():
    shapes = _shape_module()
    return {
        piece.name: dict(
            assembly_position=list(piece.assembly_position),
            assembly_quaternion=list(piece.assembly_quat_wxyz),
            parking_position=list(piece.target_position),
            parking_quaternion=list(piece.target_quat_wxyz),
        ) for piece in shapes.CANONICAL_SPEC.pieces
    }


def _case_rows(block, subtask, prefix, index, difficulty, pose_id, dx, dy, yaw, target_pieces):
    rows = _base_piece_rows()
    initial = {}
    goal = {}
    for name, row in rows.items():
        assembly = _transform_pose(row["assembly_position"], row["assembly_quaternion"], dx, dy, yaw)
        parking = _transform_pose(row["parking_position"], row["parking_quaternion"], dx, dy, yaw)
        row["assembly_position"], row["assembly_quaternion"] = assembly
        row["parking_position"], row["parking_quaternion"] = parking
        if block == "full":
            initial[name] = parking if prefix == "A" else assembly
            goal[name] = assembly if prefix == "A" else parking
        else:
            moved = name in target_pieces
            initial[name] = parking if (moved and prefix == "A") else assembly
            goal[name] = assembly if (moved and prefix == "A") else parking if (moved and prefix == "D") else assembly
            if prefix == "D" and not moved:
                goal[name] = assembly
    case_id = f"{prefix}{index:02d}"
    return dict(
        case_id=case_id,
        catalog_version=CATALOG_VERSION,
        fixture_version=FIXTURE_VERSION,
        task=prefix.lower() == "a" and "assemble" or "disassemble",
        subtask=subtask,
        goal="assembled" if prefix == "A" else "disassembled",
        difficulty=difficulty,
        pose_id=pose_id,
        seed=1000 + index + (0 if prefix == "A" else 100),
        center_xy_m=[round(LOCK_CENTER[0] + dx, 6), round(LOCK_CENTER[1] + dy, 6)],
        yaw_rad=round(__import__("math").radians(yaw), 9),
        target_pieces=list(target_pieces),
        expected_stage_count=9 if block == "full" else 1 if block == "key" else 2,
        pieces=rows,
        initial=initial,
        goal_state=goal,
        state_hash=hashlib.sha256(_canonical(dict(initial=initial, goal=goal))).hexdigest(),
    )


def _build_cases():
    cases = []
    counters = {"A": 0, "D": 0}
    for block, task, prefix, subtask, target_pieces in _TASK_BLOCKS:
        for pose_id, difficulty, dx, dy, yaw in POSE_TEMPLATES:
            counters[prefix] += 1
            cases.append(_case_rows(block, subtask, prefix, counters[prefix], difficulty, pose_id, dx, dy, yaw, target_pieces))
    return tuple(cases)


CASES = _build_cases()


def _manifest_without_hash():
    return dict(catalog_version=CATALOG_VERSION, fixture_version=FIXTURE_VERSION,
                bar_case_piece=BAR_CASE_PIECE, cases=list(CASES))


MANIFEST_SHA256 = hashlib.sha256(_canonical(_manifest_without_hash())).hexdigest()


def _public_case(case):
    # Geometry, initial poses and goal poses remain trusted-runtime inputs.
    return {key: case[key] for key in (
        "case_id", "task", "subtask", "goal", "difficulty", "target_pieces",
        "expected_stage_count", "state_hash")}


PUBLIC_MANIFEST = dict(catalog_version=CATALOG_VERSION, fixture_version=FIXTURE_VERSION,
                       bar_case_piece=BAR_CASE_PIECE, manifest_sha256=MANIFEST_SHA256,
                       cases=[{**_public_case(case), "manifest_sha256": MANIFEST_SHA256} for case in CASES])


def case_ids():
    return tuple(case["case_id"] for case in CASES)


def get_case(case_id):
    for case in CASES:
        if case["case_id"] == case_id:
            return deepcopy({**case, "manifest_sha256": MANIFEST_SHA256})
    raise ValueError(f"Unknown Kongming public case_id: {case_id}")


def public_manifest():
    return deepcopy(PUBLIC_MANIFEST)


def public_description(case_id):
    case = get_case(case_id)
    return describe_case_spec(case)


def describe_case_spec(case):
    """Task intent only: never export the private pose projections."""
    selected = list(case['target_pieces']) or list(case['pieces'])
    verb = 'Assemble' if case['task'] == 'assemble' else 'Remove and park'
    objects = 'all six wooden pieces' if case['subtask'] == 'complete' else ', '.join(selected)
    description = f'{verb} {objects} in the marked goal regions.'
    if case['subtask'] != 'complete':
        description += ' Keep all other pieces in their assembled configuration.'
    return dict(case_id=case['case_id'], task=case['task'], subtask=case['subtask'],
                goal=case.get('goal', 'assembled' if case['task']=='assemble' else 'disassembled'),
                target_pieces=selected, description=description)


def goal_reference_spec(case):
    """Independent reset projection for a goal-only rendering instance."""
    result = deepcopy(case)
    result['initial'] = deepcopy(case['goal_state'])
    return result


def trusted_case_spec(case_id):
    case = get_case(case_id)
    return dict(case_id=case["case_id"], task=case["task"], subtask=case["subtask"],
                target_pieces=list(case["target_pieces"]), initial=deepcopy(case["initial"]),
                goal_state=deepcopy(case["goal_state"]), pieces=deepcopy(case["pieces"]),
                state_hash=case["state_hash"], manifest_sha256=MANIFEST_SHA256)


def validate_manifest(manifest):
    if _canonical(manifest) != _canonical(PUBLIC_MANIFEST):
        raise ValueError("public Kongming manifest differs from frozen catalog")


def write_manifest(path):
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(PUBLIC_MANIFEST, indent=2, sort_keys=True) + "\n")
    return destination


def case_evidence(case_id):
    case = get_case(case_id)
    return dict(catalog_version=CATALOG_VERSION, case_id=case["case_id"], task=case["task"],
                subtask=case["subtask"], difficulty=case["difficulty"], seed=case["seed"],
                fixture_version=FIXTURE_VERSION, manifest_sha256=MANIFEST_SHA256,
                state_hash=case["state_hash"], target_pieces=case["target_pieces"])


def transformed_case_bounds(case_id):
    """Cheap preflight bounds for reset acceptance and tests."""
    case = get_case(case_id)
    positions = [pose[0] for row in case["pieces"].values() for pose in (
        (row["assembly_position"], row["assembly_quaternion"]),
        (row["parking_position"], row["parking_quaternion"]),)]
    return dict(min_x=min(p[0] for p in positions), max_x=max(p[0] for p in positions),
                min_y=min(p[1] for p in positions), max_y=max(p[1] for p in positions),
                min_z=min(p[2] for p in positions), max_z=max(p[2] for p in positions))


def _validate_cases():
    expected = [f"A{i:02d}" for i in range(1, 16)] + [f"D{i:02d}" for i in range(1, 16)]
    if list(case_ids()) != expected:
        raise ValueError("Kongming catalog order must be A01..A15,D01..D15")
    if len({case["state_hash"] for case in CASES}) != len(CASES):
        raise ValueError("Kongming cases must have unique state hashes")
    for case in CASES:
        bounds = transformed_case_bounds(case["case_id"])
        if not (0.45 <= bounds["min_x"] and bounds["max_x"] <= 1.05 and
                -0.78 <= bounds["min_y"] and bounds["max_y"] <= 0.25):
            raise ValueError(f"{case['case_id']}: transformed poses outside native workspace")
        if abs(case["yaw_rad"]) > __import__("math").radians(10.0) + 1e-9:
            raise ValueError(f"{case['case_id']}: yaw outside v1 bound")
        if case["subtask"] == "key_plus_bar" and case["target_pieces"] != ["key", BAR_CASE_PIECE]:
            raise ValueError(f"{case['case_id']}: key-plus-bar target mismatch")


_validate_cases()
