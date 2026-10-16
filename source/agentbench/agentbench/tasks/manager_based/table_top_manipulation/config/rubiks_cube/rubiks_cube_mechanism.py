"""Hybrid Rubik's Cube constraint-switching state machine.

This module is intentionally independent of Isaac Sim.  A backend performs one
atomic USD joint transaction for each high-level transition.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
import math
from typing import Protocol, Sequence

try:
    from .rubiks_cube_rules import (
        CubeFrame,
        CubeState,
        FACE_AXIS_SIGN,
        FACE_GRID_AXES,
        FACE_NORMALS,
        NORMAL_TO_FACE,
        evaluate_quarter_turn,
        parse_sequence,
    )
except ImportError:  # Loaded directly by dependency-light unit tests.
    from rubiks_cube_rules import (
        CubeFrame,
        CubeState,
        FACE_AXIS_SIGN,
        FACE_GRID_AXES,
        FACE_NORMALS,
        NORMAL_TO_FACE,
        evaluate_quarter_turn,
        parse_sequence,
    )


DETENT_PEAK_TORQUE_NM = 0.0015
DETENT_DAMPING_NM_S_RAD = 0.0002
SAFETY_GUARD_RAD = math.radians(120.0)
REORIENTATION_LIFT_MINIMUM_M = 0.04
REORIENTATION_POSITION_TOLERANCE_M = 0.005
REORIENTATION_ANGLE_TOLERANCE_RAD = math.radians(3.0)
REORIENTATION_LINEAR_SPEED_TOLERANCE_M_S = 0.02
REORIENTATION_ANGULAR_SPEED_TOLERANCE_RAD_S = 0.1
REORIENTATION_CUBIE_ALIGNMENT_TOLERANCE_M = 0.001
REORIENTATION_CONTACT_OBSERVED_N = 1.0
REORIENTATION_CONTACT_MAINTAINED_N = 0.5
REORIENTATION_CONTACT_MAINTAINED_FRACTION = 0.75


_CORNER_SLOT_FACES = {
    (1, -1, 1): ("U", "R", "F"),
    (-1, -1, 1): ("U", "F", "L"),
    (-1, 1, 1): ("U", "L", "B"),
    (1, 1, 1): ("U", "B", "R"),
    (1, -1, -1): ("D", "F", "R"),
    (-1, -1, -1): ("D", "L", "F"),
    (-1, 1, -1): ("D", "B", "L"),
    (1, 1, -1): ("D", "R", "B"),
}
_EDGE_SLOT_FACES = {
    (1, 0, 1): ("U", "R"),
    (0, -1, 1): ("U", "F"),
    (-1, 0, 1): ("U", "L"),
    (0, 1, 1): ("U", "B"),
    (1, 0, -1): ("D", "R"),
    (0, -1, -1): ("D", "F"),
    (-1, 0, -1): ("D", "L"),
    (0, 1, -1): ("D", "B"),
    (1, -1, 0): ("F", "R"),
    (-1, -1, 0): ("F", "L"),
    (-1, 1, 0): ("B", "L"),
    (1, 1, 0): ("B", "R"),
}
_CENTER_SLOT_FACES = {
    (0, 0, 1): ("U",),
    (1, 0, 0): ("R",),
    (0, -1, 0): ("F",),
    (0, 0, -1): ("D",),
    (-1, 0, 0): ("L",),
    (0, 1, 0): ("B",),
}
_SLOT_FACES = {
    **_CORNER_SLOT_FACES,
    **_EDGE_SLOT_FACES,
    **_CENTER_SLOT_FACES,
}


class MechanismPhase(str, Enum):
    ANCHORED = "anchored"
    PREPARE = "prepare"
    ACTIVE = "active"
    SETTLE = "settle"
    VALIDATE = "validate"
    COMMIT = "commit"
    FAILED = "failed"


class ReorientationPhase(str, Enum):
    ANCHORED = "anchored"
    PREPARE = "prepare"
    GRASPED = "grasped"
    RELEASED = "released"
    ATTACHED = "attached"
    ATTACHMENT_VERIFIED = "attachment_verified"
    LIFTED = "lifted"
    ROTATED = "rotated"
    RELEASE_READY = "release_ready"
    SUPPORT_CAPTURED = "support_captured"
    HAND_RELEASED = "hand_released"
    SETTLE = "settle"
    VALIDATE = "validate"
    REANCHOR = "reanchor"
    COMMIT = "commit"
    FAILED = "failed"


@dataclass(frozen=True)
class ConstraintFrame:
    position: tuple[float, float, float]
    quaternion: tuple[float, float, float, float]


def _rotate_geometry_reference(frame: ConstraintFrame, axis: str, sign: int) -> ConstraintFrame:
    """Rotate a constraint target one measured, accepted quarter about the core."""

    axis_index = "xyz".index(axis)
    first = (axis_index + 1) % 3
    second = (axis_index + 2) % 3
    position = list(frame.position)
    position[first], position[second] = -sign * position[second], sign * position[first]
    # Left-compose the active WXYZ axis rotation. Keep positions as exact
    # signed permutations so repeated detents cannot accumulate pitch drift.
    w, *vector = frame.quaternion
    h = math.sqrt(0.5)
    rotated = list(vector)
    rotated[axis_index] = h * (vector[axis_index] + sign * w)
    rotated[first] = h * (vector[first] - sign * vector[second])
    rotated[second] = h * (vector[second] + sign * vector[first])
    quaternion = (h * (w - sign * vector[axis_index]), *rotated)
    norm = math.sqrt(sum(value * value for value in quaternion))
    return ConstraintFrame(tuple(position), tuple(value / norm for value in quaternion))


@dataclass(frozen=True)
class TurnObservation:
    """Measured turn values in intrinsic cube coordinates.

    ``wrist_axis_delta_rad`` is the signed measured delta about the positive
    intrinsic carrier axis. ``native_pose_window_valid`` comes from the fresh
    native pose-window/prefix validator; raw angular velocity is diagnostic.
    """

    final_angle_rad: float
    final_angular_velocity_rad_s: float
    left_contact_forces_n: Sequence[float]
    right_contact_forces_n: Sequence[float]
    wrist_axis_delta_rad: float
    core_pose_error_m: float
    active_cubie_alignment_error_m: float
    non_active_cubie_displacement_m: float
    permutation_matches: bool
    native_pose_window_valid: bool = False
    abort_reason: str | None = None


@dataclass(frozen=True)
class ReorientationObservation:
    left_contact_forces_n: Sequence[float]
    right_contact_forces_n: Sequence[float]
    lift_height_m: float
    final_core_position_error_m: float
    final_orientation_error_rad: float
    final_linear_speed_m_s: float
    final_angular_speed_rad_s: float
    max_cubie_alignment_error_m: float
    facelets_before: str
    facelets_after: str
    permutation_checksum_before: str
    permutation_checksum_after: str
    used_direct_core_pose_during_move: bool = False
    used_robot_cube_attachment: bool = False
    attachment_verified: bool = False
    attachment_maintained: bool = False
    support_handoff_completed: bool = False
    abort_reason: str | None = None


@dataclass
class CarrierAngleTracker:
    """Unwrap a carrier quaternion angle across repeated quarter turns."""

    previous_wrapped_rad: float | None = None
    unwrapped_rad: float = 0.0

    def update(self, wrapped_angle_rad: float) -> float:
        if self.previous_wrapped_rad is None:
            self.unwrapped_rad = float(wrapped_angle_rad)
        else:
            delta = math.atan2(
                math.sin(wrapped_angle_rad - self.previous_wrapped_rad),
                math.cos(wrapped_angle_rad - self.previous_wrapped_rad),
            )
            self.unwrapped_rad += delta
        self.previous_wrapped_rad = float(wrapped_angle_rad)
        return self.unwrapped_rad


class ConstraintBackend(Protocol):
    """Backend whose methods each apply one indivisible constraint transaction."""

    def activate_layer(self, axis: str, cubie_frames: dict[str, ConstraintFrame]) -> None: ...

    def anchor_all(self, cubie_frames: dict[str, ConstraintFrame]) -> None: ...

    def reset(
        self,
        cubie_frames: dict[str, ConstraintFrame],
        world_core_frame: ConstraintFrame,
    ) -> None: ...

    def prepare_transport(self, carrier_frames: dict[str, ConstraintFrame]) -> None: ...

    def release_world_anchor(self) -> None: ...

    def acquire_hand_attachment(self, core_frame: ConstraintFrame) -> None: ...

    def capture_support_and_detach(self, core_frame: ConstraintFrame) -> None: ...

    def reanchor_world(self, core_frame: ConstraintFrame) -> None: ...

    def finish_transport(self) -> None: ...


def is_legal_cube_state(cube_state: CubeState, *, ignore_center_twist: bool = False) -> bool:
    """Return whether a classified piece state belongs to the Rubik cube group."""

    if type(ignore_center_twist) is not bool:
        raise TypeError("ignore_center_twist must be bool")
    solved = CubeState.solved()
    pieces = getattr(cube_state, "pieces", None)
    if not isinstance(pieces, dict) or set(pieces) != set(solved.pieces):
        return False

    valid_orientations = {
        frame.logical_to_world for frame in CubeFrame.all()
    }
    piece_at_position = {}
    corner_twist_sum = 0
    edge_flip_sum = 0
    center_quarter_turn_sum = 0
    for identity, reference in solved.pieces.items():
        piece = pieces[identity]
        if (
            getattr(piece, "identity", None) != identity
            or getattr(piece, "home_position", None) != reference.home_position
            or getattr(piece, "stickers", None) != reference.stickers
        ):
            return False

        position = getattr(piece, "position", None)
        try:
            slot_faces = _SLOT_FACES[position]
        except (KeyError, TypeError):
            return False
        piece_class = sum(coordinate != 0 for coordinate in reference.home_position)
        if (
            sum(coordinate != 0 for coordinate in position) != piece_class
            or position in piece_at_position
            or (piece_class == 1 and position != reference.home_position)
        ):
            return False

        orientation = getattr(piece, "orientation", None)
        try:
            if orientation not in valid_orientations:
                return False
        except TypeError:
            return False

        observed_faces = {}
        for sticker in reference.stickers:
            normal = FACE_NORMALS[sticker]
            rotated_normal = tuple(
                sum(row[index] * normal[index] for index in range(3))
                for row in orientation
            )
            face = NORMAL_TO_FACE.get(rotated_normal)
            if face is None:
                return False
            observed_faces[sticker] = face
        if set(observed_faces.values()) != set(slot_faces):
            return False

        if piece_class == 3:
            reference_sticker = next(
                sticker for sticker in reference.stickers if sticker in "UD"
            )
            corner_twist_sum += slot_faces.index(
                observed_faces[reference_sticker]
            )
        elif piece_class == 2:
            reference_sticker = next(
                (sticker for sticker in reference.stickers if sticker in "UD"),
                None,
            )
            if reference_sticker is None:
                reference_sticker = next(
                    sticker for sticker in reference.stickers if sticker in "FB"
                )
            edge_flip_sum += slot_faces.index(observed_faces[reference_sticker])
        else:
            center_face = reference.stickers[0]
            up_axis, right_axis = FACE_GRID_AXES[center_face]
            rotated_right = tuple(
                sum(row[index] * right_axis[index] for index in range(3))
                for row in orientation
            )
            # Positive turns are right -> up about the outward face normal.
            signed_quarter_turn = {
                right_axis: 0,
                up_axis: 1,
                tuple(-value for value in right_axis): 2,
                tuple(-value for value in up_axis): -1,
            }.get(rotated_right)
            if signed_quarter_turn is None:
                return False
            center_quarter_turn_sum += signed_quarter_turn
        piece_at_position[position] = piece

    if set(piece_at_position) != set(_SLOT_FACES):
        return False
    if corner_twist_sum % 3 != 0 or edge_flip_sum % 2 != 0:
        return False

    def permutation_parity(slots):
        identity_index = {
            next(
                identity
                for identity, piece in solved.pieces.items()
                if piece.home_position == slot
            ): index
            for index, slot in enumerate(slots)
        }
        permutation = tuple(
            identity_index[piece_at_position[slot].identity] for slot in slots
        )
        return sum(
            left > right
            for index, left in enumerate(permutation)
            for right in permutation[index + 1 :]
        ) % 2

    corner_parity = permutation_parity(tuple(_CORNER_SLOT_FACES))
    edge_parity = permutation_parity(tuple(_EDGE_SLOT_FACES))
    return (
        corner_parity == edge_parity
        and (ignore_center_twist or corner_parity == center_quarter_turn_sum % 2)
    )


def passive_detent_torque(
    angle_rad: float,
    angular_velocity_rad_s: float,
    *,
    peak_torque_nm: float = DETENT_PEAK_TORQUE_NM,
    damping_nm_s_rad: float = DETENT_DAMPING_NM_S_RAD,
) -> float:
    """Return passive periodic detent and viscous damping torque."""

    return -peak_torque_nm * math.sin(4.0 * angle_rad) - damping_nm_s_rad * angular_velocity_rad_s


def passive_detent_torques(
    carrier_measurements: dict[str, tuple[float, float]],
) -> dict[str, float]:
    """Apply the same target-independent detent law to every carrier axis."""

    if set(carrier_measurements) != {"x", "y", "z"}:
        raise ValueError("passive detent requires x, y, and z carrier measurements")
    return {
        axis: passive_detent_torque(angle, angular_velocity)
        for axis, (angle, angular_velocity) in carrier_measurements.items()
    }


def safety_guard_reason(relative_angle_rad: float) -> str | None:
    """Return a software abort reason without imposing a physical joint limit."""

    if abs(relative_angle_rad) > SAFETY_GUARD_RAD + 1e-12:
        return "relative_angle_safety_guard_exceeded"
    return None


def _reorientation_contact_fraction(
    left_forces_n: Sequence[float], right_forces_n: Sequence[float]
) -> float:
    if len(left_forces_n) != len(right_forces_n):
        raise ValueError("left and right reorientation contact samples must have equal length")
    if not left_forces_n:
        return 0.0
    maintained = sum(
        left > REORIENTATION_CONTACT_MAINTAINED_N
        and right > REORIENTATION_CONTACT_MAINTAINED_N
        for left, right in zip(left_forces_n, right_forces_n, strict=True)
    )
    return maintained / len(left_forces_n)


def evaluate_reorientation(
    observation: ReorientationObservation,
    *,
    expected_initial_checksum: str,
    minimum_observed_contact_n: float | None = None,
) -> dict[str, object]:
    """Evaluate a physical whole-cube reorientation without accepting hidden motion."""

    left_observed = any(
        force > REORIENTATION_CONTACT_OBSERVED_N
        for force in observation.left_contact_forces_n
    )
    right_observed = any(
        force > REORIENTATION_CONTACT_OBSERVED_N
        for force in observation.right_contact_forces_n
    )
    maintained_fraction = _reorientation_contact_fraction(
        observation.left_contact_forces_n,
        observation.right_contact_forces_n,
    )
    if minimum_observed_contact_n is not None:
        minimum = minimum_observed_contact_n
        left, right = observation.left_contact_forces_n, observation.right_contact_forces_n
        if (isinstance(minimum, bool) or not isinstance(minimum, (int, float))
                or not math.isfinite(minimum) or minimum <= 0
                or not left or len(left) != len(right)
                or any(isinstance(force, bool) or not isinstance(force, (int, float))
                       or not math.isfinite(force) for force in (*left, *right))):
            raise ValueError('explicit transport contact requires finite samples and a positive threshold')
        left_observed = any(force >= minimum for force in left)
        right_observed = any(force >= minimum for force in right)
        maintained_fraction = sum(a >= minimum and b >= minimum for a, b in zip(left, right, strict=True))/len(left)
    reason = observation.abort_reason
    if (reason is None and minimum_observed_contact_n is not None
            and (not left_observed or not right_observed
                 or maintained_fraction < REORIENTATION_CONTACT_MAINTAINED_FRACTION)):
        reason = 'whole_cube_contact_not_maintained'
    if reason is None and observation.used_direct_core_pose_during_move:
        reason = "strict_mode_violation"
    if reason is None and (
        observation.permutation_checksum_before != expected_initial_checksum
        or observation.permutation_checksum_after != observation.permutation_checksum_before
        or observation.facelets_after != observation.facelets_before
    ):
        reason = "cube_state_changed_during_reorientation"
    if reason is None and not observation.used_robot_cube_attachment:
        reason = "whole_cube_attachment_driver_missing"
    if reason is None and not observation.attachment_verified:
        reason = "whole_cube_attachment_not_verified"
    if reason is None and not observation.attachment_maintained:
        reason = "whole_cube_attachment_not_maintained"
    if reason is None and not observation.support_handoff_completed:
        reason = "whole_cube_support_handoff_incomplete"
    if reason is None and any(
        force > 20.0
        for force in (*observation.left_contact_forces_n, *observation.right_contact_forces_n)
    ):
        reason = "whole_cube_excessive_contact_force"
    if reason is None and observation.lift_height_m + 1e-12 < REORIENTATION_LIFT_MINIMUM_M:
        reason = "whole_cube_lift_insufficient"
    if (
        reason is None
        and observation.final_core_position_error_m
        > REORIENTATION_POSITION_TOLERANCE_M + 1e-12
    ):
        reason = "whole_cube_position_error"
    if (
        reason is None
        and observation.final_orientation_error_rad
        > REORIENTATION_ANGLE_TOLERANCE_RAD + 1e-12
    ):
        reason = "whole_cube_orientation_error"
    if (
        reason is None
        and observation.final_linear_speed_m_s
        > REORIENTATION_LINEAR_SPEED_TOLERANCE_M_S + 1e-12
    ):
        reason = "whole_cube_not_settled"
    if (
        reason is None
        and observation.final_angular_speed_rad_s
        > REORIENTATION_ANGULAR_SPEED_TOLERANCE_RAD_S + 1e-12
    ):
        reason = "whole_cube_not_settled"
    if (
        reason is None
        and observation.max_cubie_alignment_error_m
        > REORIENTATION_CUBIE_ALIGNMENT_TOLERANCE_M + 1e-12
    ):
        reason = "whole_cube_internal_alignment_error"

    return {
        "lift_height_m": float(observation.lift_height_m),
        "final_core_position_error_m": float(observation.final_core_position_error_m),
        "final_orientation_error_rad": float(observation.final_orientation_error_rad),
        "final_linear_speed_m_s": float(observation.final_linear_speed_m_s),
        "final_angular_speed_rad_s": float(observation.final_angular_speed_rad_s),
        "max_cubie_alignment_error_m": float(observation.max_cubie_alignment_error_m),
        "left_contact_observed": left_observed,
        "right_contact_observed": right_observed,
        "contact_maintained_fraction": float(maintained_fraction),
        "facelets_before": observation.facelets_before,
        "facelets_after": observation.facelets_after,
        "permutation_checksum_before": observation.permutation_checksum_before,
        "permutation_checksum_after": observation.permutation_checksum_after,
        "success_tolerance_met": reason is None,
        "abort_reason": reason,
        "used_internal_constraint_switching": True,
        "used_world_core_anchor_switching": True,
        "used_carrier_transport_locks": True,
        "used_direct_cubie_state_during_move": False,
        "used_direct_core_pose_during_move": bool(
            observation.used_direct_core_pose_during_move
        ),
        "used_active_cube_drive": False,
        "used_hard_joint_limit": False,
        "used_robot_cube_attachment": bool(observation.used_robot_cube_attachment),
        "attachment_verified": bool(observation.attachment_verified),
        "attachment_maintained": bool(observation.attachment_maintained),
        "support_handoff_completed": bool(observation.support_handoff_completed),
        "used_passive_detent": True,
    }


class CubeReorientationMechanism:
    """Coordinate whole-cube transport independently of cubie permutation."""

    def __init__(self, backend: ConstraintBackend):
        self.backend = backend
        self.cube_frame = CubeFrame.identity()
        self.phase = ReorientationPhase.ANCHORED
        self.phase_history = [self.phase]
        self.target_frame: CubeFrame | None = None
        self.initial_state_checksum: str | None = None
        self._settle_branch: str | None = None

    def _transition(self, phase: ReorientationPhase) -> None:
        self.phase = phase
        self.phase_history.append(phase)

    def _require(self, expected: ReorientationPhase, action: str) -> None:
        if self.phase is not expected:
            raise RuntimeError(f"cannot {action} while reorientation is {self.phase.value}")

    def reset(self, initial_frame: CubeFrame | None = None) -> None:
        # This is the declared discrete factor, not the raw yaw/tilt pose.
        frame = CubeFrame.identity() if initial_frame is None else initial_frame
        if not isinstance(frame, CubeFrame) or frame not in CubeFrame.all():
            raise ValueError("initial_frame must be an exact legal CubeFrame")
        self.cube_frame = frame
        self.phase = ReorientationPhase.ANCHORED
        self.phase_history = [self.phase]
        self.target_frame = None
        self.initial_state_checksum = None
        self._settle_branch = None

    def prepare(
        self,
        target_frame: CubeFrame,
        carrier_frames: dict[str, ConstraintFrame],
        state_checksum: str,
    ) -> None:
        self._require(ReorientationPhase.ANCHORED, "prepare transport")
        if not state_checksum:
            raise ValueError("reorientation requires a non-empty cube-state checksum")
        self.phase_history = [ReorientationPhase.ANCHORED]
        self._settle_branch = None
        self.backend.prepare_transport(carrier_frames)
        self.target_frame = target_frame
        self.initial_state_checksum = state_checksum
        self._transition(ReorientationPhase.PREPARE)

    def mark_grasped(self) -> None:
        self._require(ReorientationPhase.PREPARE, "mark the cube grasped")
        self._transition(ReorientationPhase.GRASPED)

    def attach_measured_grasp(self, core_frame: ConstraintFrame) -> None:
        self._require(ReorientationPhase.PREPARE, "attach the measured grasp")
        try:
            self.backend.acquire_hand_attachment(core_frame)
        except Exception:
            self._transition(ReorientationPhase.FAILED)
            raise
        self._transition(ReorientationPhase.ATTACHED)

    def verify_measured_grasp(self) -> None:
        self._require(ReorientationPhase.ATTACHED, "verify the measured grasp")
        self._transition(ReorientationPhase.ATTACHMENT_VERIFIED)

    def release_anchor(self) -> None:
        self._require(ReorientationPhase.GRASPED, "release the world anchor")
        self.backend.release_world_anchor()
        self._transition(ReorientationPhase.RELEASED)

    def mark_lifted(self) -> None:
        if self.phase not in {
            ReorientationPhase.ATTACHMENT_VERIFIED,
            ReorientationPhase.RELEASED,
        }:
            raise RuntimeError(
                f"cannot mark the cube lifted while reorientation is {self.phase.value}"
            )
        self._transition(ReorientationPhase.LIFTED)

    def mark_rotated(self) -> None:
        self._require(ReorientationPhase.LIFTED, "mark the cube rotated")
        self._transition(ReorientationPhase.ROTATED)

    def mark_release_ready(self) -> None:
        self._require(ReorientationPhase.ROTATED, "mark the cube release-ready")
        self._transition(ReorientationPhase.RELEASE_READY)

    def begin_settle(self) -> None:
        self._require(ReorientationPhase.RELEASE_READY, "settle the cube")
        self._settle_branch = "canonical"
        self._transition(ReorientationPhase.SETTLE)

    def capture_measured_support(self, core_frame: ConstraintFrame) -> None:
        self._require(ReorientationPhase.RELEASE_READY, "capture measured support")
        self._settle_branch = "captured"
        try:
            self.backend.capture_support_and_detach(core_frame)
        except Exception:
            self._transition(ReorientationPhase.FAILED)
            raise
        self._transition(ReorientationPhase.SUPPORT_CAPTURED)

    def mark_support_hand_released(self) -> None:
        self._require(
            ReorientationPhase.SUPPORT_CAPTURED,
            "mark the support hand released",
        )
        self._transition(ReorientationPhase.HAND_RELEASED)

    def begin_captured_support_settle(self) -> None:
        self._require(ReorientationPhase.HAND_RELEASED, "settle captured support")
        self._transition(ReorientationPhase.SETTLE)

    def fail_captured_transport(self, *, capture_attempted: bool = False) -> None:
        """Fail a captured-support transaction without changing its constraints."""

        if self.phase is ReorientationPhase.FAILED:
            return
        if (
            capture_attempted
            and self.phase is ReorientationPhase.RELEASE_READY
            and self._settle_branch is None
        ):
            self._settle_branch = "captured"
            self._transition(ReorientationPhase.FAILED)
            return
        if self._settle_branch != "captured" or self.phase not in {
            ReorientationPhase.SUPPORT_CAPTURED,
            ReorientationPhase.HAND_RELEASED,
            ReorientationPhase.SETTLE,
            ReorientationPhase.VALIDATE,
            ReorientationPhase.COMMIT,
        }:
            raise RuntimeError(
                f"cannot fail captured transport while reorientation is {self.phase.value}"
            )
        self._transition(ReorientationPhase.FAILED)

    def validate_captured_support_and_commit(
        self,
        observation: ReorientationObservation,
        *,
        minimum_observed_contact_n: float | None = None,
    ) -> dict[str, object]:
        self._require(ReorientationPhase.SETTLE, "validate captured support")
        if self._settle_branch != "captured":
            raise RuntimeError("cannot validate captured support from the canonical branch")
        if self.target_frame is None or self.initial_state_checksum is None:
            raise RuntimeError("reorientation target state is missing")
        initial_frame = self.cube_frame
        self._transition(ReorientationPhase.VALIDATE)
        try:
            result = evaluate_reorientation(
                observation,
                expected_initial_checksum=self.initial_state_checksum,
                minimum_observed_contact_n=minimum_observed_contact_n,
            )
        except Exception:
            self._transition(ReorientationPhase.FAILED)
            raise
        if result["success_tolerance_met"]:
            self._transition(ReorientationPhase.COMMIT)
            try:
                self.backend.finish_transport()
            except Exception:
                self._transition(ReorientationPhase.FAILED)
                raise
            self.cube_frame = self.target_frame
            self._transition(ReorientationPhase.ANCHORED)
        else:
            self._transition(ReorientationPhase.FAILED)
        result.update(
            {
                "initial_cube_frame": [list(row) for row in initial_frame.logical_to_world],
                "final_cube_frame": [list(row) for row in self.cube_frame.logical_to_world],
                "phase_history": [phase.value for phase in self.phase_history],
            }
        )
        return result

    def validate_and_reanchor(
        self,
        observation: ReorientationObservation,
        core_frame: ConstraintFrame,
    ) -> dict[str, object]:
        self._require(ReorientationPhase.SETTLE, "validate the cube")
        if self._settle_branch != "canonical":
            raise RuntimeError("cannot validate the canonical branch from captured support")
        if self.target_frame is None or self.initial_state_checksum is None:
            raise RuntimeError("reorientation target state is missing")
        initial_frame = self.cube_frame
        self._transition(ReorientationPhase.VALIDATE)
        result = evaluate_reorientation(
            observation,
            expected_initial_checksum=self.initial_state_checksum,
        )
        if result["success_tolerance_met"]:
            self._transition(ReorientationPhase.REANCHOR)
            self.backend.reanchor_world(core_frame)
            self.backend.finish_transport()
            self.cube_frame = self.target_frame
            self._transition(ReorientationPhase.ANCHORED)
        else:
            self._transition(ReorientationPhase.FAILED)
        result.update(
            {
                "initial_cube_frame": [list(row) for row in initial_frame.logical_to_world],
                "final_cube_frame": [list(row) for row in self.cube_frame.logical_to_world],
                "phase_history": [phase.value for phase in self.phase_history],
            }
        )
        return result


def legacy_turn_audit(result: dict[str, object]) -> dict[str, object]:
    """Report a completed historical decision without inventing observations.

    The historical mechanism commits predicted state after validation. Record
    that fact only in its return audit, without changing the evaluator's inputs
    or treating measurements absent from TurnObservation as observed defaults.
    """

    audit = dict(result)
    for field in (
        "active_cubie_target_position_error_m",
        "active_cubie_geometry_valid",
        "active_cubie_geometry_reason",
        "core_orientation_error_rad",
        "non_active_cubie_orientation_displacement_rad",
        "fixture_locked",
        "transport_safely_finalized",
        "max_contact_force_n",
        "contact_force_limit_n",
    ):
        audit.pop(field, None)
    audit["predicted_state_committed"] = bool(audit["committed"])
    return audit


class HybridCubeMechanism:
    """Own the discrete cube state and coordinate atomic constraint switches."""

    def __init__(self, backend: ConstraintBackend, cube_state: CubeState | None = None):
        self.backend = backend
        self.cube_state = CubeState.solved() if cube_state is None else cube_state
        self.phase = MechanismPhase.ANCHORED
        self.phase_history = [self.phase]
        self.active_move: str | None = None
        self.active_cubie_ids: tuple[str, ...] = ()
        self.initial_angle_rad = 0.0
        self._geometry_reference: dict[str, ConstraintFrame] | None = None
        self._geometry_detent_applied = False
        self._geometry_detent_uncertain = False

    def geometry_detent_disclosure(self) -> dict[str, bool]:
        """Retain assistance across unpublished actions and failed USD edits."""

        return {
            "used_persistent_geometry_detent": self._geometry_detent_applied,
            "geometry_detent_transaction_uncertain": self._geometry_detent_uncertain,
        }

    def reset(
        self,
        cube_state: CubeState,
        cubie_frames: dict[str, ConstraintFrame],
        world_core_frame: ConstraintFrame,
    ) -> dict[str, object]:
        if set(cubie_frames) != set(cube_state.pieces):
            raise ValueError("reset requires frames for all 26 cubies")
        self.backend.reset(cubie_frames, world_core_frame)
        self._geometry_reference = dict(cubie_frames)
        self._geometry_detent_applied = False
        self._geometry_detent_uncertain = False
        self.cube_state = cube_state
        self.phase = MechanismPhase.ANCHORED
        self.phase_history = [self.phase]
        self.active_move = None
        self.active_cubie_ids = ()
        self.initial_angle_rad = 0.0
        return {
            "reset_applied": True,
            "used_direct_cubie_state_during_move": False,
            "permutation_checksum": cube_state.permutation_checksum(),
            "facelets_urfdlb": cube_state.facelet_string(),
        }

    def begin_turn(
        self,
        move: str,
        cubie_frames: dict[str, ConstraintFrame],
        *,
        initial_angle_rad: float = 0.0,
    ) -> tuple[str, ...]:
        if self.phase is not MechanismPhase.ANCHORED:
            raise RuntimeError(f"cannot begin a turn while mechanism is {self.phase.value}")
        if self._geometry_reference is None:
            raise RuntimeError("reset must initialize geometry references before a turn")
        self.phase_history = [MechanismPhase.ANCHORED]
        atomic = parse_sequence((move,))
        if len(atomic) != 1:
            raise ValueError("begin_turn requires one atomic quarter turn")
        canonical_move = atomic[0]
        active = self.cube_state.active_cubie_ids(canonical_move[0])
        missing = set(active) - set(cubie_frames)
        if missing:
            raise ValueError(f"missing constraint frames for active cubies: {sorted(missing)}")
        axis = FACE_AXIS_SIGN[canonical_move[0]][0].lower()
        self._transition(MechanismPhase.PREPARE)
        self.backend.activate_layer(axis, {cubie_id: cubie_frames[cubie_id] for cubie_id in active})
        self._transition(MechanismPhase.ACTIVE)
        self.active_move = canonical_move
        self.active_cubie_ids = active
        self.initial_angle_rad = float(initial_angle_rad)
        return active

    def begin_settle(self) -> None:
        """Mark the end of robot-driven rotation before release/settling."""

        if self.phase is not MechanismPhase.ACTIVE:
            raise RuntimeError(f"cannot settle while mechanism is {self.phase.value}")
        self._transition(MechanismPhase.SETTLE)

    def _transition(self, phase: MechanismPhase) -> None:
        self.phase = phase
        self.phase_history.append(phase)

    def validate_and_commit(
        self,
        observation: TurnObservation,
        cubie_frames: dict[str, ConstraintFrame],
    ) -> dict[str, object]:
        """Historical Panda decision; its audit discloses predicted-state commit."""

        return legacy_turn_audit(self._validate_and_commit(observation, cubie_frames))

    def validate_and_commit_measured(
        self,
        observation: TurnObservation,
        cubie_frames: dict[str, ConstraintFrame],
        measured_state: CubeState,
        *,
        minimum_observed_contact_n: float | None = None,
        minimum_maintained_contact_n: float | None = None,
    ) -> dict[str, object]:
        """Commit an owned snapshot reconstructed from a fresh native window.

        The environment validates the raw window. This pure boundary compares
        its reconstructed state against the required move instead of trusting
        the controller's permutation flag. Prediction is used only for comparison.
        """

        if not isinstance(measured_state, CubeState):
            raise TypeError("measured commit requires a reconstructed CubeState")
        if self.active_move is None:
            raise RuntimeError("cannot validate without an active turn")
        measured = CubeState.from_dict(measured_state.to_dict())
        checked = replace(
            observation,
            permutation_matches=(measured == self.cube_state.apply_move(self.active_move)),
        )
        audit = legacy_turn_audit(self._validate_and_commit(
            checked, cubie_frames, measured,
            minimum_observed_contact_n=minimum_observed_contact_n,
            minimum_maintained_contact_n=minimum_maintained_contact_n,
        ))
        audit["predicted_state_committed"] = False
        audit["committed_state_source"] = "native_observation" if audit["committed"] else None
        return audit

    def _validate_and_commit(
        self,
        observation: TurnObservation,
        cubie_frames: dict[str, ConstraintFrame],
        measured_state: CubeState | None = None,
        *,
        minimum_observed_contact_n: float | None = None,
        minimum_maintained_contact_n: float | None = None,
    ) -> dict[str, object]:
        if self.phase is MechanismPhase.ACTIVE:
            self.begin_settle()
        if self.phase is not MechanismPhase.SETTLE or self.active_move is None:
            raise RuntimeError("cannot validate without an active turn")
        self._transition(MechanismPhase.VALIDATE)
        result = evaluate_quarter_turn(
            move=self.active_move,
            initial_angle_rad=self.initial_angle_rad,
            final_angle_rad=observation.final_angle_rad,
            final_angular_velocity_rad_s=observation.final_angular_velocity_rad_s,
            left_contact_forces_n=observation.left_contact_forces_n,
            right_contact_forces_n=observation.right_contact_forces_n,
            wrist_axis_delta_rad=observation.wrist_axis_delta_rad,
            core_pose_error_m=observation.core_pose_error_m,
            active_cubie_alignment_error_m=observation.active_cubie_alignment_error_m,
            non_active_cubie_displacement_m=observation.non_active_cubie_displacement_m,
            permutation_matches=observation.permutation_matches,
            native_pose_window_valid=observation.native_pose_window_valid,
            abort_reason=observation.abort_reason,
            used_internal_constraint_switching=True,
            used_direct_cubie_state_during_move=False,
            used_active_cube_drive=False,
            used_hard_joint_limit=False,
            used_robot_cube_attachment=False,
            used_passive_detent=True,
            minimum_observed_contact_n=minimum_observed_contact_n,
            minimum_maintained_contact_n=minimum_maintained_contact_n,
        )
        committed = bool(result["success_tolerance_met"])
        if committed:
            expected_ids = set(self.cube_state.pieces)
            if set(cubie_frames) != expected_ids:
                raise ValueError("commit requires current frames for all 26 cubies")
            # These targets preserve the reset geometry. They are advanced only
            # after actual carrier/wrist motion and the measured prefix pass;
            # endpoint solver deformation never becomes the next reference.
            if self._geometry_reference is None:
                raise RuntimeError("reset geometry references are missing")
            delta = observation.final_angle_rad - self.initial_angle_rad
            sign = 1 if delta > 0.0 else -1
            axis = FACE_AXIS_SIGN[self.active_move[0]][0].lower()
            reference = dict(self._geometry_reference)
            for cubie_id in self.active_cubie_ids:
                reference[cubie_id] = _rotate_geometry_reference(reference[cubie_id], axis, sign)
            self._transition(MechanismPhase.COMMIT)
            self._geometry_detent_uncertain = True
            try:
                self.backend.anchor_all(reference)
            except BaseException:
                self._transition(MechanismPhase.FAILED)
                raise
            self._geometry_detent_applied = True
            self._geometry_detent_uncertain = False
            self._geometry_reference = reference
            self.cube_state = (
                measured_state if measured_state is not None
                else self.cube_state.apply_move(self.active_move)
            )
            self._transition(MechanismPhase.ANCHORED)
        else:
            self._transition(MechanismPhase.FAILED)
        result.update(
            {
                "committed": committed,
                "used_persistent_geometry_detent": committed,
                "geometry_reference_source": "reset_frames_and_accepted_measured_quarter_turns",
                "active_cubie_ids": list(self.active_cubie_ids),
                "permutation_checksum": self.cube_state.permutation_checksum(),
                "facelets_urfdlb": self.cube_state.facelet_string(),
                "phase_history": [phase.value for phase in self.phase_history],
            }
        )
        return result
