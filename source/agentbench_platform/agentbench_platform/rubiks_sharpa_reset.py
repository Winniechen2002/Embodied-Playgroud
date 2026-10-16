"""Reset-only scorer and replay verifier for Floating Sharpa public cases."""
from __future__ import annotations

from collections import Counter, deque
from copy import deepcopy
import gzip
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import runpy

import numpy as np
from scipy.spatial.transform import Rotation

from .rubiks_physics import load_physics
from .native_clock import period_from_samples, check_elapsed
from .rubiks_cases import case_evidence
from .rubiks_case_evidence import verify_case_binding


def _array(value, shape, label):
    result = np.asarray(value, dtype=float)
    if result.shape != shape or not np.isfinite(result).all():
        raise ValueError(f'invalid {label}')
    return result


def _contacts(row):
    contacts = row.get('finger_contacts')
    if not isinstance(contacts, list) or len(contacts) != 5:
        raise ValueError('incomplete Sharpa contact rows')
    values = []
    for contact in contacts:
        if not isinstance(contact.get('finger'), str):
            raise ValueError('invalid Sharpa contact identity')
        values.append(float(np.max(np.linalg.norm(_array(contact['forces_w'], (26, 3), 'contact forces'), axis=1))))
        _array(contact['net_w'], (3,), 'net contact force')
    return values


def _without_counters(row):
    result = deepcopy(row)
    result.pop('control_step', None)
    result.pop('physics_step', None)
    return result


def _json_equal(left, right):
    """Compare evidence after the same JSON round-trip used by the trace writer."""
    try:
        return json.loads(json.dumps(left, allow_nan=False)) == right
    except (TypeError, ValueError):
        return False


def _official_joint_names():
    """Load the dependency-light official joint order without task registration."""
    spec = importlib.util.find_spec('agentbench')
    if spec is None or not spec.submodule_search_locations:
        raise ValueError('Sharpa source package is unavailable')
    path = Path(next(iter(spec.submodule_search_locations))) / 'sharpa_joint_names.py'
    names = runpy.run_path(str(path))
    return tuple('sharpa.' + name for name in (
        *names['SHARPA_MOTION_JOINT_NAMES'], *names['SHARPA_FINGER_JOINT_NAMES']))


def _validate_sharpa_manifest(data):
    """Validate immutable identity and public-boundary facts before replay."""
    config = data.get('config')
    if not isinstance(config, dict):
        raise ValueError('Sharpa manifest configuration is missing')
    if hashlib.sha256(json.dumps(config, sort_keys=True, allow_nan=False).encode()).hexdigest() != data.get('config_sha256'):
        raise ValueError('Sharpa manifest configuration hash mismatch')
    if config.get('task_family') != 'rubiks_cube' or config.get('embodiment') != 'floating-sharpa':
        raise ValueError('Sharpa trace task identity mismatch')
    if config.get('mode') != 'solve' or config.get('physics_hz') != 120 or config.get('control_hz') != 30:
        raise ValueError('Sharpa trace runtime contract mismatch')
    if config.get('case_id') is None or config.get('case') != case_evidence(config['case_id']):
        raise ValueError('Sharpa case identity mismatch')
    verify_case_binding(config)
    action = config.get('action_spec')
    if not isinstance(action, dict) or action.get('size') != 28:
        raise ValueError('Sharpa trace must use 28 actions')
    names = tuple(action.get('names', ()))
    if names != _official_joint_names():
        raise ValueError('Sharpa action joint order mismatch')
    if (len(action.get('low', ())) != 28 or len(action.get('high', ())) != 28
            or len(action.get('semantics', ())) != 28
            or any(not isinstance(value, (int, float)) or not math.isfinite(value)
                   for values in (action['low'], action['high']) for value in values)
            or any(low > high for low, high in zip(action['low'], action['high']))
            or any(value != 'Absolute native joint target in the declared joint order.'
                   for value in action['semantics'])):
        raise ValueError('Sharpa action bounds or semantics mismatch')
    physical = config.get('physical_spec')
    if (not isinstance(physical, dict) or physical.get('embodiment') != 'floating-sharpa'
            or len(physical.get('joint_ids', ())) != 28
            or len(physical.get('motion_joint_ids', ())) != 6
            or len(physical.get('finger_joint_ids', ())) != 22
            or len(physical.get('home_joint_positions', ())) != 28):
        raise ValueError('Sharpa physical identity is incomplete')
    run_profile = config.get('run_profile')
    if (not isinstance(run_profile, dict) or run_profile.get('observation') != config.get('profile')
            or run_profile.get('tools') != [] or run_profile.get('experience') != 'none'):
        raise ValueError('Sharpa run profile mismatch')
    sources = data.get('sources')
    if not isinstance(sources, dict) or not sources:
        raise ValueError('Sharpa source manifest is missing')
    required = (
        'Floating_Sharpa_right/official_wave_01', 'franka_sharpa_right.py',
        'sharpa_joint_names.py', 'rubiks_cube_sharpa_benchmark.py',
        'rubiks_sharpa_reset.py', 'agentbench_platform_runtime.py',
    )
    for marker in required:
        if not any(marker in path for path in sources):
            raise ValueError('Sharpa source identity missing: ' + marker)
    for path, digest in sources.items():
        if (not isinstance(path, str) or not isinstance(digest, dict)
                or not isinstance(digest.get('sha256'), str)
                or len(digest['sha256']) != 64 or not isinstance(digest.get('bytes'), int)
                or digest['bytes'] <= 0):
            raise ValueError('invalid Sharpa source manifest entry')
    return config


