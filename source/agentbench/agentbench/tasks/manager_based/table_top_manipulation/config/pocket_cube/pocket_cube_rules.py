"""Discrete 2x2 state and rules for the switchable single-carrier mechanism."""

from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Mapping, Sequence


FACE_NAMES = ("U", "D", "F", "B", "R", "L")
FACE_JOINT_NAMES = tuple(f"face_{face.lower()}_joint" for face in FACE_NAMES)
OPPOSITE_FACE = {"U": "D", "D": "U", "F": "B", "B": "F", "R": "L", "L": "R"}
QUARTER_TURN = math.pi / 2.0

# Corner positions and cubie identifiers use the standard cubie-cube order.
CORNER_NAMES = ("URF", "UFL", "ULB", "UBR", "DFR", "DLF", "DBL", "DRB")

# Geometric conventions shared by the carrier hinge and cubie renderer.
# Cube-local coordinates are +x=R, +y=F, +z=U.  Positive face travel is a
# clockwise turn when looking directly at the named face.
FACE_AXES = (
    (0.0, 0.0, -1.0),  # U
    (0.0, 0.0, 1.0),   # D
    (0.0, -1.0, 0.0),  # F
    (0.0, 1.0, 0.0),   # B
    (-1.0, 0.0, 0.0),  # R
    (1.0, 0.0, 0.0),   # L
)
FACE_CORNER_POSITIONS = (
    (0, 1, 2, 3),  # U
    (4, 5, 6, 7),  # D
    (0, 1, 4, 5),  # F
    (2, 3, 6, 7),  # B
    (0, 3, 4, 7),  # R
    (1, 2, 5, 6),  # L
)

# For one clockwise face turn, ``new_position[i]`` receives the cubie that was
# at ``permutation[i]``.  Orientation deltas follow the same destination index.
_MOVE_TABLES: dict[str, tuple[tuple[int, ...], tuple[int, ...]]] = {
    "U": ((1, 2, 3, 0, 4, 5, 6, 7), (0, 0, 0, 0, 0, 0, 0, 0)),
    "D": ((0, 1, 2, 3, 7, 4, 5, 6), (0, 0, 0, 0, 0, 0, 0, 0)),
    "F": ((4, 0, 2, 3, 5, 1, 6, 7), (1, 2, 0, 0, 2, 1, 0, 0)),
    "B": ((0, 1, 6, 2, 4, 5, 7, 3), (0, 0, 1, 2, 0, 0, 2, 1)),
    "R": ((3, 1, 2, 7, 0, 5, 6, 4), (2, 0, 0, 1, 1, 0, 0, 2)),
    "L": ((0, 5, 1, 3, 4, 6, 2, 7), (0, 1, 2, 0, 0, 2, 1, 0)),
}


def _check_face(face: str) -> str:
    face = face.upper()
    if face not in FACE_NAMES:
        raise ValueError(f"Unknown pocket-cube face {face!r}; expected one of {FACE_NAMES}")
    return face


def detent_index(angle: float) -> int:
    """Return the closest quarter-turn detent index for ``angle``."""

    return int(round(float(angle) / QUARTER_TURN))


def detent_error(angle: float) -> float:
    """Signed distance in radians from ``angle`` to its nearest detent."""

    return float(angle) - detent_index(angle) * QUARTER_TURN


def is_detented(angle: float, tolerance: float) -> bool:
    return abs(detent_error(angle)) <= tolerance


@dataclass(frozen=True)
class PocketCubeState:
    """Eight-corner state of a 2x2 cube.

    ``permutation[position]`` is the cubie at that position and
    ``orientation[position]`` is its twist (0, 1, or 2).
    """

    permutation: tuple[int, ...] = tuple(range(8))
    orientation: tuple[int, ...] = (0,) * 8

    def __post_init__(self) -> None:
        if len(self.permutation) != 8 or sorted(self.permutation) != list(range(8)):
            raise ValueError("permutation must contain every corner index exactly once")
        if len(self.orientation) != 8 or any(value not in (0, 1, 2) for value in self.orientation):
            raise ValueError("orientation must contain eight values in {0, 1, 2}")
        if sum(self.orientation) % 3 != 0:
            raise ValueError("corner orientation sum must be divisible by three")

    @property
    def solved(self) -> bool:
        return self.permutation == tuple(range(8)) and self.orientation == (0,) * 8

    def turn(self, face: str, quarter_turns: int = 1) -> "PocketCubeState":
        """Return the state after signed quarter turns of ``face``."""

        face = _check_face(face)
        turns = quarter_turns % 4
        state = self
        permutation, orientation_delta = _MOVE_TABLES[face]
        for _ in range(turns):
            state = PocketCubeState(
                permutation=tuple(state.permutation[source] for source in permutation),
                orientation=tuple(
                    (state.orientation[source] + orientation_delta[destination]) % 3
                    for destination, source in enumerate(permutation)
                ),
            )
        return state

    def apply(self, moves: Sequence[tuple[str, int]]) -> "PocketCubeState":
        state = self
        for face, turns in moves:
            state = state.turn(face, turns)
        return state

    def as_vector(self) -> tuple[int, ...]:
        """Return a compact observation vector: 8 permutation + 8 twists."""

        return self.permutation + self.orientation

    @classmethod
    def from_vector(cls, values: Sequence[int]) -> "PocketCubeState":
        if len(values) != 16:
            raise ValueError("a pocket-cube state vector must contain 16 integers")
        return cls(tuple(int(value) for value in values[:8]), tuple(int(value) for value in values[8:]))


