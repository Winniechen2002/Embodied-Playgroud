import copy
import importlib.util
from pathlib import Path
import sys
import unittest

RULES_PATH = Path(__file__).with_name("hanoi_rules.py")
SPEC = importlib.util.spec_from_file_location("hanoi_rules", RULES_PATH)
hanoi_rules = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = hanoi_rules
SPEC.loader.exec_module(hanoi_rules)

DEFAULT_SEATED_XY_TOLERANCE = hanoi_rules.DEFAULT_SEATED_XY_TOLERANCE
DEFAULT_SEATED_Z_TOLERANCE = hanoi_rules.DEFAULT_SEATED_Z_TOLERANCE
PEG_X = hanoi_rules.PEG_X
PEG_YS = hanoi_rules.PEG_YS
PEG_CLEARANCE = hanoi_rules.PEG_CLEARANCE
RING_BASE_Z = hanoi_rules.RING_BASE_Z
RING_LEVEL_STEP = hanoi_rules.RING_LEVEL_STEP
RING_SPECS = hanoi_rules.RING_SPECS
ActiveMove = hanoi_rules.ActiveMove
HanoiRuleMonitor = hanoi_rules.HanoiRuleMonitor
classify_hanoi_state = hanoi_rules.classify_hanoi_state
expected_hanoi_environment_fingerprint = hanoi_rules.expected_hanoi_environment_fingerprint
is_hanoi_target_state = hanoi_rules.is_hanoi_target_state
validate_hanoi_transition = hanoi_rules.validate_hanoi_transition


RINGS_BOTTOM_TO_TOP = ["xlarge", "large", "medium", "small", "xsmall"]


def ideal_pose(peg: str, level: int) -> tuple[float, float, float]:
    return (PEG_X, PEG_YS[peg], RING_BASE_Z + level * RING_LEVEL_STEP)


def positions_from_stacks(stacks: dict[str, list[str]]) -> dict[str, tuple[float, float, float]]:
    positions = {}
    for peg, stack in stacks.items():
        for level, ring in enumerate(stack):
            positions[RING_SPECS[ring]["asset_name"]] = ideal_pose(peg, level)
    missing = set(RINGS_BOTTOM_TO_TOP) - {ring for stack in stacks.values() for ring in stack}
    if missing:
        raise AssertionError(f"Missing rings in test fixture: {sorted(missing)}")
    return positions


def all_left() -> dict[str, tuple[float, float, float]]:
    return positions_from_stacks({"left": RINGS_BOTTOM_TO_TOP, "middle": [], "right": []})


