# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import os
import numpy as np
import torch
from typing import TYPE_CHECKING

from isaaclab.assets import Articulation, RigidObject
from isaaclab.managers import ManagerTermBase, SceneEntityCfg
from isaaclab.utils.math import (
    normalize,
    quat_apply,
    quat_apply_inverse,
    quat_from_angle_axis,
    quat_inv,
    quat_mul,
    subtract_frame_transforms,
)

from .utils import sample_object_point_cloud
import pickle
from pathlib import Path

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


def object_pos_b(
    env: ManagerBasedRLEnv,
    robot_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
):
    """Object position in the robot's root frame.

    Args:
        env: The environment.
        robot_cfg: Scene entity for the robot (reference frame). Defaults to ``SceneEntityCfg("robot")``.
        object_cfg: Scene entity for the object. Defaults to ``SceneEntityCfg("object")``.

    Returns:
        Tensor of shape ``(num_envs, 3)``: object position [x, y, z] expressed in the robot root frame.
    """
    robot: RigidObject = env.scene[robot_cfg.name]
    object: RigidObject = env.scene[object_cfg.name]
    return quat_apply_inverse(robot.data.root_quat_w, object.data.root_pos_w - robot.data.root_pos_w)


def object_quat_b(
    env: ManagerBasedRLEnv,
    robot_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Object orientation in the robot's root frame.

    Args:
        env: The environment.
        robot_cfg: Scene entity for the robot (reference frame). Defaults to ``SceneEntityCfg("robot")``.
        object_cfg: Scene entity for the object. Defaults to ``SceneEntityCfg("object")``.

    Returns:
        Tensor of shape ``(num_envs, 4)``: object quaternion ``(w, x, y, z)`` in the robot root frame.
    """
    robot: RigidObject = env.scene[robot_cfg.name]
    object: RigidObject = env.scene[object_cfg.name]
    return quat_mul(quat_inv(robot.data.root_quat_w), object.data.root_quat_w)


def object_up_b(
    env: ManagerBasedRLEnv,
    robot_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Object local +Z axis expressed in the robot's root frame."""
    robot: RigidObject = env.scene[robot_cfg.name]
    object: RigidObject = env.scene[object_cfg.name]
    up_local = torch.tensor([0.0, 0.0, 1.0], device=env.device).repeat(env.num_envs, 1)
    up_w = quat_apply(object.data.root_quat_w, up_local)
    return quat_apply_inverse(robot.data.root_quat_w, up_w)


def object_tilt_angle(
    env: ManagerBasedRLEnv,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """Angle (rad) between object's +Z axis and world +Z (0=up, pi=down)."""
    object: RigidObject = env.scene[object_cfg.name]
    up_local = torch.tensor([0.0, 0.0, 1.0], device=env.device).repeat(env.num_envs, 1)
    up_w = quat_apply(object.data.root_quat_w, up_local)
    world_up = torch.tensor([0.0, 0.0, 1.0], device=env.device).repeat(env.num_envs, 1)
    cos_angle = torch.sum(up_w * world_up, dim=1).clamp(-1.0, 1.0)
    return torch.acos(cos_angle).unsqueeze(1)


def body_state_b(
    env: ManagerBasedRLEnv,
    body_asset_cfg: SceneEntityCfg,
    base_asset_cfg: SceneEntityCfg,
) -> torch.Tensor:
    """Body state (pos, quat, lin vel, ang vel) in the base asset's root frame.

    The state for each body is stacked horizontally as
    ``[position(3), quaternion(4)(wxyz), linvel(3), angvel(3)]`` and then concatenated over bodies.

    Args:
        env: The environment.
        body_asset_cfg: Scene entity for the articulated body whose links are observed.
        base_asset_cfg: Scene entity providing the reference (root) frame.

    Returns:
        Tensor of shape ``(num_envs, num_bodies * 13)`` with per-body states expressed in the base root frame.
    """
    body_asset: Articulation = env.scene[body_asset_cfg.name]
    base_asset: Articulation = env.scene[base_asset_cfg.name]
    # get world pose of bodies
    body_pos_w = body_asset.data.body_pos_w[:, body_asset_cfg.body_ids].view(-1, 3)
    body_quat_w = body_asset.data.body_quat_w[:, body_asset_cfg.body_ids].view(-1, 4)
    body_lin_vel_w = body_asset.data.body_lin_vel_w[:, body_asset_cfg.body_ids].view(-1, 3)
    body_ang_vel_w = body_asset.data.body_ang_vel_w[:, body_asset_cfg.body_ids].view(-1, 3)
    num_bodies = int(body_pos_w.shape[0] / env.num_envs)
    # get world pose of base frame
    root_pos_w = base_asset.data.root_link_pos_w.unsqueeze(1).repeat_interleave(num_bodies, dim=1).view(-1, 3)
    root_quat_w = base_asset.data.root_link_quat_w.unsqueeze(1).repeat_interleave(num_bodies, dim=1).view(-1, 4)
    # transform from world body pose to local body pose
    body_pos_b, body_quat_b = subtract_frame_transforms(root_pos_w, root_quat_w, body_pos_w, body_quat_w)
    body_lin_vel_b = quat_apply_inverse(root_quat_w, body_lin_vel_w)
    body_ang_vel_b = quat_apply_inverse(root_quat_w, body_ang_vel_w)
    # concate and return
    out = torch.cat((body_pos_b, body_quat_b, body_lin_vel_b, body_ang_vel_b), dim=1)
    return out.view(env.num_envs, -1)


class body_state_b_vis(ManagerTermBase):
    """Body state with visualization - draws dots on observed body links."""

    def __init__(self, cfg, env: ManagerBasedRLEnv):
        super().__init__(cfg, env)
        self.body_asset_cfg: SceneEntityCfg = cfg.params.get("body_asset_cfg", SceneEntityCfg("robot"))
        self.base_asset_cfg: SceneEntityCfg = cfg.params.get("base_asset_cfg", SceneEntityCfg("robot"))
        
        from isaaclab.markers import VisualizationMarkers, VisualizationMarkersCfg
        import isaaclab.sim as sim_utils
        
        marker_cfg = VisualizationMarkersCfg(
            prim_path="/Visuals/BodyStateMarkers",
            markers={
                "dot": sim_utils.SphereCfg(
                    radius=0.01,
                    visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 0.0, 0.0)),
                ),
            },
        )
        self.visualizer = VisualizationMarkers(marker_cfg)

    def __call__(
        self,
        env: ManagerBasedRLEnv,
        body_asset_cfg: SceneEntityCfg = None,
        base_asset_cfg: SceneEntityCfg = None,
    ) -> torch.Tensor:
        """Compute body state and visualize body positions."""
        body_asset_cfg = body_asset_cfg or self.body_asset_cfg
        base_asset_cfg = base_asset_cfg or self.base_asset_cfg
        
        # Use exact same computation as body_state_b
        body_asset: Articulation = env.scene[body_asset_cfg.name]
        base_asset: Articulation = env.scene[base_asset_cfg.name]
        body_pos_w = body_asset.data.body_pos_w[:, body_asset_cfg.body_ids]
        body_quat_w = body_asset.data.body_quat_w[:, body_asset_cfg.body_ids]
        body_lin_vel_w = body_asset.data.body_lin_vel_w[:, body_asset_cfg.body_ids]
        body_ang_vel_w = body_asset.data.body_ang_vel_w[:, body_asset_cfg.body_ids]
        num_bodies = body_pos_w.shape[1]
        
        root_pos_w = base_asset.data.root_link_pos_w.unsqueeze(1).repeat_interleave(num_bodies, dim=1)
        root_quat_w = base_asset.data.root_link_quat_w.unsqueeze(1).repeat_interleave(num_bodies, dim=1)
        
        body_pos_w_flat = body_pos_w.view(-1, 3)
        body_quat_w_flat = body_quat_w.view(-1, 4)
        root_pos_w_flat = root_pos_w.view(-1, 3)
        root_quat_w_flat = root_quat_w.view(-1, 4)
        
        body_pos_b, body_quat_b = subtract_frame_transforms(root_pos_w_flat, root_quat_w_flat, body_pos_w_flat, body_quat_w_flat)
        body_lin_vel_b = quat_apply_inverse(root_quat_w_flat, body_lin_vel_w.view(-1, 3))
        body_ang_vel_b = quat_apply_inverse(root_quat_w_flat, body_ang_vel_w.view(-1, 3))
        
        # Visualize body positions in world frame
        self.visualizer.visualize(translations=body_pos_w_flat)
        
        out = torch.cat((body_pos_b, body_quat_b, body_lin_vel_b, body_ang_vel_b), dim=1)
        return out.view(env.num_envs, -1)


