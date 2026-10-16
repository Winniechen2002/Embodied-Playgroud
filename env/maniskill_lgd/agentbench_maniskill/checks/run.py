"""Asset-free regression against frozen simulator snapshots; never a robot rollout."""
import hashlib,json
from pathlib import Path
from .. import ROOT,specification
from .long_horizon import run as test_long_horizon
from .geometry_dynamics import test as test_geometry_dynamics

def run(evidence_root=None):
    reports=[]
    for suite,expected in [('long_horizon',10),('geometry_dynamics',40)]:
        cases=json.loads((ROOT/suite/'cases.json').read_text())
        assert len(cases)==expected
        for c in cases:
            folder=ROOT/'evidence'/suite/c['key']
            if evidence_root is not None:
                candidate=Path(evidence_root)/suite/c['key']
                if candidate.exists():folder=candidate
            base=json.loads((ROOT/suite/'tasks.json').read_text())[c['task_id']-1]
            _,task=specification(base['code'],c['physics_variant'])
            initial=json.loads((folder/'initial_state.json').read_text());goal=json.loads((folder/'goal_fixture_state.json').read_text())
            h=hashlib.sha256(json.dumps(task,sort_keys=True).encode()).hexdigest()
            assert initial['task_spec_sha256']==goal['task_spec_sha256']==h,(base['code'],'stale evidence')
            fn=test_long_horizon if suite=='long_horizon' else test_geometry_dynamics
            report=fn(task,initial,goal);report.update(code=task['code'],physics_variant=c['physics_variant']);reports.append(report)
    return dict(passed=all(r['passed'] for r in reports),configurations=len(reports),checks=sum(len(r['checks']) for r in reports),reports=reports,scope='Synthetic evaluator regression on saved initial/goal fixtures; no robot-executed demonstrations.')
