"""Bounded-memory stationarity checks for measured Rubik's Cube twist."""

from __future__ import annotations

from collections import deque
import math
from numbers import Real


_QUARTER_TURN_RAD = math.pi / 2.0
_MAX_RETAINED_SAMPLES = 4096


def _positive_finite(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a finite positive number")
    converted = float(value)
    if not math.isfinite(converted) or converted <= 0.0:
        raise ValueError(f"{name} must be a finite positive number")
    return converted


def _finite_sample(value: Real) -> float | None:
    if isinstance(value, bool) or not isinstance(value, Real):
        return None
    converted = float(value)
    return converted if math.isfinite(converted) else None


class AngularStationarityWindow:
    """Evaluate a contiguous measured-pose window near a quarter-turn detent.

    ``stable_duration_s`` is the real-time coverage of the retained candidate
    window, capped at the required duration. ``last_rate_rad_s`` describes only
    the latest valid adjacent pair and is never an acceptance condition.
    """

    def __init__(
        self,
        *,
        duration_s: float,
        max_span_rad: float,
        max_phase_error_rad: float,
        max_sample_gap_s: float,
    ) -> None:
        self._duration_s = _positive_finite(duration_s, "duration_s")
        self._max_span_rad = _positive_finite(max_span_rad, "max_span_rad")
        self._max_phase_error_rad = _positive_finite(
            max_phase_error_rad, "max_phase_error_rad"
        )
        if self._max_phase_error_rad >= math.pi / 4.0:
            raise ValueError("max_phase_error_rad must be less than pi/4")
        self._max_sample_gap_s = _positive_finite(
            max_sample_gap_s, "max_sample_gap_s"
        )
        self.reset()

    @property
    def last_rate_rad_s(self) -> float | None:
        return self._last_rate_rad_s

    @property
    def angle_span_rad(self) -> float | None:
        return self._angle_span_rad

    @property
    def max_phase_error_rad(self) -> float | None:
        return self._observed_max_phase_error_rad

    @property
    def sample_count(self) -> int:
        return len(self._samples)

    @property
    def stable_duration_s(self) -> float:
        return self._stable_duration_s

    @property
    def capacity_exceeded(self) -> bool:
        return self._capacity_exceeded

    @property
    def is_stable(self) -> bool:
        return self._is_stable

    def reset(self) -> None:
        """Start a new monitored phase with no elapsed evidence."""

        self._samples: deque[tuple[float, float, float]] = deque()
        self._previous_time_s: float | None = None
        self._previous_angle_rad: float | None = None
        self._previous_unwrapped_angle_rad: float | None = None
        self._last_rate_rad_s: float | None = None
        self._last_phase_error_rad: float | None = None
        self._angle_span_rad: float | None = None
        self._observed_max_phase_error_rad: float | None = None
        self._stable_duration_s = 0.0
        self._capacity_exceeded = False
        self._is_stable = False

    def update(self, time_s: float, angle_rad: float) -> bool:
        """Add one sample and report whether the full pose window is stable."""

        time = _finite_sample(time_s)
        angle = _finite_sample(angle_rad)
        if time is None or angle is None:
            self.reset()
            return False

        if self._capacity_exceeded:
            self._is_stable = False
            return False

        phase_error = self._phase_error_rad(angle)
        self._last_phase_error_rad = phase_error
        phase_valid = phase_error <= self._max_phase_error_rad
        if self._previous_time_s is None or self._previous_angle_rad is None:
            self._last_rate_rad_s = None
            if phase_valid:
                self._seed(time, angle, phase_error)
            else:
                self._clear_evidence()
            return False

        elapsed_s = time - self._previous_time_s
        if elapsed_s <= 0.0 or elapsed_s > self._max_sample_gap_s:
            self.reset()
            if phase_valid:
                self._seed(time, angle, phase_error)
            return False

        if self._has_unwrapped_discontinuity(angle, self._previous_angle_rad):
            self.reset()
            if phase_valid:
                self._seed(time, angle, phase_error)
            return False

        current_wrapped = math.remainder(angle, math.tau)
        previous_wrapped = math.remainder(self._previous_angle_rad, math.tau)
        wrapped_increment = math.remainder(
            current_wrapped - previous_wrapped, math.tau
        )
        rate = abs(wrapped_increment) / elapsed_s
        if not math.isfinite(rate):
            rate = None

        if rate is None or not phase_valid:
            self._clear_evidence()
            self._last_rate_rad_s = rate
            return False

        self._last_rate_rad_s = rate
        assert self._previous_unwrapped_angle_rad is not None
        unwrapped_angle = self._previous_unwrapped_angle_rad + wrapped_increment

        cutoff_time = time - self._duration_s
        while len(self._samples) >= 2 and self._samples[1][0] <= cutoff_time:
            self._samples.popleft()
        if len(self._samples) >= _MAX_RETAINED_SAMPLES:
            self._capacity_exceeded = True
            self._is_stable = False
            return False

        self._samples.append((time, unwrapped_angle, phase_error))
        self._previous_time_s = time
        self._previous_angle_rad = angle
        self._previous_unwrapped_angle_rad = unwrapped_angle
        self._refresh_window_diagnostics()
        available_duration_s = self._samples[-1][0] - self._samples[0][0]
        full_duration = available_duration_s >= self._duration_s or math.isclose(
            available_duration_s,
            self._duration_s,
            rel_tol=1e-12,
            abs_tol=1e-15,
        )
        self._stable_duration_s = min(available_duration_s, self._duration_s)
        assert self._angle_span_rad is not None
        self._is_stable = full_duration and self._angle_span_rad <= self._max_span_rad
        return self._is_stable

    def report(self) -> dict[str, object]:
        """Return compact measured-window evidence for runtime diagnostics."""

        return {
            "policy": "all_sample_unwrapped_angular_span",
            "required_duration_s": self._duration_s,
            "available_duration_s": self._stable_duration_s,
            "max_allowed_span_rad": self._max_span_rad,
            "observed_span_rad": self._angle_span_rad,
            "max_allowed_phase_error_rad": self._max_phase_error_rad,
            "max_observed_phase_error_rad": self._observed_max_phase_error_rad,
            "last_phase_error_rad": self._last_phase_error_rad,
            "max_sample_gap_s": self._max_sample_gap_s,
            "sample_count": len(self._samples),
            "last_rate_rad_s": self._last_rate_rad_s,
            "capacity_exceeded": self._capacity_exceeded,
            "pose_stationary": self._is_stable,
        }

    @staticmethod
    def _phase_error_rad(angle_rad: float) -> float:
        return abs(math.remainder(angle_rad, _QUARTER_TURN_RAD))

    @staticmethod
    def _has_unwrapped_discontinuity(
        angle_rad: float, previous_angle_rad: float
    ) -> bool:
        if angle_rad >= previous_angle_rad:
            exceeds_half_turn = angle_rad - math.pi > previous_angle_rad
        else:
            exceeds_half_turn = previous_angle_rad - math.pi > angle_rad
        if not exceeds_half_turn:
            return False
        canonical_wrap = (
            -math.pi <= angle_rad <= math.pi
            and -math.pi <= previous_angle_rad <= math.pi
        )
        return not canonical_wrap

    def _clear_evidence(self) -> None:
        self._samples.clear()
        self._previous_time_s = None
        self._previous_angle_rad = None
        self._previous_unwrapped_angle_rad = None
        self._angle_span_rad = None
        self._observed_max_phase_error_rad = None
        self._stable_duration_s = 0.0
        self._is_stable = False

    def _seed(
        self,
        time_s: float,
        angle_rad: float,
        phase_error_rad: float,
    ) -> None:
        self._samples.append((time_s, angle_rad, phase_error_rad))
        self._previous_time_s = time_s
        self._previous_angle_rad = angle_rad
        self._previous_unwrapped_angle_rad = angle_rad
        self._angle_span_rad = 0.0
        self._observed_max_phase_error_rad = phase_error_rad

    def _refresh_window_diagnostics(self) -> None:
        angles = [sample[1] for sample in self._samples]
        phase_errors = [sample[2] for sample in self._samples]
        self._angle_span_rad = max(angles) - min(angles)
        self._observed_max_phase_error_rad = max(phase_errors)
