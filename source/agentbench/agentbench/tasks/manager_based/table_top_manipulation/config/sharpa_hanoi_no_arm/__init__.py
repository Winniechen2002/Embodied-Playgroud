"""Floating Sharpa Hand variant of the Tower-of-Hanoi environment."""

import importlib

import gymnasium as gym
import numpy as np


def make_sharpa_hanoi_no_arm_env(
    *, cfg=None, env_cfg_entry_point: str | None = None, **kwargs
):
    """Create the non-RL floating-hand Hanoi environment."""

    if cfg is None:
        if env_cfg_entry_point is None:
            raise ValueError(
                "Sharpa Hanoi no-arm environment requires either 'cfg' or "
                "'env_cfg_entry_point'."
            )
        mod_name, attr_name = env_cfg_entry_point.split(":")
        cfg_cls = getattr(importlib.import_module(mod_name), attr_name)
        cfg = cfg_cls()

    from isaaclab.envs import ManagerBasedEnv

    class SharpaHanoiNoArmGymEnv(ManagerBasedEnv, gym.Env):
        """Gym-compatible shell around Isaac Lab's non-RL environment."""

        def __init__(self, env_cfg):
            super().__init__(env_cfg)

            self.single_observation_space = gym.spaces.Dict()
            for group_name in self.observation_manager.active_terms:
                group_dim = self.observation_manager.group_obs_dim[group_name]
                self.single_observation_space[group_name] = gym.spaces.Box(
                    low=-np.inf,
                    high=np.inf,
                    shape=group_dim,
                    dtype=np.float32,
                )

            action_dim = sum(self.action_manager.action_term_dim)
            self.single_action_space = gym.spaces.Box(
                low=-np.inf,
                high=np.inf,
                shape=(action_dim,),
                dtype=np.float32,
            )
            self.observation_space = gym.vector.utils.batch_space(
                self.single_observation_space, self.num_envs
            )
            self.action_space = gym.vector.utils.batch_space(
                self.single_action_space, self.num_envs
            )

    return SharpaHanoiNoArmGymEnv(cfg)


def make_sharpa_hanoi_no_arm_vision_env(
    *, cfg=None, env_cfg_entry_point: str | None = None, **kwargs
):
    """Create floating Sharpa with the strict RGB/proprioception interface."""

    if cfg is None:
        if env_cfg_entry_point is None:
            raise ValueError(
                "Sharpa Hanoi no-arm vision environment requires either "
                "'cfg' or 'env_cfg_entry_point'."
            )
        mod_name, attr_name = env_cfg_entry_point.split(":")
        cfg_cls = getattr(importlib.import_module(mod_name), attr_name)
        cfg = cfg_cls()

    from ..hanoi.vision_env import HanoiVisionEnv

    return HanoiVisionEnv(cfg=cfg, **kwargs)


gym.register(
    id="Agentbench-SharpaHanoiNoArm-v0",
    entry_point=f"{__name__}:make_sharpa_hanoi_no_arm_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": (
            f"{__name__}.sharpa_hanoi_no_arm_cfg:SharpaHanoiNoArmEnvCfg"
        ),
    },
)


gym.register(
    id="Agentbench-SharpaHanoiNoArm-Play-v0",
    entry_point=f"{__name__}:make_sharpa_hanoi_no_arm_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": (
            f"{__name__}.sharpa_hanoi_no_arm_cfg:SharpaHanoiNoArmEnvCfg_PLAY"
        ),
    },
)


gym.register(
    id="Agentbench-SharpaHanoiNoArm-Vision-v0",
    entry_point=f"{__name__}:make_sharpa_hanoi_no_arm_vision_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": (
            f"{__name__}.sharpa_hanoi_no_arm_cfg:"
            "SharpaHanoiNoArmVisionEnvCfg"
        ),
    },
)


gym.register(
    id="Agentbench-SharpaHanoiNoArm-Vision-Play-v0",
    entry_point=f"{__name__}:make_sharpa_hanoi_no_arm_vision_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": (
            f"{__name__}.sharpa_hanoi_no_arm_cfg:"
            "SharpaHanoiNoArmVisionEnvCfg_PLAY"
        ),
    },
)
