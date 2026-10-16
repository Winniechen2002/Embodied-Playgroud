from __future__ import annotations

import torch

from isaaclab.controllers.differential_ik import DifferentialIKController
from isaaclab.controllers.differential_ik_cfg import DifferentialIKControllerCfg
from isaaclab.envs.mdp import reset_root_state_uniform as _reset_root_state_uniform
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils.math import (
    quat_from_euler_xyz,
    subtract_frame_transforms,
    quat_apply,
    quat_from_matrix,
    euler_xyz_from_quat,
    quat_mul,
)
from isaaclab.markers import VisualizationMarkers
from isaaclab.markers.config import FRAME_MARKER_CFG
import os
import numpy as np
import pickle 

def _get_or_create_frame_marker(env, key: str, frame_scale: tuple[float, float, float], prim_path: str):
    if not hasattr(env, "_reset_vis_markers"):
        env._reset_vis_markers = {}
    markers = env._reset_vis_markers
    if key not in markers:
        frame_marker_cfg = FRAME_MARKER_CFG.copy()
        frame_marker_cfg.markers["frame"].scale = frame_scale
        markers[key] = VisualizationMarkers(frame_marker_cfg.replace(prim_path=prim_path))
    return markers[key]

def reset_root_pose_uniform(
    env,
    env_ids: torch.Tensor,
    asset_cfg: SceneEntityCfg,
    pose_range: dict,
):
    """Reset root pose (position + orientation) without writing velocities.

    This is safe for kinematic / fixed-base articulations.
    pose_range values are treated as offsets from default_root_state.
    """
    asset = env.scene[asset_cfg.name]

    if isinstance(env_ids, slice):
        env_ids_t = torch.arange(env.num_envs, device=env.device, dtype=torch.long)
    else:
        env_ids_t = env_ids.to(device=env.device, dtype=torch.long)

    root_state = asset.data.default_root_state[env_ids_t].clone()  # (N, 13)
    num = env_ids_t.shape[0]

    # Translation offsets
    offsets = torch.zeros((num, 3), device=env.device)
    x_range = pose_range.get("x", (0.0, 0.0))
    y_range = pose_range.get("y", (0.0, 0.0))
    z_range = pose_range.get("z", (0.0, 0.0))
    offsets[:, 0].uniform_(x_range[0], x_range[1])
    offsets[:, 1].uniform_(y_range[0], y_range[1])
    offsets[:, 2].uniform_(z_range[0], z_range[1])
    root_state[:, 0:3] = root_state[:, 0:3] + env.scene.env_origins[env_ids_t] + offsets

    # Orientation offsets (roll/pitch/yaw)
    roll_range = pose_range.get("roll", (0.0, 0.0))
    pitch_range = pose_range.get("pitch", (0.0, 0.0))
    yaw_range = pose_range.get("yaw", (0.0, 0.0))
    euler = torch.zeros((num, 3), device=env.device)
    euler[:, 0].uniform_(roll_range[0], roll_range[1])
    euler[:, 1].uniform_(pitch_range[0], pitch_range[1])
    euler[:, 2].uniform_(yaw_range[0], yaw_range[1])
    delta_quat = quat_from_euler_xyz(euler[:, 0], euler[:, 1], euler[:, 2])
    root_state[:, 3:7] = quat_mul(root_state[:, 3:7], delta_quat)

    # Write pose only (no velocity)
    asset.write_root_pose_to_sim(root_state[:, 0:7], env_ids=env_ids_t)


def reset_object_extra(
    env,
    env_ids: torch.Tensor,
    object_name: str,
    pose_range: dict,
    velocity_range: dict | None = None,
):
    """Reset a rigid object by name using the standard root-state reset."""
    if velocity_range is None:
        velocity_range = {"x": (0.0, 0.0), "y": (0.0, 0.0), "z": (0.0, 0.0)}
    asset_cfg = SceneEntityCfg(object_name)
    _reset_root_state_uniform(env, env_ids, asset_cfg=asset_cfg, pose_range=pose_range, velocity_range=velocity_range)


def sync_object(
    env,
    env_ids: torch.Tensor,
    target_cfg: SceneEntityCfg,
    source_cfg: SceneEntityCfg,
    z_offset: float = 0.0,
    quat: tuple[float, float, float, float] | None = None,
):
    """Align target XY to source and set target Z offset and orientation."""
    target = env.scene[target_cfg.name]
    source = env.scene[source_cfg.name]

    if isinstance(env_ids, slice):
        env_ids_t = torch.arange(env.num_envs, device=env.device, dtype=torch.long)
    else:
        env_ids_t = env_ids.to(device=env.device, dtype=torch.long)

    pos = source.data.root_pos_w[env_ids_t].clone()
    pos[:, 2] = pos[:, 2] + z_offset

    if quat is None:
        quat_t = target.data.root_quat_w[env_ids_t]
    else:
        quat_t = torch.tensor(quat, device=env.device, dtype=pos.dtype).unsqueeze(0).repeat(env_ids_t.shape[0], 1)

    target.write_root_pose_to_sim(torch.cat([pos, quat_t], dim=1), env_ids=env_ids_t)

def reset_joints_to_pos(
    env,
    env_ids: torch.Tensor,
    joint_pos,
    joint_vel: float = 0.0,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
):
    """Reset joints to the given positions (clamped to limits)."""
    asset = env.scene[asset_cfg.name]

    if isinstance(asset_cfg.joint_ids, slice) and asset_cfg.joint_ids == slice(None) and asset_cfg.joint_names is not None:
        asset_cfg.resolve(env.scene)
    joint_ids = asset_cfg.joint_ids

    if isinstance(env_ids, slice):
        env_ids_t = torch.arange(env.num_envs, device=env.device, dtype=torch.long)
    else:
        env_ids_t = env_ids.to(device=env.device, dtype=torch.long)

    num_envs = env_ids_t.shape[0]
    num_joints = len(joint_ids) if not isinstance(joint_ids, slice) else asset.num_joints

    if torch.is_tensor(joint_pos):
        pos = joint_pos.to(device=env.device, dtype=torch.float32)
        if pos.ndim == 1:
            pos = pos.unsqueeze(0).repeat(num_envs, 1)
    elif isinstance(joint_pos, (list, tuple)):
        pos = torch.tensor(joint_pos, device=env.device, dtype=torch.float32).unsqueeze(0).repeat(num_envs, 1)
    else:
        pos = torch.full((num_envs, num_joints), float(joint_pos), device=env.device, dtype=torch.float32)

    vel = torch.full_like(pos, float(joint_vel))

    # clamp joint pos to limits
    joint_pos_limits = asset.data.soft_joint_pos_limits[env_ids_t, joint_ids]
    pos = pos.clamp_(joint_pos_limits[..., 0], joint_pos_limits[..., 1])

    asset.write_joint_state_to_sim(pos, vel, joint_ids=joint_ids, env_ids=env_ids_t)


