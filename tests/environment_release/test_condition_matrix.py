import copy
from collections import Counter
from agentbench_platform.environment_catalog import catalog, digest
from agentbench_platform.environment_matrix import matrix, schedule
from agentbench_platform.environment_release import CHECKS, GLOBAL_CHECKS, evidence_identity, gate


def test_union_preserves_every_legacy_and_protocol_membership():
    data=catalog()
    old=schedule(data,'legacy'); protocol=schedule(data,'protocol'); union=schedule(data)
    assert (old['unique_conditions'],old['planned_memberships'])==(4970,4970)
    assert (protocol['unique_conditions'],protocol['planned_memberships'])==(5160,6120)
    assert (union['unique_conditions'],union['planned_memberships'])==(9390,11090)
    assert {r['key'] for r in union['conditions']}=={r['key'] for r in old['conditions']}|{r['key'] for r in protocol['conditions']}
    slots=Counter((r['task_id'],m['base_seed'],m['variant']) for r in union['conditions']
        for m in r['memberships'] if m['suite']=='protocol')
    assert len(slots)==1530 and set(slots.values())=={4}
    assert all(r['episode_time_limit_seconds']==r['condition']['budgets']['simulation_seconds'] for r in union['conditions'])


def test_visual_and_offset_conditions_do_not_collapse_into_legacy_rows():
    rows=matrix(catalog())
    assert all(len(r['condition']['environment_parameters'])==5 for r in rows if r['task_id'].startswith('marble/'))
    for row in rows:
        if row['task_id'].startswith(('rubiks_','kongming_')):
            assert set(row['condition']['environment_parameters'])=={'authored_sky_light_scale'}
    assert len({digest(r['condition']) for r in rows if r['task_id']=='marble/dual-panda/A001'})==48


def evidence_fixture():
    task=next(t for t in catalog()['tasks'] if t['id']=='marble/dual-panda/A001')
    manifest=dict(count=1,tasks=[task]);identity=evidence_identity(manifest,{})
    rows=[]
    for required in matrix(manifest):
        seconds=required['episode_time_limit_seconds'] if required['full_horizon_stability'] else 5
        rows.append(dict(required,status='passed',versions=identity,
            actual_initialization=copy.deepcopy(required['condition']),
            checks={k:'passed' for k in CHECKS},measurements={k:{'fixture':True} for k in CHECKS},
            physics_steps=round(seconds*1000),settle_seconds=2,hold_seconds=seconds-2,
            no_operation_seconds=seconds,runtime={'mujoco':'test-fixture'}))
    return manifest,dict(**identity,cases=rows,global_checks={k:'passed' for k in GLOBAL_CHECKS},
        global_measurements={k:dict(versions=identity,fixture=True) for k in GLOBAL_CHECKS})


def test_gate_requires_current_complete_measurements_and_retains_package_state():
    manifest,evidence=evidence_fixture()
    assert gate(manifest,{},evidence)['source_release_ready']
    assert gate(manifest,{},evidence)['distribution_validation']=='not_executed'
    for mutate in (
        lambda e:e['cases'].append(copy.deepcopy(e['cases'][0])),
        lambda e:e['cases'][0].update(key='unknown'),
        lambda e:e['cases'][0]['versions'].update(source_digest='stale'),
        lambda e:e['cases'][0]['actual_initialization'].update(seed=99),
        lambda e:e['cases'][0].update(measurements={}),
        lambda e:e['cases'][0].update(hold_seconds=float('nan')),
        lambda e:e['cases'][0].update(physics_steps=True),
        lambda e:e['global_measurements'].clear(),
        lambda e:e['global_measurements']['local_contact'].pop('fixture'),
    ):
        broken=copy.deepcopy(evidence);mutate(broken)
        assert not gate(manifest,{},broken)['source_release_ready']


def test_local_contact_is_an_environment_gate():
    manifest,evidence=evidence_fixture()
    evidence['global_checks']['local_contact']='not_executed'
    assert not gate(manifest,{},evidence)['environment_qualified']
