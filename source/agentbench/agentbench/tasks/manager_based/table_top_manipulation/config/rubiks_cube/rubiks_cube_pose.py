"""Pure interpretation of continuous, face-supported Rubik's Cube poses."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from functools import lru_cache
import math
from typing import Sequence

try:
    from .rubiks_cube_rules import CubeFrame, HYBRID_ANGLE_TOLERANCE_RAD
except ImportError:  # Loaded directly by dependency-light unit tests.
    from rubiks_cube_rules import CubeFrame, HYBRID_ANGLE_TOLERANCE_RAD


DEFAULT_TILT_TOLERANCE_RAD = HYBRID_ANGLE_TOLERANCE_RAD
DEFAULT_LINEAR_SPEED_TOLERANCE_M_S = 0.02
DEFAULT_ANGULAR_SPEED_TOLERANCE_RAD_S = 0.1

_FACTOR_TIE_TOLERANCE_RAD = 1e-9
_POSE_WINDOW_ROUNDING_TOLERANCE = 1e-12

Matrix3 = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]
WorkspaceXYBounds = tuple[tuple[float, float], tuple[float, float]]
PoseTransformSample = tuple[
    tuple[float, float, float], tuple[float, float, float, float]
]
IndexedPoseTransformSample = tuple[
    int, tuple[float, float, float], tuple[float, float, float, float]
]


class PoseStatus(str, Enum):
    STABLE = "stable"
    MOVING = "moving"
    NONCANONICAL = "noncanonical"
    OUT_OF_WORKSPACE = "out_of_workspace"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class PhysicalCubePose:
    position: tuple[float, float, float]
    quaternion: tuple[float, float, float, float]
    logical_orientation: CubeFrame | None
    support_face: str | None
    yaw_rad: float | None
    tilt_rad: float
    linear_speed_m_s: float
    angular_speed_rad_s: float
    status: PoseStatus


@dataclass(frozen=True)
class _FactorCandidate:
    frame: CubeFrame
    yaw_rad: float
    tilt_rad: float


@dataclass(frozen=True)
class FaceSupportedPoseFactorization:
    """One raw-pose-preserving factorization authorized by a frame tie."""

    pose: PhysicalCubePose
    reconstruction_error_rad: float


def multiply_quaternions(
    first: Sequence[float], second: Sequence[float]
) -> tuple[float, float, float, float]:
    """Compose active WXYZ rotations, applying ``second`` before ``first``."""

    w1, x1, y1, z1 = first
    w2, x2, y2, z2 = second
    return (
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
    )


def _finite_pose_tuple(value, length: int, label: str) -> tuple[float, ...]:
    if not isinstance(value, (list, tuple)) or len(value) != length:
        raise ValueError(f"{label} must contain exactly {length} values")
    converted = []
    for item in value:
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise TypeError(f"{label} values must be real numbers")
        number = float(item)
        if not math.isfinite(number):
            raise ValueError(f"{label} values must be finite")
        converted.append(number)
    return tuple(converted)


def _normalized_pose_quaternion(value, label: str) -> tuple[float, float, float, float]:
    quaternion = _finite_pose_tuple(value, 4, label)
    scale = max(abs(component) for component in quaternion)
    if scale == 0.0:
        raise ValueError(f"{label} must be nonzero")
    scaled = tuple(component / scale for component in quaternion)
    norm = math.hypot(*scaled)
    return tuple(component / norm for component in scaled)  # type: ignore[return-value]


def _stable_wxyz_distance_rad(first, second) -> float:
    first_quaternion = _normalized_pose_quaternion(first, "first pose quaternion")
    second_quaternion = _normalized_pose_quaternion(second, "second pose quaternion")
    relative = multiply_quaternions(
        second_quaternion,
        (
            first_quaternion[0],
            -first_quaternion[1],
            -first_quaternion[2],
            -first_quaternion[3],
        ),
    )
    normalized_relative = _normalized_pose_quaternion(
        relative, "relative pose quaternion"
    )
    return 2.0 * math.atan2(
        math.hypot(*normalized_relative[1:]), abs(normalized_relative[0])
    )


def pose_window_drift_speed(
    samples: Sequence[PoseTransformSample], *, physics_dt_s: float
) -> tuple[float, float]:
    """Measure rigid-pose drift across one contiguous simulation window."""

    if isinstance(physics_dt_s, bool) or not isinstance(physics_dt_s, (int, float)):
        raise TypeError("physics_dt_s must be a finite positive number")
    physics_dt = float(physics_dt_s)
    if not math.isfinite(physics_dt) or physics_dt <= 0.0:
        raise ValueError("physics_dt_s must be a finite positive number")
    if not isinstance(samples, (list, tuple)) or len(samples) < 2:
        raise ValueError("pose window must contain at least two samples")
    parsed = []
    for sample in samples:
        if not isinstance(sample, (list, tuple)) or len(sample) != 2:
            raise ValueError("pose samples must contain exactly position and quaternion")
        parsed.append(
            (
                _finite_pose_tuple(sample[0], 3, "pose position"),
                _normalized_pose_quaternion(sample[1], "pose quaternion"),
            )
        )
    first_position, first_quaternion = parsed[0]
    final_position, final_quaternion = parsed[-1]
    elapsed = (len(parsed) - 1) * physics_dt
    linear = math.dist(first_position, final_position) / elapsed
    angular = _stable_wxyz_distance_rad(first_quaternion, final_quaternion) / elapsed
    return linear, angular


def contiguous_pose_window_drift_speed(
    samples: Sequence[IndexedPoseTransformSample],
    *,
    physics_dt_s: float,
    window_steps: int,
) -> tuple[float, float]:
    """Measure one exact, adjacent-step rigid-pose window."""

    if isinstance(window_steps, bool) or not isinstance(window_steps, int):
        raise TypeError("window_steps must be an integer")
    if window_steps < 2:
        raise ValueError("window_steps must span at least two physics steps")
    if not isinstance(samples, (list, tuple)) or len(samples) != window_steps:
        raise ValueError("pose window length differs from window_steps")
    parsed: list[IndexedPoseTransformSample] = []
    for sample in samples:
        if not isinstance(sample, (list, tuple)) or len(sample) != 3:
            raise ValueError("indexed pose samples must contain step, position, quaternion")
        step = sample[0]
        if isinstance(step, bool) or not isinstance(step, int):
            raise TypeError("pose sample step must be an integer")
        if step < 0:
            raise ValueError("pose sample step must be non-negative")
        parsed.append(
            (
                step,
                _finite_pose_tuple(sample[1], 3, "pose position"),  # type: ignore[arg-type]
                _normalized_pose_quaternion(sample[2], "pose quaternion"),  # type: ignore[arg-type]
            )
        )
    if any(
        current[0] != previous[0] + 1
        for previous, current in zip(parsed, parsed[1:])
    ):
        raise ValueError("pose window physics steps must be contiguous")
    return pose_window_drift_speed(
        [(position, quaternion) for _, position, quaternion in parsed],
        physics_dt_s=physics_dt_s,
    )


def _unit_quaternion_diameter_scalar(quaternions) -> float:
    """All-pairs SO(3) diameter; inputs were validated and normalized once.

    atan2 is invariant to scaling the relative quaternion, so repeating its
    normalization for every pair changes no geometric test or tolerance.
    """
    maximum = 0.0
    for index, first in enumerate(quaternions):
        conjugate = (first[0], -first[1], -first[2], -first[3])
        for second in quaternions[index + 1:]:
            relative = multiply_quaternions(second, conjugate)
            angle = 2.0 * math.atan2(math.hypot(*relative[1:]), abs(relative[0]))
            maximum = max(maximum, angle)
    return maximum


@lru_cache(maxsize=1)
def _pose_window_numpy():
    # Geometry utilities remain usable without the optional scoring dependencies.
    try:
        import numpy
    except ModuleNotFoundError:
        return None
    return numpy


def _unit_quaternion_diameter_numpy(quaternions, np) -> float:
    """Rank every pair in float64, then return the original scalar maximum.

    The 1e-12 margin selects *additional candidates*, never stable poses. For
    normalized quaternions it exceeds the rounding error of these four-term
    products/hypot/atan2 operations by orders of magnitude. Near ties are all
    recomputed using exactly the old arithmetic and math.hypot/atan2, preserving
    boundary decisions and reported scalar values. No acos loss near zero.
    """
    first_indices, second_indices = np.triu_indices(len(quaternions), 1)
    values = np.asarray(quaternions, dtype=np.float64)
    w, x, y, z = values[second_indices].T
    first = values[first_indices].T
    v, s, t, u = first[0], -first[1], -first[2], -first[3]
    rw = w*v-x*s-y*t-z*u
    rx = w*s+x*v+y*u-z*t
    ry = w*t-x*u+y*v+z*s
    rz = w*u+x*t-y*s+z*v
    angles = 2*np.arctan2(np.hypot(np.hypot(rx, ry), rz), np.abs(rw))
    candidates = np.flatnonzero(angles >= float(angles.max())-1e-12)
    maximum = 0.0
    seen = set()
    for index in candidates:
        first = quaternions[int(first_indices[index])]
        second = quaternions[int(second_indices[index])]
        pair = (first, second)
        if pair in seen:
            continue
        seen.add(pair)
        relative = multiply_quaternions(second, (first[0], -first[1], -first[2], -first[3]))
        angle = 2.0*math.atan2(math.hypot(*relative[1:]), abs(relative[0]))
        maximum = max(maximum, angle)
    return maximum


def _unit_quaternion_diameter(quaternions) -> float:
    # Bound temporary quadratic storage; long or tiny windows keep the original
    # streaming implementation. The native 61/64-sample windows use NumPy.
    if 8 <= len(quaternions) <= 256:
        np = _pose_window_numpy()
        if np is not None:
            return _unit_quaternion_diameter_numpy(quaternions, np)
    return _unit_quaternion_diameter_scalar(quaternions)


def evaluate_contiguous_pose_window(
    samples: Sequence[IndexedPoseTransformSample],
    *,
    physics_dt_s: float,
    minimum_duration_s: float = 0.5,
    after_step: int | None = None,
    position_tolerance_m: float = 0.001,
    rotation_tolerance_rad: float = math.radians(1.0),
) -> dict:
    """Evaluate whole-window rigid-pose diameter for one observed body."""

    config_values = (
        (physics_dt_s, "physics_dt_s"),
        (minimum_duration_s, "minimum_duration_s"),
        (position_tolerance_m, "position_tolerance_m"),
        (rotation_tolerance_rad, "rotation_tolerance_rad"),
    )
    parsed_config = []
    for value, label in config_values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{label} must be a finite positive number")
        number = float(value)
        if not math.isfinite(number) or number <= 0.0:
            raise ValueError(f"{label} must be a finite positive number")
        parsed_config.append(number)
    physics_dt, minimum_duration, position_tolerance, rotation_tolerance = (
        parsed_config
    )
    if after_step is not None:
        if isinstance(after_step, bool) or not isinstance(after_step, int):
            raise TypeError("after_step must be a non-negative integer")
        if after_step < 0:
            raise ValueError("after_step must be a non-negative integer")
    if not isinstance(samples, (list, tuple)) or len(samples) < 2:
        raise ValueError("pose window must contain at least two samples")
    parsed: list[IndexedPoseTransformSample] = []
    for sample in samples:
        if not isinstance(sample, (list, tuple)) or len(sample) != 3:
            raise ValueError(
                "indexed pose samples must contain step, position, quaternion"
            )
        step = sample[0]
        if isinstance(step, bool) or not isinstance(step, int):
            raise TypeError("pose sample step must be an integer")
        if step < 0:
            raise ValueError("pose sample step must be non-negative")
        parsed.append(
            (
                step,
                _finite_pose_tuple(sample[1], 3, "pose position"),  # type: ignore[arg-type]
                _normalized_pose_quaternion(sample[2], "pose quaternion"),  # type: ignore[arg-type]
            )
        )
    if any(
        current[0] != previous[0] + 1
        for previous, current in zip(parsed, parsed[1:])
    ):
        raise ValueError("pose window physics steps must be contiguous")
    if after_step is not None and parsed[0][0] <= after_step:
        raise ValueError("first pose sample step must be greater than after_step")
    duration = (parsed[-1][0] - parsed[0][0]) * physics_dt
    if duration + _POSE_WINDOW_ROUNDING_TOLERANCE < minimum_duration:
        raise ValueError("pose window does not meet minimum duration")
    position_diameter = max(
        math.dist(first[1], second[1])
        for index, first in enumerate(parsed)
        for second in parsed[index + 1 :]
    )
    rotation_diameter = _unit_quaternion_diameter([sample[2] for sample in parsed])
    return {
        "stable": (
            position_diameter
            <= position_tolerance + _POSE_WINDOW_ROUNDING_TOLERANCE
            and rotation_diameter
            <= rotation_tolerance + _POSE_WINDOW_ROUNDING_TOLERANCE
        ),
        "sample_count": len(parsed),
        "first_native_step": parsed[0][0],
        "last_native_step": parsed[-1][0],
        "duration_s": duration,
        "after_step": after_step,
        "position_diameter_m": position_diameter,
        "rotation_diameter_rad": rotation_diameter,
        "position_tolerance_m": position_tolerance,
        "rotation_tolerance_rad": rotation_tolerance,
    }


def axis_angle_quaternion(
    axis: str, angle_rad: float
) -> tuple[float, float, float, float]:
    """Return an active WXYZ quaternion about a world coordinate axis."""

    unit_axis = {
        "X": (1.0, 0.0, 0.0),
        "Y": (0.0, 1.0, 0.0),
        "Z": (0.0, 0.0, 1.0),
    }.get(axis.upper())
    if unit_axis is None:
        raise ValueError(f"unsupported rotation axis: {axis!r}")
    half_angle = 0.5 * angle_rad
    sine = math.sin(half_angle)
    return (
        math.cos(half_angle),
        unit_axis[0] * sine,
        unit_axis[1] * sine,
        unit_axis[2] * sine,
    )


def _normalize_quaternion(
    quaternion: Sequence[float],
) -> tuple[float, float, float, float] | None:
    if not all(math.isfinite(value) for value in quaternion):
        return None
    scale = max(abs(value) for value in quaternion)
    if scale == 0.0:
        return None
    scaled = tuple(value / scale for value in quaternion)
    norm = math.hypot(*scaled)
    return tuple(value / norm for value in scaled)  # type: ignore[return-value]


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


def _matrix_to_quaternion(matrix: Sequence[Sequence[float]]) -> tuple[float, float, float, float]:
    trace = matrix[0][0] + matrix[1][1] + matrix[2][2]
    if trace > 0.0:
        scale = 2.0 * math.sqrt(trace + 1.0)
        quaternion = (
            0.25 * scale,
            (matrix[2][1] - matrix[1][2]) / scale,
            (matrix[0][2] - matrix[2][0]) / scale,
            (matrix[1][0] - matrix[0][1]) / scale,
        )
    else:
        diagonal = (matrix[0][0], matrix[1][1], matrix[2][2])
        index = max(range(3), key=diagonal.__getitem__)
        if index == 0:
            scale = 2.0 * math.sqrt(1.0 + matrix[0][0] - matrix[1][1] - matrix[2][2])
            quaternion = (
                (matrix[2][1] - matrix[1][2]) / scale,
                0.25 * scale,
                (matrix[0][1] + matrix[1][0]) / scale,
                (matrix[0][2] + matrix[2][0]) / scale,
            )
        elif index == 1:
            scale = 2.0 * math.sqrt(1.0 + matrix[1][1] - matrix[0][0] - matrix[2][2])
            quaternion = (
                (matrix[0][2] - matrix[2][0]) / scale,
                (matrix[0][1] + matrix[1][0]) / scale,
                0.25 * scale,
                (matrix[1][2] + matrix[2][1]) / scale,
            )
        else:
            scale = 2.0 * math.sqrt(1.0 + matrix[2][2] - matrix[0][0] - matrix[1][1])
            quaternion = (
                (matrix[1][0] - matrix[0][1]) / scale,
                (matrix[0][2] + matrix[2][0]) / scale,
                (matrix[1][2] + matrix[2][1]) / scale,
                0.25 * scale,
            )
    normalized = _normalize_quaternion(quaternion)
    if normalized is None:  # A proper CubeFrame matrix cannot reach this branch.
        raise ValueError("rotation matrix produced an invalid quaternion")
    return normalized


def quaternion_from_yaw_and_frame(
    yaw_rad: float, frame: CubeFrame
) -> tuple[float, float, float, float]:
    """Compose ``Rz(yaw_rad) @ frame.logical_to_world`` as active WXYZ."""

    frame_quaternion = _matrix_to_quaternion(frame.logical_to_world)
    quaternion = multiply_quaternions(
        axis_angle_quaternion("Z", yaw_rad), frame_quaternion
    )
    normalized = _normalize_quaternion(quaternion)
    if normalized is None:
        raise ValueError("yaw/frame composition produced an invalid quaternion")
    return normalized


def _transpose(matrix: Sequence[Sequence[float]]) -> Matrix3:
    return tuple(zip(*matrix, strict=True))  # type: ignore[return-value]


def _multiply_matrices(
    left: Sequence[Sequence[float]], right: Sequence[Sequence[float]]
) -> Matrix3:
    columns = tuple(zip(*right, strict=True))
    return tuple(
        tuple(
            sum(a * b for a, b in zip(row, column, strict=True))
            for column in columns
        )
        for row in left
    )  # type: ignore[return-value]


def _yaw_matrix(yaw_rad: float) -> Matrix3:
    cosine = math.cos(yaw_rad)
    sine = math.sin(yaw_rad)
    return (
        (cosine, -sine, 0.0),
        (sine, cosine, 0.0),
        (0.0, 0.0, 1.0),
    )


def _rotation_angle(matrix: Sequence[Sequence[float]]) -> float:
    quaternion = _matrix_to_quaternion(matrix)
    return 2.0 * math.atan2(math.hypot(*quaternion[1:]), abs(quaternion[0]))


def _factor_candidate(measured: Matrix3, frame: CubeFrame) -> _FactorCandidate:
    relative = _multiply_matrices(measured, _transpose(frame.logical_to_world))
    yaw_rad = math.atan2(
        relative[1][0] - relative[0][1],
        relative[0][0] + relative[1][1],
    )
    residual = _multiply_matrices(_yaw_matrix(-yaw_rad), relative)
    return _FactorCandidate(frame, yaw_rad, _rotation_angle(residual))


def refactor_face_supported_pose(
    pose: PhysicalCubePose,
    factorization_reference: CubeFrame,
) -> FaceSupportedPoseFactorization:
    """Select an equivalent minimum-tilt frame without changing raw pose truth."""

    if not isinstance(pose, PhysicalCubePose) or pose.status is not PoseStatus.STABLE:
        raise ValueError("target factorization requires a stable physical pose")
    if (
        factorization_reference not in CubeFrame.all()
        or pose.logical_orientation not in CubeFrame.all()
        or pose.support_face != pose.logical_orientation.support_face()
    ):
        raise ValueError("target factorization requires legal supported frames")
    _finite_pose_tuple(pose.position, 3, "raw pose position")
    normalized_quaternion = _normalized_pose_quaternion(
        pose.quaternion, "raw pose quaternion"
    )
    _finite_pose_tuple(
        (
            pose.yaw_rad,
            pose.tilt_rad,
            pose.linear_speed_m_s,
            pose.angular_speed_rad_s,
        ),
        4,
        "raw pose scalars",
    )

    measured_matrix = _quaternion_to_matrix(normalized_quaternion)
    candidates = tuple(
        _factor_candidate(measured_matrix, frame) for frame in CubeFrame.all()
    )
    best_tilt = min(candidate.tilt_rad for candidate in candidates)
    target_candidate = next(
        candidate
        for candidate in candidates
        if candidate.frame == factorization_reference
    )
    if abs(target_candidate.tilt_rad - best_tilt) > _FACTOR_TIE_TOLERANCE_RAD:
        raise ValueError("target frame is not in the minimum-tilt tie")

    reconstructed = quaternion_from_yaw_and_frame(
        target_candidate.yaw_rad, factorization_reference
    )
    reconstruction_error = _stable_wxyz_distance_rad(
        normalized_quaternion, reconstructed
    )
    if reconstruction_error > DEFAULT_TILT_TOLERANCE_RAD + 1e-12:
        raise ValueError("target factorization does not reconstruct raw quaternion")

    return FaceSupportedPoseFactorization(
        pose=replace(
            pose,
            logical_orientation=factorization_reference,
            support_face=factorization_reference.support_face(),
            yaw_rad=target_candidate.yaw_rad,
            tilt_rad=target_candidate.tilt_rad,
        ),
        reconstruction_error_rad=reconstruction_error,
    )


def _as_float_tuple(values: Sequence[float], expected_length: int, label: str):
    converted = tuple(float(value) for value in values)
    if len(converted) != expected_length:
        raise ValueError(f"{label} must contain {expected_length} values")
    return converted


def _validate_tolerance(value: float, label: str) -> float:
    converted = float(value)
    if not math.isfinite(converted) or converted < 0.0:
        raise ValueError(f"{label} must be a finite non-negative value")
    return converted


def _validate_workspace_bounds(bounds: WorkspaceXYBounds | None) -> WorkspaceXYBounds | None:
    if bounds is None:
        return None
    if len(bounds) != 2 or any(len(axis_bounds) != 2 for axis_bounds in bounds):
        raise ValueError("workspace_xy_bounds must be ((min_x, max_x), (min_y, max_y))")
    converted = tuple(
        tuple(float(value) for value in axis_bounds) for axis_bounds in bounds
    )
    if not all(math.isfinite(value) for axis_bounds in converted for value in axis_bounds):
        raise ValueError("workspace_xy_bounds must contain finite values")
    if converted[0][0] > converted[0][1] or converted[1][0] > converted[1][1]:
        raise ValueError("workspace_xy_bounds minima must not exceed maxima")
    return converted  # type: ignore[return-value]


def _unknown_pose(
    position: tuple[float, float, float],
    quaternion: tuple[float, float, float, float],
    linear_speed_m_s: float,
    angular_speed_rad_s: float,
    *,
    status: PoseStatus = PoseStatus.UNKNOWN,
) -> PhysicalCubePose:
    return PhysicalCubePose(
        position=position,
        quaternion=quaternion,
        logical_orientation=None,
        support_face=None,
        yaw_rad=None,
        tilt_rad=math.inf,
        linear_speed_m_s=linear_speed_m_s,
        angular_speed_rad_s=angular_speed_rad_s,
        status=status,
    )


def interpret_face_supported_pose(
    position: Sequence[float],
    quaternion: Sequence[float],
    linear_velocity: Sequence[float],
    angular_velocity: Sequence[float],
    *,
    previous_orientation: CubeFrame | None = None,
    tilt_tolerance_rad: float = DEFAULT_TILT_TOLERANCE_RAD,
    linear_speed_tolerance_m_s: float = DEFAULT_LINEAR_SPEED_TOLERANCE_M_S,
    angular_speed_tolerance_rad_s: float = DEFAULT_ANGULAR_SPEED_TOLERANCE_RAD_S,
    workspace_xy_bounds: WorkspaceXYBounds | None = None,
) -> PhysicalCubePose:
    """Interpret a measured pose without altering or snapping the measurement.

    Status precedence is out-of-workspace, invalid/ambiguous, moving,
    noncanonical, then stable. Workspace limits are opt-in and inclusive.
    """

    measured_position = _as_float_tuple(position, 3, "position")
    measured_quaternion = _as_float_tuple(quaternion, 4, "quaternion")
    measured_linear_velocity = _as_float_tuple(linear_velocity, 3, "linear_velocity")
    measured_angular_velocity = _as_float_tuple(angular_velocity, 3, "angular_velocity")
    tilt_tolerance = _validate_tolerance(tilt_tolerance_rad, "tilt_tolerance_rad")
    linear_tolerance = _validate_tolerance(
        linear_speed_tolerance_m_s, "linear_speed_tolerance_m_s"
    )
    angular_tolerance = _validate_tolerance(
        angular_speed_tolerance_rad_s, "angular_speed_tolerance_rad_s"
    )
    workspace_bounds = _validate_workspace_bounds(workspace_xy_bounds)

    linear_speed = math.hypot(*measured_linear_velocity)
    angular_speed = math.hypot(*measured_angular_velocity)
    observation_values = (
        *measured_position,
        *measured_quaternion,
        *measured_linear_velocity,
        *measured_angular_velocity,
    )
    if not all(math.isfinite(value) for value in observation_values):
        return _unknown_pose(
            measured_position,
            measured_quaternion,
            linear_speed,
            angular_speed,
        )

    outside_workspace = workspace_bounds is not None and not (
        workspace_bounds[0][0] <= measured_position[0] <= workspace_bounds[0][1]
        and workspace_bounds[1][0] <= measured_position[1] <= workspace_bounds[1][1]
    )
    normalized_quaternion = _normalize_quaternion(measured_quaternion)
    if normalized_quaternion is None:
        return _unknown_pose(
            measured_position,
            measured_quaternion,
            linear_speed,
            angular_speed,
            status=(
                PoseStatus.OUT_OF_WORKSPACE
                if outside_workspace
                else PoseStatus.UNKNOWN
            ),
        )

    measured_matrix = _quaternion_to_matrix(normalized_quaternion)
    candidates = tuple(
        _factor_candidate(measured_matrix, frame) for frame in CubeFrame.all()
    )
    best_tilt = min(candidate.tilt_rad for candidate in candidates)
    tied = tuple(
        candidate
        for candidate in candidates
        if abs(candidate.tilt_rad - best_tilt) <= _FACTOR_TIE_TOLERANCE_RAD
    )
    ambiguous_support = len({candidate.frame.support_face() for candidate in tied}) > 1
    previous_candidate = next(
        (
            candidate
            for candidate in tied
            if previous_orientation is not None and candidate.frame == previous_orientation
        ),
        None,
    )
    selected = previous_candidate or min(
        tied, key=lambda candidate: (abs(candidate.yaw_rad), candidate.frame.key)
    )

    canonical = best_tilt <= tilt_tolerance
    moving = linear_speed > linear_tolerance or angular_speed > angular_tolerance
    if outside_workspace:
        status = PoseStatus.OUT_OF_WORKSPACE
    elif ambiguous_support:
        status = PoseStatus.UNKNOWN
    elif moving:
        status = PoseStatus.MOVING
    elif not canonical:
        status = PoseStatus.NONCANONICAL
    else:
        status = PoseStatus.STABLE

    logical_orientation = selected.frame if canonical and not ambiguous_support else None
    return PhysicalCubePose(
        position=measured_position,
        quaternion=measured_quaternion,
        logical_orientation=logical_orientation,
        support_face=(logical_orientation.support_face() if logical_orientation else None),
        yaw_rad=(selected.yaw_rad if logical_orientation else None),
        tilt_rad=best_tilt,
        linear_speed_m_s=linear_speed,
        angular_speed_rad_s=angular_speed,
        status=status,
    )