def reset_joints_to_init(
    env,
    env_ids: torch.Tensor,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
):
    """Reset joints to init_state positions (fallback to default if not specified)."""
    asset = env.scene[asset_cfg.name]

    if isinstance(asset_cfg.joint_ids, slice) and asset_cfg.joint_ids == slice(None) and asset_cfg.joint_names is not None:
        asset_cfg.resolve(env.scene)
    joint_ids = asset_cfg.joint_ids

    if isinstance(env_ids, slice):
        env_ids_t = torch.arange(env.num_envs, device=env.device, dtype=torch.long)
    else:
        env_ids_t = env_ids.to(device=env.device, dtype=torch.long)

    joint_pos = asset.data.default_joint_pos[env_ids_t].clone()
    joint_vel = torch.zeros_like(joint_pos)

    init_joint_pos = getattr(asset.cfg.init_state, "joint_pos", None) or {}
    if init_joint_pos:
        name_to_id = {name: idx for idx, name in enumerate(asset.joint_names)}
        if isinstance(joint_ids, slice):
            target_ids = None
        else:
            if torch.is_tensor(joint_ids):
                target_ids = set(joint_ids.tolist())
            else:
                target_ids = set(joint_ids)
        for name, value in init_joint_pos.items():
            jid = name_to_id.get(name, None)
            if jid is None:
                continue
            if target_ids is not None and jid not in target_ids:
                continue
            joint_pos[:, jid] = float(value)

    joint_pos_limits = asset.data.soft_joint_pos_limits[env_ids_t]
    joint_pos = joint_pos.clamp_(joint_pos_limits[..., 0], joint_pos_limits[..., 1])

    if not isinstance(joint_ids, slice):
        joint_pos = joint_pos[:, joint_ids]
        joint_vel = joint_vel[:, joint_ids]

    asset.write_joint_state_to_sim(joint_pos, joint_vel, joint_ids=joint_ids, env_ids=env_ids_t)


