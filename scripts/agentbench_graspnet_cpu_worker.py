#!/usr/bin/env python3
"""Image-local CPU inference entrypoint; receives only bound RGB-D on stdin."""
import json
from pathlib import Path
import sys


def main():
    root=Path(__file__).resolve().parent
    sys.path.insert(0,str(root))
    from agentbench_platform.graspnet import inference,validate_result,CHECKPOINT_SHA256
    from agentbench_platform.graspnet_cpu import digest
    metadata=json.loads((root/'image-manifest.json').read_text())
    for name,sha in metadata['files'].items():
        if digest(root/name)!=sha:raise ValueError('Frozen image member changed')
    checkpoint=Path('/weights.tar')
    if digest(checkpoint)!=CHECKPOINT_SHA256:raise ValueError('Checkpoint mismatch')
    if sys.argv[1:]==['--preflight']:
        import os,socket,torch
        from agentbench_platform.graspnet_cpu_ops import install_extension
        install_extension();torch.set_num_threads(2)
        for sub in ('models','utils','pointnet2','knn'):sys.path.insert(0,str(root/'source'/sub))
        from graspnet import GraspNet
        model=GraspNet(input_feature_dim=0,num_view=300,num_angle=12,num_depth=4,cylinder_radius=.05,
            hmin=-.02,hmax_list=[.01,.02,.03,.04],is_training=False).cpu().eval()
        model.load_state_dict(torch.load(checkpoint,weights_only=True,map_location='cpu')['model_state_dict'],strict=True)
        if os.getuid()==0 or torch.cuda.is_initialized():raise ValueError('Unexpected runtime identity/device')
        if any(Path('/dev').glob('nvidia*')):raise ValueError('Unexpected GPU access')
        try:socket.create_connection(('1.1.1.1',443),timeout=.5)
        except OSError:pass
        else:raise ValueError('Unexpected network access')
        try:(root/'readonly-probe').write_text('probe')
        except OSError:pass
        else:raise ValueError('Writable image')
        print(json.dumps(dict(device='cpu',cuda_initialized=False,torch=torch.__version__,
            image_manifest_sha256=digest(root/'image-manifest.json'))))
    elif sys.argv[1:]==['--worker']:
        payload=json.load(sys.stdin)
        result=inference(payload,root/'source',checkpoint,device='cpu');validate_result(result,payload)
        print(json.dumps(result,allow_nan=False,separators=(',',':')))
    else:raise SystemExit('Expected --preflight or --worker')


if __name__=='__main__':main()
