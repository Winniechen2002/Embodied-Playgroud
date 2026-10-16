"""Physical history and protocol isolation; no model or solver execution."""
import copy
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'env/maniskill_lgd'))
from agentbench_maniskill import specification
from agentbench_maniskill.common.evaluation import lighting_parameters
from agentbench_maniskill.geometry_dynamics.oracle import TaskOracle


def fixture(code='P3'):
    _,task=specification(code)
    n=int(code[1:])+(10 if code.startswith('D') else 0)
    root=ROOT/'env/maniskill_lgd/agentbench_maniskill/evidence/geometry_dynamics'/f'{n:02}'
    return task,json.loads((root/'initial_state.json').read_text()),json.loads((root/'goal_fixture_state.json').read_text())


def test_substep_force_peak_is_latched_after_state_recovers():
    task,initial,goal=fixture();o=TaskOracle(task,initial)
    rule=next(r for r in task['history_rules'] if r['type']=='force_limit')
    bad=copy.deepcopy(initial)
    bad['objects'][rule['object']].setdefault('contact_forces',{})[rule['support']]=rule['max_force']*2
    o.audit(bad,physics_step=3,simulation_time=3/240)
    o.done={m['id'] for m in task['milestones']}
    for _ in range(30):o.advance(goal)
    assert rule['name'] in o.violations and not o.assess(goal)['success']
    assert o.first_violation==dict(reason=rule['name'],physics_step=3,simulation_time_s=3/240)


def test_physics_audit_never_completes_control_dwell():
    task,initial,goal=fixture('P1');o=TaskOracle(task,initial)
    o.done={m['id'] for m in task['milestones']}
    for i in range(240):o.audit(goal,physics_step=i+1,simulation_time=(i+1)/240)
    assert o.dwell==0 and o.steps==0 and not o.assess(goal)['success']
    for _ in range(19):o.advance(goal)
    assert not o.assess(goal)['success']
    assert o.advance(goal)['success']


def test_transient_motion_restarts_continuous_stability():
    task,initial,goal=fixture('P1');o=TaskOracle(task,initial);o.done={m['id'] for m in task['milestones']}
    for _ in range(19):o.advance(goal)
    moving=copy.deepcopy(goal);next(iter(moving['objects'].values()))['v']=[1,0,0]
    o.audit(moving,physics_step=239,simulation_time=239/240)
    assert o.dwell==0 and not o.advance(goal)['success']
    assert o.dwell==0, 'The partially stable control interval cannot earn a full dwell tick'
    for _ in range(19):assert not o.advance(goal)['success']
    assert o.advance(goal)['success']


def test_repaired_book_shelf_has_real_vertical_clearance():
    _,task=specification('P7')
    shelf=next(s for s in task['furniture'] if s['name']=='bookshelf')
    bottom,_,top=shelf['shapes']
    clearance=top['p'][2]-top['half'][2]-(bottom['p'][2]+bottom['half'][2])
    for o in task['objects']:
        assert 2*max(s['half'][2] for s in o['shapes'])+o['initial']['gap']<clearance


def test_light_scaling_changes_only_colors():
    base=lighting_parameters(1.)
    for scale in (.85,.95,1.05,1.15):
        actual=lighting_parameters(scale)
        assert actual['ambient']==[v*scale for v in base['ambient']]
        assert actual['directional']==[[v*scale for v in color] for color in base['directional']]
    with pytest.raises(ValueError):lighting_parameters(float('nan'))


