"""Rubik's Cube task registration."""

import importlib

import gymnasium as gym


def make_rubiks_cube_env(*, cfg=None, env_cfg_entry_point: str | None = None, **kwargs):
    """Create the non-RL Rubik's Cube ManagerBasedEnv."""

    if cfg is None:
        if env_cfg_entry_point is None:
            raise ValueError("Rubik's Cube environment requires 'cfg' or 'env_cfg_entry_point'.")
        mod_name, attr_name = env_cfg_entry_point.split(":")
        cfg_cls = getattr(importlib.import_module(mod_name), attr_name)
        cfg = cfg_cls()

    from .rubiks_cube_env import RubiksCubeEnv

    return RubiksCubeEnv(cfg)


gym.register(
    id="Agentbench-RubiksCube-FrankaPanda-v0",
    entry_point=f"{__name__}:make_rubiks_cube_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rubiks_cube_cfg:RubiksCubeEnvFrankaPandaCfg",
    },
)

gym.register(
    id="Agentbench-RubiksCube-FrankaPanda-Play-v0",
    entry_point=f"{__name__}:make_rubiks_cube_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rubiks_cube_cfg:RubiksCubeEnvFrankaPandaCfg_PLAY",
    },
)

gym.register(
    id="Agentbench-RubiksCube-FloatingSharpaRight-v0",
    entry_point=f"{__name__}:make_rubiks_cube_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rubiks_cube_sharpa_cfg:RubiksCubeEnvFloatingSharpaRightCfg",
    },
)

gym.register(
    id="Agentbench-RubiksCube-FloatingSharpaRight-Play-v0",
    entry_point=f"{__name__}:make_rubiks_cube_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rubiks_cube_sharpa_cfg:RubiksCubeEnvFloatingSharpaRightCfg_PLAY",
    },
)
