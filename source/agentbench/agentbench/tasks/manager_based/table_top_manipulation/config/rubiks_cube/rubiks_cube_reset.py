"""Pure validation and reset geometry for the hybrid Rubik's Cube."""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Real
from typing import Mapping, Sequence

try:
    from .rubiks_cube_geometry import (
        CUBIE_PITCH_M,
        CUBIE_SIZE_M,
        sticker_box_transform,
    )
    from .rubiks_cube_mechanism import ConstraintFrame, is_legal_cube_state
    from .rubiks_cube_pose import multiply_quaternions, quaternion_from_yaw_and_frame
    from .rubiks_cube_rules import CubeFrame, CubeState, CubieState
except ImportError:  # Loaded directly by dependency-light unit tests.
    try:
        from rubiks_cube_geometry import (
            CUBIE_PITCH_M,
            CUBIE_SIZE_M,
            sticker_box_transform,
        )
    except ImportError:
        # Direct file loaders do not add this directory to ``sys.path``.  Load
        # the dependency-light owner explicitly without defining a second
        # geometry constant in this module.
        import importlib.util
        from pathlib import Path
        import sys

        _geometry_spec = importlib.util.spec_from_file_location(
            "rubiks_cube_geometry", Path(__file__).with_name("rubiks_cube_geometry.py")
        )
        if _geometry_spec is None or _geometry_spec.loader is None:
            raise ImportError("unable to load rubiks_cube_geometry")
        _geometry_module = importlib.util.module_from_spec(_geometry_spec)
        sys.modules["rubiks_cube_geometry"] = _geometry_module
        _geometry_spec.loader.exec_module(_geometry_module)
        for _geometry_name in (
            "CUBIE_PITCH_M",
            "CUBIE_SIZE_M",
            "sticker_box_transform",
        ):
            globals()[_geometry_name] = getattr(_geometry_module, _geometry_name)
    from rubiks_cube_mechanism import ConstraintFrame, is_legal_cube_state
    from rubiks_cube_pose import multiply_quaternions, quaternion_from_yaw_and_frame
    from rubiks_cube_rules import CubeFrame, CubeState, CubieState

_TRANSFORM_TOLERANCE = 1e-8
_MAX_INITIAL_TILT_RAD = math.radians(3.0)
_TILT_LIMIT_TOLERANCE_RAD = 1e-12

Matrix3 = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]


class CubeResetExecutionError(RuntimeError):
    """Reset failure carrying authoritative direct-write boundary truth."""

    __slots__ = ("_used_direct_cubie_state_during_reset",)

    def __init__(
        self,
        reason: str,
        *,
        used_direct_cubie_state_during_reset: bool,
    ) -> None:
        if not isinstance(used_direct_cubie_state_during_reset, bool):
            raise TypeError(
                "used_direct_cubie_state_during_reset must be a bool"
            )
        super().__init__(reason)
        self._used_direct_cubie_state_during_reset = (
            used_direct_cubie_state_during_reset
        )

    @property
    def used_direct_cubie_state_during_reset(self) -> bool:
        """Whether the failing reset crossed the direct-state-write boundary."""

        return self._used_direct_cubie_state_during_reset


@dataclass(frozen=True)
class CubeResetSpec:
    """A complete legal cube state and its requested face-supported world pose."""

    cube_state: CubeState
    logical_orientation: CubeFrame
    center_position: tuple[float, float, float]
    yaw_rad: float
    tilt_xy_rad: tuple[float, float] = (0.0, 0.0)

    def __post_init__(self) -> None:
        validate_reset_spec(self)


def _as_finite_tuple(
    values: Sequence[float], expected_length: int, label: str
) -> tuple[float, ...]:
    try:
        raw = tuple(values)
    except TypeError as error:
        raise ValueError(f"{label} must contain {expected_length} finite values") from error
    if len(raw) != expected_length or any(
        isinstance(value, bool) or not isinstance(value, Real) for value in raw
    ):
        raise ValueError(f"{label} must contain {expected_length} finite values")
    converted = tuple(float(value) for value in raw)
    if not all(math.isfinite(value) for value in converted):
        raise ValueError(f"{label} must contain {expected_length} finite values")
    return converted


