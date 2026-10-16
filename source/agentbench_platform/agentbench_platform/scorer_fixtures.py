"""Private deterministic scorer fixtures. Never installed as gateway tools.

These validate endpoint scoring, not physical solutions. Timeout and finish
behavior is tested separately at the native backend/lifecycle boundary.
"""
from copy import copy,deepcopy
from types import SimpleNamespace
from .environment_catalog import ROOT,source_module


def marble_fixture(env,task):
    import numpy as np
    target=copy(env)
    target.target_alive=np.zeros_like(env.target_alive)
    target.target_alive[list(env.protected_indices)]=True
    target.toppled=set(range(task['contract']['scoring']['minimum_toppled']))
    target.fracture=SimpleNamespace(broken=set(task['contract']['scoring']['required_fractures']))
    target.target_hits=[dict(time=0.,protected=False)]
    target.data=SimpleNamespace(time=3.)
    target.failure=None
    assert target.success,'Legal endpoint rejected'
    target.target_alive[env.required_indices[0]]=True
    assert not target.success,'Wrong endpoint accepted'
    target.target_alive[env.required_indices[0]]=False
    if env.protected_indices:
        target.data.time=2.999
        assert not target.success,'Protected observation window bypassed'
        target.data.time=3.
    target.failure='fixture_first_violation'
    assert not target.success,'Violation accepted'
    # The shallow fixture must leave the physical instance and its arrays alone.
    assert np.array_equal(env.target_alive,np.ones_like(env.target_alive))
    return dict(legal_goal=True,wrong_goal_rejected=True,first_violation_denies_success=True,
        stable_time='protected_window_checked' if env.protected_indices else 'no_hold_required_by_contract',
        scope='scorer_endpoint_only')


def symbolic_fixture(task,condition):
    """Exercise every authored Hanoi/cube goal with the actual condition parameters."""
    family=task['family']
    if family.startswith('hanoi_'):
        rules=source_module('_qa_hanoi',ROOT/'source/agentbench/agentbench_hanoi40','rules')
        authored=source_module('_qa_hanoi',ROOT/'source/agentbench/agentbench_hanoi40','catalog').BY_ID[task['case_id']]
        monitor=rules.ObservedMonitor(authored,condition['environment_parameters'])
        poses=[monitor.expected(i) for i in range(5)]
        assert not monitor.result(poses)['task_success']
        # Test-only endpoint construction; no reset/state-write is exposed to clients.
        monitor.state=tuple(authored.goal)
        poses=[monitor.expected(i) for i in range(5)]
        for _ in range(119):monitor.observe(poses,dt=1/120)
        assert not monitor.result(poses)['task_success']
        monitor.observe(poses,dt=1/120)
        assert monitor.result(poses)['task_success']
        try:monitor.observe(poses,depth=.0051,dt=1/120)
        except rules.RuleFailure:pass
        else:raise AssertionError('Penetration violation was not detected')
        first=deepcopy(monitor.failure)
        try:monitor.observe(poses,dt=1/120)
        except rules.RuleFailure:pass
        assert monitor.failure==first and not monitor.result(poses)['task_success']
        return dict(legal_goal=True,wrong_goal_rejected=True,stable_short_rejected=True,
            first_violation_latched=True,stable_seconds_required=1.,scope='scorer_endpoint_only')
    if family=='pocket_cube':
        module=source_module('_qa_cube',ROOT/'source/agentbench/agentbench_cube20','evaluation')
        authored=module.BY_ID[task['case_id']]
        values=dict(state=list(authored.goal.as_vector()),angles=[0.]*6,speeds=[0.]*6,
            active_face=-1,committed_turns=len(module.moves(authored.transition)),native_failed=False,
            penetration_m=0.,fingerprint='fixture',dt=1/240,physical_goal_matches=True)
        guard=module.TerminalGuard(task['case_id'],'fixture')
        assert not guard.update(**dict(values,state=list(authored.start.as_vector())))
        for _ in range(239):assert not guard.update(**values)
        assert guard.update(**values)
        for name,value in [('committed_turns',values['committed_turns']+1),('physical_goal_matches',False),
            ('active_face',0),('speeds',[.051]*6),('angles',[.03]*6)]:
            probe=module.TerminalGuard(task['case_id'],'fixture')
            for _ in range(241):assert not probe.update(**dict(values,**{name:value}))
        for corruption in (dict(penetration_m=.00026),dict(fingerprint='changed'),dict(native_failed=True)):
            probe=module.TerminalGuard(task['case_id'],'fixture')
            assert not probe.update(**dict(values,**corruption))
            first=probe.first_failure
            for _ in range(241):assert not probe.update(**values)
            assert probe.first_failure==first and first
        return dict(legal_goal=True,wrong_goal_rejected=True,stable_short_rejected=True,
            committed_turns_checked=True,physical_goal_checked=True,detents_checked=True,
            first_violation_latched=True,fingerprint_checked=True,scope='scorer_endpoint_only')
    raise ValueError('No symbolic fixture for '+family)


