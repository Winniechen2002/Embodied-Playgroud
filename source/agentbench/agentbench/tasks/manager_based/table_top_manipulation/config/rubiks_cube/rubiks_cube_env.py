"""Isaac Lab runtime for the hybrid 26-cubie Rubik's Cube."""

from __future__ import annotations

import math
from dataclasses import replace
from typing import Sequence

import torch

from isaaclab.envs import ManagerBasedEnv
from isaaclab.utils.math import quat_apply, subtract_frame_transforms

from .rubiks_cube_cfg import CUBIE_IDS
from .rubiks_cube_mechanism import (
    CarrierAngleTracker,
    ConstraintFrame,
    CubeReorientationMechanism,
    HybridCubeMechanism,
    MechanismPhase,
    ReorientationObservation,
    ReorientationPhase,
    TurnObservation,
    passive_detent_torques,
)
from .rubiks_cube_native_observation import evaluate_native_cube_window, read_native_cube_sample
from .rubiks_cube_reset import (
    CubeResetExecutionError,
    CubeResetSpec,
    build_reset_body_transforms,
    build_reset_constraint_frames,
    build_reset_core_transform,
    build_reset_world_anchor_frame,
    snapshot_cube_state,
    snapshot_reset_spec,
)
from .rubiks_cube_rules import CubeFrame, CubeState, FACE_AXIS_SIGN, parse_sequence
from .rubiks_cube_usd_backend import PxrJointEditor, UsdConstraintBackend


