import argparse
from pathlib import Path
import sys
import pytest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"source/agentbench_platform"))

def test_frozen_runtime_profile_and_missing_tool_fail_closed():
    from agentbench_platform.profile_cli import frozen_profile
    assert frozen_profile('rgb',(), 'reference') == {'observation':'rgb','tools':[],'experience':'reference'}
    with pytest.raises(ValueError,match='unavailable'):
        frozen_profile('rgbd',('graspnet',),'none')


def test_native_cli_freezes_explicit_experience_without_isaac_flag_collision():
    import argparse
    from agentbench_platform.profile_cli import add_profile_arguments, profile_from_args
    parser=argparse.ArgumentParser()
    parser.add_argument('--experience',default='isaac.kit')
    add_profile_arguments(parser)
    args=parser.parse_args(['--profile','rgb','--experience-profile','reference'])
    assert args.experience=='isaac.kit'
    assert profile_from_args(args)=={'observation':'rgb','tools':[],'experience':'reference'}
    with pytest.raises(ValueError,match='unavailable'):
        profile_from_args(parser.parse_args(['--tool','graspnet']))


