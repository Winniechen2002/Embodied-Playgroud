"""Private maintainer probes; never registered as client endpoints."""
from copy import deepcopy
from pathlib import Path
from .environment_catalog import digest


def structure_displacement(reference, current):
    """Measure native body displacement without accepting missing/nonfinite poses."""
    import numpy as np
    assert reference and set(reference) == set(current), 'Native body identity changed'
    maximum = 0.
    for name in reference:
        before = np.asarray(reference[name], dtype=float)
        after = np.asarray(current[name], dtype=float)
        assert before.shape == after.shape == (3,), 'Invalid native position shape'
        assert np.isfinite(before).all() and np.isfinite(after).all(), 'Nonfinite native position'
        maximum = max(maximum, float(np.linalg.norm(after - before)))
    return maximum


def local_action_probe(backend):
    """Measure a small command on each robot on a disposable instance.

    This checks actuation and observation, not contact reachability or a solution.
    The caller must create a fresh instance before stability measurements.
    """
    import numpy as np
    spec = backend.describe()['action_spec']
    action = np.asarray(spec['neutral_action'], dtype=float)
    low=np.asarray([-np.inf if v is None else v for v in spec['low']])
    high=np.asarray([np.inf if v is None else v for v in spec['high']])
    selections = []
    if hasattr(backend.env, 'robot_q'):
        for arm in range(2):
            coordinate = int(backend.env.robot_q[arm * 7])
            selections.append((str(arm), arm * 8,
                               lambda coordinate=coordinate: float(backend.env.data.qpos[coordinate])))
    elif getattr(backend,'task',{}).get('backend')=='maniskill':
        robot=backend.e.agent.robot
        names=[j.name for j in robot.get_active_joints()]
        # Check one arm coordinate and one actual gripper coordinate per robot.
        for prefix in ('arm','gripper' if 'gripper' in backend.e.agent.controller.controllers else 'hand'):
            found=False
            for index,name in enumerate(spec['names']):
                joint=name.rsplit('.',1)[-1]
                controller=backend.e.agent.controller.controllers.get(name.split('.',1)[0].split('[',1)[0])
                if name.startswith(prefix) and controller is not None:
                    controlled=list(getattr(controller.config,'joint_names',()))
                    joint=joint if joint in names else controlled[0]
                    coordinate=names.index(joint)
                    selections.append((prefix,index,lambda robot=robot,coordinate=coordinate:float(robot.get_qpos()[0,coordinate])))
                    found=True;break
            if not found:raise AssertionError('No measured '+prefix+' action mapping')
    else:
        for name, robot in backend.env.scene.articulations.items():
            found = None
            for index, command in enumerate(spec['names']):
                joint = command.rsplit('.', 1)[-1]
                if joint in robot.joint_names:
                    # Dual robots may share joint names. Match the action term's
                    # asset when available rather than commanding the other arm.
                    manager = getattr(backend.env, 'action_manager', None)
                    prefix = command.split('.', 1)[0]
                    if manager is not None and prefix in manager.active_terms:
                        term = manager.get_term(prefix)
                        if term._asset is not robot:
                            continue
                    elif len(backend.env.scene.articulations) > 1 and prefix != name.removesuffix('_robot'):
                        continue
                    coordinate = robot.joint_names.index(joint)
                    found = (name, index, lambda robot=robot, coordinate=coordinate:
                             float(robot.data.joint_pos[0, coordinate]))
                    break
            if found is None:
                raise AssertionError('No measured action mapping for robot ' + name)
            selections.append(found)
    if not selections:
        raise AssertionError('No robot actuation to check')
    readings = []
    before_steps = backend.snapshot()['physics_step_count']
    for name, index, read in selections:
        before = read()
        direction = 1. if high[index] - action[index] >= action[index] - low[index] else -1.
        delta = min(.02, float((high[index] - low[index]) * .01))
        if not np.isfinite(delta) or delta <= 0:
            raise AssertionError('Invalid action interval')
        commanded = action.copy()
        commanded[index] += direction * delta
        for _ in range(15):
            observation = backend.step(commanded.tolist())
            if observation['terminated'] or observation['truncated']:
                raise AssertionError('Safe local action ended the episode')
        measured = read() - before
        if not np.isfinite(measured) or abs(measured) <= 1e-7:
            raise AssertionError(f'Native joint did not respond: {name}, action_delta={direction*delta}, measured_joint_delta={measured}')
        readings.append(dict(robot=name, action_index=index, action_delta=direction*delta,
                             measured_joint_delta=measured, minimum_motion=1e-7))
    after = backend.snapshot()
    for robot in after['robots'].values():
        if not np.isfinite(robot['joint_positions']).all() or not np.isfinite(robot['joint_velocities']).all():
            raise AssertionError('Nonfinite proprioception')
    return dict(robot_commands=readings, physics_steps=after['physics_step_count']-before_steps,
                scope='small_joint_actions_and_proprioception', contact_qualification='not_established')


