"""Pure cube notation, state, and acceptance rules for Rubik's Cube twists."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from numbers import Real
from typing import Mapping, Sequence


ANGLE_TOLERANCE_RAD = math.radians(5.0)
HYBRID_ANGLE_TOLERANCE_RAD = math.radians(3.0)
JOINT_VELOCITY_TOLERANCE_RAD_S = 0.1
CONTACT_OBSERVED_THRESHOLD_N = 1.0
CONTACT_MAINTAINED_THRESHOLD_N = 0.5
CONTACT_MAINTAINED_FRACTION = 0.75
WRIST_YAW_MINIMUM_RAD = math.radians(80.0)
BASE_POSE_TOLERANCE_M = 0.001
CUBIE_ALIGNMENT_TOLERANCE_M = 0.001
CORE_ORIENTATION_TOLERANCE_RAD = math.radians(3.0)
NON_ACTIVE_CUBIE_ORIENTATION_TOLERANCE_RAD = math.radians(3.0)

PROHIBITED_MOVE_TECHNIQUE_DISCLOSURES = (
    "used_direct_cubie_state_during_move",
    "used_direct_core_pose_during_move",
    "used_active_cube_drive",
    "used_constraint_switching_outside_fixture_lifecycle",
    "used_hard_joint_limit",
    "used_target_snapping",
    "used_robot_cube_attachment",
    "predicted_state_committed",
)

_ACTIVE_CUBIE_GEOMETRY_FAILURE_REASONS = frozenset(
    {
        "active_cubie_geometry_malformed",
        "active_cubie_geometry_nonfinite",
        "active_cubie_grid_ambiguous",
        "active_cubie_grid_duplicate",
        "active_cubie_off_grid",
    }
)
_CUBE_LATTICE_SLOTS = tuple(
    (x, y, z)
    for x in (-1, 0, 1)
    for y in (-1, 0, 1)
    for z in (-1, 0, 1)
    if (x, y, z) != (0, 0, 0)
)


def merge_authoritative_disclosures(
    defaults: Mapping[str, object],
    authoritative: Mapping[str, object],
    *,
    authoritative_fields: Sequence[str] = PROHIBITED_MOVE_TECHNIQUE_DISCLOSURES,
) -> dict[str, object]:
    """Merge metrics without replacing an owner's disclosure with a default.

    ``defaults`` may fill fields for which no runtime producer owns the value.
    Every field listed in ``authoritative_fields`` instead belongs to
    ``authoritative``: its exact value wins, and its absence removes any
    default.  In particular, this function never turns true, malformed, or
    missing authoritative disclosures into false.
    """

    if not isinstance(defaults, Mapping):
        raise TypeError("disclosure defaults must be a mapping")
    if not isinstance(authoritative, Mapping):
        raise TypeError("authoritative disclosures must be a mapping")
    fields = tuple(authoritative_fields)
    if any(not isinstance(name, str) or not name for name in fields):
        raise ValueError("authoritative disclosure fields must be non-empty strings")

    merged = {**dict(defaults), **dict(authoritative)}
    for name in fields:
        if name not in authoritative:
            merged.pop(name, None)
    return merged

FACE_AXIS_SIGN = {
    "U": ("Z", 1),
    "D": ("Z", -1),
    "R": ("X", 1),
    "L": ("X", -1),
    "F": ("Y", -1),
    "B": ("Y", 1),
}
FACE_NORMALS = {
    "U": (0, 0, 1),
    "R": (1, 0, 0),
    "F": (0, -1, 0),
    "D": (0, 0, -1),
    "L": (-1, 0, 0),
    "B": (0, 1, 0),
}
NORMAL_TO_FACE = {normal: face for face, normal in FACE_NORMALS.items()}
IDENTITY_ORIENTATION = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
FACE_GRID_AXES = {
    "U": ((0, 1, 0), (1, 0, 0)),
    "R": ((0, 0, 1), (0, 1, 0)),
    "F": ((0, 0, 1), (1, 0, 0)),
    "D": ((0, -1, 0), (1, 0, 0)),
    "L": ((0, 0, 1), (0, -1, 0)),
    "B": ((0, 0, 1), (-1, 0, 0)),
}


def _piece_id(position: tuple[int, int, int]) -> str:
    labels = {-1: "m1", 0: "z0", 1: "p1"}
    return "cubie_" + "_".join(labels[value] for value in position)


def _stickers_at(position: tuple[int, int, int]) -> tuple[str, ...]:
    return tuple(
        face
        for face in "URFDLB"
        if sum(coordinate * normal for coordinate, normal in zip(position, FACE_NORMALS[face])) == 1
    )


def _dot(left: tuple[int, int, int], right: tuple[int, int, int]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def _mat_vec(
    matrix: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]],
    vector: tuple[int, int, int],
) -> tuple[int, int, int]:
    return tuple(_dot(row, vector) for row in matrix)  # type: ignore[return-value]


def _mat_mul(
    left: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]],
    right: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]],
) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    columns = tuple(zip(*right, strict=True))
    return tuple(
        tuple(_dot(row, column) for column in columns)
        for row in left
    )  # type: ignore[return-value]


def _quarter_rotation(
    axis: str, quarter_turns: int
) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    normalized = quarter_turns % 4
    positive = {
        "X": ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
        "Y": ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
        "Z": ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
    }[axis]
    result = IDENTITY_ORIENTATION
    for _ in range(normalized):
        result = _mat_mul(positive, result)
    return result


@dataclass(frozen=True)
class CubeFrame:
    """Discrete orientation mapping logical cube axes into world axes."""

    logical_to_world: tuple[
        tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]
    ]

    @classmethod
    def identity(cls) -> "CubeFrame":
        return cls(IDENTITY_ORIENTATION)

    @property
    def key(self) -> tuple[int, ...]:
        return tuple(value for row in self.logical_to_world for value in row)

    @classmethod
    def all(cls) -> tuple["CubeFrame", ...]:
        identity = cls.identity()
        pending = [identity]
        ordered = []
        seen = set()
        while pending:
            frame = pending.pop(0)
            if frame.key in seen:
                continue
            seen.add(frame.key)
            ordered.append(frame)
            for axis in ("X", "Y"):
                for quarter_turns in (-1, 1):
                    pending.append(frame.rotate(axis, quarter_turns))
        if len(ordered) != 24:
            raise RuntimeError(f"cube rotation group has {len(ordered)} states")
        return tuple(ordered)

    def rotate(self, axis: str, quarter_turns: int) -> "CubeFrame":
        normalized_axis = axis.upper()
        if normalized_axis not in "XYZ":
            raise ValueError(f"unsupported cube-frame rotation axis: {axis!r}")
        return CubeFrame(
            _mat_mul(_quarter_rotation(normalized_axis, quarter_turns), self.logical_to_world)
        )

    def compose(self, other: "CubeFrame") -> "CubeFrame":
        return CubeFrame(_mat_mul(self.logical_to_world, other.logical_to_world))

    def inverse(self) -> "CubeFrame":
        return CubeFrame(tuple(zip(*self.logical_to_world, strict=True)))

    def relative_rotation_to(self, target: "CubeFrame") -> "CubeFrame":
        return target.compose(self.inverse())

    def world_normal(self, face: str) -> tuple[int, int, int]:
        normalized_face = face.upper()
        if normalized_face not in FACE_NORMALS:
            raise ValueError(f"unsupported face: {face!r}")
        return _mat_vec(self.logical_to_world, FACE_NORMALS[normalized_face])

    def world_top_face(self) -> str:
        return next(face for face in "URFDLB" if self.world_normal(face) == (0, 0, 1))

    def support_face(self) -> str:
        return next(face for face in "URFDLB" if self.world_normal(face) == (0, 0, -1))

    def carrier_axis_in_world(self, face: str) -> tuple[str, int]:
        normalized_face = face.upper()
        if normalized_face not in FACE_AXIS_SIGN:
            raise ValueError(f"unsupported face: {face!r}")
        local_axis = FACE_AXIS_SIGN[normalized_face][0]
        local_unit = {
            "X": (1, 0, 0),
            "Y": (0, 1, 0),
            "Z": (0, 0, 1),
        }[local_axis]
        world_unit = _mat_vec(self.logical_to_world, local_unit)
        component = next(index for index, value in enumerate(world_unit) if value)
        return "XYZ"[component], world_unit[component]

    @property
    def is_identity(self) -> bool:
        return self.logical_to_world == IDENTITY_ORIENTATION


@dataclass(frozen=True)
class CubieState:
    identity: str
    home_position: tuple[int, int, int]
    position: tuple[int, int, int]
    orientation: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
    stickers: tuple[str, ...]


@dataclass(frozen=True)
class CubeState:
    """Discrete, piece-accurate state of the 26 visible cubies."""

    pieces: dict[str, CubieState]

    @classmethod
    def solved(cls) -> "CubeState":
        pieces = {}
        for z in (-1, 0, 1):
            for y in (-1, 0, 1):
                for x in (-1, 0, 1):
                    position = (x, y, z)
                    if position == (0, 0, 0):
                        continue
                    identity = _piece_id(position)
                    pieces[identity] = CubieState(
                        identity=identity,
                        home_position=position,
                        position=position,
                        orientation=IDENTITY_ORIENTATION,
                        stickers=_stickers_at(position),
                    )
        return cls(pieces)

    def active_cubie_ids(self, face: str) -> tuple[str, ...]:
        normalized_face = face.upper()
        if normalized_face not in FACE_NORMALS:
            raise ValueError(f"unsupported face: {face!r}")
        normal = FACE_NORMALS[normalized_face]
        return tuple(
            sorted(
                identity
                for identity, piece in self.pieces.items()
                if _dot(piece.position, normal) == 1
            )
        )

    def facelet_string(self) -> str:
        facelets: dict[str, list[str | None]] = {face: [None] * 9 for face in "URFDLB"}
        for piece in self.pieces.values():
            for sticker in piece.stickers:
                world_normal = _mat_vec(piece.orientation, FACE_NORMALS[sticker])
                world_face = NORMAL_TO_FACE[world_normal]
                up_axis, right_axis = FACE_GRID_AXES[world_face]
                row = 1 - _dot(piece.position, up_axis)
                column = 1 + _dot(piece.position, right_axis)
                facelets[world_face][3 * row + column] = sticker
        if any(value is None for values in facelets.values() for value in values):
            raise ValueError("cube state does not define all 54 facelets")
        return "".join(str(value) for face in "URFDLB" for value in facelets[face])

    def apply_move(self, move: str) -> "CubeState":
        atomic = parse_sequence((move,))
        if len(atomic) != 1:
            return self.apply_sequence(atomic)
        normalized = atomic[0]
        face = normalized[0]
        axis, outward_axis_sign = FACE_AXIS_SIGN[face]
        clockwise_sign = -1 if not normalized.endswith("-prime") else 1
        rotation = _quarter_rotation(axis, clockwise_sign * outward_axis_sign)
        active = set(self.active_cubie_ids(face))
        pieces = {}
        for identity, piece in self.pieces.items():
            if identity not in active:
                pieces[identity] = piece
                continue
            pieces[identity] = CubieState(
                identity=piece.identity,
                home_position=piece.home_position,
                position=_mat_vec(rotation, piece.position),
                orientation=_mat_mul(rotation, piece.orientation),
                stickers=piece.stickers,
            )
        return CubeState(pieces)

    def apply_sequence(self, sequence: str | Sequence[str]) -> "CubeState":
        state = self
        for move in parse_sequence(sequence):
            state = state.apply_move(move)
        return state

    def permutation_checksum(self) -> str:
        payload = "|".join(
            f"{identity}:{piece.position}:{piece.orientation}"
            for identity, piece in sorted(self.pieces.items())
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, object]:
        return {
            "pieces": {
                identity: {
                    "home_position": list(piece.home_position),
                    "position": list(piece.position),
                    "orientation": [list(row) for row in piece.orientation],
                    "stickers": list(piece.stickers),
                }
                for identity, piece in sorted(self.pieces.items())
            },
            "facelets_urfdlb": self.facelet_string(),
            "permutation_checksum": self.permutation_checksum(),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "CubeState":
        raw_pieces = payload.get("pieces")
        if not isinstance(raw_pieces, dict) or len(raw_pieces) != 26:
            raise ValueError("cube state must contain exactly 26 pieces")
        pieces = {}
        for identity, raw_piece in raw_pieces.items():
            if not isinstance(identity, str) or not isinstance(raw_piece, dict):
                raise ValueError("invalid serialized cubie")
            home_position = tuple(int(value) for value in raw_piece["home_position"])
            position = tuple(int(value) for value in raw_piece["position"])
            orientation = tuple(
                tuple(int(value) for value in row) for row in raw_piece["orientation"]
            )
            stickers = tuple(str(value) for value in raw_piece["stickers"])
            if len(home_position) != 3 or len(position) != 3 or len(orientation) != 3:
                raise ValueError(f"invalid serialized cubie geometry: {identity}")
            pieces[identity] = CubieState(
                identity=identity,
                home_position=home_position,  # type: ignore[arg-type]
                position=position,  # type: ignore[arg-type]
                orientation=orientation,  # type: ignore[arg-type]
                stickers=stickers,
            )
        state = cls(pieces)
        if len({piece.position for piece in pieces.values()}) != 26:
            raise ValueError("cube state contains duplicate cubie positions")
        return state


def normalize_move(move: str) -> tuple[str, bool]:
    """Return ``(canonical quarter turn, is_double)`` for one move token."""

    token = move.strip()
    if not token:
        raise ValueError("move token cannot be empty")
    face = token[0].upper()
    if face not in FACE_AXIS_SIGN:
        raise ValueError(f"unsupported face in move: {move!r}")
    suffix = token[1:]
    if suffix == "":
        return face, False
    if suffix in ("'", "-prime"):
        return f"{face}-prime", False
    if suffix == "2":
        return face, True
    raise ValueError(f"unsupported move suffix in: {move!r}")


def parse_sequence(sequence: str | Sequence[str]) -> tuple[str, ...]:
    """Parse notation and expand double turns into atomic quarter turns."""

    tokens = sequence.split() if isinstance(sequence, str) else list(sequence)
    atomic: list[str] = []
    for token in tokens:
        normalized, is_double = normalize_move(token)
        atomic.append(normalized)
        if is_double:
            atomic.append(normalized)
    return tuple(atomic)


def inverse_sequence(sequence: str | Sequence[str]) -> tuple[str, ...]:
    """Return the atomic inverse of a move sequence."""

    return tuple(
        move[0] if move.endswith("-prime") else f"{move[0]}-prime"
        for move in reversed(parse_sequence(sequence))
    )


def move_delta_rad(move: str) -> float:
    """Return a quarter-turn angle about the carrier's positive world axis."""

    normalized, is_double = normalize_move(move)
    if is_double:
        raise ValueError("move_delta_rad accepts one atomic quarter turn, not a double turn")
    face = normalized[0]
    outward_axis_sign = FACE_AXIS_SIGN[face][1]
    clockwise_sign = -1 if not normalized.endswith("-prime") else 1
    return clockwise_sign * outward_axis_sign * math.pi / 2.0


