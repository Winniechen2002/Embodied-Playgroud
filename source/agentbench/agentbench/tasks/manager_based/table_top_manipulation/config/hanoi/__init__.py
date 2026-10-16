"""Tower-of-Hanoi task configurations for table top manipulation."""

import importlib

import gymnasium as gym


def make_hanoi_env(*, cfg=None, env_cfg_entry_point: str | None = None, **kwargs):
    """Create the non-RL Hanoi ManagerBasedEnv from a registry entry."""

    if cfg is None:
        if env_cfg_entry_point is None:
            raise ValueError("Hanoi environment requires either 'cfg' or 'env_cfg_entry_point'.")
        mod_name, attr_name = env_cfg_entry_point.split(":")
        cfg_cls = getattr(importlib.import_module(mod_name), attr_name)
        cfg = cfg_cls()

    from isaaclab.envs import ManagerBasedEnv

    return ManagerBasedEnv(cfg)


def make_hanoi_vision_env(*, cfg=None, env_cfg_entry_point: str | None = None, **kwargs):
    """Create Hanoi with an agent-facing RGB and robot-state-only interface."""

    if cfg is None:
        if env_cfg_entry_point is None:
            raise ValueError("Hanoi vision environment requires either 'cfg' or 'env_cfg_entry_point'.")
        mod_name, attr_name = env_cfg_entry_point.split(":")
        cfg_cls = getattr(importlib.import_module(mod_name), attr_name)
        cfg = cfg_cls()

    from .vision_env import HanoiVisionEnv

    return HanoiVisionEnv(cfg=cfg, **kwargs)


gym.register(
    id="Agentbench-Hanoi-FrankaPanda-v0",
    entry_point=f"{__name__}:make_hanoi_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.hanoi_cfg:HanoiEnvFrankaPandaCfg",
    },
)


gym.register(
    id="Agentbench-Hanoi-FrankaPanda-Play-v0",
    entry_point=f"{__name__}:make_hanoi_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.hanoi_cfg:HanoiEnvFrankaPandaCfg_PLAY",
    },
)


gym.register(
    id="Agentbench-Hanoi-FrankaPanda-Vision-v0",
    entry_point=f"{__name__}:make_hanoi_vision_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.hanoi_cfg:HanoiEnvFrankaPandaVisionCfg",
    },
)


gym.register(
    id="Agentbench-Hanoi-FrankaPanda-Vision-Play-v0",
    entry_point=f"{__name__}:make_hanoi_vision_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.hanoi_cfg:HanoiEnvFrankaPandaVisionCfg_PLAY",
    },
)
