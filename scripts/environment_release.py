#!/usr/bin/env python3
"""Inventory, validate or stage the independent environment distribution."""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/agentbench_platform'))


def main(argv=None):
    from agentbench_platform.environment_catalog import catalog
    from agentbench_platform.environment_release import inventory,gate,build
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('operation',choices=['catalog','check','audit','build'])
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--evidence',type=Path)
    p.add_argument('--candidate',action='store_true')
    p.add_argument('--task-id')
    args=p.parse_args(argv)
    manifest=catalog()
    if args.task_id and args.task_id not in {t['id'] for t in manifest['tasks']}:p.error('Unknown task')
    evidence=json.loads(args.evidence.read_text()) if args.evidence else {}
    if args.operation=='build':
        try:result=build(args.output,evidence=evidence,candidate=args.candidate)
        except ValueError as exc:p.error(str(exc))
        print(json.dumps({k:result[k] for k in ('release_ready','task_count','scope')}));return
    if args.operation=='audit':
        from agentbench_platform.public_content import audit
        result=audit()
    elif args.operation=='catalog':result=manifest
    else:result=gate(manifest,inventory(),evidence)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(args.output)
    if args.operation=='check' and not result['release_ready']:raise SystemExit(1)


if __name__=='__main__':main()