def wrap_angle(angle_rad: float) -> float:
    """Wrap an angle to the shortest signed equivalent in [-pi, pi]."""

    return math.atan2(math.sin(angle_rad), math.cos(angle_rad))


def angle_error_rad(actual_rad: float, target_rad: float) -> float:
    """Return the absolute shortest angular distance to the target."""

    return abs(wrap_angle(actual_rad - target_rad))


def _contact_fraction(
    left_forces_n: Sequence[float], right_forces_n: Sequence[float], *,
    minimum_maintained_contact_n: float | None = None,
) -> float:
    if minimum_maintained_contact_n is not None:
        if (isinstance(minimum_maintained_contact_n, bool)
                or not isinstance(minimum_maintained_contact_n, Real)
                or not math.isfinite(minimum_maintained_contact_n)
                or minimum_maintained_contact_n <= 0):
            raise ValueError('invalid maintained contact threshold')
    if len(left_forces_n) != len(right_forces_n):
        raise ValueError("left and right contact force sequences must have equal length")
    if not left_forces_n:
        return 0.0
    maintained = sum(
        (left > CONTACT_MAINTAINED_THRESHOLD_N and right > CONTACT_MAINTAINED_THRESHOLD_N)
        if minimum_maintained_contact_n is None else
        (left >= minimum_maintained_contact_n and right >= minimum_maintained_contact_n)
        for left, right in zip(left_forces_n, right_forces_n, strict=True)
    )
    return maintained / len(left_forces_n)


