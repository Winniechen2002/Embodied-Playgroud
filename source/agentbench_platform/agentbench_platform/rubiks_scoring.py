"""Independent Rubik episode scorer over raw 120 Hz and joint-readback evidence.

No agent phases, route indices, symbolic environment cache or self-reported
completion enter this scorer. Its constraint checks cover the declared cube
joint graph, not arbitrary constraints elsewhere in the scene. Runtime ownership
and the no-body-write policy remain separate enforcement requirements.
"""
from collections import deque
from copy import deepcopy
import hashlib
import json
import math

import numpy as np
from scipy.spatial.transform import Rotation

from .rubiks_physics import load_physics
from .tasks import validate_task
from .native_clock import period_from_samples,check_elapsed


def _digest(row):
    return hashlib.sha256(json.dumps(row, sort_keys=True, allow_nan=False).encode()).hexdigest()


def _array(value, shape):
    value = np.asarray(value, dtype=float)
    if value.shape != shape or not np.isfinite(value).all():
        raise ValueError('Invalid native measurement')
    return value


def contact_pair(row, names):
    contacts = row['finger_contacts']
    if not isinstance(contacts, list) or len(contacts) != 2:
        raise ValueError('Incomplete bilateral contacts')
    result = []
    for side, contact in zip(('left', 'right'), contacts):
        if contact['finger'] != side or contact['cubie_names'] != list(names):
            raise ValueError('Contact body ordering changed')
        forces = _array(contact['forces_w'], (26, 3))
        _array(contact['net_w'], (3,))
        result.append(float(np.max(np.linalg.norm(forces, axis=1))))
    return result


