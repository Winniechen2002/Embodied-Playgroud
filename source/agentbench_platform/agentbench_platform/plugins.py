"""Trusted registration, explicit public contracts and bounded process execution.

Workers receive one detached sanctioned capture, never a backend or path supplied
by a client. Production workers must supply explicit isolation; GraspNet supports
bubblewrap and the validated Docker worker. The generic process adapter also
supports maintainer/test executables but does not itself provide OS isolation.
"""
import base64
from copy import deepcopy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import uuid


class ToolFailure(ValueError):
    """An expected, publicly recoverable input/worker failure."""


def _schema(schema):
    if not isinstance(schema,dict):raise ValueError('Invalid tool schema')
    allowed={'type','properties','required','additionalProperties','items','minItems','maxItems','minimum','maximum','minLength','maxLength','enum'}
    if set(schema)-allowed or schema.get('type') not in ('object','array','string','number','integer','boolean'):
        raise ValueError('Invalid tool schema')
    result=deepcopy(schema)
    if schema['type']=='object':
        props=schema.get('properties',{})
        if not isinstance(props,dict) or any(not isinstance(k,str) or not re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]{0,63}',k) for k in props):raise ValueError('Invalid tool schema')
        if 'properties' in schema:result['properties']={k:_schema(v) for k,v in props.items()}
        required=schema.get('required',[])
        if not isinstance(required,list) or any(k not in props for k in required) or len(set(required))!=len(required):raise ValueError('Invalid tool schema')
        if schema.get('additionalProperties',False) is not False:raise ValueError('Open tool schemas are forbidden')
    elif schema['type']=='array':result['items']=_schema(schema.get('items'))
    for key in ('minimum','maximum','minItems','maxItems','minLength','maxLength'):
        if key in schema and (type(schema[key]) not in (int,float) or not math.isfinite(schema[key])):raise ValueError('Invalid tool schema')
    if 'enum' in schema and (not isinstance(schema['enum'],list) or any(type(v) not in (str,int,float,bool) for v in schema['enum'])):raise ValueError('Invalid tool schema')
    return result


def validate(value,schema):
    kind=schema['type']
    if kind=='object':
        if not isinstance(value,dict) or set(value)-set(schema.get('properties',{})) or set(schema.get('required',[]))-set(value):raise ValueError('Invalid tool value')
        for k,v in value.items():validate(v,schema['properties'][k])
    elif kind=='array':
        if not isinstance(value,list) or not schema.get('minItems',0)<=len(value)<=schema.get('maxItems',10000):raise ValueError('Invalid tool value')
        for v in value:validate(v,schema['items'])
    elif kind=='string':
        if not isinstance(value,str) or not schema.get('minLength',0)<=len(value)<=schema.get('maxLength',4096):raise ValueError('Invalid tool value')
    elif kind=='boolean':
        if type(value) is not bool:raise ValueError('Invalid tool value')
    else:
        if type(value) not in ((int,) if kind=='integer' else (int,float)) or not math.isfinite(value) or not schema.get('minimum',-math.inf)<=value<=schema.get('maximum',math.inf):raise ValueError('Invalid tool value')
    if 'enum' in schema and value not in schema['enum']:raise ValueError('Invalid tool value')