def _finite_nonnegative_metric(
    metrics: Mapping[str, object], name: str
) -> float | None:
    value = metrics.get(name)
    if isinstance(value, bool) or not isinstance(value, Real):
        return None
    converted = float(value)
    if not math.isfinite(converted) or converted < 0.0:
        return None
    return converted


def _strict_metric_tree_is_finite(value: object) -> bool:
    if isinstance(value, bool) or value is None:
        return True
    if isinstance(value, Real):
        return math.isfinite(float(value))
    if isinstance(value, Mapping):
        return all(_strict_metric_tree_is_finite(item) for item in value.values())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return all(_strict_metric_tree_is_finite(item) for item in value)
    return True


def measure_active_cubie_lattice_alignment(
    relative_positions_m: Mapping[str, Sequence[float]],
    *,
    pitch_m: float,
) -> dict[str, object]:
    """Measure active cubies against unique legal core-frame lattice slots.

    Piece identity and the requested permutation are deliberately irrelevant.
    Every measured active cubie is assigned to its unique nearest one of the 26
    legal 3x3 cube slots.  The assignment fails closed when the nine-position
    geometry is malformed, nonfinite, ambiguous, duplicated, or off-grid.
    """

    if (
        isinstance(pitch_m, bool)
        or not isinstance(pitch_m, Real)
        or not math.isfinite(float(pitch_m))
        or float(pitch_m) <= 0.0
    ):
        raise ValueError("cubie pitch must be a finite positive number")
    pitch = float(pitch_m)

    assigned: dict[str, tuple[int, int, int]] = {}

    def failed(
        reason: str,
        *,
        max_error_m: float | None = None,
    ) -> dict[str, object]:
        return {
            "active_cubie_alignment_error_m": max_error_m,
            "active_cubie_geometry_valid": False,
            "active_cubie_geometry_reason": reason,
            "active_cubie_nearest_grid_slots": dict(assigned),
        }

    if not isinstance(relative_positions_m, Mapping) or len(relative_positions_m) != 9:
        return failed("active_cubie_geometry_malformed")

    errors: list[float] = []
    occupied: dict[tuple[int, int, int], str] = {}
    for identity, raw_position in relative_positions_m.items():
        if not isinstance(identity, str) or not identity:
            return failed("active_cubie_geometry_malformed")
        try:
            position = tuple(raw_position)
        except TypeError:
            return failed("active_cubie_geometry_malformed")
        if len(position) != 3 or any(
            isinstance(value, bool) or not isinstance(value, Real)
            for value in position
        ):
            return failed("active_cubie_geometry_malformed")
        measured = tuple(float(value) for value in position)
        if not all(math.isfinite(value) for value in measured):
            return failed("active_cubie_geometry_nonfinite")

        candidates = sorted(
            (
                math.dist(
                    measured,
                    tuple(coordinate * pitch for coordinate in slot),
                ),
                slot,
            )
            for slot in _CUBE_LATTICE_SLOTS
        )
        nearest_error, nearest_slot = candidates[0]
        if math.isclose(
            nearest_error,
            candidates[1][0],
            rel_tol=1e-12,
            abs_tol=1e-12,
        ):
            return failed("active_cubie_grid_ambiguous")
        if nearest_slot in occupied:
            return failed("active_cubie_grid_duplicate")
        occupied[nearest_slot] = identity
        assigned[identity] = nearest_slot
        errors.append(nearest_error)

    maximum_error = max(errors)
    if maximum_error > CUBIE_ALIGNMENT_TOLERANCE_M + 1e-12:
        return failed(
            "active_cubie_off_grid",
            max_error_m=maximum_error,
        )
    return {
        "active_cubie_alignment_error_m": maximum_error,
        "active_cubie_geometry_valid": True,
        "active_cubie_geometry_reason": None,
        "active_cubie_nearest_grid_slots": dict(assigned),
    }