def lifecycle_probe(backend, directory):
    """One neutral action, durable replay and early finish on a disposable instance."""
    from .profiles import RunProfile,CAPABILITY_VERSION
    from .protocol import ProtocolService
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    service=ProtocolService(backend,token='lifecycle',profile=RunProfile(observation='rgb',
        capability_level=0,capability_profile_version=CAPABILITY_VERSION),
        journal_path=directory/'requests.sqlite',resources=backend.resources)
    def request(ident,method,params):
        return dict(version=1,id=ident,token='lifecycle',method=method,params=params)
    try:
        before=backend.snapshot()['physics_step_count']
        action=backend.describe()['action_spec']['neutral_action']
        step=request('once','step',dict(action=action))
        reply=service.handle(step)
        assert reply['ok'],reply
        after=backend.snapshot()['physics_step_count']
        assert after>before
        assert service.handle(step)==reply and backend.snapshot()['physics_step_count']==after
        invalid=service.handle(request('bad','step',dict(action=action+[0])))
        assert not invalid['ok'] and invalid['error']['code']=='invalid_action'
        assert backend.snapshot()['physics_step_count']==after
        finish=service.handle(request('finish','finish',{}))
        assert finish['ok']
        assert not finish['result'].get('success',False), 'Early finish credited an unfinished task'
        denied=service.handle(request('after','step',dict(action=action)))
        assert not denied['ok'] and denied['error']['code']=='episode_closed'
        assert backend.snapshot()['physics_step_count']==after
        return dict(executed_physics_steps=after-before,replayed_steps=0,
            invalid_action_steps=0,post_finish_steps=0,early_finish_result=finish['result'])
    finally:service.close()


def repeat_measurement(first, second):
    """Predeclared tolerances for same-platform native initialization."""
    import numpy as np
    a,b=first['privileged']['pieces'],second['privileged']['pieces']
    assert set(a)==set(b), 'Repeated body identity changed'
    position=angle=joint=0.
    for name in a:
        position=max(position,float(np.linalg.norm(np.asarray(a[name]['position'])-b[name]['position'])))
        qa=np.asarray(a[name]['quaternion']);qb=np.asarray(b[name]['quaternion'])
        cosine=abs(float(np.dot(qa,qb)/(np.linalg.norm(qa)*np.linalg.norm(qb))))
        angle=max(angle,float(2*np.arccos(np.clip(cosine,0.,1.))))
    assert set(first['robots'])==set(second['robots'])
    for name in first['robots']:
        joint=max(joint,float(np.max(np.abs(np.asarray(first['robots'][name]['joint_positions'])-
            second['robots'][name]['joint_positions']),initial=0.)))
    limits=dict(position_m=.0001,orientation_rad=.001,joint_coordinate=.001)
    assert position<=limits['position_m'] and angle<=limits['orientation_rad'] and joint<=limits['joint_coordinate'], 'Native repeat tolerance exceeded'
    return dict(maximum_position_error_m=position,maximum_orientation_error_rad=angle,
        maximum_joint_error=joint,tolerances=limits)


def contract_probe(backend,task):
    import numpy as np
    actual=backend.describe()['action_spec'];expected=task['action_spec']
    for key in ('size','names','semantics','physics_period_s','control_period_s'):
        assert actual[key]==expected[key], 'Native action contract changed: '+key
    for key in ('low','high'):
        assert len(actual[key])==len(expected[key]) and all((a is None and b is None) or (a is not None and b is not None and np.isclose(a,b,atol=1e-7,rtol=0)) for a,b in zip(actual[key],expected[key])), 'Native action range changed'
    assert len(actual['low'])==len(actual['high'])==actual['size']
    return dict(action_spec=actual,contract_sha256=task['contract']['sha256'])


