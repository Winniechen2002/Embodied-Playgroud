"""Observation terms shared by both bimanual pocket-cube tasks."""

from __future__ import annotations

import torch

def cube_detent_state(
    env,
) -> torch.Tensor:
    """Continuous, wrap-safe state of the six logical face coordinates.

    The output is ``[sin(q), cos(q), qdot]``.  It exposes partial turns without
    discontinuities at +/-pi and lets a policy see whether every layer is at a
    quarter-turn detent.
    """

    if not hasattr(env, "get_pocket_cube_face_joint_state"):
        return torch.cat(
            (
                torch.zeros((env.num_envs, 6), device=env.device),
                torch.ones((env.num_envs, 6), device=env.device),
                torch.zeros((env.num_envs, 6), device=env.device),
            ),
            dim=-1,
        )
    joint_pos, joint_vel = env.get_pocket_cube_face_joint_state()
    return torch.cat((torch.sin(joint_pos), torch.cos(joint_pos), joint_vel), dim=-1)


def cube_cubie_state(env) -> torch.Tensor:
    """Return 8 corner identities followed by 8 corner orientations."""

    if hasattr(env, "pocket_cube_state_tensor"):
        return env.pocket_cube_state_tensor
    return torch.cat(
        (
            torch.arange(8, device=env.device).expand(env.num_envs, -1),
            torch.zeros((env.num_envs, 8), device=env.device),
        ),
        dim=-1,
    ).to(torch.float32)


def cube_interlock_state(env) -> torch.Tensor:
    """One-hot active face plus failure bit for the physical interlock."""

    if not hasattr(env, "pocket_cube_active_face"):
        return torch.zeros((env.num_envs, 7), device=env.device)
    active = env.pocket_cube_active_face
    one_hot = torch.zeros((env.num_envs, 6), device=env.device)
    valid = active >= 0
    if valid.any():
        one_hot[valid, active[valid]] = 1.0
    failed = env.pocket_cube_rule_failed.to(torch.float32).unsqueeze(-1)
    return torch.cat((one_hot, failed), dim=-1)


def cube_target_state(env) -> torch.Tensor:
    """Return the configured 8-corner target state."""

    if hasattr(env, "pocket_cube_target_tensor"):
        return env.pocket_cube_target_tensor
    return cube_cubie_state(env)


def cube_success(env) -> torch.Tensor:
    """Exact target-state indicator, independent of planned actions."""

    if hasattr(env, "pocket_cube_success"):
        return env.pocket_cube_success.to(torch.float32).unsqueeze(-1)
    return torch.zeros((env.num_envs, 1), device=env.device)