class robot_fingertips_vis(ManagerTermBase):
    """Visualize robot fingertips with colored spheres matching human fingertips.
    
    Colors match the retargeter visualization:
    - thumb_fingertip: Red
    - fingertip (index): Green
    - fingertip_2 (middle): Blue
    - fingertip_3 (ring): Yellow
    - fingertip_4 (little/pinky): Magenta
    """

    def __init__(self, cfg, env: ManagerBasedRLEnv):
        super().__init__(cfg, env)
        self.body_asset_cfg: SceneEntityCfg = cfg.params.get("body_asset_cfg", SceneEntityCfg("robot"))
        
        from isaaclab.markers import VisualizationMarkers, VisualizationMarkersCfg
        import isaaclab.sim as sim_utils
        
        # Create markers with colors matching human fingertips
        marker_cfg = VisualizationMarkersCfg(
            prim_path="/Visuals/RobotFingertipMarkers",
            markers={
                "thumb_tip": sim_utils.SphereCfg(
                    radius=0.015,
                    visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 0.0, 0.0)),  # Red for thumb
                ),
                "index_tip": sim_utils.SphereCfg(
                    radius=0.015,
                    visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 1.0, 0.0)),  # Green for index
                ),
                "middle_tip": sim_utils.SphereCfg(
                    radius=0.015,
                    visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 0.0, 1.0)),  # Blue for middle
                ),
                "ring_tip": sim_utils.SphereCfg(
                    radius=0.015,
                    visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 1.0, 0.0)),  # Yellow for ring
                ),
                "little_tip": sim_utils.SphereCfg(
                    radius=0.015,
                    visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 0.0, 1.0)),  # Magenta for little/pinky
                ),
            },
        )
        self.visualizer = VisualizationMarkers(marker_cfg)
        
        # Map robot fingertip body names to marker indices
        # Using tip_head links: thumb_tip_head=0 (Red), index_tip_head=1 (Green), middle_tip_head=2 (Blue), ring_tip_head=3 (Yellow), little_tip_head=4 (Magenta)
        # Also support standard naming conventions (thdistal, ffdistal, mfdistal, rfdistal, lfdistal for Shadow Hand)
        self.fingertip_marker_map = {
            "thumb_tip_head": 0,    # Red
            "index_tip_head": 1,    # Green (index)
            "middle_tip_head": 2,   # Blue (middle)
            "ring_tip_head": 3,     # Yellow (ring)
            "little_tip_head": 4,   # Magenta (little/pinky)
            # Shadow Hand standard naming (fallback)
            "thdistal": 0,          # Red (thumb)
            "ffdistal": 1,          # Green (index/first finger)
            "mfdistal": 2,          # Blue (middle finger)
            "rfdistal": 3,          # Yellow (ring finger)
            "lfdistal": 4,          # Magenta (little finger)
            # Also support other naming conventions as fallback
            # "thumb_fingertip": 0,   # Red (fallback)
            # "fingertip": 1,         # Green (fallback)
            # "fingertip_2": 2,       # Blue (fallback)
            # "fingertip_3": 3,       # Yellow (fallback)
        }

    def __call__(
        self,
        env: ManagerBasedRLEnv,
        body_asset_cfg: SceneEntityCfg = None,
    ) -> torch.Tensor:
        """Visualize robot fingertip positions with colored spheres."""
        body_asset_cfg = body_asset_cfg or self.body_asset_cfg
        
        body_asset: Articulation = env.scene[body_asset_cfg.name]
        fingertip_body_names = body_asset_cfg.body_names
        
        if fingertip_body_names is None or len(fingertip_body_names) == 0:
            return torch.zeros(env.num_envs, 0, device=env.device)
        
        # Debug: Print available body names and requested fingertip names (only once)
        if not hasattr(self, "_debug_printed"):
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Robot fingertip visualization - Available body names: {body_asset.body_names}")
            logger.info(f"Robot fingertip visualization - Requested fingertip names: {fingertip_body_names}")
            self._debug_printed = True
        
        # Get fingertip body indices
        fingertip_body_ids = []
        marker_indices_list = []
        for idx, body_name in enumerate(fingertip_body_names):
            if body_name in body_asset.body_names:
                body_idx = body_asset.body_names.index(body_name)
                fingertip_body_ids.append(body_idx)
                # Get marker index: use mapping if available, otherwise use order (thumb=0, index=1, middle=2, ring=3, little=4)
                marker_idx = self.fingertip_marker_map.get(body_name, min(idx, 4))
                marker_indices_list.append(marker_idx)
        
        if len(fingertip_body_ids) == 0:
            return torch.zeros(env.num_envs, 0, device=env.device)
        
        # Get fingertip positions in world frame
        fingertip_pos_w = body_asset.data.body_pos_w[:, fingertip_body_ids]  # Shape: (num_envs, num_fingertips, 3)
        num_fingertips = fingertip_pos_w.shape[1]
        
        # Flatten for visualization: (num_envs * num_fingertips, 3)
        fingertip_pos_w_flat = fingertip_pos_w.view(-1, 3)
        
        # Create marker indices tensor: (num_envs * num_fingertips,)
        marker_indices = torch.tensor(
            marker_indices_list * env.num_envs,
            dtype=torch.int32,
            device=env.device
        )
        
        # Visualize fingertip positions with colored markers
        self.visualizer.visualize(
            translations=fingertip_pos_w_flat,
            marker_indices=marker_indices
        )
        
        # Return empty tensor (this is just for visualization, not used as observation)
        return torch.zeros(env.num_envs, 0, device=env.device)


