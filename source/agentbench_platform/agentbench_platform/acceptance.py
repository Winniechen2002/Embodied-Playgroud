"""Streaming maintainer verification; never imported by the public SDK.

Recomputes every physical sample with a fresh instance of the same scorer.
This is independent execution, not a second physical scoring algorithm.
"""
from collections import Counter
import gzip
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
from .kongming_scoring import KongmingScorer


def sha256_file(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()


def equal(a,b,path=''):
    if isinstance(a,dict):
        check(isinstance(b,dict) and a.keys()==b.keys(),'keys '+path)
        for key,value in a.items():equal(value,b[key],path+'.'+key)
    elif isinstance(a,(list,tuple)):
        check(isinstance(b,(list,tuple)) and len(a)==len(b),'list '+path)
        for i,(x,y) in enumerate(zip(a,b)):equal(x,y,path+f'[{i}]')
    elif type(a) in (int,float) and type(b) in (int,float):
        check(math.isfinite(a) and math.isfinite(b) and math.isclose(a,b,rel_tol=1e-8,abs_tol=1e-10),'number '+path)
    else:check(type(a)==type(b) and a==b,'value '+path)


def check(condition,message):
    if not condition:raise ValueError(message)


def verify_trace(directory, *, require_success=False, progress=None):
    directory=Path(directory);trace=directory/'trace.jsonl.gz';started=time.monotonic()
    with gzip.open(trace,'rt') as stream:
        first=json.loads(stream.readline())
    if first.get('kind')=='manifest' and first['data'].get('config',{}).get('task_family')=='rubiks_cube':
        from .rubiks_acceptance import verify_rubiks_trace
        return verify_rubiks_trace(directory,require_success=require_success,progress=progress)
    saved=json.loads((directory/'result.json').read_text())
    counts=Counter();control=physics=0;samples=[];action=None;final=None;manifest=None;scorer=None
    expected={};peak_pen=peak_force=0.
    class RecomputedScorer(KongmingScorer):
        def _physical(self,snapshot):
            nonlocal peak_pen,peak_force
            value=super()._physical(snapshot);metrics=value[2];audit=expected[snapshot['physics_step']]
            for name in ('max_penetration_m','max_forbidden_contact_n'):equal(metrics[name],audit[name],'substep.'+name)
            equal(self.hard_failure,audit['hard_failure'],'substep.hard_failure')
            peak_pen=max(peak_pen,metrics['max_penetration_m']);peak_force=max(peak_force,metrics['max_forbidden_contact_n'])
            return value
    with gzip.open(trace,'rt') as stream:
        for line in stream:
            row=json.loads(line);kind=row['kind'];data=row['data'];counts[kind]+=1
            check(final is None,'record after final')
            if kind=='manifest':
                check(sum(counts.values())==1,'manifest order');manifest=data
                check(data['config']['physics_hz']==120 and data['config']['control_hz']==30,'runtime rates')
                scorer=RecomputedScorer(data['config']['mode'],data['config']['physical_spec'])
            elif kind=='reset':
                check(manifest is not None and counts['reset']==1 and control==physics==0 and sum(counts.values())==2,'reset order')
                check(data['contacts_fresh'] is False,'reset contacts must be explicitly stale')
            elif kind=='action_begin':
                check(counts['reset']==1 and action is None and not samples,'action order')
                check(data['control_step']==control+1 and data['physics_step']==physics,'action chronology')
                action=data
                check(np.asarray(data['requested_action'],dtype=np.float32).astype(float).tolist()==data['applied_action'],'applied float32 action mismatch')
            elif kind=='substep':
                check(action is not None and len(samples)<4,'substep order')
                snapshot=data['snapshot'];physics+=1
                check(snapshot['physics_step']==physics and snapshot['control_step']==control+1,'substep chronology')
                samples.append(snapshot);expected[physics]=data['audit']
            elif kind=='control':
                check(action is not None and len(samples)==4,'incomplete control')
                control+=1
                check(data['observation']['step_index']==control and physics==4*control,'control chronology')
                equal(data['observation']['simulation_time_s'],physics/120,'native time')
                check(data['requested_action']==action['requested_action'] and data['applied_action']==action['applied_action'],'control action mismatch')
                equal(scorer.update(samples[-1],samples),data['result'],'control.result')
                action=None;samples=[];expected={}
                if progress and control%1000==0:progress(dict(controls=control,substeps=physics,elapsed_seconds=time.monotonic()-started))
            elif kind=='capture':
                check(counts['reset']==1 and action is None,'capture order')
                for view in data.values():check(view['capture_step']==control,'capture advances physics')
            elif kind=='final':
                check(scorer is not None and counts['reset']==1 and action is None and not samples,'final order')
                equal(scorer.result(),data['result'],'final.result');final=data
                check(data['step_count']==control and data['physics_steps']==physics,'final chronology')
            else:raise ValueError('Unsupported/incomplete evidence record: '+kind)
    check(final is not None,'missing final')
    check(counts['manifest']==counts['reset']==counts['final']==1 and counts['substep']==4*counts['control']==4*counts['action_begin'],'coverage')
    equal(final,saved,'saved.result')
    if require_success:check(final['result']['success'] and final['termination_reason']=='success','physical task did not succeed')
    reason = final['termination_reason']
    external_causes = {'agent_finish', 'wall_time_limit', 'runtime_shutdown'}
    check(reason in external_causes | {'success', 'hard_failure', 'step_limit'}, 'unsupported termination reason')
    max_steps = manifest['config'].get('max_steps', 36000)  # v1 native default for older manifests.
    check(type(max_steps) is int and max_steps > 0 and control <= max_steps, 'invalid step limit')
    expected_reason = ('success' if final['result']['success'] else
        'hard_failure' if final['result']['hard_failure'] else 'step_limit' if control >= max_steps else None)
    check(reason == expected_reason if expected_reason else reason in external_causes, 'terminal cause inconsistent with physical state')
    return dict(kind='independent_same_scorer_full_recompute',valid=True,controls=control,substeps=physics,counts=dict(counts),
        termination_verification=dict(physical_precedence_checked=True, external_cause_authenticated=False,
            step_limit_source='manifest' if 'max_steps' in manifest['config'] else 'v1_default_36000'),
        final=final,max_penetration_m=peak_pen,max_forbidden_contact_n=peak_force,
        elapsed_seconds=time.monotonic()-started,trace_sha256=sha256_file(trace),
        scorer_sha256=sha256_file(Path(__file__).with_name('kongming_scoring.py')),verifier_sha256=sha256_file(__file__))
