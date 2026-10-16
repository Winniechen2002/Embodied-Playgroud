# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Common functions that can be used to activate certain terminations for the dexsuite task.

The functions can be passed to the :class:`isaaclab.managers.TerminationTermCfg` object to enable
the termination introduced by the function.
"""

from __future__ import annotations

import os
import numpy as np
import torch
from typing import TYPE_CHECKING

from isaaclab.assets import Articulation, RigidObject
from isaaclab.managers import ManagerTermBase, SceneEntityCfg
from isaaclab.utils.math import combine_frame_transforms, compute_pose_error, quat_apply, subtract_frame_transforms
from .resets import reset_joints_to_init
from pathlib import Path

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv

# Try to import PhysX for contact force access
try:
    import omni.isaac.core.utils.nucleus as nucleus_utils
    from omni.isaac.core.utils.types import ArticulationAction
    import omni.physx as _physx
    PHYSX_AVAILABLE = True
except ImportError:
    PHYSX_AVAILABLE = False


def out_of_bound(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    in_bound_range: dict[str, tuple[float, float]] = {},
) -> torch.Tensor:
    """Termination condition for the object falls out of bound.

    Args:
        env: The environment.
        asset_cfg: The object configuration. Defaults to SceneEntityCfg("object").
        in_bound_range: The range in x, y, z such that the object is considered in range
    """
    object: RigidObject = env.scene[asset_cfg.name]
    range_list = [in_bound_range.get(key, (0.0, 0.0)) for key in ["x", "y", "z"]]
    ranges = torch.tensor(range_list, device=env.device)

    object_pos_local = object.data.root_pos_w - env.scene.env_origins
    outside_bounds = ((object_pos_local < ranges[:, 0]) | (object_pos_local > ranges[:, 1])).any(dim=1)
    return outside_bounds


def abnormal_robot_state(env: ManagerBasedRLEnv, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot")) -> torch.Tensor:
    """Terminating environment when violation of velocity limits detects, this usually indicates unstable physics caused
    by very bad, or aggressive action"""
    robot: Articulation = env.scene[asset_cfg.name]
    
    # Compute violation mask: joint_vel.abs() > (joint_vel_limits * 2)
    joint_vel_abs = robot.data.joint_vel.abs()
    joint_vel_limit_threshold = robot.data.joint_vel_limits * 10
    violation_mask = joint_vel_abs > joint_vel_limit_threshold  # [num_envs, num_joints]
    
    # # Check which environments have any violations
    abnormal_envs = violation_mask.any(dim=1)  # [num_envs]
    return abnormal_envs

def object_at_goal_position(
    env: ManagerBasedRLEnv,
    command_name: str,
    threshold: float = 0.02,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Termination condition for when the object is close enough to the goal position.
    
    This checks if the object's position is within the specified threshold of the goal position.
    Orientation is ignored - only position matters.
    
    Args:
        env: The environment.
        command_name: The name of the command term that contains the goal position.
        threshold: Distance threshold in meters. Defaults to 0.05.
        object_cfg: The object configuration. Defaults to SceneEntityCfg("object").
    
    Returns:
        A boolean tensor indicating which environments have succeeded (object at goal position).
    """
    # Get the command term which has position_error metric
    command_term = env.command_manager.get_term(command_name)
    
    # Check if position error is below threshold
    position_error = command_term.metrics["position_error"]
    success = position_error < threshold
    
    return success

def success_position(
    env: ManagerBasedRLEnv,
    command_name: str,
    asset_cfg: SceneEntityCfg,
    align_asset_cfg: SceneEntityCfg,
    pos_threshold: float = 0.05,
) -> torch.Tensor:
    """Terminate when object reaches commanded position within a threshold."""
    asset: RigidObject = env.scene[asset_cfg.name]
    object: RigidObject = env.scene[align_asset_cfg.name]
    command = env.command_manager.get_command(command_name)
    des_pos_w, _ = combine_frame_transforms(asset.data.root_pos_w, asset.data.root_quat_w, command[:, :3])
    distance = torch.norm(object.data.root_pos_w - des_pos_w, dim=1)
    return distance < pos_threshold


