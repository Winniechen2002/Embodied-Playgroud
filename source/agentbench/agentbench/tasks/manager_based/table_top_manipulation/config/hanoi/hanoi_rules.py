"""Deterministic rule checks for the Tower-of-Hanoi task.

The functions in this module are intentionally Isaac-free.  They consume ring
poses from simulation and classify whether the Hanoi state obeys the hard task
rules used by evaluation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence


TABLE_TOP_Z = 0.60
BOARD_HEIGHT = 0.025
RING_HEIGHT = 0.035
RING_Z_GAP = 0.0
RING_BASE_Z = TABLE_TOP_Z + BOARD_HEIGHT + RING_HEIGHT * 0.5
TABLE_SIZE = (1.0, 1.5, 0.5)
TABLE_CENTER = (0.5, 0.0, 0.35)
BOARD_SIZE = (0.58, 0.88, BOARD_HEIGHT)
BOARD_CENTER = (0.71, 0.0, TABLE_TOP_Z + BOARD_HEIGHT * 0.5)
PEG_X = 0.67
PEG_YS = {"left": -0.32, "middle": 0.0, "right": 0.32}
PEG_RADIUS = 0.016
PEG_HEIGHT = 0.20
PEG_CLEARANCE = 0.022
RING_INNER_RADIUS = PEG_RADIUS + PEG_CLEARANCE
RING_LEVEL_STEP = RING_HEIGHT + RING_Z_GAP
RING_MASS = 0.03
RING_CONTACT_OFFSET = 0.001
RING_REST_OFFSET = 0.0
PEG_CONTACT_OFFSET = 0.001
PEG_REST_OFFSET = 0.0

RING_PHYSICS_MATERIAL = {
    "static_friction": 1.6,
    "dynamic_friction": 1.2,
    "restitution": 0.0,
    "friction_combine_mode": "average",
    "restitution_combine_mode": "min",
}
PEG_PHYSICS_MATERIAL = {
    "static_friction": 0.005,
    "dynamic_friction": 0.002,
    "restitution": 0.0,
    "friction_combine_mode": "average",
    "restitution_combine_mode": "min",
}
SURFACE_PHYSICS_MATERIAL = {
    "static_friction": 0.8,
    "dynamic_friction": 0.6,
    "restitution": 0.0,
    "friction_combine_mode": "average",
    "restitution_combine_mode": "min",
}

# A ring remains on-peg while the peg center is inside its nominal inner
# opening. Contact-solver offsets can place a resting ring at this boundary.
DEFAULT_SEATED_XY_TOLERANCE = PEG_CLEARANCE
DEFAULT_SEATED_Z_TOLERANCE = 0.016
DEFAULT_RECOVERABLE_XY_TOLERANCE = 0.12
DEFAULT_WORKSPACE_X_MARGIN = 0.65
DEFAULT_WORKSPACE_Y_MARGIN = 0.45
DEFAULT_MIN_Z = TABLE_TOP_Z - 0.08
DEFAULT_MAX_Z = TABLE_TOP_Z + BOARD_HEIGHT + PEG_HEIGHT + 0.75

RING_SPECS = {
    "xlarge": {"asset_name": "ring_xlarge", "outer_radius": 0.102},
    "large": {"asset_name": "ring_large", "outer_radius": 0.091},
    "medium": {"asset_name": "ring_medium", "outer_radius": 0.080},
    "small": {"asset_name": "ring_small", "outer_radius": 0.069},
    "xsmall": {"asset_name": "ring_xsmall", "outer_radius": 0.058},
}
RINGS_BOTTOM_TO_TOP = ["xlarge", "large", "medium", "small", "xsmall"]
ASSET_TO_RING = {spec["asset_name"]: ring for ring, spec in RING_SPECS.items()}
PEG_NAMES = ("left", "middle", "right")


@dataclass(frozen=True)
class HanoiRuleConfig:
    seated_xy_tolerance: float = DEFAULT_SEATED_XY_TOLERANCE
    seated_z_tolerance: float = DEFAULT_SEATED_Z_TOLERANCE
    recoverable_xy_tolerance: float = DEFAULT_RECOVERABLE_XY_TOLERANCE
    workspace_x_margin: float = DEFAULT_WORKSPACE_X_MARGIN
    workspace_y_margin: float = DEFAULT_WORKSPACE_Y_MARGIN
    min_z: float = DEFAULT_MIN_Z
    max_z: float = DEFAULT_MAX_Z


@dataclass(frozen=True)
class RingState:
    ring: str
    asset_name: str
    pos: tuple[float, float, float]
    status: str
    peg: str | None
    level: int | None
    xy_error: float | None
    z_error: float | None
    reason: str | None = None

    def to_dict(self) -> dict:
        return {
            "ring": self.ring,
            "asset_name": self.asset_name,
            "pos": self.pos,
            "status": self.status,
            "peg": self.peg,
            "level": self.level,
            "xy_error": self.xy_error,
            "z_error": self.z_error,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class HanoiState:
    rings: dict[str, RingState]
    stacks: dict[str, list[str]]
    violations: list[dict]

    @property
    def unseated_rings(self) -> list[str]:
        return [ring for ring, state in self.rings.items() if state.status == "unseated"]

    @property
    def unrecoverable_rings(self) -> list[str]:
        return [ring for ring, state in self.rings.items() if state.status == "unrecoverable"]

    def to_dict(self) -> dict:
        return {
            "rings": {ring: state.to_dict() for ring, state in self.rings.items()},
            "stacks": self.stacks,
            "violations": list(self.violations),
        }


@dataclass(frozen=True)
class ActiveMove:
    ring: str
    source_peg: str | None = None
    target_peg: str | None = None


@dataclass(frozen=True)
class RuleResult:
    status: str
    reason: str | None
    violating_ring: str | None
    state_snapshot: dict

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "reason": self.reason,
            "violating_ring": self.violating_ring,
            "state_snapshot": self.state_snapshot,
        }


def canonical_ring_name(name: str) -> str:
    if name in RING_SPECS:
        return name
    if name in ASSET_TO_RING:
        return ASSET_TO_RING[name]
    raise KeyError(f"Unknown Hanoi ring name: {name}")


def normalize_active_move(active_move: ActiveMove | Mapping | tuple | None) -> ActiveMove | None:
    if active_move is None:
        return None
    if isinstance(active_move, ActiveMove):
        return ActiveMove(canonical_ring_name(active_move.ring), active_move.source_peg, active_move.target_peg)
    if isinstance(active_move, Mapping):
        ring = active_move.get("ring") or active_move.get("asset_name")
        if ring is None:
            raise KeyError("active_move must include 'ring' or 'asset_name'.")
        return ActiveMove(canonical_ring_name(str(ring)), active_move.get("source_peg"), active_move.get("target_peg"))
    if isinstance(active_move, tuple):
        if len(active_move) == 3:
            ring, source_peg, target_peg = active_move
            return ActiveMove(canonical_ring_name(str(ring)), str(source_peg), str(target_peg))
        if len(active_move) == 2:
            ring, target_peg = active_move
            return ActiveMove(canonical_ring_name(str(ring)), None, str(target_peg))
    raise TypeError(f"Unsupported active_move type: {type(active_move).__name__}")


def expected_hanoi_environment_fingerprint() -> dict:
    return {
        "table_top_z": TABLE_TOP_Z,
        "board_height": BOARD_HEIGHT,
        "ring_height": RING_HEIGHT,
        "ring_z_gap": RING_Z_GAP,
        "table_size": TABLE_SIZE,
        "table_center": TABLE_CENTER,
        "board_size": BOARD_SIZE,
        "board_center": BOARD_CENTER,
        "peg_x": PEG_X,
        "peg_ys": dict(PEG_YS),
        "peg_radius": PEG_RADIUS,
        "peg_height": PEG_HEIGHT,
        "ring_inner_radius": RING_INNER_RADIUS,
        "ring_mass": RING_MASS,
        "ring_contact_offset": RING_CONTACT_OFFSET,
        "ring_rest_offset": RING_REST_OFFSET,
        "peg_contact_offset": PEG_CONTACT_OFFSET,
        "peg_rest_offset": PEG_REST_OFFSET,
        "ring_physics_material": dict(RING_PHYSICS_MATERIAL),
        "peg_physics_material": dict(PEG_PHYSICS_MATERIAL),
        "surface_physics_material": dict(SURFACE_PHYSICS_MATERIAL),
        "rings": {ring: dict(spec) for ring, spec in RING_SPECS.items()},
    }


def normalize_ring_positions(
    ring_positions: Mapping[str, Sequence[float]],
) -> dict[str, tuple[float, float, float]]:
    normalized = {}
    for name, pos in ring_positions.items():
        ring = canonical_ring_name(str(name))
        if len(pos) < 3:
            raise ValueError(f"Ring position for {name} must have at least 3 values.")
        normalized[ring] = (float(pos[0]), float(pos[1]), float(pos[2]))
    return normalized


def nearest_peg(pos_xy: tuple[float, float]) -> tuple[str, float]:
    best_peg = min(PEG_YS, key=lambda peg: math.hypot(pos_xy[0] - PEG_X, pos_xy[1] - PEG_YS[peg]))
    distance = math.hypot(pos_xy[0] - PEG_X, pos_xy[1] - PEG_YS[best_peg])
    return best_peg, distance


def expected_level_z(level: int) -> float:
    return RING_BASE_Z + level * RING_LEVEL_STEP


def classify_hanoi_state(
    ring_positions: Mapping[str, Sequence[float]],
    *,
    config: HanoiRuleConfig | None = None,
) -> HanoiState:
    cfg = config or HanoiRuleConfig()
    normalized = normalize_ring_positions(ring_positions)
    rings: dict[str, RingState] = {}
    violations: list[dict] = []
    stacks_by_level: dict[str, list[tuple[int, str]]] = {peg: [] for peg in PEG_NAMES}

    for ring in RINGS_BOTTOM_TO_TOP:
        asset_name = str(RING_SPECS[ring]["asset_name"])
        pos = normalized.get(ring)
        if pos is None:
            state = RingState(ring, asset_name, (math.nan, math.nan, math.nan), "unrecoverable", None, None, None, None, "missing_ring_pose")
            rings[ring] = state
            violations.append({"type": "missing_ring_pose", "ring": ring})
            continue
        if any(not math.isfinite(value) for value in pos):
            state = RingState(ring, asset_name, pos, "unrecoverable", None, None, None, None, "non_finite_pose")
            rings[ring] = state
            violations.append({"type": "non_finite_pose", "ring": ring, "pos": pos})
            continue

        peg, xy_error = nearest_peg((pos[0], pos[1]))
        outside_workspace = (
            abs(pos[0] - PEG_X) > cfg.workspace_x_margin
            or pos[1] < min(PEG_YS.values()) - cfg.workspace_y_margin
            or pos[1] > max(PEG_YS.values()) + cfg.workspace_y_margin
            or pos[2] < cfg.min_z
            or pos[2] > cfg.max_z
        )
        if outside_workspace:
            state = RingState(ring, asset_name, pos, "unrecoverable", peg, None, xy_error, None, "outside_recoverable_workspace")
            rings[ring] = state
            violations.append({"type": "unrecoverable_pose", "ring": ring, "pos": pos, "nearest_peg": peg})
            continue

        raw_level = (pos[2] - RING_BASE_Z) / RING_LEVEL_STEP
        level = int(round(raw_level))
        z_error = abs(pos[2] - expected_level_z(level)) if 0 <= level < len(RINGS_BOTTOM_TO_TOP) else None
        seated = (
            xy_error <= cfg.seated_xy_tolerance
            and z_error is not None
            and z_error <= cfg.seated_z_tolerance
        )
        if seated:
            state = RingState(ring, asset_name, pos, "seated", peg, level, xy_error, z_error)
            stacks_by_level[peg].append((level, ring))
        else:
            reason = "not_centered_on_peg" if xy_error > cfg.seated_xy_tolerance else "not_at_valid_stack_height"
            if xy_error > cfg.recoverable_xy_tolerance:
                reason = "off_peg_but_recoverable"
            state = RingState(ring, asset_name, pos, "unseated", peg, level if z_error is not None else None, xy_error, z_error, reason)
        rings[ring] = state

    stacks: dict[str, list[str]] = {}
    for peg, items in stacks_by_level.items():
        sorted_items = sorted(items, key=lambda item: item[0])
        stacks[peg] = [ring for _, ring in sorted_items]
        levels = [level for level, _ in sorted_items]
        if len(levels) != len(set(levels)):
            violations.append({"type": "duplicate_stack_level", "peg": peg, "levels": levels})
        if levels and levels != list(range(len(levels))):
            violations.append({"type": "non_contiguous_stack_levels", "peg": peg, "levels": levels})
        for lower, upper in zip(stacks[peg], stacks[peg][1:]):
            lower_radius = float(RING_SPECS[lower]["outer_radius"])
            upper_radius = float(RING_SPECS[upper]["outer_radius"])
            if lower_radius <= upper_radius:
                violations.append({"type": "larger_on_smaller", "peg": peg, "lower": lower, "upper": upper})

    return HanoiState(rings=rings, stacks=stacks, violations=violations)


def _first_fail(reason: str, state: HanoiState, violating_ring: str | None = None) -> RuleResult:
    return RuleResult("fail", reason, violating_ring, state.to_dict())


def _top_ring_on_peg(state: HanoiState, peg: str) -> str | None:
    stack = state.stacks.get(peg, [])
    return stack[-1] if stack else None


def _stack_violations_from_items(stacks_by_level: Mapping[str, Sequence[tuple[int, str]]]) -> list[dict]:
    violations: list[dict] = []
    for peg, items in stacks_by_level.items():
        sorted_items = sorted(items, key=lambda item: item[0])
        stack = [ring for _, ring in sorted_items]
        levels = [level for level, _ in sorted_items]
        if len(levels) != len(set(levels)):
            violations.append({"type": "duplicate_stack_level", "peg": peg, "levels": levels})
        if levels and levels != list(range(len(levels))):
            violations.append({"type": "non_contiguous_stack_levels", "peg": peg, "levels": levels})
        for lower, upper in zip(stack, stack[1:]):
            lower_radius = float(RING_SPECS[lower]["outer_radius"])
            upper_radius = float(RING_SPECS[upper]["outer_radius"])
            if lower_radius <= upper_radius:
                violations.append({"type": "larger_on_smaller", "peg": peg, "lower": lower, "upper": upper})
    return violations


def _stack_items_from_state(state: HanoiState, *, exclude_ring: str | None = None) -> dict[str, list[tuple[int, str]]]:
    stacks_by_level: dict[str, list[tuple[int, str]]] = {peg: [] for peg in PEG_NAMES}
    for ring, ring_state in state.rings.items():
        if ring == exclude_ring or ring_state.status != "seated":
            continue
        assert ring_state.peg is not None
        assert ring_state.level is not None
        stacks_by_level[ring_state.peg].append((ring_state.level, ring))
    return stacks_by_level


def _transition_stack_violations(state: HanoiState, move: ActiveMove | None) -> list[dict]:
    if move is None:
        return list(state.violations)

    active_state = state.rings[move.ring]
    non_active_items = _stack_items_from_state(state, exclude_ring=move.ring)
    non_active_violations = _stack_violations_from_items(non_active_items)

    # While the gripper is carrying the active ring it may pass over a peg at a
    # height that numerically matches a high stack level.  That is not a static
    # Hanoi stack yet.  The active ring becomes part of stack legality as soon
    # as it is seated at the next contiguous level on a peg.
    active_participates_in_stack = False
    if active_state.status == "seated" and active_state.peg is not None and active_state.level is not None:
        active_participates_in_stack = active_state.level == len(non_active_items[active_state.peg])

    if not active_participates_in_stack:
        return non_active_violations
    return list(state.violations)


def validate_hanoi_transition(
    prev_state: HanoiState,
    curr_state: HanoiState,
    active_move: ActiveMove | Mapping | tuple | None = None,
) -> RuleResult:
    move = normalize_active_move(active_move)

    for ring in curr_state.unrecoverable_rings:
        return _first_fail("unrecoverable_ring_pose", curr_state, ring)

    curr_unseated = set(curr_state.unseated_rings)
    if len(curr_unseated) > 1:
        return _first_fail("multiple_rings_left_pegs", curr_state, sorted(curr_unseated)[0])
    if curr_unseated and move is None:
        return _first_fail("ring_left_peg_without_active_move", curr_state, next(iter(curr_unseated)))
    if move is not None and curr_unseated - {move.ring}:
        return _first_fail("non_active_ring_left_peg", curr_state, sorted(curr_unseated - {move.ring})[0])

    for ring, prev_ring_state in prev_state.rings.items():
        curr_ring_state = curr_state.rings[ring]
        if move is not None and ring == move.ring:
            continue
        if prev_ring_state.status == "seated" and curr_ring_state.status != "seated":
            return _first_fail("non_active_ring_left_peg", curr_state, ring)
        if (
            prev_ring_state.status == "seated"
            and curr_ring_state.status == "seated"
            and prev_ring_state.peg != curr_ring_state.peg
        ):
            return _first_fail("non_active_ring_changed_peg", curr_state, ring)

    if move is not None:
        prev_active = prev_state.rings[move.ring]
        curr_active = curr_state.rings[move.ring]
        if curr_active.status == "unseated" and prev_active.status == "seated":
            top_ring = _top_ring_on_peg(prev_state, prev_active.peg or "")
            if top_ring != move.ring:
                return _first_fail("non_top_ring_left_peg", curr_state, move.ring)
        if curr_active.status == "seated" and move.target_peg is not None and curr_active.peg not in {prev_active.peg, move.target_peg}:
            return _first_fail("active_ring_seated_on_wrong_peg", curr_state, move.ring)

    stack_violations = _transition_stack_violations(curr_state, move)
    if stack_violations:
        violation = stack_violations[0]
        return _first_fail(str(violation["type"]), curr_state, violation.get("ring") or violation.get("upper"))

    return RuleResult("running", None, None, curr_state.to_dict())


def normalize_target_state(target_state: Mapping[str, Sequence[str]]) -> dict[str, list[str]]:
    normalized: dict[str, list[str]] = {peg: [] for peg in PEG_NAMES}
    for peg, stack in target_state.items():
        if peg not in normalized:
            raise KeyError(f"Unknown target peg: {peg}")
        normalized[peg] = [canonical_ring_name(str(ring)) for ring in stack]
    return normalized


def is_hanoi_target_state(
    sim_state: HanoiState | Mapping[str, Sequence[float]],
    target_state: Mapping[str, Sequence[str]],
    *,
    config: HanoiRuleConfig | None = None,
) -> bool:
    state = sim_state if isinstance(sim_state, HanoiState) else classify_hanoi_state(sim_state, config=config)
    if state.violations or state.unseated_rings or state.unrecoverable_rings:
        return False
    return state.stacks == normalize_target_state(target_state)


class HanoiRuleMonitor:
    def __init__(
        self,
        initial_ring_positions: Mapping[str, Sequence[float]],
        *,
        target_state: Mapping[str, Sequence[str]] | None = None,
        environment_fingerprint: Mapping | None = None,
        config: HanoiRuleConfig | None = None,
    ) -> None:
        self.config = config or HanoiRuleConfig()
        self.target_state = normalize_target_state(target_state) if target_state is not None else None
        self.environment_fingerprint = dict(environment_fingerprint or expected_hanoi_environment_fingerprint())
        self.prev_state = classify_hanoi_state(initial_ring_positions, config=self.config)
        self.active_move: ActiveMove | None = None
        self.status = "running"
        self.reason: str | None = None
        self.violating_ring: str | None = None
        if self.prev_state.violations or self.prev_state.unseated_rings or self.prev_state.unrecoverable_rings:
            violation = self.prev_state.violations[0] if self.prev_state.violations else {"type": "invalid_initial_hanoi_state"}
            self._set_fail(str(violation["type"]), violation.get("ring"))

    def _set_fail(self, reason: str, violating_ring: str | None = None) -> RuleResult:
        self.status = "fail"
        self.reason = reason
        self.violating_ring = violating_ring
        return RuleResult("fail", reason, violating_ring, self.prev_state.to_dict())

    def begin_move(self, active_move: ActiveMove | Mapping | tuple) -> RuleResult:
        if self.status == "fail":
            return self.result()
        self.active_move = normalize_active_move(active_move)
        assert self.active_move is not None
        active_state = self.prev_state.rings[self.active_move.ring]
        if active_state.status != "seated":
            return self._set_fail("active_ring_not_seated_before_move", self.active_move.ring)
        if self.active_move.source_peg is not None and active_state.peg != self.active_move.source_peg:
            return self._set_fail("active_ring_not_on_declared_source_peg", self.active_move.ring)
        if _top_ring_on_peg(self.prev_state, active_state.peg or "") != self.active_move.ring:
            return self._set_fail("active_move_not_top_ring", self.active_move.ring)
        return self.result()

    def end_move(self) -> RuleResult:
        if self.status == "fail":
            return self.result()
        if self.active_move is not None:
            active_state = self.prev_state.rings[self.active_move.ring]
            if self.prev_state.violations:
                violation = self.prev_state.violations[0]
                result = self._set_fail(str(violation["type"]), violation.get("ring") or violation.get("upper"))
            elif active_state.status != "seated":
                result = self._set_fail("active_ring_not_seated_after_move", self.active_move.ring)
            elif self.active_move.target_peg is not None and active_state.peg != self.active_move.target_peg:
                result = self._set_fail("active_ring_not_on_target_after_move", self.active_move.ring)
            else:
                result = self.result()
            self.active_move = None
            return result
        return self.result()

    def update(
        self,
        ring_positions: Mapping[str, Sequence[float]],
        *,
        active_move: ActiveMove | Mapping | tuple | None = None,
        environment_fingerprint: Mapping | None = None,
    ) -> RuleResult:
        if self.status == "fail":
            return self.result()
        if environment_fingerprint is not None and dict(environment_fingerprint) != self.environment_fingerprint:
            return self._set_fail("environment_fingerprint_changed")
        curr_state = classify_hanoi_state(ring_positions, config=self.config)
        result = validate_hanoi_transition(self.prev_state, curr_state, active_move or self.active_move)
        self.prev_state = curr_state
        if result.status == "fail":
            self.status = "fail"
            self.reason = result.reason
            self.violating_ring = result.violating_ring
            return result
        if self.target_state is not None and is_hanoi_target_state(curr_state, self.target_state, config=self.config):
            self.status = "success"
            return RuleResult("success", None, None, curr_state.to_dict())
        return result

    def result(self) -> RuleResult:
        return RuleResult(self.status, self.reason, self.violating_ring, self.prev_state.to_dict())
