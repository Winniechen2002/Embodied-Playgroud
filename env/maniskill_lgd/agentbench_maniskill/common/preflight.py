"""Fail on missing robot collision meshes before constructing a simulator."""
import xml.etree.ElementTree as ET
from pathlib import Path
from .paths import LEGACY,NATIVE_ROOT

def check_urdf(path):
    path=Path(path)
    if not path.is_file():raise FileNotFoundError(f'{path}: run python -m agentbench_maniskill assets first')
    meshes=list(ET.parse(path).iter('mesh'))
    missing=[]
    for mesh in meshes:
        raw=mesh.get('filename').removeprefix('package://');p=path.parent/raw
        if not p.is_file():missing.append(str(p))
    if missing:raise FileNotFoundError('Missing robot meshes: '+', '.join(sorted(set(missing))))
    return len(meshes)

def check_robot(uid):
    if uid=='panda':path=NATIVE_ROOT/'panda/panda_v2.urdf'
    elif uid=='fetch':path=NATIVE_ROOT/'fetch/fetch.urdf'
    else:
        folders=list((LEGACY/'robots').glob(f'{int(uid.split("_")[-1]):02d}_*'))
        if not folders:raise FileNotFoundError('Robot assets absent; run python -m agentbench_maniskill assets')
        path=folders[0]/'robot.urdf'
    return check_urdf(path)