def public_descriptor(raw):
    """Explicit nested whitelist; legacy injected descriptors remain compatible."""
    out={k:raw[k] for k in ('name','version','description') if isinstance(raw.get(k),str)}
    if 'input_binding' in raw:
        if raw['input_binding'] not in ('capture','submitted_arguments'):raise ValueError('Invalid tool input binding')
        out['input_binding']=raw['input_binding']
    for k in ('input_schema','output_schema'):
        if k in raw:out[k]=_schema(raw[k])
    if 'observation_profiles' in raw:
        p=raw['observation_profiles']
        if not isinstance(p,list) or any(v not in ('rgb','rgbd','privileged') for v in p):raise ValueError('Invalid tool profiles')
        out['observation_profiles']=list(p)
    if 'coordinate_contract' in raw:
        row=raw['coordinate_contract']
        out['coordinate_contract']={k:row[k] for k in ('frame','convention','units') if isinstance(row.get(k),str)}
    for k in ('source','checkpoint'):
        if k in raw:
            row=raw[k];out[k]={}
            for field,length in (('revision',40),('sha256',64)):
                if field in row:
                    if not isinstance(row[field],str) or not re.fullmatch('[0-9a-f]{'+str(length)+'}',row[field]):raise ValueError('Invalid tool provenance')
                    out[k][field]=row[field]
    if 'resources' in raw:
        if not isinstance(raw['resources'],list) or any(v not in ('rgb','depth','validity','calibration') for v in raw['resources']):raise ValueError('Invalid tool resources')
        out['resources']=list(raw['resources'])
    if 'execution_contract' in raw:
        row=raw['execution_contract'];out['execution_contract']={}
        if row.get('isolation') not in ('docker','podman','bwrap','process'):raise ValueError('Invalid tool execution contract')
        out['execution_contract']['isolation']=row['isolation']
        for key in ('offline','gpu'):
            if type(row.get(key)) is not bool:raise ValueError('Invalid tool execution contract')
            out['execution_contract'][key]=row[key]
        if 'device' in row:
            if row['device'] not in ('cpu','cuda') or row['gpu']!=(row['device']=='cuda'):
                raise ValueError('Invalid tool device contract')
            out['execution_contract']['device']=row['device']
        for key in ('max_wall_seconds','max_output_bytes'):
            if type(row.get(key)) is not int or row[key]<=0:raise ValueError('Invalid tool execution contract')
            out['execution_contract'][key]=row[key]
        for key in ('image_sha256','worker_sha256'):
            if key in row:
                if not isinstance(row[key],str) or not re.fullmatch('[0-9a-f]{64}',row[key]):raise ValueError('Invalid execution digest')
                out['execution_contract'][key]=row[key]
    return out


def _json(value):return json.dumps(value,allow_nan=False,separators=(',',':')).encode()


def _pairs(pairs):
    result={}
    for k,v in pairs:
        if k in result:raise ValueError('Duplicate worker key')
        result[k]=v
    return result


