"""Measured rigid-pose mathematics and placement checks, without controller plans."""
from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Pose:
    position: tuple[float, float, float]
    quaternion: tuple[float, float, float, float]  # WXYZ


PLACEMENT_CORE_XY_MAX_ERROR_M = 0.002


PLACEMENT_CORE_Z_MAX_ERROR_M = 0.002


PLACEMENT_CORE_ORIENTATION_MAX_ERROR_RAD = math.radians(2.0)


PLACEMENT_EE_POSITION_MAX_ERROR_M = 0.003


PLACEMENT_EE_ORIENTATION_MAX_ERROR_RAD = math.radians(2.0)


def _normalize_quaternion(quaternion) -> tuple[float, float, float, float]:
    values = tuple(float(value) for value in quaternion)
    if len(values) != 4 or not all(math.isfinite(value) for value in values):
        raise ValueError("quaternion must contain four finite values")
    norm = math.sqrt(sum(value * value for value in values))
    if norm < 1e-12:
        raise ValueError("quaternion norm must be positive")
    return tuple(value / norm for value in values)


def quaternion_conjugate(quaternion) -> tuple[float, float, float, float]:
    w, x, y, z = _normalize_quaternion(quaternion)
    return w, -x, -y, -z


def quaternion_multiply(first, second) -> tuple[float, float, float, float]:
    w1, x1, y1, z1 = _normalize_quaternion(first)
    w2, x2, y2, z2 = _normalize_quaternion(second)
    return _normalize_quaternion(
        (
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        )
    )


def rotate_vector(quaternion, vector) -> tuple[float, float, float]:
    w, x, y, z = _normalize_quaternion(quaternion)
    vx, vy, vz = (float(value) for value in vector)
    # Expanded q * (0, v) * conjugate(q), avoiding normalization of (0, v).
    tx, ty, tz = (
        2.0 * (y * vz - z * vy),
        2.0 * (z * vx - x * vz),
        2.0 * (x * vy - y * vx),
    )
    return (
        vx + w * tx + y * tz - z * ty,
        vy + w * ty + z * tx - x * tz,
        vz + w * tz + x * ty - y * tx,
    )


def compose_pose(reference: Pose, relative: Pose) -> Pose:
    translated = rotate_vector(reference.quaternion, relative.position)
    return Pose(
        tuple(a + b for a, b in zip(reference.position, translated, strict=True)),
        quaternion_multiply(reference.quaternion, relative.quaternion),
    )


def inverse_pose(pose: Pose) -> Pose:
    inverse_quaternion = quaternion_conjugate(pose.quaternion)
    inverse_position = rotate_vector(
        inverse_quaternion, tuple(-value for value in pose.position)
    )
    return Pose(inverse_position, inverse_quaternion)


def relative_pose(reference: Pose, target: Pose) -> Pose:
    return compose_pose(inverse_pose(reference), target)


def hand_pose_for_core(desired_core_pose: Pose, hand_to_core: Pose) -> Pose:
    """Map a desired core pose through the inverse measured grasp transform."""

    return compose_pose(desired_core_pose, inverse_pose(hand_to_core))


def axis_angle_quaternion(axis: str, angle_rad: float):
    unit = {
        "X": (1.0, 0.0, 0.0),
        "Y": (0.0, 1.0, 0.0),
        "Z": (0.0, 0.0, 1.0),
    }.get(axis.upper())
    if unit is None:
        raise ValueError(f"unsupported rotation axis: {axis}")
    half = 0.5 * float(angle_rad)
    sine = math.sin(half)
    return math.cos(half), unit[0] * sine, unit[1] * sine, unit[2] * sine


def quaternion_from_matrix(matrix) -> tuple[float, float, float, float]:
    rows = tuple(tuple(float(value) for value in row) for row in matrix)
    if len(rows) != 3 or any(len(row) != 3 for row in rows):
        raise ValueError("rotation matrix must be 3x3")
    m00, m01, m02 = rows[0]
    m10, m11, m12 = rows[1]
    m20, m21, m22 = rows[2]
    trace = m00 + m11 + m22
    if trace > 0.0:
        scale = math.sqrt(trace + 1.0) * 2.0
        quaternion = (0.25 * scale, (m21 - m12) / scale,
                      (m02 - m20) / scale, (m10 - m01) / scale)
    elif m00 > m11 and m00 > m22:
        scale = math.sqrt(1.0 + m00 - m11 - m22) * 2.0
        quaternion = ((m21 - m12) / scale, 0.25 * scale,
                      (m01 + m10) / scale, (m02 + m20) / scale)
    elif m11 > m22:
        scale = math.sqrt(1.0 + m11 - m00 - m22) * 2.0
        quaternion = ((m02 - m20) / scale, (m01 + m10) / scale,
                      0.25 * scale, (m12 + m21) / scale)
    else:
        scale = math.sqrt(1.0 + m22 - m00 - m11) * 2.0
        quaternion = ((m10 - m01) / scale, (m02 + m20) / scale,
                      (m12 + m21) / scale, 0.25 * scale)
    return _normalize_quaternion(quaternion)


