#!/usr/bin/env python3
"""Per-task endpoint scorer fixtures. No models, solutions or release packaging."""
import argparse
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
for package in ('agentbench','agentbench_platform','agentbench_sdk'):
    sys.path.insert(0,str(ROOT/'source'/package))


def main():
    from agentbench_platform.environment_catalog import catalog
    from agentbench_platform.environment_matrix import effective_condition
    from agentbench_platform.environment_release import inventory,evidence_identity
    from agentbench_platform.scorer_fixtures import marble_fixture,symbolic_fixture,kongming_fixture,bookshelf_fixture
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--backend',choices=['mujoco','isaac','maniskill'])
    parser.add_argument('--maniskill-evidence-root',type=Path)
    parser.add_argument('--task-id',action='append')
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();manifest=catalog()
    tasks=[t for t in manifest['tasks'] if (not args.backend or t['backend']==args.backend)
        and (not args.task_id or t['id'] in args.task_id)]
    if args.task_id and set(args.task_id)!={t['id'] for t in tasks}:parser.error('Unknown or mismatched task ID')
    report=dict(scope='scorer_endpoint_fixtures_only',**evidence_identity(manifest,inventory()),
        expected_tasks=len(tasks),run_status='running',tasks=[],
        limitations=['Fixtures do not prove physical solutions or full condition qualification',
            'Native timeout, early finish and violation generation require separate backend fixtures'])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    def save():
        temp=args.output.with_suffix('.tmp');temp.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');temp.replace(args.output)
    for task in tasks:
        start=time.monotonic();backend=None
        row=dict(task_id=task['id'],contract_sha256=task['contract']['sha256'],status='failed')
        try:
            family=task['family']
            if family=='marble':
                from agentbench_platform.environment_backend import MarbleBackend
                backend=MarbleBackend(task)
                row['measurements']=marble_fixture(backend.env,task)
                assert [t['impulse_threshold'] for t in backend.env.scene_spec['targets']]==task['contract']['scoring']['impulse_thresholds_N_s']
            elif family.startswith('hanoi_') or family=='pocket_cube':
                row['measurements']=symbolic_fixture(task,effective_condition(task))
            elif family=='kongming_lock':row['measurements']=kongming_fixture(task['case_id'],
                'dual-floating-sharpa' if task['embodiment']=='dual-floating-sharpa' else 'franka-panda')
            elif family.startswith('maniskill_'):
                sys.path.insert(0,str(ROOT/'env/maniskill_lgd'))
                from agentbench_maniskill.checks.run import run
                if 'maniskill_fixtures' not in locals():maniskill_fixtures=run(args.maniskill_evidence_root)
                matches=[r for r in maniskill_fixtures['reports'] if r['code']==task['case_id']]
                assert matches and all(r['passed'] for r in matches),'Failed ManiSkill scoring fixtures'
                row['measurements']=dict(configurations=matches,scope='scorer_endpoint_only')
            elif family.startswith('rubiks_'):
                from agentbench_platform.rubiks_endpoint_fixture import check
                row['measurements']=check(task)
            elif family=='bookshelf':row['measurements']=bookshelf_fixture(task)
            else:raise ValueError('Unregistered scorer family')
            row['status']='passed_fixture'
        except Exception as exc:
            import traceback
            row.update(error=type(exc).__name__+': '+str(exc),failure_traceback=traceback.format_exc())
        finally:
            if backend is not None:backend.close()
        row['elapsed_seconds']=time.monotonic()-start
        report['tasks'].append(row);save()
        print(task['id'],row['status'],row.get('error',''),flush=True)
    report['run_status']='failed' if any(r['status']=='failed' for r in report['tasks']) else 'completed';save()
    return int(report['run_status']=='failed')


if __name__=='__main__':raise SystemExit(main())
