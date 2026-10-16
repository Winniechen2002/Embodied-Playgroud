"""Classify one measured native-link snapshot into a discrete cubie state.

This module classifies only the supplied snapshot.  It does not establish sample
freshness, motion direction, grasp, stability, or complete sequence success.
"""

from __future__ import annotations

import math
from numbers import Real
from typing import Sequence

import numpy as np

try:
    from .rubiks_cube_mechanism import is_legal_cube_state
    from .rubiks_cube_pose import (
        _stable_wxyz_distance_rad,
        multiply_quaternions,
        quaternion_from_yaw_and_frame,
    )
    from .rubiks_cube_rules import CubeFrame, CubeState, CubieState, FACE_NORMALS
except ImportError:  # Loaded directly by dependency-light unit tests.
    from rubiks_cube_mechanism import is_legal_cube_state
    from rubiks_cube_pose import (
        _stable_wxyz_distance_rad,
        multiply_quaternions,
        quaternion_from_yaw_and_frame,
    )
    from rubiks_cube_rules import CubeFrame, CubeState, CubieState, FACE_NORMALS


_SOLVED_CATALOG = CubeState.solved().pieces
_EXPECTED_BODY_NAMES = frozenset(_SOLVED_CATALOG) | {
    "world_anchor",
    "core",
    "carrier_x",
    "carrier_y",
    "carrier_z",
}
_SLOTS = np.asarray(
    [piece.home_position for piece in _SOLVED_CATALOG.values()], dtype=np.float64
)
_FRAMES = CubeFrame.all()
_FRAME_QUATERNIONS = tuple(
    quaternion_from_yaw_and_frame(0.0, frame) for frame in _FRAMES
)


def _finite_positive(value, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{label} must be a finite positive real number")
    converted = float(value)
    if not math.isfinite(converted) or converted <= 0.0:
        raise ValueError(f"{label} must be a finite positive real number")
    return converted


def _validate_body_names(body_names) -> tuple[str, ...]:
    try:
        names = tuple(body_names)
    except TypeError as error:
        raise ValueError("exactly 31 unique known body names are required") from error
    if (
        len(names) != 31
        or any(not isinstance(name, str) for name in names)
        or len(set(names)) != 31
        or set(names) != _EXPECTED_BODY_NAMES
    ):
        raise ValueError("exactly 31 unique known body names are required")
    return names


def _validate_native_poses(native_link_transforms_xyzw) -> tuple[np.ndarray, np.ndarray]:
    try:
        poses = np.asarray(native_link_transforms_xyzw, dtype=np.float64)
    except (TypeError, ValueError) as error:
        raise ValueError("finite (31, 7) native link poses are required") from error
    if poses.shape != (31, 7) or not np.isfinite(poses).all():
        raise ValueError("finite (31, 7) native link poses are required")
    norms = np.linalg.norm(poses[:, 3:], axis=1)
    if np.any(np.abs(norms - 1.0) > 1e-3):
        raise ValueError("native quaternion norm differs materially from unity")
    return poses, norms


def _rotation_matrix(quaternion_wxyz: Sequence[float]) -> np.ndarray:
    w, x, y, z = quaternion_wxyz
    return np.asarray(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ],
        dtype=np.float64,
    )