class object_world_frame_vis(ManagerTermBase):
    """Visualize object and world frames with axis markers."""

    def __init__(self, cfg, env: ManagerBasedRLEnv):
        super().__init__(cfg, env)
        self.object_cfg: SceneEntityCfg = cfg.params.get("object_cfg", SceneEntityCfg("object"))
        frame_scale = cfg.params.get("frame_scale", (0.08, 0.08, 0.08))

        from isaaclab.markers import VisualizationMarkers
        from isaaclab.markers.config import FRAME_MARKER_CFG

        frame_cfg = FRAME_MARKER_CFG.copy()
        frame_cfg.markers["frame"].scale = frame_scale
        self.object_frame_vis = VisualizationMarkers(frame_cfg.replace(prim_path="/Visuals/ObjectFrame"))
        self.world_frame_vis = VisualizationMarkers(frame_cfg.replace(prim_path="/Visuals/WorldFrame"))

    def __call__(
        self,
        env: ManagerBasedRLEnv,
        object_cfg: SceneEntityCfg | None = None,
    ) -> torch.Tensor:
        object_cfg = object_cfg or self.object_cfg
        obj: RigidObject = env.scene[object_cfg.name]

        marker_indices = torch.zeros(env.num_envs, dtype=torch.int32, device=env.device)
        self.object_frame_vis.visualize(
            translations=obj.data.root_pos_w,
            orientations=obj.data.root_quat_w,
            marker_indices=marker_indices,
        )

        world_pos = env.scene.env_origins
        world_quat = torch.tensor([1.0, 0.0, 0.0, 0.0], device=env.device, dtype=world_pos.dtype).unsqueeze(0).repeat(env.num_envs, 1)
        self.world_frame_vis.visualize(
            translations=world_pos,
            orientations=world_quat,
            marker_indices=marker_indices,
        )

        return torch.zeros(env.num_envs, 0, device=env.device)


