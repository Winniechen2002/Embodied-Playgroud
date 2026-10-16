"""Pure eligibility for measured support capture, never capture or sequence success.

A passing gate still requires independent post-release/retreat validation. The
caller supplies actual execution/contact history; this module cannot authenticate
its provenance and never accesses a backend or advances simulation.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import math

try:
    from .rubiks_cube_native_observation import (
        NativeCubeSample, evaluate_native_cube_window, measure_native_support_geometry,
        _finite_real, _nonnegative_integer, _nonnegative_real, _positive_real,
    )
    from .rubiks_cube_native_prefix import NativeSampleRing, evaluate_native_prefix
    from .rubiks_cube_rigid_pose import Pose, evaluate_placement_evidence
    from .rubiks_cube_rules import CubeState
    from .rubiks_cube_mechanism import (
        REORIENTATION_LIFT_MINIMUM_M,
    )
except ImportError:  # Dependency-light direct loading.
    from rubiks_cube_native_observation import (
        NativeCubeSample, evaluate_native_cube_window, measure_native_support_geometry,
        _finite_real, _nonnegative_integer, _nonnegative_real, _positive_real,
    )
    from rubiks_cube_native_prefix import NativeSampleRing, evaluate_native_prefix
    from rubiks_cube_rigid_pose import Pose, evaluate_placement_evidence
    from rubiks_cube_rules import CubeState
    from rubiks_cube_mechanism import (
        REORIENTATION_LIFT_MINIMUM_M,
    )


@dataclass(frozen=True)
class SupportCaptureMotionEvidence:
    """Observed transport phases, measured peak lift and ordered paired forces.

    Each force pair is (left, right), in newtons, for one transport step. Forces
    remain diagnostics after attachment and reject only above 20 N. Driver flags
    are strict bools; force values and lift are finite, nonnegative numbers.
    """
    attachment_acquired: bool
    attachment_verified: bool
    attachment_maintained: bool
    executed_lift: bool
    executed_continuous_motion: bool
    lift_height_m: float
    contact_force_pairs_n: tuple[tuple[float, float], ...]

    def __post_init__(self):
        for name in ('attachment_acquired', 'attachment_verified', 'attachment_maintained',
                     'executed_lift', 'executed_continuous_motion'):
            if type(getattr(self, name)) is not bool:
                raise TypeError(f'{name} must be bool')
        object.__setattr__(self, 'lift_height_m', _nonnegative_real(self.lift_height_m, 'lift_height_m'))
        pairs = []
        for pair in self.contact_force_pairs_n:
            if len(pair) != 2:
                raise ValueError('contact samples must be left/right pairs')
            pairs.append(tuple(_nonnegative_real(value, 'contact force') for value in pair))
        object.__setattr__(self, 'contact_force_pairs_n', tuple(pairs))


def _validate_pose(pose: Pose, label: str) -> Pose:
    if not isinstance(pose, Pose):
        raise TypeError(f'{label} must be Pose')
    if len(pose.position) != 3 or len(pose.quaternion) != 4:
        raise ValueError(f'{label} must have 3 position and 4 quaternion values')
    position = tuple(_finite_real(value, label) for value in pose.position)
    quaternion = tuple(_finite_real(value, label) for value in pose.quaternion)
    norm = math.hypot(*quaternion)
    if not math.isfinite(norm) or norm < 1e-12:
        raise ValueError(f'{label} quaternion norm must be finite and positive')
    return Pose(position, quaternion)


def _motion_diagnostics(evidence: SupportCaptureMotionEvidence) -> dict:
    pairs = evidence.contact_force_pairs_n
    max_force = max((force for pair in pairs for force in pair), default=0.0)
    reason = next((f'support_capture_{name}_missing' for name in
                   ('attachment_acquired', 'attachment_verified', 'attachment_maintained',
                    'executed_lift', 'executed_continuous_motion')
                   if not getattr(evidence, name)), None)
    if reason is None:
        if evidence.lift_height_m < REORIENTATION_LIFT_MINIMUM_M:
            reason = 'whole_cube_lift_insufficient'
        elif max_force > 20.0:
            reason = 'whole_cube_excessive_contact_force'
    return dict(asdict(evidence), max_contact_force_n=max_force,
                accepted=reason is None, abort_reason=reason)


def _json_safe(value):
    """Represent overflow diagnostics as null, never JSON's nonstandard Infinity."""
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_safe(item) for item in value]
    return value