class RubiksScorer:
    """Online and replay use the same deterministic raw-evidence computation."""
    def __init__(self, mode, spec, initialization, *, initialization_after_step, target_sequence=None):
        self.physics = load_physics()
        self.mode = mode
        self.target_sequence = validate_task('rubiks_cube', mode, target_sequence)
        self.spec = deepcopy(spec)
        initial_target = self.spec.pop('initial_target', None)
        ids = list(spec['arm_joint_ids'])+list(spec['finger_joint_ids'])
        if (len(spec['arm_joint_ids']) != 7 or len(spec['finger_joint_ids']) != 2
                or any(type(i) is not int for i in ids) or sorted(ids) != list(range(9))
                or not math.isfinite(spec['table_height_m'])):
            raise ValueError('Invalid Panda/scene specification')
        home = _array(spec['home_joint_positions'], (7,))
        if not isinstance(initialization, list) or len(initialization) < 61:
            raise ValueError('Complete accepted initialization evidence required')
        self.initial = deepcopy(initialization[-1])
        self.initial_native = self.physics.native.NativeCubeSample(**self.initial['native'])
        first=initialization[0]['native']
        self.native_clock_period=period_from_samples(first['native_step'],first['native_time_s'],
            self.initial_native.native_step,self.initial_native.native_time_s)
        self.names = tuple(sorted(n for n in self.initial_native.body_names if n.startswith('cubie_')))
        self.fixture = self.physics.constraints.ConstraintAudit(self.initial['mechanism']['joints'])
        for row in initialization:
            self._validate_row(row)
            self.fixture.verify_current(row['mechanism']['joints'])
            if row['mechanism']['epoch'] != 0 or row['mechanism']['state'] != 'idle':
                raise ValueError('Initialization fixture is not idle')
            if max(self._contact_pair(row)) > 20.:
                raise ValueError('Initialization excessive contact force')
        # The post-reset window establishes the reference; subsequent terminal
        # windows must be strictly newer than its final native step.
        measured, stable = self.physics.native.evaluate_native_cube_window(
            [self.physics.native.NativeCubeSample(**r['native']) for r in initialization],
            physics_dt_s=1/120, after_step=initialization_after_step, ignore_center_twist=True)
        q = np.array([r['robot']['joint_positions'] for r in initialization])
        support = self.physics.native.measure_native_support_geometry(self.initial_native,
            table_height_m=spec['table_height_m'], include_stickers=True)
        gates = dict(native_configuration=measured is not None, stable=bool(stable['stable']),
            fingers_open=bool(np.min(q[:,spec['finger_joint_ids']]) >= .035-1e-12),
            arm_home=bool(np.max(np.abs(q[:,spec['arm_joint_ids']]-home)) <= .05+1e-12),
            supported=abs(support['table_gap_m']) <= .002)
        if initial_target is not None:
            pose = self._core(self.initial)
            target_position = _array(initial_target['position'], (3,))
            target_rotation = self.physics.events.hand_rotation(initial_target['quaternion'])
            angle = (Rotation.from_quat(pose[3:])*Rotation.from_matrix(target_rotation).inv()).magnitude()
            gates['requested_configuration'] = bool(measured is not None and
                measured.facelet_string() == initial_target['facelets_urfdlb'])
            gates['requested_pose'] = bool(np.linalg.norm(pose[:3]-target_position) <= .001+1e-12
                and angle <= math.radians(2)+1e-12)
            if 'permutation_checksum' in initial_target:
                # The catalog specifies the complete cubie state, including
                # single-color center spins. Ordinary solve scoring may ignore
                # those spins; trusted initialization must match them exactly.
                exact, _ = self.physics.native.classify_native_snapshot(
                    self.initial_native.body_names, self.initial_native.native_link_transforms_xyzw,
                    ignore_center_twist=False)
                gates['requested_permutation'] = bool(exact is not None and
                    exact.permutation_checksum() == initial_target['permutation_checksum'])
        accepted = dict(passed=all(gates.values()), gates=gates, stable_window=stable, support=support)
        if not accepted['passed']:
            raise ValueError('Initialization physical gates failed')
        self.initialization = accepted
        self.turns = self.physics.events.MeasuredTurns(self.initial_native,
            hand_quaternion_wxyz=self.initial['robot']['hand_quaternion'])
        self.rows = deque(maxlen=61)
        self.last_row = self.initial
        self.after_step = self.initial_native.native_step
        self.observed_substeps = self.last_control = 0
        self.coverage_complete = True
        self.hard_failure = False
        self.failure_reasons = set()
        self.pending = []
        self.terminal = dict(passed=False, reason='insufficient_stable_window')
        self.peak_contact_force_n = 0.
        self.turn_request = None
        self.turn_event_count = 0
        self.transport = None

    def _contact_pair(self, row):
        return contact_pair(row, self.names)

    def _terminal_window(self):
        # Embodiment is metadata, not an argument of the physical predicate.
        spec={k:v for k,v in self.spec.items() if k != 'embodiment'}
        return self.physics.terminal.evaluate_terminal_window(list(self.rows),
            initial_native=self.initial_native, after_step=self.after_step, **spec)

    def _grasp_ready(self, row):
        q=np.array(row['robot']['joint_positions'])[self.spec['finger_joint_ids']]
        return min(self._contact_pair(row)) > .5 and bool(np.all((q>=0)&(q<=.04)))

    def _released(self, row):
        return bool(min(np.array(row['robot']['joint_positions'])[self.spec['finger_joint_ids']]) >= .035)

    def _validate_row(self, row):
        native = self.physics.native.NativeCubeSample(**row['native'])
        if native.body_names != self.initial_native.body_names:
            raise ValueError('Native body ordering changed')
        robot = row['robot']
        if (robot['arm_joint_ids'] != self.spec['arm_joint_ids']
                or robot['finger_joint_ids'] != self.spec['finger_joint_ids']):
            raise ValueError('Panda joint ordering changed')
        _array(robot['joint_positions'], (9,)); _array(robot['joint_velocities'], (9,))
        _array(robot['hand_position'], (3,))
        self.physics.events.hand_rotation(robot['hand_quaternion'])
        if row['mechanism']['version'] != 'hybrid_fixture_v1':
            raise ValueError('Fixture version mismatch')
        self._contact_pair(row)
        return native

    def _fail(self, reason, *, coverage=False):
        self.hard_failure = True
        self.failure_reasons.add(reason)
        if coverage:
            self.coverage_complete = False

    def _core(self, row):
        n = row['native']
        return np.asarray(n['native_link_transforms_xyzw'][n['body_names'].index('core')], dtype=float)

    def _fixed_relations(self, row):
        _, poses = self.physics.constraints._poses(row)
        for name, joint in self.fixture.joints.items():
            if joint['enabled'] and joint['type'] == 'PhysicsFixedJoint':
                actual = deepcopy(joint)
                self.physics.constraints._capture(actual, poses)
                position = np.linalg.norm(np.array(actual['position0'])-joint['position0'])
                a, b = np.array(actual['quaternion0']), np.array(joint['quaternion0'])
                angle = (Rotation.from_quat(a[[1,2,3,0]])*Rotation.from_quat(b[[1,2,3,0]]).inv()).magnitude()
                tolerance = math.radians(1 if name == 'robot_hand_core_attachment' else 2)
                if position > .001+1e-12 or angle > tolerance+1e-12:
                    raise ValueError('Native fixed-joint relation exceeded tolerance: '+name)

    def audit_substep(self, row):
        """Each real substep is audited exactly once, before the control result."""
        try:
            native = self._validate_row(row)
            step = self.observed_substeps+1
            if (type(row['physics_step']) is not int or row['physics_step'] != step
                    or type(row['control_step']) is not int or row['control_step'] != (step+3)//4
                    or native.native_step != self.initial_native.native_step+step
                    or len(self.pending) >= 4):
                raise ValueError('Noncontiguous episode evidence')
            check_elapsed(native.native_time_s,self.initial_native.native_time_s,step,self.native_clock_period)
            self.fixture.verify_current(row['mechanism']['joints'])
            if (row['mechanism']['epoch'] != self.fixture.epoch or row['mechanism']['state'] != self.fixture.state):
                raise ValueError('Unrecorded fixture transition')
            self._fixed_relations(row)
            forces = self._contact_pair(row)
            self.peak_contact_force_n = max(self.peak_contact_force_n, *forces)
            if max(forces) > 20.:
                self._fail('excessive_contact_force')
            event = self.turns.observe(native, hand_quaternion_wxyz=row['robot']['hand_quaternion'],
                                       finger_contact_forces_n=forces)
            if event is not None and self.fixture.state != 'turning':
                raise ValueError('Measured face turn outside active layer transaction')
            if self.transport is not None and self.fixture.state == 'attached':
                core = self._core(row)
                self.transport['peak_lift_m'] = max(self.transport['peak_lift_m'],
                    float(core[2]-self.transport['start_core'][2]))
                if not self.transport['verified']:
                    for current, before in ((core, self.transport['attached_core']),
                        (np.r_[row['robot']['hand_position'], np.array(row['robot']['hand_quaternion'])[[1,2,3,0]]],
                         self.transport['attached_hand'])):
                        if (np.linalg.norm(current[:3]-before[:3]) > .001+1e-12
                                or (Rotation.from_quat(current[3:])*Rotation.from_quat(before[3:]).inv()).magnitude() > math.radians(1)+1e-12):
                            raise ValueError('Attachment activation jump')
                    self.transport['verified'] = True
            self.observed_substeps = step
            self.pending.append(_digest(row))
            self.last_row = deepcopy(row)
            self.rows.append(self.last_row)
        except (KeyError, TypeError, ValueError) as exc:
            self._fail('invalid_substep: '+str(exc), coverage=True)
        return dict(hard_failure=self.hard_failure, coverage_complete=self.coverage_complete,
                    max_contact_force_n=self.peak_contact_force_n)

    def update(self, snapshot, substep_audits=()):
        """Complete one four-substep interval without re-auditing or double counting."""
        try:
            if (len(substep_audits) != 4 or len(self.pending) != 4
                    or [_digest(s) for s in substep_audits] != self.pending
                    or _digest(snapshot) != self.pending[-1]
                    or snapshot['control_step'] != self.last_control+1
                    or snapshot['physics_step'] != 4*(self.last_control+1)):
                raise ValueError('Incomplete or repeated control interval')
            self.last_control += 1
            if len(self.rows) == 61:
                self.terminal = self._terminal_window()
        except (KeyError, TypeError, ValueError) as exc:
            self._fail('invalid_control: '+str(exc), coverage=True)
        self.pending.clear()
        return self.result()

    def _stable(self):
        if len(self.rows) < 61:
            raise ValueError('Fresh stable window unavailable')
        samples = [self.physics.native.NativeCubeSample(**r['native']) for r in self.rows]
        state, report = self.physics.native.evaluate_native_cube_window(samples, physics_dt_s=1/120,
            after_step=self.after_step, ignore_center_twist=True)
        if state is None or not report['stable']:
            raise ValueError('Fixture transition requires a stable valid cube')
        return state

    def mechanism_plan(self, name, arguments):
        """Pure private proposal: guards + expected joint exchange, no scene writes."""
        if self.hard_failure or self.pending:
            raise ValueError('Fixture request outside healthy control boundary')
        row = self.last_row
        expected = self.fixture.expected_transaction(name, arguments, row)
        forces = self._contact_pair(row)
        if name != 'detent.begin':
            measured = self._stable()
        if name in ('turn.begin', 'detent.begin') and max(forces) > .5:
            raise ValueError('Layer/detent activation requires unloaded fingers')
        if name == 'turn.end':
            if (len(self.turns.events) != self.turn_event_count+1
                    or self.turns.events[-1]['move'] != self.turn_request or self.turns.active is not None):
                raise ValueError('No measured requested quarter turn to commit')
        if name == 'transport.attach':
            for r in list(self.rows)[-3:]:
                if not self._grasp_ready(r):
                    raise ValueError('Three real bilateral grasp samples required')
            # Unlike a reference controller's desired hand pose, these frames
            # come only from measured poses; acquisition requires no 1 mm jump.
            positions = np.array([r['robot']['hand_position'] for r in list(self.rows)[-3:]])
            if max(np.linalg.norm(positions-positions[-1],axis=1)) > .001:
                raise ValueError('Measured grasp has not settled')
        if name == 'transport.capture_support':
            if not self.transport['verified'] or self.transport['peak_lift_m'] < .04-1e-12:
                raise ValueError('Fresh verified attachment and measured 4 cm lift required')
            if measured.facelet_string() != self.transport['facelets']:
                raise ValueError('Internal cube changed during transport')
            core = self._core(row)
            target = Rotation.from_matrix(self.transport['target_frame'])
            if (np.linalg.norm(core[:3]-self.transport['start_core'][:3]) > .005+1e-12
                    or (Rotation.from_quat(core[3:])*target.inv()).magnitude() > math.radians(3)+1e-12):
                raise ValueError('Transport placement differs from declared target')
            support = self.physics.native.measure_native_support_geometry(
                self.physics.native.NativeCubeSample(**row['native']),
                table_height_m=self.spec['table_height_m'], include_stickers=True)
            if abs(support['table_gap_m']) > .002:
                raise ValueError('Measured table support missing')
        if name in ('transport.release', 'transport.end'):
            if any(not self._released(r) for r in list(self.rows)[-4:]):
                raise ValueError('Transport release needs open measured fingers')
        return expected

    def mechanism_event(self, event):
        """Recompute accepted operations; a result/phase flag is never proof."""
        try:
            before, after = event['before'], event['after']
            if (event['control_step'] != self.last_control or event['physics_step'] != self.observed_substeps
                    or _digest(before) != _digest(self.last_row)
                    or _digest({k:v for k,v in before.items() if k != 'mechanism'}) !=
                       _digest({k:v for k,v in after.items() if k != 'mechanism'})):
                raise ValueError('Fixture command changed physics or used stale evidence')
            accepted = event['result']['accepted']
            if type(accepted) is not bool:
                raise ValueError('Invalid mechanism receipt')
            if not accepted:
                if _digest(before) != _digest(after):
                    raise ValueError('Rejected command mutated fixture')
                return
            name, arguments = event['name'], event['arguments']
            expected = self.mechanism_plan(name, arguments)
            self.physics.constraints.compare_joints(expected, after['mechanism']['joints'])
            if name == 'turn.begin':
                self.turn_request = arguments['move']; self.turn_event_count = len(self.turns.events)
            if name == 'transport.begin':
                self.transport = dict(start_core=self._core(before), target_frame=arguments['target_frame'],
                    facelets=self.turns.measured_state.facelet_string(), peak_lift_m=0., verified=False)
            if name == 'transport.attach':
                self.transport['attached_core'] = self._core(before)
                self.transport['attached_hand'] = np.r_[before['robot']['hand_position'],
                    np.array(before['robot']['hand_quaternion'])[[1,2,3,0]]]
            self.fixture.accept(name, arguments, before, after['mechanism']['joints'])
            for receipt in (after['mechanism'], event['result']):
                if receipt['state'] != self.fixture.state or receipt['epoch'] != self.fixture.epoch:
                    raise ValueError('Fixture receipt differs from actual transaction')
            self.last_row = deepcopy(after)
            self.after_step = after['native']['native_step']
            self.rows.clear(); self.turns.invalidate_window(self.after_step)
            self.terminal = dict(passed=False, reason='post_transition_window_required')
        except (KeyError, TypeError, ValueError) as exc:
            self._fail('invalid_mechanism: '+str(exc), coverage=True)

    def result(self):
        sequence = (self.physics.terminal.sequence_goal(self.target_sequence, self.turns.events)
                    if self.mode == 'execute_sequence' else None)
        task = (sequence['passed'] if sequence is not None else self.terminal.get('cube', {}).get('solved', False))
        physical = bool(self.terminal['passed'] and task and self.fixture.state == 'idle' and self.turns.active is None)
        return dict(success=bool(physical and not self.hard_failure and self.coverage_complete and not self.pending),
            physical_success=physical, hard_failure=self.hard_failure, failure_reasons=sorted(self.failure_reasons),
            coverage_complete=self.coverage_complete, observed_substeps=self.observed_substeps,
            control_steps=self.last_control, fixture_epoch=self.fixture.epoch,
            measured_quarters=[e['move'] for e in self.turns.events], terminal=deepcopy(self.terminal),
            sequence=sequence, peak_contact_force_n=self.peak_contact_force_n,
            detection_scope='31 native bodies, Panda proprioception, bilateral cubie contacts, declared cube USD joints')