class object_point_cloud_b(ManagerTermBase):
    """Object surface point cloud expressed in a reference asset's root frame.

    Points are pre-sampled on the object's surface in its local frame and transformed to world,
    then into the reference (e.g., robot) root frame. Optionally visualizes the points.

    Args (from ``cfg.params``):
        object_cfg: Scene entity for the object to sample. Defaults to ``SceneEntityCfg("object")``.
        ref_asset_cfg: Scene entity providing the reference frame. Defaults to ``SceneEntityCfg("robot")``.
        num_points: Number of points to sample on the object surface. Defaults to ``10``.
        visualize: Whether to draw markers for the points. Defaults to ``True``.
        static: If ``True``, cache world-space points on reset and reuse them (no per-step resampling).

    Returns (from ``__call__``):
        If ``flatten=False``: tensor of shape ``(num_envs, num_points, 3)``.
        If ``flatten=True``: tensor of shape ``(num_envs, 3 * num_points)``.
    """

    def __init__(self, cfg, env: ManagerBasedRLEnv):
        super().__init__(cfg, env)

        self.object_cfg: SceneEntityCfg = cfg.params.get("object_cfg", SceneEntityCfg("object"))
        self.ref_asset_cfg: SceneEntityCfg = cfg.params.get("ref_asset_cfg", SceneEntityCfg("robot"))
        num_points: int = cfg.params.get("num_points", 10)
        self.object: RigidObject = env.scene[self.object_cfg.name]
        self.ref_asset: Articulation = env.scene[self.ref_asset_cfg.name]
        # lazy initialize visualizer and point cloud
        if cfg.params.get("visualize", True):
            from isaaclab.markers import VisualizationMarkers
            from isaaclab.markers.config import RAY_CASTER_MARKER_CFG

            ray_cfg = RAY_CASTER_MARKER_CFG.replace(prim_path="/Visuals/ObservationPointCloud")
            ray_cfg.markers["hit"].radius = 0.0025
            self.visualizer = VisualizationMarkers(ray_cfg)
        self.points_local = sample_object_point_cloud(
            env.num_envs, num_points, self.object.cfg.prim_path, device=env.device
        )
        self.points_w = torch.zeros_like(self.points_local)

    def __call__(
        self,
        env: ManagerBasedRLEnv,
        ref_asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
        object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
        num_points: int = 10,
        flatten: bool = False,
        visualize: bool = True,
    ):
        """Compute the object point cloud in the reference asset's root frame.

        Note:
            Points are pre-sampled at initialization using ``self.num_points``; the ``num_points`` argument is
            kept for API symmetry and does not change the sampled set at runtime.

        Args:
            env: The environment.
            ref_asset_cfg: Reference frame provider (root). Defaults to ``SceneEntityCfg("robot")``.
            object_cfg: Object to sample. Defaults to ``SceneEntityCfg("object")``.
            num_points: Unused at runtime; see note above.
            flatten: If ``True``, return a flattened tensor ``(num_envs, 3 * num_points)``.
            visualize: If ``True``, draw markers for the points.

        Returns:
            Tensor of shape ``(num_envs, num_points, 3)`` or flattened if requested.
        """
        ref_pos_w = self.ref_asset.data.root_pos_w.unsqueeze(1).repeat(1, num_points, 1)
        ref_quat_w = self.ref_asset.data.root_quat_w.unsqueeze(1).repeat(1, num_points, 1)

        object_pos_w = self.object.data.root_pos_w.unsqueeze(1).repeat(1, num_points, 1)
        object_quat_w = self.object.data.root_quat_w.unsqueeze(1).repeat(1, num_points, 1)
        # apply rotation + translation
        self.points_w = quat_apply(object_quat_w, self.points_local) + object_pos_w
        if visualize:
            self.visualizer.visualize(translations=self.points_w.view(-1, 3))
        object_point_cloud_pos_b, _ = subtract_frame_transforms(ref_pos_w, ref_quat_w, self.points_w, None)

        return object_point_cloud_pos_b.view(env.num_envs, -1) if flatten else object_point_cloud_pos_b


