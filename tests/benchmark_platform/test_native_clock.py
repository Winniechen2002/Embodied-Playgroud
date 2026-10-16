"""Isaac's float32 fixed dt must not look like a dropped sample after 38 seconds."""
import numpy as np
import pytest


def test_frozen_native_clock_preserves_120hz_over_six_hours():
    from agentbench_platform.native_clock import period_from_samples,check_elapsed
    for dt in (1/120,float(np.float32(1/120))):
        period=period_from_samples(3,3*dt,66,66*dt)
        for steps in (4601,4602,864000,2592000):
            check_elapsed((66+steps)*dt,66*dt,steps,period)
            with pytest.raises(ValueError):check_elapsed((67+steps)*dt,66*dt,steps,period)
        assert period==dt
    with pytest.raises(ValueError):period_from_samples(3,0.,66,63*.0084)


def test_actual_long_episode_clock_is_accepted_but_gap_still_fails():
    from test_rubiks_scoring import setup,snapshot
    from agentbench_platform.rubiks_scoring import RubiksScorer
    trace,joints,old=setup('execute_sequence',['U'])
    dt=float(np.float32(1/120));init=[]
    for step in range(1,62):
        trace.step=step;row=snapshot(trace,0,joints);row['native']['native_time_s']=step*dt;init.append(row)
    scorer=RubiksScorer('execute_sequence',old.spec,init,initialization_after_step=0,target_sequence=['U'])
    # Jump the accounting cursor only in this test to reach the known native
    # regression boundary without thousands of repeated geometry audits.
    scorer.observed_substeps=4601
    from dataclasses import replace
    scorer.turns.last=replace(scorer.turns.last,native_step=4662,native_time_s=4662*dt)
    trace.step=4663;row=snapshot(trace,4602,joints);row['native']['native_time_s']=4663*dt
    result=scorer.audit_substep(row)
    assert result['coverage_complete'],scorer.failure_reasons
    trace.step=4665;row=snapshot(trace,4603,joints);row['native']['native_time_s']=4665*dt
    assert not scorer.audit_substep(row)['coverage_complete']