class HanoiRuleTests(unittest.TestCase):
    def test_default_seating_tolerances_preserve_geometric_separation(self):
        self.assertLessEqual(DEFAULT_SEATED_XY_TOLERANCE, PEG_CLEARANCE)
        self.assertLess(DEFAULT_SEATED_Z_TOLERANCE, 0.5 * RING_LEVEL_STEP)

    def test_contact_solver_height_jitter_remains_seated(self):
        positions = all_left()
        x, y, z = positions["ring_small"]
        positions["ring_small"] = (x, y, z + 0.008852)

        state = classify_hanoi_state(positions)

        self.assertEqual(state.rings["small"].status, "seated")

    def test_ring_orientation_is_not_part_of_state_classification(self):
        positions = {
            ring: (*position, 0.5, 0.5, 0.5, 0.5)
            for ring, position in all_left().items()
        }

        state = classify_hanoi_state(positions)

        self.assertFalse(state.unseated_rings)
        self.assertFalse(state.violations)

    def test_legal_top_ring_move_passes(self):
        prev = classify_hanoi_state(all_left())
        curr_positions = all_left()
        curr_positions["ring_xsmall"] = (PEG_X, PEG_YS["right"], RING_BASE_Z + 0.20)
        curr = classify_hanoi_state(curr_positions)

        result = validate_hanoi_transition(prev, curr, ActiveMove("xsmall", "left", "right"))

        self.assertEqual(result.status, "running")
        self.assertIsNone(result.reason)

    def test_active_ring_high_over_target_peg_is_transient(self):
        prev = classify_hanoi_state(all_left())
        curr_positions = all_left()
        curr_positions["ring_xsmall"] = ideal_pose("right", 4)
        curr = classify_hanoi_state(curr_positions)
        self.assertIn("non_contiguous_stack_levels", {violation["type"] for violation in curr.violations})

        result = validate_hanoi_transition(prev, curr, ActiveMove("xsmall", "left", "right"))

        self.assertEqual(result.status, "running")
        self.assertIsNone(result.reason)

    def test_active_ring_noncontiguous_at_move_end_fails(self):
        monitor = HanoiRuleMonitor(all_left())
        begin = monitor.begin_move(ActiveMove("xsmall", "left", "right"))
        self.assertNotEqual(begin.status, "fail")
        curr_positions = all_left()
        curr_positions["ring_xsmall"] = ideal_pose("right", 4)

        update = monitor.update(curr_positions)
        end = monitor.end_move()

        self.assertEqual(update.status, "running")
        self.assertEqual(end.status, "fail")
        self.assertEqual(end.reason, "non_contiguous_stack_levels")

    def test_active_ring_high_over_target_can_span_multiple_updates(self):
        monitor = HanoiRuleMonitor(all_left())
        begin = monitor.begin_move(ActiveMove("xsmall", "left", "right"))
        self.assertNotEqual(begin.status, "fail")
        curr_positions = all_left()
        curr_positions["ring_xsmall"] = ideal_pose("right", 4)

        first = monitor.update(curr_positions)
        second = monitor.update(curr_positions)

        self.assertEqual(first.status, "running")
        self.assertEqual(second.status, "running")

    def test_non_top_ring_leaving_peg_fails(self):
        prev = classify_hanoi_state(all_left())
        curr_positions = all_left()
        curr_positions["ring_medium"] = (PEG_X, PEG_YS["right"], RING_BASE_Z + 0.20)
        curr = classify_hanoi_state(curr_positions)

        result = validate_hanoi_transition(prev, curr, ActiveMove("medium", "left", "right"))

        self.assertEqual(result.status, "fail")
        self.assertEqual(result.reason, "non_top_ring_left_peg")
        self.assertEqual(result.violating_ring, "medium")

    def test_two_rings_leaving_pegs_fails(self):
        prev = classify_hanoi_state(all_left())
        curr_positions = all_left()
        curr_positions["ring_xsmall"] = (PEG_X, PEG_YS["right"], RING_BASE_Z + 0.20)
        curr_positions["ring_small"] = (PEG_X, PEG_YS["middle"], RING_BASE_Z + 0.20)
        curr = classify_hanoi_state(curr_positions)

        result = validate_hanoi_transition(prev, curr, ActiveMove("xsmall", "left", "right"))

        self.assertEqual(result.status, "fail")
        self.assertEqual(result.reason, "multiple_rings_left_pegs")

    def test_larger_ring_on_smaller_ring_fails(self):
        state = classify_hanoi_state(
            positions_from_stacks(
                {
                    "left": ["xlarge", "large", "medium"],
                    "middle": [],
                    "right": ["xsmall", "small"],
                }
            )
        )

        self.assertIn("larger_on_smaller", {violation["type"] for violation in state.violations})

    def test_active_larger_ring_on_smaller_ring_fails_when_placed(self):
        prev = classify_hanoi_state(
            positions_from_stacks(
                {
                    "left": ["xlarge", "large", "medium", "small"],
                    "middle": [],
                    "right": ["xsmall"],
                }
            )
        )
        curr = classify_hanoi_state(
            positions_from_stacks(
                {
                    "left": ["xlarge", "large", "medium"],
                    "middle": [],
                    "right": ["xsmall", "small"],
                }
            )
        )

        result = validate_hanoi_transition(prev, curr, ActiveMove("small", "left", "right"))

        self.assertEqual(result.status, "fail")
        self.assertEqual(result.reason, "larger_on_smaller")
        self.assertEqual(result.violating_ring, "small")

    def test_inaccurate_peg_seating_fails_at_move_end(self):
        monitor = HanoiRuleMonitor(all_left())
        begin = monitor.begin_move(ActiveMove("xsmall", "left", "right"))
        self.assertNotEqual(begin.status, "fail")
        curr_positions = all_left()
        curr_positions["ring_xsmall"] = (
            PEG_X + DEFAULT_SEATED_XY_TOLERANCE + 0.002,
            PEG_YS["right"],
            RING_BASE_Z,
        )
        update = monitor.update(curr_positions)
        self.assertEqual(update.status, "running")

        end = monitor.end_move()

        self.assertEqual(end.status, "fail")
        self.assertEqual(end.reason, "active_ring_not_seated_after_move")

    def test_unrecoverable_pose_fails(self):
        prev = classify_hanoi_state(all_left())
        curr_positions = all_left()
        curr_positions["ring_xsmall"] = (PEG_X + 2.0, PEG_YS["left"], RING_BASE_Z)
        curr = classify_hanoi_state(curr_positions)

        result = validate_hanoi_transition(prev, curr, ActiveMove("xsmall", "left", "right"))

        self.assertEqual(result.status, "fail")
        self.assertIn(result.reason, {"unrecoverable_pose", "unrecoverable_ring_pose"})

    def test_environment_fingerprint_change_fails(self):
        fingerprint = expected_hanoi_environment_fingerprint()
        changed = copy.deepcopy(fingerprint)
        changed["peg_radius"] += 0.001
        monitor = HanoiRuleMonitor(all_left(), environment_fingerprint=fingerprint)

        result = monitor.update(all_left(), environment_fingerprint=changed)

        self.assertEqual(result.status, "fail")
        self.assertEqual(result.reason, "environment_fingerprint_changed")

    def test_target_state_is_deterministic(self):
        positions = positions_from_stacks(
            {
                "left": ["xlarge", "large", "medium"],
                "middle": [],
                "right": ["small", "xsmall"],
            }
        )

        self.assertTrue(
            is_hanoi_target_state(
                positions,
                {"left": ["xlarge", "large", "medium"], "middle": [], "right": ["small", "xsmall"]},
            )
        )
        self.assertFalse(
            is_hanoi_target_state(
                positions,
                {"left": ["xlarge", "large"], "middle": ["medium"], "right": ["small", "xsmall"]},
            )
        )


if __name__ == "__main__":
    unittest.main()
