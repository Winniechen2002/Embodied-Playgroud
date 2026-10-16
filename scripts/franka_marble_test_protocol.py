"""Private, deterministic four-trial campaign protocol; no simulator dependency.

The schedule is public and RGB remains authentic. Metadata omission is not
statistical blinding or an OS sandbox: theme appearance can reveal a trial.
"""
import copy
import hashlib
import math

# Compatibility import for historical workers; the environment owns the schedule.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'source/agentbench_platform'))
from agentbench_platform.marble_protocol import (
    PROTOCOL_VERSION, PUBLIC_TASK_METADATA_VERSION, PROTOCOLS, PUBLIC_VARIATION_NOTICE,
    THEMES, SPRINGS, LAUNCHER_X, AMMUNITION_OFFSETS, MOTIONS, ENV_DEFAULTS,
    PUBLIC_VARIANT_KEYS, protocol_trials,
)


def trial_variant(base_variant, trial_record):
    out = copy.deepcopy(base_variant or {})
    if trial_record is not None:
        out.update(copy.deepcopy(trial_record['environment_parameters']))
    return out


def validate_protocol(protocol, variant, *, scenario=None, trial_index=None):
    if protocol not in PROTOCOLS:
        raise ValueError('Unknown test protocol')
    if trial_index is not None and (isinstance(trial_index, bool) or trial_index not in range(1, 5)):
        raise ValueError('Trial index must be 1..4')
    spring = variant.get('spring_stiffness', 25.)
    if isinstance(spring, bool) or not isinstance(spring, (int, float)) or not math.isfinite(spring) or spring <= 0:
        raise ValueError('Spring stiffness must be positive and finite')
    for key in ('launcher_offset_m', 'ammunition_offset_m'):
        value = variant.get(key, (0., 0., 0.))
        if not isinstance(value, (list, tuple)) or len(value) != 3 or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in value):
            raise ValueError(key+' must contain three finite numbers')
    if variant.get('background_motion', 'static') not in MOTIONS:
        raise ValueError('Unknown background motion')
    if protocol == 'legacy':
        if trial_index is not None:
            raise ValueError('--trial-index requires --test-protocol four-trial-v1')
        return
    expected = dict(target_profile='authored', variation='nominal', position_randomization='off',
                    background='park', visual_seed=None, **ENV_DEFAULTS)
    for key, default in expected.items():
        value = variant.get(key, default)
        if isinstance(default, tuple):
            value = tuple(value)
        if value != default:
            raise ValueError(f'{PROTOCOL_VERSION} controls {key}; use default authored/nominal/off settings '
                             'or --test-protocol legacy for custom variations')


def select_trial(protocol, scenario, base_seed, variant, trial_index=None):
    validate_protocol(protocol, variant, scenario=scenario, trial_index=trial_index)
    if protocol == 'legacy':
        return None
    if not scenario:
        raise ValueError('four-trial-v1 requires a campaign --scenario')
    # A single-episode worker defaults to the first reproducible trial.
    return protocol_trials(scenario, base_seed)[(trial_index or 1)-1]


def public_configuration(request, protocol=None):
    """Public task configuration, including the current spring constant in N/m.

    The harness owns request and protocol. For registered trials, the selected
    trial is authoritative even if request contains stale or forged metadata.
    Only this one physical constant is disclosed; no whole private record passes.
    """
    request = request or {}
    out = {key: copy.deepcopy(request[key]) for key in PUBLIC_VARIANT_KEYS if key in request}
    spring = request.get('spring_stiffness', ENV_DEFAULTS['spring_stiffness'])
    if protocol and protocol.get('version') == PROTOCOL_VERSION:
        spring = protocol['environment_parameters']['spring_stiffness']
        out.pop('background', None)
        out.pop('visual_seed', None)
    if isinstance(spring, bool) or not isinstance(spring, (int, float)) or not math.isfinite(spring) or spring <= 0:
        raise ValueError('Public spring stiffness must be positive and finite')
    out.update(spring_stiffness=float(spring), spring_stiffness_unit='N/m')
    return out


def environment_variant(env, request=None, protocol=None):
    """Use the actual environment's configured spring, without reading hidden state.

    Read only the compiled draw joint's static spring constant when available.
    Legacy adapters without that model retain their configured scalar/request
    (or the original 25 N/m default). A registered trial mismatch fails closed.
    """
    out = copy.deepcopy(request or {})
    model = getattr(env, 'model', None)
    actual = (float(model.jnt_stiffness[model.joint('draw').id])
              if hasattr(model, 'jnt_stiffness') else getattr(env, 'spring_stiffness', None))
    if actual is not None:
        if protocol and protocol.get('version') == PROTOCOL_VERSION:
            expected = protocol['environment_parameters']['spring_stiffness']
            if actual != expected:
                raise ValueError('Environment spring stiffness differs from selected trial')
        out['spring_stiffness'] = float(actual)
    public_configuration(out, protocol)
    return out


def task_metadata_version(rows):
    """Never pool results from different public information contracts."""
    versions = {row.get('task_metadata_version') for row in rows}
    if len(versions) > 1:
        raise ValueError('Cannot aggregate mixed task metadata versions')
    version = next(iter(versions), None)
    if version not in (None, PUBLIC_TASK_METADATA_VERSION):
        raise ValueError('Unrecognized task metadata version')
    return version