def object_tilted(
    env: ManagerBasedRLEnv,
    threshold_rad: float = 2.35619449,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Terminate when object tilt angle exceeds threshold (rad)."""
    object: RigidObject = env.scene[object_cfg.name]
    up_local = torch.tensor([0.0, 0.0, 1.0], device=env.device).repeat(env.num_envs, 1)
    up_w = quat_apply(object.data.root_quat_w, up_local)
    world_up = torch.tensor([0.0, 0.0, 1.0], device=env.device).repeat(env.num_envs, 1)
    cos_angle = torch.sum(up_w * world_up, dim=1).clamp(-1.0, 1.0)
    angle = torch.acos(cos_angle)
    return angle >= threshold_rad


def object_axis_tilted(
    env: ManagerBasedRLEnv,
    axis_local: tuple[float, float, float] = (0.0, 0.0, 1.0),
    threshold_rad: float = 2.35619449,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Terminate when a specified object local axis tilts beyond threshold (rad) from world +Z."""
    object: RigidObject = env.scene[object_cfg.name]
    axis = torch.tensor(axis_local, device=env.device, dtype=object.data.root_quat_w.dtype)
    axis = axis / torch.norm(axis)
    axis_local_w = axis.repeat(env.num_envs, 1)
    axis_w = quat_apply(object.data.root_quat_w, axis_local_w)
    world_up = torch.tensor([0.0, 0.0, 1.0], device=env.device, dtype=axis_w.dtype).repeat(env.num_envs, 1)
    cos_angle = torch.sum(axis_w * world_up, dim=1).clamp(-1.0, 1.0)
    angle = torch.acos(cos_angle)
    return angle >= threshold_rad


def lift_and_tilt(
    env: ManagerBasedRLEnv,
    min_height: float,
    threshold_rad: float,
    axis_local: tuple[float, float, float] = (0.0, 0.0, 1.0),
    world_axis: tuple[float, float, float] = (0.0, 0.0, 1.0),
    tilt_ge: bool = True,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Terminate when object is lifted above min_height and tilt angle meets threshold."""
    object: RigidObject = env.scene[object_cfg.name]
    axis = torch.tensor(axis_local, device=env.device, dtype=object.data.root_quat_w.dtype)
    axis = axis / torch.norm(axis)
    axis_local_w = axis.repeat(env.num_envs, 1)
    axis_w = quat_apply(object.data.root_quat_w, axis_local_w)
    world_axis_t = torch.tensor(world_axis, device=env.device, dtype=axis_w.dtype)
    world_axis_t = world_axis_t / torch.norm(world_axis_t)
    world_axis_w = world_axis_t.repeat(env.num_envs, 1)
    cos_angle = torch.sum(axis_w * world_axis_w, dim=1).clamp(-1.0, 1.0)
    angle = torch.acos(cos_angle)
    tilt_ok = angle >= threshold_rad if tilt_ge else angle <= threshold_rad
    lifted = object_lifted(env, asset_cfg=object_cfg, min_height=min_height)
    return lifted & tilt_ok


def pour_object(
    env: ManagerBasedRLEnv,
    min_height: float,
    threshold_rad: float,
    axis_local: tuple[float, float, float] = (0.0, -1.0, 0.0),
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Terminate when object is lifted above min_height and tilted beyond threshold_rad."""
    return lift_and_tilt(
        env,
        min_height=min_height,
        threshold_rad=threshold_rad,
        axis_local=axis_local,
        tilt_ge=True,
        object_cfg=object_cfg,
    )


def object_upright_and_lifted(
    env: ManagerBasedRLEnv,
    min_height: float = 0.10,
    max_tilt_rad: float = 0.174532925,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Terminate when object is upright (tilt <= max_tilt_rad) and lifted above init height."""
    object: RigidObject = env.scene[object_cfg.name]
    up_local = torch.tensor([0.0, 0.0, 1.0], device=env.device).repeat(env.num_envs, 1)
    up_w = quat_apply(object.data.root_quat_w, up_local)
    world_up = torch.tensor([0.0, 0.0, 1.0], device=env.device).repeat(env.num_envs, 1)
    cos_angle = torch.sum(up_w * world_up, dim=1).clamp(-1.0, 1.0)
    angle = torch.acos(cos_angle)
    upright = angle <= max_tilt_rad

    z = object.data.root_pos_w[:, 2]
    default_z = object.data.default_root_state[:, 2]
    lifted = (z - default_z) >= min_height
    return upright & lifted


def _resolve_joint_ids(asset_cfg: SceneEntityCfg, env: ManagerBasedRLEnv) -> None:
    if isinstance(asset_cfg.joint_ids, slice) and asset_cfg.joint_ids == slice(None) and asset_cfg.joint_names is not None:
        asset_cfg.resolve(env.scene)


def _get_init_joint_pos(asset: Articulation, joint_ids) -> torch.Tensor:
    init_joint_pos = asset.data.default_joint_pos.clone()
    init_cfg = getattr(asset.cfg.init_state, "joint_pos", None) or {}
    if init_cfg:
        name_to_id = {name: idx for idx, name in enumerate(asset.joint_names)}
        if isinstance(joint_ids, slice):
            target_ids = None
        else:
            if torch.is_tensor(joint_ids):
                target_ids = set(joint_ids.tolist())
            else:
                target_ids = set(joint_ids)
        for name, value in init_cfg.items():
            jid = name_to_id.get(name, None)
            if jid is None:
                continue
            if target_ids is not None and jid not in target_ids:
                continue
            init_joint_pos[:, jid] = float(value)
    return init_joint_pos[:, joint_ids]


def _compare(value: torch.Tensor, target: torch.Tensor | float, op: str, tol: float) -> torch.Tensor:
    if op == ">=":
        return value >= (target - tol)
    if op == ">":
        return value > (target - tol)
    if op == "<=":
        return value <= (target + tol)
    if op == "<":
        return value < (target + tol)
    raise ValueError(f"Unsupported op: {op}")


def joint_reach_threshold(
    env: ManagerBasedRLEnv,
    threshold: float,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    op: str = ">=",
    ref: str = "value",
    tol: float = 0.0,
    reduce: str = "any",
) -> torch.Tensor:
    """Terminate when joint values cross a threshold."""
    asset: Articulation = env.scene[asset_cfg.name]
    _resolve_joint_ids(asset_cfg, env)
    joint_ids = asset_cfg.joint_ids
    joint_pos = asset.data.joint_pos[:, joint_ids]

    if ref == "value":
        target = threshold
    elif ref == "upper_limit":
        target = asset.data.joint_pos_limits[:, joint_ids, 1] + threshold
    elif ref == "lower_limit":
        target = asset.data.joint_pos_limits[:, joint_ids, 0] + threshold
    else:
        raise ValueError(f"Unsupported ref: {ref}")

    cmp = _compare(joint_pos, target, op, tol)
    if reduce == "any":
        return cmp.any(dim=1)
    if reduce == "all":
        return cmp.all(dim=1)
    raise ValueError(f"Unsupported reduce: {reduce}")


def joint_relative_move(
    env: ManagerBasedRLEnv,
    threshold: float,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    mode: str = "displacement",
    op: str = ">=",
    reduce: str = "any",
) -> torch.Tensor:
    """Terminate when joint displacement or progress crosses a threshold."""
    asset: Articulation = env.scene[asset_cfg.name]
    _resolve_joint_ids(asset_cfg, env)
    joint_ids = asset_cfg.joint_ids
    joint_pos = asset.data.joint_pos[:, joint_ids]

    init_joint_pos = _get_init_joint_pos(asset, joint_ids)
    delta = torch.abs(joint_pos - init_joint_pos)

    if mode == "displacement":
        value = delta
    elif mode == "progress":
        lower = asset.data.joint_pos_limits[:, joint_ids, 0]
        upper = asset.data.joint_pos_limits[:, joint_ids, 1]
        reachable = torch.maximum(init_joint_pos - lower, upper - init_joint_pos)
        denom = torch.clamp(reachable, min=1e-6)
        value = delta / denom
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    cmp = _compare(value, threshold, op, 0.0)
    if reduce == "any":
        return cmp.any(dim=1)
    if reduce == "all":
        return cmp.all(dim=1)
    raise ValueError(f"Unsupported reduce: {reduce}")


def reset_joints_to_limits(
    env: ManagerBasedRLEnv,
    env_ids: torch.Tensor,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    use_upper: bool = False,
):
    """Reset joints to their lower/upper limits for the given asset."""
    asset: Articulation = env.scene[asset_cfg.name]
    if isinstance(asset_cfg.joint_ids, slice) and asset_cfg.joint_ids == slice(None) and asset_cfg.joint_names is not None:
        asset_cfg.resolve(env.scene)
    joint_ids = asset_cfg.joint_ids
    limits = asset.data.joint_pos_limits[:, joint_ids, 1 if use_upper else 0]
    joint_pos = limits.clone()
    joint_vel = torch.zeros_like(joint_pos)
    asset.write_joint_state_to_sim(joint_pos, joint_vel, env_ids=env_ids)


def reset_board_and_switch_xy(
    env: ManagerBasedRLEnv,
    env_ids: torch.Tensor,
    board_cfg: SceneEntityCfg,
    switch_cfg: SceneEntityCfg,
    switch_joint_cfg: SceneEntityCfg | None = None,
    xy_range: tuple[float, float] | None = None,
    x_range: tuple[float, float] | None = None,
    y_range: tuple[float, float] | None = None,
):
    """Reset board and switch positions with the same XY offset."""
    board = env.scene[board_cfg.name]
    switch = env.scene[switch_cfg.name]

    if isinstance(env_ids, slice):
        env_ids_t = torch.arange(env.num_envs, device=env.device, dtype=torch.long)
    else:
        env_ids_t = env_ids.to(device=env.device, dtype=torch.long)

    if x_range is None:
        if xy_range is None:
            raise ValueError("reset_board_and_switch_xy requires xy_range or x_range.")
        x_range = xy_range
    if y_range is None:
        if xy_range is None:
            raise ValueError("reset_board_and_switch_xy requires xy_range or y_range.")
        y_range = xy_range

    # sample offsets
    offsets = torch.zeros((env_ids_t.shape[0], 3), device=env.device)
    offsets[:, 0].uniform_(x_range[0], x_range[1])
    offsets[:, 1].uniform_(y_range[0], y_range[1])

    board_state = board.data.default_root_state[env_ids_t].clone()
    switch_state = switch.data.default_root_state[env_ids_t].clone()
    board_state[:, :3] += offsets
    switch_state[:, :3] += offsets

    board.write_root_pose_to_sim(board_state[:, 0:7], env_ids=env_ids_t)
    switch.write_root_pose_to_sim(switch_state[:, 0:7], env_ids=env_ids_t)
    if switch_joint_cfg is not None:
        reset_joints_to_init(env, env_ids_t, switch_joint_cfg)


def set_joint_position_limits(
    env: ManagerBasedRLEnv,
    env_ids: torch.Tensor | None,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    lower: float | None = None,
    upper: float | None = None,
):
    """Set joint position limits for an articulation asset."""
    asset: Articulation = env.scene[asset_cfg.name]
    if isinstance(asset_cfg.joint_ids, slice) and asset_cfg.joint_ids == slice(None) and asset_cfg.joint_names is not None:
        asset_cfg.resolve(env.scene)
    joint_ids = asset_cfg.joint_ids

    if env_ids is None or isinstance(env_ids, slice):
        env_ids_t = torch.arange(env.num_envs, device=env.device, dtype=torch.long)
    else:
        env_ids_t = env_ids.to(device=env.device, dtype=torch.long)

    limits = asset.data.default_joint_pos_limits.clone()
    if lower is not None:
        limits[env_ids_t, joint_ids, 0] = lower
    if upper is not None:
        limits[env_ids_t, joint_ids, 1] = upper
    # Clamp to PhysX supported range for revolute joints.
    limits[env_ids_t, joint_ids, 0] = torch.clamp(limits[env_ids_t, joint_ids, 0], -2.0 * torch.pi, 2.0 * torch.pi)
    limits[env_ids_t, joint_ids, 1] = torch.clamp(limits[env_ids_t, joint_ids, 1], -2.0 * torch.pi, 2.0 * torch.pi)
    limits_to_set = limits[env_ids_t][:, joint_ids]
    asset.write_joint_position_limit_to_sim(limits_to_set, joint_ids=joint_ids, env_ids=env_ids_t, warn_limit_violation=False)


def debug_reset_reasons(
    env: ManagerBasedRLEnv,
    env_ids: torch.Tensor,
    prefix: str = "Env reset",
):
    """Print reset reasons for each env_id based on active termination terms."""
    if isinstance(env_ids, slice):
        env_ids_t = torch.arange(env.num_envs, device=env.device, dtype=torch.long)
    else:
        env_ids_t = env_ids.to(device=env.device, dtype=torch.long)

    term_names = env.termination_manager.active_terms
    if not term_names:
        for env_id in env_ids_t.tolist():
            print(f"{prefix} [{env_id}]: no termination terms active")
        return

    term_buffers = {name: env.termination_manager.get_term(name) for name in term_names}
    for env_id in env_ids_t.tolist():
        reasons = [name for name in term_names if bool(term_buffers[name][env_id])]
        if reasons:
            print(f"{prefix} [{env_id}]: {', '.join(reasons)}")
        else:
            print(f"{prefix} [{env_id}]: unknown")




def object_lifted(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    min_height: float = 0.05,
) -> torch.Tensor:
    """Terminate when an asset is lifted above its default height by min_height."""
    asset = env.scene[asset_cfg.name]
    if isinstance(asset, Articulation):
        z = asset.data.root_pos_w[:, 2]
        default_z = asset.data.default_root_state[:, 2]
    else:
        z = asset.data.root_pos_w[:, 2]
        default_z = asset.data.default_root_state[:, 2]
    return (z - default_z) >= min_height


def joint_above_mid(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Terminate when any joint reaches or exceeds the mid-point of its limits."""
    asset: Articulation = env.scene[asset_cfg.name]
    joint_pos = asset.data.joint_pos[:, asset_cfg.joint_ids]
    lower = asset.data.joint_pos_limits[:, asset_cfg.joint_ids, 0]
    upper = asset.data.joint_pos_limits[:, asset_cfg.joint_ids, 1]
    mid = (lower + upper) * 0.5
    return (joint_pos >= mid).any(dim=1)


def update_articulation_root_from_object(
    env: ManagerBasedRLEnv,
    env_ids: torch.Tensor | None,
    target_cfg: SceneEntityCfg,
    source_cfg: SceneEntityCfg,
):
    """Update an articulation root pose to follow a rigid object's root pose."""
    target: Articulation = env.scene[target_cfg.name]
    source = env.scene[source_cfg.name]

    if env_ids is None or isinstance(env_ids, slice):
        env_ids_t = torch.arange(env.num_envs, device=env.device, dtype=torch.long)
    else:
        env_ids_t = env_ids.to(device=env.device, dtype=torch.long)

    pos = source.data.root_pos_w[env_ids_t]
    quat = source.data.root_quat_w[env_ids_t]
    root_pose = torch.cat([pos, quat], dim=-1)
    target.write_root_pose_to_sim(root_pose, env_ids=env_ids_t)


def update_marker_from_body(
    env: ManagerBasedRLEnv,
    env_ids: torch.Tensor | None,
    marker_cfg: SceneEntityCfg,
    body_cfg: SceneEntityCfg,
    offset: tuple[float, float, float] = (0.0, 0.0, 0.0),
    debug_every_n: int | None = 60,
):
    """Update a marker pose to follow a given articulation body with a local offset."""
    marker: RigidObject = env.scene[marker_cfg.name]
    asset: Articulation = env.scene[body_cfg.name]

    if isinstance(body_cfg.body_ids, slice) and body_cfg.body_ids == slice(None) and body_cfg.body_names is not None:
        body_cfg.resolve(env.scene)
    body_ids = body_cfg.body_ids
    if isinstance(body_ids, slice):
        body_id = 0
    else:
        body_id = body_ids[0]

    if env_ids is None or isinstance(env_ids, slice):
        env_ids_t = torch.arange(env.num_envs, device=env.device, dtype=torch.long)
    else:
        env_ids_t = env_ids.to(device=env.device, dtype=torch.long)

    body_pose = asset.data.body_pose_w[env_ids_t, body_id]
    offset_t = torch.tensor(offset, device=env.device, dtype=body_pose.dtype).unsqueeze(0).repeat(env_ids_t.shape[0], 1)
    pos = body_pose[:, 0:3] + quat_apply(body_pose[:, 3:7], offset_t)
    root_pose = torch.cat([pos, body_pose[:, 3:7]], dim=-1)
    marker.write_root_pose_to_sim(root_pose, env_ids=env_ids_t)

    if debug_every_n is not None and debug_every_n > 0:
        if not hasattr(env, "_marker_debug_step"):
            env._marker_debug_step = 0
        env._marker_debug_step += 1
        if env._marker_debug_step % debug_every_n == 0:
            # Print first env's orientation to reduce spam.
            q = body_pose[0, 3:7].detach().cpu().numpy().tolist()
            p = body_pose[0, 0:3].detach().cpu().numpy().tolist()
            print(f"[marker] body pose pos={p} quat(wxyz)={q}")
