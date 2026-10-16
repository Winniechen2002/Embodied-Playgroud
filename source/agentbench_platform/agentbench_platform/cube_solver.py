"""Facelet-only symbolic solver contract, frozen tables and independent replay."""
import hashlib
from pathlib import Path


SOLVED=''.join(face*9 for face in 'URFDLB')


def check_facelets(value):
    if (not isinstance(value,str) or len(value)!=54 or set(value)!=set('URFDLB')
            or any(value.count(face)!=9 or value[9*i+4]!=face for i,face in enumerate('URFDLB'))):
        raise ValueError('Invalid URFDLB facelets')
    return value


def solver_colors(facelets):
    check_facelets(facelets)
    colors=str.maketrans(dict(zip('URFDLB','WRGYOB')))
    return ''.join(facelets[9*'URFDLB'.index(face):9*('URFDLB'.index(face)+1)] for face in 'ULFRBD').translate(colors)


def validate_solution(result,payload):
    from .cube_rules import load_rules
    facelets=check_facelets(payload['arguments']['facelets_urfdlb'])
    rules=load_rules()
    if result['version']!='1.1.4':raise ValueError('Unexpected solver version')
    atomic=rules.parse_sequence(result['solution'])
    inverse=tuple(move[0] if move.endswith('-prime') else move[0]+'-prime' for move in reversed(atomic))
    # Construct the unique state solved by this solution using independent cube
    # mathematics. No worker state, scramble history or environment is read.
    if rules.CubeState.solved().apply_sequence(inverse).facelet_string()!=facelets:
        raise ValueError('Symbolic solution failed independent replay')


def descriptor(source_hash,table_hash):
    return dict(name='cube_solver',version='1.1.4',description='Solve only the 54 submitted URFDLB facelets; returns symbolic moves.',
        input_binding='submitted_arguments',
        input_schema=dict(type='object',properties={'facelets_urfdlb':dict(type='string',minLength=54,maxLength=54)},
                          required=['facelets_urfdlb'],additionalProperties=False),
        output_schema=dict(type='object',properties={
            'solution':dict(type='array',items=dict(type='string',enum=[f+s for f in 'URFDLB' for s in ('',"'",'2')]),maxItems=30),
            'version':dict(type='string',enum=['1.1.4']), 'search_timed_out':dict(type='boolean'),
            'search_wall_s':dict(type='number',minimum=0)},
            required=['solution','version','search_timed_out','search_wall_s'],additionalProperties=False),
        observation_profiles=['rgb','rgbd','privileged'],resources=[],
        coordinate_contract=dict(frame='logical_cube',convention='URFDLB row-major faces; Singmaster moves',units='quarter turns'),
        source=dict(sha256=source_hash),checkpoint=dict(sha256=table_hash),
        execution_contract=dict(isolation='process',offline=True,gpu=False,max_wall_seconds=60,max_output_bytes=8192))


def frozen_table_loader(cache,tables):
    """Replacement for cube-solver's cache-or-generate function during episodes."""
    import numpy as np
    root=Path(cache).resolve()/'tables'

    def read(filename,definitions,generate_table_fn,accumulate=False):
        if not isinstance(filename,str) or Path(filename).name!=filename or filename not in tables:
            raise ValueError('Unfrozen solver table requested')
        path=root/filename
        if path.is_symlink() or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=tables[filename]:
            raise ValueError('Solver table missing or changed')
        with np.load(path,allow_pickle=False) as data:
            required={item.name for item in definitions}
            if not required<=set(data.files):raise ValueError('Incomplete frozen solver tables')
            return {name:data[name] for name in (data.files if accumulate else required)}

    return read


def _digest(path):
    path=Path(path)
    if path.is_symlink() or not path.is_file():raise ValueError('Missing or linked solver input')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _frozen_cache(cache):
    import json,re
    root=Path(cache)
    if not root.is_absolute() or root.is_symlink() or not root.is_dir():raise ValueError('Invalid frozen cache')
    setup=root/'setup.json'
    setup_hash=_digest(setup)
    frozen=json.loads(setup.read_text())
    if frozen.get('version')!=1 or frozen.get('solver_version')!='1.1.4':raise ValueError('Invalid solver setup')
    source=frozen['source'];tables=frozen['tables']
    if (not isinstance(source,dict) or not {'worker','adapter'}<=set(source)
            or not all(isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v) for v in source.values())
            or set(tables)!={'transition.npz','pruning_kociemba.npz'}):raise ValueError('Invalid frozen solver inputs')
    if (root/'tables').is_symlink():raise ValueError('Linked solver tables')
    for name,digest in tables.items():
        if _digest(root/'tables'/name)!=digest:raise ValueError('Solver table changed')
    aggregate=lambda value:hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return dict(cache_setup_sha256=setup_hash,source_sha256=aggregate(source),tables_sha256=aggregate(tables))