def add_protocol_arguments(parser, *, single=False, default=PROTOCOL_VERSION):
    parser.add_argument('--test-protocol', choices=PROTOCOLS, default=default,
                        help='Four fixed trials per campaign task; legacy keeps custom single-run behavior')
    if single:
        parser.add_argument('--trial-index', '--trial', dest='trial_index', type=int, choices=range(1, 5),
                            help='Private reproducible trial selection (default 1); four-trial-v1 only')


def trial_identity(scenario, mode, base_seed, operation_key, trial_record):
    """Private IDs shared by batch, worker and preview runners."""
    if trial_record is None:
        return dict(episode_id=f'{scenario}--{mode}--seed-{base_seed}')
    group = f'{scenario}--{mode}--{operation_key}--seed-{base_seed}'
    return dict(task_group_id=group,
                episode_id=f'{group}--{PROTOCOL_VERSION}--trial-{trial_record["trial_index"]}')


def summarize_protocol(rows):
    metadata_version = task_metadata_version(rows)
    groups = {}
    for row in rows:
        record = row.get('test_protocol') or {}
        if not record or record.get('version') == 'legacy':
            continue
        if record.get('version') != PROTOCOL_VERSION:
            raise ValueError('Unrecognized protocol version in result record')
        expected = protocol_trials(row['scenario'], row['seed'])
        index = record.get('trial_index')
        if isinstance(index, bool) or index not in range(1, 5) or record != expected[index-1]:
            raise ValueError('Protocol record differs from the registered schedule')
        request = row.get('variation_request', {})
        if any(request.get(k) != v for k, v in record['environment_parameters'].items()):
            raise ValueError('Actual variation request differs from protocol record')
        base = {k:v for k,v in request.items() if k not in record['environment_parameters']}
        validate_protocol(PROTOCOL_VERSION, base)
        operation_key = row.get('operation_profile_requested') or row.get('difficulty', {}).get('operation_profile', 'authored')
        identity_fields = trial_identity(row['scenario'], row['mode'], row['seed'], operation_key, record)
        if any(row.get(k) != v for k,v in identity_fields.items()):
            raise ValueError('Protocol episode/group identity differs from configuration')
        key = row['task_group_id']
        groups.setdefault(key, []).append(row)
    tasks = {}
    for key, values in groups.items():
        indices = [v['test_protocol']['trial_index'] for v in values]
        if len(indices) != len(set(indices)) or any(i not in range(1, 5) for i in indices):
            raise ValueError('Duplicate or invalid protocol trial in task group: '+key)
        reference = values[0]
        identity = lambda v: (v['scenario'], v['mode'], v['seed'], v.get('operation_profile_requested'),
                              v.get('variation_request', {}).get('yaw_enabled'))
        if any(identity(v) != identity(reference) for v in values):
            raise ValueError('Mixed task identity in protocol group: '+key)
        attempted = [v for v in values if v.get('status') == 'completed']
        invalid_reasons = {'initialization_error', 'environment_error', 'evaluator_error',
                           'policy_error', 'baseline_error', 'wall_timeout'}
        invalid = [v for v in attempted if v.get('error') or v.get('finish_reason') in invalid_reasons]
        invalid_indices = {v['test_protocol']['trial_index'] for v in invalid}
        done = [v for v in attempted if v['test_protocol']['trial_index'] not in invalid_indices]
        done_indices = {v['test_protocol']['trial_index'] for v in done}
        successes = sum(bool(v.get('metrics', {}).get('success')) for v in done)
        complete = done_indices == {1, 2, 3, 4}
        tasks[key] = dict(scenario=reference['scenario'], mode=reference['mode'], base_seed=reference['seed'],
                         operation_profile_requested=reference.get('operation_profile_requested'),
                         expected_trials=4, recorded_trials=len(values), attempted_trials=len(attempted),
                         completed_trials=len(done), invalid_trial_indices=sorted(invalid_indices),
                         missing_trial_indices=sorted({1, 2, 3, 4}-done_indices-invalid_indices), complete=complete,
                         status='complete' if complete else 'partial', observed_success_rate_lower_bound=successes/4,
                         observed_successes=successes, successes_out_of_four=successes if complete else None,
                         success_rate=successes/4 if complete else None,
                         all_four_success=bool(successes == 4) if complete else None)
    complete = [v for v in tasks.values() if v['complete']]
    rates = [v['success_rate'] for v in complete]
    return dict(version=PROTOCOL_VERSION, task_metadata_version=metadata_version,
                task_groups=len(tasks), complete_task_groups=len(complete),
                incomplete_task_groups=len(tasks)-len(complete),
                mean_success_rate_complete_tasks=sum(rates)/len(rates) if rates else None,
                all_four_success_tasks=sum(v['all_four_success'] for v in complete),
                all_four_success_rate_complete_tasks=sum(v['all_four_success'] for v in complete)/len(complete) if complete else None,
                missing_trials=sum(len(v['missing_trial_indices']) for v in tasks.values()),
                invalid_trials=sum(len(v['invalid_trial_indices']) for v in tasks.values()), by_task=tasks)
