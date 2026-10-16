#!/usr/bin/env python3
"""Publish only complete, current native measurements, never refresh hashes alone."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
for package in ('agentbench','agentbench_platform','agentbench_sdk'):
    sys.path.insert(0,str(ROOT/'source'/package))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native-report',type=Path,action='append',default=[])
    p.add_argument('--maniskill-report',type=Path,action='append',required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--apply',action='store_true')
    p.add_argument('--maniskill-only',action='store_true',help='Recapture every ManiSkill task and preserve other native records')
    args=p.parse_args()
    if args.maniskill_only and args.native_report:p.error('--maniskill-only cannot publish other backends')
    if not args.maniskill_only and not args.native_report:p.error('--native-report is required for full revalidation')
    from agentbench_platform.environment_catalog import catalog
    from agentbench_platform.environment_backend import MarbleBackend
    from agentbench_platform.environment_release import source_files
    manifest=catalog(_native_records={});tasks={t['id']:t for t in manifest['tasks']}
    def key(t):return t['family']+'/'+t['embodiment']+('/'+t['case_id'] if t['backend']=='maniskill' else '')
    path=ROOT/'source/agentbench_platform/agentbench_platform/action_contracts.json'
    old=json.loads(path.read_text());records={};sources={};inputs=[]
    captured=set()
    if args.maniskill_only:
        records={k:v for k,v in old['records'].items() if not k.startswith('maniskill_')}
        sources={k:v for k,v in old['sources'].items() if not k.startswith('env/maniskill_lgd/agentbench_maniskill/')
            and k!='source/agentbench_platform/agentbench_platform/maniskill_backend.py'}
        for name,expected_hash in sources.items():
            if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected_hash:
                raise ValueError('Unrelated native dependency changed: '+name)
    for report_path in args.native_report+args.maniskill_report:
        report=json.loads(report_path.read_text())
        if not report.get('execution',{}).get('capture_contracts') or report['run_status']!='completed':
            raise ValueError('Incomplete native capture: '+str(report_path))
        mani=report_path in args.maniskill_report
        selected=[n for n in map(str,source_files()) if (
            n.startswith('env/maniskill_lgd/agentbench_maniskill/') and (n.endswith('.py') or n.endswith('/tasks.json'))
            or n=='source/agentbench_platform/agentbench_platform/maniskill_backend.py') ] if mani else [
            n for n in map(str,source_files()) if n.endswith('.py') and (n.startswith('source/agentbench/agentbench/')
                or n in ('source/agentbench_platform/agentbench_platform/native_environment.py',
                    'source/agentbench_platform/agentbench_platform/environment_backend.py',
                    'source/agentbench_platform/agentbench_platform/native_backend.py',
                    'source/agentbench_platform/agentbench_platform/native_state.py'))]
        for name in selected:
            actual=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
            if report['source_manifest'].get(name,{}).get('sha256')!=actual:raise ValueError('Changed capture dependency: '+name)
            sources[name]=actual
        for row in report['cases']:
            if row['status']!='passed_probe' or row['physics_steps']<=0:raise ValueError('Failed or empty native measurement')
            task=tasks[row['task_id']];ident=key(task)
            if mani!=(task['backend']=='maniskill'):raise ValueError('Report backend mismatch: '+ident)
            if ident in records:raise ValueError('Duplicate capture: '+ident)
            captured.add(ident)
            description=row['native_description'];records[ident]={n:description[n] for n in ('action_spec','robots')}
        inputs.append(dict(path=str(report_path),sha256=hashlib.sha256(report_path.read_bytes()).hexdigest()))
    if args.maniskill_only:
        expected_capture={key(t) for t in tasks.values() if t['backend']=='maniskill'}
        if captured!=expected_capture:raise ValueError('Incomplete ManiSkill coverage: '+str(sorted(expected_capture-captured)))
    else:
        bird=next(t for t in tasks.values() if t['family']=='marble');backend=MarbleBackend(bird)
        try:
            d=backend.describe();records[key(bird)]={n:d[n] for n in ('action_spec','robots')}
        finally:backend.close()
        for n in map(str,source_files()):
            if n.startswith('source/agentbench/agentbench_mujoco/') and n.endswith('.py'):sources[n]=hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
    expected={key(t) for t in tasks.values()}
    if set(records)!=expected:raise ValueError('Incomplete native coverage: '+str(sorted(expected-set(records))))
    import numpy as np
    differences={}
    for ident,record in records.items():
        action=record['action_spec'];size=action['size']
        low=np.asarray([-np.inf if v is None else v for v in action['low']],dtype=float)
        high=np.asarray([np.inf if v is None else v for v in action['high']],dtype=float)
        neutral=np.asarray(action['neutral_action'],dtype=float)
        if any(a.shape!=(size,) or np.isnan(a).any() for a in (low,high,neutral)) or not np.isfinite(neutral).all() or len(action['names'])!=size or np.any(low>high) or np.any(neutral<low) or np.any(neutral>high):
            raise ValueError('Invalid measured action contract: '+ident)
        if ident in old['records']:
            changes=[n for n in ('size','names','semantics','control_period_s','physics_period_s','low','high') if action[n]!=old['records'][ident]['action_spec'][n]]
            if changes:differences[ident]=changes
    result=dict(scope='maniskill_action_contract_revalidation' if args.maniskill_only else 'native_action_contract_revalidation',inputs=inputs,measured_records=sorted(captured if args.maniskill_only else records),
        added_records=sorted(set(records)-set(old['records'])),contract_differences=differences,applied=bool(args.apply and not differences))
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    if differences:raise ValueError('Existing action contracts changed; inspect '+str(args.output))
    if args.apply:
        measurements=old.get('measurements',[])+inputs if args.maniskill_only else inputs
        path.write_text(json.dumps(dict(version=3,sources=dict(sorted(sources.items())),records=records,measurements=measurements),indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
