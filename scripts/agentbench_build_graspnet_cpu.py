#!/usr/bin/env python3
"""Build the isolated CPU worker using pinned source and offline CPU wheels."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"source/agentbench_platform"))
import re
from agentbench_platform.container_engine import add_container_arguments,engine_from_args
from agentbench_platform.image_build import build_image
from agentbench_platform.graspnet_cpu import export_container_context,freeze_container_setup


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-image',required=True,help='Official python@sha256: digest, Python 3.11')
    parser.add_argument('--source-archive',type=Path,required=True)
    parser.add_argument('--checkpoint',type=Path,required=True)
    parser.add_argument('--wheelhouse',type=Path,required=True)
    parser.add_argument('--requirements',type=Path,required=True,help='Fully pinned CPU Torch 2.5.1 / NumPy 1.26.4 --require-hashes lock')
    parser.add_argument('--output',type=Path,required=True)
    add_container_arguments(parser);args=parser.parse_args();engine=engine_from_args(args)
    if not re.fullmatch('python@sha256:[0-9a-f]{64}',args.base_image):parser.error('Immutable official Python base required')
    args.output.mkdir(mode=0o700,parents=True,exist_ok=False)
    context=args.output/'context'
    files=export_container_context(Path(__file__).resolve().parents[1],context,args.source_archive,args.wheelhouse,args.requirements)
    (args.output/'inputs.json').write_text(json.dumps(dict(base_image=args.base_image,files=files,engine=engine.manifest()),indent=2)+'\n')
    build_image(engine=engine,context=context,output=args.output,base_image=args.base_image,
        entrypoint=['/usr/local/bin/python3','-I','-B','/opt/worker/worker.py'])
    manifest=freeze_container_setup(args.checkpoint,(args.output/'image.id').read_text().strip(),context,args.output/'tool.json')
    print(json.dumps(manifest))


if __name__=='__main__':main()
