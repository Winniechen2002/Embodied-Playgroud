import copy
import pytest
from agentbench_platform.kongming_cases import case_ids,trusted_case_spec,_shape_module
from agentbench_platform.native_state import scorer_spec
from agentbench_platform.kongming_scoring import KongmingScorer


def fixture(case_id):
    shapes=_shape_module();case=trusted_case_spec(case_id)
    spec=scorer_spec(shapes.CANONICAL_SPEC,shapes.collision_boxes,shapes.TABLE_TOP_Z,case_spec=case)
    row=dict(control_step=1,physics_step=4,pieces={n:dict(position=copy.deepcopy(p[0]),quaternion=copy.deepcopy(p[1]),
        linear_velocity=[0.,0.,0.],angular_velocity=[0.,0.,0.]) for n,p in case['goal_state'].items()},
        robots={side:dict(fingers=[.04,.04],tcp=[-1.,1.,1.],arm_forces_w=[[0.]*3]*8,
            finger_contacts=[dict(net_w=[0.]*3,allowed_piece_sum_w=[0.]*3,
                forbidden_forces_w=[[0.]*3]*23) for _ in range(2)]) for side in ('left','right')})
    return KongmingScorer(case['task'],spec,case_spec=case),row


@pytest.mark.parametrize('case_id',case_ids())
def test_each_registered_exact_goal_is_admissible_but_not_instant_success(case_id):
    scorer,row=fixture(case_id);result=scorer.update(row)
    assert result['instantaneous_goal'],(case_id,result)
    assert not result['success']


@pytest.mark.parametrize('case_id',['A06','D06','A11','D11'])
def test_non_target_pieces_cannot_be_translated_as_an_alternative_assembly(case_id):
    scorer,row=fixture(case_id)
    selected=set(scorer.case_spec['target_pieces'])
    for name,piece in row['pieces'].items():
        if name not in selected:piece['position'][0]+=.04
    assert not scorer.update(row)['pose_goal_reached']


@pytest.mark.parametrize('case_id',['D06','D11'])
def test_floating_retained_assembly_is_still_rejected(case_id):
    scorer,row=fixture(case_id)
    selected=set(scorer.case_spec['target_pieces'])
    for name,piece in row['pieces'].items():
        if name not in selected:piece['position'][2]+=.01
    result=scorer.update(row)
    assert not result['support_ok'] and not result['instantaneous_goal']
