"""Pure synchronized evidence gates for the measured whole-cube grasp."""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Integral, Real
from typing import Sequence

try:
    from .rubiks_cube_mechanism import ConstraintFrame
    from .rubiks_cube_native_observation import NativeCubeSample
    from .rubiks_cube_observer import classify_native_snapshot
    from .rubiks_cube_rules import CubeState
except ImportError:  # Dependency-light direct loading.
    from rubiks_cube_mechanism import ConstraintFrame
    from rubiks_cube_native_observation import NativeCubeSample
    from rubiks_cube_observer import classify_native_snapshot
    from rubiks_cube_rules import CubeState


GRASP_ACQUISITION_MIN_FORCE_N = 0.5
GRASP_FORCE_LIMIT_N = 20.0
GRASP_REQUIRED_CONSECUTIVE_SAMPLES = 3
GRASP_POSITION_TOLERANCE_M = 0.001
GRASP_ANGLE_TOLERANCE_RAD = math.radians(1.0)
GRASP_NATIVE_POSITION_TOLERANCE_M = 0.001
GRASP_NATIVE_ANGLE_TOLERANCE_RAD = math.radians(2.0)
_CLOCK_TOLERANCE_S = 2e-6
_FORCE_CROSSCHECK_TOLERANCE_N = 1e-6


