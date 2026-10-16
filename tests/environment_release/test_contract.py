import copy
from pathlib import Path
import sys
import pytest
ROOT=Path(__file__).resolve().parents[2]
for name in ('agentbench','agentbench_platform','agentbench_sdk'):
    sys.path.insert(0,str(ROOT/'source'/name))
from agentbench_platform.profiles import RunProfile,CAPABILITY_VERSION,sanitize_snapshot,sanitize_description
from agentbench_platform.environment_catalog import catalog,digest
from agentbench_platform.environment_release import gate,matrix,source_files


def profile(level,**kwargs):
    return RunProfile(capability_level=level,capability_profile_version=CAPABILITY_VERSION,
        observation='privileged' if level==3 else 'rgb',**kwargs)


def test_inventory_contains_only_410_unique_environment_identities():
    data=catalog()
    assert data['count']==410==len({t['id'] for t in data['tasks']})
    assert sum(data['counts'].values())==410
    assert all('capability_levels' in t and 'difficulty' in t for t in data['tasks'])
    assert all('success_rate' not in t and 'completed' not in t for t in data['tasks'])
    assert len(matrix(data))>410*3


@pytest.mark.parametrize('level',range(4))
def test_all_levels_filter_unknown_and_private_fields(level):
    p=profile(level)
    raw=dict(step_index=0,simulation_time_s=0,terminated=False,truncated=False,
        secret_path='/private/scene',privileged=dict(pieces={'key':dict(position=[1,2,3],secret='hidden')}))
    public=sanitize_snapshot(raw,p)
    assert 'secret_path' not in public
    assert ('privileged' in public)==(level==3)
    if level==3:assert public['privileged']['pieces']['key']=={'position':[1,2,3]}


@pytest.mark.parametrize('level',range(3))
def test_privileged_profile_rejected_below_l3(level):
    with pytest.raises(ValueError):RunProfile('privileged',capability_level=level,capability_profile_version=CAPABILITY_VERSION)


def test_l0_code_is_not_a_gateway_tool_and_domain_tools_are_denied():
    assert profile(0).tools==()
    for name in ('pyroki','graspnet','cube_solver','unknown'):
        with pytest.raises(ValueError):profile(0,tools=(name,))
    with pytest.raises(ValueError):profile(1,tools=('graspnet',))
    assert profile(2,tools=('graspnet',)).tools==('graspnet',)
    assert profile(3).tools==()  # higher level does not grant installed tools
    with pytest.raises(ValueError):profile(3,tools=('unknown',))


def test_legacy_profile_is_not_silently_relabelled():
    assert 'capability_level' not in RunProfile().public_record()
    with pytest.raises(ValueError):RunProfile('rgb',capability_level=0)


def test_case_goal_projection_is_independent_and_public_intent_is_correct():
    from agentbench_platform.kongming_cases import trusted_case_spec,goal_reference_spec,describe_case_spec
    for case_id in ('A01','A06','A11','D01','D06','D11'):
        case=trusted_case_spec(case_id);old=copy.deepcopy(case)
        goal=goal_reference_spec(case)
        assert goal['initial']==case['goal_state'] and case==old
        goal['initial']['key'][0][0]+=1
        assert case==old
        desc=describe_case_spec(case)
        assert 'initial' not in desc and 'goal_state' not in desc
        if case['subtask']!='complete':assert 'all other pieces' in desc['description']


def test_hanoi_observer_infers_motion_without_client_move_claims():
    from agentbench_hanoi40.catalog import BY_ID
    from agentbench_hanoi40.isaac_cfg import sample
    from agentbench_hanoi40.rules import ObservedMonitor,RuleFailure
    task=BY_ID['H01'];m=ObservedMonitor(task,sample(task.id))
    pos=[m.expected(i) for i in range(5)]
    for ring, (src, dst) in enumerate(zip(task.start, task.goal)):
        if src == dst: continue
        pos[ring]=(pos[ring][0],pos[ring][1],pos[ring][2]+.1)
        m.observe(pos,dt=1/120)
        state=list(m.state);state[ring]=dst
        pos[ring]=m.expected(ring,state)
        m.observe(pos,dt=1/120)
    assert not m.result(pos)['task_success']
    for _ in range(120):m.observe(pos,dt=1/120)
    assert m.result(pos)['task_success']
    with pytest.raises(RuleFailure):m.observe(pos,depth=.006,dt=1/120)
    assert not m.result(pos)['task_success']


