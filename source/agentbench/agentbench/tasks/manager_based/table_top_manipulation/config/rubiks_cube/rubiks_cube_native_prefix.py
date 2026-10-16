"""Pure prefix accounting and native-window control for Rubik execution."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import json
import math
from pathlib import Path


@dataclass(frozen=True)
class UserMoveToken:
    normalized: str
    atomic_moves: tuple[str, ...]


class NativeSampleRing:
    """Bounded contiguous native samples collected by the physics callback."""

    def __init__(self, *, physics_dt_s: float, minimum_duration_s: float = 0.5):
        if physics_dt_s <= 0.0 or minimum_duration_s <= 0.0:
            raise ValueError("native sample timing must be positive")
        self.physics_dt_s = float(physics_dt_s)
        self.minimum_duration_s = float(minimum_duration_s)
        self.capacity = math.ceil(minimum_duration_s / physics_dt_s) + 1
        self._samples = deque(maxlen=self.capacity)

    @property
    def samples(self) -> tuple[object, ...]:
        return tuple(self._samples)

    def append(self, sample) -> bool:
        step = int(sample.native_step)
        if self._samples:
            previous = int(self._samples[-1].native_step)
            if step == previous:
                return False
            if step != previous + 1:
                raise RuntimeError(
                    f"native sample step gap or reversal: {previous} -> {step}"
                )
        self._samples.append(sample)
        return True

    def fresh_window(self, *, after_step: int) -> tuple[object, ...]:
        return tuple(
            sample for sample in self._samples if int(sample.native_step) > after_step
        )

    def ready(self, *, after_step: int) -> bool:
        samples = self.fresh_window(after_step=after_step)
        if len(samples) < 2:
            return False
        elapsed = (
            int(samples[-1].native_step) - int(samples[0].native_step)
        ) * self.physics_dt_s
        return elapsed + 1e-12 >= self.minimum_duration_s


def parse_user_sequence(sequence: str, *, normalize_move) -> tuple[UserMoveToken, ...]:
    """Normalize user tokens without losing double-turn completion boundaries."""

    parsed: list[UserMoveToken] = []
    for raw_token in sequence.split():
        move, is_double = normalize_move(raw_token)
        parsed.append(
            UserMoveToken(
                normalized=f"{move}2" if is_double else move,
                atomic_moves=(move, move) if is_double else (move,),
            )
        )
    if not parsed:
        raise ValueError("cube sequence cannot be empty")
    return tuple(parsed)


def user_sequence_progress(
    tokens: tuple[UserMoveToken, ...], completed_atomic_moves: int
) -> dict[str, int | list[str]]:
    if completed_atomic_moves < 0:
        raise ValueError("completed atomic move count cannot be negative")
    atom_cursor = 0
    completed_tokens = 0
    for token in tokens:
        atom_cursor += len(token.atomic_moves)
        if atom_cursor <= completed_atomic_moves:
            completed_tokens += 1
    return {
        "requested_user_tokens": len(tokens),
        "completed_user_tokens": completed_tokens,
        "remaining_user_tokens": len(tokens) - completed_tokens,
        "requested_user_token_sequence": [token.normalized for token in tokens],
        "completed_user_token_sequence": [
            token.normalized for token in tokens[:completed_tokens]
        ],
        "remaining_user_token_sequence": [
            token.normalized for token in tokens[completed_tokens:]
        ],
        "completed_atomic_moves": completed_atomic_moves,
    }


def expected_atomic_prefixes(initial_state, atomic_moves) -> tuple[object, ...]:
    prefixes = [initial_state]
    for move in atomic_moves:
        prefixes.append(prefixes[-1].apply_move(move))
    return tuple(prefixes)


def _native_prefix_decision(measured_state, diagnostics, expected_state) -> str:
    if measured_state is None:
        return "native_state_unknown"
    if measured_state != expected_state:
        return "native_state_mismatch"
    if not bool(diagnostics.get("stable", False)):
        return "native_window_unstable"
    return "accepted"


def _native_observation_bounds(
    sample_ring: NativeSampleRing, *, after_step: int, status: str
) -> dict[str, object]:
    samples = sample_ring.fresh_window(after_step=after_step)
    first = samples[0] if samples else None
    last = samples[-1] if samples else None
    return {
        "status": status,
        "ready": sample_ring.ready(after_step=after_step),
        "after_native_step": int(after_step),
        "sample_count": len(samples),
        "first_native_step": int(first.native_step) if first is not None else None,
        "last_native_step": int(last.native_step) if last is not None else None,
        "first_native_time_s": float(first.native_time_s) if first is not None else None,
        "last_native_time_s": float(last.native_time_s) if last is not None else None,
    }


def _native_observation(
    sample_ring: NativeSampleRing,
    *,
    after_step: int,
    measured_state,
    diagnostics,
) -> dict[str, object]:
    if measured_state is None:
        status = "unknown"
    elif not bool(diagnostics.get("stable", False)):
        status = "unstable"
    else:
        status = "valid"
    return {
        **_native_observation_bounds(
            sample_ring, after_step=after_step, status=status
        ),
        **diagnostics,
        "status": status,
    }


def evaluate_native_prefix(
    *, sample_ring: NativeSampleRing, after_step: int, expected_state, evaluate_window
) -> dict[str, object]:
    if not sample_ring.ready(after_step=after_step):
        return {
            "success": False,
            "abort_reason": "native_window_not_ready",
            "measured_state": None,
            "native_observation": _native_observation_bounds(
                sample_ring, after_step=after_step, status="not_ready"
            ),
        }
    samples = sample_ring.fresh_window(after_step=after_step)
    try:
        measured_state, diagnostics = evaluate_window(
            samples,
            physics_dt_s=sample_ring.physics_dt_s,
            after_step=after_step,
        )
    except (TypeError, ValueError, RuntimeError) as error:
        observation = _native_observation_bounds(
            sample_ring, after_step=after_step, status="invalid"
        )
        observation["evaluation_error"] = f"{type(error).__name__}:{error}"
        return {
            "success": False,
            "abort_reason": f"native_window_invalid:{type(error).__name__}:{error}",
            "measured_state": None,
            "native_observation": observation,
        }
    decision = _native_prefix_decision(measured_state, diagnostics, expected_state)
    return {
        "success": decision == "accepted",
        "abort_reason": None if decision == "accepted" else decision,
        "measured_state": measured_state,
        "native_observation": _native_observation(
            sample_ring,
            after_step=after_step,
            measured_state=measured_state,
            diagnostics=diagnostics,
        ),
    }


def evaluate_initial_native_prefix(
    *, sample_ring: NativeSampleRing, after_step: int, evaluate_window
) -> dict[str, object]:
    if not sample_ring.ready(after_step=after_step):
        return {
            "success": False,
            "abort_reason": "initial_native_window_not_ready",
            "measured_state": None,
            "native_observation": _native_observation_bounds(
                sample_ring, after_step=after_step, status="not_ready"
            ),
        }
    try:
        measured_state, diagnostics = evaluate_window(
            sample_ring.fresh_window(after_step=after_step),
            physics_dt_s=sample_ring.physics_dt_s,
            after_step=after_step,
        )
    except (TypeError, ValueError, RuntimeError) as error:
        observation = _native_observation_bounds(
            sample_ring, after_step=after_step, status="invalid"
        )
        observation["evaluation_error"] = f"{type(error).__name__}:{error}"
        return {
            "success": False,
            "abort_reason": f"initial_native_window_invalid:{type(error).__name__}:{error}",
            "measured_state": None,
            "native_observation": observation,
        }
    if measured_state is None:
        abort_reason = "initial_native_state_unknown"
    elif not bool(diagnostics.get("stable", False)):
        abort_reason = "initial_native_window_unstable"
    else:
        abort_reason = None
    return {
        "success": abort_reason is None,
        "abort_reason": abort_reason,
        "measured_state": measured_state,
        "native_observation": _native_observation(
            sample_ring,
            after_step=after_step,
            measured_state=measured_state,
            diagnostics=diagnostics,
        ),
    }


def run_bounded_native_settle(
    *,
    max_control_steps: int,
    sample_ring: NativeSampleRing,
    after_step: int,
    expected_state,
    control_step,
    evaluate_window,
) -> dict[str, object]:
    """Hold one caller-provided target until a fresh exact prefix is stable."""

    if max_control_steps < 1:
        raise ValueError("native settle maximum must be positive")
    last_evaluation_step = None
    last_result = None
    evaluation_interval_steps = math.ceil(
        sample_ring.minimum_duration_s / sample_ring.physics_dt_s
    )
    for control_index in range(1, max_control_steps + 1):
        if control_step() is False:
            return {
                "success": False,
                "abort_reason": "native_settle_control_failed",
                "measured_state": None,
                "native_observation": None,
                "control_steps_executed": control_index,
            }
        if not sample_ring.ready(after_step=after_step):
            continue
        final_step = int(sample_ring.samples[-1].native_step)
        if (
            last_evaluation_step is not None
            and final_step - last_evaluation_step < evaluation_interval_steps
        ):
            continue
        last_result = evaluate_native_prefix(
            sample_ring=sample_ring,
            after_step=after_step,
            expected_state=expected_state,
            evaluate_window=evaluate_window,
        )
        last_evaluation_step = final_step
        last_result["control_steps_executed"] = control_index
        if last_result["success"]:
            return last_result
        if last_result["abort_reason"] == "native_state_mismatch" or str(
            last_result["abort_reason"]
        ).startswith("native_window_invalid:"):
            return last_result
    if last_result is None:
        return {
            "success": False,
            "abort_reason": "native_settle_window_not_ready",
            "measured_state": None,
            "native_observation": _native_observation_bounds(
                sample_ring, after_step=after_step, status="not_ready"
            ),
            "control_steps_executed": max_control_steps,
        }
    last_result["success"] = False
    last_result["abort_reason"] = (
        f"native_settle_timeout:{last_result['abort_reason']}"
    )
    last_result["control_steps_executed"] = max_control_steps
    return last_result


def final_native_acceptance(
    *,
    measured_state,
    expected_state,
    completed_user_tokens: int,
    requested_user_tokens: int,
    initial_core_pose,
    final_core_pose,
) -> dict[str, float | bool]:
    initial_position, initial_quaternion = initial_core_pose
    final_position, final_quaternion = final_core_pose
    position_error = math.sqrt(
        sum(
            (final - initial) ** 2
            for initial, final in zip(
                initial_position, final_position, strict=True
            )
        )
    )
    orientation_error = quaternion_distance_rad(
        initial_quaternion, final_quaternion
    )
    return {
        "success": (
            measured_state == expected_state
            and completed_user_tokens == requested_user_tokens
            and position_error <= 0.005
            and orientation_error <= math.radians(2.0)
        ),
        "core_position_error_m": position_error,
        "core_orientation_error_rad": orientation_error,
    }


def quaternion_distance_rad(first_wxyz, second_wxyz) -> float:
    dot = abs(
        sum(
            first * second
            for first, second in zip(first_wxyz, second_wxyz, strict=True)
        )
    )
    return 2.0 * math.acos(max(-1.0, min(1.0, dot)))


def action_evidence_path(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    return resolved.with_name(f"{resolved.stem}.actions.jsonl")


def append_action_evidence(path: Path | None, payload: dict) -> None:
    if path is None:
        return
    evidence_path = action_evidence_path(path)
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    with evidence_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True) + "\n")


__all__ = [
    "NativeSampleRing",
    "UserMoveToken",
    "action_evidence_path",
    "append_action_evidence",
    "evaluate_initial_native_prefix",
    "evaluate_native_prefix",
    "expected_atomic_prefixes",
    "final_native_acceptance",
    "parse_user_sequence",
    "run_bounded_native_settle",
    "user_sequence_progress",
]