def _validate_public_boundary(directory):
    """Reject private reset fields copied into the agent-visible directory."""
    public = Path(directory).parent / 'public'
    if not public.is_dir():
        return
    forbidden = ('scramble', 'seed', 'expected_facelets', 'permutation_checksum',
                 'logical_orientation', 'yaw_rad', 'support_geometry', 'native_journal')
    for path in public.rglob('*'):
        if path.is_file() and path.name != 'token':
            text = path.read_text(errors='replace')
            if any(term in text for term in forbidden):
                raise ValueError('private Rubik field leaked into public evidence')


class SharpaResetScorer:
    """Online/replay scorer for initialization only; it never claims solve success."""

    def __init__(self, mode, spec, initialization, *, initialization_after_step, target_sequence=None):
        if mode != 'solve' or target_sequence is not None:
            raise ValueError('Sharpa reset scorer only supports solve initialization')
        self.mode = mode
        self.physics = load_physics()
        self.spec = deepcopy(spec)
        self.initial = deepcopy(initialization[-1]) if initialization else None
        if not isinstance(initialization, list) or len(initialization) < 61:
            raise ValueError('complete Sharpa initialization evidence required')
        self.initial_native = self.physics.native.NativeCubeSample(**self.initial['native'])
        first = initialization[0]['native']
        self.native_clock_period = period_from_samples(first['native_step'], first['native_time_s'],
                                                       self.initial_native.native_step,
                                                       self.initial_native.native_time_s)
        self.names = self.initial_native.body_names
        self.joint_ids = tuple(spec['joint_ids'])
        self.finger_ids = tuple(spec['finger_joint_ids'])
        if len(self.joint_ids) != 28 or len(self.finger_ids) != 22:
            raise ValueError('Sharpa reset specification must expose 28 joints and 22 fingers')
        self.expected_target = self.spec.get('initial_target')
        if not isinstance(self.expected_target, dict):
            raise ValueError('Sharpa reset target is missing')
        for row in initialization:
            self._validate_row(row)
            if max(_contacts(row)) > 20.:
                raise ValueError('Sharpa initialization contact force exceeds 20 N')
        samples = [self.physics.native.NativeCubeSample(**row['native']) for row in initialization]
        measured, stable = self.physics.native.evaluate_native_cube_window(
            samples, physics_dt_s=1 / 120, after_step=initialization_after_step,
            minimum_duration_s=.5, ignore_center_twist=False)
        final_state = measured
        expected_state = self.physics.rules.CubeState.solved()
        # The catalog checksum is authoritative; reconstruct it through the
        # dependency-light rules module rather than trusting a stored state.
        expected_state = expected_state.apply_sequence(self.spec.get('initial_scramble', ''))
        exact, exact_diag = self.physics.native.classify_native_snapshot(
            self.initial_native.body_names, self.initial_native.native_link_transforms_xyzw,
            ignore_center_twist=False)
        state_matches = (final_state is not None and exact is not None
                         and exact.permutation_checksum() == self.expected_target['permutation_checksum']
                         and final_state.facelet_string() == self.expected_target['facelets_urfdlb'])
        support = self.physics.native.measure_native_support_geometry(
            self.initial_native, table_height_m=spec['table_height_m'], include_stickers=True)
        positions = _array([row['robot']['joint_positions'] for row in initialization],
                           (len(initialization), len(self.joint_ids)), 'joint positions')
        home = _array(spec['home_joint_positions'], (28,), 'home joint positions')
        target_position = _array(self.expected_target['position'], (3,), 'target position')
        target_quaternion = _array(self.expected_target['quaternion'], (4,), 'target quaternion')
        native_core = self.initial_native.native_link_transforms_xyzw[
            self.names.index('core')]
        core_position = _array(native_core[:3], (3,), 'native core position')
        core_quaternion = _array([native_core[6], *native_core[3:6]], (4,), 'native core quaternion')
        angle = (Rotation.from_quat(core_quaternion[[1, 2, 3, 0]])
                 * Rotation.from_quat(target_quaternion[[1, 2, 3, 0]]).inv()).magnitude()
        gates = dict(native_configuration=measured is not None,
                     stable=bool(stable['stable']),
                     state_matches=state_matches,
                     requested_pose=(np.linalg.norm(core_position - target_position) <= .001 + 1e-12
                                     and angle <= math.radians(2) + 1e-12),
                     supported=abs(support['table_gap_m']) <= .002,
                     joint_positions_finite=True,
                     home_within_tolerance=bool(np.max(np.abs(positions[:, self.joint_ids] - home)) <= .05 + 1e-12),
                     contact_force_within_limit=max(max(_contacts(row)) for row in initialization) <= 20.)
        self.initialization = dict(passed=all(gates.values()), gates=gates,
            stable_window=stable, support=support,
            exact_state_diagnostics=exact_diag,
            expected_facelets_urfdlb=self.expected_target['facelets_urfdlb'],
            expected_permutation_checksum=self.expected_target['permutation_checksum'])
        if not self.initialization['passed']:
            raise ValueError('Sharpa initialization physical gates failed')
        self.rows = deque(maxlen=61)
        self.last_row = self.initial
        self.after_step = self.initial_native.native_step
        self.observed_substeps = self.last_control = 0
        self.coverage_complete = True
        self.hard_failure = False
        self.failure_reasons = set()
        self.pending = []

    def _validate_row(self, row):
        native = self.physics.native.NativeCubeSample(**row['native'])
        if native.body_names != self.names:
            raise ValueError('native body ordering changed')
        robot = row['robot']
        _array(robot['joint_positions'], (28,), 'joint positions')
        _array(robot['joint_velocities'], (28,), 'joint velocities')
        _array(robot['hand_position'], (3,), 'hand position')
        _array(robot['hand_quaternion'], (4,), 'hand quaternion')
        _contacts(row)
        return native

    def audit_substep(self, row):
        try:
            native = self._validate_row(row)
            step = self.observed_substeps + 1
            if (row['physics_step'] != step or row['control_step'] != (step + 3) // 4
                    or native.native_step != self.initial_native.native_step + step
                    or len(self.pending) >= 4):
                raise ValueError('noncontiguous Sharpa reset evidence')
            check_elapsed(native.native_time_s, self.initial_native.native_time_s,
                          step, self.native_clock_period)
            self.observed_substeps = step
            self.pending.append(hashlib.sha256(json.dumps(row, sort_keys=True, allow_nan=False).encode()).hexdigest())
            self.last_row = deepcopy(row)
            self.rows.append(self.last_row)
        except (KeyError, TypeError, ValueError) as exc:
            self.hard_failure = True
            self.coverage_complete = False
            self.failure_reasons.add('invalid_substep: ' + str(exc))
        return dict(hard_failure=self.hard_failure, coverage_complete=self.coverage_complete,
                    max_contact_force_n=max(_contacts(row)))

    def update(self, snapshot, substep_audits=()):
        try:
            if len(substep_audits) != 4 or len(self.pending) != 4:
                raise ValueError('incomplete Sharpa control interval')
            self.last_control += 1
        except (KeyError, TypeError, ValueError) as exc:
            self.hard_failure = True
            self.coverage_complete = False
            self.failure_reasons.add('invalid_control: ' + str(exc))
        self.pending.clear()
        return self.result()

    def result(self):
        return dict(success=False, physical_success=False, hard_failure=self.hard_failure,
            failure_reasons=sorted(self.failure_reasons), coverage_complete=self.coverage_complete,
            observed_substeps=self.observed_substeps, control_steps=self.last_control,
            initialization=deepcopy(self.initialization), detection_scope='31 native bodies, Sharpa proprioception, five native contact sensors')