def quarter_turn_hard_safety_reason(
    metrics: Mapping[str, object],
) -> str | None:
    """Return an independent non-target safety failure for a turn result.

    Requested direction, requested target angle, and requested permutation are
    intentionally excluded: a fresh legal observation may reconcile those
    discrepancies.  Every contact, finite-value, geometry, fixture, transport,
    and hidden-actuation condition must still pass.
    """

    if not isinstance(metrics, Mapping):
        return "strict_metrics_invalid"

    for name in PROHIBITED_MOVE_TECHNIQUE_DISCLOSURES:
        if name not in metrics:
            return f"{name}_disclosure_missing"
        value = metrics[name]
        if type(value) is not bool:
            return f"{name}_disclosure_invalid"
        if value:
            return f"{name}_forbidden"

    if "active_cubie_geometry_valid" not in metrics:
        return "active_cubie_geometry_disclosure_missing"
    geometry_valid = metrics["active_cubie_geometry_valid"]
    geometry_reason = metrics.get("active_cubie_geometry_reason")
    if type(geometry_valid) is not bool:
        return "active_cubie_geometry_disclosure_invalid"
    if geometry_valid:
        if geometry_reason is not None:
            return "active_cubie_geometry_disclosure_invalid"
    else:
        if geometry_reason not in _ACTIVE_CUBIE_GEOMETRY_FAILURE_REASONS:
            return "active_cubie_geometry_disclosure_invalid"
        return str(geometry_reason)

    if not _strict_metric_tree_is_finite(metrics):
        return "nonfinite_strict_metric"
    required_finite = (
        "initial_angle_rad",
        "final_angle_rad",
        "final_angular_velocity_rad_s",
        "wrist_axis_delta_rad",
        "core_pose_error_m",
        "active_cubie_alignment_error_m",
        "non_active_cubie_displacement_m",
        "contact_maintained_fraction",
    )
    numeric: dict[str, float] = {}
    for name in required_finite:
        value = _finite_nonnegative_metric(metrics, name)
        if name in (
            "initial_angle_rad",
            "final_angle_rad",
            "final_angular_velocity_rad_s",
            "wrist_axis_delta_rad",
        ):
            raw = metrics.get(name)
            if isinstance(raw, bool) or not isinstance(raw, Real):
                return "strict_metrics_incomplete"
            value = float(raw)
            if not math.isfinite(value):
                return "nonfinite_strict_metric"
        if value is None:
            return (
                "nonfinite_strict_metric"
                if name in metrics
                else "strict_metrics_incomplete"
            )
        numeric[name] = value

    if metrics.get("used_internal_constraint_switching") is not True:
        return "internal_constraint_switching_missing"
    if metrics.get("used_passive_detent") is not True:
        return "passive_detent_missing"
    actual_delta = numeric["final_angle_rad"] - numeric["initial_angle_rad"]
    if (
        abs(abs(actual_delta) - math.pi / 2.0)
        > HYBRID_ANGLE_TOLERANCE_RAD + 1e-12
    ):
        return "angle_tolerance_exceeded"
    # Raw solver velocity can disagree with the actual pose trajectory under
    # the declared internal constraints. The caller must validate a fresh,
    # stable native window; keep the raw finite velocity above for diagnostics.
    if metrics.get("native_pose_window_valid") is not True:
        return "native_pose_window_invalid"
    if abs(numeric["wrist_axis_delta_rad"]) + 1e-12 < WRIST_YAW_MINIMUM_RAD:
        return "wrist_rotation_insufficient"
    if metrics.get("left_contact_observed") is not True:
        return "left_contact_missing"
    if metrics.get("right_contact_observed") is not True:
        return "right_contact_missing"
    maintained_fraction = numeric["contact_maintained_fraction"]
    if (
        maintained_fraction > 1.0 + 1e-12
        or maintained_fraction + 1e-12 < CONTACT_MAINTAINED_FRACTION
    ):
        return "contact_maintenance_below_threshold"
    if numeric["core_pose_error_m"] > BASE_POSE_TOLERANCE_M + 1e-12:
        return "core_pose_drift"
    if (
        numeric["active_cubie_alignment_error_m"]
        > CUBIE_ALIGNMENT_TOLERANCE_M + 1e-12
    ):
        return "active_cubie_alignment_error"
    if (
        numeric["non_active_cubie_displacement_m"]
        > CUBIE_ALIGNMENT_TOLERANCE_M + 1e-12
    ):
        return "non_active_cubie_displacement"

    optional_tolerances = (
        ("core_orientation_error_rad", CORE_ORIENTATION_TOLERANCE_RAD),
        (
            "non_active_cubie_orientation_displacement_rad",
            NON_ACTIVE_CUBIE_ORIENTATION_TOLERANCE_RAD,
        ),
    )
    for name, tolerance in optional_tolerances:
        if name not in metrics:
            continue
        value = _finite_nonnegative_metric(metrics, name)
        if value is None:
            return "nonfinite_strict_metric"
        if value > tolerance + 1e-12:
            return name.removesuffix("_rad")

    force_keys = ("max_contact_force_n", "contact_force_limit_n")
    if any(name in metrics for name in force_keys):
        maximum = _finite_nonnegative_metric(metrics, force_keys[0])
        limit = _finite_nonnegative_metric(metrics, force_keys[1])
        if maximum is None or limit is None:
            return "nonfinite_strict_metric"
        if maximum > limit + 1e-12:
            return "excessive_contact_force"

    for name, reason in (
        ("physically_finalized", "physical_finalization_failed"),
        ("fixture_locked", "fixture_unlocked"),
        ("transport_safely_finalized", "transport_finalization_failed"),
    ):
        if name in metrics and metrics.get(name) is not True:
            return reason
    return None