def reset_robot_to_pose_ik(
    env,
    env_ids: torch.Tensor,
    resolved_scene_cfg: SceneEntityCfg,
    ik_method: str = "dls",
    max_time: float = 1.0,
    num_ik_iters: int = 10,
    visualize: bool = True,
    frame_scale: tuple[float, float, float] = (0.05, 0.05, 0.05),
    instant_set: bool = False,
    z_offset: float = 0.02,
    override_xyz: tuple[float, float, float] | None = None,
    override_quat: tuple[float, float, float, float] | None = None,
):
    # TODO: make this more efficient
    robot = env.scene[resolved_scene_cfg.name]
    
    # Ensure SceneEntityCfg is resolved (convert names to indices)
    # Check if resolution is needed by seeing if joint_ids/body_ids are still slices
    if isinstance(resolved_scene_cfg.joint_ids, slice) and resolved_scene_cfg.joint_ids == slice(None) and resolved_scene_cfg.joint_names is not None:
        resolved_scene_cfg.resolve(env.scene)
    if isinstance(resolved_scene_cfg.body_ids, slice) and resolved_scene_cfg.body_ids == slice(None) and resolved_scene_cfg.body_names is not None:
        resolved_scene_cfg.resolve(env.scene)
    
    # Handle body_ids which can be a list or slice
    body_ids = resolved_scene_cfg.body_ids
    if isinstance(body_ids, slice):
        # Convert slice to list (slice(None) means all bodies, so use first body)
        if body_ids == slice(None):
            body_id = 0  # Use first body
        else:
            # For other slices, convert to list and take first
            body_id = list(range(robot.num_bodies))[body_ids][0]
    else:
        # It's a list, take first element
        body_id = body_ids[0]
    
    # Resolve jacobian body index (see tutorial: fixed-base has one less body index)
    # For fixed-base robots, the base body (index 0) is not included in the jacobian computation
    # So we need to subtract 1 from the body index to get the correct jacobian index
    if robot.is_fixed_base:
        ee_jacobi_idx = body_id - 1
    else:
        ee_jacobi_idx = body_id
    
    # Joints to control
    joint_ids = resolved_scene_cfg.joint_ids

    ik_controller = DifferentialIKController(
        cfg=DifferentialIKControllerCfg(
            command_type="pose",
            use_relative_mode=False,
            ik_method=ik_method,
        ),
        num_envs=env.num_envs,
        device=env.device,
    )
    target_pos_w = torch.zeros(env.num_envs, 3, device=env.device, dtype=torch.float32)
    target_quat_w = torch.zeros(env.num_envs, 4, device=env.device, dtype=torch.float32)
    wrist_pos_rel: torch.Tensor = env._cached_wrist_pose_npz_simple["wrist_pos_rel"]  # (3,)
    wrist_rot_rel: torch.Tensor = env._cached_wrist_pose_npz_simple["wrist_rot_rel"]  # (3,3)
    obj = env.scene["object"]
    obj_pos_w = obj.data.root_pos_w  # (N,3)
    obj_quat_w = obj.data.root_quat_w  # (N,4)
    wrist_pos_rel_expand = wrist_pos_rel.unsqueeze(0).repeat(env.num_envs, 1)  # (N,3)
    wrist_quat_rel = wrist_rot_rel.unsqueeze(0).repeat(env.num_envs, 1)  # (N,4)
    # Map demo wrist orientation to robot wrist orientation (orientation only)
    demo2robot_R = torch.tensor([[[0.0, 0.0, 1.0],
                                    [0.0, -1.0, 0.0],
                                    [1.0, 0.0, 0.0]]], device=env.device, dtype=torch.float32)  # (1,3,3)
    q_map = quat_from_matrix(demo2robot_R).repeat(env.num_envs, 1)  # (N,4)
    wrist_quat_rel = quat_mul(wrist_quat_rel, q_map)
    wrist_pos_w = quat_apply(obj_quat_w, wrist_pos_rel_expand) + obj_pos_w
    # apply a small lift along world z-axis
    wrist_pos_w[:, 2] += float(z_offset)
    wrist_quat_w = quat_mul(obj_quat_w, wrist_quat_rel)
    target_pos_w[env_ids] = wrist_pos_w[env_ids]
    target_quat_w[env_ids] = wrist_quat_w[env_ids]

    root_pose_w = robot.data.root_pose_w  # [N, 7]
    root_pos_w = root_pose_w[:, 0:3]
    root_quat_w = root_pose_w[:, 3:7]
    target_pos_b, target_quat_b = subtract_frame_transforms(root_pos_w, root_quat_w, target_pos_w, target_quat_w)

    # Optional visualization markers (world-frame). Cache to avoid creating new prims every reset.
    ee_marker = None
    goal_marker = None
    if visualize:
        ee_marker = _get_or_create_frame_marker(env, "ee", frame_scale, "/Visuals/Reset/EE")
        goal_marker = _get_or_create_frame_marker(env, "goal", frame_scale, "/Visuals/Reset/Goal")

    # Prepare IK command buffer (7 for absolute pose: x y z qw qx qy qz)
    ik_cmds = torch.zeros(env.num_envs, ik_controller.action_dim, device=env.device, dtype=torch.float)
    # Fill only for env_ids; others remain zeros and will be set to no-op below each step
    # target_pos_b[:, 0] = -0.5
    # target_pos_b[:, 1] = 0.1
    # target_pos_b[:, 2] = 0.5
    ik_cmds[env_ids, 0:3] = target_pos_b[env_ids]
    ik_cmds[env_ids, 3:7] = target_quat_b[env_ids]
 
    # Normalize env ids tensor for consistent indexing and save object state before IK
    if isinstance(env_ids, slice):
        env_ids_t = torch.arange(env.num_envs, device=env.device, dtype=torch.long)
    elif isinstance(env_ids, torch.Tensor):
        env_ids_t = env_ids.to(device=env.device, dtype=torch.long)
    else:
        env_ids_t = torch.as_tensor(list(env_ids), device=env.device, dtype=torch.long)
    saved_obj_pose = torch.cat(
        [obj.data.root_pos_w[env_ids_t], obj.data.root_quat_w[env_ids_t]], dim=-1
    ).clone()  # (K,7)
    saved_obj_vel = torch.cat(
        [obj.data.root_lin_vel_w[env_ids_t], obj.data.root_ang_vel_w[env_ids_t]], dim=-1
    ).clone()  # (K,6)

    # before IK, reset the robot joints to default state
    default_joint_pos = robot.data.default_joint_pos[env_ids].clone()
    default_joint_vel = robot.data.default_joint_vel[env_ids].clone()
    robot.write_joint_state_to_sim(default_joint_pos, default_joint_vel, env_ids=env_ids)
    env.scene.write_data_to_sim()
    env.sim.step()
    env.scene.update(dt=env.physics_dt)

    if instant_set:
        # Current EE pose and jacobian
        # Optimized: reduce iterations (now 3 instead of 10) - most IK convergence happens in first few iterations
        # NOTE: sim.step() steps ALL environments, not just env_ids. This is a simulator limitation.
        # Non-resetting environments will advance in time, but their joint states are not modified.
        for i in range(num_ik_iters):
            jacobian = robot.root_physx_view.get_jacobians()[:, ee_jacobi_idx, :, joint_ids]
            ee_pose_w = robot.data.body_pose_w[:, body_id]  # [N, 7]
            root_pose_w = robot.data.root_pose_w
            joint_pos = robot.data.joint_pos[:, joint_ids]
            # EE pose in base frame
            ee_pos_b, ee_quat_b = subtract_frame_transforms(
                root_pose_w[:, 0:3], root_pose_w[:, 3:7], ee_pose_w[:, 0:3], ee_pose_w[:, 3:7]
            )
            # Compute single-shot IK and write state
            ik_controller.set_command(ik_cmds)
            joint_pos_des = ik_controller.compute(ee_pos_b, ee_quat_b, jacobian, joint_pos)
            joint_vel_full = torch.zeros_like(joint_pos_des)
            # Only modify joint states for environments being reset
            joint_pos_des = joint_pos_des[env_ids, ...]
            joint_vel_full = joint_vel_full[env_ids, ...] 
            robot.write_joint_state_to_sim(joint_pos_des, joint_vel_full, env_ids=env_ids, joint_ids=joint_ids)
            env.scene.write_data_to_sim()
            # WARNING: This steps ALL environments, not just env_ids. Non-resetting envs advance in time.
            env.sim.step()
            env.scene.update(dt=env.physics_dt)
            if visualize and ee_marker is not None and goal_marker is not None:
                ee_marker.visualize(ee_pose_w[:, 0:3], ee_pose_w[:, 3:7])
                goal_marker.visualize(target_pos_w, target_quat_w)
        
        # Restore object to its saved pose/velocity (preserve randomized placement)
        obj.write_root_pose_to_sim(saved_obj_pose, env_ids=env_ids_t)
        obj.write_root_velocity_to_sim(saved_obj_vel, env_ids=env_ids_t)
        
        # Get final joint positions after IK (from last iteration)
        final_joint_pos = robot.data.joint_pos[env_ids_t].clone()
        final_joint_vel = torch.zeros_like(final_joint_pos)
        
        # Reset finger joints to their default positions to remove IK disturbances
        num_total_joints = robot.data.joint_pos.shape[1]
        if isinstance(joint_ids, slice):
            hand_joint_ids_list = []
        else:
            all_indices = torch.arange(num_total_joints, device=env.device, dtype=torch.long)
            arm_mask = torch.zeros(num_total_joints, dtype=torch.bool, device=env.device)
            arm_mask[joint_ids] = True
            hand_joint_ids = all_indices[~arm_mask]
            hand_joint_ids_list = hand_joint_ids.tolist()
        if len(hand_joint_ids_list) > 0:
            default_hand_pos = robot.data.default_joint_pos[env_ids_t][:, hand_joint_ids_list].clone()
            default_hand_vel = torch.zeros_like(default_hand_pos)
            final_joint_pos[:, hand_joint_ids_list] = default_hand_pos
            final_joint_vel[:, hand_joint_ids_list] = default_hand_vel
        
        # Write final joint state (arm + hand) to ensure everything is set correctly
        robot.write_joint_state_to_sim(final_joint_pos, final_joint_vel, env_ids=env_ids_t)
        
        # Clear any residual joint targets and forces to prevent unwanted motion
        # Reset actuators and clear external forces/torques
        robot.reset(env_ids=env_ids_t)
        # Set position targets to current positions (so PD controller holds them)
        robot.set_joint_position_target(final_joint_pos, env_ids=env_ids_t)
        # Set velocity targets to zero
        robot.set_joint_velocity_target(final_joint_vel, env_ids=env_ids_t)
        # Zero out any effort/torque targets
        zero_efforts = torch.zeros_like(final_joint_pos)
        robot.set_joint_effort_target(zero_efforts, env_ids=env_ids_t)
        
        # Write all data to sim and do a final step to ensure physics is settled
        # WARNING: This steps ALL environments, not just env_ids. Non-resetting envs advance in time.
        env.scene.write_data_to_sim()
        env.sim.step()
        env.scene.update(dt=env.physics_dt)
    else: 
        # Drive over time using joint position targets
        physics_dt = env.physics_dt
        sim_time = 0.0
        while sim_time < max_time:
            # Current EE pose and jacobian
            jacobian = robot.root_physx_view.get_jacobians()[:, ee_jacobi_idx, :, joint_ids]
            ee_pose_w = robot.data.body_pose_w[:, body_id]  # [N, 7]
            root_pose_w = robot.data.root_pose_w
            joint_pos = robot.data.joint_pos[:, joint_ids]
            # EE pose in base frame
            ee_pos_b, ee_quat_b = subtract_frame_transforms(
                root_pose_w[:, 0:3], root_pose_w[:, 3:7], ee_pose_w[:, 0:3], ee_pose_w[:, 3:7]
            )
            # For non-target envs, set command to current so they no-op
            not_env_mask = torch.ones(env.num_envs, dtype=torch.bool, device=env.device)
            not_env_mask[env_ids] = False
            if not_env_mask.any():
                ik_cmds[not_env_mask, 0:3] = ee_pos_b[not_env_mask]
                ik_cmds[not_env_mask, 3:7] = ee_quat_b[not_env_mask]
            # Compute IK and set joint position targets for selected envs
            ik_controller.set_command(ik_cmds)
            joint_pos_des = ik_controller.compute(ee_pos_b, ee_quat_b, jacobian, joint_pos)
            robot.set_joint_position_target(joint_pos_des[env_ids], joint_ids=joint_ids, env_ids=env_ids)
            env.scene.write_data_to_sim()
            env.sim.step()
            env.scene.update(dt=physics_dt)
            sim_time += physics_dt
            # visualize frames (world)
            if visualize and ee_marker is not None and goal_marker is not None:
                ee_marker.visualize(ee_pose_w[:, 0:3], ee_pose_w[:, 3:7])
                goal_marker.visualize(target_pos_w, target_quat_w)
        # Zero velocities for affected envs to avoid residual motion
        joint_pos_cur = robot.data.joint_pos[env_ids_t].clone()
        joint_vel_cur = robot.data.joint_vel[env_ids_t].clone()
        joint_vel_cur[:, :] = 0.0
        robot.write_joint_state_to_sim(joint_pos_cur, joint_vel_cur, env_ids=env_ids_t)
        # Restore object to its saved pose/velocity (preserve randomized placement)
        obj.write_root_pose_to_sim(saved_obj_pose, env_ids=env_ids_t)
        obj.write_root_velocity_to_sim(saved_obj_vel, env_ids=env_ids_t)
        # Reset finger joints to their default positions to remove IK disturbances
        num_total_joints = robot.data.joint_pos.shape[1]
        if isinstance(joint_ids, slice):
            hand_joint_ids_list = []
        else:
            all_indices = torch.arange(num_total_joints, device=env.device, dtype=torch.long)
            arm_mask = torch.zeros(num_total_joints, dtype=torch.bool, device=env.device)
            arm_mask[joint_ids] = True
            hand_joint_ids = all_indices[~arm_mask]
            hand_joint_ids_list = hand_joint_ids.tolist()
        if len(hand_joint_ids_list) > 0:
            default_hand_pos = robot.data.default_joint_pos[env_ids_t][:, hand_joint_ids_list].clone()
            default_hand_vel = torch.zeros_like(default_hand_pos)
            robot.write_joint_state_to_sim(default_hand_pos, default_hand_vel, env_ids=env_ids_t, joint_ids=hand_joint_ids_list)