def matrix_from_quaternion(quaternion):
    w, x, y, z = _normalize_quaternion(quaternion)
    values = (
        (1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)),
        (2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)),
        (2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)),
    )
    return tuple(
        tuple(int(round(value)) if abs(value - round(value)) < 1e-10 else value for value in row)
        for row in values
    )


def evaluate_placement_evidence(
    *,
    actual_core_pose: Pose,
    target_core_pose: Pose,
    actual_hand_pose: Pose,
    target_hand_pose: Pose,
) -> dict[str, object]:
    """Evaluate measured placement before XY recovery, release, or commit."""

    measured_values = (
        *actual_core_pose.position,
        *actual_core_pose.quaternion,
        *actual_hand_pose.position,
        *actual_hand_pose.quaternion,
    )
    finite_measurements = all(math.isfinite(float(value)) for value in measured_values)

    def orientation_error(actual, target) -> float:
        try:
            return _quaternion_distance_rad(actual, target)
        except ValueError:
            return math.nan

    errors = {
        "core_xy_m": math.hypot(
            float(actual_core_pose.position[0]) - float(target_core_pose.position[0]),
            float(actual_core_pose.position[1]) - float(target_core_pose.position[1]),
        ),
        "core_z_m": abs(
            float(actual_core_pose.position[2]) - float(target_core_pose.position[2])
        ),
        "core_orientation_rad": orientation_error(
            actual_core_pose.quaternion, target_core_pose.quaternion
        ),
        "ee_position_m": math.dist(
            actual_hand_pose.position, target_hand_pose.position
        ),
        "ee_orientation_rad": orientation_error(
            actual_hand_pose.quaternion, target_hand_pose.quaternion
        ),
    }
    thresholds = {
        "core_xy_m": PLACEMENT_CORE_XY_MAX_ERROR_M,
        "core_z_m": PLACEMENT_CORE_Z_MAX_ERROR_M,
        "core_orientation_rad": PLACEMENT_CORE_ORIENTATION_MAX_ERROR_RAD,
        "ee_position_m": PLACEMENT_EE_POSITION_MAX_ERROR_M,
        "ee_orientation_rad": PLACEMENT_EE_ORIENTATION_MAX_ERROR_RAD,
    }
    abort_reason = None
    if not finite_measurements or not all(
        math.isfinite(error) for error in errors.values()
    ):
        abort_reason = "whole_cube_placement_nonfinite_measurement"
    elif errors["core_z_m"] > thresholds["core_z_m"]:
        abort_reason = "whole_cube_placement_core_z_error"
    elif errors["core_orientation_rad"] > thresholds["core_orientation_rad"]:
        abort_reason = "whole_cube_placement_core_orientation_error"
    elif errors["ee_position_m"] > thresholds["ee_position_m"]:
        abort_reason = "whole_cube_placement_ee_position_error"
    elif errors["ee_orientation_rad"] > thresholds["ee_orientation_rad"]:
        abort_reason = "whole_cube_placement_ee_orientation_error"
    non_xy_gates_pass = abort_reason is None
    return {
        "accepted": bool(
            non_xy_gates_pass and errors["core_xy_m"] <= thresholds["core_xy_m"]
        ),
        "xy_correction_allowed": bool(
            non_xy_gates_pass and errors["core_xy_m"] > thresholds["core_xy_m"]
        ),
        "abort_reason": abort_reason,
        "finite_measurements": finite_measurements,
        "actual_core_pose": {
            "position": list(actual_core_pose.position),
            "quaternion": list(actual_core_pose.quaternion),
        },
        "target_core_pose": {
            "position": list(target_core_pose.position),
            "quaternion": list(target_core_pose.quaternion),
        },
        "actual_ee_pose": {
            "position": list(actual_hand_pose.position),
            "quaternion": list(actual_hand_pose.quaternion),
        },
        "target_ee_pose": {
            "position": list(target_hand_pose.position),
            "quaternion": list(target_hand_pose.quaternion),
        },
        "errors": errors,
        "thresholds": thresholds,
    }


def _quaternion_distance_rad(first, second) -> float:
    left = _normalize_quaternion(first)
    right = _normalize_quaternion(second)
    dot = abs(sum(a * b for a, b in zip(left, right, strict=True)))
    return 2.0 * math.acos(max(-1.0, min(1.0, dot)))

