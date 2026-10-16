"""Content identity for native Rubik engineering evidence; no simulator imports."""
import hashlib
import json
from pathlib import Path


def rubiks_source_hashes(root):
    root=Path(root).resolve()
    prefixes=(
        'source/agentbench/agentbench/tasks/manager_based/table_top_manipulation/config/rubiks_cube',
        'source/agentbench/agentbench/robot_usds/Sharpa_hand',
        'source/agentbench_platform/agentbench_platform',
    )
    records={}
    for prefix in prefixes:
        directory=root/prefix
        if not directory.is_dir():raise ValueError('Missing source identity root: '+prefix)
        for path in sorted(directory.rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts:continue
            if path.suffix not in ('.py','.json','.usd','.usda','.usdc','.urdf','.stl','.obj','.dae'):continue
            records[str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()
    shared = root/'source/agentbench/agentbench/tasks/manager_based/table_top_manipulation/config'
    for path in sorted(shared.glob('tabletop_background*.py')):
        records[str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()
    if not records:raise ValueError('Empty source identity')
    return records


def source_identity_sha256(hashes):
    return hashlib.sha256(json.dumps(hashes,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