def is_recoverable_quarter_turn_metrics(metrics: Mapping[str, object]) -> bool:
    """Allow only a clean measured target discrepancy to reach reconciliation."""

    required_terminal_metrics = (
        "active_cubie_geometry_valid",
        "active_cubie_geometry_reason",
        "core_orientation_error_rad",
        "non_active_cubie_orientation_displacement_rad",
        "max_contact_force_n",
        "contact_force_limit_n",
        "physically_finalized",
        "fixture_locked",
        "transport_safely_finalized",
    )
    return (
        isinstance(metrics, Mapping)
        and all(name in metrics for name in required_terminal_metrics)
        and metrics.get("abort_reason")
        in ("wrist_rotation_wrong_direction", "permutation_mismatch")
        and metrics.get("success_tolerance_met") is False
        and quarter_turn_hard_safety_reason(metrics) is None
    )


def evaluate_quarter_turn(
    *,
    move: str,
    initial_angle_rad: float,
    final_angle_rad: float,
    final_angular_velocity_rad_s: float,
    left_contact_forces_n: Sequence[float],
    right_contact_forces_n: Sequence[float],
    wrist_axis_delta_rad: float,
    core_pose_error_m: float,
    active_cubie_alignment_error_m: float | None,
    non_active_cubie_displacement_m: float,
    permutation_matches: bool,
    native_pose_window_valid: bool = False,
    active_cubie_target_position_error_m: float | None = 0.0,
    active_cubie_geometry_valid: bool = True,
    active_cubie_geometry_reason: str | None = None,
    core_orientation_error_rad: float = 0.0,
    non_active_cubie_orientation_displacement_rad: float = 0.0,
    max_contact_force_n: float | None = None,
    contact_force_limit_n: float | None = None,
    fixture_locked: bool = True,
    transport_safely_finalized: bool = True,
    abort_reason: str | None = None,
    used_internal_constraint_switching: bool = True,
    used_direct_cubie_state_during_move: bool = False,
    used_direct_core_pose_during_move: bool = False,
    used_active_cube_drive: bool = False,
    used_constraint_switching_outside_fixture_lifecycle: bool = False,
    used_hard_joint_limit: bool = False,
    used_target_snapping: bool = False,
    used_robot_cube_attachment: bool = False,
    predicted_state_committed: bool = False,
    used_passive_detent: bool = True,
    minimum_observed_contact_n: float | None = None,
    minimum_maintained_contact_n: float | None = None,
) -> dict[str, object]:
    """Evaluate one hybrid-cube atomic turn without accepting hidden actuation."""

    requested_delta = move_delta_rad(move)
    target_angle = initial_angle_rad + requested_delta
    angle_error = abs(final_angle_rad - target_angle)
    if minimum_observed_contact_n is None:
        threshold = CONTACT_OBSERVED_THRESHOLD_N
        comparison = '>'
        left_observed = any(force > threshold for force in left_contact_forces_n)
        right_observed = any(force > threshold for force in right_contact_forces_n)
    else:
        threshold = float(minimum_observed_contact_n)
        if not math.isfinite(threshold) or threshold <= 0:
            raise ValueError('invalid observed contact threshold')
        comparison = '>='
        left_observed = any(force >= threshold for force in left_contact_forces_n)
        right_observed = any(force >= threshold for force in right_contact_forces_n)
    maintained_fraction = _contact_fraction(left_contact_forces_n, right_contact_forces_n,
        minimum_maintained_contact_n=minimum_maintained_contact_n)
    strict_violation = any(
        value is True
        for value in (
            used_direct_cubie_state_during_move,
            used_direct_core_pose_during_move,
            used_active_cube_drive,
            used_constraint_switching_outside_fixture_lifecycle,
            used_hard_joint_limit,
            used_target_snapping,
            used_robot_cube_attachment,
            predicted_state_committed,
        )
    )

    metrics: dict[str, object] = {
        "move": move,
        "initial_angle_rad": float(initial_angle_rad),
        "target_angle_rad": float(target_angle),
        "final_angle_rad": float(final_angle_rad),
        "angle_error_rad": float(angle_error),
        "final_angular_velocity_rad_s": float(final_angular_velocity_rad_s),
        "native_pose_window_valid": native_pose_window_valid,
        "contact_observed_threshold_n": float(threshold),
        "contact_observed_comparison": comparison,
        "left_contact_observed": left_observed,
        "right_contact_observed": right_observed,
        "contact_maintained_threshold_n": float(CONTACT_MAINTAINED_THRESHOLD_N
            if minimum_maintained_contact_n is None else minimum_maintained_contact_n),
        "contact_maintained_comparison": '>' if minimum_maintained_contact_n is None else '>=',
        "contact_maintained_fraction": float(maintained_fraction),
        "wrist_axis_delta_rad": float(wrist_axis_delta_rad),
        "core_pose_error_m": float(core_pose_error_m),
        "active_cubie_alignment_error_m": (
            None
            if active_cubie_alignment_error_m is None
            else float(active_cubie_alignment_error_m)
        ),
        "active_cubie_target_position_error_m": (
            None
            if active_cubie_target_position_error_m is None
            else float(active_cubie_target_position_error_m)
        ),
        "active_cubie_geometry_valid": active_cubie_geometry_valid,
        "active_cubie_geometry_reason": active_cubie_geometry_reason,
        "non_active_cubie_displacement_m": float(non_active_cubie_displacement_m),
        "core_orientation_error_rad": float(core_orientation_error_rad),
        "non_active_cubie_orientation_displacement_rad": float(
            non_active_cubie_orientation_displacement_rad
        ),
        "permutation_matches": bool(permutation_matches),
        "used_internal_constraint_switching": bool(used_internal_constraint_switching),
        "used_direct_cubie_state_during_move": used_direct_cubie_state_during_move,
        "used_direct_core_pose_during_move": used_direct_core_pose_during_move,
        "used_active_cube_drive": used_active_cube_drive,
        "used_constraint_switching_outside_fixture_lifecycle": (
            used_constraint_switching_outside_fixture_lifecycle
        ),
        "used_hard_joint_limit": used_hard_joint_limit,
        "used_target_snapping": used_target_snapping,
        "used_robot_cube_attachment": used_robot_cube_attachment,
        "predicted_state_committed": predicted_state_committed,
        "used_passive_detent": bool(used_passive_detent),
        "fixture_locked": bool(fixture_locked),
        "transport_safely_finalized": bool(transport_safely_finalized),
    }
    if max_contact_force_n is not None or contact_force_limit_n is not None:
        metrics["max_contact_force_n"] = (
            None if max_contact_force_n is None else float(max_contact_force_n)
        )
        metrics["contact_force_limit_n"] = (
            None if contact_force_limit_n is None else float(contact_force_limit_n)
        )
    hard_safety_reason = quarter_turn_hard_safety_reason(metrics)
    reason = abort_reason
    if reason is None and strict_violation:
        reason = "strict_mode_violation"
    if reason is None and not used_internal_constraint_switching:
        reason = "internal_constraint_switching_missing"
    if reason is None and not used_passive_detent:
        reason = "passive_detent_missing"
    if reason is None and wrist_axis_delta_rad * requested_delta <= 0.0:
        reason = "wrist_rotation_wrong_direction"
    if reason is None and hard_safety_reason is not None:
        reason = hard_safety_reason
    if reason is None and angle_error > HYBRID_ANGLE_TOLERANCE_RAD + 1e-12:
        reason = "angle_tolerance_exceeded"
    if reason is None and not permutation_matches:
        reason = "permutation_mismatch"
    metrics["success_tolerance_met"] = reason is None
    metrics["abort_reason"] = reason
    return metrics


