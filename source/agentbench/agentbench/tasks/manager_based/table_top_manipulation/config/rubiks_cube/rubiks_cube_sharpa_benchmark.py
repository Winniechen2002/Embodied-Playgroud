"""Trusted SDK bridge for the official Floating Sharpa Rubik scene.

This adapter owns the native 28-joint action boundary.  It deliberately does
not import the Sharpa calibration controller or expose any private case data.
Reset-time cube writes remain owned by :class:`RubiksCubeEnv`; after reset this
object only submits joint targets and reads native state.
"""
from __future__ import annotations

from collections import deque
from dataclasses import asdict
import json
import math

import numpy as np

from agentbench_platform.native_state import plain, rigid_parameters
from agentbench_platform.profiles import number
from agentbench_platform.tasks import normalize_embodiment, validate_task
from .rubiks_cube_embodiment import get_embodiment, validate_robot_mapping
from .rubiks_cube_geometry import CUBIE_SIZE_M
from .rubiks_cube_observer import classify_native_snapshot
from .rubiks_cube_sharpa_cfg import SHARPA_SENSOR_NAMES


VIEWS = {
    'front_left': ((1.04, -.34, .98), (.70, 0, .665), (0, 0, 1)),
    'front_right': ((1.04, .34, .98), (.70, 0, .665), (0, 0, 1)),
    'top': ((.70, 0, 1.27), (.70, 0, .6355), (0, 1, 0)),
}


def _without_counters(row):
    result = dict(row)
    result.pop('control_step', None)
    result.pop('physics_step', None)
    return result


