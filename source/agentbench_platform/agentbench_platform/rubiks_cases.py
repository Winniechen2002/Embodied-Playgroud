"""Versioned public initial states for the single-Panda Rubik benchmark.

The catalog is deliberately dependency-light.  It contains public reset
inputs and symbolic checksums, while the native runner consumes only the
selected case's reset projection.  Reference actions and physical traces do
not belong here.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import random
import sys
from typing import Mapping


CATALOG_VERSION = "rubiks-public-cases-v1"
FIXTURE_VERSION = "hybrid_fixture_v1"
GOAL = "solved"
DEFAULT_CENTER_XY_M = (0.700, 0.000)
CENTER_X_BOUNDS_M = (0.675, 0.725)
CENTER_Y_BOUNDS_M = (-0.025, 0.025)
MAX_ABS_YAW_RAD = math.radians(30)
ZERO_TILT = (0.0, 0.0)

# The six frames are the stable support faces specified by the benchmark
# protocol.  Keep these as tuples internally so accidental mutation cannot
# change a case after its checksum is published.
POSE_TEMPLATES: dict[str, dict[str, object]] = {
    "P01": {"center_xy_m": (0.675, -0.025), "logical_orientation": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "yaw_rad": -math.radians(30)},
    "P02": {"center_xy_m": (0.675, 0.025), "logical_orientation": ((0, 0, -1), (0, 1, 0), (1, 0, 0)), "yaw_rad": math.radians(30)},
    "P03": {"center_xy_m": (0.6875, -0.0125), "logical_orientation": ((1, 0, 0), (0, 0, 1), (0, -1, 0)), "yaw_rad": math.radians(15)},
    "P04": {"center_xy_m": (0.6875, 0.0125), "logical_orientation": ((1, 0, 0), (0, -1, 0), (0, 0, -1)), "yaw_rad": -math.radians(15)},
    "P05": {"center_xy_m": (0.700, 0.000), "logical_orientation": ((0, 0, 1), (0, 1, 0), (-1, 0, 0)), "yaw_rad": 0.0},
    "P06": {"center_xy_m": (0.7125, -0.0125), "logical_orientation": ((1, 0, 0), (0, 0, -1), (0, 1, 0)), "yaw_rad": -math.radians(15)},
    "P07": {"center_xy_m": (0.7125, 0.0125), "logical_orientation": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "yaw_rad": math.radians(15)},
    "P08": {"center_xy_m": (0.725, -0.025), "logical_orientation": ((0, 0, -1), (0, 1, 0), (1, 0, 0)), "yaw_rad": -math.radians(30)},
    "P09": {"center_xy_m": (0.725, 0.025), "logical_orientation": ((1, 0, 0), (0, 0, 1), (0, -1, 0)), "yaw_rad": math.radians(30)},
    "P10": {"center_xy_m": (0.700, 0.000), "logical_orientation": ((1, 0, 0), (0, -1, 0), (0, 0, -1)), "yaw_rad": 0.0},
}


_RAW_CASES = (
    ("C01", "P01", "easy", 1101, "F' D R F2 B", 6),
    ("C02", "P02", "easy", 1102, "B' R2 B2 D' R", 7),
    ("C03", "P03", "easy", 1103, "D2 L2 D R F", 7),
    ("C04", "P04", "easy", 1104, "F' D F' U' D2", 6),
    ("C05", "P05", "easy", 1105, "U D2 U F2 R2", 8),
    ("C06", "P06", "easy", 1106, "D' F L B R", 5),
    ("C07", "P07", "easy", 1107, "B D' B2 R' U", 6),
    ("C08", "P08", "easy", 1108, "R2 B' D2 B F", 7),
    ("C09", "P09", "easy", 1109, "D L2 U2 B L2", 8),
    ("C10", "P10", "easy", 1110, "D B U2 L' B'", 6),
    ("C11", "P01", "medium", 1211, "F2 L' B' F2 U B' U D' L2 R2", 14),
    ("C12", "P02", "medium", 1212, "F' B' R2 B2 R' L' U L2 F' B2", 14),
    ("C13", "P03", "medium", 1213, "L' B F2 B' R2 F2 L B' F' R'", 13),
    ("C14", "P04", "medium", 1214, "F2 U L2 D' B' F2 B2 U' B' D", 14),
    ("C15", "P05", "medium", 1215, "D2 B' U' R2 L' B2 F' L F2 R'", 14),
    ("C16", "P06", "medium", 1216, "L U R' B U R B' L R' B'", 10),
    ("C17", "P07", "medium", 1217, "U2 F2 R' B' R' F2 L2 B U2 D'", 15),
    ("C18", "P08", "medium", 1218, "L U2 R' U2 R F' L' B U B2", 13),
    ("C19", "P09", "medium", 1219, "L' R' B R2 U2 F B' L2 R L", 13),
    ("C20", "P10", "medium", 1220, "F2 D F D' F B' D2 L2 F B'", 13),
    ("C21", "P01", "hard", 1321, "L' R D L D2 B2 U L' D' F' L' B2 L' R L'", 18),
    ("C22", "P02", "hard", 1322, "D' F D B R' U B' F B U' R L2 U2 B L'", 17),
    ("C23", "P03", "hard", 1323, "D' F L2 R D2 F U L' B U' D' B F B R2", 18),
    ("C24", "P04", "hard", 1324, "D' L' R' F' R B' D L' F U2 B L2 D' L2 B2", 19),
    ("C25", "P05", "hard", 1325, "L F L' R L2 D B2 D B2 D F' D2 L D R", 19),
    ("C26", "P06", "hard", 1326, "D U2 F L2 B D2 B2 U2 D' B' D U F2 B D2", 22),
    ("C27", "P07", "hard", 1327, "R2 B' L U D R' D' U R' D2 L' B' D' R2 D2", 19),
    ("C28", "P08", "hard", 1328, "R2 B' F' B2 F' R D2 L' F' D' F' D L2 D2 U'", 20),
    ("C29", "P09", "hard", 1329, "D' R2 L2 U' D L2 U' R' D2 U2 F' L R' L U", 20),
    ("C30", "P10", "hard", 1330, "F R L' D R' B U2 B' L D L R2 B2 F2 R2", 20),
)


def _load_rules():
    """Load cube rules without importing Isaac or task registration modules."""
    try:
        from .cube_rules import load_rules
        return load_rules()
    except (ImportError, ModuleNotFoundError):
        path = Path(__file__).resolve().parents[2] / "agentbench" / "agentbench" / "tasks" / "manager_based" / "table_top_manipulation" / "config" / "rubiks_cube" / "rubiks_cube_rules.py"
        spec = importlib.util.spec_from_file_location("_agentbench_catalog_rules", path)
        if spec is None or spec.loader is None:
            raise ImportError(f"cube mathematics source unavailable: {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _manifest_hash(manifest_without_hash: Mapping[str, object]) -> str:
    return hashlib.sha256(_canonical(manifest_without_hash)).hexdigest()


def seeded_scramble(token_count: int, seed: int) -> str:
    """Frozen v1 generation provenance; runtime always uses the stored moves."""
    if type(token_count) is not int or not 0 <= token_count <= 100 or type(seed) is not int:
        raise ValueError('integer token count 0..100 and integer seed required')
    rng = random.Random(seed)
    tokens = []
    for _ in range(token_count):
        faces = [face for face in 'URFDLB' if not tokens or face != tokens[-1][0]]
        tokens.append(rng.choice(faces) + rng.choice(('', "'", '2')))
    return ' '.join(tokens)


def _build_cases() -> tuple[dict[str, object], ...]:
    rules = _load_rules()
    frames = {frame.logical_to_world for frame in rules.CubeFrame.all()}
    cases = []
    for case_id, pose_id, difficulty, seed, scramble, quarter_turns in _RAW_CASES:
        pose = POSE_TEMPLATES[pose_id]
        tokens = scramble.split()
        atomic = rules.parse_sequence(scramble)
        state = rules.CubeState.solved().apply_sequence(atomic)
        case = {
            "case_id": case_id,
            "difficulty": difficulty,
            "seed": seed,
            "pose_id": pose_id,
            "center_xy_m": list(pose["center_xy_m"]),
            "logical_orientation": [list(row) for row in pose["logical_orientation"]],
            "yaw_rad": pose["yaw_rad"],
            "tilt_xy_rad": list(ZERO_TILT),
            "scramble": scramble,
            "scramble_token_count": len(tokens),
            "scramble_quarter_turn_count": len(atomic),
            "goal": GOAL,
            "fixture_version": FIXTURE_VERSION,
            "expected_facelets_urfdlb": state.facelet_string(),
            "permutation_checksum": state.permutation_checksum(),
        }
        if len(atomic) != quarter_turns:
            raise ValueError(f"{case_id}: quarter-turn count mismatch")
        if len(tokens) != {'easy': 5, 'medium': 10, 'hard': 15}[difficulty]:
            raise ValueError(f"{case_id}: difficulty token count mismatch")
        if seeded_scramble(len(tokens), seed) != scramble:
            raise ValueError(f"{case_id}: deterministic seed mismatch")
        if tuple(tuple(row) for row in case["logical_orientation"]) not in frames:
            raise ValueError(f"{case_id}: logical orientation is not a cube frame")
        faces = [token[0] for token in tokens]
        if any(a == b for a, b in zip(faces, faces[1:])):
            raise ValueError(f"{case_id}: adjacent scramble faces must differ")
        cases.append(case)
    return tuple(cases)


CASES = _build_cases()


def _validate_cases(cases: tuple[dict[str, object], ...]) -> None:
    if len(cases) != 30 or {case["case_id"] for case in cases} != {f"C{i:02d}" for i in range(1, 31)}:
        raise ValueError("public Rubik catalog must contain C01..C30 exactly once")
    checksums = set()
    for case in cases:
        x, y = case["center_xy_m"]
        if not CENTER_X_BOUNDS_M[0] <= x <= CENTER_X_BOUNDS_M[1] or not CENTER_Y_BOUNDS_M[0] <= y <= CENTER_Y_BOUNDS_M[1]:
            raise ValueError(f"{case['case_id']}: center is outside public bounds")
        if abs(case["yaw_rad"]) > MAX_ABS_YAW_RAD + 1e-9:
            raise ValueError(f"{case['case_id']}: yaw is outside public bounds")
        if tuple(case["tilt_xy_rad"]) != ZERO_TILT:
            raise ValueError(f"{case['case_id']}: v1 tilt must be zero")
        if case["scramble_token_count"] != len(case["scramble"].split()):
            raise ValueError(f"{case['case_id']}: token count mismatch")
        if case["permutation_checksum"] in checksums:
            raise ValueError(f"{case['case_id']}: duplicate symbolic cube state")
        checksums.add(case["permutation_checksum"])


_validate_cases(CASES)


def _manifest_without_hash() -> dict[str, object]:
    return {"catalog_version": CATALOG_VERSION, "fixture_version": FIXTURE_VERSION, "cases": deepcopy(list(CASES))}


MANIFEST_SHA256 = _manifest_hash(_manifest_without_hash())
PUBLIC_MANIFEST = {
    "catalog_version": CATALOG_VERSION,
    "fixture_version": FIXTURE_VERSION,
    "manifest_sha256": MANIFEST_SHA256,
    "cases": [{**deepcopy(case), "manifest_sha256": MANIFEST_SHA256} for case in CASES],
}


def get_case(case_id: str) -> dict[str, object]:
    """Return an immutable-by-convention copy of one catalog entry."""
    if not isinstance(case_id, str):
        raise ValueError("case_id must be a string")
    for case in CASES:
        if case["case_id"] == case_id:
            return deepcopy({**case, "manifest_sha256": MANIFEST_SHA256})
    raise ValueError(f"Unknown Rubik public case_id: {case_id}")


def case_ids() -> tuple[str, ...]:
    return tuple(case["case_id"] for case in CASES)


def public_manifest() -> dict[str, object]:
    return deepcopy(PUBLIC_MANIFEST)


def public_reset_data(case_id: str) -> dict[str, object]:
    """Return only fields accepted by trusted native reset."""
    case = get_case(case_id)
    return {key: deepcopy(case[key]) for key in ("center_xy_m", "logical_orientation", "yaw_rad", "tilt_xy_rad", "scramble")}


def public_description(case_id: str) -> dict[str, object]:
    """The case identity an agent may see; no public reset config is returned."""
    case = get_case(case_id)
    return {"case_id": case["case_id"], "goal": case["goal"]}


def case_evidence(case_id: str) -> dict[str, object]:
    """Trusted journal identity, never returned through the SDK."""
    case = get_case(case_id)
    return {"catalog_version": CATALOG_VERSION, **{key: case[key] for key in (
        "case_id", "seed", "fixture_version", "manifest_sha256", "expected_facelets_urfdlb",
        "permutation_checksum")}}


def validate_manifest(manifest: object) -> None:
    """Require the exact frozen v1 catalog, including every derived state hash."""
    if _canonical(manifest) != _canonical(PUBLIC_MANIFEST):
        raise ValueError('public Rubik manifest differs from the frozen catalog')


def write_manifest(path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(PUBLIC_MANIFEST, indent=2, sort_keys=True) + "\n")
    return destination
