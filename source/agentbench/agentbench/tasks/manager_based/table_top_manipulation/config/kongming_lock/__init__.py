"""Dual-Franka six-piece Kongming-lock task registration."""

import gymnasium as gym


def _make(*, cfg=None, env_cfg_entry_point: str | None = None, **kwargs):
    from .kongming_lock_env import make_kongming_lock_env

    return make_kongming_lock_env(cfg=cfg, env_cfg_entry_point=env_cfg_entry_point, **kwargs)


gym.register(
    id="Agentbench-KongmingLock-DualFranka-Disassemble-v0",
    entry_point=f"{__name__}:_make",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.kongming_lock_cfg:KongmingLockEnvCfg",
        "task_mode": "disassemble",
    },
)

gym.register(
    id="Agentbench-KongmingLock-DualSharpa-Assemble-v0",
    entry_point=f"{__name__}:_make",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.kongming_lock_sharpa_cfg:KongmingDualSharpaEnvCfg_ASSEMBLE",
        "task_mode": "assemble",
    },
)

gym.register(
    id="Agentbench-KongmingLock-DualSharpa-Disassemble-v0",
    entry_point=f"{__name__}:_make",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.kongming_lock_sharpa_cfg:KongmingDualSharpaEnvCfg",
        "task_mode": "disassemble",
    },
)

gym.register(
    id="Agentbench-KongmingLock-DualSharpa-Assemble-Play-v0",
    entry_point=f"{__name__}:_make",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.kongming_lock_sharpa_cfg:KongmingDualSharpaEnvCfg_ASSEMBLE_PLAY",
        "task_mode": "assemble",
    },
)

gym.register(
    id="Agentbench-KongmingLock-DualSharpa-Disassemble-Play-v0",
    entry_point=f"{__name__}:_make",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.kongming_lock_sharpa_cfg:KongmingDualSharpaEnvCfg_PLAY",
        "task_mode": "disassemble",
    },
)

gym.register(
    id="Agentbench-KongmingLock-DualFranka-Assemble-v0",
    entry_point=f"{__name__}:_make",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.kongming_lock_cfg:KongmingLockEnvCfg_ASSEMBLE",
        "task_mode": "assemble",
    },
)

gym.register(
    id="Agentbench-KongmingLock-DualFranka-Assemble-Play-v0",
    entry_point=f"{__name__}:_make",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.kongming_lock_cfg:KongmingLockEnvCfg_ASSEMBLE_PLAY",
        "task_mode": "assemble",
    },
)

gym.register(
    id="Agentbench-KongmingLock-DualFranka-Disassemble-Play-v0",
    entry_point=f"{__name__}:_make",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.kongming_lock_cfg:KongmingLockEnvCfg_PLAY",
        "task_mode": "disassemble",
    },
)

__all__ = []
