"""Trusted native bridge for two Floating Sharpa Kongming episodes."""
from __future__ import annotations

import math

import numpy as np

from agentbench_platform.native_state import plain, rigid_parameters
from agentbench_platform.profiles import number
from agentbench_platform.tasks import validate_task
from agentbench.sharpa_joint_names import (
    SHARPA_CONTACT_BODY_NAMES,
    SHARPA_FINGER_JOINT_NAMES,
    SHARPA_MOTION_JOINT_NAMES,
    SHARPA_PALM_BODY_NAME,
)
from .shapes import CANONICAL_SPEC
from .sharpa_calibration import NON_PAD_BODIES, preflight


JOINT_NAMES = tuple(SHARPA_MOTION_JOINT_NAMES) + tuple(SHARPA_FINGER_JOINT_NAMES)
FINGER_SENSOR_NAMES = tuple(SHARPA_CONTACT_BODY_NAMES)
PIECE_NAMES = tuple(CANONICAL_SPEC.piece_names)
VIEWS = {
    "front_left": ((1.75, -2.05, 1.55), (.70, 0, .72), (0, 0, 1)),
    "front_right": ((1.75, 2.05, 1.55), (.70, 0, .72), (0, 0, 1)),
    "top": ((.70, 0, 2.20), (.70, 0, .60), (0, 1, 0)),
}


def link_origin_jacobian(jacobian, link_position, com_position):
    """PhysX supplies COM linear velocity; public poses refer to link origins."""
    result = np.array(jacobian, dtype=float, copy=True)
    x, y, z = np.asarray(com_position)-np.asarray(link_position)
    skew = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    result[:3] += skew @ result[3:]
    return result


