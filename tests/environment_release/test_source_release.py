import pytest
from agentbench_platform.environment_catalog import catalog
from agentbench_platform.environment_release import evidence_identity


def source_release_evidence_fixture():
    from agentbench_platform.environment_release import SOURCE_RELEASE_CHECKS
    task=next(t for t in catalog()['tasks'] if t['id']=='marble/dual-panda/A001')
    manifest=dict(count=1,tasks=[task]);evidence=evidence_identity(manifest,{})
    identity=evidence_identity(manifest,{})
    evidence['global_checks']={k:'passed' for k in SOURCE_RELEASE_CHECKS}
    evidence['global_measurements']={k:dict(versions=identity,fixture=True) for k in SOURCE_RELEASE_CHECKS}
    return manifest,evidence


def test_source_release_accepts_complete_current_measurements():
    from agentbench_platform.environment_release import gate as release_gate
    manifest,evidence=source_release_evidence_fixture()
    result=release_gate(manifest,{},evidence)
    assert result['release_ready'] and result['source_release_ready']
    assert 'local_contact' not in result['required_global_checks']
    evidence['global_checks']['assets']='failed'
    assert not release_gate(manifest,{},evidence)['release_ready']


def test_source_release_still_rejects_stale_global_evidence():
    from agentbench_platform.environment_release import gate as release_gate
    manifest,evidence=source_release_evidence_fixture()
    evidence['global_measurements']['licenses']['versions']['source_digest']='stale'
    assert not release_gate(manifest,{},evidence)['release_ready']


def test_source_release_requires_current_validation_identity():
    from agentbench_platform.environment_release import gate as release_gate
    manifest,evidence=source_release_evidence_fixture()
    evidence.pop('validation_version')
    assert not release_gate(manifest,{},evidence)['release_ready']


@pytest.mark.parametrize('check',['source_regression','scorer_fixtures','default_physics','export_smoke'])
@pytest.mark.parametrize('failure',['missing','failed','empty_measurement','nonfinite_measurement'])
def test_source_release_requires_approved_validation_categories(check,failure):
    from agentbench_platform.environment_release import gate as release_gate
    manifest,evidence=source_release_evidence_fixture()
    if failure=='missing':evidence['global_checks'].pop(check)
    elif failure=='failed':evidence['global_checks'][check]='failed'
    elif failure=='empty_measurement':evidence['global_measurements'][check].pop('fixture')
    else:evidence['global_measurements'][check]['fixture']=float('nan')
    assert not release_gate(manifest,{},evidence)['release_ready']