def fingers_contact_force_b(
    env: ManagerBasedRLEnv,
    contact_sensor_names: list[str],
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """base-frame contact forces from listed sensors, concatenated per env.

    Args:
        env: The environment.
        contact_sensor_names: Names of contact sensors in ``env.scene.sensors`` to read.

    Returns:
        Tensor of shape ``(num_envs, 3 * num_sensors)`` with forces stacked horizontally as
        ``[fx, fy, fz]`` per sensor.
    """
    force_w = [env.scene.sensors[name].data.force_matrix_w.view(env.num_envs, 3) for name in contact_sensor_names]
    force_w = torch.stack(force_w, dim=1)  # Shape: (num_envs, num_sensors, 3)
    robot: Articulation = env.scene[asset_cfg.name]
    forces_b = quat_apply_inverse(robot.data.root_link_quat_w.unsqueeze(1).repeat(1, force_w.shape[1], 1), force_w)
    # Flatten to (num_envs, 3 * num_sensors) for concatenation with other observations
    return forces_b.view(env.num_envs, -1)


def max_joint_pos(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Maximum absolute joint position for the given asset."""
    asset: Articulation = env.scene[asset_cfg.name]
    joint_pos = asset.data.joint_pos[:, asset_cfg.joint_ids]
    max_abs = torch.abs(joint_pos).max(dim=1).values
    return max_abs.unsqueeze(1)


def max_joint_pos_signed(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Maximum joint position (signed) for the given asset."""
    asset: Articulation = env.scene[asset_cfg.name]
    joint_pos = asset.data.joint_pos[:, asset_cfg.joint_ids]
    max_pos = joint_pos.max(dim=1).values
    return max_pos.unsqueeze(1)