def gateway_probe(backend, directory):
    """Read-only probes against a real backend with model-free authorization tools.

    These workers test permission routing only and make no perception or planning
    claim. No tool ever receives the backend or privileged fields.
    """
    from .plugins import ToolRegistry
    from .profiles import RunProfile, CAPABILITY_VERSION
    from .protocol import ProtocolService
    from .resources import ResourceStore
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    results={}
    foreign=ResourceStore().register(b'other',modality='rgb',profiles=('rgb',),capture_step=0)
    for level in range(4):
        grants=() if level==0 else ('pyroki',) if level==1 else ('pyroki','graspnet')
        profile=RunProfile(observation='privileged' if level==3 else 'rgb',tools=grants,
            capability_level=level,capability_profile_version=CAPABILITY_VERSION)
        registry=ToolRegistry(resources=backend.resources,observation=profile.observation,granted=grants)
        invoked=[]
        for name in ('pyroki','graspnet'):
            def worker(payload, name=name):
                assert payload=={'arguments':{}}
                invoked.append(name)
                return dict(authorized=True)
            registry.register(dict(name=name,version='qa-fixture-v1',description='Authorization fixture; no model',
                input_binding='submitted_arguments',
                input_schema=dict(type='object',properties={},additionalProperties=False),
                output_schema=dict(type='object',properties=dict(authorized=dict(type='boolean')),
                    required=['authorized'],additionalProperties=False),
                observation_profiles=['rgb','rgbd','privileged'],resources=[],
                coordinate_contract=dict(frame='none',convention='none',units='none'),
                source=dict(sha256=digest('authorization-fixture')),checkpoint=dict(sha256=digest('no-model'))),worker)
        service=ProtocolService(backend,token='maintainer-test',profile=profile,
            journal_path=directory/f'level{level}.sqlite',resources=backend.resources,tools=registry)
        index=0
        def call(method,params=None):
            nonlocal index
            index+=1
            return service.handle(dict(version=1,id=str(index),token='maintainer-test',method=method,params=params or {}))
        try:
            before=deepcopy(backend.snapshot())
            observation=call('observe')
            assert observation['ok'] and ('privileged' in observation['result'])==(level==3)
            for method in ('reset','set_seed','set_state'):
                reply=call(method)
                assert not reply['ok'] and reply['error']['code']=='unsupported_method'
            assert not call('observe',dict(fields=['secret']))['ok']
            for resource in (foreign,'/etc/passwd','../scene.usda'):
                assert not call('get_resource',dict(resource_id=resource))['ok']
            listed=call('tools.list')['result']['tools']
            assert {d['name'] for d in listed}==set(grants)
            for tool in ('pyroki','graspnet','unknown'):
                reply=call('tools.call',dict(name=tool,arguments={}))
                assert reply['ok']==(tool in grants)
            assert invoked==list(grants)
            # Authorization without an installed capability also fails closed.
            registry._tools.clear()
            assert call('tools.list')['result']==dict(tools=[])
            for tool in grants:
                rejected=call('tools.call',dict(name=tool,arguments={}))
                assert not rejected['ok'] and rejected['error']['code']=='tool_unavailable'
            assert backend.snapshot()==before
            results['gateway_l'+str(level)]=dict(allowed=list(grants),denied=['reset','set_seed','set_state',
                'unknown_fields','cross_instance_resource','file_paths','uninstalled_tools'],
                observation_digest=digest(observation['result']),physics_unchanged=True,
                fixture_scope='authorization_only_no_model')
        finally:
            service.close()
    return results


def marble_readback(backend, condition):
    """Inspect the compiled joint and scene realization, not CLI arguments."""
    import numpy as np
    env=backend.env; requested=condition['environment_parameters']
    configuration=env.scene_spec['launcher_configuration']
    variant=env.scene_spec['variant']['realized']['background']
    actual=dict(spring_stiffness=float(env.model.jnt_stiffness[env.model.joint('draw').id]),
        launcher_offset_m=env.launcher_offset_m.tolist(),
        ammunition_offset_m=env.ammunition_offset_m.tolist(),
        background=variant['name'],background_motion=variant['motion'])
    assert actual==requested, 'Actual bird initialization differs from condition'
    assert configuration['requested']=={k:requested[k] for k in configuration['requested']}
    # Verify authored ammo coordinates reached compiled free-joint initial state.
    realized=configuration['realized']
    from agentbench_mujoco.scene import LAUNCH_ORIGIN
    pivot=env.model.body('carriage').id
    while env.model.body_parentid[pivot]:pivot=int(env.model.body_parentid[pivot])
    compiled_anchor=env.model.body_pos[pivot].copy()
    assert np.allclose(compiled_anchor,realized['launcher_anchor_m'],atol=1e-12,rtol=0)
    assert np.allclose(compiled_anchor-np.asarray(LAUNCH_ORIGIN),requested['launcher_offset_m'],atol=1e-12,rtol=0)
    errors=[]
    for ammo in env.scene_spec['ammo']:
        q=int(env.model.jnt_qposadr[env.model.joint(ammo['joint']).id])
        errors.append(float(np.max(np.abs(env.model.qpos0[q:q+3]-realized['ammunition_positions_m'][ammo['name']]))))
    assert max(errors,default=0)<1e-12, 'Compiled ammunition pose mismatch'
    cosmetic=env.model.geom_group==4
    assert not np.any(env.model.geom_contype[cosmetic]) and not np.any(env.model.geom_conaffinity[cosmetic])
    observed=deepcopy(condition);observed['environment_parameters']=actual
    return observed,dict(compiled_spring_N_m=actual['spring_stiffness'],
        compiled_launcher_anchor_m=compiled_anchor.tolist(),
        maximum_ammunition_initial_error_m=max(errors,default=0),
        launcher_configuration=deepcopy(configuration),background=deepcopy(variant),
        cosmetic_collision_enabled=False)


