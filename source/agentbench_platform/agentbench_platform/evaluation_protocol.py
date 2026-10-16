"""Maintainer-owned, deterministic four-episode plans. No model or simulator imports.

The birds retain their original four-trial-v1 mapping. Other families reuse
native reset samplers or declared visual perturbations; no goal is resampled.
"""
from copy import deepcopy
import json
from .environment_catalog import ROOT, catalog, source_module

VERSION = 'environment-four-trial-v2'
LEGACY_VERSION = 'environment-four-trial-v1'
TRIALS = 4
LIGHT_SCALES = (.85, .95, 1.05, 1.15)


def trial_plan(task, base_seed=0, *, initial_mode='loaded'):
    if type(base_seed) is not int or not 0 <= base_seed <= 2**31-4:
        raise ValueError('base_seed must be an integer in 0..2147483644')
    if initial_mode not in ('loaded', 'ground'):
        raise ValueError('Unknown initial mode')
    family = task['family']
    if family != 'marble' and initial_mode != 'loaded':
        raise ValueError('Initial mode applies only to marble')
    rows = []
    birds = None
    if family == 'marble':
        from .marble_protocol import protocol_trials
        birds = protocol_trials(task['scenario'], base_seed)
    for k in range(TRIALS):
        seed = base_seed if family.startswith('maniskill_') or family in ('marble','rubiks_panda','rubiks_sharpa','kongming_lock') else base_seed+k
        row = dict(trial_index=k+1, reset_seed=seed, split='nominal', environment_parameters={})
        if birds:
            row.update(legacy_protocol=birds[k], initial_mode=initial_mode,
                       environment_parameters=deepcopy(birds[k]['environment_parameters']))
        elif family.startswith('hanoi_'):
            sampler = source_module('_evaluation_hanoi', ROOT/'source/agentbench/agentbench_hanoi40', 'isaac_cfg')
            row.update(split='train', environment_parameters=sampler.sample(task['case_id'],seed,'train'))
        elif family == 'pocket_cube':
            sampler = source_module('_evaluation_cube', ROOT/'source/agentbench/agentbench_cube20', 'catalog')
            row.update(split='train', environment_parameters=sampler.sample(task['case_id'],seed,'train'))
        elif family == 'bookshelf':
            row['environment_parameters'] = dict(native_layout_seed=seed)
        elif family.startswith('maniskill_'):
            row['environment_parameters'] = dict(authored_light_scale=LIGHT_SCALES[k],physics_variant=0)
        elif family in ('rubiks_panda','rubiks_sharpa','kongming_lock'):
            row['environment_parameters'] = dict(authored_sky_light_scale=LIGHT_SCALES[k])
        else:
            raise ValueError('No registered evaluation mapping for '+family)
        rows.append(row)
    return rows


def budgets(task):
    family=task['family']
    if family.startswith('maniskill_'):
        seconds=300 if family=='maniskill_long_horizon' else 120
        return dict(control_hz=20,physics_hz=240,simulation_seconds=seconds,max_steps=seconds*20,wall_seconds=3600)
    hz=50 if family=='marble' else 60 if family=='pocket_cube' else 30
    seconds=150 if family=='marble' else 3660 if family.startswith('rubiks_') else 1200 if family=='kongming_lock' else 300 if family=='pocket_cube' else 600
    if family=='bookshelf':
        books=json.loads((ROOT/'source/agentbench_platform/agentbench_platform/bookshelf_catalog.json').read_text())
        record=next(v['record'] for v in books['variants'] if v['id']==task['case_id'])
        seconds=record['episode_length_s']
    return dict(control_hz=hz, physics_hz=1000 if family=='marble' else 240 if family=='pocket_cube' else 120,
                simulation_seconds=seconds, max_steps=round(seconds*hz),
                wall_seconds=600 if family=='marble' else 19800 if family.startswith('rubiks_') else 3600)


def task_protocol(task, base_seed=0):
    modes=('loaded','ground') if task['family']=='marble' else ('loaded',)
    return dict(task_id=task['id'], version=VERSION, expected_trials_per_group=TRIALS,
        configuration_sha256=task['configuration_sha256'], goal=deepcopy(task['goal']),
        authoring_source=task['authoring_source'], action_size=task['action_spec']['size'],
        budgets=budgets(task),contract=deepcopy(task['contract']),
        groups=[dict(variant=mode if task['family']=='marble' else 'default', base_seed=base_seed,
                     trials=trial_plan(task,base_seed,initial_mode=mode)) for mode in modes])


def manifest(base_seed=0):
    rows=[task_protocol(t,base_seed) for t in catalog()['tasks']]
    return dict(version=VERSION,base_seed=base_seed,task_count=len(rows),
                group_count=sum(len(t['groups']) for t in rows),
                planned_episodes=sum(len(t['groups'])*TRIALS for t in rows),tasks=rows)


def select_trial(task, base_seed, trial_index, *, initial_mode='loaded'):
    if type(trial_index) is not int or trial_index not in range(1,5):
        raise ValueError('trial_index must be 1..4')
    return trial_plan(task,base_seed,initial_mode=initial_mode)[trial_index-1]


def summarize_group(records):
    """Four fixed slots, no dropping errors/missing trials and no best-of-four."""
    by_index={}
    for row in records:
        index=row['trial_index']
        if type(index) is not int or index not in range(1,5) or index in by_index:
            raise ValueError('Invalid or duplicate trial index')
        if row['outcome'] not in ('success','failure','invalid','missing'):
            raise ValueError('Unknown outcome')
        by_index[index]=row['outcome']
    invalid=[i for i in range(1,5) if by_index.get(i)=='invalid']
    missing=[i for i in range(1,5) if by_index.get(i,'missing')=='missing']
    successes=sum(value=='success' for value in by_index.values())
    complete=not invalid and not missing
    return dict(expected_trials=4,status='complete' if complete else 'partial',
        invalid_trial_indices=invalid,missing_trial_indices=missing,
        observed_successes=successes,observed_success_rate_lower_bound=successes/4,
        success_rate=successes/4 if complete else None,
        all_four_success=successes==4 if complete else None)


def apply_visual_trial(cfg, scale):
    """Initialization only. Visual light intensity never changes physical state."""
    if scale is None:
        return
    if type(scale) not in (float,int) or scale not in LIGHT_SCALES:
        raise ValueError('Unregistered evaluation light scale')
    cfg.scene.sky_light.spawn.intensity *= scale