def verify_sharpa_reset_trace(directory):
    """Replay a Sharpa reset trace and reject Panda-shaped or hidden-state traces."""
    directory = directory if hasattr(directory, 'joinpath') else __import__('pathlib').Path(directory)
    trace = directory / 'trace.jsonl.gz'
    saved = json.loads((directory / 'result.json').read_text())
    config = None
    counts = Counter()
    initialization = []
    init_begin = None
    scorer = None
    controls = substeps = 0
    action = None
    samples = []
    final = None
    with gzip.open(trace, 'rt') as stream:
        for line in stream:
            row = json.loads(line)
            kind, data = row['kind'], row['data']
            counts[kind] += 1
            if final is not None:
                raise ValueError('Sharpa trace contains records after final')
            if kind == 'manifest':
                if counts['manifest'] != 1 or sum(counts.values()) != 1:
                    raise ValueError('invalid Sharpa manifest boundary')
                config = _validate_sharpa_manifest(data)
            elif kind == 'initialization_begin':
                if config is None or init_begin is not None or scorer is not None:
                    raise ValueError('invalid Sharpa initialization boundary')
                init_begin = data
            elif kind == 'initialization_substep':
                if (init_begin is None or scorer is not None
                        or data.get('index') != len(initialization) + 1):
                    raise ValueError('invalid Sharpa initialization sample order')
                native = load_physics().native.NativeCubeSample(**data['snapshot']['native'])
                if native.native_step != init_begin['after_step'] + len(initialization) + 1:
                    raise ValueError('invalid Sharpa initialization chronology')
                initialization.append(data['snapshot'])
            elif kind == 'initialization':
                if init_begin is None or scorer is not None or counts['initialization'] != 1:
                    raise ValueError('missing Sharpa initialization boundary')
                scorer = SharpaResetScorer(config['mode'], config['physical_spec'], data['samples'],
                    initialization_after_step=data['after_step'])
                if (data.get('initialization_substeps') != len(initialization)
                        or data.get('after_step') != init_begin.get('after_step')
                        or not _json_equal(data.get('samples'), initialization)):
                    raise ValueError('Sharpa initialization samples mismatch')
                if not _json_equal(scorer.initialization, data['validation']):
                    raise ValueError('Sharpa initialization validation mismatch')
            elif kind == 'reset':
                if (scorer is None or counts['reset'] != 1 or data['contacts_fresh'] is not True
                        or not _json_equal(data.get('physical'), scorer.initial)):
                    raise ValueError('invalid Sharpa reset endpoint')
            elif kind == 'action_begin':
                if action is not None or len(data['requested_action']) != 28:
                    raise ValueError('invalid Sharpa action boundary')
                action = data
            elif kind == 'substep':
                if action is None or len(samples) >= 4:
                    raise ValueError('invalid Sharpa substep order')
                substeps += 1
                scorer.audit_substep(data['snapshot'])
                samples.append(data['snapshot'])
            elif kind == 'control':
                if action is None or len(samples) != 4:
                    raise ValueError('incomplete Sharpa control')
                controls += 1
                scorer.update(samples[-1], samples)
                action = None
                samples = []
            elif kind == 'final':
                final = data
            elif kind in {'capture', 'native_error'}:
                continue
            else:
                raise ValueError('unsupported Sharpa trace record: ' + kind)
    _validate_public_boundary(directory)
    if (config is None or scorer is None or final is None or saved != final
            or any(counts[name] != 1 for name in ('manifest', 'initialization', 'reset', 'final'))):
        raise ValueError('incomplete Sharpa reset trace')
    if not _json_equal(scorer.result(), final['result']):
        raise ValueError('Sharpa final result mismatch')
    return dict(kind='independent_sharpa_reset_recompute', task_family='rubiks_cube',
        embodiment='floating-sharpa', valid=True, controls=controls, substeps=substeps,
        final=final, case=case_evidence(config['case_id']) if config.get('case_id') else None,
        case_binding_verified=config.get('case_id') is not None,
        initialization=scorer.initialization,
        trace_sha256=hashlib.sha256(trace.read_bytes()).hexdigest(),
        evidence_coverage=dict(complete=not scorer.hard_failure, control_attempts=controls))
