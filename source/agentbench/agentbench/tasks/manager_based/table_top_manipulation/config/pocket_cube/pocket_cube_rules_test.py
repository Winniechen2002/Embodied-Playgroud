"""Unit tests for the pocket-cube cubie model and physical interlock."""

import math

import pytest

try:
    from .pocket_cube_rules import (
        CORNER_NAMES,
        FACE_AXES,
        FACE_CORNER_POSITIONS,
        FACE_NAMES,
        PocketCubeRuleMonitor,
        PocketCubeState,
        _MOVE_TABLES,
        can_start_face_turn,
        is_pocket_cube_target_state,
    )
except ImportError:  # Allow standalone pytest without importing Isaac Lab.
    from pocket_cube_rules import (  # type: ignore[no-redef]
        CORNER_NAMES,
        FACE_AXES,
        FACE_CORNER_POSITIONS,
        FACE_NAMES,
        PocketCubeRuleMonitor,
        PocketCubeState,
        _MOVE_TABLES,
        can_start_face_turn,
        is_pocket_cube_target_state,
    )


def _angles(**overrides):
    values = {face: 0.0 for face in FACE_NAMES}
    values.update(overrides)
    return values


@pytest.mark.parametrize("face", FACE_NAMES)
def test_four_quarter_turns_are_identity(face):
    solved = PocketCubeState()
    assert solved.turn(face, 4) == solved


@pytest.mark.parametrize("face", FACE_NAMES)
def test_move_and_inverse_are_identity(face):
    solved = PocketCubeState()
    assert solved.turn(face, 1).turn(face, -1) == solved


@pytest.mark.parametrize("face_index,face", list(enumerate(FACE_NAMES)))
def test_move_table_matches_physical_axis_and_layer(face_index, face):
    """The discrete permutation must match the switchable carrier axis."""

    coordinates = []
    for name in CORNER_NAMES:
        coordinates.append(
            (
                1 if "R" in name else -1,
                1 if "F" in name else -1,
                1 if "U" in name else -1,
            )
        )
    axis = FACE_AXES[face_index]

    def rotate_quarter(vector):
        # Rodrigues at +90 degrees: v' = a x v + a(a dot v).
        ax, ay, az = axis
        x, y, z = vector
        dot = ax * x + ay * y + az * z
        return (
            int(round(ay * z - az * y + ax * dot)),
            int(round(az * x - ax * z + ay * dot)),
            int(round(ax * y - ay * x + az * dot)),
        )

    source, _ = _MOVE_TABLES[face]
    moved_positions = set(FACE_CORNER_POSITIONS[face_index])
    for destination, source_position in enumerate(source):
        expected = (
            rotate_quarter(coordinates[source_position])
            if source_position in moved_positions
            else coordinates[source_position]
        )
        assert expected == coordinates[destination]


def test_arbitrary_sequence_and_exact_inverse_restore_all_corners():
    moves = (("U", 1), ("R", -1), ("F", 1), ("D", 1), ("L", -1), ("B", 1))
    inverse = tuple((face, -turns) for face, turns in reversed(moves))
    state = PocketCubeState().apply(moves)
    assert not state.solved
    assert state.apply(inverse).solved


def test_scramble_changes_permutation_and_preserves_cube_invariants():
    state = PocketCubeState().apply((("R", 1), ("U", 1), ("F", -1)))
    assert not state.solved
    assert sorted(state.permutation) == list(range(8))
    assert sum(state.orientation) % 3 == 0
    assert state.apply((("F", 1), ("U", -1), ("R", -1))).solved
    assert is_pocket_cube_target_state(state.as_vector(), state)


def test_opposite_face_has_narrower_clearance_window():
    assert can_start_face_turn(_angles(D=math.radians(4.0)), "U").valid
    result = can_start_face_turn(_angles(D=math.radians(6.0)), "U")
    assert not result.valid
    assert "opposite face D" in result.reason


def test_intersecting_face_must_be_near_detent():
    result = can_start_face_turn(_angles(F=math.radians(9.0)), "U")
    assert not result.valid
    assert "intersecting face F" in result.reason


def test_monitor_commits_only_complete_quarter_turn():
    monitor = PocketCubeRuleMonitor()
    assert monitor.begin_turn("R", _angles()).valid
    assert monitor.update(_angles(R=math.radians(45.0))).valid
    result = monitor.end_turn(_angles(R=math.radians(90.0)))
    assert result.valid and result.committed_turn == 1
    assert monitor.state == PocketCubeState().turn("R", 1)


def test_monitor_rejects_motion_of_locked_face_and_preserves_first_failure():
    monitor = PocketCubeRuleMonitor()
    assert monitor.begin_turn("F", _angles()).valid
    failure = monitor.update(_angles(F=0.4, R=math.radians(3.0)))
    assert not failure.valid
    assert "locked face R moved" in failure.reason
    assert monitor.end_turn(_angles(F=math.pi / 2)).reason == failure.reason


def test_incomplete_turn_is_not_committed():
    monitor = PocketCubeRuleMonitor()
    assert monitor.begin_turn("L", _angles()).valid
    result = monitor.end_turn(_angles(L=math.radians(70.0)))
    assert not result.valid
    assert monitor.state.solved
