"""Portable adapter checks with native-buffer stand-ins, not a PhysX acceptance."""
import importlib
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT/'source/agentbench/agentbench/tasks/manager_based/table_top_manipulation/config/rubiks_cube'
sys.path.insert(0, str(ROOT/'source/agentbench_platform'))


def module(name):
    # Load the real dependency-light physics helpers without Isaac's task registry.
    package_name = '_benchmark_rubiks_physics'
    if package_name not in sys.modules:
        package = ModuleType(package_name); package.__path__ = [str(PACKAGE)]
        sys.modules[package_name] = package
    assert (PACKAGE/(name+'.py')).exists(), name+' missing'
    return importlib.import_module(package_name+'.'+name)


class Tensor:
    def __init__(self, value): self.value = np.asarray(value)
    def __getitem__(self, key): return Tensor(self.value[key])
    def detach(self): return self
    def cpu(self): return self
    def numpy(self): return self.value


def environment():
    rules = module('rubiks_cube_rules')
    native = module('rubiks_cube_native_observation')
    names = tuple(sorted(rules.CubeState.solved().pieces)) + ('world_anchor','core','carrier_x','carrier_y','carrier_z')
    poses = np.zeros((31, 7)); poses[:, :3] = [.70, 0., .6355]; poses[:, 6] = 1.
    for i, name in enumerate(names[:26]):
        poses[i, :3] += .024*np.array(rules.CubeState.solved().pieces[name].home_position)
    events = []
    data = SimpleNamespace(
        joint_pos_limits=Tensor([[[-3.,3.]]*7+[[0.,.04]]*2]),
        soft_joint_pos_limits=Tensor([[[-2.9,2.9]]*7+[[0.,.04]]*2]),
        default_joint_pos=Tensor([[.1]*7+[.04,.04]]),
        joint_pos=Tensor([[.1]*7+[.04,.04]]), joint_vel=Tensor(np.zeros((1,9))),
        root_pos_w=Tensor([[.36,0,.6]]), root_quat_w=Tensor([[1.,0,0,0]]),
        body_pos_w=Tensor([[[.36,0,.6],[.5,0,.9]]]), body_quat_w=Tensor([[[1.,0,0,0]]*2]),
        body_com_pos_w=Tensor([[[.36,0,.6],[.5,0,.9]]]),
        body_link_lin_vel_w=Tensor(np.zeros((1,2,3))), body_link_ang_vel_w=Tensor(np.zeros((1,2,3))),
        body_state_w=Tensor(np.zeros((1,2,13))))
    class View:
        def __init__(self, count): self.count = count
        def get_masses(self): return Tensor(np.ones((self.count,1)))
        def get_inertias(self): return Tensor(np.tile(np.eye(3).flatten(),(self.count,1)))
        def get_material_properties(self): return Tensor(np.tile([[[.8,.6,0.]]],(self.count,1,1)))
        def get_contact_offsets(self): return Tensor(np.zeros((self.count,1)))
        def get_rest_offsets(self): return Tensor(np.zeros((self.count,1)))
        def get_jacobians(self): return Tensor(np.zeros((1,1,6,9)))
    robot = SimpleNamespace(data=data, body_names=['panda_link0','panda_hand'],
        joint_names=['panda_joint'+str(i) for i in range(1,8)]+['panda_finger_joint1','panda_finger_joint2'],
        find_joints=lambda pattern: (list(range(7)) if pattern=='panda_joint[1-7]' else [7,8], []),
        find_bodies=lambda pattern: ([1], []), root_physx_view=View(1),
        set_joint_position_target=lambda values, joint_ids: events.append(('target', np.asarray(values).copy(), list(joint_ids))))
    parts = SimpleNamespace(object_names=names, root_physx_view=View(31),
                            write_object_state_to_sim=lambda *_: events.append(('illegal_write',)))
    class Scene(dict):
        def write_data_to_sim(self): events.append(('write',))
        def update(self, *, dt): events.append(('update',dt))
    scene = Scene(robot=robot, cube_parts=parts)
    for side in ('left','right'):
        scene[side+'_finger_cube_contact'] = SimpleNamespace(data=SimpleNamespace(
            force_matrix_w=Tensor(np.zeros((1,1,26,3))), net_forces_w=Tensor(np.zeros((1,1,3)))))
    sim = SimpleNamespace(current_time_step_index=0, current_time=0., render=lambda: events.append(('render',)))
    def step(*, render):
        assert render is False
        sim.current_time_step_index += 1; sim.current_time = sim.current_time_step_index/120
        events.append(('step',sim.current_time_step_index))
    sim.step = step
    env = SimpleNamespace(scene=scene, sim=sim, device='cuda:0', num_envs=1, physics_dt=1/120,
        cfg=SimpleNamespace(decimation=4,sim=SimpleNamespace(render_interval=4,gravity=(0.,0.,-9.81))),
        _sim_step_counter=0, reset=lambda: events.append(('reset',)),
        apply_passive_detent=lambda: events.append(('detent',)),
        refresh_active_turn_state=lambda: events.append(('refresh',)),
        read_native_cube_sample=lambda: native.NativeCubeSample(sim.current_time_step_index,sim.current_time,names,poses,np.zeros((31,6))))
    return env, events, poses


