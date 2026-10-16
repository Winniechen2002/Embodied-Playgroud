"""Environment-only release inventory. Never imports Isaac or experiment results."""
from collections import Counter
import hashlib
import importlib
import json
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[3]
CONFIG = ROOT / 'source/agentbench/agentbench/tasks/manager_based/table_top_manipulation/config'
VERSION = 'environment-catalog-v3'
EXPECTED = {'marble':100, 'hanoi_panda':40, 'hanoi_sharpa':40, 'hanoi_floating':40,
            'pocket_cube':20, 'rubiks_panda':30, 'rubiks_sharpa':30, 'kongming_lock':60, 'bookshelf':20,
            'maniskill_long_horizon':10, 'maniskill_geometry':10, 'maniskill_dynamics':10}


def source_module(package, directory, module):
    """Import pure authoring data without the simulator-heavy parent __init__."""
    if package not in sys.modules:
        obj = types.ModuleType(package)
        obj.__path__ = [str(directory)]
        sys.modules[package] = obj
    return importlib.import_module(package + '.' + module)


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,allow_nan=False,
        separators=(',',':')).encode()).hexdigest()


def catalog(*, _native_records=None):
    from .kongming_cases import CASES as locks, describe_case_spec
    from .rubiks_cases import PUBLIC_MANIFEST as cubes
    hanoi = source_module('_release_hanoi',ROOT/'source/agentbench/agentbench_hanoi40','catalog')
    pocket = source_module('_release_pocket',ROOT/'source/agentbench/agentbench_cube20','catalog')
    birds = source_module('_release_marble',ROOT/'source/agentbench/agentbench_mujoco','campaign_scene')
    # Tensor-free clients consume a source-bound projection, never import torch
    # merely to discover a MuJoCo environment.
    books = json.loads(Path(__file__).with_name('bookshelf_catalog.json').read_text())
    for name,expected in books['sources'].items():
        actual=hashlib.sha256((CONFIG/'organize_bookshelf'/name).read_bytes()).hexdigest()
        if actual!=expected:raise ValueError('Bookshelf catalog projection is stale: '+name)
    rows=[]
    def add(family,case,robot,difficulty,goal,action_size,source,configuration,**extra):
        ident=f'{family}/{robot}/{case}'
        row=dict(id=ident,family=family,case_id=case,embodiment=robot,
            backend='maniskill' if family.startswith('maniskill_') else 'mujoco' if family=='marble' else 'isaac',difficulty=difficulty,
            goal=goal,action_spec=dict(size=action_size),
            observations=dict(public=['rgb','proprioception','declared_task_metadata'],privileged='explicit Level 3 fields only'),
            termination=['goal_and_stability','physical_violation','time_limit','owner_finish'],
            capability_levels=[0,1,2,3],contract_source='docs/evaluation/tasks.json#'+ident,
            authoring_source=source,
            evaluation_protocol=dict(version='environment-four-trial-v2',trials_per_group=4,
                specification='docs/evaluation/tasks.json',task_key=ident),
            configuration_sha256=digest([robot,configuration]),validation_seeds=[0,1,2],
            asset_manifest='docs/environment_assets.en.md',
            launch=['python','scripts/environment_runtime.py','--task-id',ident,'--capability-level','0'],
            acceptance=['python','scripts/environment_smoke.py','--task-id',ident,'--output','environment-probe.json'],
            release_gate=['python','scripts/environment_release.py','check','--output','environment-check.json'],**extra)
        from .environment_contracts import contract
        if _native_records is not None and not _native_records:
            # Private native measurement bootstrap: no qualified action contract.
            rows.append(row)
            return
        if not (ROOT/source).is_file():raise ValueError('Missing authoring source: '+source)
        row['contract']=contract(row,configuration,_native_records=_native_records)
        row['action_spec']=row['contract']['action_spec']
        row['contract_source']='docs/evaluation/tasks.json#'+ident
        row['asset_manifest']='docs/environment_assets.en.md'
        rows.append(row)
    for i,(name,cfg) in enumerate(birds.SCENARIOS.items(),1):
        physical={k:v for k,v in cfg.items() if k not in ('plan','yaw_plan','reference')}
        protected=list(cfg.get('protected',[]))
        required=[j for j in range(len(cfg['targets'])) if j not in protected]
        goal=(cfg.get('description',cfg['title'])+
              f' Target indices are zero-based. Required targets: {required}; protected targets: {protected};'
              f' required order: {cfg.get("target_order",[])} (empty means unrestricted);'
              f' minimum toppled structures: {cfg.get("min_toppled",0)}.'+
              (f' Allowed damage sources: {cfg["damage_sources"]}.' if 'damage_sources' in cfg else '')+
              (f' Required fractures: {cfg["fracture_required"]}.' if 'fracture_required' in cfg else ''))
        add('marble',f'A{i:03d}','dual-panda',cfg['tier'],goal,16,
            'source/agentbench/agentbench_mujoco/campaign_scene.py',physical,scenario=name,
            randomization=dict(modes=['loaded','ground'],spring_stiffness_N_m=[22,24,26,28]),
            physical_model='mujoco-rigid-fracture',
            full_horizon_stability=any(not o.get('fixed',False) for o in physical.get('obstacles',[])),
            episode_time_limit_seconds=150.)
    for family,robot,size in [('hanoi_panda','panda',8),
            ('hanoi_sharpa','fr3-sharpa',29),
            ('hanoi_floating','floating-sharpa',28)]:
        for task in hanoi.TASKS:
            add(family,task.id,robot,task.level,dict(ring_pegs=list(task.goal),stable_seconds=1),size,
                'source/agentbench/agentbench_hanoi40/catalog.py',task.record(),
                randomization=dict(splits=['nominal','train','heldout']),
                physical_model='contact-only-hanoi',full_horizon_stability=True)
    for task in pocket.TASKS:
        for robot,size in [('aloha',16),('dual-sharpa',56)]:
            add('pocket_cube',task.id,robot,task.difficulty,
                dict(state=list(task.goal.as_vector()),stable_seconds=1),size,
                'source/agentbench/agentbench_cube20/catalog.py',task.record(),randomization=dict(splits=['nominal','train','heldout']),
                physical_model='switchable-carrier-pocket-cube',full_horizon_stability=True)
    for family,robot,size in [('rubiks_panda','panda',8),('rubiks_sharpa','floating-sharpa',28)]:
        for case in cubes['cases']:
            add(family,case['case_id'],robot,case['difficulty'],'Restore uniform face colors and return home.',size,
                'source/agentbench_platform/agentbench_platform/rubiks_cases.py',case,randomization=dict(catalog='rubiks-public-cases-v1'),
                physical_model='hybrid_fixture_v1',
                full_horizon_stability=True)
    for case in locks:
        add('kongming_lock',case['case_id'],'dual-panda',case['difficulty'],describe_case_spec(case),16,
            'source/agentbench_platform/agentbench_platform/kongming_cases.py',case,mode=case['task'],
            randomization=dict(catalog='kongming-public-cases-v1'),physical_model='shape_v1.5',full_horizon_stability=True)
    for case in locks:
        add('kongming_lock',case['case_id'],'dual-floating-sharpa',case['difficulty'],describe_case_spec(case),56,
            'source/agentbench_platform/agentbench_platform/kongming_cases.py',case,mode=case['task'],
            randomization=dict(catalog='kongming-public-cases-v1'),physical_model='shape_v1.5',full_horizon_stability=True)
    for suite in ('long_horizon','geometry_dynamics'):
        path=ROOT/'env/maniskill_lgd/agentbench_maniskill'/suite/'tasks.json'
        for task in json.loads(path.read_text()):
            category=1 if suite=='long_horizon' else task['category']
            family={1:'maniskill_long_horizon',2:'maniskill_geometry',3:'maniskill_dynamics'}[category]
            add(family,task['code'],task['robot']['uid'],task.get('difficulty','authored'),
                dict(instruction=task.get('instruction',task['title']),final=task['final'],milestones=task['milestones']),
                None,str(path.relative_to(ROOT)),task,suite=suite,
                randomization=dict(physical_layout='fixed',formal_physics_variant=0,
                    engineering_physics_variants=list(range(len(task.get('physics_variants',[])) or 1))),
                physical_model='sapien-rigid-articulated',full_horizon_stability=category!=3,
                physics_acceptance='expected_dynamics' if category==3 else 'static_stability')
    for variant in books['variants']:
        add('bookshelf',variant['id'],'dual-panda',variant['level'],variant['goal'],16,
            str((CONFIG/'organize_bookshelf/catalog.py').relative_to(ROOT)),variant['record'],gym_id=variant['gym_id'],
            randomization=dict(seeds=[0,1,2,3]),physical_model='dual-panda-bookshelf-v1',full_horizon_stability=True)
    counts=dict(Counter(r['family'] for r in rows))
    if counts != EXPECTED or len({r['id'] for r in rows}) != 410:
        raise ValueError(f'Unexpected release inventory: {counts}')
    return dict(version=VERSION,count=len(rows),counts=counts,tasks=rows)


def find_task(task_id):
    for task in catalog()['tasks']:
        if task['id']==task_id:return task
    raise ValueError('Unknown release task ID')