def test_complete_schedule_preserves_old_cases_and_default_only_formal_physics():
    from agentbench_platform.environment_catalog import catalog
    from agentbench_platform.environment_matrix import schedule
    m=catalog(_native_records={});s=schedule(m)
    assert m['count']==410 and len({t['id'] for t in m['tasks']})==410
    assert (s['unique_conditions'],s['planned_memberships'])==(9390,11090)
    slots=0;extra=0;old=0
    for row in s['conditions']:
        for member in row['memberships']:
            if member['suite']=='protocol':
                slots+=1
                if row['task_id'].startswith('maniskill_'):assert row['condition']['environment_parameters']['physics_variant']==0
            if member['suite']=='additional_physics':extra+=1
            if member['suite']=='legacy' and not row['task_id'].startswith('maniskill_') and '/dual-floating-sharpa/' not in row['task_id']:old+=1
    assert slots==6120 and extra==240 and old==4490


def test_dual_sharpa_constructor_applies_private_parameters_before_make(monkeypatch):
    # Execute the real shared constructor against minimal native-module doubles.
    import types
    from agentbench_platform.native_environment import create_dual_sharpa_environment
    cfg=types.SimpleNamespace(scene=types.SimpleNamespace(sky_light=types.SimpleNamespace(spawn=types.SimpleNamespace(intensity=1000.))))
    observed={}
    modules={
        'gymnasium':types.SimpleNamespace(make=lambda task,**kw: observed.update(seed=kw['cfg'].seed,intensity=kw['cfg'].scene.sky_light.spawn.intensity) or types.SimpleNamespace(unwrapped=object())),
        'isaaclab_tasks':types.ModuleType('isaaclab_tasks'),
        'agentbench':types.ModuleType('agentbench'),
        'agentbench.tasks':types.ModuleType('agentbench.tasks'),
        'agentbench.tasks.utils':types.SimpleNamespace(parse_env_cfg=lambda *a,**k:cfg),
        'agentbench_platform.native_cameras':types.SimpleNamespace(add_cameras=lambda *a,**k:None,add_target_outlines=lambda *a,**k:None,NativeCameras=lambda *a,**k:object()),
        'agentbench_platform.native_state':types.SimpleNamespace(scorer_spec=lambda *a,**k:{}),
    }
    prefix='agentbench.tasks.manager_based.table_top_manipulation.config.kongming_lock.'
    modules[prefix+'shapes']=types.SimpleNamespace(CANONICAL_SPEC={},collision_boxes={},TABLE_TOP_Z=.5)
    modules[prefix+'sharpa_calibration']=types.SimpleNamespace(PRESET_SHA256='fixture')
    modules[prefix+'kongming_sharpa_benchmark']=types.SimpleNamespace(KongmingDualSharpaState=lambda *a,**k:types.SimpleNamespace(physical_arrays=lambda:[]),VIEWS={})
    for name,module in modules.items():monkeypatch.setitem(sys.modules,name,module)
    args=types.SimpleNamespace(mode='assemble',goal_reference=False,device='cuda:0',case_reset_only=True,
        environment_seed=7,evaluation_light_scale=.85,case_id='A01',case_spec=dict(state_hash='a',manifest_sha256='b'))
    create_dual_sharpa_environment(args,object())
    assert observed==dict(seed=7,intensity=850.)


def test_continuous_action_bounds_preserve_finite_targets_without_invented_limits(tmp_path):
    from agentbench_platform.protocol import ProtocolService
    from agentbench_platform.profiles import RunProfile,CAPABILITY_VERSION
    class Backend:
        def describe(self):return dict(task={},robots={},cameras={},goal={},action_spec=dict(size=2,low=[None,-1.],high=[None,1.]))
        def snapshot(self,camera_ids=()):return dict(step_index=0,simulation_time_s=0.,terminated=False,truncated=False)
    service=ProtocolService(Backend(),token='test',profile=RunProfile(observation='rgb',capability_level=0,capability_profile_version=CAPABILITY_VERSION),journal_path=tmp_path/'requests.sqlite')
    try:
        assert service._description['action_spec']['low']==[None,-1.]
        service._action([100.,0.])
        for bad in ([float('inf'),0.],[float('nan'),0.],[True,0.],[0.,2.]):
            with pytest.raises(Exception):service._action(bad)
    finally:service.close()