def validate_legal_cube_state(state: CubeState) -> None:
    """Raise if ``state`` is not an exact, complete member of the cube group."""

    if not isinstance(state, CubeState):
        raise ValueError("cube state must be a CubeState")
    solved = CubeState.solved()
    pieces = state.pieces
    if not isinstance(pieces, dict) or set(pieces) != set(solved.pieces):
        raise ValueError("cube state must contain exactly all 26 cubies")

    valid_orientations = {frame.logical_to_world for frame in CubeFrame.all()}
    occupied: set[tuple[int, int, int]] = set()
    for identity, reference in solved.pieces.items():
        piece = pieces[identity]
        if not isinstance(piece, CubieState):
            raise ValueError(f"cubie {identity} must be a CubieState")
        if (
            piece.identity != identity
            or piece.home_position != reference.home_position
            or piece.stickers != reference.stickers
        ):
            raise ValueError(f"cubie metadata does not match identity: {identity}")
        position = piece.position
        if (
            not isinstance(position, tuple)
            or len(position) != 3
            or any(
                isinstance(value, bool)
                or not isinstance(value, int)
                or value not in (-1, 0, 1)
                for value in position
            )
            or position == (0, 0, 0)
        ):
            raise ValueError(f"cubie position is invalid: {identity}")
        if position in occupied:
            raise ValueError("cube state contains duplicate cubie positions")
        occupied.add(position)
        try:
            orientation_is_valid = piece.orientation in valid_orientations
        except TypeError:
            orientation_is_valid = False
        if not orientation_is_valid:
            raise ValueError(
                f"cubie orientation is not a proper signed-permutation rotation: {identity}"
            )

    # The shared group-membership implementation
    # covers fixed centers, sticker/slot reachability, edge flips, corner
    # twists, center orientation parity, and edge/corner permutation parity.
    if not is_legal_cube_state(state):
        raise ValueError("cube state violates Rubik's Cube legality invariants")


def validate_reset_spec(spec: CubeResetSpec) -> None:
    """Validate every value needed to prepare a reset before simulator writes."""

    if not isinstance(spec, CubeResetSpec):
        raise ValueError("reset spec must be a CubeResetSpec")
    validate_legal_cube_state(spec.cube_state)
    if (
        not isinstance(spec.logical_orientation, CubeFrame)
        or spec.logical_orientation not in CubeFrame.all()
    ):
        raise ValueError("logical_orientation must be an exact legal CubeFrame")
    _as_finite_tuple(spec.center_position, 3, "center_position")
    if (
        isinstance(spec.yaw_rad, bool)
        or not isinstance(spec.yaw_rad, Real)
        or not math.isfinite(float(spec.yaw_rad))
    ):
        raise ValueError("yaw_rad must be finite")
    tilt = _as_finite_tuple(spec.tilt_xy_rad, 2, "tilt_xy_rad")
    if math.hypot(*tilt) > _MAX_INITIAL_TILT_RAD + _TILT_LIMIT_TOLERANCE_RAD:
        raise ValueError("tilt_xy_rad total tilt must not exceed 3 degrees")


def snapshot_cube_state(state: CubeState) -> CubeState:
    """Return a validated canonical copy with no caller-owned mutable mapping."""

    validate_legal_cube_state(state)
    snapshot = CubeState(
        {
            identity: CubieState(
                identity=str(piece.identity),
                home_position=tuple(int(value) for value in piece.home_position),
                position=tuple(int(value) for value in piece.position),
                orientation=tuple(
                    tuple(int(value) for value in row)
                    for row in piece.orientation
                ),
                stickers=tuple(str(sticker) for sticker in piece.stickers),
            )
            for identity, piece in sorted(state.pieces.items())
        }
    )
    validate_legal_cube_state(snapshot)
    return snapshot


