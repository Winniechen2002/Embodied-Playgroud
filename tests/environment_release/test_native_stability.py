import pytest

from agentbench_platform.environment_qa import structure_displacement


def test_settling_does_not_hide_a_collapsed_initial_structure():
    initial = {'upper_block': [0., 0., .2], 'support': [0., 0., 0.]}
    settled = {'upper_block': [0., 0., .1], 'support': [0., 0., 0.]}
    assert structure_displacement(settled, settled) == 0.
    assert structure_displacement(initial, settled) > .003


@pytest.mark.parametrize('current', [{}, {'block': [0., 0., float('nan')]},
    {'block': [0., 0.]}, {'other_block': [0., 0., 0.]}])
def test_missing_or_invalid_native_pose_is_rejected(current):
    with pytest.raises(AssertionError):
        structure_displacement({'block': [0., 0., 0.]}, current)
