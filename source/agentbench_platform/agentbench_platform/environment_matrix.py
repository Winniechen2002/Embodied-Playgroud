"""One maintainer schedule for legacy, protocol and union qualification.

Identity includes the reset seed, every effective perturbation and time budget.
Membership is provenance, not identity: overlapping four-trial groups share a
physical execution without losing any of their planned slots.
"""
from .environment_catalog import ROOT, digest, source_module
from .evaluation_protocol import budgets, trial_plan, VERSION as PROTOCOL_VERSION

VERSION = 'environment-conditions-v3'
BASE_SEEDS = (0, 1, 2)


def effective_condition(task, *, seed=0, split='nominal', initial_mode='loaded', parameters=None):
    if type(seed) is not int or seed < 0:
        raise ValueError('Invalid reset seed')
    family = task['family']
    if split not in ('nominal', 'train', 'heldout'):
        raise ValueError('Unknown split')
    if family == 'marble':
        if initial_mode not in ('loaded', 'ground') or split != 'nominal':
            raise ValueError('Invalid bird condition')
        actual = dict(spring_stiffness=22., launcher_offset_m=[0., 0., 0.],
            ammunition_offset_m=[0., 0., 0.], background='park', background_motion='static')
        if parameters:
            if set(parameters) - set(actual):
                raise ValueError('Unknown bird parameter')
            actual.update(parameters)
        actual['spring_stiffness'] = float(actual['spring_stiffness'])
        for name in ('launcher_offset_m', 'ammunition_offset_m'):
            actual[name] = [float(x) for x in actual[name]]
    elif family.startswith('hanoi_') or family == 'pocket_cube':
        folder = 'agentbench_hanoi40' if family.startswith('hanoi_') else 'agentbench_cube20'
        module = 'isaac_cfg' if family.startswith('hanoi_') else 'catalog'
        sampler = source_module('_matrix_' + folder, ROOT/'source/agentbench'/folder, module)
        actual = sampler.sample(task['case_id'], seed, split)
        if parameters is not None and digest(parameters) != digest(actual):
            raise ValueError('Parameters differ from native reset sampler')
    elif family.startswith('maniskill_'):
        actual=dict(authored_light_scale=1.,physics_variant=0)
        if parameters:
            if set(parameters)!=set(actual):raise ValueError('Unknown ManiSkill parameter')
            actual.update(parameters)
        allowed=task['randomization']['engineering_physics_variants']
        if type(actual['physics_variant']) is not int or actual['physics_variant'] not in allowed:
            raise ValueError('Unknown physical variant')
        if actual['authored_light_scale'] not in (.85,.95,1.,1.05,1.15):raise ValueError('Unknown light scale')
    elif family == 'bookshelf':
        actual = dict(native_layout_seed=seed)
    elif family in ('rubiks_panda', 'rubiks_sharpa', 'kongming_lock'):
        actual = dict(authored_sky_light_scale=1.)
        if parameters:
            if set(parameters) != set(actual):
                raise ValueError('Unknown fixed-case parameter')
            actual.update(parameters)
    else:
        raise ValueError('Unknown environment family')
    if family not in ('marble', 'pocket_cube') and not family.startswith('hanoi_') and split != 'nominal':
        raise ValueError('Family has no physical split randomization')
    if family != 'marble' and parameters is not None and digest(parameters) != digest(actual):
        raise ValueError('Invalid effective parameters')
    result = dict(seed=seed, split=split, environment_parameters=actual, budgets=budgets(task))
    if family == 'marble':
        result['initial_mode'] = initial_mode
    return result


def legacy_conditions(task):
    family = task['family']
    if family.startswith('maniskill_'):
        for variant in task['randomization']['engineering_physics_variants']:
            for seed in BASE_SEEDS:
                yield effective_condition(task,seed=seed,parameters=dict(authored_light_scale=1.,physics_variant=variant))
        return
    if family == 'marble':
        for seed in BASE_SEEDS:
            for mode in ('loaded', 'ground'):
                for spring in (22., 24., 26., 28.):
                    yield effective_condition(task, seed=seed, initial_mode=mode,
                        parameters=dict(spring_stiffness=spring))
        return
    splits = ('nominal', 'train', 'heldout') if family.startswith('hanoi_') or family == 'pocket_cube' else ('nominal',)
    for split in splits:
        seeds = range(5) if family.startswith('hanoi_') and split != 'nominal' else range(4) if family == 'bookshelf' else BASE_SEEDS
        for seed in seeds:
            yield effective_condition(task, seed=seed, split=split)


def matrix(manifest, selection='union'):
    if selection not in ('legacy', 'protocol', 'union'):
        raise ValueError('Unknown matrix selection')
    from .environment_release import CHECKS
    rows = {}
    def add(task, condition, member):
        key = digest([VERSION, task['id'], task['configuration_sha256'], condition])
        if key not in rows:
            rows[key] = dict(key=key, task_id=task['id'], condition=condition,
                configuration_sha256=task['configuration_sha256'], memberships=[], checks=list(CHECKS),
                settle_seconds=2., hold_seconds=3.,
                physics_acceptance=task.get('physics_acceptance','static_stability'),
                full_horizon_stability=task.get('full_horizon_stability', False),
                episode_time_limit_seconds=condition['budgets']['simulation_seconds'])
        rows[key]['memberships'].append(member)
    for task in manifest['tasks']:
        if selection in ('legacy', 'union'):
            for condition in legacy_conditions(task):
                add(task, condition, dict(suite='legacy'))
        if selection in ('protocol', 'union'):
            for seed in BASE_SEEDS:
                for mode in (('loaded', 'ground') if task['family']=='marble' else ('loaded',)):
                    for trial in trial_plan(task, seed, initial_mode=mode):
                        condition = effective_condition(task, seed=trial['reset_seed'], split=trial['split'],
                            initial_mode=mode, parameters=trial['environment_parameters'])
                        add(task, condition, dict(suite='protocol', version=PROTOCOL_VERSION,
                            base_seed=seed, variant=mode if task['family']=='marble' else 'default',
                            trial_index=trial['trial_index']))
        if selection in ('legacy','union') and task['family']=='maniskill_dynamics':
            for variant in (1,2):
                for seed in BASE_SEEDS:
                    for scale in (.85,.95,1.05,1.15):
                        condition=effective_condition(task,seed=seed,parameters=dict(authored_light_scale=scale,physics_variant=variant))
                        add(task,condition,dict(suite='additional_physics',physics_variant=variant,base_seed=seed))
    return list(rows.values())


def schedule(manifest, selection='union'):
    rows = matrix(manifest, selection)
    return dict(version=VERSION, selection=selection, base_seeds=list(BASE_SEEDS),
        unique_conditions=len(rows), planned_memberships=sum(len(r['memberships']) for r in rows),
        digest=digest(rows), conditions=rows)