def snapshot_reset_spec(spec: CubeResetSpec) -> CubeResetSpec:
    """Return a complete validated reset transaction owned by the receiver."""

    validate_reset_spec(spec)
    frame = CubeFrame(
        tuple(
            tuple(int(value) for value in row)
            for row in spec.logical_orientation.logical_to_world
        )
    )
    center = tuple(float(value) for value in spec.center_position)
    tilt = tuple(float(value) for value in spec.tilt_xy_rad)
    snapshot = CubeResetSpec(
        cube_state=snapshot_cube_state(spec.cube_state),
        logical_orientation=frame,
        center_position=center,  # type: ignore[arg-type]
        yaw_rad=float(spec.yaw_rad),
        tilt_xy_rad=tilt,  # type: ignore[arg-type]
    )
    validate_reset_spec(snapshot)
    return snapshot


def _mat_vec(
    matrix: Sequence[Sequence[float]], vector: Sequence[float]
) -> tuple[float, float, float]:
    return tuple(
        sum(a * b for a, b in zip(row, vector, strict=True)) for row in matrix
    )  # type: ignore[return-value]


def _tilt_quaternion(
    tilt_xy_rad: Sequence[float],
) -> tuple[float, float, float, float]:
    tilt_x, tilt_y = tilt_xy_rad
    angle = math.hypot(tilt_x, tilt_y)
    if angle == 0.0:
        return (1.0, 0.0, 0.0, 0.0)
    axis_scale = math.sin(0.5 * angle) / angle
    return (
        math.cos(0.5 * angle),
        tilt_x * axis_scale,
        tilt_y * axis_scale,
        0.0,
    )


def _whole_cube_quaternion(
    spec: CubeResetSpec, frame: CubeFrame | None = None
) -> tuple[float, float, float, float]:
    yaw_and_frame = quaternion_from_yaw_and_frame(
        float(spec.yaw_rad), frame or spec.logical_orientation
    )
    if tuple(spec.tilt_xy_rad) == (0.0, 0.0):
        return yaw_and_frame
    return multiply_quaternions(_tilt_quaternion(spec.tilt_xy_rad), yaw_and_frame)


def _quaternion_to_matrix(quaternion: Sequence[float]) -> Matrix3:
    w, x, y, z = quaternion
    return (
        (
            1.0 - 2.0 * (y * y + z * z),
            2.0 * (x * y - w * z),
            2.0 * (x * z + w * y),
        ),
        (
            2.0 * (x * y + w * z),
            1.0 - 2.0 * (x * x + z * z),
            2.0 * (y * z - w * x),
        ),
        (
            2.0 * (x * z - w * y),
            2.0 * (y * z + w * x),
            1.0 - 2.0 * (x * x + y * y),
        ),
    )


def _rotate_by_quaternion(
    vector: Sequence[float], quaternion: Sequence[float]
) -> tuple[float, float, float]:
    return _mat_vec(_quaternion_to_matrix(quaternion), vector)


def _world_offset(
    spec: CubeResetSpec, logical_offset: Sequence[float]
) -> tuple[float, float, float]:
    if tuple(spec.tilt_xy_rad) != (0.0, 0.0):
        return _rotate_by_quaternion(logical_offset, _whole_cube_quaternion(spec))

    # Preserve the exact arithmetic of the established yaw-only path. Building
    # an equivalent rotation matrix through a quaternion changes a few low bits
    # for some discrete frames.
    framed = _mat_vec(
        spec.logical_orientation.logical_to_world, logical_offset
    )
    cosine = math.cos(float(spec.yaw_rad))
    sine = math.sin(float(spec.yaw_rad))
    return (
        cosine * framed[0] - sine * framed[1],
        sine * framed[0] + cosine * framed[1],
        framed[2],
    )


def _validate_constraint_frame(frame: ConstraintFrame, label: str) -> None:
    if not isinstance(frame, ConstraintFrame):
        raise ValueError(f"{label} transform must be a ConstraintFrame")
    _as_finite_tuple(frame.position, 3, f"{label} position")
    quaternion = _as_finite_tuple(frame.quaternion, 4, f"{label} quaternion")
    if abs(math.hypot(*quaternion) - 1.0) > _TRANSFORM_TOLERANCE:
        raise ValueError(f"{label} quaternion must be normalized")


def build_reset_core_transform(spec: CubeResetSpec) -> ConstraintFrame:
    """Return the requested core transform as a finite WXYZ frame."""

    validate_reset_spec(spec)
    frame = ConstraintFrame(
        position=tuple(float(value) for value in spec.center_position),
        quaternion=_whole_cube_quaternion(spec),
    )
    _validate_constraint_frame(frame, "core")
    return frame


