"""Maintainer SDK diagnostic; sequence probe deliberately performs no face turn."""
import base64
import json
from pathlib import Path
import sys
import threading

import numpy as np


def record_rgbd(client, captures, directory, *, table_height):
    from PIL import Image
    result = {}
    for name, view in captures.items():
        def fetch(key, dtype, shape):
            raw = client.get_resource(view[key])
            return np.frombuffer(base64.b64decode(raw['data_base64']), dtype=dtype).reshape(shape)
        rgb = fetch('rgb_resource_id', np.uint8, (480,640,3))
        depth = fetch('depth_resource_id', '<f4', (480,640))
        mask = fetch('validity_resource_id', np.uint8, (480,640)).astype(bool)
        assert mask.sum() > 1000 and np.isfinite(depth).all() and rgb.std() > 1
        calibration = view['calibration']
        k = np.asarray(calibration['intrinsics']); w = np.asarray(calibration['world_from_camera'])
        offset = calibration['pixel_center_offset']; y,x = np.indices(depth.shape)
        rays = np.stack(((x+offset[0]-k[0,2])/k[0,0], (y+offset[1]-k[1,2])/k[1,1], np.ones_like(x)),axis=-1)
        world = (rays*depth[...,None])@w[:3,:3].T+w[:3,3]
        table = mask & (abs(world[...,2]-table_height)<.003)
        assert table.sum() > 1000, (name, int(table.sum()))
        error = float(np.quantile(abs(world[...,2][table]-table_height), .95))
        assert error < .0001, (name, error)
        Image.fromarray(rgb).save(Path(directory)/(name+'.png'))
        np.savez_compressed(Path(directory)/(name+'.npz'),rgb=rgb,depth=depth,validity=mask,
            intrinsics=k,world_from_camera=w,pixel_center_offset=offset,
            capture_step=view['capture_step'],capture_id=view['capture_id'])
        result[name] = dict(valid_pixels=int(mask.sum()),table_plane_pixels=int(table.sum()),
            table_z_error_p95=error,capture_id=view['capture_id'],capture_step=view['capture_step'])
    return result


def record_rgb(client, captures, directory):
    """Fetch one non-depth RGB frame per camera without advancing native time."""
    import base64
    from PIL import Image
    result = {}
    for name, view in captures.items():
        raw = client.get_resource(view['rgb_resource_id'])
        rgb = np.frombuffer(base64.b64decode(raw['data_base64']), dtype=np.uint8).reshape(480, 640, 3)
        assert rgb.std() > 1
        Image.fromarray(rgb).save(Path(directory)/(name+'.png'))
        result[name] = dict(capture_id=view['capture_id'], capture_step=view['capture_step'],
                            mean=float(rgb.mean()), std=float(rgb.std()))
    return result


def run_smoke(backend, env, resources, directory, socket_path, *, journal_path, storage_guard=None,
              profile='rgbd'):
    from agentbench_sdk import Client
    from agentbench_sdk.client import ProtocolError
    from scipy.spatial.transform import Rotation
    from .native_backend import MainThreadDispatcher, DispatchedBackend
    from .profiles import RunProfile
    from .protocol import ProtocolService, ProtocolServer
    if profile not in ('privileged', 'rgb', 'rgbd'):
        raise ValueError('invalid native smoke profile')
    dispatcher = MainThreadDispatcher()
    service = ProtocolService(DispatchedBackend(backend,dispatcher),token='native-smoke',
        profile=RunProfile(observation=profile),journal_path=journal_path,resources=resources,storage_guard=storage_guard)
    server = ProtocolServer(socket_path,service); server.start()
    results = {}; errors = []
    mode = backend.scorer.mode
    sharpa = backend.bridge.describe()['task'].get('embodiment') == 'floating-sharpa'
    action_size = 28 if sharpa else 8
    target_frame = None
    if not sharpa:
        pose = backend.scorer._core(backend.scorer.initial)
        target_frame = Rotation.from_quat(pose[3:]).as_matrix().tolist()
    table_height = backend.scorer.spec['table_height_m']
    def client_work():
        try:
            client = Client(str(server.socket_path),'native-smoke',timeout=120.)
            description = client.describe(); initial = client.observe()
            assert description['action_spec']['size'] == action_size
            assert initial['step_index'] == 0 and not initial['terminated']
            try:
                client.step([0.]*(action_size-1))
            except ProtocolError:
                pass
            else:
                raise AssertionError('Invalid action was not rejected')
            assert client.observe()['step_index'] == 0
            capture = client.observe(camera_ids=['front_left','front_right','top'])
            again = client.observe(camera_ids=['top'])
            assert capture['simulation_time_s'] == again['simulation_time_s'] == 0.
            assert capture['robots'] == again['robots']
            if profile == 'privileged':
                assert 'privileged' in capture
                geometry = dict(profile='privileged', cameras=sorted(capture['cameras']))
            elif profile == 'rgb':
                assert 'privileged' not in capture
                geometry = dict(profile='rgb', cameras=record_rgb(client,capture['cameras'],directory))
            else:
                assert 'privileged' not in capture
                geometry = dict(profile='rgbd', cameras=record_rgbd(client,capture['cameras'],directory,table_height=table_height))
            hold = backend.bridge.neutral_action() if sharpa else [0.]*7+[1.]
            action = hold[:]
            observation = client.step(action)['observation']
            assert observation['step_index'] == 1 and not observation['terminated']
            for _ in range(15):
                observation = client.step(hold)['observation']
            receipts = []
            if mode == 'execute_sequence' and not sharpa:
                assert not observation['terminated']
                request_id = 'transport-begin-once'
                receipt = client.mechanism.command('transport.begin',{'target_frame':target_frame},request_id=request_id)
                assert receipt == dict(accepted=True,state='transporting',epoch=1)
                repeated = client.mechanism.command('transport.begin',{'target_frame':target_frame},request_id=request_id)
                assert repeated == receipt
                receipts.append(receipt)
                assert not client.mechanism.command('transport.attach',{})['accepted']
                for _ in range(16):
                    observation = client.step(hold)['observation']
                    assert not observation['terminated']
                denied = client.mechanism.command('transport.attach',{})
                assert denied == dict(accepted=False,state='transporting',epoch=1)
                receipts.append(denied)
            client.finish()
            results.update(sdk_smoke_passed=True,kind='maintainer SDK wiring diagnostic',profile=profile,
                full_moving_task_acceptance=False,agent_acceptance=False,container_acceptance=False,
                geometry=geometry,mechanism_receipts=receipts,observation_nonadvancing=True,
                illegal_action_nonadvancing=True)
        except BaseException as exc:
            errors.append(exc)
    thread = threading.Thread(target=client_work); thread.start()
    try:
        while thread.is_alive(): dispatcher.pump(timeout=.05)
        thread.join()
        if errors: raise errors[0]
        assert not backend.scorer.hard_failure and backend.scorer.coverage_complete
        assert backend.physics == 4*backend.control
        if mode == 'execute_sequence' and not sharpa:
            assert backend.control == 32 and not backend.result['success']
        elif not sharpa:
            assert backend.control == 16 and backend.result['success']
        assert not any(n=='baselines' or n.startswith('baselines.') for n in sys.modules)
        results.update(controls=backend.control,physics_steps=backend.physics,
                       native_result=backend.result,baseline_modules_loaded=False)
        (Path(directory)/'smoke_result.json').write_text(json.dumps(results,indent=2)+'\n')
        print('RUBIKS_NATIVE_SDK_SMOKE_OK',json.dumps(results),flush=True)
    finally:
        dispatcher.close(); server.close(); service.close()
