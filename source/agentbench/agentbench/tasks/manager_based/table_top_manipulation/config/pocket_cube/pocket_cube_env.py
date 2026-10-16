"""Isaac Lab environment for a switchable-carrier physical pocket cube."""

from __future__ import annotations

import math
import re

import gymnasium as gym
import numpy as np
import torch
from pxr import Gf, Sdf, Usd, UsdGeom, UsdPhysics

import isaaclab.sim as sim_utils
from isaaclab.envs import ManagerBasedEnv
from isaaclab.markers import VisualizationMarkers, VisualizationMarkersCfg
from isaaclab.utils.math import (
    axis_angle_from_quat,
    quat_apply,
    quat_from_angle_axis,
    quat_inv,
    quat_mul,
)

from .pocket_cube_cfg import (
    CUBE_REST_SIZE,
    CUBIE_CENTER_OFFSET,
    CUBIE_VISUAL_SIZE,
    SCANNED_CUBIE_ASSET_DIR,
)
from .pocket_cube_rules import (
    CORNER_NAMES,
    FACE_AXES,
    FACE_CORNER_POSITIONS,
    FACE_NAMES,
    QUARTER_TURN,
    PocketCubeState,
    _MOVE_TABLES,
)


class InterlockedPocketCubeEnv(ManagerBasedEnv, gym.Env):
    """Eight corners connected to a core or one temporary rotating carrier."""

    SNAP_CAPTURE_ANGLE = math.radians(6.0)
    SNAP_FINISH_TOLERANCE = math.radians(1.0)
    HINGE_OVERTRAVEL = math.radians(5.0)
    MIN_CONTACT_FORCE = 0.05
    MIN_TURN_TORQUE = 1.5e-4
    MIN_CONTACT_DRIVEN_ANGLE = math.radians(87.0)
    DETENT_STIFFNESS = 0.08
    # Four 5 g corner bodies at the pocket-cube radius give the moving layer
    # an inertia on the order of 2.5e-5 kg m^2.  The old 0.001 Nms/rad value
    # left the old 0.20 Nm/rad local detent strongly under-damped: after a gripper
    # crossed the six-degree capture boundary the layer could rebound above
    # 2 rad/s and strike the stationary support hand.  This value is close to
    # critical damping for the reduced 0.08 Nm/rad spring.  The 3 mNm cap also
    # prevents the finite detent from accelerating a lightly loaded face to
    # an implausible speed; mid-turn motion remains fully contact-driven.
    DETENT_DAMPING = 0.003
    DETENT_MAX_TORQUE = 0.003
    LATCH_DAMPING = 0.020
    # A committed live hinge can retain about 0.4 rad/s of relative velocity
    # inside its narrow PhysX limit.  Reusing the 3 mNm moving-detent cap
    # saturates the viscous term and lets that limit oscillation persist for
    # hundreds of steps.  This larger cap applies only after a physical turn
    # has committed and the public active-face flag is clear.
    LATCH_MAX_DAMPING_TORQUE = 0.010
    MAX_VISIBLE_SHELL_PENETRATION = 0.00025
    CANCEL_SPEED = math.radians(8.0)
    CANCEL_MIN_STEPS = 4
    MAX_CENTER_ERROR = 0.003

    # Positive carrier rotation is measured about X/Y/Z.  Face travel is
    # clockwise as viewed from that face, hence these axis signs.
    FACE_AXIS_INDEX = (2, 2, 1, 1, 0, 0)
    FACE_AXIS_SIGN = (-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
    FACE_HINGE_AXIS = ("Z", "Z", "Y", "Y", "X", "X")

    def load_managers(self):
        self._initialize_pocket_cube()
        super().load_managers()
        if "startup" in self.event_manager.available_modes:
            self.event_manager.apply(mode="startup")

    def _initialize_pocket_cube(self) -> None:
        cubies = self.scene["pocket_cubies"]
        cubie_ids, cubie_names = cubies.find_objects(
            [name.lower() for name in CORNER_NAMES], preserve_order=True
        )
        if tuple(cubie_names) != tuple(name.lower() for name in CORNER_NAMES):
            raise RuntimeError(f"Unexpected pocket-cubie order: {cubie_names}")
        self._cube_cubie_ids = cubie_ids

        self._cube_env_roots = self._find_cube_env_roots()
        # Agent-to-cube fixed joints are intentionally absent.  Grasping must
        # be realized by the robot collision bodies and PhysX contact alone.
        self._cube_suction_joints = [{} for _ in self._cube_env_roots]
        stage = sim_utils.get_current_stage()
        self._cube_joint_handles = [self._joint_handles(root) for root in self._cube_env_roots]

        self.pocket_cube_active_face = torch.full(
            (self.num_envs,), -1, dtype=torch.long, device=self.device
        )
        self.pocket_cube_rule_failed = torch.zeros(
            self.num_envs, dtype=torch.bool, device=self.device
        )
        self._cube_face_angles = torch.zeros(
            (self.num_envs, 6), dtype=torch.float32, device=self.device
        )
        self._cube_face_velocities = torch.zeros_like(self._cube_face_angles)
        self._cube_active_steps = torch.zeros(
            self.num_envs, dtype=torch.long, device=self.device
        )
        self._cube_selected_ids = torch.full(
            (self.num_envs, 4), -1, dtype=torch.long, device=self.device
        )
        self._cube_contact_driven_ready = torch.zeros(
            self.num_envs, dtype=torch.bool, device=self.device
        )
        self._cube_permutation = torch.arange(
            8, dtype=torch.long, device=self.device
        ).expand(self.num_envs, -1).clone()
        self._cube_orientation = torch.zeros(
            (self.num_envs, 8), dtype=torch.long, device=self.device
        )
        self._cube_cubie_quat = torch.zeros(
            (self.num_envs, 8, 4), dtype=torch.float32, device=self.device
        )
        self._cube_cubie_quat[..., 0] = 1.0
        self._cube_committed_turns = torch.zeros(
            self.num_envs, dtype=torch.long, device=self.device
        )
        self._cube_latched_face = torch.full(
            (self.num_envs,), -1, dtype=torch.long, device=self.device
        )
        # Multi-move reindexing is deliberately spread over separate physics
        # steps.  Runtime pose writes and joint enables in the same step make
        # PhysX create a fixed joint from stale body transforms, which can
        # visibly snap cubies.  Phases are: 0=idle, 1=core frames authored,
        # 2=empty carrier reset, 3=next carrier frames authored.
        self._cube_reindex_phase = torch.zeros(
            self.num_envs, dtype=torch.long, device=self.device
        )
        self._cube_reindex_next_face = torch.full(
            (self.num_envs,), -1, dtype=torch.long, device=self.device
        )
        self._cube_latched_ids = torch.full(
            (self.num_envs, 4), -1, dtype=torch.long, device=self.device
        )
        self._cube_armed_face = torch.full(
            (self.num_envs,), -1, dtype=torch.long, device=self.device
        )
        self._cube_order_arm_quiet_steps = torch.zeros(
            self.num_envs, dtype=torch.long, device=self.device
        )
        self._cube_max_shell_penetration = torch.zeros(
            self.num_envs, dtype=torch.float32, device=self.device
        )
        self._cube_first_penetration: list[dict | None] = [None] * self.num_envs
        self._cube_preconfigured_face = -1
        if bool(getattr(self.cfg, "preconfigure_single_target_face", False)):
            moves = tuple(self.cfg.target_moves)
            if len(moves) != 1:
                raise RuntimeError(
                    "preconfigure_single_target_face requires exactly one target move"
                )
            self._cube_preconfigured_face = FACE_NAMES.index(str(moves[0][0]).upper())

        target = PocketCubeState().apply(tuple(self.cfg.target_moves))
        self.pocket_cube_target_tensor = torch.tensor(
            target.as_vector(), dtype=torch.float32, device=self.device
        ).expand(self.num_envs, -1).clone()
        self._initialize_cubie_geometry()
        self._refresh_state_observation()

    def _find_cube_env_roots(self) -> list[str]:
        stage = sim_utils.get_current_stage()
        roots = []
        suffix = "/PocketCube/Joints"
        for prim in stage.Traverse():
            path = str(prim.GetPath())
            if path.endswith(suffix):
                roots.append(path[: -len(suffix)])

        def natural_key(path: str):
            match = re.search(r"env_(\d+)$", path)
            return int(match.group(1)) if match else path

        roots.sort(key=natural_key)
        if len(roots) != self.num_envs:
            raise RuntimeError(
                f"Expected {self.num_envs} pocket-cube joint roots, found {len(roots)}"
            )
        return roots

    @staticmethod
    def _joint_handles(env_root: str) -> dict[str, object]:
        stage = sim_utils.get_current_stage()
        base = f"{env_root}/PocketCube/Joints"
        handles: dict[str, object] = {
            "core_carrier": UsdPhysics.FixedJoint.Get(stage, f"{base}/CoreCarrierLock"),
            "hinges": {
                axis: UsdPhysics.RevoluteJoint.Get(stage, f"{base}/Hinge{axis}")
                for axis in ("X", "Y", "Z")
            },
            "core": {},
            "carrier": {},
        }
        for name in CORNER_NAMES:
            key = name.lower()
            handles["core"][key] = UsdPhysics.FixedJoint.Get(
                stage, f"{base}/CoreLocks/{key}"
            )
            handles["carrier"][key] = UsdPhysics.FixedJoint.Get(
                stage, f"{base}/CarrierLocks/{key}"
            )
        return handles

    def _initialize_cubie_geometry(self) -> None:
        """Create pose-synchronized visuals and declared-shell audit geometry."""

        centers = []
        sticker_offsets = []
        sticker_cubies = []
        sticker_faces = []
        sticker_thickness = 0.0007
        sticker_surface_gap = 0.00002
        for cubie_id, name in enumerate(CORNER_NAMES):
            center = [
                CUBIE_CENTER_OFFSET if "R" in name else -CUBIE_CENTER_OFFSET,
                CUBIE_CENTER_OFFSET if "F" in name else -CUBIE_CENTER_OFFSET,
                CUBIE_CENTER_OFFSET if "U" in name else -CUBIE_CENTER_OFFSET,
            ]
            centers.append(center)
            for face in name:
                offset = [0.0, 0.0, 0.0]
                face_id = FACE_NAMES.index(face)
                axis_id = self.FACE_AXIS_INDEX[face_id]
                outward_sign = -self.FACE_AXIS_SIGN[face_id]
                offset[axis_id] = outward_sign * (
                    CUBIE_VISUAL_SIZE / 2.0
                    + sticker_thickness / 2.0
                    + sticker_surface_gap
                )
                sticker_offsets.append(offset)
                sticker_cubies.append(cubie_id)
                sticker_faces.append(face_id)
        self._cube_solved_centers = torch.tensor(
            centers, dtype=torch.float32, device=self.device
        )
        self._cube_sticker_offsets = torch.tensor(
            sticker_offsets, dtype=torch.float32, device=self.device
        )
        self._cube_sticker_cubies = torch.tensor(
            sticker_cubies, dtype=torch.long, device=self.device
        )
        self._cube_sticker_faces = torch.tensor(
            sticker_faces, dtype=torch.long, device=self.device
        )

        # The physical USDs are hidden below the rigid bodies because nested
        # transforms can lag under Fabric. VisualizationMarkers strips their
        # rigid/collision schemas and drives the full-resolution scanned mesh
        # from the live rigid-body tensor pose. The source was captured during
        # a layer turn, so its baked colors are replaced by the task's solved
        # face convention; otherwise one logical face starts visibly mixed.
        body_material = sim_utils.PreviewSurfaceCfg(
            diffuse_color=(0.018, 0.020, 0.024), roughness=0.72
        )
        self._cube_body_markers = VisualizationMarkers(
            VisualizationMarkersCfg(
                prim_path="/World/Visuals/PocketCubeScannedCubies",
                markers={
                    name.lower(): sim_utils.UsdFileCfg(
                        usd_path=str(
                            SCANNED_CUBIE_ASSET_DIR
                            / f"cubie_{name.lower()}.usd"
                        ),
                        visual_material=body_material,
                    )
                    for name in CORNER_NAMES
                },
            )
        )
        self._cube_body_marker_indices = torch.arange(
            len(CORNER_NAMES), dtype=torch.long, device=self.device
        ).repeat(self.num_envs)
        colors = {
            "U": (0.92, 0.92, 0.90),
            "D": (0.98, 0.78, 0.02),
            "F": (0.02, 0.58, 0.18),
            "B": (0.03, 0.22, 0.86),
            "R": (0.86, 0.04, 0.035),
            "L": (1.0, 0.30, 0.015),
        }
        sticker_size = CUBIE_VISUAL_SIZE - 0.0007
        sizes = {
            "U": (sticker_size, sticker_size, sticker_thickness),
            "D": (sticker_size, sticker_size, sticker_thickness),
            "F": (sticker_size, sticker_thickness, sticker_size),
            "B": (sticker_size, sticker_thickness, sticker_size),
            "R": (sticker_thickness, sticker_size, sticker_size),
            "L": (sticker_thickness, sticker_size, sticker_size),
        }
        self._cube_sticker_markers = {
            face: VisualizationMarkers(
                VisualizationMarkersCfg(
                    prim_path=f"/World/Visuals/PocketCubeStickers/{face}",
                    markers={
                        "sticker": sim_utils.CuboidCfg(
                            size=sizes[face],
                            visual_material=sim_utils.PreviewSurfaceCfg(
                                diffuse_color=colors[face], roughness=0.42
                            ),
                        )
                    },
                )
            )
            for face in FACE_NAMES
        }
        self._robot_tool_shank_markers = None
        self._robot_tool_pad_markers = None
        self._robot_tool_body_ids = {}
        self._robot_tool_surface_samples = {}
        robots = {
            side: self.scene[f"{side}_robot"] for side in ("left", "right")
        }
        tool_body_variants = (
            ("gripper_base", "gripper_link1", "gripper_link2"),
            (
                "right_hand_C_MC",
                "right_thumb_elastomer",
                "right_index_elastomer",
                "right_middle_elastomer",
                "right_ring_elastomer",
                "right_pinky_elastomer",
            ),
        )
        tool_body_names = next(
            (
                variant
                for variant in tool_body_variants
                if all(
                    set(variant).issubset(set(robot.body_names))
                    for robot in robots.values()
                )
            ),
            None,
        )
        if tool_body_names is None:
            body_names = {
                side: tuple(robot.body_names) for side, robot in robots.items()
            }
            raise RuntimeError(
                "Pocket-cube visible-shell audit has no geometry mapping for "
                f"robot bodies: {body_names}"
            )

        for side, robot in robots.items():
            body_entries = []
            for body_name in tool_body_names:
                body_ids, matched_names = robot.find_bodies(
                    [body_name], preserve_order=True
                )
                if len(body_ids) != 1 or tuple(matched_names) != (body_name,):
                    raise RuntimeError(
                        f"Unexpected {side} tool body match for {body_name}: "
                        f"ids={body_ids}, names={matched_names}"
                    )
                body_entries.append((body_name, body_ids[0]))
            self._robot_tool_body_ids[side] = tuple(body_entries)
        self._robot_tool_names = tuple(
            f"{side}_{body_name}"
            for side in ("left", "right")
            for body_name in tool_body_names
        )

        def deterministic_subset(points: np.ndarray, limit: int) -> np.ndarray:
            if len(points) <= limit:
                return points
            indices = np.linspace(0, len(points) - 1, limit).astype(np.int64)
            return points[indices]

        stage = sim_utils.get_current_stage()
        xform_cache = UsdGeom.XformCache()
        reference_robot = robots["left"]
        reference_links = reference_robot.root_physx_view.link_paths[0]
        reference_ids = dict(self._robot_tool_body_ids["left"])

        def belongs_to_collision(mesh_prim, body_prim) -> bool:
            current = mesh_prim
            while current and current != body_prim:
                if current.HasAPI(UsdPhysics.CollisionAPI):
                    return True
                current = current.GetParent()
            return False

        for body_name in tool_body_names:
            body_prim = stage.GetPrimAtPath(reference_links[reference_ids[body_name]])
            vertices = []
            centroids = []
            for mesh_prim in Usd.PrimRange(
                body_prim, Usd.TraverseInstanceProxies()
            ):
                if not mesh_prim.IsA(UsdGeom.Mesh) or not belongs_to_collision(
                    mesh_prim, body_prim
                ):
                    continue
                mesh = UsdGeom.Mesh(mesh_prim)
                points = mesh.GetPointsAttr().Get()
                if not points:
                    continue
                mesh_to_body, _ = xform_cache.ComputeRelativeTransform(
                    mesh_prim, body_prim
                )
                local_points = np.asarray(
                    [tuple(mesh_to_body.Transform(point)) for point in points],
                    dtype=np.float32,
                )
                vertices.append(local_points)
                face_counts = mesh.GetFaceVertexCountsAttr().Get()
                face_indices = mesh.GetFaceVertexIndicesAttr().Get()
                if face_counts and face_indices:
                    cursor = 0
                    mesh_centroids = []
                    for count in face_counts:
                        next_cursor = cursor + int(count)
                        indices = face_indices[cursor:next_cursor]
                        mesh_centroids.append(local_points[indices].mean(axis=0))
                        cursor = next_cursor
                    centroids.append(np.asarray(mesh_centroids, dtype=np.float32))
            if not vertices:
                raise RuntimeError(
                    f"No collision mesh found below robot tool body {body_prim.GetPath()}"
                )
            vertex_samples = np.concatenate(vertices, axis=0)
            centroid_samples = (
                np.concatenate(centroids, axis=0)
                if centroids
                else np.empty((0, 3), dtype=np.float32)
            )
            # Vertices catch narrow edges; polygon centroids cover broad faces
            # whose vertices can remain outside a cubie during a shallow
            # crossing. Reading the composed USD collision prim keeps this
            # audit aligned with either robot asset and its local transforms.
            samples = np.concatenate(
                (
                    deterministic_subset(vertex_samples, 4096),
                    deterministic_subset(centroid_samples, 4096),
                ),
                axis=0,
            )
            self._robot_tool_surface_samples[body_name] = torch.as_tensor(
                samples, dtype=torch.float32, device=self.device
            )
        self.sync_pocket_cube_visuals()

    def sync_pocket_cube_visuals(self) -> None:
        if self._cube_body_markers is None:
            return
        cubies = self.scene["pocket_cubies"]
        positions = cubies.data.object_link_pos_w[:, self._cube_cubie_ids]
        quaternions = cubies.data.object_link_quat_w[:, self._cube_cubie_ids]
        # Bodies and stickers use the same current tensor pose and are authored
        # in one update, so RTX cannot show a moving sticker on a stale body.
        self._cube_body_markers.visualize(
            translations=positions.reshape(-1, 3),
            orientations=quaternions.reshape(-1, 4),
            marker_indices=self._cube_body_marker_indices,
        )
        sticker_quat = quaternions[:, self._cube_sticker_cubies]
        offsets = self._cube_sticker_offsets.unsqueeze(0).expand(
            self.num_envs, -1, -1
        )
        sticker_pos = positions[:, self._cube_sticker_cubies] + quat_apply(
            sticker_quat.reshape(-1, 4), offsets.reshape(-1, 3)
        ).reshape(self.num_envs, 24, 3)
        flat_faces = self._cube_sticker_faces.repeat(self.num_envs)
        for face_id, face in enumerate(FACE_NAMES):
            selected = flat_faces == face_id
            self._cube_sticker_markers[face].visualize(
                translations=sticker_pos.reshape(-1, 3)[selected],
                orientations=sticker_quat.reshape(-1, 4)[selected],
            )

    def _sync_robot_contact_visuals(self) -> None:
        """Draw the real contact-tool collision bodies at their live poses."""

        if self._robot_tool_shank_markers is None:
            return
        shank_positions = []
        shank_quaternions = []
        pad_positions = []
        pad_quaternions = []
        shank_local_center = torch.tensor(
            [0.0, 0.0, 0.066], dtype=torch.float32, device=self.device
        )
        pad_local_center = torch.tensor(
            [0.0, -0.006, 0.0], dtype=torch.float32, device=self.device
        )
        for side in ("left", "right"):
            robot = self.scene[f"{side}_robot"]
            body_ids = dict(self._robot_tool_body_ids[side])
            base_id = body_ids["gripper_base"]
            pad_ids = (body_ids["gripper_link1"], body_ids["gripper_link2"])
            base_pos = robot.data.body_pos_w[:, base_id]
            base_quat = robot.data.body_quat_w[:, base_id]
            shank_positions.append(
                base_pos
                + quat_apply(
                    base_quat.reshape(-1, 4),
                    shank_local_center.expand(self.num_envs, -1),
                )
            )
            shank_quaternions.append(base_quat)
            current_pad_pos = robot.data.body_pos_w[:, list(pad_ids)]
            current_pad_quat = robot.data.body_quat_w[:, list(pad_ids)]
            pad_positions.append(
                current_pad_pos
                + quat_apply(
                    current_pad_quat.reshape(-1, 4),
                    pad_local_center.expand(self.num_envs * 2, -1),
                ).reshape(self.num_envs, 2, 3)
            )
            pad_quaternions.append(current_pad_quat)
        self._robot_tool_shank_markers.visualize(
            translations=torch.stack(shank_positions, dim=1).reshape(-1, 3),
            orientations=torch.stack(shank_quaternions, dim=1).reshape(-1, 4),
        )
        self._robot_tool_pad_markers.visualize(
            translations=torch.cat(pad_positions, dim=1).reshape(-1, 3),
            orientations=torch.cat(pad_quaternions, dim=1).reshape(-1, 4),
        )

    @staticmethod
    def _quaternion_box_axes(quaternions: torch.Tensor) -> torch.Tensor:
        """Return each box's three local axes expressed in world coordinates."""

        identity = torch.eye(
            3, dtype=quaternions.dtype, device=quaternions.device
        ).reshape(1, 1, 3, 3)
        local_axes = identity.expand(*quaternions.shape[:-1], 3, 3)
        expanded_quaternions = quaternions.unsqueeze(-2).expand(
            *quaternions.shape[:-1], 3, 4
        )
        return quat_apply(
            expanded_quaternions.reshape(-1, 4), local_axes.reshape(-1, 3)
        ).reshape(*quaternions.shape[:-1], 3, 3)

    def _robot_cube_visible_shell_penetration(
        self,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Measure original robot-tool surface penetration into cubie shells.

        Returns the maximum penetration and the corresponding tool/cubie
        indices for each environment. Dense deterministic samples of the
        upstream Piper or Sharpa collision meshes make the audit independent
        of the PhysX solver's contact report.
        """
        cubies = self.scene["pocket_cubies"]
        cubie_centers = cubies.data.object_link_pos_w[:, self._cube_cubie_ids]
        cubie_quaternions = cubies.data.object_link_quat_w[:, self._cube_cubie_ids]
        cubie_inverse = quat_inv(cubie_quaternions.reshape(-1, 4)).reshape(
            self.num_envs, 8, 4
        )
        pair_depths = []
        for side in ("left", "right"):
            robot = self.scene[f"{side}_robot"]
            for body_name, body_id in self._robot_tool_body_ids[side]:
                samples = self._robot_tool_surface_samples[body_name]
                point_count = samples.shape[0]
                body_pos = robot.data.body_pos_w[:, body_id]
                body_quat = robot.data.body_quat_w[:, body_id]
                world_points = body_pos[:, None] + quat_apply(
                    body_quat[:, None].expand(-1, point_count, -1).reshape(-1, 4),
                    samples[None].expand(self.num_envs, -1, -1).reshape(-1, 3),
                ).reshape(self.num_envs, point_count, 3)
                relative = world_points[:, None] - cubie_centers[:, :, None]
                cubie_local = quat_apply(
                    cubie_inverse[:, :, None]
                    .expand(-1, -1, point_count, -1)
                    .reshape(-1, 4),
                    relative.reshape(-1, 3),
                ).reshape(self.num_envs, 8, point_count, 3)
                inward = CUBIE_VISUAL_SIZE / 2.0 - cubie_local.abs()
                point_depth = inward.min(dim=-1).values
                pair_depths.append(point_depth.max(dim=-1).values)

        pair_penetration = torch.stack(pair_depths, dim=1)
        env_count, tool_count, cubie_count = pair_penetration.shape
        flat_penetration = pair_penetration.reshape(env_count, -1)
        max_penetration, flat_pair = flat_penetration.max(dim=-1)
        return (
            max_penetration,
            flat_pair // cubie_count,
            flat_pair % cubie_count,
        )

    @staticmethod
    def _points_inside_box_depth(
        world_points: torch.Tensor,
        box_position: torch.Tensor,
        box_quaternion: torch.Tensor,
        half_extents: torch.Tensor,
    ) -> torch.Tensor:
        """Return the deepest sampled-point intrusion into an oriented box."""

        point_count = world_points.shape[1]
        inverse = quat_inv(box_quaternion)
        local_points = quat_apply(
            inverse[:, None].expand(-1, point_count, -1).reshape(-1, 4),
            (world_points - box_position[:, None]).reshape(-1, 3),
        ).reshape(world_points.shape)
        inward = half_extents.reshape(1, 1, 3) - local_points.abs()
        return inward.min(dim=-1).values.max(dim=-1).values

    def _support_visible_shell_penetration(
        self,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Audit tool/cubie visible shells against the table and open rest."""

        support_specs = (
            ("table", self.scene["table"], (0.525, 0.55, 0.25)),
            (
                "cube_rest",
                self.scene["cube_rest"],
                tuple(0.5 * extent for extent in CUBE_REST_SIZE),
            ),
        )
        pair_depths = []
        pair_names = []
        for side in ("left", "right"):
            robot = self.scene[f"{side}_robot"]
            for body_name, body_id in self._robot_tool_body_ids[side]:
                samples = self._robot_tool_surface_samples[body_name]
                point_count = samples.shape[0]
                body_pos = robot.data.body_pos_w[:, body_id]
                body_quat = robot.data.body_quat_w[:, body_id]
                world_points = body_pos[:, None] + quat_apply(
                    body_quat[:, None]
                    .expand(-1, point_count, -1)
                    .reshape(-1, 4),
                    samples[None]
                    .expand(self.num_envs, -1, -1)
                    .reshape(-1, 3),
                ).reshape(self.num_envs, point_count, 3)
                for support_name, support, half_extents in support_specs:
                    pair_depths.append(
                        self._points_inside_box_depth(
                            world_points,
                            support.data.root_pos_w,
                            support.data.root_quat_w,
                            torch.tensor(
                                half_extents,
                                dtype=torch.float32,
                                device=self.device,
                            ),
                        )
                    )
                    pair_names.append((f"{side}_{body_name}", support_name))

        cubies = self.scene["pocket_cubies"]
        cubie_pos = cubies.data.object_link_pos_w[:, self._cube_cubie_ids]
        cubie_quat = cubies.data.object_link_quat_w[:, self._cube_cubie_ids]
        signs = torch.tensor(
            [
                (x, y, z)
                for x in (-1.0, 1.0)
                for y in (-1.0, 1.0)
                for z in (-1.0, 1.0)
            ],
            dtype=torch.float32,
            device=self.device,
        )
        local_vertices = signs * (CUBIE_VISUAL_SIZE / 2.0)
        for cubie_id, cubie_name in enumerate(CORNER_NAMES):
            vertices = cubie_pos[:, cubie_id, None] + quat_apply(
                cubie_quat[:, cubie_id, None]
                .expand(-1, 8, -1)
                .reshape(-1, 4),
                local_vertices[None]
                .expand(self.num_envs, -1, -1)
                .reshape(-1, 3),
            ).reshape(self.num_envs, 8, 3)
            for support_name, support, half_extents in support_specs:
                pair_depths.append(
                    self._points_inside_box_depth(
                        vertices,
                        support.data.root_pos_w,
                        support.data.root_quat_w,
                        torch.tensor(
                            half_extents,
                            dtype=torch.float32,
                            device=self.device,
                        ),
                    )
                )
                pair_names.append((f"cubie_{cubie_name}", support_name))

        depths = torch.stack(pair_depths, dim=1)
        max_penetration, pair_ids = depths.max(dim=1)
        self._support_penetration_pair_names = tuple(pair_names)
        return max_penetration, pair_ids

    @staticmethod
    def _enable(joint, enabled: bool) -> None:
        joint.GetJointEnabledAttr().Set(enabled)

    @staticmethod
    def _set_hinge_limits(joint, center_deg: float, half_width_deg: float) -> None:
        joint.GetLowerLimitAttr().Set(float(center_deg - half_width_deg))
        joint.GetUpperLimitAttr().Set(float(center_deg + half_width_deg))

    @staticmethod
    def _set_fixed_frame(joint, position: torch.Tensor, quaternion: torch.Tensor) -> None:
        # These four values define one joint frame and must reach PhysX as one
        # coherent edit.  Without a ChangeBlock, each Attr.Set emits a USD
        # notice; PhysX briefly recreates the joint after localPos0 changes but
        # before localRot0 does, observes disjoint anchors, and may snap the
        # bodies even though the final pair is mathematically coincident.
        with Sdf.ChangeBlock():
            joint.GetLocalPos0Attr().Set(
                Gf.Vec3f(float(position[0]), float(position[1]), float(position[2]))
            )
            joint.GetLocalRot0Attr().Set(
                Gf.Quatf(
                    float(quaternion[0]),
                    Gf.Vec3f(
                        float(quaternion[1]),
                        float(quaternion[2]),
                        float(quaternion[3]),
                    ),
                )
            )
            joint.GetLocalPos1Attr().Set(Gf.Vec3f(0.0))
            joint.GetLocalRot1Attr().Set(Gf.Quatf(1.0, Gf.Vec3f(0.0)))

    def _reset_joint_switches(self, env_id: int) -> None:
        for joint in self._cube_suction_joints[env_id].values():
            self._enable(joint, False)
        handles = self._cube_joint_handles[env_id]
        for hinge in handles["hinges"].values():
            self._enable(hinge, False)
            self._set_hinge_limits(hinge, 0.0, 95.0)
        preconfigured = self._cube_preconfigured_face
        if preconfigured < 0 and bool(
            getattr(self.cfg, "enforce_target_face_order", True)
        ):
            # Arm the first requested hinge while the cube is still exactly on
            # its reset grid.  Waiting for contact before transferring four
            # loaded cubies from Core to Carrier creates a constraint-switch
            # impulse; on a real indexed mechanism the next slot is selected
            # before the operator applies turning torque.
            first_face = str(tuple(self.cfg.target_moves)[0][0]).upper()
            preconfigured = FACE_NAMES.index(first_face)
        selected = (
            set(FACE_CORNER_POSITIONS[preconfigured]) if preconfigured >= 0 else set()
        )
        for cubie_id, name in enumerate(CORNER_NAMES):
            key = name.lower()
            self._set_fixed_frame(
                handles["core"][key],
                self._cube_solved_centers[cubie_id],
                torch.tensor((1.0, 0.0, 0.0, 0.0), device=self.device),
            )
            self._set_fixed_frame(
                handles["carrier"][key],
                self._cube_solved_centers[cubie_id],
                torch.tensor((1.0, 0.0, 0.0, 0.0), device=self.device),
            )
            self._enable(handles["core"][key], cubie_id not in selected)
            self._enable(handles["carrier"][key], cubie_id in selected)
        if preconfigured >= 0:
            self._enable(handles["core_carrier"], False)
            active_axis = self.FACE_HINGE_AXIS[preconfigured]
            self._enable(handles["hinges"][active_axis], True)
            self._set_hinge_limits(handles["hinges"][active_axis], 0.0, 0.05)
        else:
            self._enable(handles["core_carrier"], True)

    def set_magnetic_suction_frames(
        self,
        env_id: int,
        frames: dict[str, tuple[np.ndarray, np.ndarray]] | None,
    ) -> None:
        """Reject agent-authored grasp constraints.

        A fixed joint between a tool and the cube bypasses contact dynamics and
        is explicitly forbidden by ``rules_grasp.md`` and ``pocket_cube.md``.
        The API is retained only so old diagnostic controllers fail loudly
        instead of silently producing evaluator false positives.
        """

        if frames is None:
            # Releasing already-disabled startup joints is harmless and keeps
            # cleanup code idempotent.
            for joint in self._cube_suction_joints[int(env_id)].values():
                self._enable(joint, False)
            return
        self.pocket_cube_rule_failed[int(env_id)] = True
        raise RuntimeError(
            "agent-authored magnetic/fixed grasp constraints are prohibited; "
            "manipulation must be driven by robot collision contact"
        )

    def _reset_idx(self, env_ids):
        super()._reset_idx(env_ids)
        if not hasattr(self, "_cube_joint_handles"):
            return
        if isinstance(env_ids, slice):
            env_ids = torch.arange(self.num_envs, device=self.device, dtype=torch.long)
        else:
            env_ids = torch.as_tensor(env_ids, device=self.device, dtype=torch.long)
        for env_id in env_ids.tolist():
            self._reset_joint_switches(env_id)
        self.pocket_cube_active_face[env_ids] = -1
        self.pocket_cube_rule_failed[env_ids] = False
        self._cube_face_angles[env_ids] = 0.0
        self._cube_face_velocities[env_ids] = 0.0
        self._cube_active_steps[env_ids] = 0
        self._cube_selected_ids[env_ids] = -1
        self._cube_contact_driven_ready[env_ids] = False
        self._cube_permutation[env_ids] = torch.arange(8, device=self.device)
        self._cube_orientation[env_ids] = 0
        self._cube_cubie_quat[env_ids] = 0.0
        self._cube_cubie_quat[env_ids, :, 0] = 1.0
        self._cube_committed_turns[env_ids] = 0
        self._cube_latched_face[env_ids] = -1
        self._cube_reindex_phase[env_ids] = 0
        self._cube_reindex_next_face[env_ids] = -1
        self._cube_latched_ids[env_ids] = -1
        if self._cube_preconfigured_face >= 0:
            self._cube_armed_face[env_ids] = self._cube_preconfigured_face
        elif bool(getattr(self.cfg, "enforce_target_face_order", True)):
            first_face = FACE_NAMES.index(
                str(tuple(self.cfg.target_moves)[0][0]).upper()
            )
            self._cube_armed_face[env_ids] = first_face
        else:
            self._cube_armed_face[env_ids] = -1
        self._cube_order_arm_quiet_steps[env_ids] = 0
        self._cube_max_shell_penetration[env_ids] = 0.0
        for env_id in env_ids.tolist():
            self._cube_first_penetration[env_id] = None
        self._refresh_state_observation()

    def _carrier_displacement_and_velocity(self) -> tuple[torch.Tensor, torch.Tensor]:
        core = self.scene["pocket_cube"]
        carrier = self.scene["pocket_cube_carrier"]
        relative_quat = quat_mul(quat_inv(core.data.root_quat_w), carrier.data.root_quat_w)
        rotation_vector = axis_angle_from_quat(relative_quat)
        displacement = torch.zeros(self.num_envs, device=self.device)
        velocity = torch.zeros_like(displacement)
        relative_omega = carrier.data.root_ang_vel_w - core.data.root_ang_vel_w
        for env_id in range(self.num_envs):
            face_id = int(self.pocket_cube_active_face[env_id])
            if face_id < 0:
                continue
            axis_id = self.FACE_AXIS_INDEX[face_id]
            sign = self.FACE_AXIS_SIGN[face_id]
            displacement[env_id] = sign * rotation_vector[env_id, axis_id]
            local_axis = torch.zeros(3, device=self.device)
            local_axis[axis_id] = 1.0
            world_axis = quat_apply(core.data.root_quat_w[env_id : env_id + 1], local_axis[None])[0]
            velocity[env_id] = sign * torch.dot(relative_omega[env_id], world_axis)
        return displacement, velocity

    def get_pocket_cube_face_joint_state(self) -> tuple[torch.Tensor, torch.Tensor]:
        angles = self._cube_face_angles.clone()
        velocities = torch.zeros_like(angles)
        displacement, active_velocity = self._carrier_displacement_and_velocity()
        active_envs = torch.nonzero(self.pocket_cube_active_face >= 0, as_tuple=False).squeeze(-1)
        if active_envs.numel() > 0:
            faces = self.pocket_cube_active_face[active_envs]
            angles[active_envs, faces] += displacement[active_envs]
            velocities[active_envs, faces] = active_velocity[active_envs]
        # A completed preconfigured one-turn mechanism remains physically
        # locked at its 90-degree hinge limit.  Report that live relative pose
        # (and velocity) while keeping the logical active-face flag clear.
        latched_envs = torch.nonzero(
            (self.pocket_cube_active_face < 0) & (self._cube_latched_face >= 0),
            as_tuple=False,
        ).squeeze(-1)
        if latched_envs.numel() > 0:
            core = self.scene["pocket_cube"]
            carrier = self.scene["pocket_cube_carrier"]
            relative_quat = quat_mul(
                quat_inv(core.data.root_quat_w), carrier.data.root_quat_w
            )
            rotation_vector = axis_angle_from_quat(relative_quat)
            relative_omega = carrier.data.root_ang_vel_w - core.data.root_ang_vel_w
            for env_id in latched_envs.tolist():
                face_id = int(self._cube_latched_face[env_id])
                axis_id = self.FACE_AXIS_INDEX[face_id]
                sign = self.FACE_AXIS_SIGN[face_id]
                angles[env_id, face_id] = sign * rotation_vector[env_id, axis_id]
                local_axis = torch.zeros(3, device=self.device)
                local_axis[axis_id] = 1.0
                world_axis = quat_apply(
                    core.data.root_quat_w[env_id : env_id + 1], local_axis[None]
                )[0]
                velocities[env_id, face_id] = sign * torch.dot(
                    relative_omega[env_id], world_axis
                )
        self._cube_face_velocities.copy_(velocities)
        return angles, velocities

    def _robot_contact_wrench_by_face(self) -> tuple[torch.Tensor, torch.Tensor]:
        """Project robot-on-cubie contact into candidate face torques."""

        cubie_forces = torch.zeros(
            (self.num_envs, 8, 3), dtype=torch.float32, device=self.device
        )
        for sensor_name, sensor in self.scene.sensors.items():
            if not sensor_name.endswith("_face_contacts") or sensor.data.force_matrix_w is None:
                continue
            matrix = torch.nan_to_num(sensor.data.force_matrix_w)
            if matrix.shape[-2] != 8:
                continue
            cubie_forces += matrix.reshape(self.num_envs, -1, 8, 3).sum(dim=1)

        core = self.scene["pocket_cube"]
        cubies = self.scene["pocket_cubies"]
        cubie_pos = cubies.data.object_link_pos_w[:, self._cube_cubie_ids]
        moment = torch.linalg.cross(
            cubie_pos - core.data.root_pos_w[:, None, :], cubie_forces, dim=-1
        )
        torque_by_face = torch.zeros((self.num_envs, 6), device=self.device)
        force_by_face = torch.zeros_like(torque_by_face)
        for face_id in range(6):
            positions = torch.tensor(
                FACE_CORNER_POSITIONS[face_id], dtype=torch.long, device=self.device
            )
            ids = self._cube_permutation[:, positions]
            gather = ids.unsqueeze(-1).expand(-1, -1, 3)
            layer_moment = torch.gather(moment, 1, gather).sum(dim=1)
            layer_force = torch.gather(cubie_forces, 1, gather)
            local_axis = torch.tensor(
                FACE_AXES[face_id], dtype=torch.float32, device=self.device
            ).expand(self.num_envs, -1)
            world_axis = quat_apply(core.data.root_quat_w, local_axis)
            torque_by_face[:, face_id] = (layer_moment * world_axis).sum(dim=-1)
            force_by_face[:, face_id] = torch.linalg.norm(layer_force, dim=-1).sum(dim=-1)
        return torque_by_face, force_by_face

    def _prepare_carrier_lock_frames(self, env_id: int, face_id: int) -> None:
        """Author disabled Carrier locks from live poses before ownership changes."""

        handles = self._cube_joint_handles[env_id]
        carrier = self.scene["pocket_cube_carrier"]
        cubies = self.scene["pocket_cubies"]
        carrier_pos = carrier.data.root_pos_w[env_id]
        carrier_quat_inv = quat_inv(carrier.data.root_quat_w[env_id : env_id + 1])[0]
        positions = torch.tensor(
            FACE_CORNER_POSITIONS[face_id], dtype=torch.long, device=self.device
        )
        selected_ids = self._cube_permutation[env_id, positions]
        for cubie_id in selected_ids.tolist():
            key = CORNER_NAMES[cubie_id].lower()
            actual_pos = cubies.data.object_link_pos_w[
                env_id, self._cube_cubie_ids[cubie_id]
            ]
            actual_quat = cubies.data.object_link_quat_w[
                env_id, self._cube_cubie_ids[cubie_id]
            ]
            # Capture the live body1-in-body0 pose before changing ownership.
            # This makes Core -> Carrier handoff continuous even if the solver
            # left a microscopic residual from the previous lock.
            local_pos = quat_apply(
                carrier_quat_inv[None], (actual_pos - carrier_pos)[None]
            )[0]
            local_quat = quat_mul(
                carrier_quat_inv[None], actual_quat[None]
            )[0]
            self._set_fixed_frame(
                handles["carrier"][key],
                local_pos,
                local_quat,
            )

    def _prepare_core_lock_frames_for_ids(
        self, env_id: int, selected_ids: torch.Tensor
    ) -> None:
        """Author disabled Core locks from current rigid-body poses."""

        handles = self._cube_joint_handles[env_id]
        core = self.scene["pocket_cube"]
        cubies = self.scene["pocket_cubies"]
        core_pos = core.data.root_pos_w[env_id]
        core_quat_inv = quat_inv(core.data.root_quat_w[env_id : env_id + 1])[0]
        for cubie_id in selected_ids.tolist():
            key = CORNER_NAMES[cubie_id].lower()
            actual_pos = cubies.data.object_link_pos_w[
                env_id, self._cube_cubie_ids[cubie_id]
            ]
            actual_quat = cubies.data.object_link_quat_w[
                env_id, self._cube_cubie_ids[cubie_id]
            ]
            local_pos = quat_apply(
                core_quat_inv[None], (actual_pos - core_pos)[None]
            )[0]
            local_quat = quat_mul(core_quat_inv[None], actual_quat[None])[0]
            self._set_fixed_frame(handles["core"][key], local_pos, local_quat)

    @staticmethod
    def _sync_usd_body_pose(
        prim_path: str, position_w: torch.Tensor, quaternion_w: torch.Tensor
    ) -> None:
        """Mirror one live Fabric pose into USD without changing its value.

        Runtime USD joint creation reads body transforms from the USD stage,
        while GPU PhysX/Fabric keeps dynamic body transforms outside USD.  A
        switched joint therefore compares a current tensor frame with a stale
        reset-time body frame unless the latter is synchronized first.
        """

        stage = sim_utils.get_current_stage()
        prim = stage.GetPrimAtPath(prim_path)
        if not prim.IsValid():
            raise RuntimeError(f"missing rigid body prim for joint sync: {prim_path}")
        position = tuple(float(value) for value in position_w.tolist())
        quaternion = tuple(float(value) for value in quaternion_w.tolist())
        local_pos, local_quat = sim_utils.convert_world_pose_to_local(
            position, quaternion, prim.GetParent()
        )
        translate_attr = prim.GetAttribute("xformOp:translate")
        orient_attr = prim.GetAttribute("xformOp:orient")
        if not translate_attr.IsValid() or not orient_attr.IsValid():
            raise RuntimeError(f"rigid body lacks standard xform ops: {prim_path}")
        current_translation = translate_attr.Get()
        current_orientation = orient_attr.Get()
        vec_type = Gf.Vec3f if isinstance(current_translation, Gf.Vec3f) else Gf.Vec3d
        quat_type = Gf.Quatf if isinstance(current_orientation, Gf.Quatf) else Gf.Quatd
        quat_vec_type = Gf.Vec3f if quat_type is Gf.Quatf else Gf.Vec3d
        translate_attr.Set(vec_type(*local_pos))
        orient_attr.Set(
            quat_type(
                float(local_quat[0]),
                quat_vec_type(
                    float(local_quat[1]),
                    float(local_quat[2]),
                    float(local_quat[3]),
                ),
            )
        )

    def _sync_reindex_bodies_to_usd(
        self, env_id: int, selected_ids: torch.Tensor
    ) -> None:
        """Synchronize every body referenced by the next switched joints."""

        root = self._cube_env_roots[env_id]
        core = self.scene["pocket_cube"]
        carrier = self.scene["pocket_cube_carrier"]
        cubies = self.scene["pocket_cubies"]
        self._sync_usd_body_pose(
            f"{root}/PocketCube/Core",
            core.data.root_pos_w[env_id],
            core.data.root_quat_w[env_id],
        )
        self._sync_usd_body_pose(
            f"{root}/PocketCube/Carrier",
            carrier.data.root_pos_w[env_id],
            carrier.data.root_quat_w[env_id],
        )
        for cubie_id in selected_ids.tolist():
            self._sync_usd_body_pose(
                f"{root}/PocketCube/Cubies/Cubie_{CORNER_NAMES[cubie_id].lower()}",
                cubies.data.object_link_pos_w[
                    env_id, self._cube_cubie_ids[cubie_id]
                ],
                cubies.data.object_link_quat_w[
                    env_id, self._cube_cubie_ids[cubie_id]
                ],
            )

    def _start_ordered_reindex(self, env_id: int, next_face: int) -> None:
        """Start a no-snap handoff from the latched layer to the next layer."""

        if int(self._cube_latched_face[env_id]) < 0:
            raise RuntimeError("ordered reindex requested without a latched layer")
        selected_ids = self._cube_latched_ids[env_id]
        if bool(torch.any(selected_ids < 0)):
            raise RuntimeError("ordered reindex lost the latched cubie ids")
        # Only author frames here.  The fixed joints are enabled after another
        # simulation step, when PhysX and the scene tensors agree on them.
        # Fabric does not write dynamic body transforms back to USD.  Mirror
        # the unchanged live poses and the matching joint anchors in one USD
        # notice so the joint creator never observes mixed reference frames.
        with Sdf.ChangeBlock():
            self._sync_reindex_bodies_to_usd(env_id, selected_ids)
            self._prepare_core_lock_frames_for_ids(env_id, selected_ids)
        self._cube_reindex_next_face[env_id] = next_face
        self._cube_reindex_phase[env_id] = 1

    def _advance_ordered_reindex(self) -> None:
        """Advance one stage of the physical carrier reindex state machine."""

        for env_id in torch.nonzero(
            self._cube_reindex_phase > 0, as_tuple=False
        ).squeeze(-1).tolist():
            phase = int(self._cube_reindex_phase[env_id])
            handles = self._cube_joint_handles[env_id]
            if phase == 1:
                # The previous layer is still held by its 90-degree hinge, so
                # the frames authored one step ago remain coincident.  Transfer
                # those cubies to Core before detaching the empty carrier.
                for cubie_id in self._cube_latched_ids[env_id].tolist():
                    key = CORNER_NAMES[cubie_id].lower()
                    self._enable(handles["carrier"][key], False)
                    self._enable(handles["core"][key], True)
                old_face = int(self._cube_latched_face[env_id])
                self._enable(handles["hinges"][self.FACE_HINGE_AXIS[old_face]], False)

                core = self.scene["pocket_cube"]
                carrier = self.scene["pocket_cube_carrier"]
                carrier.write_root_state_to_sim(
                    core.data.root_state_w[env_id : env_id + 1].clone(),
                    env_ids=torch.tensor([env_id], device=self.device),
                )
                self._cube_latched_face[env_id] = -1
                self._cube_latched_ids[env_id] = -1
                self._cube_reindex_phase[env_id] = 2
            elif phase == 2:
                # The empty carrier pose write has now crossed a physics step.
                # Author the next layer's live carrier frames, but do not yet
                # enable those joints in this same update.
                next_face = int(self._cube_reindex_next_face[env_id])
                positions = torch.tensor(
                    FACE_CORNER_POSITIONS[next_face],
                    dtype=torch.long,
                    device=self.device,
                )
                selected_ids = self._cube_permutation[env_id, positions]
                with Sdf.ChangeBlock():
                    self._sync_reindex_bodies_to_usd(env_id, selected_ids)
                    self._prepare_carrier_lock_frames(env_id, next_face)
                self._cube_reindex_phase[env_id] = 3
            elif phase == 3:
                next_face = int(self._cube_reindex_next_face[env_id])
                positions = torch.tensor(
                    FACE_CORNER_POSITIONS[next_face],
                    dtype=torch.long,
                    device=self.device,
                )
                selected_ids = self._cube_permutation[env_id, positions]
                for cubie_id in selected_ids.tolist():
                    key = CORNER_NAMES[cubie_id].lower()
                    self._enable(handles["core"][key], False)
                    self._enable(handles["carrier"][key], True)
                for axis, hinge in handles["hinges"].items():
                    enabled = axis == self.FACE_HINGE_AXIS[next_face]
                    self._enable(hinge, enabled)
                    if enabled:
                        self._set_hinge_limits(hinge, 0.0, 0.05)
                self._cube_armed_face[env_id] = next_face
                self._cube_order_arm_quiet_steps[env_id] = 0
                self._cube_reindex_next_face[env_id] = -1
                self._cube_reindex_phase[env_id] = 0
            else:
                raise RuntimeError(f"invalid pocket-cube reindex phase: {phase}")

    def _begin_turn(self, env_id: int, face_id: int) -> None:
        ordered_prearmed = bool(
            getattr(self.cfg, "enforce_target_face_order", True)
        )
        if self._cube_preconfigured_face >= 0 or ordered_prearmed:
            if self._cube_preconfigured_face >= 0:
                expected_face = self._cube_preconfigured_face
            else:
                move_index = int(self._cube_committed_turns[env_id])
                expected_face = FACE_NAMES.index(
                    str(tuple(self.cfg.target_moves)[move_index][0]).upper()
                )
            if (
                face_id != expected_face
                or int(self._cube_armed_face[env_id]) != expected_face
            ):
                # The single-target mechanism physically locks every other
                # layer.  A support grasp can therefore register projected
                # torque on a locked candidate without creating a face turn;
                # ignore it and wait for qualifying torque on the configured
                # L hinge.  Any actual non-L motion remains impossible through
                # the fixed Core locks and is still covered by finite/workspace
                # and final-state checks.
                return
            handles = self._cube_joint_handles[env_id]
            positions = torch.tensor(
                FACE_CORNER_POSITIONS[face_id], dtype=torch.long, device=self.device
            )
            self._cube_selected_ids[env_id] = self._cube_permutation[env_id, positions]
            hinge = handles["hinges"][self.FACE_HINGE_AXIS[face_id]]
            self._set_hinge_limits(hinge, 0.0, 95.0)
            self.pocket_cube_active_face[env_id] = face_id
            self._cube_active_steps[env_id] = 0
            self._cube_contact_driven_ready[env_id] = False
            return
        self._prepare_carrier_lock_frames(env_id, face_id)
        handles = self._cube_joint_handles[env_id]
        positions = torch.tensor(
            FACE_CORNER_POSITIONS[face_id], dtype=torch.long, device=self.device
        )
        selected_ids = self._cube_permutation[env_id, positions]
        self._cube_selected_ids[env_id] = selected_ids
        for cubie_id in selected_ids.tolist():
            key = CORNER_NAMES[cubie_id].lower()
            self._enable(handles["core"][key], False)
            self._enable(handles["carrier"][key], True)
        self._enable(handles["core_carrier"], False)
        for axis, hinge in handles["hinges"].items():
            self._enable(hinge, axis == self.FACE_HINGE_AXIS[face_id])
        self.pocket_cube_active_face[env_id] = face_id
        self._cube_active_steps[env_id] = 0
        self._cube_contact_driven_ready[env_id] = False

    def _arm_ordered_face_at_grid(self, env_id: int, face_id: int) -> None:
        """Preselect the next requested face at a zero/quarter-turn detent.

        This is the multi-move counterpart of the reset-time preconfiguration:
        ownership changes only after the previous face has snapped to its
        exact grid pose, never after a loaded contact has started a turn.
        """

        self._prepare_carrier_lock_frames(env_id, face_id)
        handles = self._cube_joint_handles[env_id]
        positions = torch.tensor(
            FACE_CORNER_POSITIONS[face_id], dtype=torch.long, device=self.device
        )
        selected_ids = self._cube_permutation[env_id, positions]
        for cubie_id in selected_ids.tolist():
            key = CORNER_NAMES[cubie_id].lower()
            self._enable(handles["core"][key], False)
            self._enable(handles["carrier"][key], True)
        self._enable(handles["core_carrier"], False)
        for axis, hinge in handles["hinges"].items():
            enabled = axis == self.FACE_HINGE_AXIS[face_id]
            self._enable(hinge, enabled)
            if enabled:
                self._set_hinge_limits(hinge, 0.0, 0.05)
        self._cube_armed_face[env_id] = face_id
        self._cube_order_arm_quiet_steps[env_id] = 0

    def _apply_move(self, env_id: int, face_id: int, direction: int) -> None:
        face = FACE_NAMES[face_id]
        source, delta = _MOVE_TABLES[face]
        source_t = torch.tensor(source, dtype=torch.long, device=self.device)
        delta_t = torch.tensor(delta, dtype=torch.long, device=self.device)
        axis = torch.tensor(FACE_AXES[face_id], dtype=torch.float32, device=self.device)
        turn_quat = quat_from_angle_axis(
            torch.tensor([QUARTER_TURN], device=self.device), axis.unsqueeze(0)
        )[0]
        repetitions = 1 if direction > 0 else 3
        for _ in range(repetitions):
            old_perm = self._cube_permutation[env_id].clone()
            old_ori = self._cube_orientation[env_id].clone()
            positions = torch.tensor(
                FACE_CORNER_POSITIONS[face_id], dtype=torch.long, device=self.device
            )
            ids = old_perm[positions]
            self._cube_cubie_quat[env_id, ids] = quat_mul(
                turn_quat.expand(4, -1), self._cube_cubie_quat[env_id, ids]
            )
            self._cube_permutation[env_id] = old_perm[source_t]
            self._cube_orientation[env_id] = (old_ori[source_t] + delta_t) % 3

    def _snap_selected_to_grid(self, env_id: int) -> None:
        """Snap only the active layer, after it enters the +/-90 degree pocket."""

        core = self.scene["pocket_cube"]
        cubies = self.scene["pocket_cubies"]
        selected = self._cube_selected_ids[env_id]
        states = torch.zeros((1, 4, 13), dtype=torch.float32, device=self.device)
        root_pos = core.data.root_pos_w[env_id]
        root_quat = core.data.root_quat_w[env_id]
        root_lin = core.data.root_lin_vel_w[env_id]
        root_ang = core.data.root_ang_vel_w[env_id]
        local_positions = []
        for row, cubie_id in enumerate(selected.tolist()):
            position_id = int(
                torch.nonzero(self._cube_permutation[env_id] == cubie_id, as_tuple=False)[0]
            )
            local_pos = self._cube_solved_centers[position_id]
            local_quat = self._cube_cubie_quat[env_id, cubie_id]
            radial = quat_apply(root_quat[None], local_pos[None])[0]
            states[0, row, :3] = root_pos + radial
            states[0, row, 3:7] = quat_mul(root_quat[None], local_quat[None])[0]
            states[0, row, 7:10] = root_lin + torch.linalg.cross(root_ang, radial)
            states[0, row, 10:13] = root_ang
            local_positions.append((cubie_id, local_pos, local_quat))
        cubies.write_object_state_to_sim(
            states,
            env_ids=torch.tensor([env_id], device=self.device),
            object_ids=selected,
        )

        handles = self._cube_joint_handles[env_id]
        active_axis = self.FACE_HINGE_AXIS[int(self.pocket_cube_active_face[env_id])]
        self._enable(handles["hinges"][active_axis], False)
        for cubie_id, local_pos, local_quat in local_positions:
            key = CORNER_NAMES[cubie_id].lower()
            self._enable(handles["carrier"][key], False)
            self._set_fixed_frame(handles["core"][key], local_pos, local_quat)
            self._enable(handles["core"][key], True)

        carrier = self.scene["pocket_cube_carrier"]
        carrier_state = core.data.root_state_w[env_id : env_id + 1].clone()
        carrier.write_root_state_to_sim(
            carrier_state, env_ids=torch.tensor([env_id], device=self.device)
        )
        self._enable(handles["core_carrier"], True)

    def _finish_turn(self, env_id: int, direction: int) -> None:
        face_id = int(self.pocket_cube_active_face[env_id])
        self._apply_move(env_id, face_id, direction)
        self._cube_face_angles[env_id, face_id] += direction * QUARTER_TURN
        if self._cube_preconfigured_face >= 0:
            hinge = self._cube_joint_handles[env_id]["hinges"][
                self.FACE_HINGE_AXIS[face_id]
            ]
            # ``direction`` is expressed in the public face convention, while
            # the authored revolute joint uses its raw local-axis convention.
            # In particular R has FACE_AXIS_SIGN == -1.  Applying the public
            # sign directly made an R layer that had smoothly reached its
            # quarter turn get pulled toward the opposite raw hinge limit at
            # commit, producing an unphysical visible jump.  Convert back to
            # the joint coordinate so latching preserves the live pose.
            raw_hinge_center_deg = (
                direction * 90.0 * self.FACE_AXIS_SIGN[face_id]
            )
            self._set_hinge_limits(hinge, raw_hinge_center_deg, 0.05)
            self._cube_committed_turns[env_id] += 1
            self._cube_latched_face[env_id] = face_id
            self.pocket_cube_active_face[env_id] = -1
            self._cube_selected_ids[env_id] = -1
            self._cube_contact_driven_ready[env_id] = False
            return
        # Keep the genuinely contact-driven carrier pose and latch its live
        # revolute joint at the reached quarter turn.  In particular, do not
        # teleport the four cubies onto an ideal grid and immediately create
        # fixed joints from stale transforms.
        hinge = self._cube_joint_handles[env_id]["hinges"][
            self.FACE_HINGE_AXIS[face_id]
        ]
        raw_hinge_center_deg = direction * 90.0 * self.FACE_AXIS_SIGN[face_id]
        self._set_hinge_limits(hinge, raw_hinge_center_deg, 0.05)
        self._cube_latched_ids[env_id] = self._cube_selected_ids[env_id].clone()
        self._cube_committed_turns[env_id] += 1
        self._cube_latched_face[env_id] = face_id
        self.pocket_cube_active_face[env_id] = -1
        self._cube_selected_ids[env_id] = -1
        self._cube_contact_driven_ready[env_id] = False
        if bool(getattr(self.cfg, "enforce_target_face_order", True)):
            move_index = int(self._cube_committed_turns[env_id])
            moves = tuple(self.cfg.target_moves)
            if move_index < len(moves):
                # Keep every cubie on Core until the robot has unloaded the
                # just-finished layer.  The next face is armed later from
                # _update_pocket_cube_interlock after several quiet contact
                # steps, so a trailing wrist motion cannot accidentally start
                # the next requested hinge.
                self._cube_armed_face[env_id] = -1
                self._cube_order_arm_quiet_steps[env_id] = 0

    def _cancel_turn_at_zero(self, env_id: int) -> None:
        if self._cube_preconfigured_face >= 0 or bool(
            getattr(self.cfg, "enforce_target_face_order", True)
        ):
            face_id = int(self.pocket_cube_active_face[env_id])
            hinge = self._cube_joint_handles[env_id]["hinges"][
                self.FACE_HINGE_AXIS[face_id]
            ]
            self._set_hinge_limits(hinge, 0.0, 0.05)
            self.pocket_cube_active_face[env_id] = -1
            self._cube_selected_ids[env_id] = -1
            self._cube_contact_driven_ready[env_id] = False
            return
        # The logical state is unchanged; the same helper restores its exact
        # current grid poses.  This is allowed only inside the 0-degree pocket.
        self._snap_selected_to_grid(env_id)
        self.pocket_cube_active_face[env_id] = -1
        self._cube_selected_ids[env_id] = -1
        self._cube_contact_driven_ready[env_id] = False

    def _set_local_snap_torques(self) -> None:
        """Apply detent torque only near 0 or +/-90 degrees, never mid-turn."""

        core = self.scene["pocket_cube"]
        carrier = self.scene["pocket_cube_carrier"]
        displacement, velocity = self._carrier_displacement_and_velocity()
        carrier_torque = torch.zeros((self.num_envs, 1, 3), device=self.device)
        core_torque = torch.zeros_like(carrier_torque)
        for env_id in range(self.num_envs):
            face_id = int(self.pocket_cube_active_face[env_id])
            if face_id < 0:
                continue
            angle = float(displacement[env_id])
            candidates = (-QUARTER_TURN, 0.0, QUARTER_TURN)
            target = min(candidates, key=lambda value: abs(angle - value))
            error = target - angle
            if abs(error) > self.SNAP_CAPTURE_ANGLE:
                continue
            face_torque = self.DETENT_STIFFNESS * error - self.DETENT_DAMPING * float(
                velocity[env_id]
            )
            face_torque = max(-self.DETENT_MAX_TORQUE, min(self.DETENT_MAX_TORQUE, face_torque))
            axis_id = self.FACE_AXIS_INDEX[face_id]
            local_axis = torch.zeros(3, device=self.device)
            local_axis[axis_id] = self.FACE_AXIS_SIGN[face_id]
            world_axis = quat_apply(core.data.root_quat_w[env_id : env_id + 1], local_axis[None])[0]
            carrier_torque[env_id, 0] = face_torque * world_axis
            core_torque[env_id, 0] = -carrier_torque[env_id, 0]

        # A committed one-turn mechanism stays as a live revolute joint at its
        # narrow physical limit.  GPU PhysX can retain a small relative angular
        # velocity inside that limit even while its pose looks stationary.
        # Dissipate that energy with a physical viscous torque; this neither
        # writes a pose nor alters the logical cube state.
        relative_omega = carrier.data.root_ang_vel_w - core.data.root_ang_vel_w
        latched_envs = torch.nonzero(
            (self.pocket_cube_active_face < 0) & (self._cube_latched_face >= 0),
            as_tuple=False,
        ).squeeze(-1)
        for env_id in latched_envs.tolist():
            face_id = int(self._cube_latched_face[env_id])
            axis_id = self.FACE_AXIS_INDEX[face_id]
            local_axis = torch.zeros(3, device=self.device)
            local_axis[axis_id] = self.FACE_AXIS_SIGN[face_id]
            world_axis = quat_apply(
                core.data.root_quat_w[env_id : env_id + 1], local_axis[None]
            )[0]
            public_speed = float(torch.dot(relative_omega[env_id], world_axis))
            damping_torque = max(
                -self.LATCH_MAX_DAMPING_TORQUE,
                min(
                    self.LATCH_MAX_DAMPING_TORQUE,
                    -self.LATCH_DAMPING * public_speed,
                ),
            )
            carrier_torque[env_id, 0] = damping_torque * world_axis
            core_torque[env_id, 0] = -carrier_torque[env_id, 0]
        carrier.instantaneous_wrench_composer.set_forces_and_torques(
            torques=carrier_torque, is_global=True
        )
        core.instantaneous_wrench_composer.set_forces_and_torques(
            torques=core_torque, is_global=True
        )

    def _update_pocket_cube_interlock(self) -> None:
        core = self.scene["pocket_cube"]
        carrier = self.scene["pocket_cube_carrier"]
        cubies = self.scene["pocket_cubies"]
        finite = (
            torch.isfinite(core.data.root_state_w).all(dim=-1)
            & torch.isfinite(carrier.data.root_state_w).all(dim=-1)
            & torch.isfinite(cubies.data.object_link_state_w).all(dim=(-1, -2))
        )
        self.pocket_cube_rule_failed |= ~finite
        cube_penetration, tool_ids, cubie_ids = (
            self._robot_cube_visible_shell_penetration()
        )
        support_penetration, support_pair_ids = (
            self._support_visible_shell_penetration()
        )
        penetration = torch.maximum(cube_penetration, support_penetration)
        self._cube_max_shell_penetration = torch.maximum(
            self._cube_max_shell_penetration, penetration
        )
        penetration_failed = penetration > self.MAX_VISIBLE_SHELL_PENETRATION
        for env_id in torch.nonzero(penetration_failed, as_tuple=False).squeeze(-1).tolist():
            if self._cube_first_penetration[env_id] is None:
                if float(cube_penetration[env_id]) >= float(
                    support_penetration[env_id]
                ):
                    cubie_id = int(cubie_ids[env_id])
                    object_a = self._robot_tool_names[int(tool_ids[env_id])]
                    object_b = f"cubie_{CORNER_NAMES[cubie_id]}"
                else:
                    object_a, object_b = self._support_penetration_pair_names[
                        int(support_pair_ids[env_id])
                    ]
                self._cube_first_penetration[env_id] = {
                    "object_a": object_a,
                    "object_b": object_b,
                    "tool": object_a,
                    "cubie": object_b.removeprefix("cubie_"),
                    "penetration_depth_m": float(penetration[env_id]),
                    "tolerance_m": self.MAX_VISIBLE_SHELL_PENETRATION,
                }
        self.pocket_cube_rule_failed |= penetration_failed
        torque_by_face, force_by_face = self._robot_contact_wrench_by_face()

        # Joint ownership and empty-carrier pose changes are intentionally
        # separated by real physics steps.  Advance before looking for a new
        # turn so a newly armed hinge cannot consume stale contact data.
        self._advance_ordered_reindex()

        if bool(getattr(self.cfg, "enforce_target_face_order", True)):
            pending_envs = torch.nonzero(
                (self.pocket_cube_active_face < 0)
                & (self._cube_armed_face < 0)
                & (self._cube_reindex_phase == 0)
                & (self._cube_committed_turns < len(tuple(self.cfg.target_moves)))
                & ~self.pocket_cube_rule_failed,
                as_tuple=False,
            ).squeeze(-1)
            for env_id in pending_envs.tolist():
                quiet_dwell_steps = 350
                if float(force_by_face[env_id].abs().max()) < self.MIN_CONTACT_FORCE:
                    self._cube_order_arm_quiet_steps[env_id] += 1
                elif int(self._cube_order_arm_quiet_steps[env_id]) < quiet_dwell_steps:
                    self._cube_order_arm_quiet_steps[env_id] = 0
                # Reindex only while both hands are unloaded and the cube is
                # resting.  Requiring a prior lift creates a physical cycle:
                # the just-turned layer is still carried by its 90-degree
                # hinge, while the opposite-layer pickup needs the cube to be
                # rigidly reassembled before it can lift.  The staged handoff
                # below changes no cubie pose and is safest on the pedestal.
                if int(self._cube_order_arm_quiet_steps[env_id]) >= quiet_dwell_steps:
                    move_index = int(self._cube_committed_turns[env_id])
                    next_face = FACE_NAMES.index(
                        str(tuple(self.cfg.target_moves)[move_index][0]).upper()
                    )
                    self._start_ordered_reindex(env_id, next_face)

        ordered_idle_ready = (
            (self._cube_armed_face >= 0) & (self._cube_reindex_phase == 0)
            if bool(getattr(self.cfg, "enforce_target_face_order", True))
            else torch.ones(self.num_envs, dtype=torch.bool, device=self.device)
        )
        idle_envs = torch.nonzero(
            (self.pocket_cube_active_face < 0)
            & (self._cube_committed_turns < len(tuple(self.cfg.target_moves)))
            & ordered_idle_ready
            & ~self.pocket_cube_rule_failed,
            as_tuple=False,
        ).squeeze(-1)
        for env_id in idle_envs.tolist():
            if self._cube_preconfigured_face >= 0:
                face_id = self._cube_preconfigured_face
                magnitude = torque_by_face[env_id, face_id].abs()
            elif bool(getattr(self.cfg, "enforce_target_face_order", True)):
                move_index = int(self._cube_committed_turns[env_id])
                requested_face = str(tuple(self.cfg.target_moves)[move_index][0]).upper()
                face_id = FACE_NAMES.index(requested_face)
                magnitude = torque_by_face[env_id, face_id].abs()
            else:
                magnitude, face_id_t = torque_by_face[env_id].abs().max(dim=0)
                face_id = int(face_id_t)
            if (
                float(magnitude) >= self.MIN_TURN_TORQUE
                and float(force_by_face[env_id, face_id]) >= self.MIN_CONTACT_FORCE
            ):
                self._begin_turn(env_id, face_id)

        displacement, velocity = self._carrier_displacement_and_velocity()
        active_envs = torch.nonzero(
            (self.pocket_cube_active_face >= 0) & ~self.pocket_cube_rule_failed,
            as_tuple=False,
        ).squeeze(-1)
        for env_id in active_envs.tolist():
            self._cube_active_steps[env_id] += 1
            face_id = int(self.pocket_cube_active_face[env_id])
            angle = float(displacement[env_id])
            speed = float(velocity[env_id])
            if abs(angle) > QUARTER_TURN + self.HINGE_OVERTRAVEL + math.radians(0.5):
                self.pocket_cube_rule_failed[env_id] = True
                continue
            if (
                abs(angle) >= self.MIN_CONTACT_DRIVEN_ANGLE
                and float(force_by_face[env_id, face_id]) >= self.MIN_CONTACT_FORCE
            ):
                self._cube_contact_driven_ready[env_id] = True
            near_quarter = abs(abs(angle) - QUARTER_TURN) <= self.SNAP_FINISH_TOLERANCE
            if near_quarter and bool(self._cube_contact_driven_ready[env_id]):
                self._finish_turn(env_id, 1 if angle > 0.0 else -1)
                continue
            near_zero = abs(angle) <= self.SNAP_FINISH_TOLERANCE
            contact_released = float(force_by_face[env_id, face_id]) < self.MIN_CONTACT_FORCE
            if (
                near_zero
                and contact_released
                and abs(speed) <= self.CANCEL_SPEED
                and int(self._cube_active_steps[env_id]) >= self.CANCEL_MIN_STEPS
            ):
                self._cancel_turn_at_zero(env_id)

        self._refresh_state_observation()

    def _refresh_state_observation(self) -> None:
        self.pocket_cube_state_tensor = torch.cat(
            (self._cube_permutation, self._cube_orientation), dim=-1
        ).to(torch.float32)
        self.pocket_cube_success = torch.all(
            self.pocket_cube_state_tensor == self.pocket_cube_target_tensor, dim=-1
        ) & ~self.pocket_cube_rule_failed

    def step(self, action: torch.Tensor):
        self.action_manager.process_action(action.to(self.device))
        self.recorder_manager.record_pre_step()
        is_rendering = self.sim.has_gui() or self.sim.has_rtx_sensors()
        for _ in range(self.cfg.decimation):
            self._sim_step_counter += 1
            self.action_manager.apply_action()
            self._set_local_snap_torques()
            self.scene.write_data_to_sim()
            self.sim.step(render=False)
            self.scene.update(dt=self.physics_dt)
            self._update_pocket_cube_interlock()
            if getattr(self, 'benchmark_stop_requested', False):
                break
            if self._sim_step_counter % self.cfg.sim.render_interval == 0 and is_rendering:
                self.sync_pocket_cube_visuals()
                self.sim.render()

        if "interval" in self.event_manager.available_modes:
            self.event_manager.apply(mode="interval", dt=self.step_dt)
        self.obs_buf = self.observation_manager.compute(update_history=True)
        self.extras["pocket_cube"] = {
            "active_face": self.pocket_cube_active_face.clone(),
            "rule_failed": self.pocket_cube_rule_failed.clone(),
            "committed_turns": self._cube_committed_turns.clone(),
            "max_visible_shell_penetration_m": self._cube_max_shell_penetration.clone(),
            "success": self.pocket_cube_success.clone(),
        }
        self.recorder_manager.record_post_step()
        return self.obs_buf, self.extras

    def __init__(self, cfg):
        super().__init__(cfg)
        self.single_observation_space = gym.spaces.Dict()
        for group_name in self.observation_manager.active_terms:
            group_dim = self.observation_manager.group_obs_dim[group_name]
            self.single_observation_space[group_name] = gym.spaces.Box(
                low=-np.inf, high=np.inf, shape=group_dim, dtype=np.float32
            )
        action_dim = sum(self.action_manager.action_term_dim)
        self.single_action_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(action_dim,), dtype=np.float32
        )
        self.observation_space = gym.vector.utils.batch_space(
            self.single_observation_space, self.num_envs
        )
        self.action_space = gym.vector.utils.batch_space(
            self.single_action_space, self.num_envs
        )
