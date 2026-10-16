"""Resolve one concrete task configuration for native source-release checks."""
from .environment_catalog import ROOT, digest, source_module
from .evaluation_protocol import budgets

VERSION = 'source-default-conditions-v1'


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
        sampler = source_module('_condition_' + folder, ROOT/'source/agentbench'/folder, module)
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



def condition_case(task, **parameters):
    condition=effective_condition(task,**parameters)
    return dict(task_id=task['id'],condition=condition,
        key=digest([VERSION,task['id'],task['configuration_sha256'],condition]),
        configuration_sha256=task['configuration_sha256'],
        physics_acceptance=task.get('physics_acceptance','static_stability'),
        full_horizon_stability=task.get('full_horizon_stability',False),
        episode_time_limit_seconds=condition['budgets']['simulation_seconds'])