class ProcessWorker:
    def __init__(self,command,*,private_directory,timeout_seconds=60,max_output_bytes=256*1024,container_attach=False):
        if not command or not all(isinstance(v,str) for v in command) or not math.isfinite(timeout_seconds) or not 0<timeout_seconds<=120 or type(max_output_bytes) is not int or not 0<max_output_bytes<=512*1024 or type(container_attach) is not bool:
            raise ValueError('Invalid worker configuration')
        self.command=tuple(command);self.private=Path(private_directory)
        self.timeout=timeout_seconds;self.limit=max_output_bytes
        self.container_attach=container_attach

    def __call__(self,payload):
        self.private.mkdir(mode=0o700,parents=True,exist_ok=True)
        os.chmod(self.private,0o700)
        run=self.private/uuid.uuid4().hex;run.mkdir(mode=0o700)
        data=_json(payload)
        if len(data)>5*1024*1024:raise ValueError('Tool input too large')
        (run/'input.sha256').write_text(hashlib.sha256(data).hexdigest()+'\n')
        launcher=[sys.executable,'-I','-S','-B',str(Path(__file__).with_name('worker_limits.py')),str(self.limit),
                  *(['--container-attach'] if self.container_attach else []),*self.command]
        process=None
        try:
            # Podman stdin from a PFS TMPDIR can stall waiting for EOF. Keep
            # this unlinked input local; durable evidence still belongs to run.
            with tempfile.TemporaryFile(dir='/tmp' if self.container_attach else None) as inp,(run/'stdout').open('wb') as stdout,(run/'stderr').open('wb') as stderr:
                inp.write(data);inp.seek(0)
                process=subprocess.Popen(launcher,stdin=inp,stdout=stdout,stderr=stderr,cwd=run,
                    env={'PATH':'/usr/bin:/bin','HOME':'/tmp','LC_ALL':'C','PYTHONNOUSERSITE':'1'},start_new_session=True)
                try:code=process.wait(timeout=self.timeout)
                except subprocess.TimeoutExpired:
                    raise ValueError('Worker timeout')
            raw=(run/'stdout').read_bytes()
            if code!=0 or len(raw)>=self.limit:raise ValueError('Worker failed or exceeded output bound')
            result=json.loads(raw,object_pairs_hook=_pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('Nonfinite worker value')))
            (run/'result.sha256').write_text(hashlib.sha256(raw).hexdigest()+'\n')
            return result
        except Exception as exc:
            import traceback
            (run/'error.txt').write_text(traceback.format_exc())
            raise ToolFailure('Tool inference failed; contact run owner') from None
        finally:
            if process is not None:
                # start_new_session gives this invocation its own group. Kill
                # remaining members even when the leader already exited/reaped.
                try:
                    try:os.killpg(process.pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                    process.wait(timeout=5)
                    (run/'cleanup.json').write_text(json.dumps(dict(process_group=process.pid,leader_reaped=True))+'\n')
                except Exception:
                    import traceback
                    (run/'cleanup-error.txt').write_text(traceback.format_exc())
                    raise ToolFailure('Tool process cleanup failed; contact run owner') from None


class ToolRegistry:
    def __init__(self,*,resources,observation,granted=()):
        if observation not in ('rgb','rgbd','privileged'):raise ValueError('Invalid observation profile')
        self.resources=resources;self.observation=observation;self.granted=tuple(granted);self._tools={}

    def register(self,descriptor,worker,*,result_validator=None):
        d=public_descriptor(descriptor)
        required={'name','version','description','input_schema','output_schema','observation_profiles','coordinate_contract','source','checkpoint','resources'}
        if not required<=set(d) or set(d)-required-{'execution_contract','input_binding'} or not callable(worker):raise ValueError('Incomplete tool contract')
        if d.get('input_binding')=='submitted_arguments' and d['resources']:raise ValueError('Symbolic tools cannot acquire environment resources')
        if not re.fullmatch('[a-zA-Z][a-zA-Z0-9_.-]{0,63}',d['name']) or d['name'] in self._tools:raise ValueError('Duplicate or invalid tool name')
        if set(d['coordinate_contract'])!={'frame','convention','units'} or 'sha256' not in d['source'] or 'sha256' not in d['checkpoint']:raise ValueError('Incomplete provenance')
        self._tools[d['name']]=(deepcopy(d),worker,result_validator)

    def list(self):
        return [deepcopy(d) for name,(d,_,_) in self._tools.items() if name in self.granted and self.observation in d['observation_profiles']]

    def call(self,name,arguments):
        if name not in {d['name'] for d in self.list()}:raise ValueError('Tool unavailable')
        d,worker,result_validator=self._tools[name]
        try:
            validate(arguments,d['input_schema'])
            if d.get('input_binding')=='submitted_arguments':
                payload={'arguments':deepcopy(arguments)}
            else:
                capture=self.resources.resolve_capture(arguments['capture_id'],self.observation)
                # Calibration and resource IDs come only from this immutable binding.
                resources={m:self.resources.get(capture[m+'_resource_id'],self.observation) for m in d['resources'] if m!='calibration'}
                payload={'capture':capture,'resources':resources}
            result=worker(payload)
            validate(result,d['output_schema'])
            if result_validator is not None:result_validator(result,payload)
            return result
        except (KeyError,ValueError):
            raise ToolFailure('Tool input or inference failed; contact run owner') from None


def configured_registry(args,*,resources,private_directory):
    """Maintainer startup configuration; never consumes public path arguments."""
    from .profile_cli import selected_tools
    from .container_engine import ContainerEngine,engine_from_args
    granted=selected_tools(args)
    if not granted:return None
    if (set(granted)-{'graspnet'} or len(set(granted))!=len(granted)
            or ('graspnet' in granted and (args.profile=='rgb' or not args.tool_setup))
):
        raise ValueError('Selected tools unavailable')
    engine=engine_from_args(args) if hasattr(args,'container_engine') else ContainerEngine()
    registry=ToolRegistry(resources=resources,observation=args.profile,granted=granted)
    if 'graspnet' in granted:
        from .graspnet import registry_from_setup
        registry_from_setup(args.tool_setup,resources=resources,observation=args.profile,
            granted=granted,private_directory=Path(private_directory)/'graspnet',registry=registry,engine=engine)
    return registry


class DockerWorker:
    """Create and remove only the verified owned container, even on attach timeout."""
    def __init__(self,create_command,*,private_directory,timeout_seconds=90,max_output_bytes=256*1024,engine=None):
        from .container_engine import ContainerEngine
        self.engine=engine or ContainerEngine()
        prefix=self.engine.command('create')
        if list(create_command[:len(prefix)])!=prefix:raise ValueError('Worker create command does not match selected engine')
        self.create_command=tuple(create_command);self.private=Path(private_directory)
        self.timeout=timeout_seconds;self.limit=max_output_bytes

    def __call__(self,payload):
        self.private.mkdir(mode=0o700,parents=True,exist_ok=True)
        run=self.private/uuid.uuid4().hex;run.mkdir(mode=0o700)
        name='agentbench-graspnet-'+uuid.uuid4().hex
        prefix=len(self.engine.command('create'))
        command=list(self.create_command[:prefix])+['--name',name,'--label','agentbench.tool.owner='+name]+list(self.create_command[prefix:])
        owned=None
        env={'PATH':'/usr/bin:/bin','HOME':'/tmp','LC_ALL':'C'}
        def invoke(args,timeout=20):return subprocess.run(args,capture_output=True,timeout=timeout,env=env,check=False)
        def inspect_owned():
            result=invoke(self.engine.command('inspect',name))
            if result.returncode:return None
            rows=json.loads(result.stdout)
            if len(rows)!=1 or rows[0]['Config']['Labels'].get('agentbench.tool.owner')!=name:return None
            identity=rows[0]['Id']
            if not re.fullmatch('[0-9a-f]{64}',identity):return None
            (run/'container.json').write_text(json.dumps(rows[0],indent=2)+'\n')
            return identity
        try:
            created=invoke(command)
            (run/'create.stderr').write_bytes(created.stderr)
            # Never start/stop by name: verify the capability ownership and exact ID.
            owned=inspect_owned()
            if created.returncode or owned is None or created.stdout.decode().strip()!=owned:raise ValueError('Worker container creation failed')
            return ProcessWorker(self.engine.command('start','--attach','--interactive',owned),private_directory=run/'process',
                timeout_seconds=self.timeout,max_output_bytes=self.limit,container_attach=True)(payload)
        except Exception:
            import traceback
            (run/'error.txt').write_text(traceback.format_exc())
            raise ToolFailure('Tool container failed; contact run owner') from None
        finally:
            if owned is None:
                try:owned=inspect_owned()
                except Exception:pass
            if owned is not None:
                try:
                    removed=invoke(self.engine.command('rm','--force',owned))
                    (run/'cleanup.json').write_text(json.dumps(dict(container_id=owned,exit_code=removed.returncode,
                        stdout=removed.stdout.decode(errors='replace'),stderr=removed.stderr.decode(errors='replace')))+'\n')
                    if removed.returncode:raise ToolFailure('Tool container cleanup failed; contact run owner')
                except subprocess.TimeoutExpired:
                    (run/'cleanup.json').write_text(json.dumps(dict(container_id=owned,error='cleanup timeout'))+'\n')
                    raise ToolFailure('Tool container cleanup failed; contact run owner') from None