def is_pocket_cube_target_state(
    state: PocketCubeState | Sequence[int],
    target: PocketCubeState | Sequence[int],
) -> bool:
    """Deterministically compare a simulated cubie state with a target."""

    if not isinstance(state, PocketCubeState):
        state = PocketCubeState.from_vector(state)
    if not isinstance(target, PocketCubeState):
        target = PocketCubeState.from_vector(target)
    return state == target


@dataclass(frozen=True)
class InterlockConfig:
    """Angular tolerances for the physical face-joint interlock."""

    alignment_tolerance: float = math.radians(8.0)
    opposite_clearance: float = math.radians(5.0)
    locked_joint_slop: float = math.radians(2.5)
    completion_tolerance: float = math.radians(7.0)
    max_overtravel: float = math.radians(8.0)


@dataclass(frozen=True)
class RuleResult:
    valid: bool
    reason: str = ""
    face: str | None = None
    committed_turn: int = 0


def can_start_face_turn(
    joint_angles: Mapping[str, float],
    face: str,
    config: InterlockConfig = InterlockConfig(),
) -> RuleResult:
    """Check whether ``face`` may leave its current detent.

    The opposite face has the narrowest clearance requirement, mirroring the
    limited internal space of a real cube.  Every remaining face must also be
    close to a 90-degree detent so intersecting layers cannot move together.
    """

    face = _check_face(face)
    missing = [name for name in FACE_NAMES if name not in joint_angles]
    if missing:
        return RuleResult(False, f"missing face angles: {missing}", face)

    for other in FACE_NAMES:
        if other == face:
            continue
        tolerance = config.opposite_clearance if other == OPPOSITE_FACE[face] else config.alignment_tolerance
        if not is_detented(joint_angles[other], tolerance):
            relation = "opposite" if other == OPPOSITE_FACE[face] else "intersecting"
            return RuleResult(
                False,
                f"{relation} face {other} is {math.degrees(detent_error(joint_angles[other])):.2f} deg "
                f"from its nearest detent (limit {math.degrees(tolerance):.2f} deg)",
                face,
            )
    if not is_detented(joint_angles[face], config.alignment_tolerance):
        return RuleResult(False, f"requested face {face} did not start at a detent", face)
    return RuleResult(True, face=face)


@dataclass
class PocketCubeRuleMonitor:
    """Stateful validator for one physically executed quarter turn."""

    state: PocketCubeState = field(default_factory=PocketCubeState)
    config: InterlockConfig = field(default_factory=InterlockConfig)
    active_face: str | None = None
    start_angles: dict[str, float] = field(default_factory=dict)
    first_failure: RuleResult | None = None

    def begin_turn(self, face: str, joint_angles: Mapping[str, float]) -> RuleResult:
        if self.first_failure is not None:
            return self.first_failure
        if self.active_face is not None:
            return self._fail(f"face {self.active_face} is already turning", face)
        result = can_start_face_turn(joint_angles, face, self.config)
        if not result.valid:
            return self._fail(result.reason, result.face)
        self.active_face = _check_face(face)
        self.start_angles = {name: float(joint_angles[name]) for name in FACE_NAMES}
        return result

    def update(self, joint_angles: Mapping[str, float]) -> RuleResult:
        if self.first_failure is not None:
            return self.first_failure
        if self.active_face is None:
            return RuleResult(True)

        for other in FACE_NAMES:
            if other == self.active_face:
                continue
            displacement = float(joint_angles[other]) - self.start_angles[other]
            if abs(displacement) > self.config.locked_joint_slop:
                return self._fail(
                    f"locked face {other} moved {math.degrees(displacement):.2f} deg while "
                    f"{self.active_face} was active",
                    other,
                )

        active_displacement = float(joint_angles[self.active_face]) - self.start_angles[self.active_face]
        if abs(active_displacement) > QUARTER_TURN + self.config.max_overtravel:
            return self._fail(
                f"face {self.active_face} exceeded one quarter turn by "
                f"{math.degrees(abs(active_displacement) - QUARTER_TURN):.2f} deg",
                self.active_face,
            )
        return RuleResult(True, face=self.active_face)

    def end_turn(self, joint_angles: Mapping[str, float]) -> RuleResult:
        result = self.update(joint_angles)
        if not result.valid:
            return result
        if self.active_face is None:
            return self._fail("cannot end a turn when no face is active")

        face = self.active_face
        displacement = float(joint_angles[face]) - self.start_angles[face]
        quarter_turns = int(round(displacement / QUARTER_TURN))
        error = displacement - quarter_turns * QUARTER_TURN
        if abs(quarter_turns) != 1 or abs(error) > self.config.completion_tolerance:
            return self._fail(
                f"face {face} ended at {math.degrees(displacement):.2f} deg; expected one complete quarter turn",
                face,
            )

        self.state = self.state.turn(face, quarter_turns)
        self.active_face = None
        self.start_angles.clear()
        return RuleResult(True, face=face, committed_turn=quarter_turns)

    def _fail(self, reason: str, face: str | None = None) -> RuleResult:
        if self.first_failure is None:
            self.first_failure = RuleResult(False, reason, face)
        return self.first_failure

    def reset(self, state: PocketCubeState | None = None) -> None:
        self.state = PocketCubeState() if state is None else state
        self.active_face = None
        self.start_angles.clear()
        self.first_failure = None