def kongming_fixture(case_id,embodiment='franka-panda'):
    from .kongming_cases import trusted_case_spec,_shape_module
    from .native_state import scorer_spec
    from .kongming_scoring import KongmingScorer
    shapes=_shape_module();case=trusted_case_spec(case_id)
    spec=scorer_spec(shapes.CANONICAL_SPEC,shapes.collision_boxes,shapes.TABLE_TOP_Z,case_spec=case)
    goal=dict(pieces={n:dict(position=deepcopy(p[0]),quaternion=deepcopy(p[1]),
        linear_velocity=[0.]*3,angular_velocity=[0.]*3) for n,p in case['goal_state'].items()},
        robots={side:dict(fingers=[.04]*2,tcp=[-1.,1.,1.],arm_forces_w=[[0.]*3]*8,
            finger_contacts=[dict(net_w=[0.]*3,allowed_piece_sum_w=[0.]*3,
                forbidden_forces_w=[[0.]*3]*23) for _ in range(2)]) for side in ('left','right')})
    if embodiment=='dual-floating-sharpa':
        contact=dict(net_w=[0.]*3,forces_w=[[0.]*3 for _ in range(6)],
            forbidden_forces_w=[[0.]*3 for _ in range(7)],piece_names=list(spec['pieces']))
        for robot in goal['robots'].values():
            robot.update(finger_positions=[0.]*22,finger_default_positions=[0.]*22,
                fingertip_contacts=[deepcopy(contact) for _ in range(5)],palm_contacts=[deepcopy(contact)],
                body_forces_w=[[0.]*3 for _ in range(21)])
    def run(scorer,start,count,template):
        for control in range(start,start+count):
            samples=[dict(deepcopy(template),control_step=control,physics_step=step)
                for step in range(4*control-3,4*control+1)]
            result=scorer.update(samples[-1],samples)
        return result
    scorer=KongmingScorer(case['task'],spec,case_spec=case,embodiment=embodiment)
    count=60 if case['task']=='assemble' else 30
    assert not run(scorer,1,count-1,goal)['success'], 'Insufficient hold accepted'
    legal=run(scorer,count,1,goal)
    assert legal['success'],(case_id,legal)
    wrong=deepcopy(goal)
    wrong['pieces']['key']['position'][0]+=.06
    probe=KongmingScorer(case['task'],spec,case_spec=case,embodiment=embodiment)
    assert not run(probe,1,1,wrong)['instantaneous_goal'], 'Incorrect goal accepted'
    bad=deepcopy(goal);bad['robots']['left']['arm_forces_w']=[[1.,0.,0.]]*8
    if embodiment=='dual-floating-sharpa':bad['robots']['left']['body_forces_w']=[[1.,0.,0.]]*21
    probe=KongmingScorer(case['task'],spec,case_spec=case,embodiment=embodiment)
    first=run(probe,1,1,bad)
    assert first['hard_failure'] and not first['success']
    recovered=run(probe,2,count,goal)
    assert recovered['hard_failure'] and not recovered['success']
    return dict(case_id=case_id,legal_goal=True,wrong_goal_rejected=True,stable_short_rejected=True,
        first_violation_latched=True,required_controls=count,scope='scorer_endpoint_only')


def bookshelf_fixture(task):
    import torch
    from .environment_catalog import CONFIG
    directory=CONFIG/'organize_bookshelf'
    rules=source_module('_qa_books',directory,'rules')
    geometry=source_module('_qa_books',directory,'geometry')
    variants=source_module('_qa_books',directory,'variants')
    variant=variants.BY_ID[task['case_id']];table=variant.slot_table();slots=table.tensors()
    wall=1 if variant.wall_anchor=='positive_y' else -1
    pos,rot=rules.goal_layout(table,wall,layout=geometry.LAYOUTS[variant.layout])
    pos,rot=pos[None].clone(),rot[None].clone()
    released=torch.ones((1,len(table.present)),dtype=torch.bool)
    interior=source_module('_qa_books',directory,'catalog').CRATE_CLASS.part('interior') if table.crate else None
    def evaluate(points,free=released):
        return rules.slot_rules(points,rot,torch.zeros_like(points),torch.zeros_like(points),free,slots,
            wall_anchor=variant.wall_anchor,crate_interior=interior,layout=geometry.LAYOUTS[variant.layout])
    valid=evaluate(pos)['valid'];assert valid.item(),'Legal shelf layout rejected'
    wrong=pos.clone();wrong[0,next(iter(table.present_indices())),2]+=2.
    assert not evaluate(wrong)['valid'].item(),'Wrong shelf layout accepted'
    assert not evaluate(pos,torch.zeros_like(released))['valid'].item(),'Unreleased objects accepted'
    hold=geometry.HoldCounter(1,'cpu')
    for step in range(1,15):assert not hold.update(valid,torch.tensor([step]),1/30).item()
    assert hold.update(valid,torch.tensor([15]),1/30).item()
    assert not hold.update(torch.tensor([False]),torch.tensor([16]),1/30).item()
    assert not hold.update(valid,torch.tensor([17]),1/30).item()
    return dict(case_id=task['case_id'],legal_goal=True,wrong_goal_rejected=True,
        unreleased_rejected=True,stable_short_rejected=True,continuous_hold_checked=True,scope='scorer_endpoint_only')