def reset_robot_to_position_ik(
    env,
    env_ids: torch.Tensor,
    resolved_scene_cfg: SceneEntityCfg,
    relative_offset: tuple[float, float, float] = (0.0, 0.0, 0.0),
    ik_method: str = "dls",
    num_ik_iters: int = 5,
    # visualize: bool = False,
    # frame_scale: tuple[float, float, float] = (0.05, 0.05, 0.05),
):
    """Simplified IK reset that only controls end-effector position (not orientation).
    
    This function:
    1. Resets robot to default joint positions
    2. Gets the default end-effector position
    3. Applies a relative offset (dx, dy, dz) to the default position
    4. Uses IK to drive the robot to the target position while keeping current orientation
    
    Args:
        env: The environment.
        env_ids: Environment IDs to reset.
        resolved_scene_cfg: Scene entity configuration for the robot (must specify joint_names and body_names).
        relative_offset: Relative translation (dx, dy, dz) in meters relative to default end-effector position.
        ik_method: IK method to use ("dls", "pinv", "svd", "trans"). Defaults to "dls".
        num_ik_iters: Number of IK iterations. Defaults to 5.
        visualize: Whether to visualize the target position. Defaults to False.
        frame_scale: Scale of visualization markers. Defaults to (0.05, 0.05, 0.05).
    """
    robot = env.scene[resolved_scene_cfg.name]
    # Handle body_ids which can be a list or slice
    body_id = resolved_scene_cfg.body_ids[0]
    # Resolve jacobian body index (fixed-base has one less body index)
    if robot.is_fixed_base:
        ee_jacobi_idx = body_id - 1
    else:
        ee_jacobi_idx = body_id
    
    # Joints to control
    joint_ids = resolved_scene_cfg.joint_ids
    
    # Step 1: Reset robot to default joint positions
    default_joint_pos = robot.data.default_joint_pos[env_ids].clone()
    default_joint_vel = robot.data.default_joint_vel[env_ids].clone()
    robot.write_joint_state_to_sim(default_joint_pos, default_joint_vel, env_ids=env_ids)
    env.scene.write_data_to_sim()
    env.sim.step()
    env.scene.update(dt=env.physics_dt)
    
    # Step 2: Get default end-effector position (after reset to default joints)
    ee_pose_w = robot.data.body_pose_w[:, body_id]  # [N, 7]
    # default_ee_pos_w = ee_pose_w[:, 0:3].clone()  # [N, 3]
    # default_ee_quat_w = ee_pose_w[:, 3:7].clone()  # [N, 4] - keep current orientation
    
    # Step 3: Apply relative offset to get target position
    relative_offset_tensor = torch.tensor(relative_offset, device=env.device, dtype=torch.float32)
    # target_pos_w = default_ee_pos_w.clone()
    # target_pos_w[env_ids] = default_ee_pos_w[env_ids] + relative_offset_tensor.unsqueeze(0)
    
    # Step 4: Convert target position to base frame for IK
    root_pose_w = robot.data.root_pose_w
    root_pos_w = root_pose_w[:, 0:3]
    root_quat_w = root_pose_w[:, 3:7]
    # target_pos_b, _ = subtract_frame_transforms(root_pos_w, root_quat_w, target_pos_w, None)
    
    # Step 5: Initialize IK controller for position-only control
    ik_controller = DifferentialIKController(
        cfg=DifferentialIKControllerCfg(
            command_type="position",
            use_relative_mode=True,  # Use relative mode for position offset
            ik_method=ik_method,
        ),
        num_envs=env.num_envs,
        device=env.device,
    )
    
    # Optional visualization
    # goal_marker = None
    # if visualize:
    #     goal_marker = _get_or_create_frame_marker(env, "goal", frame_scale, "/Visuals/Reset/GoalPosition")
    
    # Step 6: Iteratively solve IK to reach target position
    for i in range(num_ik_iters):
        # Get current end-effector pose
        ee_pose_w = robot.data.body_pose_w[:, body_id]  # [N, 7]
        ee_pos_w = ee_pose_w[:, 0:3]
        ee_quat_w = ee_pose_w[:, 3:7]
        
        # Convert to base frame
        ee_pos_b, ee_quat_b = subtract_frame_transforms(
            root_pos_w, root_quat_w, ee_pos_w, ee_quat_w
        )
        # # Compute relative position command (target - current)
        # # Only compute delta for resetting environments, others get zero command
        # relative_pos_cmd = torch.zeros(env.num_envs, 3, device=env.device, dtype=torch.float32)
        # relative_pos_cmd[env_ids_t] = target_pos_b[env_ids_t] - ee_pos_b[env_ids_t]  # [K, 3]
        relative_pos_cmd = relative_offset_tensor.unsqueeze(0)
        
        # Set command in controller (needs current pose for relative mode)
        ik_controller.set_command(relative_pos_cmd, ee_pos_b, ee_quat_b)
        
        # Get jacobian and current joint positions
        jacobian = robot.root_physx_view.get_jacobians()[:, ee_jacobi_idx, :, joint_ids]
        joint_pos = robot.data.joint_pos[:, joint_ids]
        
        # Compute IK solution
        joint_pos_des = ik_controller.compute(ee_pos_b, ee_quat_b, jacobian, joint_pos)
        
        # Apply joint positions (only for env_ids)
        joint_pos_des = joint_pos_des[env_ids]
        joint_vel_des = torch.zeros_like(joint_pos_des)
        robot.write_joint_state_to_sim(joint_pos_des, joint_vel_des, env_ids=env_ids, joint_ids=joint_ids)
        
        # Step simulation
        env.scene.write_data_to_sim()
        env.sim.step()
        env.scene.update(dt=env.physics_dt)
        
        # Visualize target position
        # if visualize and goal_marker is not None:
        #     goal_marker.visualize(target_pos_w, default_ee_quat_w)
    
    # Step 7: Finalize - set joint targets and zero velocities
    final_joint_pos = robot.data.joint_pos[env_ids].clone()
    final_joint_vel = torch.zeros_like(final_joint_pos)
    robot.write_joint_state_to_sim(final_joint_pos, final_joint_vel, env_ids=env_ids)
    
    # Reset actuators and set position targets to hold current pose
    robot.reset(env_ids=env_ids)
    robot.set_joint_position_target(final_joint_pos, env_ids=env_ids)
    robot.set_joint_velocity_target(final_joint_vel, env_ids=env_ids)
    
    # Final simulation step
    env.scene.write_data_to_sim()
    env.sim.step()
    env.scene.update(dt=env.physics_dt)
