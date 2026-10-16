"""Optional adapter for owner-provisioned offline GraspNet inference on calibrated camera data."""
import base64
import hashlib
import json
from pathlib import Path
import sys

REVISION='280c215129f759ed8649cb4e89fc5dfee55f4f80'
SOURCE_SHA256='177849327fa21c7271df45421186706050e7fda80f02c8689c055a7c2113d1fc'
DOCKER_IMAGE='sha256:fb215244390a812ba2ed26a1c69851337edc5df2e400fdd3e1bde530d049e5f1'
CHECKPOINT_SHA256='60680087c61cba2b6791614fef1519071e294f6dcaf99b3f581bb95f7c51a868'


def backproject(rgb,depth,validity,intrinsics,pixel_center_offset,near,far):
    import numpy as np
    rgb=np.asarray(rgb);depth=np.asarray(depth);validity=np.asarray(validity);k=np.asarray(intrinsics,dtype=float);offset=np.asarray(pixel_center_offset,dtype=float)
    if (depth.ndim!=2 or validity.shape!=depth.shape or rgb.shape!=(*depth.shape,3) or k.shape!=(3,3)
            or not np.isfinite(k).all() or k[0,0]<=0 or k[1,1]<=0 or offset.shape!=(2,)
            or not np.isfinite(offset).all() or not 0<near<far or not np.allclose(k[2],[0,0,1])
            or k[0,1]!=0 or k[1,0]!=0):raise ValueError('Invalid camera geometry')
    v,u=np.nonzero((validity!=0)&np.isfinite(depth)&(depth>near)&(depth<far))
    z=depth[v,u].astype(np.float32)
    points=np.column_stack(((u+offset[0]-k[0,2])*z/k[0,0],(v+offset[1]-k[1,2])*z/k[1,1],z)).astype(np.float32)
    return points,rgb[v,u].astype(np.float32)/255.


def _hash(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _object(properties):return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)


def _array(items,n):return dict(type='array',items=items,minItems=n,maxItems=n)


def descriptor(manifest=None):
    number={'type':'number'};text={'type':'string'}
    hashes=_object({k:dict(type='string',minLength=64,maxLength=64) for k in ('rgb','depth','validity','calibration')})
    provenance=_object(dict(source_revision=text,source_sha256=text,checkpoint_sha256=text,input_sha256=text,resource_sha256=hashes))
    candidate=_object(dict(camera_from_grasp=_array(_array(number,4),4),width_m=dict(type='number',minimum=0,maximum=.1),score=dict(type='number',minimum=0,maximum=1)))
    calibration=_object(dict(intrinsics=_array(_array(number,3),3),world_from_camera=_array(_array(number,4),4),
        pixel_center_offset=_array(number,2),convention=text,near_m=number,far_m=number))
    output=_object(dict(candidates=dict(type='array',items=candidate,minItems=1,maxItems=128),
        capture_id=text,camera_id=text,capture_step=dict(type='integer',minimum=0),point_count=dict(type='integer',minimum=1),
        coordinate_contract=_object(dict(frame=text,convention=text,units=text)),calibration=calibration,provenance=provenance))
    result=dict(name='graspnet',version='1.0.0',description='Offline parallel-jaw grasp candidates. camera_from_grasp maps GraspNet local +X approach, +Y jaw separation, +Z height to camera; origin is decoded fp2_xyz sampled-cloud grasp center. No wrist transform, collision certification, Panda feasibility guarantee or actuation.',
        input_schema=_object(dict(capture_id=dict(type='string',minLength=1,maxLength=128))),output_schema=output,
        observation_profiles=['rgbd','privileged'],coordinate_contract=dict(frame='camera',convention='opencv_x_right_y_down_z_forward',units='m'),
        source=dict(revision=REVISION,sha256=SOURCE_SHA256),checkpoint=dict(sha256=CHECKPOINT_SHA256),resources=['rgb','depth','validity','calibration'])
    if manifest is not None:
        if manifest.get('kind')=='graspnet_cpu_container':
            result['version']='1.1.0-cpu'
            result['execution_contract']=dict(isolation='docker',offline=True,gpu=False,device='cpu',max_wall_seconds=90,
                max_output_bytes=262144,worker_sha256=manifest['worker_sha256'],image_sha256=manifest['image'].split(':')[1])
            return result
        result['execution_contract']=dict(isolation=manifest['isolation'],offline=True,gpu=True,max_wall_seconds=90,max_output_bytes=262144,worker_sha256=manifest['files'][manifest['worker']])
        if manifest['isolation']=='docker':result['execution_contract']['image_sha256']=manifest['image'].split(':')[1]
    return result


