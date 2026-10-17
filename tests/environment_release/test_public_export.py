"""Source distribution regressions; no simulator or agent is launched."""
import hashlib
import json
from pathlib import Path

from agentbench_platform.environment_catalog import ROOT
from agentbench_platform.environment_contracts import action_contracts
from agentbench_platform.environment_release import build, export_content, source_files
from agentbench_platform.public_content import public_files


def test_native_contracts_remain_source_bound_and_original_records_preserved():
    source = ROOT/'source/agentbench_platform/agentbench_platform/action_contracts.json'
    data = json.loads(source.read_text())
    assert action_contracts() == data['records']
    projection = json.dumps(data['records'], sort_keys=True, separators=(',', ':')).encode()
    provenance = data['release_provenance']
    assert provenance['native_records_sha256'] == hashlib.sha256(projection).hexdigest()
    assert provenance['native_records_changed'] is False
    assert provenance['validation_limitation']
    for name, expected in data['sources'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected


def test_export_is_closed_over_rules_protocol_tests_and_fixture_inputs():
    files = set(public_files())
    for name in ('Agent.md','Agent.en.md','Agent.zh-CN.md','rules/rules.md', 'rules/rules.zh-CN.md', 'docs/evaluation/tasks.json',
                 'scripts/franka_marble_test_protocol.py',
                 'tests/benchmark_platform/test_protocol.py'):
        assert name in files
    snapshots = [name for name in files if '/evidence/' in name]
    assert len(snapshots) == 100
    assert {Path(name).name for name in snapshots} == {'initial_state.json', 'goal_fixture_state.json'}


def test_public_sources_preserve_optional_solver_and_exclude_private_controllers():
    forbidden = {'controller.py', 'baseline.py', 'joint_planner.py',
                 'rubiks_cube_continuous_plan.py', 'rubiks_cube_planner.py',
                 'rubiks_cube_reconcile.py', 'rubiks_cube_session.py', 'rubiks_cube_reorientation.py', 'rubiks_cube_continuous_pose.py'}
    for path in source_files():
        if str(path).startswith("third_party/"):continue
        assert path.name not in forbidden
        content = (ROOT/path).read_bytes()
        once = export_content(path, content)
        assert export_content(path, once) == once
    from agentbench_hanoi40 import catalog as hanoi
    assert not hasattr(hanoi, 'plan')
    assert hanoi.shortest_distance((0,)*5, (2,)*5) == 31


def test_staging_export_preserves_protocol_document_and_never_writes_uri_fragments(tmp_path):
    destination = tmp_path/'source-package'
    status = build(destination)
    assert not status['release_ready']
    assert not (destination/'acceptance-matrix.json').exists()
    assert not (destination/'rules.md').exists()
    assert not (destination/'Vision_rules.md').exists()
    for removed in ('scripts/environment_status.py',
                    'source/agentbench_platform/agentbench_platform/environment_matrix.py',
                    'tests/environment_release/test_condition_matrix.py',
                    'tests/environment_release/test_progress.py'):
        assert not (destination/removed).exists()
    assert not any(key.startswith('matrix_') for key in status)
    assert (destination/'DISTRIBUTION_STATUS').read_text() == 'staging-not-qualified\n'
    assert (destination/'docs/evaluation/tasks.json').is_file()
    assert (destination/'rules/rules.md').read_bytes() == (ROOT/'rules/rules.md').read_bytes()
    assert not any('#' in str(path.relative_to(destination)) for path in destination.rglob('*'))
    assert (destination/'source/agentbench_platform/agentbench_platform/cube_solver.py').exists()
    manifest = json.loads((destination/'distribution-manifest.json').read_text())
    upstream=json.loads((destination/'third_party/manifest.json').read_text())
    assert len(upstream['projects'])==33
    for name,record in upstream['files'].items():
        assert manifest[name]['sha256']==record['sha256']
        assert manifest[name]['bytes']==record['bytes']
    for name in ('tools/cube_solver/Dockerfile','tools/graspnet_cpu/build.py',
                 'tools/rubiks_cube/generate_asset.py','scripts/agentbench_graspnet_cpu_worker.py'):
        assert name in manifest
    import subprocess
    import sys
    for script in ('agentbench_cube_solver.py','agentbench_build_cube_solver.py',
                   'agentbench_build_graspnet_cpu.py','agentbench_graspnet.py'):
        result=subprocess.run([sys.executable,'-I',str(destination/'scripts'/script),'--help'],
                              capture_output=True,text=True)
        assert result.returncode==0,result.stdout+result.stderr

    for name in ('docs/evaluation/tasks.json', 'rules/rules.md', 'scripts/franka_marble_test_protocol.py'):
        assert manifest[name]['sha256'] == hashlib.sha256((destination/name).read_bytes()).hexdigest()
    # Check discovery from the actual exported tree in a fresh interpreter;
    # tests importing the development modules cannot detect changed source pins.
    import subprocess
    import sys
    discovered = destination/'exported-catalog.json'
    result = subprocess.run([sys.executable, '-I',
        str(destination/'scripts/environment_release.py'), 'catalog',
        '--output', str(discovered)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(discovered.read_text())['count'] == 410
    for operation in ('matrix', 'check-matrix'):
        rejected = subprocess.run([sys.executable, '-I',
            str(destination/'scripts/environment_release.py'), operation,
            '--output', str(destination/'removed-command.json')], capture_output=True, text=True)
        assert rejected.returncode == 2
    assert not (destination/'removed-command.json').exists()
    # Retained native checks must still plan exactly one default per task,
    # including when launched from the standalone package without repo imports.
    for script, expected in [('validate_environment_physics.py', 100),
                             ('validate_maniskill_environments.py', 30)]:
        planned = destination/(script+'.json')
        probe = subprocess.run([sys.executable, '-I', str(destination/'scripts'/script),
            '--list-conditions', '--output', str(planned)], capture_output=True, text=True)
        assert probe.returncode == 0, probe.stdout + probe.stderr
        data = json.loads(planned.read_text())
        rows = data['conditions'] if isinstance(data, dict) else data
        assert len(rows) == len({row['task_id'] for row in rows}) == expected
        assert all(row['condition']['seed'] == 0 for row in rows)


def test_public_launcher_rejects_development_demo_and_recording_options():
    import importlib.util
    import pytest
    spec=importlib.util.spec_from_file_location('public_runtime', ROOT/'scripts/agentbench_platform_runtime.py')
    runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
    class Launcher:
        @staticmethod
        def add_app_launcher_args(parser):parser.add_argument('--device')
    for option in ('--dual-sharpa-demo', '--record-video', '--video-control-stride'):
        with pytest.raises(SystemExit):
            runtime.parse_runtime_args(Launcher, ['--output','/tmp/parse-only',option])


def test_optional_grasp_adapter_includes_offline_build_helpers():
    from agentbench_platform import graspnet, graspnet_cpu
    assert callable(graspnet.freeze_setup)
    assert callable(graspnet_cpu.freeze_container_setup)
    assert callable(graspnet_cpu.export_container_context)
    assert callable(graspnet.registry_from_setup)
    assert callable(graspnet_cpu.verify_container_setup)
    assert graspnet.descriptor()['name']=='graspnet'
    assert len(graspnet_cpu.worker_digest())==64