# def reset_robot_to_pose_ik(
#     env,
#     env_ids: torch.Tensor,
#     resolved_scene_cfg: SceneEntityCfg,
#     target_pos=(-0.7, 0.0, 0.5),
#     target_rot_euler=(0.0, 0.0, 0.0),
#     ik_method: str = "dls",
#     max_time: float = 2.0,
#     num_ik_iters: int = 10,
#     reset_to_default_first: bool = True,
#     random_pos_range: tuple[float, float] = (0.0, 0.0),
#     random_quat_range: tuple[float, float, float] = (0.0, 0.0, 0.0),
#     visualize: bool = False,
#     frame_scale: tuple[float, float, float] = (0.05, 0.05, 0.05),
#     use_cached_wrist_targets: bool = True,
#     instant_set: bool = True,
# ):
#     # TODO: make this more efficient
#     robot = env.scene[resolved_scene_cfg.name]
#     # Resolve jacobian body index (see tutorial: fixed-base has one less body index)
#     if robot.is_fixed_base:
#         ee_jacobi_idx = resolved_scene_cfg.body_ids[0] - 1
#     else:
#         ee_jacobi_idx = resolved_scene_cfg.body_ids[0]

#     # Joints to control
#     joint_ids = resolved_scene_cfg.joint_ids