def result_contract(payload,candidates,*,point_count):
    c=payload['capture'];hashes={m:payload['resources'][m]['sha256'] for m in ('rgb','depth','validity')}
    hashes['calibration']=hashlib.sha256(json.dumps(c['calibration'],sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    input_hash=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    return dict(candidates=candidates,capture_id=c['capture_id'],camera_id=c['camera_id'],capture_step=c['capture_step'],point_count=point_count,
        coordinate_contract=descriptor()['coordinate_contract'],calibration=c['calibration'],
        provenance=dict(source_revision=REVISION,source_sha256=SOURCE_SHA256,checkpoint_sha256=CHECKPOINT_SHA256,input_sha256=input_hash,resource_sha256=hashes))


def validate_result(result,payload):
    import numpy as np
    expected=result_contract(payload,result['candidates'],point_count=result['point_count'])
    if result!=expected:raise ValueError('Mismatched tool provenance')
    for candidate in result['candidates']:
        pose=np.asarray(candidate['camera_from_grasp'],dtype=float)
        if (pose.shape!=(4,4) or not np.isfinite(pose).all() or not np.allclose(pose[3],[0,0,0,1],atol=1e-6)
                or not np.allclose(pose[:3,:3].T@pose[:3,:3],np.eye(3),atol=1e-4)
                or not np.isclose(np.linalg.det(pose[:3,:3]),1,atol=1e-4)
                or not 0<=candidate['width_m']<=.1 or not 0<=candidate['score']<=1):raise ValueError('Invalid grasp geometry')


def verify_source_members(source,files):
    for path in Path(source).rglob('*'):
        if path.suffix in ('.py','.so','.cpp','.cu','.h','.hpp') and (path.is_symlink() or str(path) not in files):
            raise ValueError('Unpinned source or extension member')



def verify_setup(path):
    try:
        manifest=json.loads(Path(path).read_text())
        if manifest.get('kind')=='graspnet_cpu_container':
            from .graspnet_cpu import verify_container_setup
            return verify_container_setup(path)
        if manifest['isolation'] not in ('docker','bwrap') or (manifest['isolation']=='docker' and manifest['image']!=DOCKER_IMAGE):raise ValueError('Isolation configuration changed')
        if manifest['version']!=1 or manifest['revision']!=REVISION or manifest['source_sha256']!=SOURCE_SHA256 or manifest['checkpoint_sha256']!=CHECKPOINT_SHA256:
            raise ValueError('Pinned manifest mismatch')
        if _hash(manifest['archive'])!=SOURCE_SHA256 or _hash(manifest['checkpoint'])!=CHECKPOINT_SHA256:raise ValueError('Asset digest mismatch')
        if not manifest['files'] or not Path(manifest['python']).is_file():raise ValueError('Missing runtime')
        verify_source_members(manifest['source'],manifest['files'])
        for path,digest in manifest['files'].items():
            if _hash(path)!=digest:raise ValueError('Installed asset changed')
        if str(Path(__file__).resolve())!=manifest['worker'] or _hash(__file__)!=manifest['files'][manifest['worker']]:raise ValueError('Worker changed')
        return manifest
    except Exception:raise ValueError('GraspNet assets unavailable or verification failed; provide a verified owner-provisioned setup manifest') from None


def sandbox_command(manifest,*,preflight=False):
    import shutil
    if sys.platform!='linux' or shutil.which('bwrap') is None:raise ValueError('GraspNet requires Linux bubblewrap isolation')
    command=['/usr/bin/bwrap','--die-with-parent','--new-session','--unshare-all','--clearenv','--proc','/proc','--dev','/dev','--tmpfs','/tmp']
    # Read-only runtime libraries, no host root/project/home mount. Keep venv paths
    # unchanged because pyvenv.cfg and extension loaders use their exact locations.
    for folder in ('/usr/lib','/usr/lib64',manifest['base_environment'],str(Path(manifest['python']).parent.parent)):
        if Path(folder).exists():command+=['--ro-bind',folder,folder]
    command+=['--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64']
    for path in ('/etc/ld.so.cache','/dev/nvidia0','/dev/nvidiactl','/dev/nvidia-uvm','/dev/nvidia-uvm-tools'):
        if Path(path).exists():command+=['--dev-bind' if path.startswith('/dev/') else '--ro-bind',path,path]
    for sub in ('models','utils','pointnet2','knn'):
        command+=['--ro-bind',str(Path(manifest['source'])/sub),'/source/'+sub]
    command+=['--ro-bind',manifest['checkpoint'],'/weights.tar',
        '--ro-bind',manifest['worker'],'/worker.py','--chdir','/tmp','--setenv','HOME','/tmp',
        '--setenv','PATH','/usr/bin:/bin','--setenv','OMP_NUM_THREADS','2',
        '--',manifest['python'],'-I','-B','-X','pycache_prefix=/tmp/pycache','/worker.py','--preflight' if preflight else '--worker','/source','/weights.tar']
    return command




def docker_create_command(manifest,*,preflight=False,engine=None):
    import os
    from .container_engine import ContainerEngine
    engine=engine or ContainerEngine()
    command=engine.command('create')+['--interactive',*engine.create_options(),'--network','none','--read-only',
        '--user',f'{os.getuid()}:{os.getgid()}','--cap-drop','ALL','--security-opt','no-new-privileges',
        *engine.resource_options(memory='3g'),*(['--runtime','runc'] if engine.kind=='docker' else []),
        '--tmpfs','/tmp:rw,nosuid,nodev,size=268435456,mode=1777',
        '--env','HOME=/tmp','--env','OMP_NUM_THREADS=2','--env','NVIDIA_DRIVER_CAPABILITIES=compute,utility',
        '--workdir','/tmp','--entrypoint',manifest['python']]
    for device in ('/dev/nvidia0','/dev/nvidiactl','/dev/nvidia-uvm','/dev/nvidia-uvm-tools'):
        command+=['--device',device+':'+device+':rwm']
    mounts=[('/usr/lib','/usr/lib'),('/usr/lib64','/usr/lib64'),
        (manifest['base_environment'],manifest['base_environment']),
        (str(Path(manifest['python']).parent.parent),str(Path(manifest['python']).parent.parent))]
    mounts += [(str(Path(manifest['source'])/sub),'/source/'+sub) for sub in ('models','utils','pointnet2','knn')]
    mounts += [(manifest['checkpoint'],'/weights.tar'),(manifest['worker'],'/worker.py')]
    for source,target in mounts:
        if ',' in source or ',' in target:raise ValueError('Invalid worker mount')
        command+=['--mount',f'type=bind,src={source},dst={target},readonly']
    command += [manifest['image'],'-I','-B','-X','pycache_prefix=/tmp/pycache','/worker.py','--preflight' if preflight else '--worker','/source','/weights.tar']
    return command


def make_worker(manifest,*,private_directory,preflight=False,engine=None):
    from .plugins import DockerWorker,ProcessWorker
    if manifest.get('kind')=='graspnet_cpu_container':
        from .container_engine import ContainerEngine
        from .graspnet_cpu import container_create_command
        engine=engine or ContainerEngine()
        return DockerWorker(container_create_command(manifest,preflight=preflight,engine=engine),engine=engine,
            private_directory=private_directory,timeout_seconds=90)
    if manifest['isolation']=='docker':
        return DockerWorker(docker_create_command(manifest,preflight=preflight,engine=engine),engine=engine,private_directory=private_directory,timeout_seconds=30 if preflight else 90)
    return ProcessWorker(sandbox_command(manifest,preflight=preflight),private_directory=private_directory,timeout_seconds=30 if preflight else 90)


def registry_from_setup(path,*,resources,observation,granted,private_directory,registry=None,engine=None):
    from .plugins import ToolRegistry
    manifest=verify_setup(path)
    preflight=make_worker(manifest,private_directory=private_directory,preflight=True,engine=engine)({})
    if manifest.get('kind')=='graspnet_cpu_container':
        if (preflight.get('device')!='cpu' or preflight.get('cuda_initialized') is not False
                or preflight.get('image_manifest_sha256')!=manifest['image_manifest_sha256']):
            raise ValueError('GraspNet CPU worker preflight does not match frozen image')
    worker=make_worker(manifest,private_directory=private_directory,engine=engine)
    registry=registry or ToolRegistry(resources=resources,observation=observation,granted=granted)
    contract=descriptor(manifest)
    if manifest['isolation']=='docker' and engine is not None:contract['execution_contract']['isolation']=engine.kind
    registry.register(contract,worker,result_validator=validate_result)
    return registry


def inference(payload,source,checkpoint,*,device='cuda'):
    if device not in ('cpu','cuda'):raise ValueError('Unsupported GraspNet device')
    import numpy as np
    import torch
    if _hash(checkpoint)!=CHECKPOINT_SHA256:raise ValueError('Checkpoint mismatch')
    if device=='cpu':
        from .graspnet_cpu_ops import install_extension
        install_extension();torch.set_num_threads(2)
    for sub in ('models','utils','pointnet2','knn'):sys.path.insert(0,str(Path(source)/sub))
    from graspnet import GraspNet,pred_decode
    if device=='cuda' and not torch.cuda.is_available():raise ValueError('CUDA unavailable')
    c=payload['capture'];height,width=c['height'],c['width']
    arrays={}
    for m,dtype,shape in (('rgb',np.uint8,(height,width,3)),('depth','<f4',(height,width)),('validity',np.uint8,(height,width))):
        r=payload['resources'][m];data=base64.b64decode(r['data_base64'],validate=True)
        if hashlib.sha256(data).hexdigest()!=r['sha256'] or r['capture_step']!=c['capture_step']:raise ValueError('Capture resource mismatch')
        arrays[m]=np.frombuffer(data,dtype=dtype).reshape(shape)
    calibration=c['calibration']
    points,colors=backproject(arrays['rgb'],arrays['depth'],arrays['validity'],calibration['intrinsics'],calibration['pixel_center_offset'],calibration['near_m'],calibration['far_m'])
    if not len(points):raise ValueError('No valid depth points')
    rng=np.random.default_rng(0);indices=rng.choice(len(points),20000,replace=len(points)<20000)
    model=GraspNet(input_feature_dim=0,num_view=300,num_angle=12,num_depth=4,cylinder_radius=.05,hmin=-.02,hmax_list=[.01,.02,.03,.04],is_training=False).to(device)
    state=torch.load(checkpoint,weights_only=True,map_location='cpu');model.load_state_dict(state['model_state_dict'],strict=True);model.eval()
    torch.manual_seed(0)
    with torch.inference_mode():decoded=pred_decode(model({'point_clouds':torch.from_numpy(points[indices][None]).to(device)}))[0].detach().cpu().numpy()
    if decoded.ndim!=2 or decoded.shape[1]!=17 or not np.isfinite(decoded).all():raise ValueError('Malformed model candidates')
    candidates=[]
    for item in decoded[np.argsort(-decoded[:,0],kind='stable')]:
        if not 0<=float(item[0])<=1 or not 0<=float(item[1])<=.1:continue
        pose=np.eye(4);pose[:3,:3]=item[4:13].reshape(3,3);pose[:3,3]=item[13:16]
        candidates.append(dict(camera_from_grasp=pose.tolist(),width_m=float(item[1]),score=float(item[0])))
        if len(candidates)==128:break
    if not candidates:raise ValueError('No valid candidates')
    return result_contract(payload,candidates,point_count=len(points))


if __name__=='__main__':
    if len(sys.argv)==4 and sys.argv[1]=='--preflight':
        import torch
        for sub in ('models','utils','pointnet2','knn'):sys.path.insert(0,str(Path(sys.argv[2])/sub))
        from graspnet import GraspNet,pred_decode
        if not torch.cuda.is_available():raise ValueError('CUDA unavailable')
        torch.empty(1,device='cuda')
        import os,socket
        assert os.getuid()!=0
        assert not Path('/var/run/docker.sock').exists()
        # Worker containers receive only their declared model and request mounts.
        # Check conventional private mount locations without host-specific paths.
        for private_path in ('/workspace', '/baselines', '/run/secrets'):
            assert not Path(private_path).exists()
        try:
            socket.create_connection(('1.1.1.1',443),timeout=.5)
        except OSError:pass
        else:raise ValueError('Unexpected network access')
        try:Path('/worker.py').write_text('mutation')
        except OSError:pass
        else:raise ValueError('Writable worker mount')
        assert not any(k in os.environ for k in ('OPENAI_API_KEY','CUDA_VISIBLE_DEVICES','CODEX_HOME'))
        print(json.dumps(dict(torch=torch.__version__,cuda=torch.version.cuda,gpu=torch.cuda.get_device_name(0),boundary_probes='nonroot/read-only/private paths/socket/network/env denied')))
    elif len(sys.argv)==4 and sys.argv[1]=='--worker':
        payload=json.load(sys.stdin);result=inference(payload,sys.argv[2],sys.argv[3]);validate_result(result,payload)
        print(json.dumps(result,allow_nan=False,separators=(',',':')))
    else:raise SystemExit('This module is an optional isolated worker; provision it through the owner tool interface.')