def evaluate_support_capture_gate(
    *,
    current_sample: NativeCubeSample,
    sample_ring: NativeSampleRing,
    placement_endpoint_step: int,
    expected_state: CubeState,
    actual_hand_pose: Pose,
    hand_native_step: int,
    target_core_pose: Pose,
    target_hand_pose: Pose,
    table_height_m: float,
    motion_evidence: SupportCaptureMotionEvidence,
) -> dict[str, object]:
    """Return JSON-safe eligibility and evidence without any side effects.

    Malformed API inputs raise TypeError/ValueError. Valid but insufficient
    evidence rejects. First failure order: timestamps, real native prefix/window,
    actual support geometry, placement, motion/contact. All diagnostics are kept.
    Target poses express placement expectations, never measured support geometry.
    """
    for value, kind, label in ((current_sample, NativeCubeSample, 'current_sample'),
                               (sample_ring, NativeSampleRing, 'sample_ring'),
                               (expected_state, CubeState, 'expected_state'),
                               (motion_evidence, SupportCaptureMotionEvidence, 'motion_evidence')):
        if not isinstance(value, kind):
            raise TypeError(f'{label} must be {kind.__name__}')
    endpoint = _nonnegative_integer(placement_endpoint_step, 'placement_endpoint_step')
    hand_step = _nonnegative_integer(hand_native_step, 'hand_native_step')
    _positive_real(sample_ring.physics_dt_s, 'physics_dt_s')
    _positive_real(sample_ring.minimum_duration_s, 'minimum_duration_s')
    table_height = _finite_real(table_height_m, 'table_height_m')
    actual_hand = _validate_pose(actual_hand_pose, 'actual_hand_pose')
    target_core = _validate_pose(target_core_pose, 'target_core_pose')
    target_hand = _validate_pose(target_hand_pose, 'target_hand_pose')
    samples = sample_ring.samples
    current_matches = bool(samples and current_sample == samples[-1])
    hand_matches = hand_step == current_sample.native_step
    timestamps = dict(current_native_step=current_sample.native_step,
                      current_native_time_s=current_sample.native_time_s,
                      ring_last_native_step=samples[-1].native_step if samples else None,
                      ring_last_native_time_s=samples[-1].native_time_s if samples else None,
                      placement_endpoint_step=endpoint, hand_native_step=hand_step,
                      current_matches_ring_last=current_matches, hand_matches_current=hand_matches)
    native = evaluate_native_prefix(sample_ring=sample_ring, after_step=endpoint,
                                    expected_state=expected_state, evaluate_window=evaluate_native_cube_window)
    support = measure_native_support_geometry(current_sample, table_height_m=table_height, include_stickers=True)
    support_ok = abs(support['table_gap_m']) <= 0.002
    row = current_sample.native_link_transforms_xyzw[current_sample.body_names.index('core')]
    actual_core = Pose(row[:3], (row[6], *row[3:6]))
    placement = evaluate_placement_evidence(actual_core_pose=actual_core, target_core_pose=target_core,
                                            actual_hand_pose=actual_hand, target_hand_pose=target_hand)
    motion = _motion_diagnostics(motion_evidence)
    reason = None
    if not current_matches:
        reason = 'support_capture_current_sample_mismatch'
    elif not hand_matches:
        reason = 'support_capture_hand_step_mismatch'
    elif not native['success']:
        reason = native['abort_reason']
    elif not support_ok:
        reason = 'support_capture_table_gap_exceeded'
    elif not placement['accepted']:
        reason = placement['abort_reason'] or 'whole_cube_placement_core_xy_error'
    elif not motion['accepted']:
        reason = motion['abort_reason']
    return _json_safe(dict(accepted=reason is None, abort_reason=reason,
                           timestamps=timestamps, native_window=native['native_observation'],
                           support_geometry=dict(support, accepted=support_ok),
                           placement=placement, motion_contact=motion))


__all__ = ['SupportCaptureMotionEvidence', 'evaluate_support_capture_gate']
