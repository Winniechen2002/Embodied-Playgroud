import argparse,json
from pathlib import Path
from . import catalog
p=argparse.ArgumentParser(description='ManiSkill long-horizon, geometry and dynamics environments')
s=p.add_subparsers(dest='command',required=True)
s.add_parser('list',help='List the 30 tasks without simulator dependencies')
a=s.add_parser('assets',help='Install or verify the bundled simulator assets');a.add_argument('--verify',action='store_true');a.add_argument('--destination',type=Path)
t=s.add_parser('test-oracles',help='Run asset-free success-check regression');t.add_argument('--output',type=Path)
t.add_argument('--evidence-root',type=Path,help='Fresh private fixtures; absent cases fall back to hash-checked historical fixtures')
v=s.add_parser('validate',help='Initialize and physically settle reference fixtures; not a solver');v.add_argument('--task',required=True);v.add_argument('--physics-variant',type=int,default=0);v.add_argument('--output',type=Path,required=True)
v=s.add_parser('smoke',help='Load, step and inspect every task using the bundled assets');v.add_argument('--task',default='all');v.add_argument('--output',type=Path,required=True)
r=s.add_parser('render',help='Render an initial scene or initialized goal reference');r.add_argument('--task',required=True);r.add_argument('--physics-variant',type=int,default=0);r.add_argument('--stage',choices=['initial','goal'],default='initial');r.add_argument('--output',type=Path,required=True);r.add_argument('--backend',default='gpu');r.add_argument('--width',type=int,default=1800)
a=p.parse_args()
if a.command=='list':
    for t in catalog():print(f"{t['code']:>3}  category={t['category']}  {t['title']}  [{t['robot']}]")
elif a.command=='assets':
    from .assets import install,verify
    from .common.paths import ASSET_ROOT
    dest=a.destination or ASSET_ROOT
    if a.verify:
        bad=verify(dest);print(json.dumps(dict(passed=not bad,missing_or_changed=bad)));raise SystemExit(bool(bad))
    print(install(dest))
elif a.command=='test-oracles':
    from .checks.run import run
    report=run(a.evidence_root)
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='reports'},indent=2))
    for r in report['reports']:
        if not r['passed']:print(r['code'],r['physics_variant'],[x['name'] for x in r['checks'] if not x['passed']])
    raise SystemExit(0 if report['passed'] else 1)
else:
    from .runtime import validate,smoke,render
    if a.command=='validate':report=validate(a.task,a.physics_variant,a.output)
    elif a.command=='smoke':report=smoke(a.task,a.output)
    else:report=render(a.task,a.physics_variant,a.stage,a.output,a.backend,a.width)
    print(json.dumps(report,indent=2));raise SystemExit(0 if report.get('passed',True) else 1)