def build_reset_world_anchor_frame(
    spec: CubeResetSpec,
    *,
    canonical_anchor_position: Sequence[float],
) -> ConstraintFrame:
    """Return the core target relative to the canonical identity anchor.

    The USD ``world_anchor`` body is kinematic and remains at its canonical
    world pose.  Reset-time translation and orientation therefore belong to
    the local frame of ``world_core_anchor`` rather than to a mixed rigid-body
    collection transform write.
    """

    validate_reset_spec(spec)
    anchor_position = _as_finite_tuple(
        canonical_anchor_position, 3, "canonical anchor position"
    )
    core = build_reset_core_transform(spec)
    frame = ConstraintFrame(
        position=tuple(
            target - anchor
            for target, anchor in zip(
                core.position, anchor_position, strict=True
            )
        ),
        quaternion=tuple(core.quaternion),
    )
    _validate_constraint_frame(frame, "world core anchor")
    return frame


def build_reset_body_transforms(
    spec: CubeResetSpec,
) -> dict[str, ConstraintFrame]:
    """Build all 26 cubie world transforms implied by ``spec``."""

    validate_reset_spec(spec)
    center = tuple(float(value) for value in spec.center_position)
    transforms: dict[str, ConstraintFrame] = {}
    for identity, piece in spec.cube_state.pieces.items():
        logical_offset = tuple(
            coordinate * CUBIE_PITCH_M for coordinate in piece.position
        )
        world_offset = _world_offset(spec, logical_offset)
        world_piece_frame = spec.logical_orientation.compose(
            CubeFrame(piece.orientation)
        )
        transform = ConstraintFrame(
            position=tuple(
                center_coordinate + offset
                for center_coordinate, offset in zip(
                    center, world_offset, strict=True
                )
            ),
            quaternion=_whole_cube_quaternion(spec, world_piece_frame),
        )
        _validate_constraint_frame(transform, identity)
        transforms[identity] = transform

    reconstructed = reconstruct_cube_state(transforms, spec)
    if reconstructed != spec.cube_state:
        raise ValueError("reset transforms do not reconstruct the requested cube state")
    return transforms


def build_reset_constraint_frames(
    state: CubeState,
) -> dict[str, ConstraintFrame]:
    """Build core-relative cubie frames for the reset backend transaction."""

    validate_legal_cube_state(state)
    frames = {
        identity: ConstraintFrame(
            position=tuple(
                float(coordinate * CUBIE_PITCH_M) for coordinate in piece.position
            ),
            quaternion=quaternion_from_yaw_and_frame(
                0.0, CubeFrame(piece.orientation)
            ),
        )
        for identity, piece in state.pieces.items()
    }
    for identity, frame in frames.items():
        _validate_constraint_frame(frame, identity)
    return frames


def _normalize_quaternion(values: Sequence[float], label: str) -> tuple[float, ...]:
    quaternion = _as_finite_tuple(values, 4, label)
    norm = math.hypot(*quaternion)
    if norm == 0.0:
        raise ValueError(f"{label} must be a nonzero quaternion")
    return tuple(value / norm for value in quaternion)


