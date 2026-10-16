"""Trusted AgentBench adapter for one native Rubik scene; no controller imports."""
from collections import deque
from dataclasses import asdict
import json
import math

import numpy as np

from agentbench_platform.native_state import action_bounds, plain, rigid_parameters
from agentbench_platform.profiles import number
from agentbench_platform.tasks import validate_task
from .rubiks_cube_control import run_decimated_control_cycle
from .rubiks_cube_geometry import CUBIE_SIZE_M
from .rubiks_cube_observer import classify_native_snapshot


VIEWS = {
    'front_left': ((1.04,-.34,.98),(.70,0,.665),(0,0,1)),
    'front_right': ((1.04,.34,.98),(.70,0,.665),(0,0,1)),
    'top': ((.70,0,1.27),(.70,0,.6355),(0,1,0)),
}


class RubiksState:
    """Only reset writes rigid state. Each apply submits one eight-coordinate action.

    The optional trusted mechanism owns transition guards, not trajectories.
    Until installed no mechanism capability is advertised by this adapter.
    """
    def __init__(self, env, *, mode, target_sequence=None, mechanism=None, case_id=None):
        if (env.num_envs != 1 or not str(env.device).startswith('cuda')
                or env.cfg.decimation != 4 or env.cfg.sim.render_interval != 4
                or abs(env.physics_dt-1/120) > 1e-10):
            raise ValueError('Rubik benchmark requires single-env CUDA PhysX at 120/30 Hz')
        self.sequence = validate_task('rubiks_cube', mode, target_sequence)
        if case_id is not None and (not isinstance(case_id, str) or not case_id):
            raise ValueError('case_id must be a nonempty string')
        self.env, self.mode, self._mechanism = env, mode, mechanism
        self.case_id = case_id
        self.robot, self.parts = env.scene['robot'], env.scene['cube_parts']
        self.arm_ids = self.robot.find_joints('panda_joint[1-7]')[0]
        self.finger_ids = self.robot.find_joints('panda_finger_joint.*')[0]
        if len(self.arm_ids) != 7 or len(self.finger_ids) != 2:
            raise ValueError('Expected seven Panda arm and two finger joints')
        self.hand_id = self.robot.find_bodies('panda_hand')[0][0]
        self.cubie_ids = tuple(sorted(n for n in self.parts.object_names if n.startswith('cubie_')))
        if len(self.cubie_ids) != 26 or len(self.parts.object_names) != 31:
            raise ValueError('Expected all 31 native cube bodies')
        self.reset_done = False
        self.episode_started = False
        self.control = self.physics = 0
        self.history = deque(maxlen=1024)
        self._parameters = None
        self._hook = None
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

    def install_hook(self, hook):
        self._hook = hook

    def start_episode(self, accepted_initial):
        """Claim accepted initialization once; rebase counters without a reset."""
        if not self.reset_done or self.episode_started:
            raise RuntimeError('Prepared episode must follow exactly one initialization')
        current = self.physical(0, 0)
        if json.dumps(current, sort_keys=True) != json.dumps(accepted_initial, sort_keys=True):
            raise ValueError('Accepted initialization is no longer the current native state')
        self.episode_started = True
        self.control = self.physics = 0
        self.history.clear()
        self._hook = None

    def describe(self):
        data = self.robot.data
        defaults, limits = plain(data.default_joint_pos[0]), plain(data.joint_pos_limits[0])
        low, high = action_bounds([defaults[i] for i in self.arm_ids], [limits[i] for i in self.arm_ids])
        task = dict(id='rubiks-cube-'+self.mode+'-v1', family='rubiks_cube', name="Rubik's cube", mode=self.mode,
                    description='Restore the cube from its current measured state.' if self.mode == 'solve'
                    else 'Execute the target sequence in order, including every cancelling turn.')
        if self.sequence is not None:
            task['target_sequence'] = list(self.sequence)
        if self.case_id is not None:
            # This is the sole catalog field exposed through describe().  The
            # selected reset, seed, scramble, and reference data remain on the
            # trusted maintainer side.
            task['case_id'] = self.case_id
        result = dict(task=task, action_spec=dict(size=8, low=low+[-1.], high=high+[1.],
            neutral_action=[0.]*7+[1.],
            names=['panda.'+self.robot.joint_names[i] for i in self.arm_ids]+['panda.gripper'],
            semantics=['Seven arm targets: q=default_q+0.5*action.',
                       'Continuous gripper: each finger target is 0.02*(action+1) m.']),
            robots=dict(panda=dict(model='Franka Panda', joint_names=list(self.robot.joint_names),
                default_joint_positions=defaults, joint_limits=limits, joint_action_scale=.5,
                soft_joint_limits=plain(data.soft_joint_pos_limits[0]),
                base_position=plain(data.root_pos_w[0]), base_quaternion=plain(data.root_quat_w[0]))),
            cameras={}, goal=dict(mode=self.mode, return_position_tolerance_m=.005,
                return_angle_tolerance_rad=math.radians(2), stable_seconds=.5,
                finger_open_min_m=.035, home_joint_tolerance_rad=.05))
        if self._mechanism is not None:
            result['mechanism'] = dict(version='hybrid_fixture_v1')
        return result

    def _contacts(self):
        rows = []
        for side in ('left', 'right'):
            data = self.env.scene[side+'_finger_cube_contact'].data
            forces = np.asarray(plain(data.force_matrix_w[0]), dtype=float)
            if forces.shape != (1,26,3) or not np.isfinite(forces).all():
                raise RuntimeError('Incomplete or nonfinite native finger contacts')
            net = np.asarray(plain(data.net_forces_w[0]), dtype=float)
            if net.shape != (1,3) or not np.isfinite(net).all():
                raise RuntimeError('Invalid native net contact force')
            rows.append(dict(finger=side, cubie_names=list(self.cubie_ids),
                             forces_w=forces[0].tolist(), net_w=net[0].tolist()))
        return rows

    def physical(self, control, physics):
        sample = self.env.read_native_cube_sample()
        data = self.robot.data
        row = dict(control_step=control, physics_step=physics, native=asdict(sample),
            robot=dict(joint_positions=plain(data.joint_pos[0]), joint_velocities=plain(data.joint_vel[0]),
                arm_joint_ids=list(self.arm_ids), finger_joint_ids=list(self.finger_ids),
                hand_position=plain(data.body_pos_w[0,self.hand_id]), hand_quaternion=plain(data.body_quat_w[0,self.hand_id]),
                body_positions=plain(data.body_pos_w[0]), body_quaternions=plain(data.body_quat_w[0])),
            finger_contacts=self._contacts(), submitted_targets=self.submitted_targets)
        if (self.env.sim.current_time_step_index != sample.native_step
                or self.env.sim.current_time != sample.native_time_s):
            raise RuntimeError('Native clock changed during cube and robot extraction')
        if self._mechanism is not None:
            row['mechanism'] = self._mechanism.evidence()
        return row

    def _physics_parameters(self):
        if self._parameters is None:
            view = self.parts.root_physx_view
            # A rigid collection's first native dimension is body, not env.
            # Reading [0] here would silently expose only one of the 31 bodies.
            self._parameters = dict(
                panda=rigid_parameters(self.robot.root_physx_view, body_names=self.robot.body_names),
                cube_parts=dict(body_names=list(self.parts.object_names),
                    mass_kg=plain(view.get_masses()), inertia_kg_m2=plain(view.get_inertias()),
                    material_static_dynamic_restitution=plain(view.get_material_properties()),
                    contact_offset_m=plain(view.get_contact_offsets()), rest_offset_m=plain(view.get_rest_offsets())))
        return self._parameters

    def snapshot(self, control, previous_action):
        measured = self.physical(control, self.physics)
        sample = measured['native']; data = self.robot.data
        _, classified = classify_native_snapshot(sample['body_names'], sample['native_link_transforms_xyzw'],
                                                   ignore_center_twist=True)
        cube = dict(valid=classified['valid'], source='native_physx_link_transforms')
        if classified['valid']:
            cube['facelets_urfdlb'] = classified['measured_facelets_urfdlb']
        pieces = {}
        for name, pose, velocity in zip(sample['body_names'], sample['native_link_transforms_xyzw'],sample['raw_com_velocities']):
            pieces[name] = dict(position=list(pose[:3]), quaternion=[pose[6],*pose[3:6]],
                linear_velocity=list(velocity[:3]), angular_velocity=list(velocity[3:]))
        bodies, jacobians, contacts = {}, {}, []
        jac = self.robot.root_physx_view.get_jacobians()[0]
        for index, name in enumerate(self.robot.body_names):
            bodies['panda.'+name] = dict(position=plain(data.body_pos_w[0,index]),
                quaternion=plain(data.body_quat_w[0,index]), com_position=plain(data.body_com_pos_w[0,index]),
                linear_velocity=plain(data.body_link_lin_vel_w[0,index]), angular_velocity=plain(data.body_link_ang_vel_w[0,index]))
            if index:
                jacobians['panda.'+name] = plain(jac[index-1][:,self.arm_ids])
        for row in measured['finger_contacts']:
            for name, force in zip(row['cubie_names'],row['forces_w']):
                contacts.append(dict(body_a='panda.panda_'+row['finger']+'finger', body_b=name, force_vector_n=force))
        result = dict(robots=dict(panda=dict(joint_names=list(self.robot.joint_names),
            joint_positions=plain(data.joint_pos[0]), joint_velocities=plain(data.joint_vel[0]),
            measured_finger_positions=plain(data.joint_pos[0,self.finger_ids]), previous_action=list(previous_action))),
            privileged=dict(cube=cube, pieces=pieces, robot_bodies=bodies, jacobians=jacobians,
                contacts=contacts if self.physics else [],
                geometry={n:dict(half_extents=[CUBIE_SIZE_M/2]*3) for n in self.cubie_ids},
                physics=dict(physics_hz=120,control_hz=30,timestep_s=1/120,
                    gravity=list(self.env.cfg.sim.gravity),rigid_bodies=self._physics_parameters()),diagnostics={}))
        if self._mechanism is not None:
            result['mechanism'] = self._mechanism.public_state()
        return result

    def physical_arrays(self):
        sample = self.env.read_native_cube_sample()
        data = self.robot.data
        return [np.asarray(sample.native_link_transforms_xyzw), np.asarray(sample.raw_com_velocities),
                np.asarray(plain(data.joint_pos)), np.asarray(plain(data.joint_vel)), np.asarray(plain(data.body_state_w))]

    def _observe_substep(self):
        self.physics += 1
        measured = self.physical(self.control,self.physics)
        self.history.append(measured)
        observer = getattr(self._mechanism, 'observe', None)
        if observer is not None:
            observer(measured)
        if self._hook is not None:
            self._hook()

    def apply(self, action):
        if not self.reset_done:
            raise RuntimeError('Reset required before applying actions')
        bounds = self.describe()['action_spec']
        if (not isinstance(action,list) or len(action)!=8
                or not all(number(x) and lo<=x<=hi for x,lo,hi in zip(action,bounds['low'],bounds['high']))):
            raise ValueError('Invalid Rubik action')
        import torch
        a = np.asarray(action,dtype=np.float32)
        defaults = np.asarray(plain(self.robot.data.default_joint_pos[0]),dtype=np.float32)
        arm = defaults[self.arm_ids] + np.float32(.5)*a[:7]
        fingers = np.full(2,np.float32(.02)*(a[7]+np.float32(1)),dtype=np.float32)
        self.control += 1
        self.submitted_targets = dict(arm=arm.tolist(),fingers=fingers.tolist())
        def submit(q, g):
            self.robot.set_joint_position_target(torch.tensor([q],dtype=torch.float32,device=self.env.device),joint_ids=self.arm_ids)
            self.robot.set_joint_position_target(torch.tensor([g],dtype=torch.float32,device=self.env.device),joint_ids=self.finger_ids)
        def step(*, render):
            self.env._sim_step_counter += 1
            self.env.sim.step(render=render)
        run_decimated_control_cycle(arm_target=arm,finger_target=fingers,decimation=4,render_interval=4,
            physics_dt=self.env.physics_dt,submit_targets=submit,
            apply_passive_detent=getattr(self._mechanism, 'apply_detent', self.env.apply_passive_detent),
            write_data_to_sim=self.env.scene.write_data_to_sim,sim_step=step,scene_update=self.env.scene.update,
            refresh_active_turn_state=self.env.refresh_active_turn_state,render=self.env.sim.render,
            capture=lambda:None,observe_physics_step=self._observe_substep)
        return a.astype(float).tolist()

    def mechanism(self, name, arguments):
        if self._mechanism is None:
            raise RuntimeError('Native mechanism not installed')
        return self._mechanism.command(name,arguments)