def evaluate_twist(
    *,
    move: str,
    initial_angle_rad: float,
    final_angle_rad: float,
    final_joint_velocity_rad_s: float,
    left_contact_forces_n: Sequence[float],
    right_contact_forces_n: Sequence[float],
    left_contact_observation_forces_n: Sequence[float] | None = None,
    right_contact_observation_forces_n: Sequence[float] | None = None,
    wrist_yaw_delta_rad: float,
    base_pose_error_m: float,
    abort_reason: str | None = None,
    used_direct_cube_joint_state: bool = False,
    used_cube_joint_drive: bool = False,
    used_kinematic_attachment: bool = False,
) -> dict[str, float | bool | str | None]:
    """Evaluate one run against the strict physical-contact acceptance contract."""

    requested_delta = move_delta_rad(move)
    target_angle = wrap_angle(initial_angle_rad + requested_delta)
    error = angle_error_rad(final_angle_rad, target_angle)
    left_observation_forces = (
        left_contact_forces_n
        if left_contact_observation_forces_n is None
        else left_contact_observation_forces_n
    )
    right_observation_forces = (
        right_contact_forces_n
        if right_contact_observation_forces_n is None
        else right_contact_observation_forces_n
    )
    left_observed = any(force > CONTACT_OBSERVED_THRESHOLD_N for force in left_observation_forces)
    right_observed = any(force > CONTACT_OBSERVED_THRESHOLD_N for force in right_observation_forces)
    maintained_fraction = _contact_fraction(left_contact_forces_n, right_contact_forces_n)
    strict_violation = any(
        (used_direct_cube_joint_state, used_cube_joint_drive, used_kinematic_attachment)
    )

    reason = abort_reason
    if reason is None and strict_violation:
        reason = "strict_mode_violation"
    if reason is None and wrist_yaw_delta_rad * requested_delta <= 0.0:
        reason = "wrist_rotation_wrong_direction"
    if reason is None and error > ANGLE_TOLERANCE_RAD + 1e-12:
        reason = "angle_tolerance_exceeded"
    if reason is None and abs(final_joint_velocity_rad_s) > JOINT_VELOCITY_TOLERANCE_RAD_S + 1e-12:
        reason = "cube_joint_unsettled"
    if reason is None and not left_observed:
        reason = "left_contact_missing"
    if reason is None and not right_observed:
        reason = "right_contact_missing"
    if reason is None and maintained_fraction + 1e-12 < CONTACT_MAINTAINED_FRACTION:
        reason = "contact_maintenance_below_threshold"
    if reason is None and abs(wrist_yaw_delta_rad) + 1e-12 < WRIST_YAW_MINIMUM_RAD:
        reason = "wrist_rotation_insufficient"
    if reason is None and base_pose_error_m > BASE_POSE_TOLERANCE_M + 1e-12:
        reason = "base_pose_drift"

    return {
        "move": move,
        "initial_angle_rad": float(initial_angle_rad),
        "target_angle_rad": float(target_angle),
        "final_angle_rad": float(final_angle_rad),
        "angle_error_rad": float(error),
        "final_joint_velocity_rad_s": float(final_joint_velocity_rad_s),
        "left_contact_observed": left_observed,
        "right_contact_observed": right_observed,
        "contact_maintained_fraction": float(maintained_fraction),
        "wrist_yaw_delta_rad": float(wrist_yaw_delta_rad),
        "base_pose_error_m": float(base_pose_error_m),
        "success_tolerance_met": reason is None,
        "abort_reason": reason,
        "used_direct_cube_joint_state": bool(used_direct_cube_joint_state),
        "used_cube_joint_drive": bool(used_cube_joint_drive),
        "used_kinematic_attachment": bool(used_kinematic_attachment),
    }