#     # Optionally reset robot joints to default state before IK
#     if reset_to_default_first:
#         default_joint_pos = robot.data.default_joint_pos[env_ids].clone()
#         default_joint_vel = robot.data.default_joint_vel[env_ids].clone()
#         robot.write_joint_state_to_sim(default_joint_pos, default_joint_vel, env_ids=env_ids)
#         env.scene.write_data_to_sim()
#         env.sim.step()
#         env.scene.update(dt=env.physics_dt)

#     ik_controller = DifferentialIKController(
#         cfg=DifferentialIKControllerCfg(
#             command_type="pose",
#             use_relative_mode=False,
#             ik_method=ik_method,
#         ),
#         num_envs=env.num_envs,
#         device=env.device,
#     )
#     target_pos_w = torch.zeros(env.num_envs, 3, device=env.device, dtype=torch.float)
#     target_quat_w = torch.zeros(env.num_envs, 4, device=env.device, dtype=torch.float)
#     # If available, override targets from cached wrist info.
#     if use_cached_wrist_targets:
#         # Highest priority: precomputed world-frame targets from a prior event
#         if hasattr(env, "_reset_targets"):
#             if "wrist_pos_w" in env._reset_targets and "wrist_quat_w" in env._reset_targets:
#                 target_pos_w[env_ids] = env._reset_targets["wrist_pos_w"][env_ids]
#                 target_quat_w[env_ids] = env._reset_targets["wrist_quat_w"][env_ids]
#         # Fallback: object-frame wrist pose cached from dataset; transform to world using current object pose
#         elif hasattr(env, "_cached_wrist_pose_npz") and "wrist_pos_rel" in env._cached_wrist_pose_npz and "wrist_rot_rel" in env._cached_wrist_pose_npz:
#             wrist_pos_rel: torch.Tensor = env._cached_wrist_pose_npz["wrist_pos_rel"]  # (3,)
#             wrist_rot_rel: torch.Tensor = env._cached_wrist_pose_npz["wrist_rot_rel"]  # (3,3)
#             obj = env.scene["object"]
#             obj_pos_w = obj.data.root_pos_w  # (N,3)
#             obj_quat_w = obj.data.root_quat_w  # (N,4)
#             wrist_pos_rel_expand = wrist_pos_rel.unsqueeze(0).repeat(env.num_envs, 1)  # (N,3)
#             wrist_quat_rel = quat_from_matrix(wrist_rot_rel.unsqueeze(0)).repeat(env.num_envs, 1)  # (N,4)
#             # Map demo wrist orientation to robot wrist orientation (orientation only)
#             demo2robot_R = torch.tensor([[[0.0, 0.0, 1.0],
#                                           [0.0, 1.0, 0.0],
#                                           [-1.0, 0.0, 0.0]]], device=env.device, dtype=torch.float32).T  # (1,3,3)
#             q_map = quat_from_matrix(demo2robot_R).repeat(env.num_envs, 1)  # (N,4)
#             wrist_quat_rel = quat_mul(wrist_quat_rel, q_map)
#             wrist_pos_w = quat_apply(obj_quat_w, wrist_pos_rel_expand) + obj_pos_w
#             wrist_quat_w = quat_mul(obj_quat_w, wrist_quat_rel)
#             target_pos_w[env_ids] = wrist_pos_w[env_ids]
#             target_quat_w[env_ids] = wrist_quat_w[env_ids]

#     else:
#         # Build noisy targets in world frame
#         target_pos = torch.as_tensor(target_pos, device=env.device, dtype=torch.float)
#         target_euler = torch.as_tensor(target_rot_euler, device=env.device, dtype=torch.float)
#         # position noise (same range per axis)
#         pos_min, pos_max = float(random_pos_range[0]), float(random_pos_range[1])
#         pos_noise = torch.zeros(env.num_envs, 3, device=env.device, dtype=torch.float)
#         if pos_max > pos_min:
#             pos_noise.uniform_(pos_min, pos_max)
#         target_pos_w = target_pos.unsqueeze(0).repeat(env.num_envs, 1) + pos_noise
#         # orientation noise in euler (roll, pitch, yaw), symmetric [-r, r] per axis
#         rx, ry, rz = [float(v) for v in random_quat_range]
#         euler_noise = torch.zeros(env.num_envs, 3, device=env.device, dtype=torch.float)
#         if rx != 0.0 or ry != 0.0 or rz != 0.0:
#             euler_noise[:, 0].uniform_(-rx, rx)
#             euler_noise[:, 1].uniform_(-ry, ry)
#             euler_noise[:, 2].uniform_(-rz, rz)
#         target_euler_w = target_euler.unsqueeze(0).repeat(env.num_envs, 1) + euler_noise
#         target_quat_w = quat_from_euler_xyz(target_euler_w[:, 0], target_euler_w[:, 1], target_euler_w[:, 2])

#     # Convert desired world-frame targets to base-frame targets
#     root_pose_w = robot.data.root_pose_w  # [N, 7]
#     root_pos_w = root_pose_w[:, 0:3]
#     root_quat_w = root_pose_w[:, 3:7]
#     target_pos_b, target_quat_b = subtract_frame_transforms(root_pos_w, root_quat_w, target_pos_w, target_quat_w)

#     # Optional visualization markers (world-frame). Cache to avoid creating new prims every reset.
#     ee_marker = None
#     goal_marker = None
#     if visualize:
#         ee_marker = _get_or_create_frame_marker(env, "ee", frame_scale, "/Visuals/Reset/EE")
#         goal_marker = _get_or_create_frame_marker(env, "goal", frame_scale, "/Visuals/Reset/Goal")

#     # Prepare IK command buffer (7 for absolute pose: x y z qw qx qy qz)
#     ik_cmds = torch.zeros(env.num_envs, ik_controller.action_dim, device=env.device, dtype=torch.float)
#     # Fill only for env_ids; others remain zeros and will be set to no-op below each step
#     ik_cmds[env_ids, 0:3] = target_pos_b[env_ids]
#     ik_cmds[env_ids, 3:7] = target_quat_b[env_ids]

