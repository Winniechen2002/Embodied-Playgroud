"""Streaming Rubik recomputation from raw initialization/substeps/transactions.

This is independent execution of the same scorer, not a second scoring algorithm.
Sealed native failures can verify their preserved prefix, with incomplete
coverage explicitly reported. They can never pass require_success. Unsealed
or corrupted journals are rejected.
"""
from collections import Counter, deque
import gzip
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from .acceptance import check, equal, sha256_file
from .rubiks_scoring import RubiksScorer, contact_pair
from .rubiks_physics import load_physics
from .native_clock import period_from_samples,check_elapsed


def verify_rubiks_trace(directory, *, require_success=False, progress=None):
    directory=Path(directory); trace=directory/'trace.jsonl.gz'; started=time.monotonic()
    saved=json.loads((directory/'result.json').read_text())
    counts=Counter(); config=None; scorer=None; final=None
    control=physics=0; action=None; pending_mechanism=None; samples=[]
    settling=None; initialization_window=deque(maxlen=64)
    clock_period=None
    native_error=None;mechanism_failure=None;case=None
    with gzip.open(trace,'rt') as stream:
        for line in stream:
            row=json.loads(line); kind=row['kind']; data=row['data']; counts[kind]+=1
            check(final is None,'record after final')
            if native_error is not None:check(kind=='final','execution after native error')
            if mechanism_failure is not None and native_error is None:
                check(kind=='native_error','failed mechanism lacks native error boundary')
            if kind=='manifest':
                check(sum(counts.values())==1,'manifest order')
                config=data['config']
                check(config.get('task_family')=='rubiks_cube','Rubik task family required')
                from .rubiks_case_evidence import verify_case_binding
                case=verify_case_binding(config)
                check(config['physics_hz']==120 and config['control_hz']==30,'runtime rates')
                check(hashlib.sha256(json.dumps(config,sort_keys=True,allow_nan=False).encode()).hexdigest()
                      ==data['config_sha256'],'manifest configuration hash')
                check(type(config['max_steps']) is int and config['max_steps']>0,'invalid step budget')
                bounds=config['action_spec']
                check(bounds['size']==8 and len(bounds['low'])==len(bounds['high'])==8,'Rubik action dimensions')
                check(np.isfinite([bounds['low'],bounds['high']]).all(),'nonfinite action bounds')
            elif kind=='initialization_begin':
                check(config is not None and sum(counts.values())==2 and settling is None,'initialization begin order')
                check(type(data['max_controls']) is int and 16<=data['max_controls']<=3600,'initialization budget')
                check(type(data['after_step']) is int and data['after_step']>=0 and np.isfinite(data['native_time_s']),'initialization clock')
                settling=data
            elif kind=='initialization_substep':
                check(settling is not None and scorer is None,'initialization sample order')
                index=counts[kind]
                check(data['index']==index and index<=4*settling['max_controls'],'initialization coverage/budget')
                native=load_physics().native.NativeCubeSample(**data['snapshot']['native'])
                check(native.native_step==settling['after_step']+index,'initialization chronology')
                if clock_period is None:
                    clock_period=period_from_samples(settling['after_step'],settling['native_time_s'],
                                                     native.native_step,native.native_time_s)
                check_elapsed(native.native_time_s,settling['native_time_s'],index,clock_period)
                names=sorted(n for n in native.body_names if n.startswith('cubie_'))
                check(max(contact_pair(data['snapshot'],names))<=20.,'initialization contact force')
                initialization_window.append(data['snapshot'])
            elif kind=='initialization':
                check(config is not None and counts['initialization']==1 and scorer is None,'initialization order')
                if settling is None:
                    check(sum(counts.values())==2,'initialization order')
                else:
                    check(data['initialization_substeps']==counts['initialization_substep'] and
                          counts['initialization_substep']%4==0,'initialization completed control boundary')
                    equal(data['after_step'],settling['after_step'],'initialization boundary')
                    equal(data['samples'],list(initialization_window),'accepted raw initialization window')
                scorer=RubiksScorer(config['mode'],config['physical_spec'],data['samples'],
                    initialization_after_step=data['after_step'],target_sequence=config.get('target_sequence'))
                if 'validation' in data: equal(scorer.initialization,data['validation'],'initialization gates')
            elif kind=='reset':
                check(scorer is not None and counts['reset']==1 and sum(counts.values())==
                      3+counts['initialization_begin']+counts['initialization_substep'],'reset order')
                check(data['contacts_fresh'] is True,'Rubik reset endpoint must follow accepted fresh initialization')
                equal(data['physical'],scorer.initial,'reset.physical')
            elif kind=='action_begin':
                check(counts['reset']==1 and action is None and pending_mechanism is None and not samples,'action order')
                check(not scorer.result()['success'] and not scorer.hard_failure,'action after physical terminal')
                check(data['control_step']==control+1 and data['physics_step']==physics,'action chronology')
                check(control<config['max_steps'],'action beyond budget')
                requested=data['requested_action']; applied=data['applied_action']
                check(isinstance(requested,list) and len(requested)==8 and all(type(v) in (int,float) for v in requested),'invalid action')
                check(all(np.isfinite(v) and lo<=v<=hi for v,lo,hi in zip(requested,bounds['low'],bounds['high'])),'action bounds')
                check(np.asarray(requested,dtype=np.float32).astype(float).tolist()==applied,'float32 action mismatch')
                action=data
            elif kind=='substep':
                check(action is not None and pending_mechanism is None and len(samples)<4,'substep order')
                snapshot=data['snapshot']; physics+=1
                check(snapshot['physics_step']==physics and snapshot['control_step']==control+1,'substep chronology')
                equal(scorer.audit_substep(snapshot),data['audit'],'substep.audit')
                samples.append(snapshot)
            elif kind=='control':
                check(action is not None and len(samples)==4,'incomplete control')
                control+=1
                check(data['observation']['step_index']==control and physics==4*control,'control chronology')
                equal(data['observation']['simulation_time_s'],physics/120,'control time')
                equal(data['requested_action'],action['requested_action'],'requested action')
                equal(data['applied_action'],action['applied_action'],'applied action')
                equal(scorer.update(samples[-1],samples),data['result'],'control.result')
                action=None; samples=[]
                if progress and control%1000==0:
                    progress(dict(controls=control,substeps=physics,elapsed_seconds=time.monotonic()-started))
            elif kind=='mechanism_begin':
                check(counts['reset']==1 and action is None and pending_mechanism is None,'mechanism order')
                check(not scorer.result()['success'] and not scorer.hard_failure,'mechanism after physical terminal')
                check(data['control_step']==control and data['physics_step']==physics,'mechanism chronology')
                equal(data['before'],scorer.last_row,'mechanism.begin.before')
                pending_mechanism=data
            elif kind=='mechanism':
                check(pending_mechanism is not None and action is None,'mechanism completion order')
                for key in ('name','arguments','before','control_step','physics_step'):
                    equal(data[key],pending_mechanism[key],'mechanism.'+key)
                scorer.mechanism_event(data)
                # A forged accepted receipt is not a legitimate physical failure
                # record; the runtime must seal it with native_error evidence.
                if scorer.hard_failure:mechanism_failure=data
                pending_mechanism=None
            elif kind=='native_error':
                check(scorer is not None and counts['reset']==1 and counts['native_error']==1,'native error order')
                check(type(data['control_step']) is int and type(data['physics_step']) is int,'native error counters')
                check(isinstance(data.get('exception_type'),str) and isinstance(data.get('message'),str),'native error metadata')
                # Legacy v1 recorded only apply exceptions without an operation.
                operation=data.get('operation','control')
                stage=data.get('stage','apply' if operation=='control' else None)
                if action is not None:
                    check(operation=='control' and stage in {'apply','update','control_observer','observation'} and pending_mechanism is None,
                          'native control failure stage')
                    check(data['control_step']==control+1,'failed control chronology')
                    # A hook increments its physical tick before reading state.
                    # If that read fails, at most its final sample is missing.
                    check(physics<=data['physics_step']<=min(physics+1,4*(control+1)),'failed physical chronology')
                    if stage in {'update','control_observer','observation'}:
                        check(len(samples)==4 and data['physics_step']==physics,'failed result requires four samples')
                        scorer.update(samples[-1],samples)
                else:
                    check(data['control_step']==control and data['physics_step']==physics,'boundary failure chronology')
                    check(stage is None,'unexpected boundary control stage')
                    if operation=='mechanism':
                        event=pending_mechanism or mechanism_failure
                        check(event is not None and data.get('name')==event['name'],'failed mechanism identity')
                    else:
                        check(operation=='abort' and pending_mechanism is None and mechanism_failure is None,
                              'unexpected native failure operation')
                scorer.hard_failure=True
                scorer.failure_reasons.add('native_execution_error')
                scorer.coverage_complete=False
                native_error=data
            elif kind=='capture':
                check(counts['reset']==1 and action is None and pending_mechanism is None,'capture order')
                for view in data.values(): check(view['capture_step']==control,'capture advances physics')
            elif kind=='final':
                check(scorer is not None and counts['reset']==1,'final order')
                if native_error is None:
                    check(action is None and pending_mechanism is None and not samples,'incomplete unsealed final')
                equal(scorer.result(),data['result'],'final.result')
                check(data['step_count']==(native_error['control_step'] if native_error else control)
                      and data['physics_steps']==(native_error['physics_step'] if native_error else physics),'final chronology')
                final=data
            else:
                raise ValueError('Unsupported or incomplete Rubik evidence record: '+kind)
    check(final is not None,'missing final')
    check(counts['manifest']==counts['initialization']==counts['reset']==counts['final']==1,'episode boundaries')
    check(counts['substep']==4*counts['control']+len(samples),'recorded substep coverage')
    check(counts['action_begin']==counts['control']+int(action is not None),'action coverage')
    check(counts['mechanism_begin']==counts['mechanism']+int(pending_mechanism is not None),'transaction coverage')
    equal(final,saved,'saved.result')
    result=final['result']; reason=final['termination_reason']
    physical_reason=('success' if result['success'] else 'hard_failure' if result['hard_failure']
                     else 'step_limit' if control>=config['max_steps'] else None)
    check(reason==physical_reason if physical_reason else reason in {'agent_finish','wall_time_limit','runtime_shutdown'},
          'terminal cause inconsistent with physical state')
    if require_success: check(result['success'] and reason=='success','physical task did not succeed')
    files=[Path(__file__),Path(__file__).with_name('rubiks_scoring.py'),Path(__file__).with_name('native_clock.py')]
    files.extend(Path(module.__file__) for module in vars(load_physics()).values())
    return dict(kind='independent_same_scorer_failed_prefix_recompute' if native_error else 'independent_same_scorer_full_recompute',task_family='rubiks_cube',valid=True,
        controls=control,substeps=physics,counts=dict(counts),final=final,
        case=case,case_binding_verified=case is not None,
        initialization=scorer.initialization,
        trace_sha256=sha256_file(trace),implementation_sha256={p.name:sha256_file(p) for p in files},
        termination_verification=dict(physical_precedence_checked=True,external_cause_authenticated=False),
        evidence_coverage=dict(complete=native_error is None and scorer.coverage_complete,
            native_error_recorded=native_error is not None,control_attempts=counts['action_begin'],
            scored_controls=scorer.last_control,unrecorded_physics_steps=final['physics_steps']-physics,
            unfinished_mechanism=pending_mechanism is not None),
        elapsed_seconds=time.monotonic()-started)