def test_adapter_declares_single_arm_continuous_gripper_and_uses_native_geometry():
    api = module('rubiks_cube_benchmark')
    env, events, poses = environment()
    state = api.RubiksState(env, mode='solve'); state.reset()
    env.cube_state = 'FORGED_SYMBOLIC_CACHE'
    description = state.describe()
    assert description['task']['family'] == 'rubiks_cube'
    assert description['action_spec']['size'] == 8
    assert set(description['robots']) == {'panda'}
    raw = state.snapshot(0, [])
    assert raw['privileged']['cube']['facelets_urfdlb'] == ''.join(f*9 for f in 'URFDLB')
    assert len(raw['privileged']['pieces']) == 31
    assert len(raw['privileged']['physics']['rigid_bodies']['cube_parts']['mass_kg']) == 31
    # An intermediate/misaligned native state must not publish the cached solved string.
    poses[0, 0] += .006
    measured = state.snapshot(0, [])['privileged']['cube']
    assert not measured['valid'] and 'facelets_urfdlb' not in measured
    assert events == [('reset',)]
    with pytest.raises(RuntimeError, match='Post-reset'):
        env.scene['cube_parts'].write_object_state_to_sim(None)
    with pytest.raises(RuntimeError, match='Reset already'):
        state.reset()


def test_adapter_description_exposes_case_identity_and_no_catalog_configuration():
    import json
    env, events, _ = environment()
    state = module('rubiks_cube_benchmark').RubiksState(env, mode='solve', case_id='C01')
    state.reset()
    desc = state.describe()
    assert desc['task']['case_id'] == 'C01'
    for key in ('scramble', 'seed', 'logical_orientation', 'reference_phase', 'permutation_checksum'):
        assert key not in json.dumps(desc)
    state.snapshot(0, [])
    state.describe()
    assert events == [('reset',)]


def test_prepared_episode_preserves_native_state_and_cannot_restart():
    env,events,_=environment()
    state=module('rubiks_cube_benchmark').RubiksState(env,mode='solve');state.reset()
    state.control=16;state.physics=64
    initial=state.physical(0,0)
    assert hasattr(state,'start_episode')
    state.start_episode(initial)
    assert state.control==state.physics==0 and state.episode_started
    assert state.physical(0,0)==initial and [x[0] for x in events].count('reset')==1
    with pytest.raises(RuntimeError):state.start_episode(initial)
    with pytest.raises(RuntimeError):state.reset()


def test_prepared_episode_rejects_stale_accepted_native_endpoint():
    env,_,_=environment()
    state=module('rubiks_cube_benchmark').RubiksState(env,mode='solve');state.reset()
    initial=state.physical(0,0)
    env.sim.current_time_step_index+=1;env.sim.current_time+=1/120
    assert hasattr(state,'start_episode')
    with pytest.raises(ValueError):state.start_episode(initial)


def test_sdk_action_matches_legacy_joint_targets_and_samples_all_four_substeps(monkeypatch):
    api = module('rubiks_cube_benchmark')
    env, events, _ = environment()
    monkeypatch.setitem(sys.modules, 'torch', SimpleNamespace(tensor=lambda v, **kw: np.asarray(v,dtype=np.float32),float32=np.float32))
    state = api.RubiksState(env, mode='execute_sequence', target_sequence=['U', "U'"])
    state.reset(); samples=[]
    state.install_hook(lambda: samples.append(state.physical(1,len(samples)+1)))
    state.apply([.2]*7+[.6])
    assert len(samples)==4 and [s['native']['native_step'] for s in samples]==[1,2,3,4]
    assert env._sim_step_counter == 4
    targets = [event for event in events if event[0]=='target']
    assert targets[0][1].shape == (1,7) and np.allclose(targets[0][1], .2)
    assert targets[1][1].shape == (1,2) and np.allclose(targets[1][1], .032)
    assert sum(e[0]=='detent' for e in events) == 1
    assert [e[0] for e in events].count('write') == 4
    assert [e[0] for e in events][-2:] == ['refresh','render']
    before = len(events)
    with pytest.raises(ValueError): state.apply([0.]*7+[1.1])
    assert len(events) == before


def test_visual_observations_drop_measured_cube_state_and_physics():
    from agentbench_platform.profiles import RunProfile,sanitize_snapshot
    api = module('rubiks_cube_benchmark')
    env, _, _ = environment(); state = api.RubiksState(env,mode='solve'); state.reset()
    raw = state.snapshot(0,[])
    raw.update(step_index=0,simulation_time_s=0.,terminated=False,truncated=False,cameras={})
    for profile in ('rgb','rgbd'):
        clean = sanitize_snapshot(raw,RunProfile(observation=profile))
        assert 'privileged' not in clean and set(clean['robots']) == {'panda'}
    clean = sanitize_snapshot(raw,RunProfile())
    assert clean['privileged']['cube']['valid']
    assert len(clean['privileged']['cube']['facelets_urfdlb']) == 54


def test_privileged_facelets_use_monochrome_center_equivalence():
    from scipy.spatial.transform import Rotation
    api = module('rubiks_cube_benchmark')
    env, _, poses = environment(); state = api.RubiksState(env,mode='solve'); state.reset()
    catalog = module('rubiks_cube_rules').CubeState.solved().pieces
    center = next(n for n,p in catalog.items() if p.position==(0,0,1))
    poses[env.scene['cube_parts'].object_names.index(center),3:] = Rotation.from_euler('z',.31).as_quat()
    assert state.snapshot(0,[])['privileged']['cube']['valid']
