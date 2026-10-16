"""Observation helpers for the privileged Kongming-lock interface."""

from __future__ import annotations

import torch
from .shapes import LockPhase


def _root_state(asset):
    data = asset.data
    return (
        data.root_pos_w,
        data.root_quat_w,
        getattr(data, "root_lin_vel_w", torch.zeros_like(data.root_pos_w)),
        getattr(data, "root_ang_vel_w", torch.zeros_like(data.root_pos_w)),
    )


def privileged_lock_state(env) -> torch.Tensor:
    """Return a stable flat Level-3 state vector for each environment.

    The vector deliberately includes the source fields in a fixed order.  A
    companion dictionary is available through ``env.get_privileged_state`` for
    human-readable evidence; this term is the compact policy-facing form.
    """

    values = []
    for robot_name in ("left_robot", "right_robot"):
        robot = env.scene[robot_name]
        values.extend((robot.data.joint_pos, robot.data.joint_vel))
        body_ids = robot.find_bodies("panda_hand", preserve_order=True)[0]
        if len(body_ids) == 1 and hasattr(robot.data, "body_pos_w"):
            values.extend((robot.data.body_pos_w[:, body_ids[0]], robot.data.body_quat_w[:, body_ids[0]]))
        else:
            values.extend((torch.zeros((env.num_envs, 3), device=env.device),
                           torch.zeros((env.num_envs, 4), device=env.device)))

    for name in env.lock_piece_names:
        position, quat, linear, angular = _root_state(env.scene[f"piece_{name}"])
        values.extend((position, quat, linear, angular))

    for name in env.lock_piece_names:
        target = env.lock_target_tensor(name)
        values.append(target.expand(env.num_envs, -1))

    for sensor_name in ("left_finger_piece_contact", "right_finger_piece_contact"):
        sensor = env.scene[sensor_name]
        forces = getattr(sensor.data, "net_forces_w", None)
        if forces is None:
            values.append(torch.zeros((env.num_envs, 1), device=env.device))
        else:
            if forces.ndim == 3:
                forces = forces[:, -1]
            values.append(torch.linalg.vector_norm(forces, dim=-1, keepdim=True))

    removed = getattr(env, "lock_removed_mask", torch.zeros((env.num_envs, len(env.lock_piece_names)), device=env.device))
    placed = getattr(env, "lock_placed_mask", torch.zeros_like(removed))
    assembled = getattr(env, "lock_assembled_mask", torch.zeros_like(removed))
    phases = getattr(env, "lock_phase_one_hot", torch.zeros((env.num_envs, len(LockPhase)), device=env.device))
    penetration = getattr(env, "lock_max_penetration_m", torch.zeros((env.num_envs,), device=env.device))
    values.extend((removed, placed))
    task_mode = getattr(env, "task_mode", None)
    if getattr(task_mode, "value", task_mode) == "assemble":
        values.append(assembled)
    values.append(phases)
    values.append(penetration.view(env.num_envs, 1))
    return torch.cat([value.reshape(env.num_envs, -1).to(dtype=torch.float32) for value in values], dim=-1)


__all__ = ["privileged_lock_state"]
