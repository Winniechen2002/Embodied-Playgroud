import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('environment_status',ROOT/'scripts/environment_status.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


def test_stale_probe_is_visible_but_never_qualifies(tmp_path):
    path=tmp_path/'old.json'
    path.write_text(json.dumps(dict(source_digest='old',cases=[dict(task_id='marble/dual-panda/A001',key='old',status='passed_probe')],run_status='completed')))
    report=module.summarize([path])
    task=report['tasks']['marble/dual-panda/A001']
    assert task['observed_conditions']==task['qualified_conditions']==0
    assert task['missing_conditions']==48 and task['stale_reports']==[str(path)]
    assert report['runs'][0]['version_status']=='stale'
    assert not report['environment_qualified'] and not report['source_release_ready']
    assert report['distribution_validation']=='not_executed'


def test_duplicate_input_reports_are_rejected(tmp_path):
    path=tmp_path/'empty.json';path.write_text('{}')
    result=module.summarize([path,path])
    assert result['input_errors']==['duplicate_report:'+str(path)]
    assert not result['environment_qualified']