class KongmingDualSharpaState:
    """One native CUDA episode with a strict 56-vector action."""

    def __init__(self, env, *, mode, spec, case_id=None):
        if (env.num_envs != 1 or not str(env.device).startswith("cuda")
                or env.cfg.decimation != 4 or env.cfg.sim.render_interval != 4
                or abs(env.physics_dt - 1 / 120) > 1e-10):
            raise ValueError("Dual Floating Sharpa Kongming requires CUDA PhysX at 120/30 Hz")
        validate_task("kongming_lock", mode, embodiment="dual-floating-sharpa")
        self.env, self.mode, self.spec, self.case_id = env, mode, spec, case_id
        self.robots = {side: env.scene[side + "_robot"] for side in ("left", "right")}
        self.joint_ids = {}
        self.motion_ids = {}
        self.finger_ids = {}
        self.palm_ids = {}
        for side, robot in self.robots.items():
            names = list(robot.joint_names)
            missing = [name for name in JOINT_NAMES if name not in names]
            if missing:
                raise ValueError(f"{side} Sharpa joint mapping missing: {missing}")
            self.joint_ids[side] = [names.index(name) for name in JOINT_NAMES]
            self.motion_ids[side] = [names.index(name) for name in SHARPA_MOTION_JOINT_NAMES]
            self.finger_ids[side] = [names.index(name) for name in SHARPA_FINGER_JOINT_NAMES]
            if SHARPA_PALM_BODY_NAME not in robot.body_names:
                raise ValueError(f"{side} Sharpa palm body missing")
            self.palm_ids[side] = robot.body_names.index(SHARPA_PALM_BODY_NAME)
        self.reset_done = False
        self.control = self.physics = 0
        self._parameters = None
        self._hook = None
        self.submitted_targets = None

    @staticmethod
    def _deny_object_write(*args, **kwargs):
        raise RuntimeError("Post-reset object state write prohibited")

    def reset(self):
        if self.reset_done:
            raise RuntimeError("Reset already used")
        self.env.reset()
        # Do not advance physics here.  The case projection is the trusted
        # public initial state and must be measured before any settling can
        # move a parked piece away from its manifest pose.  Fresh contact
        # buffers are excluded from the episode score until the first real
        # agent action, exactly as in the Panda bridge.
        self.reset_done = True
        for name in PIECE_NAMES:
            piece = self.env.scene["piece_" + name]
            for method in dir(piece):
                if method.startswith("write_root_") and method.endswith("_to_sim"):
                    setattr(piece, method, self._deny_object_write)

    def install_hook(self, hook):
        self._hook = hook
        self.env.benchmark_substep_hook = self._substep if hook is not None else None

    def neutral_action(self):
        values = []
        for side in ("left", "right"):
            defaults = np.asarray(plain(self.robots[side].data.default_joint_pos[0]), dtype=np.float32)
            values.extend(defaults[self.joint_ids[side]].astype(float).tolist())
        return values

    def _action_spec(self):
        low, high, names = [], [], []
        for side in ("left", "right"):
            data = self.robots[side].data
            limits = np.asarray(plain(data.joint_pos_limits[0]), dtype=float)
            for index in self.joint_ids[side]:
                low.append(float(limits[index, 0]))
                high.append(float(limits[index, 1]))
                names.append(f"{side}.sharpa.{self.robots[side].joint_names[index]}")
        return dict(
            size=56,
            neutral_action=self.neutral_action(),
            low=low,
            high=high,
            names=names,
            semantics=["Absolute native joint target in the declared left-then-right order."] * 56,
        )

    def describe(self):
        robots = {}
        for side in ("left", "right"):
            data = self.robots[side].data
            robots[side + "_floating_sharpa"] = dict(
                model="Floating Sharpa Wave right hand",
                joint_names=list(self.robots[side].joint_names),
                default_joint_positions=plain(data.default_joint_pos[0]),
                joint_limits=plain(data.joint_pos_limits[0]),
                soft_joint_limits=plain(data.soft_joint_pos_limits[0]),
                base_position=plain(data.root_pos_w[0]),
                base_quaternion=plain(data.root_quat_w[0]),
            )
        task = dict(
            id="kongming-dual-floating-sharpa-v1",
            task_id="kongming-dual-floating-sharpa-v1",
            family="kongming_lock",
            embodiment="dual-floating-sharpa",
            name="Kongming lock",
            mode=self.mode,
            case_id=self.case_id,
            subtask=self.spec.get("subtask", "complete"),
            description=("Assemble the selected Kongming pieces." if self.mode == "assemble"
                         else "Disassemble the selected Kongming pieces."),
        )
        return dict(
            task=task,
            action_spec=self._action_spec(),
            robots=robots,
            cameras={},
            goal=dict(
                mode=self.mode,
                position_tolerance_m=.0075 if self.mode == "assemble" else .025,
                angular_tolerance_rad=.08 if self.mode == "assemble" else .25,
                stable_controls=60 if self.mode == "assemble" else 30,
                penetration_ceiling_m=.002,
            ),
        )

    def _piece_rows(self):
        rows = {}
        for name in PIECE_NAMES:
            data = self.env.scene["piece_" + name].data
            rows[name] = dict(
                position=plain(data.root_pos_w[0]),
                quaternion=plain(data.root_quat_w[0]),
                linear_velocity=plain(data.root_lin_vel_w[0]),
                angular_velocity=plain(data.root_ang_vel_w[0]),
            )
        return rows

    def reset_acceptance(self):
        rows = {}
        passed = True
        for name in PIECE_NAMES:
            measured = self._piece_rows()[name]
            expected = self.spec["pieces"][name]
            target = np.asarray(expected["initial_position"], dtype=float)
            target_q = np.asarray(expected["initial_quaternion"], dtype=float)
            position = np.asarray(measured["position"], dtype=float)
            quaternion = np.asarray(measured["quaternion"], dtype=float)
            position_error = float(np.linalg.norm(position - target))
            dot = abs(float(np.dot(quaternion / np.linalg.norm(quaternion), target_q / np.linalg.norm(target_q))))
            angle_error = float(2 * math.acos(np.clip(dot, 0.0, 1.0)))
            speed = float(np.linalg.norm(measured["linear_velocity"]))
            spin = float(np.linalg.norm(measured["angular_velocity"]))
            rows[name] = dict(position_error_m=position_error, angle_error_rad=angle_error,
                              speed_m_s=speed, spin_rad_s=spin)
            passed = passed and position_error <= .003 and angle_error <= .05 and speed < .01 and spin < .10
        # Deterministic mount preflight is part of reset acceptance.  It does
        # not claim a grasp is reachable; it catches table/inter-hand
        # collisions and obviously unusable case geometry before an agent is
        # charged for an episode.
        robot_rows = {side: self._robot_row(side) for side in ("left", "right")}
        palm_distance = float(np.linalg.norm(
            np.asarray(robot_rows["left"]["hand_position"]) -
            np.asarray(robot_rows["right"]["hand_position"])))
        fingertip_clearance = min(
            float(position[2]) - float(self.spec.get("table_top_z", .60))
            for side in ("left", "right")
            for body_name, position in zip(
                self.robots[side].body_names,
                np.asarray(plain(self.robots[side].data.body_link_pose_w[0]))[:, :3],
            )
            if body_name in FINGER_SENSOR_NAMES
        )
        piece_reach = max(
            min(float(np.linalg.norm(np.asarray(robot_rows[side]["hand_position"]) -
                                     np.asarray(piece["position"]))) for side in ("left", "right"))
            for piece in self._piece_rows().values()
        )
        robot_preflight = dict(
            palm_distance_m=palm_distance,
            fingertip_table_clearance_m=fingertip_clearance,
            farthest_piece_to_nearest_palm_m=piece_reach,
            passed=bool(palm_distance > .10 and fingertip_clearance > .02 and piece_reach < 1.0),
        )
        geometry_preflight = preflight(
            {side: dict(zip(robot.body_names, np.asarray(plain(robot.data.body_link_pose_w[0]))))
             for side, robot in self.robots.items()},
            {**self._piece_rows(), **{'goal_'+n: dict(position=p['target_position'])
                                    for n,p in self.spec['pieces'].items()}}, self.spec['table_top_z'],
            {side: np.asarray(plain(robot.data.joint_pos_limits[0]))[self.joint_ids[side]]
             for side, robot in self.robots.items()})
        robot_preflight.update(geometry_preflight)
        passed = passed and robot_preflight["passed"]
        return dict(
            passed=bool(passed), case_id=self.case_id,
            state_hash=self.spec.get("state_hash"), pieces=rows,
            robot_preflight=robot_preflight,
        )

    def _robot_row(self, side):
        robot = self.robots[side]
        data = robot.data
        pose = np.asarray(plain(data.body_link_pose_w[0]), dtype=float)
        lin = np.asarray(plain(data.body_link_lin_vel_w[0]), dtype=float)
        ang = np.asarray(plain(data.body_link_ang_vel_w[0]), dtype=float)
        palm = self.palm_ids[side]
        finger_positions = np.asarray(plain(data.joint_pos[0, self.finger_ids[side]]), dtype=float)
        finger_defaults = np.asarray(plain(data.default_joint_pos[0, self.finger_ids[side]]), dtype=float)
        return dict(
            joint_positions=plain(data.joint_pos[0]),
            joint_velocities=plain(data.joint_vel[0]),
            joint_ids=list(self.joint_ids[side]),
            motion_joint_ids=list(self.motion_ids[side]),
            finger_joint_ids=list(self.finger_ids[side]),
            finger_positions=finger_positions.tolist(),
            finger_default_positions=finger_defaults.tolist(),
            hand_open=bool(np.max(np.abs(finger_positions - finger_defaults)) <= .05),
            hand_position=pose[palm, :3].tolist(),
            hand_quaternion=pose[palm, 3:7].tolist(),
            tcp=pose[palm, :3].tolist(),
            body_positions=pose[:, :3].tolist(),
            body_quaternions=pose[:, 3:7].tolist(),
            body_linear_velocities=lin.tolist(),
            body_angular_velocities=ang.tolist(),
        )

    def _sensor_row(self, side, fingertip):
        sensor_name = f"{side}_{fingertip}_kongming_contact"
        data = self.env.scene.sensors[sensor_name].data
        matrix = np.asarray(plain(data.force_matrix_w[0]), dtype=float)
        if matrix.ndim == 3 and matrix.shape[0] == 1:
            matrix = matrix[0]
        if matrix.ndim != 2 or matrix.shape[1] != 3 or matrix.shape[0] < len(PIECE_NAMES):
            raise RuntimeError(f"Incomplete {side}/{fingertip} contact matrix")
        net = np.asarray(plain(data.net_forces_w[0]), dtype=float)
        if net.ndim > 1:
            net = net.sum(axis=0)
        if net.shape != (3,) or not np.isfinite(net).all() or not np.isfinite(matrix).all():
            raise RuntimeError(f"Invalid {side}/{fingertip} contact data")
        allowed = matrix[:len(PIECE_NAMES)]
        forbidden = matrix[len(PIECE_NAMES):]
        residual = net - allowed.sum(axis=0)
        return dict(
            finger=fingertip,
            piece_names=list(PIECE_NAMES),
            forces_w=allowed.tolist(),
            net_w=net.tolist(),
            forbidden_forces_w=forbidden.tolist(),
            residual_w=residual.tolist(),
        )

    def _palm_contact_row(self, side):
        """Read the palm sensor with the same immutable piece/forbidden split."""
        sensor_name = f"{side}_palm_kongming_contact"
        data = self.env.scene.sensors[sensor_name].data
        matrix = np.asarray(plain(data.force_matrix_w[0]), dtype=float)
        if matrix.ndim == 3 and matrix.shape[0] == 1:
            matrix = matrix[0]
        if matrix.ndim != 2 or matrix.shape[1] != 3 or matrix.shape[0] < len(PIECE_NAMES):
            raise RuntimeError(f"Incomplete {side}/palm contact matrix")
        net = np.asarray(plain(data.net_forces_w[0]), dtype=float)
        if net.ndim > 1:
            net = net.sum(axis=0)
        if net.shape != (3,) or not np.isfinite(net).all() or not np.isfinite(matrix).all():
            raise RuntimeError(f"Invalid {side}/palm contact data")
        allowed = matrix[:len(PIECE_NAMES)]
        forbidden = matrix[len(PIECE_NAMES):]
        return dict(
            finger="right_hand_C_MC",
            piece_names=list(PIECE_NAMES),
            forces_w=allowed.tolist(),
            net_w=net.tolist(),
            forbidden_forces_w=forbidden.tolist(),
            residual_w=(net - allowed.sum(axis=0)).tolist(),
        )

    def physical(self, control, physics):
        return dict(
            control_step=control,
            physics_step=physics,
            pieces=self._piece_rows(),
            robots={side: dict(
                **self._robot_row(side),
                fingertip_contacts=[self._sensor_row(side, finger) for finger in FINGER_SENSOR_NAMES],
                palm_contacts=[self._palm_contact_row(side)],
                body_forces_w=self._body_forces(side),
            ) for side in ("left", "right")},
        )

    def _body_forces(self, side):
        sensor = self.env.scene.sensors[f'{side}_body_kongming_contact']
        if set(sensor.body_names) != set(NON_PAD_BODIES):
            raise RuntimeError('Incomplete Sharpa non-pad body coverage')
        forces = np.asarray(plain(sensor.data.net_forces_w[0]))
        if forces.shape != (len(NON_PAD_BODIES), 3) or not np.isfinite(forces).all():
            raise RuntimeError('Invalid Sharpa non-pad body forces')
        return forces.tolist()

    def _physics_parameters(self):
        if self._parameters is None:
            self._parameters = {
                side: rigid_parameters(self.robots[side].root_physx_view, body_names=self.robots[side].body_names)
                for side in ("left", "right")
            }
            for name in PIECE_NAMES:
                piece = self.env.scene["piece_" + name]
                self._parameters["piece_" + name] = rigid_parameters(piece.root_physx_view, body_names=piece.body_names)
        return self._parameters

    def snapshot(self, control, previous_action):
        physical = self.physical(control, self.physics)
        robots, bodies, contacts, jacobians = {}, {}, [], {}
        for side in ("left", "right"):
            robot = self.robots[side]
            data = robot.data
            robots[side + "_floating_sharpa"] = dict(
                joint_names=list(robot.joint_names),
                joint_positions=plain(data.joint_pos[0]),
                joint_velocities=plain(data.joint_vel[0]),
                measured_finger_positions=plain(data.joint_pos[0, self.finger_ids[side]]),
                previous_action=list(previous_action),
            )
            pose = np.asarray(plain(data.body_link_pose_w[0]), dtype=float)
            lin = np.asarray(plain(data.body_link_lin_vel_w[0]), dtype=float)
            ang = np.asarray(plain(data.body_link_ang_vel_w[0]), dtype=float)
            jac = robot.root_physx_view.get_jacobians()[0]
            for index, name in enumerate(robot.body_names):
                bodies[f"{side}.sharpa.{name}"] = dict(
                    position=pose[index, :3].tolist(), quaternion=pose[index, 3:7].tolist(),
                    com_position=plain(data.body_com_pos_w[0, index]),
                    linear_velocity=lin[index].tolist(), angular_velocity=ang[index].tolist(),
                )
                jacobians[f"{side}.sharpa.{name}"] = link_origin_jacobian(
                    plain(jac[index - 1, :, self.joint_ids[side]]), pose[index, :3],
                    plain(data.body_com_pos_w[0, index])).tolist() if index else []
            for contact in physical["robots"][side]["fingertip_contacts"]:
                for piece_name, force in zip(contact["piece_names"], contact["forces_w"]):
                    contacts.append(dict(
                        body_a=f"{side}.sharpa.{contact['finger']}",
                        body_b="piece_" + piece_name,
                        force_vector_n=force,
                    ))
            for contact in physical["robots"][side]["palm_contacts"]:
                for piece_name, force in zip(contact["piece_names"], contact["forces_w"]):
                    contacts.append(dict(
                        body_a=f"{side}.sharpa.{contact['finger']}",
                        body_b="piece_" + piece_name,
                        force_vector_n=force,
                    ))
        pieces = physical["pieces"]
        return dict(
            robots=robots,
            privileged=dict(
                pieces=pieces,
                robot_bodies=bodies,
                jacobians=jacobians,
                contacts=contacts if self.physics else [],
                geometry={name: dict(collision_boxes=[
                    [list(center), list(half)] for center, half in zip(
                        self.spec["pieces"][name]["centers"], self.spec["pieces"][name]["half_extents"])
                ]) for name in PIECE_NAMES},
                physics=dict(physics_hz=120, control_hz=30, timestep_s=1 / 120,
                             gravity=list(self.env.cfg.sim.gravity), rigid_bodies=self._physics_parameters()),
                diagnostics={},
            ),
        )

    def physical_arrays(self):
        arrays = [
                np.asarray(plain(self.env.scene["piece_" + name].data.root_state_w)).copy()
            for name in PIECE_NAMES
        ]
        for side in ("left", "right"):
            data = self.robots[side].data
            arrays.extend((
                np.asarray(plain(data.joint_pos)).copy(),
                np.asarray(plain(data.joint_vel)).copy(),
                np.asarray(plain(data.body_link_pose_w)).copy(),
                np.asarray(plain(data.body_link_lin_vel_w)).copy(),
                np.asarray(plain(data.body_link_ang_vel_w)).copy(),
            ))
        return arrays

    def _substep(self):
        self.physics += 1
        if self._hook is not None:
            self._hook()

    def apply(self, action):
        if not self.reset_done:
            raise RuntimeError("Reset required before applying actions")
        bounds = self._action_spec()
        if (not isinstance(action, list) or len(action) != 56
                or not all(number(x) and lo <= x <= hi for x, lo, hi in
                           zip(action, bounds["low"], bounds["high"]))):
            raise ValueError("Invalid dual Floating Sharpa action")
        import torch
        command = np.asarray(action, dtype=np.float32).astype(float)
        self.control += 1
        self.submitted_targets = command.tolist()
        self.env.action_manager.process_action(torch.tensor(command, dtype=torch.float32, device=self.env.device)[None])
        for _ in range(self.env.cfg.decimation):
            self.env.action_manager.apply_action()
            self.env.scene.write_data_to_sim()
            self.env.sim.step(render=False)
            self.env.scene.update(self.env.physics_dt)
            self._substep()
        return command.tolist()
