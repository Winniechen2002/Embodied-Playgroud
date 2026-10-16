import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import sys
import pytest
ROOT=Path(__file__).resolve().parents[2]
for name in ('agentbench','agentbench_platform','agentbench_sdk'):
    sys.path.insert(0,str(ROOT/'source'/name))
from agentbench_platform.environment_catalog import catalog,find_task
from agentbench_platform.evaluation_protocol import (manifest,trial_plan,select_trial,budgets,
    summarize_group,apply_visual_trial,LIGHT_SCALES)


def load_script(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def test_every_task_has_four_frozen_trials_and_correct_total():
    data=manifest()
    assert (data['task_count'],data['group_count'],data['planned_episodes'])==(410,510,2040)
    assert len({t['task_id'] for t in data['tasks']})==410
    for task in data['tasks']:
        b=task['budgets']
        assert b['max_steps']==b['simulation_seconds']*b['control_hz']
        for group in task['groups']:
            assert [t['trial_index'] for t in group['trials']]==[1,2,3,4]
            assert len({json.dumps(t['environment_parameters'],sort_keys=True) for t in group['trials']})==4
    assert data==manifest()  # no global RNG or invocation-order dependence


def test_birds_keep_the_original_complete_mapping_in_both_modes():
    sys.path.insert(0,str(ROOT/'scripts'))
    from franka_marble_test_protocol import protocol_trials
    for task in catalog()['tasks'][:100]:
        for mode in ('loaded','ground'):
            rows=trial_plan(task,7,initial_mode=mode)
            assert [r['legacy_protocol'] for r in rows]==protocol_trials(task['scenario'],7)
            assert all(r['reset_seed']==7 for r in rows)
            assert [r['environment_parameters'] for r in rows]==[r['environment_parameters'] for r in protocol_trials(task['scenario'],7)]


def test_native_sampler_parameters_are_the_actual_runtime_projection():
    from agentbench_hanoi40.isaac_cfg import sample as hanoi
    from agentbench_cube20.catalog import sample as cube
    for task in catalog()['tasks']:
        if task['family'].startswith('hanoi_') or task['family']=='pocket_cube':
            sampler=hanoi if task['family'].startswith('hanoi_') else cube
            for k,row in enumerate(trial_plan(task,11)):
                assert row['reset_seed']==11+k
                assert row['split']=='train'
                assert row['environment_parameters']==sampler(task['case_id'],11+k,'train')


def test_fixed_cases_change_only_visual_intensity_not_task_geometry():
    cfg=SimpleNamespace(scene=SimpleNamespace(sky_light=SimpleNamespace(spawn=SimpleNamespace(intensity=900)),physics=object()))
    physics=cfg.scene.physics
    for scale in LIGHT_SCALES:
        cfg.scene.sky_light.spawn.intensity=900
        apply_visual_trial(cfg,scale)
        assert cfg.scene.sky_light.spawn.intensity==900*scale
        assert cfg.scene.physics is physics
    with pytest.raises(ValueError):apply_visual_trial(cfg,2.)
    for task in catalog()['tasks']:
        if task['family'].startswith('rubiks_') or task['family']=='kongming_lock':
            rows=trial_plan(task,13)
            assert all(r['reset_seed']==13 for r in rows)
            assert [r['environment_parameters'] for r in rows]==[{'authored_sky_light_scale':s} for s in LIGHT_SCALES]


@pytest.mark.parametrize('base',[-1,True,2**31-3,1.5])
def test_seed_validation(base):
    with pytest.raises(ValueError):trial_plan(find_task('marble/dual-panda/A001'),base)


def test_invalid_missing_failure_are_never_dropped_or_retried():
    summary=summarize_group([{'trial_index':1,'outcome':'success'},{'trial_index':2,'outcome':'invalid'}])
    assert summary['success_rate'] is None and summary['all_four_success'] is None
    assert summary['observed_success_rate_lower_bound']==.25
    assert summary['invalid_trial_indices']==[2] and summary['missing_trial_indices']==[3,4]
    summary=summarize_group([{'trial_index':i,'outcome':'success' if i==1 else 'failure'} for i in range(1,5)])
    assert summary['status']=='complete' and summary['success_rate']==.25 and not summary['all_four_success']
    with pytest.raises(ValueError):summarize_group([{'trial_index':1,'outcome':'failure'},{'trial_index':1,'outcome':'success'}])


def test_registered_native_launch_forwards_exact_private_trial_and_limits(monkeypatch,tmp_path):
    runtime=load_script('environment_runtime')
    captured=[]
    class Dispatched(Exception):pass
    def execute(executable,command):
        captured.extend(command);raise Dispatched
    monkeypatch.setattr(runtime.os,'execv',execute)
    monkeypatch.setenv('AGENTBENCH_EPISODE_CHILD','1')
    with pytest.raises(Dispatched):
        runtime.main(['--task-id','rubiks_sharpa/floating-sharpa/C01','--capability-level','0',
            '--seed','5','--evaluation-protocol','environment-four-trial-v1','--trial-index','3','--output',str(tmp_path/'new')])
    for key,value in {'--evaluation-light-scale':'1.05','--evaluation-base-seed':'5',
        '--evaluation-trial-index':'3','--environment-seed':'5','--max-steps':'109800','--wall-seconds':'19800'}.items():
        assert captured[captured.index(key)+1]==value
    assert not (tmp_path/'new').exists()


@pytest.mark.parametrize('extra',[['--split','train'],['--max-steps=2'],['--wall-seconds','1'],['--spring-stiffness','24']])
def test_registered_trials_reject_hidden_configuration_overrides(extra,tmp_path):
    runtime=load_script('environment_runtime')
    with pytest.raises(SystemExit):
        runtime.main(['--task-id','marble/dual-panda/A001','--capability-level','0',
            '--evaluation-protocol','environment-four-trial-v1','--trial-index','1','--output',str(tmp_path/'new')]+extra)
    assert not (tmp_path/'new').exists()


def test_bird_backend_receives_all_protocol_parameters_and_public_spring(monkeypatch):
    import agentbench_mujoco.campaign_env as campaign
    from agentbench_platform.environment_backend import MarbleBackend
    captured={}
    class Env:
        physics_dt=.001;decimation=20;max_seconds=150
        def __init__(self,**kw):captured.update(kw)
        def reset(self,seed):captured['seed']=seed
        def _after_physics(self):pass
    monkeypatch.setattr(campaign,'FrankaCampaignEnv',Env)
    task=find_task('marble/dual-panda/A001');row=select_trial(task,9,4)
    MarbleBackend(task,seed=row['reset_seed'],environment_parameters=row['environment_parameters'])
    assert all(captured[k]==v for k,v in row['environment_parameters'].items())
    assert captured['seed']==9


def test_generated_bilingual_conditions_and_hashes_are_current():
    exporter=load_script('export_evaluation_protocol')
    for name,expected in exporter.artifacts().items():
        assert (ROOT/'docs/evaluation'/name).read_text()==expected,name


def test_registered_native_options_cannot_mislabel_reset_only_or_short_budget():
    runtime=load_script('agentbench_platform_runtime')
    class Launcher:
        @staticmethod
        def add_app_launcher_args(parser):parser.add_argument('--device')
    base=['--output','/tmp/protocol-parse-only','--task-family','rubiks_cube','--mode','solve',
          '--case-id','C01','--environment-seed','0','--evaluation-base-seed','0',
          '--evaluation-trial-index','2','--evaluation-light-scale','.95']
    args=runtime.parse_runtime_args(Launcher,base)
    assert args.max_steps==109800 and args.evaluation_light_scale==.95
    for extra in (['--max-steps','1'],['--case-reset-only'],['--goal-reference'],['--wall-seconds','10']):
        with pytest.raises(SystemExit):runtime.parse_runtime_args(Launcher,base+extra)
