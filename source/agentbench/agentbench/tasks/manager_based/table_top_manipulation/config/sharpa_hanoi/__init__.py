"""Franka FR3 + Sharpa Hand variant of the Tower-of-Hanoi environment."""

import importlib

import gymnasium as gym
import numpy as np


def _apply_fr3_robot_limits(env):
    """Restore FR3 physical limits missing from the composed Sharpa USD."""

    import torch

    robot = env.scene["robot"]
    names = [f"panda_joint{index}" for index in range(1, 8)]
    joint_ids, resolved = robot.find_joints(names, preserve_order=True)
    if list(resolved) != names:
        raise RuntimeError(f"Unexpected FR3 joint order in Sharpa asset: {resolved}")
    limits = torch.tensor(
        [
            [-2.8973, 2.8973],
            [-1.7628, 1.7628],
            [-2.8973, 2.8973],
            [-3.0718, -0.0698],
            [-2.8973, 2.8973],
            [-0.0175, 3.7525],
            [-2.8973, 2.8973],
        ],
        dtype=torch.float32,
        device=robot.device,
    ).unsqueeze(0).expand(robot.num_instances, -1, -1)
    robot.write_joint_position_limit_to_sim(
        limits, joint_ids=joint_ids, warn_limit_violation=True
    )
    return env


def make_sharpa_hanoi_env(*, cfg=None, env_cfg_entry_point: str | None = None, **kwargs):
    """Create the non-RL Sharpa Hanoi ManagerBasedEnv from a registry entry."""

    if cfg is None:
        if env_cfg_entry_point is None:
            raise ValueError("Sharpa Hanoi environment requires either 'cfg' or 'env_cfg_entry_point'.")
        mod_name, attr_name = env_cfg_entry_point.split(":")
        cfg_cls = getattr(importlib.import_module(mod_name), attr_name)
        cfg = cfg_cls()

    from isaaclab.envs import ManagerBasedEnv

    class SharpaHanoiGymEnv(ManagerBasedEnv, gym.Env):
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

    return _apply_fr3_robot_limits(SharpaHanoiGymEnv(cfg))


def make_sharpa_hanoi_vision_env(
    *, cfg=None, env_cfg_entry_point: str | None = None, **kwargs
):
    """Create Sharpa Hanoi with the strict RGB/proprioception interface."""

    if cfg is None:
        if env_cfg_entry_point is None:
            raise ValueError(
                "Sharpa Hanoi vision environment requires either 'cfg' or "
                "'env_cfg_entry_point'."
            )
        mod_name, attr_name = env_cfg_entry_point.split(":")
        cfg_cls = getattr(importlib.import_module(mod_name), attr_name)
        cfg = cfg_cls()

    from ..hanoi.vision_env import HanoiVisionEnv

    return _apply_fr3_robot_limits(HanoiVisionEnv(cfg=cfg, **kwargs))


gym.register(
    id="Agentbench-SharpaHanoi-v0",
    entry_point=f"{__name__}:make_sharpa_hanoi_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.sharpa_hanoi_cfg:SharpaHanoiEnvCfg",
    },
)


gym.register(
    id="Agentbench-SharpaHanoi-Play-v0",
    entry_point=f"{__name__}:make_sharpa_hanoi_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.sharpa_hanoi_cfg:SharpaHanoiEnvCfg_PLAY",
    },
)


gym.register(
    id="Agentbench-SharpaHanoi-Vision-v0",
    entry_point=f"{__name__}:make_sharpa_hanoi_vision_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": (
            f"{__name__}.sharpa_hanoi_cfg:SharpaHanoiVisionEnvCfg"
        ),
    },
)


gym.register(
    id="Agentbench-SharpaHanoi-Vision-Play-v0",
    entry_point=f"{__name__}:make_sharpa_hanoi_vision_env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": (
            f"{__name__}.sharpa_hanoi_cfg:SharpaHanoiVisionEnvCfg_PLAY"
        ),
    },
)