def classify_native_snapshot(
    body_names,
    native_link_transforms_xyzw,
    *,
    pitch_m=0.024,
    position_tolerance_m=0.001,
    orientation_tolerance_rad=math.radians(2.0),
    ignore_center_twist=False,
) -> tuple[CubeState | None, dict[str, object]]:
    """Return the cubie state measured in one native-link snapshot.

    Poses contain world positions followed by quaternions in ``xyzw`` order.
    The solved catalog supplies immutable identity, home, and sticker metadata;
    every current position and orientation comes from a pose relative to the
    measured core.
    """

    pitch = _finite_positive(pitch_m, "pitch_m")
    if type(ignore_center_twist) is not bool:
        raise TypeError('ignore_center_twist must be bool')
    position_tolerance = _finite_positive(
        position_tolerance_m, "position_tolerance_m"
    )
    orientation_tolerance = _finite_positive(
        orientation_tolerance_rad, "orientation_tolerance_rad"
    )
    names = _validate_body_names(body_names)
    poses, quaternion_norms = _validate_native_poses(native_link_transforms_xyzw)

    indices = {name: index for index, name in enumerate(names)}
    quaternions_wxyz = poses[:, [6, 3, 4, 5]] / quaternion_norms[:, None]
    core_index = indices["core"]
    core_position = poses[core_index, :3]
    core_quaternion = quaternions_wxyz[core_index]
    core_rotation = _rotation_matrix(core_quaternion)
    inverse_core_quaternion = (
        float(core_quaternion[0]),
        -float(core_quaternion[1]),
        -float(core_quaternion[2]),
        -float(core_quaternion[3]),
    )

    pieces: dict[str, CubieState] = {}
    piece_diagnostics: list[dict[str, object]] = []
    reasons: list[str] = []
    occupied_slots: dict[tuple[int, int, int], str] = {}
    scaled_slots = _SLOTS * pitch

    for identity, home in _SOLVED_CATALOG.items():
        body_index = indices[identity]
        core_relative_position = core_rotation.T @ (
            poses[body_index, :3] - core_position
        )
        core_relative_quaternion = multiply_quaternions(
            inverse_core_quaternion, quaternions_wxyz[body_index]
        )

        position_errors = np.linalg.norm(
            scaled_slots - core_relative_position, axis=1
        )
        position_order = np.argsort(position_errors)
        nearest_slot_index = int(position_order[0])
        position_residual = float(position_errors[nearest_slot_index])
        slot = tuple(int(value) for value in _SLOTS[nearest_slot_index])

        orientation_errors = np.asarray(
            [
                _stable_wxyz_distance_rad(core_relative_quaternion, candidate)
                for candidate in _FRAME_QUATERNIONS
            ],
            dtype=np.float64,
        )
        frame_indices = list(range(len(_FRAMES)))
        if ignore_center_twist and len(home.stickers) == 1:
            # A monochrome center supplies a normal, not a roll orientation.
            # Keep one representative of each distinct sticker normal; four
            # rotations about that normal are the same visible configuration.
            normal = np.asarray(FACE_NORMALS[home.stickers[0]], dtype=float)
            actual_normal = _rotation_matrix(core_relative_quaternion) @ normal
            representatives = {}
            for index, frame in enumerate(_FRAMES):
                n = tuple(np.asarray(frame.logical_to_world) @ normal)
                representatives.setdefault(n, index)
            frame_indices = list(representatives.values())
            orientation_errors = np.arccos(np.clip(
                np.asarray(list(representatives)) @ actual_normal, -1., 1.))
        orientation_order = np.argsort(orientation_errors)
        nearest_error_index = int(orientation_order[0])
        nearest_frame_index = frame_indices[nearest_error_index]
        orientation_residual = float(orientation_errors[nearest_error_index])
        orientation = _FRAMES[nearest_frame_index].logical_to_world

        if position_residual > position_tolerance:
            reasons.append(f"{identity}:position_residual")
        if abs(
            float(position_errors[position_order[1]]) - position_residual
        ) <= 1e-10:
            reasons.append(f"{identity}:ambiguous_position")
        if orientation_residual > orientation_tolerance:
            reasons.append(f"{identity}:orientation_residual")
        if abs(
            float(orientation_errors[orientation_order[1]]) - orientation_residual
        ) <= 1e-10:
            reasons.append(f"{identity}:ambiguous_orientation")
        if slot in occupied_slots:
            reasons.append(
                f"{identity}:duplicate_slot_with_{occupied_slots[slot]}"
            )
        occupied_slots[slot] = identity

        pieces[identity] = CubieState(
            identity=identity,
            home_position=home.home_position,
            position=slot,
            orientation=orientation,
            stickers=home.stickers,
        )
        piece_diagnostics.append(
            {
                "identity": identity,
                "raw_core_relative_position_m": [
                    float(value) for value in core_relative_position
                ],
                "raw_core_relative_quaternion_wxyz": [
                    float(value) for value in core_relative_quaternion
                ],
                "nearest_slot": list(slot),
                "nearest_orientation": [list(row) for row in orientation],
                "position_residual_m": position_residual,
                "orientation_residual_rad": orientation_residual,
            }
        )

    candidate = CubeState(pieces)
    legal = is_legal_cube_state(candidate, ignore_center_twist=ignore_center_twist)
    if not legal:
        reasons.append("classified_state_illegal")
    valid = not reasons
    diagnostics: dict[str, object] = {
        "valid": valid,
        "reasons": reasons,
        "classification_tolerances": {
            "pitch_m": pitch,
            "position_m": position_tolerance,
            "orientation_rad": orientation_tolerance,
        },
        "quaternion_raw_norm_range": [
            float(quaternion_norms.min()),
            float(quaternion_norms.max()),
        ],
        "core_world_pose_xyzw": [float(value) for value in poses[core_index]],
        "pieces": piece_diagnostics,
        "max_position_residual_m": max(
            detail["position_residual_m"] for detail in piece_diagnostics
        ),
        "max_orientation_residual_rad": max(
            detail["orientation_residual_rad"] for detail in piece_diagnostics
        ),
        "measured_facelets_urfdlb": candidate.facelet_string() if valid else None,
        "measured_checksum": candidate.permutation_checksum() if valid else None,
        "legal": legal,
        "predicted_state_used": False,
    }
    return (candidate if valid else None), diagnostics


__all__ = ["classify_native_snapshot"]