#     # Branch: instant set (one-shot) vs. drive over time using joint targets
#     if instant_set:
#         # Current EE pose and jacobian
#         jacobian = robot.root_physx_view.get_jacobians()[:, ee_jacobi_idx, :, joint_ids]
#         ee_pose_w = robot.data.body_pose_w[:, resolved_scene_cfg.body_ids[0]]  # [N, 7]
#         root_pose_w = robot.data.root_pose_w
#         joint_pos = robot.data.joint_pos[:, joint_ids]
#         # EE pose in base frame
#         ee_pos_b, ee_quat_b = subtract_frame_transforms(
#             root_pose_w[:, 0:3], root_pose_w[:, 3:7], ee_pose_w[:, 0:3], ee_pose_w[:, 3:7]
#         )
#         # Compute single-shot IK and write state
#         ik_controller.set_command(ik_cmds)
#         joint_pos_des = ik_controller.compute(ee_pos_b, ee_quat_b, jacobian, joint_pos)
#         joint_pos_full = robot.data.joint_pos.clone()
#         joint_vel_full = robot.data.joint_vel.clone()
#         joint_pos_full[env_ids[:, None], joint_ids] = joint_pos_des[env_ids]
#         joint_vel_full[env_ids, :] = 0.0
#         robot.write_joint_state_to_sim(joint_pos_full, joint_vel_full, env_ids=None)
#         env.scene.write_data_to_sim()
#         env.sim.step()
#         env.scene.update(dt=env.physics_dt)
#         if visualize and ee_marker is not None and goal_marker is not None:
#             ee_marker.visualize(ee_pose_w[:, 0:3], ee_pose_w[:, 3:7])
#             goal_marker.visualize(target_pos_w, target_quat_w)
#         # Ensure selected envs have zero velocities after the snap
#         joint_pos_cur = robot.data.joint_pos.clone()
#         joint_vel_cur = robot.data.joint_vel.clone()
#         joint_vel_cur[env_ids, :] = 0.0
#         robot.write_joint_state_to_sim(joint_pos_cur, joint_vel_cur, env_ids=env_ids)
#         return
#     else:
#         # Drive over time using joint position targets
#         physics_dt = env.physics_dt
#         sim_time = 0.0
#         while sim_time < max_time:
#             # Current EE pose and jacobian
#             jacobian = robot.root_physx_view.get_jacobians()[:, ee_jacobi_idx, :, joint_ids]
#             ee_pose_w = robot.data.body_pose_w[:, resolved_scene_cfg.body_ids[0]]  # [N, 7]
#             root_pose_w = robot.data.root_pose_w
#             joint_pos = robot.data.joint_pos[:, joint_ids]
#             # EE pose in base frame
#             ee_pos_b, ee_quat_b = subtract_frame_transforms(
#                 root_pose_w[:, 0:3], root_pose_w[:, 3:7], ee_pose_w[:, 0:3], ee_pose_w[:, 3:7]
#             )
#             # For non-target envs, set command to current so they no-op
#             not_env_mask = torch.ones(env.num_envs, dtype=torch.bool, device=env.device)
#             not_env_mask[env_ids] = False
#             if not_env_mask.any():
#                 ik_cmds[not_env_mask, 0:3] = ee_pos_b[not_env_mask]
#                 ik_cmds[not_env_mask, 3:7] = ee_quat_b[not_env_mask]
#             # Compute IK and set joint targets for selected envs
#             ik_controller.set_command(ik_cmds)
#             joint_pos_des = ik_controller.compute(ee_pos_b, ee_quat_b, jacobian, joint_pos)
#             robot.set_joint_position_target(joint_pos_des[env_ids], joint_ids=joint_ids, env_ids=env_ids)
#             env.scene.write_data_to_sim()
#             env.sim.step()
#             env.scene.update(dt=physics_dt)
#             sim_time += physics_dt
#             # visualize frames (world)
#             if visualize and ee_marker is not None and goal_marker is not None:
#                 ee_marker.visualize(ee_pose_w[:, 0:3], ee_pose_w[:, 3:7])
#                 goal_marker.visualize(target_pos_w, target_quat_w)

#     # Zero velocities for affected envs to avoid residual motion
#     joint_pos = robot.data.joint_pos.clone()
#     joint_vel = robot.data.joint_vel.clone()
#     joint_vel[env_ids, :] = 0.0
#     robot.write_joint_state_to_sim(joint_pos, joint_vel, env_ids=env_ids)

    # also reset the allegro hand
 
