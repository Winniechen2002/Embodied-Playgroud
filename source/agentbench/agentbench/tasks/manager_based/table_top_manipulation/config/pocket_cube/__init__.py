"""Bimanual 2x2 Rubik's-cube task registrations."""

import importlib

import gymnasium as gym


def make_pocket_cube_env(*, cfg=None, env_cfg_entry_point: str | None = None, **kwargs):
    if cfg is None:
        if env_cfg_entry_point is None:
            raise ValueError("Pocket-cube environment requires cfg or env_cfg_entry_point")
        module_name, attribute_name = env_cfg_entry_point.split(":")
        cfg = getattr(importlib.import_module(module_name), attribute_name)()

    from .pocket_cube_env import InterlockedPocketCubeEnv

    return InterlockedPocketCubeEnv(cfg)


_TASKS = {
    "Agentbench-PocketCube-DualSharpa-v0": "dual_sharpa_cfg:DualSharpaPocketCubeEnvCfg",
    "Agentbench-PocketCube-DualSharpa-Play-v0": "dual_sharpa_cfg:DualSharpaPocketCubeEnvCfg_PLAY",
    "Agentbench-PocketCube-DualAloha-v0": "dual_aloha_cfg:DualAlohaPocketCubeEnvCfg",
    "Agentbench-PocketCube-DualAloha-Play-v0": "dual_aloha_cfg:DualAlohaPocketCubeEnvCfg_PLAY",
}

for task_id, relative_entry_point in _TASKS.items():
    gym.register(
        id=task_id,
        entry_point=f"{__name__}:make_pocket_cube_env",
        disable_env_checker=True,
        kwargs={"env_cfg_entry_point": f"{__name__}.{relative_entry_point}"},
    )

del task_id, relative_entry_point