def _finite(value, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{label} must be a finite real number")
    converted = float(value)
    if not math.isfinite(converted):
        raise ValueError(f"{label} must be a finite real number")
    return converted


def _step(value, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise TypeError(f"{label} must be a non-negative integer")
    converted = int(value)
    if converted < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return converted


def _normalized_quaternion(values: Sequence[float], label: str) -> tuple[float, ...]:
    if len(values) != 4:
        raise ValueError(f"{label} must contain four values")
    quaternion = tuple(_finite(value, label) for value in values)
    norm = math.sqrt(sum(value * value for value in quaternion))
    if norm < 1e-12:
        raise ValueError(f"{label} quaternion must be nonzero")
    if abs(norm - 1.0) > 1e-3:
        raise ValueError(f"{label} quaternion must be unit length")
    return tuple(value / norm for value in quaternion)


@dataclass(frozen=True)
class RigidPose:
    position: tuple[float, float, float]
    quaternion: tuple[float, float, float, float]

    def __post_init__(self) -> None:
        if len(self.position) != 3:
            raise ValueError("pose position must contain three values")
        object.__setattr__(
            self, "position", tuple(_finite(value, "pose position") for value in self.position)
        )
        object.__setattr__(
            self, "quaternion", _normalized_quaternion(self.quaternion, "pose")
        )


def _multiply(left: Sequence[float], right: Sequence[float]) -> tuple[float, ...]:
    lw, lx, ly, lz = left
    rw, rx, ry, rz = right
    return (
        lw * rw - lx * rx - ly * ry - lz * rz,
        lw * rx + lx * rw + ly * rz - lz * ry,
        lw * ry - lx * rz + ly * rw + lz * rx,
        lw * rz + lx * ry - ly * rx + lz * rw,
    )


def _rotate(quaternion: Sequence[float], vector: Sequence[float]) -> tuple[float, ...]:
    rotated = _multiply(
        _multiply(quaternion, (0.0, *vector)),
        (quaternion[0], -quaternion[1], -quaternion[2], -quaternion[3]),
    )
    return rotated[1:]


def relative_frame(reference: RigidPose, target: RigidPose) -> ConstraintFrame:
    inverse = (
        reference.quaternion[0],
        -reference.quaternion[1],
        -reference.quaternion[2],
        -reference.quaternion[3],
    )
    translation = tuple(
        target.position[index] - reference.position[index] for index in range(3)
    )
    return ConstraintFrame(
        position=tuple(_rotate(inverse, translation)),
        quaternion=tuple(_multiply(inverse, target.quaternion)),
    )


def _pose_error(actual: RigidPose, expected: RigidPose) -> tuple[float, float]:
    position = math.dist(actual.position, expected.position)
    dot = abs(sum(a * b for a, b in zip(actual.quaternion, expected.quaternion)))
    angle = 2.0 * math.acos(min(1.0, max(-1.0, dot)))
    return position, angle


def _joint_vector(values, length: int, label: str) -> tuple[float, ...]:
    if not isinstance(values, (tuple, list)) or len(values) != length:
        raise ValueError(f"{label} must contain {length} values")
    return tuple(_finite(value, label) for value in values)


def _force_vectors(values) -> tuple[tuple[tuple[float, float, float], ...], ...]:
    try:
        if len(values) != 2 or any(len(side) not in {0, 26} for side in values):
            raise ValueError
        return tuple(
            tuple(
                tuple(_finite(component, "contact force vector") for component in vector)
                if len(vector) == 3 else (_ for _ in ()).throw(ValueError())
                for vector in side
            )
            for side in values
        )
    except (TypeError, ValueError):
        raise ValueError("per_cubie_force_vectors_n must contain two 26x3 arrays") from None


def _native_snapshot_evidence(sample: NativeCubeSample, expected_state: CubeState):
    measured, diagnostics = classify_native_snapshot(
        sample.body_names,
        sample.native_link_transforms_xyzw,
        position_tolerance_m=GRASP_NATIVE_POSITION_TOLERANCE_M,
        orientation_tolerance_rad=GRASP_NATIVE_ANGLE_TOLERANCE_RAD,
    )
    return measured, diagnostics, measured == expected_state


def _native_core_pose(
    sample: NativeCubeSample, native_origin_position: Sequence[float]
) -> RigidPose:
    origin = _joint_vector(native_origin_position, 3, "native_origin_position")
    row = sample.native_link_transforms_xyzw[sample.body_names.index("core")]
    return RigidPose(
        tuple(float(row[index]) - origin[index] for index in range(3)),
        (float(row[6]), float(row[3]), float(row[4]), float(row[5])),
    )


def _force_vector_maxima(vectors) -> tuple[float, float]:
    return tuple(
        max((math.sqrt(sum(component * component for component in vector)) for vector in side), default=0.0)
        for side in vectors
    )


def evaluate_measured_grasp_sample(
    *,
    native_sample: NativeCubeSample,
    hand_native_step: int,
    expected_state: CubeState,
    actual_hand_pose: RigidPose,
    target_hand_pose: RigidPose,
    actual_core_pose: RigidPose,
    actual_arm_q,
    actual_finger_q,
    accepted_finger_commands,
    finger_position_bounds,
    bilateral_normal_forces_n,
    per_cubie_force_vectors_n,
    native_origin_position=(0.0, 0.0, 0.0),
) -> dict[str, object]:
    """Evaluate one same-step actual sample; never mutate an attachment."""

    if not isinstance(native_sample, NativeCubeSample):
        raise TypeError("native_sample must be NativeCubeSample")
    if not isinstance(expected_state, CubeState):
        raise TypeError("expected_state must be CubeState")
    for value, label in (
        (actual_hand_pose, "actual_hand_pose"),
        (target_hand_pose, "target_hand_pose"),
        (actual_core_pose, "actual_core_pose"),
    ):
        if not isinstance(value, RigidPose):
            raise TypeError(f"{label} must be RigidPose")
    hand_step = _step(hand_native_step, "hand_native_step")
    arm_q = _joint_vector(actual_arm_q, 7, "actual_arm_q")
    finger_q = _joint_vector(actual_finger_q, 2, "actual_finger_q")
    commands = _joint_vector(accepted_finger_commands, 2, "accepted_finger_commands")
    bounds = _joint_vector(finger_position_bounds, 2, "finger_position_bounds")
    if bounds[0] > bounds[1]:
        raise ValueError("finger_position_bounds must be ordered")
    forces = _joint_vector(bilateral_normal_forces_n, 2, "bilateral_normal_forces_n")
    vectors = _force_vectors(per_cubie_force_vectors_n)
    vector_force_maxima = _force_vector_maxima(vectors)
    position_error, angle_error = _pose_error(actual_hand_pose, target_hand_pose)
    native_core = _native_core_pose(native_sample, native_origin_position)
    core_native_position_error, core_native_angle_error = _pose_error(
        actual_core_pose, native_core
    )
    measured_state, native_diagnostics, native_matches = _native_snapshot_evidence(
        native_sample, expected_state
    )

    reason = None
    if hand_step != native_sample.native_step:
        reason = "grasp_hand_sample_step_mismatch"
    elif any(len(side) != 26 for side in vectors):
        reason = "grasp_contact_vectors_missing"
    elif core_native_position_error > GRASP_POSITION_TOLERANCE_M + 1e-12 or core_native_angle_error > GRASP_ANGLE_TOLERANCE_RAD + 1e-12:
        reason = "grasp_core_native_pose_mismatch"
    elif any(
        abs(scalar_force - vector_force) > _FORCE_CROSSCHECK_TOLERANCE_N
        for scalar_force, vector_force in zip(forces, vector_force_maxima)
    ):
        reason = "grasp_contact_scalar_vector_mismatch"
    elif not all(bounds[0] <= value <= bounds[1] for value in finger_q):
        reason = "grasp_actual_finger_out_of_bounds"
    elif not all(bounds[0] <= value <= bounds[1] for value in commands):
        reason = "grasp_finger_command_out_of_bounds"
    elif position_error > GRASP_POSITION_TOLERANCE_M + 1e-12 or angle_error > GRASP_ANGLE_TOLERANCE_RAD + 1e-12:
        reason = "grasp_hand_target_error"
    elif measured_state is None:
        reason = "grasp_native_geometry_invalid"
    elif not native_matches:
        reason = "grasp_native_state_mismatch"
    elif forces[0] <= GRASP_ACQUISITION_MIN_FORCE_N:
        reason = "grasp_left_contact_below_acquisition_threshold"
    elif forces[1] <= GRASP_ACQUISITION_MIN_FORCE_N:
        reason = "grasp_right_contact_below_acquisition_threshold"
    elif max(forces) > GRASP_FORCE_LIMIT_N:
        reason = "grasp_contact_force_limit_exceeded"

    return {
        "accepted": reason is None,
        "abort_reason": reason,
        "native_step": native_sample.native_step,
        "native_time_s": native_sample.native_time_s,
        "hand_native_step": hand_step,
        "actual_hand_pose": actual_hand_pose,
        "actual_core_pose": actual_core_pose,
        "actual_arm_q": arm_q,
        "actual_finger_q": finger_q,
        "accepted_finger_commands": commands,
        "bilateral_normal_forces_n": forces,
        "per_cubie_force_vectors_n": vectors,
        "per_finger_vector_max_force_n": vector_force_maxima,
        "core_native_position_error_m": core_native_position_error,
        "core_native_angle_error_rad": core_native_angle_error,
        "hand_target_position_error_m": position_error,
        "hand_target_angle_error_rad": angle_error,
        "native_state_matches_expected": native_matches,
        "native_geometry": native_diagnostics,
        "attachment_frame": relative_frame(actual_hand_pose, actual_core_pose),
    }


class MeasuredGraspAcquisition:
    """Require three consecutive synchronized accepted post-step samples."""

    def __init__(self, *, physics_dt_s: float, native_step_stride: int = 1):
        self.physics_dt_s = _finite(physics_dt_s, "physics_dt_s")
        if self.physics_dt_s <= 0.0:
            raise ValueError("physics_dt_s must be positive")
        self.native_step_stride = _step(native_step_stride, "native_step_stride")
        if self.native_step_stride < 1:
            raise ValueError("native_step_stride must be positive")
        self._accepted: list[dict[str, object]] = []
        self._last_observed_step: int | None = None
        self._last_observed_time_s: float | None = None

    def reset(self) -> None:
        self._accepted.clear()
        self._last_observed_step = None
        self._last_observed_time_s = None

    def observe(self, **sample_inputs) -> dict[str, object]:
        result = evaluate_measured_grasp_sample(**sample_inputs)
        step = int(result["native_step"])
        time_s = float(result["native_time_s"])
        consecutive = self._last_observed_step is None or (
            step == self._last_observed_step + self.native_step_stride
            and abs(
                time_s
                - self._last_observed_time_s
                - self.physics_dt_s * self.native_step_stride
            )
            <= _CLOCK_TOLERANCE_S
        )
        self._last_observed_step = step
        self._last_observed_time_s = time_s
        if not consecutive:
            self._accepted.clear()
            result = {**result, "accepted": False, "abort_reason": "grasp_native_step_not_consecutive"}
        elif result["accepted"]:
            self._accepted.append(result)
        else:
            self._accepted.clear()
        acquired = len(self._accepted) == GRASP_REQUIRED_CONSECUTIVE_SAMPLES
        return {
            **result,
            "consecutive_count": len(self._accepted),
            "acquired": acquired,
            "acquisition_samples": tuple(self._accepted),
        }


def evaluate_attachment_consistency(
    *,
    captured_frame: ConstraintFrame,
    native_sample: NativeCubeSample,
    hand_native_step: int,
    expected_state: CubeState,
    actual_hand_pose: RigidPose,
    actual_core_pose: RigidPose,
    hand_attachment_enabled: bool,
    world_anchor_enabled: bool,
    native_origin_position=(0.0, 0.0, 0.0),
) -> dict[str, object]:
    """Check the actual attached relation after one completed control cycle."""

    if not isinstance(captured_frame, ConstraintFrame):
        raise TypeError("captured_frame must be ConstraintFrame")
    if not isinstance(native_sample, NativeCubeSample):
        raise TypeError("native_sample must be NativeCubeSample")
    if not isinstance(expected_state, CubeState):
        raise TypeError("expected_state must be CubeState")
    if not isinstance(actual_hand_pose, RigidPose) or not isinstance(actual_core_pose, RigidPose):
        raise TypeError("actual poses must be RigidPose")
    if type(hand_attachment_enabled) is not bool or type(world_anchor_enabled) is not bool:
        raise TypeError("constraint states must be bool")
    hand_step = _step(hand_native_step, "hand_native_step")
    measured_state, diagnostics, native_matches = _native_snapshot_evidence(
        native_sample, expected_state
    )
    native_core = _native_core_pose(native_sample, native_origin_position)
    core_native_error = _pose_error(actual_core_pose, native_core)
    current_frame = relative_frame(actual_hand_pose, actual_core_pose)
    relation_error = _pose_error(
        RigidPose(current_frame.position, current_frame.quaternion),
        RigidPose(captured_frame.position, captured_frame.quaternion),
    )

    reason = None
    if hand_step != native_sample.native_step:
        reason = "attachment_hand_sample_step_mismatch"
    elif not hand_attachment_enabled or world_anchor_enabled:
        reason = "attachment_constraint_state_invalid"
    elif measured_state is None:
        reason = "attachment_native_geometry_invalid"
    elif not native_matches:
        reason = "attachment_native_state_mismatch"
    elif core_native_error[0] > GRASP_POSITION_TOLERANCE_M + 1e-12 or core_native_error[1] > GRASP_ANGLE_TOLERANCE_RAD + 1e-12:
        reason = "attachment_core_native_pose_mismatch"
    elif relation_error[0] > GRASP_POSITION_TOLERANCE_M + 1e-12 or relation_error[1] > GRASP_ANGLE_TOLERANCE_RAD + 1e-12:
        reason = "attachment_relation_error"
    return {
        "accepted": reason is None,
        "abort_reason": reason,
        "native_step": native_sample.native_step,
        "native_time_s": native_sample.native_time_s,
        "hand_native_step": hand_step,
        "actual_hand_pose": actual_hand_pose,
        "actual_core_pose": actual_core_pose,
        "hand_attachment_enabled": hand_attachment_enabled,
        "world_anchor_enabled": world_anchor_enabled,
        "core_native_position_error_m": core_native_error[0],
        "core_native_angle_error_rad": core_native_error[1],
        "attachment_relation_position_error_m": relation_error[0],
        "attachment_relation_angle_error_rad": relation_error[1],
        "native_state_matches_expected": native_matches,
        "native_geometry": diagnostics,
    }


def verify_postactivation_attachment(
    *,
    acquisition: dict[str, object],
    native_sample: NativeCubeSample,
    expected_state: CubeState,
    actual_hand_pose: RigidPose,
    actual_core_pose: RigidPose,
    hand_attachment_enabled: bool,
    world_anchor_enabled: bool,
    native_origin_position=(0.0, 0.0, 0.0),
) -> dict[str, object]:
    """Verify the first fresh physics sample after attachment before lift."""

    if not isinstance(acquisition, dict) or acquisition.get("acquired") is not True:
        raise ValueError("a completed measured acquisition is required")
    if type(hand_attachment_enabled) is not bool or type(world_anchor_enabled) is not bool:
        raise TypeError("constraint states must be bool")
    if not isinstance(native_sample, NativeCubeSample):
        raise TypeError("native_sample must be NativeCubeSample")
    if not isinstance(actual_hand_pose, RigidPose) or not isinstance(actual_core_pose, RigidPose):
        raise TypeError("postactivation poses must be RigidPose")
    accepted_step = int(acquisition["native_step"])
    accepted_time = float(acquisition["native_time_s"])
    measured_state, diagnostics, native_matches = _native_snapshot_evidence(
        native_sample, expected_state
    )
    native_core = _native_core_pose(native_sample, native_origin_position)
    core_native_error = _pose_error(actual_core_pose, native_core)
    before_hand = acquisition["actual_hand_pose"]
    before_core = acquisition["actual_core_pose"]
    captured_frame = acquisition["attachment_frame"]
    current_frame = relative_frame(actual_hand_pose, actual_core_pose)
    hand_jump = _pose_error(actual_hand_pose, before_hand)
    core_jump = _pose_error(actual_core_pose, before_core)
    relation_error = _pose_error(
        RigidPose(current_frame.position, current_frame.quaternion),
        RigidPose(captured_frame.position, captured_frame.quaternion),
    )

    reason = None
    if native_sample.native_step <= accepted_step or native_sample.native_time_s <= accepted_time:
        reason = "grasp_postactivation_sample_not_fresh"
    elif not hand_attachment_enabled or world_anchor_enabled:
        reason = "grasp_postactivation_constraint_state_invalid"
    elif measured_state is None:
        reason = "grasp_postactivation_native_geometry_invalid"
    elif not native_matches:
        reason = "grasp_postactivation_native_state_mismatch"
    elif core_native_error[0] > GRASP_POSITION_TOLERANCE_M + 1e-12 or core_native_error[1] > GRASP_ANGLE_TOLERANCE_RAD + 1e-12:
        reason = "grasp_postactivation_core_native_pose_mismatch"
    elif any(
        position > GRASP_POSITION_TOLERANCE_M + 1e-12
        or angle > GRASP_ANGLE_TOLERANCE_RAD + 1e-12
        for position, angle in (hand_jump, core_jump)
    ):
        reason = "grasp_activation_jump_exceeded"
    elif relation_error[0] > GRASP_POSITION_TOLERANCE_M + 1e-12 or relation_error[1] > GRASP_ANGLE_TOLERANCE_RAD + 1e-12:
        reason = "grasp_attachment_relation_error"
    return {
        "accepted": reason is None,
        "abort_reason": reason,
        "native_step": native_sample.native_step,
        "native_time_s": native_sample.native_time_s,
        "hand_attachment_enabled": hand_attachment_enabled,
        "world_anchor_enabled": world_anchor_enabled,
        "actual_hand_pose": actual_hand_pose,
        "actual_core_pose": actual_core_pose,
        "captured_attachment_frame": captured_frame,
        "core_native_position_error_m": core_native_error[0],
        "core_native_angle_error_rad": core_native_error[1],
        "hand_activation_jump_position_m": hand_jump[0],
        "hand_activation_jump_angle_rad": hand_jump[1],
        "core_activation_jump_position_m": core_jump[0],
        "core_activation_jump_angle_rad": core_jump[1],
        "attachment_relation_position_error_m": relation_error[0],
        "attachment_relation_angle_error_rad": relation_error[1],
        "native_state_matches_expected": native_matches,
        "native_geometry": diagnostics,
    }


__all__ = [
    "GRASP_ACQUISITION_MIN_FORCE_N",
    "GRASP_FORCE_LIMIT_N",
    "GRASP_REQUIRED_CONSECUTIVE_SAMPLES",
    "MeasuredGraspAcquisition",
    "RigidPose",
    "evaluate_measured_grasp_sample",
    "evaluate_attachment_consistency",
    "relative_frame",
    "verify_postactivation_attachment",
]