def freeze_container_setup(cache,image,output):
    """Bind an immutable prepared image to verified tables; startup still probes it."""
    import json,re
    if not isinstance(image,str) or not re.fullmatch('sha256:[0-9a-f]{64}',image):raise ValueError('Immutable image required')
    cache=Path(cache).absolute()
    manifest=dict(version=1,kind='cube_solver_container',image=image,cache=str(cache),**_frozen_cache(cache))
    with Path(output).open('x') as stream:json.dump(manifest,stream,indent=2,sort_keys=True);stream.write('\n')
    return manifest


def verify_container_setup(path):
    import json,re
    try:
        path=Path(path);_digest(path)
        manifest=json.loads(path.read_text())
        if (set(manifest)!={'version','kind','image','cache','cache_setup_sha256','source_sha256','tables_sha256'}
                or manifest['version']!=1 or manifest['kind']!='cube_solver_container'
                or not re.fullmatch('sha256:[0-9a-f]{64}',manifest['image'])):raise ValueError('Invalid solver container setup')
        if any(manifest[k]!=v for k,v in _frozen_cache(manifest['cache']).items()):raise ValueError('Frozen cache changed')
        return manifest
    except Exception:raise ValueError('cube_solver assets unavailable or verification failed; run maintainer setup') from None


def container_create_command(manifest,*,engine):
    import os
    cache=manifest['cache']
    if any(c in cache for c in (',','\n','\r','\0')):raise ValueError('Invalid cache mount')
    # Fixed unprivileged identity, no model proxy/socket, devices, source checkout
    # or host runtime bind. All executable code and dependencies live in the image.
    uid=os.getuid() or 65532;gid=os.getgid() or 65532
    command=engine.command('create','--interactive',*engine.create_options(),
        '--network','none','--read-only','--user',f'{uid}:{gid}',
        '--cap-drop','ALL','--security-opt','no-new-privileges',
        *engine.resource_options(memory='2g'),
        '--tmpfs','/tmp:rw,nosuid,nodev,size=67108864,mode=1777',
        '--env','HOME=/tmp','--env','OMP_NUM_THREADS=1','--env','OPENBLAS_NUM_THREADS=1',
        '--workdir','/tmp','--entrypoint','/usr/local/bin/python3',
        '--mount',f'type=bind,src={cache},dst=/cache,readonly',
        manifest['image'],'-I','-B','/opt/worker/scripts/agentbench_cube_solver.py','--cache','/cache')
    return command


def register_from_setup(path,*,registry,private_directory,engine):
    from .plugins import DockerWorker,validate
    manifest=verify_container_setup(path)
    contract=descriptor(manifest['source_sha256'],manifest['tables_sha256'])
    contract['execution_contract'].update(isolation=engine.kind,image_sha256=manifest['image'].split(':')[1])
    worker=DockerWorker(container_create_command(manifest,engine=engine),engine=engine,
        private_directory=private_directory,timeout_seconds=60,max_output_bytes=8192)
    # Before any native episode exists, exercise the actual isolated executable,
    # frozen source/table checks and independent replay. No host fallback exists.
    payload={'arguments':{'facelets_urfdlb':SOLVED}}
    result=worker(payload);validate(result,contract['output_schema']);validate_solution(result,payload)
    registry.register(contract,worker,result_validator=validate_solution)


def export_container_context(repository,output,wheelhouse,requirements):
    """Explicit minimal build input set; never copy a checkout or installed home."""
    import shutil
    repository=Path(repository);output=Path(output)
    output.mkdir(mode=0o700,parents=True,exist_ok=False)
    members=['scripts/agentbench_cube_solver.py',
        'source/agentbench_platform/agentbench_platform/__init__.py',
        'source/agentbench_platform/agentbench_platform/cube_solver.py',
        'source/agentbench_platform/agentbench_platform/cube_rules.py',
        'source/agentbench/agentbench/tasks/manager_based/table_top_manipulation/config/rubiks_cube/rubiks_cube_rules.py']
    for name in members:
        source=repository/name;_digest(source)
        target=output/'runtime'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    # A package locator only, without the simulation task registration initializer.
    (output/'runtime/source/agentbench/agentbench/__init__.py').write_text('')
    wheels=sorted(Path(wheelhouse).glob('*.whl'))
    if not wheels:raise ValueError('Prepare pinned offline wheels first')
    (output/'wheels').mkdir()
    for source in wheels:
        _digest(source);shutil.copyfile(source,output/'wheels'/source.name)
    _digest(requirements);shutil.copyfile(requirements,output/'requirements.lock')
    shutil.copyfile(repository/'tools/cube_solver/Dockerfile',output/'Dockerfile')
    shutil.copyfile(repository/'tools/cube_solver/build.py',output/'build.py')
    return {str(p.relative_to(output)):dict(sha256=_digest(p),bytes=p.stat().st_size)
            for p in sorted(output.rglob('*')) if p.is_file()}
