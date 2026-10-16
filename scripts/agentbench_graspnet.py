#!/usr/bin/env python3
"""Maintainer offline setup, doctor and prior-native-fixture acceptance command."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"source/agentbench_platform"))
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=('prepare','doctor','native-fixture'))
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--isolation',choices=('bwrap','docker'),default='bwrap')
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--fixture',type=Path)
    parser.add_argument('--output',type=Path)
    from agentbench_platform.container_engine import add_container_arguments,engine_from_args
    add_container_arguments(parser)
    args=parser.parse_args()
    engine=engine_from_args(args)
    from agentbench_platform.graspnet import freeze_setup,verify_setup,registry_from_setup
    from agentbench_platform.resources import ResourceStore
    if args.command=='prepare':
        manifest=freeze_setup(args.root,args.manifest,isolation=args.isolation)
        print(json.dumps(dict(manifest=str(args.manifest),source_revision=manifest['revision'],files=len(manifest['files']))));return
    manifest=verify_setup(args.manifest)
    if args.command=='doctor':
        from agentbench_platform.graspnet import make_worker
        if args.output is None:parser.error('doctor needs private --output')
        result=make_worker(manifest,private_directory=args.output,preflight=True,engine=engine)({})
        print(json.dumps(dict(ready=True,runtime=result,manifest_sha256=hashlib.sha256(args.manifest.read_bytes()).hexdigest())));return
    if args.fixture is None or args.output is None:parser.error('native-fixture needs trusted --fixture and private --output')
    import numpy as np
    # This maintainer path is never accepted by the public registry/protocol.
    args.output.mkdir(mode=0o700,parents=True,exist_ok=False)
    with np.load(args.fixture,allow_pickle=False) as data:
        expected={'rgb','depth','validity','intrinsics','world_from_camera','pixel_center_offset','capture_step','capture_id'}
        if set(data.files)!=expected:raise ValueError('Fixture contains non-observation fields')
        content={key:hashlib.sha256(data[key].tobytes()).hexdigest() for key in sorted(data.files)}
        store=ResourceStore()
        row=store.register_capture(camera_id=args.fixture.stem,capture_step=int(data['capture_step']),
            rgb=np.asarray(data['rgb'],dtype=np.uint8).tobytes(),depth=np.asarray(data['depth'],dtype='<f4').tobytes(),validity=np.asarray(data['validity'],dtype=np.uint8).tobytes(),
            calibration=dict(intrinsics=data['intrinsics'].tolist(),world_from_camera=data['world_from_camera'].tolist(),
                pixel_center_offset=data['pixel_center_offset'].tolist(),near_m=.01,far_m=10,convention='opencv_x_right_y_down_z_forward'))
        original_capture=str(data['capture_id'])
    registry=registry_from_setup(args.manifest,resources=store,observation='rgbd',granted=('graspnet',),private_directory=args.output/'worker',engine=engine)
    start=time.monotonic();result=registry.call('graspnet',{'capture_id':row['capture_id']})
    (args.output/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    evidence=dict(input_kind='prior trusted native RGB-D fixture, not fresh live capture',fixture=str(args.fixture.resolve()),
        fixture_sha256=hashlib.sha256(args.fixture.read_bytes()).hexdigest(),fixture_content_sha256=content,fixture_capture_id=original_capture,
        bound_capture_id=row['capture_id'],source_run=args.fixture.parent.parent.name,manifest_sha256=hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
        candidate_count=len(result['candidates']),elapsed_seconds=time.monotonic()-start,provenance=result['provenance'])
    (args.output/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence))


if __name__=='__main__':main()
