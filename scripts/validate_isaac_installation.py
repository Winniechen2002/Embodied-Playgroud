#!/usr/bin/env python3
"""Clean-source Isaac binary installation check; not the engineering condition matrix.

Load each default task, take one declared neutral action, finish, and check RGB
for each family/embodiment. Separate worker processes bound simulator lifetime.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
for package in ('agentbench', 'agentbench_platform', 'agentbench_sdk'):
    sys.path.insert(0, str(ROOT / 'source' / package))


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')
    temp.replace(path)


from agentbench_platform.source_checkout import git_identity


def worker(args, tasks):
    import fastapi, starlette, torch
    from isaaclab.app import AppLauncher
    app = None
    result = dict(scope='isaac_installation_worker', status='failed', tasks=[])
    try:
        app = AppLauncher(headless=True, enable_cameras=True, device='cuda:0').app
        for module in (fastapi, starlette):
            assert Path(module.__file__).resolve().is_relative_to(Path(sys.prefix).resolve()), 'HTTP dependency shadowed by vendor bundle'
        result['http_packages'] = {m.__name__:dict(version=m.__version__, path=str(Path(m.__file__).resolve())) for m in (fastapi, starlette)}
        import omni.usd
        from agentbench_platform.environment_backend import create_isaac_backend
        from agentbench_platform.resources import ResourceStore
        from validate_isaac_environments import create_journal_backend
        from environment_smoke import hold_action
        import torch
        result['gpu'] = torch.cuda.get_device_name()
        result['torch_build'] = torch.__version__
        result['torch_path'] = str(Path(torch.__file__).resolve())
        assert Path(torch.__file__).resolve().is_relative_to(Path(sys.prefix).resolve()), 'Bundled PyTorch shadowed the isolated runtime'
        for task in tasks:
            row = dict(task_id=task['id'], configuration_sha256=task['configuration_sha256'], status='failed')
            backend = None
            try:
                with tempfile.TemporaryDirectory(prefix='ab-isaac-install-') as tmp:
                    directory = Path(tmp)
                    omni.usd.get_context().new_stage()
                    resources = ResourceStore()
                    if task['family'] in ('rubiks_panda', 'rubiks_sharpa', 'kongming_lock'):
                        backend = create_journal_backend(task, 0, directory, resources, AppLauncher)
                    else:
                        backend = create_isaac_backend(task, seed=0, device='cuda:0', asset_dir=directory/'assets', resources=resources)
                    before = backend.snapshot()
                    description = backend.describe()
                    after = backend.step(hold_action(description, before))
                    # NativeBackend.step returns a snapshot, like IsaacEnvironmentBackend.
                    assert after['physics_step_count'] > before['physics_step_count'], 'No physics advance'
                    row.update(physics_steps=after['physics_step_count'], action_size=description['action_spec']['size'])
                    if not result['tasks']:
                        camera = next(iter(description['cameras']))
                        observed = backend.snapshot(camera_ids=[camera])
                        resource = resources.get(observed['cameras'][camera]['rgb_resource_id'], 'rgb')
                        assert resource['byte_length'] > 0
                        row['render'] = {k: resource[k] for k in ('byte_length', 'sha256', 'width', 'height')}
                    row['finish'] = backend.finish()
                    assert backend.finished, 'Finish did not close episode'
                    backend.close()
                    backend = None
                    row['status'] = 'loaded_stepped_finished'
            except Exception:
                row['error'] = traceback.format_exc()
            finally:
                if backend is not None:
                    try: backend.close()
                    except Exception: row['close_error'] = traceback.format_exc()
            result['tasks'].append(row)
            save(args.output, result)
            print(task['id'], row['status'], flush=True)
            if row['status'] == 'failed':
                break  # a damaged native context must not contaminate later tasks
        assert len(result['tasks']) == len(tasks) and all(r['status'] == 'loaded_stepped_finished' for r in result['tasks'])
        result['status'] = 'passed_installation_worker'
    except Exception:
        result['error'] = traceback.format_exc()
    finally:
        save(args.output, result)
        if app is not None: app.close()
    return int(result['status'] != 'passed_installation_worker')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--isaac-root', required=True, type=Path)
    parser.add_argument('--isaac-lab-root', required=True, type=Path)
    parser.add_argument('--family')
    parser.add_argument('--embodiment')
    parser.add_argument('--jobs', type=int, choices=range(1,5), default=1, help='Independent native processes; choose according to available GPU memory')
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    from agentbench_platform.environment_catalog import catalog
    manifest = catalog()
    tasks = [t for t in manifest['tasks'] if t['backend']=='isaac'
             and (not args.family or args.family==t['family'])
             and (not args.embodiment or args.embodiment==t['embodiment'])]
    if not tasks: parser.error('No matching Isaac tasks')
    if args.worker: return worker(args, tasks)
    report = dict(scope='clean_source_isaac_binary_installation', status='failed', run_status='running',
                  full_environment_acceptance='not_executed', distribution_validation='not_executed',
                  task_discovery_count=manifest['count'], expected_tasks=len(tasks), jobs=args.jobs, groups=[])
    try:
        from agentbench_platform.environment_release import inventory, evidence_identity
        report.update(evidence_identity(manifest, inventory()))
        report['checkout'] = git_identity(ROOT)
        report['isaac_lab_checkout'] = git_identity(args.isaac_lab_root)
        assert report['isaac_lab_checkout']['revision'] == 'b4c321024792976150ca55fddb26fa34480d974e'
        assert sys.prefix != sys.base_prefix
        assert 'include-system-site-packages = false' in Path(sys.prefix, 'pyvenv.cfg').read_text().lower()
        version = (args.isaac_root/'VERSION').read_text().strip()
        assert version.startswith('5.1.0'), 'Wrong binary runtime version'
        report['binary_version'] = version
        report['binary_root'] = str(args.isaac_root)
        # Check only the isolated venv; binary-bundled modules are recorded below.
        env = dict(os.environ)
        env.pop('PYTHONPATH', None)
        checked = subprocess.run([sys.executable, '-m', 'pip', 'check'], env=env, capture_output=True, text=True)
        report['dependency_check'] = dict(returncode=checked.returncode, output=checked.stdout+checked.stderr)
        assert checked.returncode == 0, 'Dependency conflicts remain'
        for line in (ROOT/'env/runtime/isaac-binary-constraints.txt').read_text().splitlines():
            if not line or line.startswith('#'): continue
            name, expected = line.split('==')
            assert metadata.version(name) == expected, 'Pin mismatch: '+name
        import fastapi, starlette, isaaclab
        report['import_paths'] = {m.__name__:str(Path(m.__file__).resolve()) for m in (fastapi, starlette, isaaclab)}
        for m in (fastapi, starlette):
            assert Path(m.__file__).resolve().is_relative_to(Path(sys.prefix).resolve()), 'Bundled HTTP package shadowed venv'
        assert Path(isaaclab.__file__).resolve().is_relative_to(args.isaac_lab_root.resolve())
        report['packages'] = json.loads(subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--format=json'], env=env, text=True))
        assert manifest['count'] == 410
        def check_group(group):
            family, robot = group
            target = args.output.with_name(args.output.stem+'-'+family+'-'+robot+'.json')
            command = [sys.executable, str(Path(__file__).resolve()), '--worker', '--isaac-root', str(args.isaac_root),
                       '--isaac-lab-root', str(args.isaac_lab_root), '--family', family, '--embodiment', robot, '--output', str(target)]
            log = target.with_suffix('.log')
            with log.open('w') as stream:
                run = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, timeout=3600)
            record = dict(family=family, embodiment=robot, returncode=run.returncode, evidence=str(target), log=str(log))
            if target.exists(): record['result'] = json.loads(target.read_text())
            return record
        groups = sorted({(t['family'], t['embodiment']) for t in tasks})
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = [pool.submit(check_group, group) for group in groups]
            for future in as_completed(futures):
                record = future.result()
                report['groups'].append(record)
                report['groups'].sort(key=lambda r: (r['family'], r['embodiment']))
                save(args.output, report)
                if record['returncode'] != 0 or record.get('result', {}).get('status') != 'passed_installation_worker':
                    for pending in futures: pending.cancel()
                    raise RuntimeError('Native installation worker failed: '+record['family']+'/'+record['embodiment'])
        rows = [row for group in report['groups'] for row in group.get('result',{}).get('tasks',[])]
        assert len(rows)==len(tasks) and {r['task_id'] for r in rows}=={t['id'] for t in tasks}
        assert all(g['returncode']==0 and g['result']['status']=='passed_installation_worker' for g in report['groups'])
        report.update(status='passed_installation_probe', run_status='completed', configuration_loads=len(rows), rendered_categories=len(report['groups']))
    except Exception:
        report.update(error=traceback.format_exc(), run_status='failed')
    save(args.output, report)
    print(args.output)
    return int(report['status']!='passed_installation_probe')


if __name__ == '__main__':
    raise SystemExit(main())