class RubiksCubeEnv(ManagerBasedEnv):
    """Non-RL environment exposing atomic hybrid-cube transitions.

    Direct cubie state writes occur only in :meth:`_reset_idx`.  During a move,
    the environment changes fixed-joint membership and applies a passive,
    target-independent periodic detent torque to all three carriers.
    """

    def __init__(self, cfg, initial_reset_spec: CubeResetSpec | None = None):
        # Own and validate all caller input before superclass construction can reset.
        self._initial_reset_spec = (
            snapshot_reset_spec(initial_reset_spec) if initial_reset_spec is not None else None
        )
        self.cube_state = (
            snapshot_cube_state(self._initial_reset_spec.cube_state)
            if self._initial_reset_spec is not None else CubeState.solved()
        )
        self.active_cube_face: str | None = None
        self.active_cube_axis: str | None = None
        self.active_cube_angle_rad = 0.0
        self.active_cube_angular_velocity_rad_s = 0.0
        self._idle_detent_axis: str | None = None
        self.used_direct_cubie_state_during_move = False
        self.used_direct_cubie_state_during_reset = False
        self.used_direct_core_pose_during_move = False
        self._mechanism: HybridCubeMechanism | None = None
        self._reorientation: CubeReorientationMechanism | None = None
        try:
            super().__init__(cfg)
            if self.num_envs != 1:
                raise ValueError("hybrid cube constraint switching currently requires num_envs=1")

            parts = self.scene["cube_parts"]
            self._part_index = {name: index for index, name in enumerate(parts.object_names)}
            missing = set(
                ("world_anchor", "core", "carrier_x", "carrier_y", "carrier_z", *CUBIE_IDS)
            ) - set(self._part_index)
            if missing:
                raise RuntimeError(f"cube collection is missing bodies: {sorted(missing)}")
            self._carrier_indices = torch.tensor(
                [self._part_index[f"carrier_{axis}"] for axis in "xyz"],
                dtype=torch.long,
                device=self.device,
            )

            from omni.usd import get_context

            root_path = "/World/envs/env_0/RubiksCube"
            backend = UsdConstraintBackend(
                root_path=root_path,
                cubie_ids=CUBIE_IDS,
                editor=PxrJointEditor(get_context().get_stage()),
            )
            self._mechanism = HybridCubeMechanism(backend, self.cube_state)
            self._reorientation = CubeReorientationMechanism(backend)
            self._angle_trackers = {axis: CarrierAngleTracker() for axis in "xyz"}
            self._zero_carrier_torques()
        except BaseException as error:
            if self._initial_reset_spec is None:
                raise
            crossed_write_boundary = bool(
                self.used_direct_cubie_state_during_reset
                or getattr(error, "used_direct_cubie_state_during_reset", False)
            )
            if isinstance(error, CubeResetExecutionError) and (
                error.used_direct_cubie_state_during_reset == crossed_write_boundary
            ):
                raise
            raise CubeResetExecutionError(
                f"{type(error).__name__}: {error}",
                used_direct_cubie_state_during_reset=crossed_write_boundary,
            ) from error

    @property
    def mechanism(self) -> HybridCubeMechanism:
        if self._mechanism is None:
            raise RuntimeError("hybrid cube mechanism has not initialized")
        return self._mechanism

    @property
    def reorientation(self) -> CubeReorientationMechanism:
        if self._reorientation is None:
            raise RuntimeError("cube reorientation mechanism has not initialized")
        return self._reorientation

    @property
    def cube_frame(self) -> CubeFrame:
        if self._reorientation is None:
            return (
                self._initial_reset_spec.logical_orientation
                if self._initial_reset_spec is not None else CubeFrame.identity()
            )
        return self._reorientation.cube_frame

    def _relative_frames(self, reference_name: str, cubie_ids: Sequence[str]) -> dict[str, ConstraintFrame]:
        parts = self.scene["cube_parts"]
        reference_index = self._part_index[reference_name]
        reference_pos = parts.data.object_link_pos_w[:, reference_index]
        reference_quat = parts.data.object_link_quat_w[:, reference_index]
        frames: dict[str, ConstraintFrame] = {}
        for cubie_id in cubie_ids:
            cubie_index = self._part_index[cubie_id]
            position, quaternion = subtract_frame_transforms(
                reference_pos,
                reference_quat,
                parts.data.object_link_pos_w[:, cubie_index],
                parts.data.object_link_quat_w[:, cubie_index],
            )
            frames[cubie_id] = ConstraintFrame(
                position=tuple(float(value) for value in position[0].tolist()),
                quaternion=tuple(float(value) for value in quaternion[0].tolist()),
            )
        return frames

    def _relative_frame(self, reference_name: str, target_name: str) -> ConstraintFrame:
        return self._relative_frames(reference_name, (target_name,))[target_name]

    def _carrier_measurement(self, axis: str) -> tuple[float, float]:
        parts = self.scene["cube_parts"]
        core_index = self._part_index["core"]
        carrier_index = self._part_index[f"carrier_{axis}"]
        _, relative_quaternion = subtract_frame_transforms(
            parts.data.object_link_pos_w[:, core_index],
            parts.data.object_link_quat_w[:, core_index],
            parts.data.object_link_pos_w[:, carrier_index],
            parts.data.object_link_quat_w[:, carrier_index],
        )
        component_index = {"x": 1, "y": 2, "z": 3}[axis]
        wrapped_angle = 2.0 * math.atan2(
            float(relative_quaternion[0, component_index]),
            float(relative_quaternion[0, 0]),
        )
        wrapped_angle = math.atan2(math.sin(wrapped_angle), math.cos(wrapped_angle))
        angle = self._angle_trackers[axis].update(wrapped_angle)
        local_axis = torch.zeros((self.num_envs, 3), device=self.device)
        local_axis[:, "xyz".index(axis)] = 1.0
        hinge_axis_w = quat_apply(
            parts.data.object_link_quat_w[:, core_index], local_axis
        )
        relative_angular_velocity_w = (
            parts.data.object_link_vel_w[:, carrier_index, 3:]
            - parts.data.object_link_vel_w[:, core_index, 3:]
        )
        angular_velocity = float(
            torch.sum(relative_angular_velocity_w * hinge_axis_w, dim=-1)[0]
        )
        return angle, angular_velocity

    def refresh_active_turn_state(self) -> tuple[float, float]:
        if self.active_cube_axis is None:
            self.active_cube_angle_rad = 0.0
            self.active_cube_angular_velocity_rad_s = 0.0
        else:
            self.active_cube_angle_rad, self.active_cube_angular_velocity_rad_s = (
                self._carrier_measurement(self.active_cube_axis)
            )
        return self.active_cube_angle_rad, self.active_cube_angular_velocity_rad_s

    def begin_cube_turn(self, move: str) -> tuple[str, ...]:
        if self._idle_detent_axis is not None:
            raise RuntimeError("cannot begin a cube turn while an idle carrier is settling")
        if self.reorientation.phase is not ReorientationPhase.ANCHORED:
            raise RuntimeError("cannot begin a face turn during whole-cube reorientation")
        atomic = parse_sequence((move,))
        if len(atomic) != 1:
            raise ValueError("begin_cube_turn requires one atomic quarter turn")
        canonical = atomic[0]
        face = canonical[0]
        axis = FACE_AXIS_SIGN[face][0].lower()
        angle, _ = self._carrier_measurement(axis)
        active = self.cube_state.active_cubie_ids(face)
        frames = self._relative_frames(f"carrier_{axis}", active)
        selected = self.mechanism.begin_turn(canonical, frames, initial_angle_rad=angle)
        self.active_cube_face = face
        self.active_cube_axis = axis
        self.active_cube_angle_rad = angle
        self.active_cube_angular_velocity_rad_s = 0.0
        self.used_direct_cubie_state_during_move = False
        return selected

    def prepare_cube_reorientation(self, target_frame: CubeFrame) -> None:
        if self.mechanism.phase is not MechanismPhase.ANCHORED:
            raise RuntimeError("cannot reorient while a cube face turn is active")
        carrier_frames = {
            axis: self._relative_frame("core", f"carrier_{axis}") for axis in "xyz"
        }
        self.reorientation.prepare(
            target_frame,
            carrier_frames,
            self.cube_state.permutation_checksum(),
        )
        self.used_direct_core_pose_during_move = False

    def mark_cube_reorientation_grasped(self) -> None:
        self.reorientation.mark_grasped()

    def activate_cube_grasp_attachment(self, hand_core_frame: ConstraintFrame) -> None:
        """Exchange world support for the accepted measured hand/core frame."""

        self.reorientation.attach_measured_grasp(hand_core_frame)

    def mark_cube_grasp_attachment_verified(self) -> None:
        self.reorientation.verify_measured_grasp()

    def cube_attachment_constraint_state(self) -> tuple[bool, bool]:
        backend = self.reorientation.backend
        return bool(backend.hand_attachment_enabled), bool(backend.world_anchor_enabled)

    def release_cube_world_anchor(self) -> None:
        self.reorientation.release_anchor()

    def mark_cube_reorientation_lifted(self) -> None:
        self.reorientation.mark_lifted()

    def mark_cube_reorientation_rotated(self) -> None:
        self.reorientation.mark_rotated()

    def mark_cube_reorientation_release_ready(self) -> None:
        self.reorientation.mark_release_ready()

    def capture_cube_support_anchor(self) -> "ConstraintFrame":
        core_frame = self._relative_frame("world_anchor", "core")
        self.reorientation.capture_measured_support(core_frame)
        return core_frame

    def mark_cube_support_hand_released(self) -> None:
        self.reorientation.mark_support_hand_released()

    def begin_captured_cube_reorientation_settle(self) -> None:
        self.reorientation.begin_captured_support_settle()

    def validate_captured_cube_support_and_commit(
        self, observation: ReorientationObservation, *,
        minimum_observed_contact_n: float | None = None,
    ) -> dict[str, object]:
        return self.reorientation.validate_captured_support_and_commit(
            observation, minimum_observed_contact_n=minimum_observed_contact_n)

    def fail_captured_cube_reorientation(self) -> None:
        self.reorientation.fail_captured_transport(capture_attempted=True)

    def begin_cube_reorientation_settle(self) -> None:
        self.reorientation.begin_settle()

    def validate_and_reanchor_cube(
        self, observation: ReorientationObservation
    ) -> dict[str, object]:
        core_frame = self._relative_frame("world_anchor", "core")
        return self.reorientation.validate_and_reanchor(observation, core_frame)

    def _zero_carrier_torques(self) -> None:
        parts = self.scene["cube_parts"]
        forces = torch.zeros((self.num_envs, 3, 3), device=self.device)
        torques = torch.zeros((self.num_envs, 3, 3), device=self.device)
        parts.set_external_force_and_torque(
            forces=forces,
            torques=torques,
            object_ids=self._carrier_indices,
            is_global=False,
        )

    def begin_idle_carrier_detent(self, axis: str) -> None:
        """Passively phase an empty carrier before attaching a logical layer."""

        normalized_axis = axis.lower()
        if normalized_axis not in "xyz":
            raise ValueError(f"unsupported idle carrier axis: {axis}")
        if self.mechanism.phase is not MechanismPhase.ANCHORED:
            raise RuntimeError("cannot settle an idle carrier during a face turn")
        if self.reorientation.phase is not ReorientationPhase.ANCHORED:
            raise RuntimeError("cannot settle an idle carrier during cube transport")
        if self.active_cube_axis is not None:
            raise RuntimeError("active cube carrier cannot be treated as idle")
        self._idle_detent_axis = normalized_axis

    def end_idle_carrier_detent(self) -> None:
        self._idle_detent_axis = None
        self._zero_carrier_torques()

    def apply_passive_detent(self) -> dict[str, float]:
        """Apply bounded periodic detents to all axes without reading a move target."""

        self._zero_carrier_torques()
        if self.reorientation.phase is not ReorientationPhase.ANCHORED:
            return {axis: 0.0 for axis in "xyz"}
        measurements = {axis: self._carrier_measurement(axis) for axis in "xyz"}
        if self.active_cube_axis is not None and self.mechanism.phase in {
            MechanismPhase.ACTIVE,
            MechanismPhase.SETTLE,
        }:
            self.active_cube_angle_rad, self.active_cube_angular_velocity_rad_s = (
                measurements[self.active_cube_axis]
            )
        detent_torques = passive_detent_torques(measurements)
        parts = self.scene["cube_parts"]
        forces = torch.zeros((self.num_envs, 3, 3), device=self.device)
        torques = torch.zeros((self.num_envs, 3, 3), device=self.device)
        for axis in "xyz":
            axis_index = "xyz".index(axis)
            torques[0, axis_index, axis_index] = detent_torques[axis]
        parts.set_external_force_and_torque(
            forces=forces,
            torques=torques,
            object_ids=self._carrier_indices,
            is_global=False,
        )
        return detent_torques

    def begin_cube_settle(self) -> None:
        self.mechanism.begin_settle()
        self._cube_settle_after_step = int(self.sim.current_time_step_index)

    def validate_and_commit_measured_cube_turn(
        self, observation: TurnObservation, native_samples, *,
        minimum_observed_contact_n: float | None = None,
        minimum_maintained_contact_n: float | None = None,
    ) -> dict[str, object]:
        """Reconstruct the committed state from current post-settle native poses."""

        if self.mechanism.phase is not MechanismPhase.SETTLE:
            raise RuntimeError("measured commit requires explicit cube settle")
        samples = tuple(native_samples)
        if not samples or samples[-1] != self.read_native_cube_sample():
            raise ValueError("measured commit window must end at the current native snapshot")
        measured, report = evaluate_native_cube_window(
            samples,
            physics_dt_s=self.physics_dt,
            after_step=self._cube_settle_after_step,
        )
        if measured is None:
            raise ValueError("native turn window cannot reconstruct a complete cube state")
        frames = self._relative_frames("core", CUBIE_IDS)
        result = self.mechanism.validate_and_commit_measured(
            replace(observation, native_pose_window_valid=bool(report["stable"])),
            frames,
            measured,
            minimum_observed_contact_n=minimum_observed_contact_n,
            minimum_maintained_contact_n=minimum_maintained_contact_n,
        )
        result["committed_native_window"] = report
        if result["committed"]:
            self.cube_state = self.mechanism.cube_state
            self.active_cube_face = None
            self.active_cube_axis = None
            self._zero_carrier_torques()
        return result

    def validate_and_commit_cube_turn(self, observation: TurnObservation) -> dict[str, object]:
        frames = self._relative_frames("core", CUBIE_IDS)
        result = self.mechanism.validate_and_commit(observation, frames)
        if result["committed"]:
            self.cube_state = self.mechanism.cube_state
            self.active_cube_face = None
            self.active_cube_axis = None
            self._zero_carrier_torques()
        return result

    def serialize_cube_state(self) -> dict[str, object]:
        return self.cube_state.to_dict()

    def read_native_cube_sample(self):
        return read_native_cube_sample(self.scene["cube_parts"], self.sim)

    def step(self, action: torch.Tensor):
        self.apply_passive_detent()
        result = super().step(action)
        self.refresh_active_turn_state()
        return result

    def _reset_idx(self, env_ids):
        spec = self._initial_reset_spec
        try:
            # Build before any reset writes; never infer requested frames from cached links.
            body_transforms = build_reset_body_transforms(spec) if spec is not None else None
            core_transform = build_reset_core_transform(spec) if spec is not None else None
            cubie_frames = build_reset_constraint_frames(
                spec.cube_state if spec is not None else CubeState.solved()
            )
            if spec is not None:
                # The configured reset event resets scene bodies too. Entering
                # that write operation counts even if it fails partway through.
                self.used_direct_cubie_state_during_reset = True
            super()._reset_idx(env_ids)
            parts = self.scene["cube_parts"]
            env_tensor = torch.as_tensor(env_ids, device=self.device, dtype=torch.long)
            default_state = parts.data.default_object_state[env_tensor].clone()
            world_core_frame = ConstraintFrame((0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0))
            if spec is not None:
                # object_names exists before our post-super index/mechanisms do.
                indices = {name: index for index, name in enumerate(parts.object_names)}
                canonical_anchor = default_state[0, indices["world_anchor"], :3].tolist()
                world_core_frame = build_reset_world_anchor_frame(
                    spec, canonical_anchor_position=canonical_anchor
                )
                for name in ("core", "carrier_x", "carrier_y", "carrier_z"):
                    body_transforms[name] = core_transform
                for name, pose in body_transforms.items():
                    default_state[:, indices[name], :7] = torch.tensor(
                        (*pose.position, *pose.quaternion),
                        dtype=default_state.dtype, device=self.device,
                    )
                default_state[..., 7:] = 0.0
                # world_anchor retains its canonical identity body pose. Only its
                # relative joint frame receives the requested continuous transform.
            default_state[..., :3] += self.scene.env_origins[env_tensor, None, :]
            if spec is not None:
                # Crossing the writer boundary is irreversible even if it raises
                # after a partial write. This records attempted direct-state writes.
                self.used_direct_cubie_state_during_reset = True
            parts.write_object_state_to_sim(default_state, env_ids=env_tensor)
            self.used_direct_cubie_state_during_reset = True
            self.used_direct_cubie_state_during_move = False
            self.used_direct_core_pose_during_move = False

            self.cube_state = snapshot_cube_state(spec.cube_state) if spec is not None else CubeState.solved()
            self.active_cube_face = None
            self.active_cube_axis = None
            self._idle_detent_axis = None
            self.active_cube_angle_rad = 0.0
            self.active_cube_angular_velocity_rad_s = 0.0
            if hasattr(self, "_angle_trackers"):
                self._angle_trackers = {axis: CarrierAngleTracker() for axis in "xyz"}
            if self._mechanism is not None:
                self._mechanism.reset(
                    self.cube_state,
                    cubie_frames,
                    world_core_frame,
                )
            if self._reorientation is not None:
                self._reorientation.reset(initial_frame=spec.logical_orientation if spec is not None else None)
            if hasattr(self, "_part_index"):
                self._zero_carrier_torques()
        except BaseException as error:
            if spec is None:
                raise
            crossed_write_boundary = bool(
                self.used_direct_cubie_state_during_reset
                or getattr(error, "used_direct_cubie_state_during_reset", False)
            )
            if isinstance(error, CubeResetExecutionError) and (
                error.used_direct_cubie_state_during_reset == crossed_write_boundary
            ):
                raise
            raise CubeResetExecutionError(
                f"{type(error).__name__}: {error}",
                used_direct_cubie_state_during_reset=crossed_write_boundary,
            ) from error
