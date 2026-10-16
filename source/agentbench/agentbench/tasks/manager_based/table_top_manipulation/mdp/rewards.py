# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from logging import Manager
import os
import numpy as np
import torch
import math
from typing import TYPE_CHECKING
import pickle
from pathlib import Path

from isaaclab.assets import Articulation, RigidObject
from isaaclab.managers import ManagerTermBase, SceneEntityCfg
from isaaclab.sensors import ContactSensor
from isaaclab.utils import math as math_utils
from isaaclab.utils.math import combine_frame_transforms, compute_pose_error, normalize, quat_apply, quat_from_angle_axis, subtract_frame_transforms
from isaaclab.envs.mdp.observations import last_action

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv

def action_rate_l2_clamped(env: ManagerBasedRLEnv) -> torch.Tensor:
    """Penalize the rate of change of the actions using L2 squared kernel."""
    return torch.sum(torch.square(env.action_manager.action - env.action_manager.prev_action), dim=1).clamp(-1000, 1000)


def action_l2_clamped(env: ManagerBasedRLEnv) -> torch.Tensor:
    """Penalize the actions using L2 squared kernel."""
    return torch.sum(torch.square(env.action_manager.action), dim=1).clamp(-1000, 1000)

def object_ee_distance(
    env: ManagerBasedRLEnv,
    std: float,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Reward reaching the object using a tanh-kernel on end-effector distance.

    The reward is close to 1 when the maximum distance between the object and any end-effector body is small.
    """
    asset: RigidObject = env.scene[asset_cfg.name]
    object: RigidObject = env.scene[object_cfg.name]
    asset_pos = asset.data.body_pos_w[:, asset_cfg.body_ids]
    object_pos = object.data.root_pos_w
    # object_ee_distance = torch.norm(asset_pos - object_pos[:, None, :], dim=-1).max(dim=-1).values
    object_ee_distance_sum = torch.norm(asset_pos - object_pos[:, None, :], dim=-1).sum(dim=-1)

    # return 1 - torch.tanh(object_ee_distance / std)
    return torch.exp(-10 * object_ee_distance_sum)


def lift_when_grasping_reward(
    env: ManagerBasedRLEnv, 
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    threshold: float = 0.07,
) -> torch.Tensor:
    """Reward lifting the object when grasping."""
    asset: Articulation = env.scene[asset_cfg.name]
    object: RigidObject = env.scene[object_cfg.name]
    asset_pos = asset.data.body_pos_w[:, asset_cfg.body_ids]
    object_pos = object.data.root_pos_w
    asset_to_obj_distances = torch.norm(asset_pos - object_pos[:, None, :], dim=-1) 
    thumb_to_obj_distance = asset_to_obj_distances[:, 0]
    index_to_obj_distance = asset_to_obj_distances[:, 1]
    middle_to_obj_distance = asset_to_obj_distances[:, 2]
    ring_to_obj_distance = asset_to_obj_distances[:, 3]

    good_contact_cond1 = (thumb_to_obj_distance <= threshold) & (
        (index_to_obj_distance <= threshold) | (middle_to_obj_distance <= threshold) | (ring_to_obj_distance <= threshold)
    )
    latest_action: torch.Tensor = last_action(env) 
    z_lift_action = latest_action[..., 2] 
    # clip to 0 
    z_lift_action = z_lift_action.clamp(0, 1)
    reward = good_contact_cond1 * z_lift_action
    return reward


def object_lift_height(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    min_height: float = 0.05,
) -> torch.Tensor:
    """Reward lifting an asset above its default height.

    Returns a [0,1] reward based on how much the object is lifted.
    """
    asset = env.scene[asset_cfg.name]
    if isinstance(asset, Articulation):
        z = asset.data.root_pos_w[:, 2]
        default_z = asset.data.default_root_state[:, 2]
    else:
        z = asset.data.root_pos_w[:, 2]
        default_z = asset.data.default_root_state[:, 2]
    lift = z - default_z
    return torch.clamp(lift / max(min_height, 1e-6), 0.0, 1.0)

def contacts_flexible(
    env: ManagerBasedRLEnv,
    threshold: float,
    fingertip_names: list[str] | None = None,
) -> torch.Tensor:
    """Reward when thumb + at least one other finger are in contact with object.
    
    Flexible version that accepts fingertip names as parameters.
    
    Args:
        env: The environment.
        threshold: Contact force threshold in Newtons.
        fingertip_names: List of fingertip body names. Expected order: [thumb, index, middle, ring].
                        Defaults to ["thumb_fingertip", "fingertip", "fingertip2", "fingertip3"].
    
    Returns:
        Tensor of shape (num_envs,) with 1.0 when good contact condition is met, 0.0 otherwise.
    """
    if fingertip_names is None:
        fingertip_names = ["thumb_fingertip", "fingertip", "fingertip2", "fingertip3"]
    
    def _get_sensor(base_name: str) -> ContactSensor:
        sensors = env.scene.sensors
        key = f"{base_name}_object_s"
        if key in sensors:
            return sensors[key]
        tip_key = f"{base_name}_tip_object_s"
        if tip_key in sensors:
            return sensors[tip_key]
        # Fall back: raise clear error listing available sensors
        available = list(sensors.keys())
        raise KeyError(f"Contact sensor for '{base_name}' not found. Tried '{key}' and '{tip_key}'. Available: {available}")
    
    # Get contact sensors for each fingertip (at least thumb, index, middle required)
    thumb_contact_sensor: ContactSensor = _get_sensor(fingertip_names[0])
    index_contact_sensor: ContactSensor = _get_sensor(fingertip_names[1])
    middle_contact_sensor: ContactSensor = _get_sensor(fingertip_names[2])
    
    # Check if contact force is above threshold
    thumb_contact = thumb_contact_sensor.data.force_matrix_w.view(env.num_envs, 3)
    index_contact = index_contact_sensor.data.force_matrix_w.view(env.num_envs, 3)
    middle_contact = middle_contact_sensor.data.force_matrix_w.view(env.num_envs, 3)
    
    thumb_contact_mag = torch.norm(thumb_contact, dim=-1)
    index_contact_mag = torch.norm(index_contact, dim=-1)
    middle_contact_mag = torch.norm(middle_contact, dim=-1)
    
    # Good contact: thumb + at least one other finger
    # Include ring finger if available
    if len(fingertip_names) > 3:
        ring_contact_sensor: ContactSensor = _get_sensor(fingertip_names[3])
        ring_contact = ring_contact_sensor.data.force_matrix_w.view(env.num_envs, 3)
        ring_contact_mag = torch.norm(ring_contact, dim=-1)
        good_contact_cond = (thumb_contact_mag > threshold) & (
            (index_contact_mag > threshold) | (middle_contact_mag > threshold) | (ring_contact_mag > threshold)
        )
    else:
        good_contact_cond = (thumb_contact_mag > threshold) & (
            (index_contact_mag > threshold) | (middle_contact_mag > threshold)
        )
    
    return good_contact_cond.float()


def position_command_error_tanh(
    env: ManagerBasedRLEnv, std: float, command_name: str, asset_cfg: SceneEntityCfg, align_asset_cfg: SceneEntityCfg
) -> torch.Tensor:
    """Reward tracking of commanded position using tanh kernel, gated by contact presence."""

    asset: RigidObject = env.scene[asset_cfg.name]
    object: RigidObject = env.scene[align_asset_cfg.name]
    command = env.command_manager.get_command(command_name)
    # obtain the desired and current positions
    des_pos_b = command[:, :3]
    des_pos_w, _ = combine_frame_transforms(asset.data.root_pos_w, asset.data.root_quat_w, des_pos_b)
    distance = torch.norm(object.data.root_pos_w - des_pos_w, dim=1)
    # return (1 - torch.tanh(distance / std)) * contacts(env, 1.0).float()
    return torch.exp(-10 * distance) #* contacts(env, 1.0).float()

def position_command_error_exp_from_metrics(
    env: ManagerBasedRLEnv, std: float, command_name: str
) -> torch.Tensor:
    """Reward tracking of commanded position using command metrics (world-frame distance)."""
    command_term = env.command_manager.get_term(command_name)
    distance = command_term.metrics["position_error"]
    return torch.exp(-distance / max(std, 1e-6))




def success_reward(
    env: ManagerBasedRLEnv,
    command_name: str,
    asset_cfg: SceneEntityCfg,
    align_asset_cfg: SceneEntityCfg,
    pos_std: float,
    rot_std: float | None = None,
) -> torch.Tensor:
    """Reward success by comparing commanded pose to the object pose using tanh kernels on error."""

    asset: RigidObject = env.scene[asset_cfg.name]
    object: RigidObject = env.scene[align_asset_cfg.name]
    command = env.command_manager.get_command(command_name)
    des_pos_w, des_quat_w = combine_frame_transforms(
        asset.data.root_pos_w, asset.data.root_quat_w, command[:, :3], command[:, 3:7]
    )
    pos_err, rot_err = compute_pose_error(des_pos_w, des_quat_w, object.data.root_pos_w, object.data.root_quat_w)
    pos_dist = torch.norm(pos_err, dim=1)
    if not rot_std:
        # square is not necessary but this help to keep the final value between having rot_std or not roughly the same
        return (1 - torch.tanh(pos_dist / pos_std)) ** 2
    rot_dist = torch.norm(rot_err, dim=1)
    return (1 - torch.tanh(pos_dist / pos_std)) * (1 - torch.tanh(rot_dist / rot_std))

def success_reward_from_metrics(
    env: ManagerBasedRLEnv,
    command_name: str,
    pos_std: float,
    rot_std: float | None = None,
) -> torch.Tensor:
    """Reward success using command metrics (world-frame errors)."""
    command_term = env.command_manager.get_term(command_name)
    pos_dist = command_term.metrics["position_error"]
    if not rot_std:
        return (1 - torch.tanh(pos_dist / pos_std)) ** 2
    rot_dist = command_term.metrics["orientation_error"]
    return (1 - torch.tanh(pos_dist / pos_std)) * (1 - torch.tanh(rot_dist / rot_std))


def tilt_angle_reward(
    env: ManagerBasedRLEnv,
    threshold_rad: float = 2.35619449,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Reward tilting the object beyond a threshold angle (in radians)."""
    object: RigidObject = env.scene[object_cfg.name]
    up_local = torch.tensor([0.0, 0.0, 1.0], device=env.device).repeat(env.num_envs, 1)
    up_w = quat_apply(object.data.root_quat_w, up_local)
    world_up = torch.tensor([0.0, 0.0, 1.0], device=env.device).repeat(env.num_envs, 1)
    cos_angle = torch.sum(up_w * world_up, dim=1).clamp(-1.0, 1.0)
    angle = torch.acos(cos_angle)
    return torch.clamp((angle - threshold_rad) / (math.pi - threshold_rad), 0.0, 1.0)


def joint_open_reward(
    env: ManagerBasedRLEnv,
    threshold_rad: float,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Reward opening a joint beyond a threshold (uses max abs joint position)."""
    asset: Articulation = env.scene[asset_cfg.name]
    joint_pos = asset.data.joint_pos[:, asset_cfg.joint_ids]
    max_abs = torch.abs(joint_pos).max(dim=1).values
    return torch.clamp(max_abs / threshold_rad, 0.0, 1.0)


def joint_displacement_reward(
    env: ManagerBasedRLEnv,
    threshold_m: float,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Reward joint displacement magnitude from init beyond a threshold."""
    asset: Articulation = env.scene[asset_cfg.name]
    if isinstance(asset_cfg.joint_ids, slice) and asset_cfg.joint_ids == slice(None) and asset_cfg.joint_names is not None:
        asset_cfg.resolve(env.scene)
    joint_ids = asset_cfg.joint_ids

    joint_pos = asset.data.joint_pos[:, joint_ids]

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
    init_joint_pos = init_joint_pos[:, joint_ids]

    max_abs = torch.abs(joint_pos - init_joint_pos).max(dim=1).values
    return torch.clamp(max_abs / threshold_m, 0.0, 1.0)


def joint_open_fraction_reward(
    env: ManagerBasedRLEnv,
    close_angle_rad: float,
    open_angle_rad: float,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Reward joint opening as a normalized fraction between close and open angles."""
    asset: Articulation = env.scene[asset_cfg.name]
    joint_pos = asset.data.joint_pos[:, asset_cfg.joint_ids]
    max_pos = joint_pos.max(dim=1).values
    denom = open_angle_rad - close_angle_rad
    if abs(denom) < 1e-6:
        return torch.zeros(env.num_envs, device=env.device)
    fraction = (max_pos - close_angle_rad) / denom
    return torch.clamp(fraction, 0.0, 1.0)


def joint_range_progress(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Reward progress of joint position from lower to upper limits (uses max joint pos)."""
    asset: Articulation = env.scene[asset_cfg.name]
    joint_pos = asset.data.joint_pos[:, asset_cfg.joint_ids]
    lower = asset.data.joint_pos_limits[:, asset_cfg.joint_ids, 0]
    upper = asset.data.joint_pos_limits[:, asset_cfg.joint_ids, 1]
    denom = torch.clamp(upper - lower, min=1e-6)
    progress = (joint_pos - lower) / denom
    max_progress = progress.max(dim=1).values
    return torch.clamp(max_progress, 0.0, 1.0)


def joint_range_progress_from_init(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Reward progress of joint motion based on absolute delta from init over reachable range."""
    asset: Articulation = env.scene[asset_cfg.name]
    if isinstance(asset_cfg.joint_ids, slice) and asset_cfg.joint_ids == slice(None) and asset_cfg.joint_names is not None:
        asset_cfg.resolve(env.scene)
    joint_ids = asset_cfg.joint_ids

    joint_pos = asset.data.joint_pos[:, joint_ids]

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
    init_joint_pos = init_joint_pos[:, joint_ids]

    lower = asset.data.joint_pos_limits[:, joint_ids, 0]
    upper = asset.data.joint_pos_limits[:, joint_ids, 1]
    reachable = torch.maximum(init_joint_pos - lower, upper - init_joint_pos)
    denom = torch.clamp(reachable, min=1e-6)
    progress = torch.abs(joint_pos - init_joint_pos) / denom
    max_progress = progress.max(dim=1).values
    return torch.clamp(max_progress, 0.0, 1.0)