def visualize_wrist_pose_from_file_simple(
    env,
    env_ids: torch.Tensor,
    resolved_scene_cfg: SceneEntityCfg,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    file_path: str = "",
    points_key: str = "relative_points",
    wrist_rot_key: str = "relative_wrist_rot",
    visualize: bool = True,
    frame_scale: tuple[float, float, float] = (0.1, 0.1, 0.1),
):
    """
    Simple reset event: load wrist pose in object frame, transform to world via current object pose,
    compute wrist pose in robot base frame, and visualize frame(s).
    """
    # load and cache file
    if not hasattr(env, "_cached_wrist_pose_npz_simple") or env._cached_wrist_pose_npz_simple.get("file", "") != file_path:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        if file_path.endswith(".npz"):
            data = np.load(file_path)
        elif file_path.endswith(".pkl"):
            with open(file_path, "rb") as f:
                data = pickle.load(f)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
        if points_key not in data or wrist_rot_key not in data:
            raise KeyError(
                f"Required keys not in npz. Have: {list(data.keys())}, need: '{points_key}', '{wrist_rot_key}'"
            )
        env._cached_wrist_pose_npz_simple = {
            "file": file_path,
            "wrist_pos_rel": torch.tensor(data[points_key], dtype=torch.float32, device=env.device),  # (3,)
            "wrist_rot_rel": torch.tensor(data[wrist_rot_key], dtype=torch.float32, device=env.device),  # (3,3)
        }
    wrist_pos_rel: torch.Tensor = env._cached_wrist_pose_npz_simple["wrist_pos_rel"]
    wrist_rot_rel: torch.Tensor = env._cached_wrist_pose_npz_simple["wrist_rot_rel"]

    # scene references
    obj = env.scene[object_cfg.name]
    robot = env.scene[resolved_scene_cfg.name]

    # expand to all envs and compose to world
    wrist_pos_rel_expand = wrist_pos_rel.unsqueeze(0).repeat(env.num_envs, 1)  # (N,3)
    # Convert rotation matrix (3x3) to quaternion (4,)
    # wrist_rot_rel is already a tensor from the cache, but check its shape
    if isinstance(wrist_rot_rel, torch.Tensor):
        wrist_rot_rel_shape = wrist_rot_rel.shape
    else:
        wrist_rot_rel_shape = np.array(wrist_rot_rel).shape
        wrist_rot_rel = torch.tensor(wrist_rot_rel, dtype=torch.float32, device=env.device)
    
    if wrist_rot_rel_shape == (3, 3):
        # It's a rotation matrix, convert to quaternion
        wrist_rot_rel_tensor = wrist_rot_rel.unsqueeze(0) if wrist_rot_rel.dim() == 2 else wrist_rot_rel  # (1, 3, 3) or (3, 3)
        if wrist_rot_rel_tensor.dim() == 2:
            wrist_rot_rel_tensor = wrist_rot_rel_tensor.unsqueeze(0)  # (1, 3, 3)
        wrist_quat_rel = quat_from_matrix(wrist_rot_rel_tensor).repeat(env.num_envs, 1)  # (N, 4)
    else:
        # Already a quaternion or different format
        if wrist_rot_rel.dim() == 1:
            wrist_quat_rel = wrist_rot_rel.unsqueeze(0).repeat(env.num_envs, 1)  # (N, 4)
        elif wrist_rot_rel.shape[0] != env.num_envs:
            wrist_quat_rel = wrist_rot_rel.unsqueeze(0).repeat(env.num_envs, 1)  # (N, 4)
        else:
            wrist_quat_rel = wrist_rot_rel
    obj_pos_w = obj.data.root_pos_w
    obj_quat_w = obj.data.root_quat_w
    wrist_pos_w = quat_apply(obj_quat_w, wrist_pos_rel_expand) + obj_pos_w
    wrist_quat_w = quat_mul(obj_quat_w, wrist_quat_rel)
    # convert to base frame (for logging / debug)
    root_pose_w = robot.data.root_pose_w
    root_pos_w = root_pose_w[:, 0:3]
    root_quat_w = root_pose_w[:, 3:7]
    wrist_pos_b, wrist_quat_b = subtract_frame_transforms(root_pos_w, root_quat_w, wrist_pos_w, wrist_quat_w)

    # Get actual robot end-effector link pose for visualization
    # Try common end-effector link names (order matters - try most specific first)
    ee_link_body_ids = []
    ee_link_names = []
    ee_body_candidates = ["palm_link", ".*ee.*", ".*wrist.*", ".*end.*effector.*"]
    
    for candidate in ee_body_candidates:
        try:
            candidate_ids, candidate_names = robot.find_bodies(candidate)
            if len(candidate_ids) > 0:
                ee_link_body_ids = candidate_ids
                ee_link_names = candidate_names
                break
        except ValueError:
            # Pattern didn't match, try next candidate
            continue
    
    if len(ee_link_body_ids) > 0:
        ee_body_id = ee_link_body_ids[0]
        ee_pose_w = robot.data.body_pose_w[:, ee_body_id]  # [N, 7]
        ee_pos_w = ee_pose_w[:, 0:3]
        ee_quat_w = ee_pose_w[:, 3:7]
        # Transform to base frame for visualization
        ee_pos_b, ee_quat_b = subtract_frame_transforms(root_pos_w, root_quat_w, ee_pos_w, ee_quat_w)
    else:
        # Fallback: use root pose if no end-effector link found
        ee_pos_b = root_pos_w
        ee_quat_b = root_quat_w

    # visualize one frame per env at the world pose and the object frame
    if visualize:
        wrist_marker = _get_or_create_frame_marker(env, "wrist_simple", frame_scale, "/Visuals/Reset/WristSimple")
        wrist_marker.visualize(translations=wrist_pos_b, orientations=wrist_quat_b)
        # Visualize actual robot ee_link pose
        ee_marker = _get_or_create_frame_marker(env, "ee_link_actual", frame_scale, "/Visuals/Reset/EEActual")
        ee_marker.visualize(translations=ee_pos_b, orientations=ee_quat_b)
        # obj_marker = _get_or_create_frame_marker(env, "object", frame_scale, "/Visuals/Reset/Object")
        # obj_marker.visualize(translations=obj_pos_w, orientations=obj_quat_w)

    # Store per-env wrist targets for later IK reset usage
    if isinstance(env_ids, slice):
        env_ids_t = torch.arange(env.num_envs, device=env.device, dtype=torch.long)
    elif isinstance(env_ids, torch.Tensor):
        env_ids_t = env_ids.to(device=env.device, dtype=torch.long)
    else:
        env_ids_t = torch.as_tensor(list(env_ids), device=env.device, dtype=torch.long)
    if not hasattr(env, "_reset_targets"):
        env._reset_targets = {}
        env._reset_targets["wrist_pos_w"] = torch.zeros(env.num_envs, 3, device=env.device, dtype=torch.float32)
        env._reset_targets["wrist_quat_w"] = torch.zeros(env.num_envs, 4, device=env.device, dtype=torch.float32)
    if "wrist_pos_w" not in env._reset_targets or env._reset_targets["wrist_pos_w"].shape[0] != env.num_envs:
        env._reset_targets["wrist_pos_w"] = torch.zeros(env.num_envs, 3, device=env.device, dtype=torch.float32)
    if "wrist_quat_w" not in env._reset_targets or env._reset_targets["wrist_quat_w"].shape[0] != env.num_envs:
        env._reset_targets["wrist_quat_w"] = torch.zeros(env.num_envs, 4, device=env.device, dtype=torch.float32)
    env._reset_targets["wrist_pos_w"][env_ids_t] = wrist_pos_w[env_ids_t]
    env._reset_targets["wrist_quat_w"][env_ids_t] = wrist_quat_w[env_ids_t]
    
