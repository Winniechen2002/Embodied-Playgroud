#!/usr/bin/env python3
"""Prepare frozen cube-solver tables, or run one submitted-facelet-only request."""
import argparse
import contextlib
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import time


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache',type=Path,required=True,help='Maintainer-owned frozen cache, never an agent argument')
    parser.add_argument('--prepare',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    sys.path[:0]=[str(root/'source/agentbench'),str(root/'source/agentbench_platform')]
    from agentbench_platform.cube_solver import check_facelets,solver_colors,frozen_table_loader,validate_solution
    import cube_solver
    from cube_solver import Cube,Kociemba
    from cube_solver.solver import utils
    if importlib.metadata.version('cube-solver')!='1.1.4':raise ValueError('cube-solver==1.1.4 required')
    cache=args.cache.resolve()
    if args.prepare:cache.mkdir(mode=0o700,parents=True,exist_ok=True)
    if not cache.is_dir():raise ValueError('Prepare fixed solver tables before the episode')
    os.chdir(cache)
    setup=cache/'setup.json'
    library=Path(cube_solver.__file__).parent
    source={str(p.relative_to(library)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(library.rglob('*.py'))}
    source['worker']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    from agentbench_platform.cube_rules import load_rules
    source['rules_loader']=hashlib.sha256((root/'source/agentbench_platform/agentbench_platform/cube_rules.py').read_bytes()).hexdigest()
    source['rules']=hashlib.sha256(Path(load_rules().__file__).read_bytes()).hexdigest()
    source['adapter']=hashlib.sha256((root/'source/agentbench_platform/agentbench_platform/cube_solver.py').read_bytes()).hexdigest()
    if args.prepare:
        import fcntl
        with (cache/'prepare.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            if setup.exists():raise FileExistsError('Frozen solver setup already exists; use a new cache version')
            with contextlib.redirect_stdout(sys.stderr):Kociemba()
            tables={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((cache/'tables').glob('*.npz'))}
            if not tables:raise RuntimeError('Solver preparation produced no tables')
            payload=dict(version=1,solver_version='1.1.4',source=source,tables=tables)
            setup.write_text(json.dumps(payload,sort_keys=True,indent=2)+'\n')
        print(json.dumps(dict(prepared=True,setup=str(setup),tables=len(tables))))
        return
    frozen=json.loads(setup.read_text())
    if frozen['solver_version']!='1.1.4' or frozen['source']!=source:
        raise ValueError('Solver implementation differs from frozen setup')
    utils.get_tables=frozen_table_loader(cache,frozen['tables'])
    payload=json.load(sys.stdin)
    if set(payload)!={'arguments'} or set(payload['arguments'])!={'facelets_urfdlb'}:
        raise ValueError('Only submitted facelets are accepted')
    facelets=check_facelets(payload['arguments']['facelets_urfdlb'])
    with contextlib.redirect_stdout(sys.stderr):
        cube=Cube(repr=solver_colors(facelets))
        cube.coords
        if cube.permutation_parity is None:raise ValueError('Invalid cube state')
        solver=Kociemba()
        started=time.monotonic()
        solution=solver.solve(cube,optimal=True,max_length=30,timeout=10)
    if solution is None:raise ValueError('No symbolic solution in the fixed search budget')
    result=dict(solution=str(solution).split(),version='1.1.4',search_timed_out=bool(solver.terminated),
                search_wall_s=time.monotonic()-started)
    validate_solution(result,payload)
    print(json.dumps(result,allow_nan=False))


if __name__=='__main__':main()