def test_release_gate_rejects_absent_stale_skipped_and_zero_step_evidence():
    data=catalog();files={'source.py':{'sha256':'a','bytes':1}}
    assert not gate(data,files,{})['release_ready']
    evidence=dict(source_digest=digest(files),catalog_digest=digest(data),capability_profile_version=CAPABILITY_VERSION)
    assert not gate(data,files,evidence)['release_ready']
    required=matrix(data)[0]
    evidence['cases']=[dict(key=required['key'],checks={k:'skipped' for k in required['checks']},physics_steps=0)]
    report=gate(data,files,evidence)
    assert not report['release_ready']
    assert any(isinstance(r,dict) and r['task_id']==required['task_id'] for r in report['missing'])


def test_allowlist_excludes_history_models_and_controllers():
    files=[str(p) for p in source_files()]
    assert files
    assert not any('/__pycache__/' in p or p.startswith(('outputs/','docs/','baselines/')) for p in files)
    assert not any(Path(p).name in ('controller.py','model_proxy.py','baseline.py') for p in files)
    assert all(not p.endswith(('.mp4','.pdf','.zip')) for p in files)
    assert not any(Path(p).name in ('rubiks_cube_route.py','rubiks_cube_solver.py',
        'rubiks_cube_sharpa_executor.py','rubiks_cube_sharpa_trajectory.py') for p in files)


def test_public_content_links_and_projection_dependencies_are_closed():
    import json
    from agentbench_platform.public_content import audit
    report=audit()
    assert not report['issues'],report['issues']
    projection=json.loads((ROOT/'source/agentbench_platform/agentbench_platform/action_contracts.json').read_text())
    assert set(projection['sources']) <= set(report['files'])
    assert 'docs/kongming_dual_sharpa_v1.md' not in report['files']


def test_candidate_export_cannot_bypass_missing_evidence(tmp_path):
    from agentbench_platform.environment_release import build
    with pytest.raises(ValueError):build(tmp_path/'candidate',candidate=True)
    assert not (tmp_path/'candidate').exists()


def test_export_removes_shot_suggestions_without_changing_physical_arguments():
    import ast
    from agentbench_platform.environment_release import export_content
    source=b'''"""Old rollout notes."""\nx=dict(targets=[[1,2,3]],plan=[[40,.2]],yaw_plan=[10.],reference="old",obstacles=[dict(mass=.4)])\n'''
    original={};exported={}
    exec(compile(ast.parse(source),'original','exec'),original)
    payload=export_content('source/agentbench/agentbench_mujoco/campaign_scene.py',source)
    exec(compile(ast.parse(payload),'exported','exec'),exported)
    assert exported['x']=={k:v for k,v in original['x'].items() if k not in {'plan','yaw_plan','reference'}}
    assert b'Old rollout' not in payload
    assert export_content('source/other.py',source)==source


def test_full_horizon_gate_rejects_short_probe_even_when_all_labels_say_passed():
    from agentbench_platform.environment_release import CHECKS,GLOBAL_CHECKS
    task=next(t for t in catalog()['tasks'] if t['case_id']=='A024')
    manifest=dict(count=1,tasks=[task]);files={}
    evidence=dict(source_digest=digest(files),catalog_digest=digest(manifest),
        capability_profile_version=CAPABILITY_VERSION,global_checks={k:'passed' for k in GLOBAL_CHECKS},
        cases=[dict(key=r['key'],checks={k:'passed' for k in CHECKS},physics_steps=5000,
            settle_seconds=2,hold_seconds=3,runtime={'mujoco':'fixture'},no_operation_seconds=5)
            for r in matrix(manifest)])
    assert not gate(manifest,files,evidence)['release_ready']
    assert any(str(r).startswith('missing_full_horizon_stability:') for r in gate(manifest,files,evidence)['missing'])


def test_explicit_profile_cli_never_loads_model_runner():
    import subprocess
    result=subprocess.run([sys.executable,'-c',
        'import sys; from agentbench_platform.profile_cli import frozen_profile; '
        'assert "agentbench_platform.runner" not in sys.modules; '
        'assert frozen_profile("rgb",capability_level=0)["tools"]==[]'],
        env={**__import__('os').environ,'PYTHONPATH':str(ROOT/'source/agentbench_platform')},capture_output=True,text=True)
    assert result.returncode==0,result.stderr
