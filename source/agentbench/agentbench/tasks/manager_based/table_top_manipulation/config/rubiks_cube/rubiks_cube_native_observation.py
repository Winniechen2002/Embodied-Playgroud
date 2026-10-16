"""Read and evaluate measured native PhysX Rubik's Cube link poses.

This module reports an observation envelope only.  It does not infer a move,
advance symbolic state, or establish acceptance of any controller action.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Integral, Real

import numpy as np

try:
    from .rubiks_cube_geometry import CUBIE_SIZE_M, sticker_box_transform
    from .rubiks_cube_observer import (
        _validate_body_names,
        _validate_native_poses,
        classify_native_snapshot,
    )
    from .rubiks_cube_pose import evaluate_contiguous_pose_window
    from .rubiks_cube_rules import CubeState
except ImportError:  # Loaded directly by dependency-light unit tests.
    from rubiks_cube_geometry import CUBIE_SIZE_M, sticker_box_transform
    from rubiks_cube_observer import (
        _validate_body_names,
        _validate_native_poses,
        classify_native_snapshot,
    )
    from rubiks_cube_pose import evaluate_contiguous_pose_window
    from rubiks_cube_rules import CubeState


_NATIVE_CLOCK_TOLERANCE_S = 2e-6
_SOLVED_STICKER_CATALOG = tuple(
    (identity, tuple(piece.stickers))
    for identity, piece in CubeState.solved().pieces.items()
)


def _nonnegative_integer(value, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise TypeError(f"{label} must be a non-negative integer")
    converted = int(value)
    if converted < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return converted


def _nonnegative_real(value, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{label} must be a finite non-negative real number")
    converted = float(value)
    if not math.isfinite(converted) or converted < 0.0:
        raise ValueError(f"{label} must be a finite non-negative real number")
    return converted


def _positive_real(value, label: str) -> float:
    converted = _nonnegative_real(value, label)
    if converted <= 0.0:
        raise ValueError(f"{label} must be a finite positive real number")
    return converted


def _finite_real(value, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{label} must be a finite real number")
    try:
        converted = float(value)
    except OverflowError as error:
        raise ValueError(f"{label} must be a finite real number") from error
    if not math.isfinite(converted):
        raise ValueError(f"{label} must be a finite real number")
    return converted


def _validate_velocities(raw_com_velocities) -> np.ndarray:
    try:
        velocities = np.asarray(raw_com_velocities, dtype=np.float64)
    except (TypeError, ValueError) as error:
        raise ValueError("finite (31, 6) raw COM velocities are required") from error
    if velocities.shape != (31, 6) or not np.isfinite(velocities).all():
        raise ValueError("finite (31, 6) raw COM velocities are required")
    return velocities


def _immutable_rows(values: np.ndarray) -> tuple[tuple[float, ...], ...]:
    return tuple(tuple(float(value) for value in row) for row in values)


@dataclass(frozen=True)
class NativeCubeSample:
    """One copied native-link measurement with no freshness or stability claim."""

    native_step: int
    native_time_s: float
    body_names: tuple[str, ...]
    native_link_transforms_xyzw: tuple[tuple[float, ...], ...]
    raw_com_velocities: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        native_step = _nonnegative_integer(self.native_step, "native_step")
        native_time = _nonnegative_real(self.native_time_s, "native_time_s")
        names = _validate_body_names(self.body_names)
        poses, _ = _validate_native_poses(self.native_link_transforms_xyzw)
        velocities = _validate_velocities(self.raw_com_velocities)
        object.__setattr__(self, "native_step", native_step)
        object.__setattr__(self, "native_time_s", native_time)
        object.__setattr__(self, "body_names", names)
        object.__setattr__(
            self, "native_link_transforms_xyzw", _immutable_rows(poses.copy())
        )
        object.__setattr__(
            self, "raw_com_velocities", _immutable_rows(velocities.copy())
        )


def _copied_numpy(buffer) -> np.ndarray:
    detached = buffer.detach() if hasattr(buffer, "detach") else buffer
    cpu_buffer = detached.cpu() if hasattr(detached, "cpu") else detached
    values = cpu_buffer.numpy() if hasattr(cpu_buffer, "numpy") else cpu_buffer
    return np.array(values, copy=True)


def _single_environment_buffer(buffer, label: str) -> np.ndarray:
    values = _copied_numpy(buffer)
    if values.ndim != 3 or values.shape[0] != 1:
        raise ValueError(f"{label} must contain exactly one environment")
    return values


def read_native_cube_sample(parts, sim) -> NativeCubeSample:
    """Copy env-0 native transforms and COM velocities without advancing PhysX."""

    step_before = sim.current_time_step_index
    time_before = sim.current_time
    native_transforms = parts.reshape_view_to_data(
        parts.root_physx_view.get_transforms()
    )
    native_velocities = parts.reshape_view_to_data(
        parts.root_physx_view.get_velocities()
    )
    transform_environments = _single_environment_buffer(
        native_transforms, "native transforms"
    )
    velocity_environments = _single_environment_buffer(
        native_velocities, "native velocities"
    )
    step_after = sim.current_time_step_index
    time_after = sim.current_time
    if step_after != step_before or time_after != time_before:
        raise RuntimeError("native simulation clock changed while reading cube sample")

    transforms = transform_environments[0].copy()
    velocities = velocity_environments[0].copy()
    return NativeCubeSample(
        native_step=step_before,
        native_time_s=time_before,
        body_names=parts.object_names,
        native_link_transforms_xyzw=transforms,
        raw_com_velocities=velocities,
    )


def _normalized_rotation_from_xyzw(pose: tuple[float, ...]) -> np.ndarray:
    quaternion_xyzw = np.asarray(pose[3:], dtype=np.float64)
    x, y, z, w = quaternion_xyzw / np.linalg.norm(quaternion_xyzw)
    return np.asarray(
        [
            [
                1.0 - 2.0 * (y * y + z * z),
                2.0 * (x * y - z * w),
                2.0 * (x * z + y * w),
            ],
            [
                2.0 * (x * y + z * w),
                1.0 - 2.0 * (x * x + z * z),
                2.0 * (y * z - x * w),
            ],
            [
                2.0 * (x * z - y * w),
                2.0 * (y * z + x * w),
                1.0 - 2.0 * (x * x + y * y),
            ],
        ],
        dtype=np.float64,
    )


def evaluate_native_cube_rigidity(
    reference: NativeCubeSample,
    sample: NativeCubeSample,
    *,
    position_tolerance_m: float = 0.001,
    rotation_tolerance_rad: float = math.pi / 180,
) -> dict[str, object]:
    """Compare all 26 cubie frames relative to their independently measured core.

    Global lift and rotation cancel out of this comparison. Calling this for
    each native sample detects transient internal deformation even when an
    action eventually returns to its initial logical state. Clock continuity,
    expected logical state, and transport qualification remain caller duties.
    """
    if not isinstance(reference, NativeCubeSample) or not isinstance(sample, NativeCubeSample):
        raise TypeError('rigidity requires copied native cube samples')
    position_tolerance_m = _positive_real(position_tolerance_m, 'position tolerance')
    rotation_tolerance_rad = _positive_real(rotation_tolerance_rad, 'rotation tolerance')

    def relative_frames(value):
        poses = dict(zip(value.body_names, value.native_link_transforms_xyzw, strict=True))
        core = poses['core']
        core_rotation = _normalized_rotation_from_xyzw(core)
        return {
            name: (core_rotation.T @ (np.asarray(pose[:3]) - core[:3]),
                   core_rotation.T @ _normalized_rotation_from_xyzw(pose))
            for name, pose in poses.items() if name.startswith('cubie_')
        }

    before, after = relative_frames(reference), relative_frames(sample)
    if set(before) != set(after) or len(before) != 26:
        raise ValueError('rigidity requires the same 26 cubie identities')
    errors = {}
    for name, (position, rotation) in before.items():
        next_position, next_rotation = after[name]
        errors[name] = {
            'position_m': float(np.linalg.norm(position - next_position)),
            'rotation_rad': float(np.arccos(np.clip((np.trace(rotation.T @ next_rotation) - 1) / 2, -1, 1))),
        }
    violations = sorted(name for name, error in errors.items()
                        if error['position_m'] > position_tolerance_m
                        or error['rotation_rad'] > rotation_tolerance_rad)
    return {'passed': not violations, 'reference_native_step': reference.native_step,
            'native_step': sample.native_step, 'violating_cubie_ids': violations,
            'maximum_position_error_m': max(error['position_m'] for error in errors.values()),
            'maximum_rotation_error_rad': max(error['rotation_rad'] for error in errors.values()),
            'cubie_errors': errors}


def evaluate_native_turn_rigidity(
    reference: NativeCubeSample,
    sample: NativeCubeSample,
    *,
    active_axis: str,
    active_cubie_ids,
    position_tolerance_m: float = 0.001,
    rotation_tolerance_rad: float = math.pi / 180,
    maximum_carrier_rotation_rad: float = math.radians(120),
) -> dict[str, object]:
    """Check a partial turn without requiring a discrete quarter-turn state.

    Core and inactive cubies stay fixed in world coordinates; each active cubie
    keeps its measured carrier-relative frame. The caller supplies identities
    from the verified prefix and invokes this at every contiguous native step.
    This neither proves contact nor accepts a final logical state or direction.
    """
    if not isinstance(reference, NativeCubeSample) or not isinstance(sample, NativeCubeSample):
        raise TypeError('turn rigidity requires copied native cube samples')
    active = tuple(active_cubie_ids)
    known = {name for name in reference.body_names if name.startswith('cubie_')}
    if (active_axis not in ('x', 'y', 'z') or len(active) != 9 or len(set(active)) != 9
            or not set(active) <= known or set(reference.body_names) != set(sample.body_names)):
        raise ValueError('invalid active layer identity or carrier axis')
    position_tolerance = _positive_real(position_tolerance_m, 'position tolerance')
    rotation_tolerance = _positive_real(rotation_tolerance_rad, 'rotation tolerance')
    maximum_rotation = _positive_real(maximum_carrier_rotation_rad, 'carrier rotation limit')
    if maximum_rotation >= math.pi:
        raise ValueError('carrier rotation limit must be less than pi')

    def frames(value):
        return {name: (np.asarray(pose[:3]), _normalized_rotation_from_xyzw(pose))
                for name, pose in zip(value.body_names, value.native_link_transforms_xyzw)}

    def error(first, second):
        return (float(np.linalg.norm(first[0] - second[0])),
                float(np.arccos(np.clip((np.trace(first[1].T @ second[1]) - 1) / 2, -1, 1))))

    def relative(carrier, body):
        return carrier[1].T @ (body[0] - carrier[0]), carrier[1].T @ body[1]

    before, after = frames(reference), frames(sample)
    carrier_name = 'carrier_' + active_axis
    core_error = error(before['core'], after['core'])
    inactive_errors = {name: error(before[name], after[name]) for name in known - set(active)}
    active_errors = {name: error(relative(before[carrier_name], before[name]),
                                 relative(after[carrier_name], after[name])) for name in active}
    carrier_rotation = error(before[carrier_name], after[carrier_name])[1]
    violates = lambda value: value[0] > position_tolerance or value[1] > rotation_tolerance
    inactive_bad = sorted(name for name, value in inactive_errors.items() if violates(value))
    active_bad = sorted(name for name, value in active_errors.items() if violates(value))
    return {'passed': not (violates(core_error) or inactive_bad or active_bad or carrier_rotation > maximum_rotation),
            'reference_native_step': reference.native_step, 'native_step': sample.native_step,
            'active_axis': active_axis, 'active_cubie_ids': list(active),
            'core_position_error_m': core_error[0], 'core_rotation_error_rad': core_error[1],
            'maximum_inactive_position_error_m': max(value[0] for value in inactive_errors.values()),
            'maximum_inactive_rotation_error_rad': max(value[1] for value in inactive_errors.values()),
            'maximum_active_position_error_m': max(value[0] for value in active_errors.values()),
            'maximum_active_rotation_error_rad': max(value[1] for value in active_errors.values()),
            'carrier_rotation_rad': carrier_rotation,
            'violating_inactive_cubie_ids': inactive_bad, 'violating_active_cubie_ids': active_bad}


def _box_minimum_world_z(
    center: np.ndarray, rotation: np.ndarray, dimensions: tuple[float, float, float]
) -> float:
    half_dimensions = 0.5 * np.asarray(dimensions, dtype=np.float64)
    vertical_radius = float(np.dot(np.abs(rotation[2]), half_dimensions))
    return float(center[2]) - vertical_radius


def measure_native_support_geometry(
    sample: NativeCubeSample,
    *,
    table_height_m: float,
    include_stickers: bool = True,
) -> dict[str, object]:
    """Measure actual cubie/sticker box support from one native pose sample.

    The result is geometry relative to the supplied table height.  It makes no
    grasp, stability, placement-acceptance, or task-success claim.
    """

    if not isinstance(sample, NativeCubeSample):
        raise TypeError("sample must be a NativeCubeSample")
    table_height = _finite_real(table_height_m, "table_height_m")
    if not isinstance(include_stickers, bool):
        raise TypeError("include_stickers must be a bool")

    indices = {name: index for index, name in enumerate(sample.body_names)}
    cubie_dimensions = (CUBIE_SIZE_M, CUBIE_SIZE_M, CUBIE_SIZE_M)
    cubie_records: list[tuple[float, str, str, tuple[float, float, float]]] = []
    sticker_records: list[tuple[float, str, str, tuple[float, float, float]]] = []

    for identity, sticker_faces in _SOLVED_STICKER_CATALOG:
        pose = sample.native_link_transforms_xyzw[indices[identity]]
        center = np.asarray(pose[:3], dtype=np.float64)
        rotation = _normalized_rotation_from_xyzw(pose)
        cubie_records.append(
            (
                _box_minimum_world_z(center, rotation, cubie_dimensions),
                identity,
                "cubie_box",
                cubie_dimensions,
            )
        )
        for face in sticker_faces:
            local_offset, dimensions = sticker_box_transform(face)
            sticker_center = center + rotation @ np.asarray(
                local_offset, dtype=np.float64
            )
            sticker_records.append(
                (
                    _box_minimum_world_z(sticker_center, rotation, dimensions),
                    identity,
                    f"sticker_{face}",
                    dimensions,
                )
            )

    cubie_minimum = min(cubie_records)
    sticker_inclusive_minimum = min((*cubie_records, *sticker_records))
    selected_minimum = (
        sticker_inclusive_minimum if include_stickers else cubie_minimum
    )
    table_gap = selected_minimum[0] - table_height

    return {
        "source": "native_physx_link_transforms",
        "native_step": sample.native_step,
        "native_time_s": sample.native_time_s,
        "table_height_m": table_height,
        "include_stickers": include_stickers,
        "evaluated_cubie_count": len(cubie_records),
        "evaluated_sticker_count": len(sticker_records),
        "cubie_box_dimensions_xyz_m": cubie_dimensions,
        "sticker_box_dimensions_xyz_m_by_face": {
            face: sticker_box_transform(face)[1] for face in "URFDLB"
        },
        "geometry_provenance": {
            "poses": "validated_native_link_transforms_xyzw",
            "cubie_dimensions": "CUBIE_SIZE_M",
            "sticker_geometry": "sticker_box_transform",
            "sticker_identity": "immutable_solved_catalog",
        },
        "cubie_only_minimum_z_m": cubie_minimum[0],
        "cubie_only_responsible_body": cubie_minimum[1],
        "cubie_only_responsible_feature": cubie_minimum[2],
        "cubie_only_responsible_dimensions_xyz_m": cubie_minimum[3],
        "sticker_inclusive_minimum_z_m": sticker_inclusive_minimum[0],
        "sticker_inclusive_responsible_body": sticker_inclusive_minimum[1],
        "sticker_inclusive_responsible_feature": sticker_inclusive_minimum[2],
        "sticker_inclusive_responsible_dimensions_xyz_m": sticker_inclusive_minimum[3],
        "selected_minimum_z_m": selected_minimum[0],
        "selected_responsible_body": selected_minimum[1],
        "selected_responsible_feature": selected_minimum[2],
        "selected_responsible_dimensions_xyz_m": selected_minimum[3],
        "table_gap_m": table_gap,
        "penetration_depth_m": max(0.0, -table_gap),
    }


def evaluate_native_cube_window(
    samples,
    *,
    physics_dt_s,
    after_step,
    minimum_duration_s=0.5,
    position_tolerance_m=0.001,
    rotation_tolerance_rad=math.radians(1.0),
    ignore_center_twist=False,
):
    """Classify the final snapshot and report stationarity of every native body."""

    if type(ignore_center_twist) is not bool:
        raise TypeError("ignore_center_twist must be bool")
    physics_dt = _positive_real(physics_dt_s, "physics_dt_s")
    minimum_duration = _positive_real(minimum_duration_s, "minimum_duration_s")
    position_tolerance = _positive_real(
        position_tolerance_m, "position_tolerance_m"
    )
    rotation_tolerance = _positive_real(
        rotation_tolerance_rad, "rotation_tolerance_rad"
    )
    after = _nonnegative_integer(after_step, "after_step")
    if not isinstance(samples, (list, tuple)) or len(samples) < 2:
        raise ValueError("native cube window must contain at least two samples")
    if any(not isinstance(sample, NativeCubeSample) for sample in samples):
        raise TypeError("native cube window must contain NativeCubeSample values")

    first = samples[0]
    names = first.body_names
    for sample in samples[1:]:
        if sample.body_names != names:
            raise ValueError("native cube body-name ordering changed within window")
    steps = [sample.native_step for sample in samples]
    if any(current != previous + 1 for previous, current in zip(steps, steps[1:])):
        raise ValueError("native cube window steps must be contiguous")
    if any(step <= after for step in steps):
        raise ValueError("all native cube samples must be later than after_step")

    times = [sample.native_time_s for sample in samples]
    if any(current <= previous for previous, current in zip(times, times[1:])):
        raise ValueError("native cube sample times must be strictly increasing")
    for previous_step, step, previous_time, time_s in zip(
        steps, steps[1:], times, times[1:]
    ):
        expected_elapsed = (step - previous_step) * physics_dt
        if abs((time_s - previous_time) - expected_elapsed) > _NATIVE_CLOCK_TOLERANCE_S:
            raise ValueError("native cube sample time does not match physics steps")
    nominal_duration = (steps[-1] - steps[0]) * physics_dt
    native_duration = times[-1] - times[0]
    if abs(native_duration - nominal_duration) > _NATIVE_CLOCK_TOLERANCE_S:
        raise ValueError("native cube window duration does not match physics steps")

    body_reports = {}
    for body_index, body_name in enumerate(names):
        body_samples = [
            (
                sample.native_step,
                sample.native_link_transforms_xyzw[body_index][:3],
                (
                    sample.native_link_transforms_xyzw[body_index][6],
                    sample.native_link_transforms_xyzw[body_index][3],
                    sample.native_link_transforms_xyzw[body_index][4],
                    sample.native_link_transforms_xyzw[body_index][5],
                ),
            )
            for sample in samples
        ]
        body_reports[body_name] = evaluate_contiguous_pose_window(
            body_samples,
            physics_dt_s=physics_dt,
            minimum_duration_s=minimum_duration,
            after_step=after,
            position_tolerance_m=position_tolerance,
            rotation_tolerance_rad=rotation_tolerance,
        )

    final = samples[-1]
    measured_state, classifier_diagnostics = classify_native_snapshot(
        final.body_names, final.native_link_transforms_xyzw,
        ignore_center_twist=ignore_center_twist,
    )
    core_pose = final.native_link_transforms_xyzw[names.index("core")]
    linear_speed_max = max(
        math.hypot(*velocity[:3])
        for sample in samples
        for velocity in sample.raw_com_velocities
    )
    angular_speed_max = max(
        math.hypot(*velocity[3:])
        for sample in samples
        for velocity in sample.raw_com_velocities
    )
    diagnostics = {
        "source": "native_physx_link_transforms",
        "stable": all(report["stable"] for report in body_reports.values()),
        "sample_count": len(samples),
        "first_native_step": steps[0],
        "last_native_step": steps[-1],
        "first_native_time_s": times[0],
        "last_native_time_s": times[-1],
        "duration_s": nominal_duration,
        "native_clock_duration_s": native_duration,
        "after_step": after,
        "physics_dt_s": physics_dt,
        "minimum_duration_s": minimum_duration,
        "position_tolerance_m": position_tolerance,
        "rotation_tolerance_rad": rotation_tolerance,
        "body_diameter_reports": body_reports,
        "final_core_world_position_xyz_m": tuple(float(value) for value in core_pose[:3]),
        "final_core_world_quaternion_wxyz": (
            float(core_pose[6]),
            float(core_pose[3]),
            float(core_pose[4]),
            float(core_pose[5]),
        ),
        "classifier_diagnostics": classifier_diagnostics,
        "raw_velocity_max_linear_m_s": linear_speed_max,
        "raw_velocity_max_angular_rad_s": angular_speed_max,
    }
    return measured_state, diagnostics


__all__ = [
    "NativeCubeSample",
    "evaluate_native_cube_window",
    "measure_native_support_geometry",
    "read_native_cube_sample",
]
