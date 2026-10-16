"""Maintainer native integration probe, explicitly not a task solve."""
import base64
import json
from pathlib import Path
import sys
import threading

import numpy as np


def run_smoke(backend,env,resources,directory,socket_path,*,journal_path=None,storage_guard=None,profile=None):
    from PIL import Image
    from agentbench_sdk import Client
    from .native_backend import MainThreadDispatcher,DispatchedBackend
    from .profiles import RunProfile
    from .protocol import ProtocolService,ProtocolServer
    dispatcher=MainThreadDispatcher()
    service=ProtocolService(DispatchedBackend(backend,dispatcher),token='native-smoke',profile=RunProfile(observation='rgbd'),
        journal_path=journal_path or Path(directory)/'private/requests.sqlite',resources=resources,storage_guard=storage_guard)
    server=ProtocolServer(socket_path,service);server.start()
    results={};errors=[]
    render_calls=[]
    original_render=env.sim.render
    def tracked_render(*args,**kwargs):
        render_calls.append((backend.control,backend.physics,float(env.sim.current_time)))
        return original_render(*args,**kwargs)
    env.sim.render=tracked_render
    def client_work():
        try:
            client=Client(str(server.socket_path),'native-smoke',timeout=120.)
            description=client.describe();initial=client.observe()
            assert initial['step_index']==0 and not initial['terminated']
            action_size=description['action_spec']['size']
            if action_size == 16:
                hold=[0.]*16;hold[7]=hold[15]=1.
            elif action_size == 56:
                hold=[]
                for side in ('left','right'):
                    robot=description['robots'][side+'_floating_sharpa']
                    for name in description['action_spec']['names'][len(hold):len(hold)+28]:
                        hold.append(robot['default_joint_positions'][robot['joint_names'].index(name.split('.',2)[2])])
            else:
                hold=[0.]*action_size
            first=client.step(hold,request_id='native-smoke-first-action')
            if action_size == 56:
                from agentbench_sdk.client import ProtocolError
                assert client.step(hold,request_id='native-smoke-first-action') == first
                try:
                    client.step(hold[:-1])
                except ProtocolError:
                    pass
                else:
                    raise AssertionError('Invalid 55-D action accepted')
                assert client.observe()['step_index'] == 1
                assert client.describe() == description
            step=first['observation']
            assert step['step_index']==1 and not step['terminated']
            action=hold[:];action[0]=.002
            step=client.step(action)['observation']
            assert step['step_index']==2 and not step['terminated']
            assert not render_calls, 'Control steps must not implicitly render cameras'
            capture=client.observe(camera_ids=['front_left','front_right','top'])
            again=client.observe(camera_ids=['top'])
            assert capture['simulation_time_s']==again['simulation_time_s']==2/30
            assert capture['robots']==again['robots']
            assert 'privileged' not in capture
            geometry={}
            for name,view in capture['cameras'].items():
                def fetch(key,dtype,shape):
                    raw=client.get_resource(view[key])
                    return np.frombuffer(base64.b64decode(raw['data_base64']),dtype=dtype).reshape(shape)
                rgb=fetch('rgb_resource_id',np.uint8,(480,640,3))
                depth=fetch('depth_resource_id','<f4',(480,640))
                mask=fetch('validity_resource_id',np.uint8,(480,640)).astype(bool)
                assert mask.sum()>1000 and np.isfinite(depth).all() and rgb.std()>1
                Image.fromarray(rgb).save(Path(directory)/(name+'.png'))
                k=np.asarray(view['calibration']['intrinsics']);w=np.asarray(view['calibration']['world_from_camera'])
                y,x=np.indices(depth.shape)
                offset=view['calibration']['pixel_center_offset']
                rays=np.stack(((x+offset[0]-k[0,2])/k[0,0],(y+offset[1]-k[1,2])/k[1,1],np.ones_like(x)),axis=-1)
                world=(rays*depth[...,None])@w[:3,:3].T+w[:3,3]
                # Known native tabletop plane at z=.60, with finite table XY extent.
                table=mask & (abs(world[...,2]-.60)<.003) & (world[...,0]>-.125)&(world[...,0]<1.525)&(abs(world[...,1])<.775)
                assert table.sum()>1000,(name,int(table.sum()))
                assert np.quantile(abs(world[...,2][table]-.60),.95)<.0001
                np.savez_compressed(Path(directory)/(name+'.npz'),rgb=rgb,depth=depth,validity=mask,
                    intrinsics=k,world_from_camera=w,pixel_center_offset=offset,capture_step=view['capture_step'],capture_id=view['capture_id'])
                geometry[name]=dict(valid_pixels=int(mask.sum()),table_plane_pixels=int(table.sum()),
                    table_z_median=float(np.median(world[...,2][table])),
                    table_z_error_p95=float(np.quantile(abs(world[...,2][table]-.60),.95)),pixel_center_offset=offset,K=k.tolist(),world_from_camera=w.tolist())
            client.finish()
            results.update(success=True,kind='native backend smoke, not full solve',geometry=geometry,
                controls=2,physics_steps=8,render_nonadvancing=True)
            if action_size == 56:
                results.update(duplicate_action_replayed=True,invalid_action_rejected=True,reads_nonadvancing=True)
        except BaseException as exc:errors.append(exc)
    thread=threading.Thread(target=client_work);thread.start()
    try:
        while thread.is_alive():dispatcher.pump(timeout=.05)
        thread.join()
        if errors:raise errors[0]
        assert backend.physics==8 and backend.result['audit_coverage']['complete']
        assert not any(n=='baselines' or n.startswith('baselines.') for n in sys.modules)
        results['audit_coverage']=backend.result['audit_coverage']
        results['render_calls']=render_calls
        assert len(render_calls)==4
        results['baseline_modules_loaded']=False
        (Path(directory)/'smoke_result.json').write_text(json.dumps(results,indent=2)+'\n')
        print('NATIVE_BACKEND_SMOKE_OK',json.dumps(results),flush=True)
    finally:
        env.sim.render=original_render
        dispatcher.close();server.close();service.close()