class SharpaState:
    """One native Sharpa episode with a strict absolute 28-vector action."""

    def __init__(self, env, *, mode, target_sequence=None, case_id=None, mechanism=None):
        if (env.num_envs != 1 or not str(env.device).startswith('cuda')
                or env.cfg.decimation != 4 or env.cfg.sim.render_interval != 4
                or abs(env.physics_dt - 1 / 120) > 1e-10):
            raise ValueError('Floating Sharpa benchmark requires CUDA PhysX at 120/30 Hz')
        self.sequence = validate_task('rubiks_cube', mode, target_sequence,
                                      embodiment='floating-sharpa')
        if case_id is not None and (not isinstance(case_id, str) or not case_id):
            raise ValueError('case_id must be a nonempty string')
        self.env, self.mode, self.case_id = env, mode, case_id
        self.spec = get_embodiment('floating-sharpa-right')
        self.robot, self.parts = env.scene['robot'], env.scene['cube_parts']
        self.mapping = validate_robot_mapping(self.spec,
            joint_names=self.robot.joint_names, body_names=self.robot.body_names)
        self.joint_ids = list(self.mapping['motion_joint_ids']) + list(self.mapping['finger_joint_ids'])
        self.motion_ids = list(self.mapping['motion_joint_ids'])
        self.finger_ids = list(self.mapping['finger_joint_ids'])
        self.palm_id = self.mapping['palm_body_id']
        self.cubie_ids = tuple(sorted(n for n in self.parts.object_names if n.startswith('cubie_')))
        if len(self.cubie_ids) != 26 or len(self.parts.object_names) != 31:
            raise ValueError('Expected all 31 native cube bodies')
        self.reset_done = False
        self.episode_started = False
        self.control = self.physics = 0
        self.history = deque(maxlen=1024)
        self._parameters = None
        self._hook = None
        self._mechanism = mechanism
        self.submitted_targets = None

    @staticmethod
    def _deny_object_write(*args, **kwargs):
        raise RuntimeError('Post-reset object state write prohibited')

    def reset(self):
        if self.reset_done:
            raise RuntimeError('Reset already used')
        self.env.reset()
        self.reset_done = True
        for method in dir(self.parts):
            if method.startswith('write_object_') and method.endswith('_to_sim'):
                setattr(self.parts, method, self._deny_object_write)

    def neutral_action(self):
        defaults = np.asarray(plain(self.robot.data.default_joint_pos[0]), dtype=np.float32)
        return defaults[self.joint_ids].astype(float).tolist()

    def install_hook(self, hook):
        self._hook = hook

    def start_episode(self, accepted_initial):
        if not self.reset_done or self.episode_started:
            raise RuntimeError('Prepared episode must follow exactly one initialization')
        current = self.physical(0, 0)
        if (json.dumps(_without_counters(current), sort_keys=True)
                != json.dumps(_without_counters(accepted_initial), sort_keys=True)):
            raise ValueError('Accepted initialization is no longer the current native state')
        self.episode_started = True
        self.control = self.physics = 0
        self.history.clear()
        self._hook = None

    def _action_spec(self):
        data = self.robot.data
        limits = np.asarray(plain(data.joint_pos_limits[0]), dtype=float)
        low = limits[self.joint_ids, 0].tolist()
        high = limits[self.joint_ids, 1].tolist()
        names = [f'sharpa.{self.robot.joint_names[i]}' for i in self.joint_ids]
        return dict(size=28, low=low, high=high, names=names,neutral_action=self.neutral_action(),
                    semantics=['Absolute native joint target in the declared joint order.'] * 28)

    def describe(self):
        data = self.robot.data
        defaults, limits = plain(data.default_joint_pos[0]), plain(data.joint_pos_limits[0])
        task = dict(id='rubiks-cube-' + self.mode + '-v1', family='rubiks_cube',
                    embodiment='floating-sharpa', name="Rubik's cube", mode=self.mode,
                    description='Restore the cube from its current measured state.' if self.mode == 'solve'
                    else 'Execute the target sequence in order, including every cancelling turn.')
        if self.sequence is not None:
            task['target_sequence'] = list(self.sequence)
        if self.case_id is not None:
            task['case_id'] = self.case_id
        result = dict(task=task, action_spec=self._action_spec(),
            robots={'floating_sharpa': dict(model='Floating Sharpa Wave right hand',
                joint_names=list(self.robot.joint_names), default_joint_positions=defaults,
                joint_limits=limits, soft_joint_limits=plain(data.soft_joint_pos_limits[0]),
                base_position=plain(data.root_pos_w[0]), base_quaternion=plain(data.root_quat_w[0]))},
            cameras={}, goal=dict(mode=self.mode, return_position_tolerance_m=.005,
                return_angle_tolerance_rad=math.radians(2), stable_seconds=.5,
                finger_open_min_m=0., home_joint_tolerance_rad=.05))
        if self._mechanism is not None:result['mechanism']=dict(version='hybrid_fixture_v1')
        return result

    def _contacts(self):
        rows = []
        for body_name, sensor_name in zip(self.spec.contact_body_names, SHARPA_SENSOR_NAMES):
            data = self.env.scene.sensors[sensor_name].data
            matrix = np.asarray(plain(data.force_matrix_w[0]), dtype=float)
            if matrix.shape != (1, 26, 3) or not np.isfinite(matrix).all():
                raise RuntimeError('Incomplete or nonfinite Sharpa contact matrix')
            net = np.asarray(plain(data.net_forces_w[0]), dtype=float)
            if net.shape != (1, 3) or not np.isfinite(net).all():
                raise RuntimeError('Invalid Sharpa net contact force')
            rows.append(dict(finger=body_name, cubie_names=list(self.cubie_ids),
                             forces_w=matrix[0].tolist(), net_w=net[0].tolist()))
        return rows

    def _robot_row(self):
        data = self.robot.data
        pose = np.asarray(plain(data.body_link_pose_w[0]), dtype=float)
        lin = np.asarray(plain(data.body_link_lin_vel_w[0]), dtype=float)
        ang = np.asarray(plain(data.body_link_ang_vel_w[0]), dtype=float)
        return dict(joint_positions=plain(data.joint_pos[0]), joint_velocities=plain(data.joint_vel[0]),
                    joint_ids=list(self.joint_ids), motion_joint_ids=list(self.motion_ids),
                    finger_joint_ids=list(self.finger_ids),
                    hand_position=pose[self.palm_id, :3].tolist(),
                    hand_quaternion=pose[self.palm_id, 3:7].tolist(),
                    body_positions=pose[:, :3].tolist(), body_quaternions=pose[:, 3:7].tolist(),
                    body_linear_velocities=lin.tolist(), body_angular_velocities=ang.tolist())

    def physical(self, control, physics):
        sample = self.env.read_native_cube_sample()
        row = dict(control_step=control, physics_step=physics, native=asdict(sample),
                   robot=self._robot_row(), finger_contacts=self._contacts(),
                   submitted_targets=self.submitted_targets)
        if (self.env.sim.current_time_step_index != sample.native_step
                or self.env.sim.current_time != sample.native_time_s):
            raise RuntimeError('Native clock changed during Sharpa extraction')
        if self._mechanism is not None:row['mechanism']=self._mechanism.evidence()
        return row

    def _physics_parameters(self):
        if self._parameters is None:
            view = self.parts.root_physx_view
            self._parameters = dict(
                floating_sharpa=rigid_parameters(self.robot.root_physx_view,
                    body_names=self.robot.body_names),
                cube_parts=dict(body_names=list(self.parts.object_names),
                    mass_kg=plain(view.get_masses()), inertia_kg_m2=plain(view.get_inertias()),
                    material_static_dynamic_restitution=plain(view.get_material_properties()),
                    contact_offset_m=plain(view.get_contact_offsets()), rest_offset_m=plain(view.get_rest_offsets())))
        return self._parameters

    def snapshot(self, control, previous_action):
        measured = self.physical(control, self.physics)
        sample = measured['native']
        data = self.robot.data
        classified, diagnostics = classify_native_snapshot(
            sample['body_names'], sample['native_link_transforms_xyzw'], ignore_center_twist=True)
        cube = dict(valid=classified is not None, source='native_physx_link_transforms')
        if classified is not None:
            cube['facelets_urfdlb'] = classified.facelet_string()
        pieces = {}
        for name, pose, velocity in zip(sample['body_names'], sample['native_link_transforms_xyzw'],
                                        sample['raw_com_velocities']):
            pieces[name] = dict(position=list(pose[:3]), quaternion=[pose[6], *pose[3:6]],
                                linear_velocity=list(velocity[:3]), angular_velocity=list(velocity[3:]))
        pose = np.asarray(plain(data.body_link_pose_w[0]), dtype=float)
        lin = np.asarray(plain(data.body_link_lin_vel_w[0]), dtype=float)
        ang = np.asarray(plain(data.body_link_ang_vel_w[0]), dtype=float)
        bodies, jacobians, contacts = {}, {}, []
        jac = self.robot.root_physx_view.get_jacobians()[0]
        for index, name in enumerate(self.robot.body_names):
            bodies['sharpa.' + name] = dict(position=pose[index, :3].tolist(),
                quaternion=pose[index, 3:7].tolist(), com_position=plain(data.body_com_pos_w[0, index]),
                linear_velocity=lin[index].tolist(), angular_velocity=ang[index].tolist())
            if index:
                jacobians['sharpa.' + name] = plain(jac[index - 1][:, self.motion_ids])
        for contact in measured['finger_contacts']:
            for name, force in zip(contact['cubie_names'], contact['forces_w']):
                contacts.append(dict(body_a='sharpa.' + contact['finger'], body_b=name,
                                     force_vector_n=force))
        result = dict(robots={'floating_sharpa': dict(joint_names=list(self.robot.joint_names),
            joint_positions=plain(data.joint_pos[0]), joint_velocities=plain(data.joint_vel[0]),
            measured_finger_positions=plain(data.joint_pos[0, self.finger_ids]),
            previous_action=list(previous_action))},
            privileged=dict(cube=cube, pieces=pieces, robot_bodies=bodies, jacobians=jacobians,
                contacts=contacts if self.physics else [],
                geometry={n: dict(half_extents=[CUBIE_SIZE_M / 2] * 3) for n in self.cubie_ids},
                physics=dict(physics_hz=120, control_hz=30, timestep_s=1 / 120,
                    gravity=list(self.env.cfg.sim.gravity), rigid_bodies=self._physics_parameters()),
                diagnostics=diagnostics))
        if self._mechanism is not None:result['mechanism']=self._mechanism.public_state()
        return result

    def physical_arrays(self):
        sample = self.env.read_native_cube_sample()
        data = self.robot.data
        pose = np.asarray(plain(data.body_link_pose_w), dtype=float)
        lin = np.asarray(plain(data.body_link_lin_vel_w), dtype=float)
        ang = np.asarray(plain(data.body_link_ang_vel_w), dtype=float)
        body_state = np.concatenate((pose, lin, ang), axis=-1)
        return [np.asarray(sample.native_link_transforms_xyzw), np.asarray(sample.raw_com_velocities),
                np.asarray(plain(data.joint_pos)), np.asarray(plain(data.joint_vel)), body_state]

    def _observe_substep(self):
        self.physics += 1
        measured = self.physical(self.control, self.physics)
        self.history.append(measured)
        if self._hook is not None:
            self._hook()

    def apply(self, action):
        if not self.reset_done:
            raise RuntimeError('Reset required before applying actions')
        bounds = self._action_spec()
        if (not isinstance(action, list) or len(action) != 28
                or not all(number(x) and lo <= x <= hi for x, lo, hi in
                           zip(action, bounds['low'], bounds['high']))):
            raise ValueError('Invalid Floating Sharpa action')
        import torch
        command = np.asarray(action, dtype=np.float32).astype(float)
        self.control += 1
        self.submitted_targets = command.tolist()
        self.env.action_manager.process_action(torch.tensor(command, dtype=torch.float32,
                                                             device=self.env.device)[None])
        for _ in range(self.env.cfg.decimation):
            self.env.action_manager.apply_action()
            self.env._sim_step_counter += 1
            getattr(self._mechanism,'apply_detent',self.env.apply_passive_detent)()
            self.env.scene.write_data_to_sim()
            self.env.sim.step(render=False)
            self.env.scene.update(self.env.physics_dt)
            self._observe_substep()
        self.env.refresh_active_turn_state()
        self.env.sim.render()
        return command.tolist()

    def mechanism(self,name,arguments):
        if self._mechanism is None:raise RuntimeError('Native mechanism not installed')
        return self._mechanism.command(name,arguments)
