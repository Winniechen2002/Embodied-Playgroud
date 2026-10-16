#!/usr/bin/env python3
"""Optional full-matrix diagnostics; this is not the source-release gate."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/agentbench_platform'))


def summarize(paths, *, global_evidence=None):
    from agentbench_platform.environment_catalog import catalog
    from agentbench_platform.environment_release import inventory,evidence_identity,matrix,matrix_gate,CHECKS
    manifest=catalog();identity=evidence_identity(manifest,inventory())
    required=matrix(manifest);known={r['key']:r for r in required}
    tasks={t['id']:dict(required_conditions=0,observed_conditions=0,qualified_conditions=0,
        failed_conditions=[],stale_reports=[],scorer_endpoint_fixture='not_executed',
        checks_observed={name:0 for name in CHECKS}) for t in manifest['tasks']}
    for row in required:tasks[row['task_id']]['required_conditions']+=1
    evidence=dict(identity,cases=[],global_checks={},global_measurements={});runs=[];input_errors=[]
    if global_evidence is not None:
        if any(global_evidence.get(k)!=v for k,v in identity.items()):input_errors.append('stale_global_evidence')
        else:
            evidence['global_checks']=global_evidence.get('global_checks',{})
            evidence['global_measurements']=global_evidence.get('global_measurements',{})
    seen_paths=set();seen_keys=set()
    for path in map(Path,paths):
        resolved=path.resolve()
        if resolved in seen_paths:input_errors.append('duplicate_report:'+str(path));continue
        seen_paths.add(resolved)
        raw=path.read_bytes();report=json.loads(raw)
        mismatches=[k for k,v in identity.items() if report.get(k)!=v]
        rows=report.get('cases',report.get('tasks',[]))
        run=dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),scope=report.get('scope'),
            version_status='stale' if mismatches else 'current',version_mismatches=mismatches,
            expected_conditions=report.get('expected_cases',report.get('expected_tasks')),
            recorded_rows=len(rows),statuses=dict(Counter(r.get('status','missing') for r in rows)),
            run_status=report.get('run_status','unspecified'))
        runs.append(run)
        for row in rows:
            task_id=row.get('task_id')
            if task_id not in tasks:input_errors.append('unknown_task:'+str(task_id));continue
            target=tasks[task_id]
            if mismatches:
                target['stale_reports'].append(str(path));continue
            if report.get('scope')=='scorer_endpoint_fixtures_only':
                if target['scorer_endpoint_fixture']!='not_executed':
                    input_errors.append('duplicate_scorer_fixture:'+task_id)
                target['scorer_endpoint_fixture']=row.get('status','missing')
                if row.get('status')=='failed':target['failed_conditions'].append(dict(scope='scorer_endpoint',reason=row.get('error')))
                continue
            key=row.get('key')
            if key not in known:input_errors.append('unknown_condition:'+str(key))
            if key in seen_keys:input_errors.append('duplicate_condition:'+str(key))
            seen_keys.add(key)
            evidence['cases'].append(row)
            target['observed_conditions']+=1
            if row.get('status')=='failed':target['failed_conditions'].append(dict(key=key,reason=row.get('error')))
            for name in CHECKS:
                if row.get('checks',{}).get(name)=='passed':target['checks_observed'][name]+=1
    verdict=matrix_gate(manifest,inventory(),evidence)
    for task_id,counts in verdict['tasks'].items():
        target=tasks[task_id];target['qualified_conditions']=counts['qualified']
        target['stale_reports']=sorted(set(target['stale_reports']))
        target['missing_conditions']=max(0,target['required_conditions']-target['observed_conditions'])
        target['environment_qualified']=counts['qualified']==counts['required'] and not input_errors
    if input_errors:
        verdict['environment_qualified']=verdict['source_release_ready']=verdict['release_ready']=False
    return dict(schema_version=2,scope='environment_quality_only',**identity,
        generated_utc=datetime.now(timezone.utc).isoformat(),input_errors=input_errors,runs=runs,
        tasks=tasks,environment_qualified=verdict['environment_qualified'],
        source_release_ready=verdict['source_release_ready'],distribution_validation='not_executed',
        acceptance=verdict,interpretation='Scorer endpoint fixtures and partial probes do not qualify a condition. Stale evidence is retained for diagnosis but excluded from the current verdict.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',action='append',type=Path,default=[],help='Explicit input report; repeat for nonoverlapping shards')
    parser.add_argument('--global-evidence',type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    result=summarize(args.report,global_evidence=json.loads(args.global_evidence.read_text()) if args.global_evidence else None)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(output=str(args.output),task_count=len(result['tasks']),
        environment_qualified=result['environment_qualified'],source_release_ready=result['source_release_ready'],
        distribution_validation=result['distribution_validation'],input_errors=result['input_errors'])))
    return int(bool(result['input_errors']))


if __name__=='__main__':raise SystemExit(main())