def reconstruct_cube_state(
    transforms: Mapping[str, ConstraintFrame], spec: CubeResetSpec
) -> CubeState:
    """Reconstruct a discrete state from validated reset world transforms."""

    validate_reset_spec(spec)
    solved = CubeState.solved()
    if not isinstance(transforms, Mapping) or set(transforms) != set(solved.pieces):
        raise ValueError("reset transforms must contain all 26 cubies")
    center = tuple(float(value) for value in spec.center_position)
    whole_cube_quaternion = _whole_cube_quaternion(spec)
    inverse_whole_cube_quaternion = (
        whole_cube_quaternion[0],
        -whole_cube_quaternion[1],
        -whole_cube_quaternion[2],
        -whole_cube_quaternion[3],
    )
    orientation_candidates = tuple(
        (
            frame,
            _whole_cube_quaternion(spec, spec.logical_orientation.compose(frame)),
        )
        for frame in CubeFrame.all()
    )
    occupied: set[tuple[int, int, int]] = set()
    pieces: dict[str, CubieState] = {}
    for identity, reference in solved.pieces.items():
        transform = transforms[identity]
        _validate_constraint_frame(transform, identity)
        delta = tuple(
            measured - origin
            for measured, origin in zip(transform.position, center, strict=True)
        )
        logical_offset = _rotate_by_quaternion(
            delta, inverse_whole_cube_quaternion
        )
        position = tuple(
            int(round(coordinate / CUBIE_PITCH_M)) for coordinate in logical_offset
        )
        if any(
            abs(measured - discrete * CUBIE_PITCH_M) > _TRANSFORM_TOLERANCE
            for measured, discrete in zip(logical_offset, position, strict=True)
        ):
            raise ValueError(f"cubie reset position is off-grid: {identity}")
        if position in occupied:
            raise ValueError("reset transforms contain duplicate cubie positions")
        occupied.add(position)  # type: ignore[arg-type]

        measured_quaternion = _normalize_quaternion(
            transform.quaternion, f"{identity} quaternion"
        )
        piece_frame, alignment = min(
            (
                (
                    frame,
                    abs(
                        sum(
                            actual * expected
                            for actual, expected in zip(
                                measured_quaternion,
                                expected_quaternion,
                                strict=True,
                            )
                        )
                    ),
                )
                for frame, expected_quaternion in orientation_candidates
            ),
            key=lambda candidate: -candidate[1],
        )
        if 1.0 - alignment > _TRANSFORM_TOLERANCE:
            raise ValueError(f"cubie reset orientation is off-grid: {identity}")
        pieces[identity] = CubieState(
            identity=identity,
            home_position=reference.home_position,
            position=position,  # type: ignore[arg-type]
            orientation=piece_frame.logical_to_world,
            stickers=reference.stickers,
        )

    state = CubeState(pieces)
    validate_legal_cube_state(state)
    return state


def reset_support_center_z(
    spec: CubeResetSpec,
    *,
    table_height_m: float,
    include_stickers: bool = True,
) -> float:
    """Return core Z placing the lowest requested geometry on the table.

    ``include_stickers=False`` gives collision support from cubie bodies only;
    the default also includes the visible sticker boxes.
    """

    validate_reset_spec(spec)
    if (
        isinstance(table_height_m, bool)
        or not isinstance(table_height_m, Real)
        or not math.isfinite(float(table_height_m))
    ):
        raise ValueError("table_height_m must be a finite real scalar")
    if not isinstance(include_stickers, bool):
        raise ValueError("include_stickers must be a bool")

    whole_rotation = _quaternion_to_matrix(_whole_cube_quaternion(spec))
    lowest_relative_z = math.inf
    for piece in spec.cube_state.pieces.values():
        logical_center = tuple(
            coordinate * CUBIE_PITCH_M for coordinate in piece.position
        )
        cubie_center = _mat_vec(whole_rotation, logical_center)
        cubie_quaternion = _whole_cube_quaternion(
            spec,
            spec.logical_orientation.compose(CubeFrame(piece.orientation)),
        )
        cubie_rotation = _quaternion_to_matrix(cubie_quaternion)
        cubie_half_extent = 0.5 * CUBIE_SIZE_M
        cubie_vertical_radius = cubie_half_extent * sum(
            abs(component) for component in cubie_rotation[2]
        )
        lowest_relative_z = min(
            lowest_relative_z, cubie_center[2] - cubie_vertical_radius
        )

        if include_stickers:
            for face in piece.stickers:
                sticker_offset, dimensions = sticker_box_transform(face)
                sticker_center_offset = _mat_vec(cubie_rotation, sticker_offset)
                sticker_center_z = cubie_center[2] + sticker_center_offset[2]
                sticker_vertical_radius = sum(
                    abs(cubie_rotation[2][axis]) * 0.5 * dimensions[axis]
                    for axis in range(3)
                )
                lowest_relative_z = min(
                    lowest_relative_z,
                    sticker_center_z - sticker_vertical_radius,
                )

    return float(table_height_m) - lowest_relative_z