def isaac_readback(backend, task, condition):
    """Check native lighting and authored mass/material/pose values after spawn."""
    import math
    import numpy as np
    import omni.usd
    from pxr import UsdGeom, UsdPhysics
    env=backend.env;cfg=env.cfg;stage=omni.usd.get_context().get_stage()
    expected=condition['environment_parameters'];family=task['family']
    assert int(cfg.seed)==condition['seed'], 'Native reset seed mismatch'
    assert math.isclose(1/env.physics_dt,condition['budgets']['physics_hz'],abs_tol=1e-9)
    assert math.isclose(1/(env.physics_dt*cfg.decimation),condition['budgets']['control_hz'],abs_tol=1e-9)
    light=stage.GetPrimAtPath(cfg.scene.sky_light.prim_path)
    intensity=float(light.GetAttribute('inputs:intensity').Get())
    desired=(expected['light_intensity'] if family.startswith('hanoi_') else expected['light']
        if family=='pocket_cube' else 900*expected['authored_sky_light_scale']
        if 'authored_sky_light_scale' in expected else cfg.scene.sky_light.spawn.intensity)
    assert math.isclose(intensity,desired,rel_tol=2e-7,abs_tol=1e-5), 'Native light intensity mismatch'
    measured=dict(sky_light_intensity=intensity,physics_hz=1/env.physics_dt,
        control_hz=1/(env.physics_dt*cfg.decimation),seed=int(cfg.seed),assets={})
    actual=deepcopy(condition)
    if family.startswith('hanoi_') or family=='pocket_cube':
        params=getattr(cfg,'hanoi40_parameters' if family.startswith('hanoi_') else 'cube20_parameters')
        assert digest(params)==digest(expected), 'Native reset sampler mismatch'
        actual['environment_parameters']=deepcopy(params)
        names=([name for name in env.scene.rigid_objects if name.startswith('ring_')]
            if family.startswith('hanoi_') else ['pocket_cube','pocket_cube_carrier'])
        for name in names:
            asset=getattr(cfg.scene,name)
            paths=env.scene[name].root_physx_view.prim_paths
            assert len(paths)==1, 'Expected one native body: '+name
            path=paths[0]
            prim=stage.GetPrimAtPath(path)
            mass=float(UsdPhysics.MassAPI(prim).GetMassAttr().Get())
            assert math.isclose(mass,asset.spawn.mass_props.mass,rel_tol=2e-6), 'Native mass mismatch: '+name
            pose=list(UsdGeom.Xformable(prim).ComputeLocalToWorldTransform(0).ExtractTranslation())
            assert np.allclose(pose,asset.init_state.pos,atol=.002,rtol=0), 'Native initial pose mismatch: '+name
            measured['assets'][name]=dict(mass_kg=mass,position_m=pose)
        if family.startswith('hanoi_'):
            materials=[]
            for prim in stage.Traverse():
                attr=prim.GetAttribute('physics:dynamicFriction')
                if attr and 'Ring' in str(prim.GetPath()):
                    value=float(attr.Get());materials.append(value)
                    assert math.isclose(value,expected['friction'],rel_tol=2e-6), 'Ring friction mismatch'
            assert materials, 'Missing native ring materials'
            measured['dynamic_friction']=materials
        else:
            assert env.pocket_cube_target_tensor[0].tolist()==task['goal']['state'], 'Cube target mismatch'
            measured['target_state']=env.pocket_cube_target_tensor[0].tolist()
    measured['initial_state_digest']=digest(backend.snapshot()['privileged']['pieces'])
    return actual,measured
