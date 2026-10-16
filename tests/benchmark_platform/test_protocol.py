"""Portable socket tests: removing validation/filtering/replay guards must fail."""
import base64
import concurrent.futures
import importlib.util
import json
import socket
import sqlite3
import sys
import threading
import tempfile
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'source/agentbench_sdk'), str(ROOT / 'source/agentbench_platform')]


def api():
    # Feature assertion gives an intentional RED before imports exist.
    assert importlib.util.find_spec('agentbench_sdk') is not None, 'pure SDK is not implemented'
    import agentbench_sdk
    assert hasattr(agentbench_sdk, 'Client'), 'pure SDK Client is not implemented'
    from agentbench_sdk import Client, ProtocolError
    from agentbench_platform.protocol import ProtocolService, ProtocolServer
    from agentbench_platform.profiles import RunProfile
    from agentbench_platform.resources import ResourceStore
    return Client, ProtocolError, ProtocolService, ProtocolServer, RunProfile, ResourceStore


CANARY = 'PRIVATE_ROUTE_CANARY'
ACTION = [0.0] * 16


class Backend:
    def __init__(self, terminal=99, fail=False):
        self.index = 0
        self.terminal = terminal
        self.fail = fail
        self.finished = 0
        self.active = 0
        self.max_active = 0

    def describe(self):
        return {'task': {'id': 'lock', 'mode': 'assemble', 'route': CANARY},
                'action_spec': {'size': 16, 'low': [-1.0]*16, 'high': [1.0]*16},
                'robots': {'left': {'model': 'panda', 'joint_names': ['j1'], 'route': CANARY}},
                'cameras': {'top': {'width': 640, 'height': 480, 'secret': CANARY}},
                'goal': {'description': 'assemble', 'route': CANARY}, 'secret': CANARY}

    def snapshot(self, camera_ids=()):
        return {'step_index': self.index, 'simulation_time_s': self.index/30,
                'robots': {'left': {'joint_names': ['j1'], 'joint_positions': [.2],
                                    'joint_velocities': [.0], 'measured_finger_positions': [.04],
                                    'previous_action': ACTION, 'nested': {'secret': CANARY}}},
                'cameras': {name: {'rgb_resource_id': 'rgb', 'depth_resource_id': 'depth',
                                  'capture_step': self.index, 'width': 640, 'height': 480,
                                  'calibration': {'intrinsics': [[1,0,0],[0,1,0],[0,0,1]], 'secret': CANARY},
                                  'labels': CANARY} for name in camera_ids},
                'privileged': {'pieces': {'key': {'position': [0,0,0], 'quaternion': [1,0,0,0], 'route': CANARY}},
                               'diagnostics': {'clearance_m': .01, 'next_action': CANARY},
                               'logical_state': CANARY},
                'terminated': self.index >= self.terminal, 'truncated': False, 'secret': CANARY}

    def step(self, action):
        self.active += 1
        self.max_active = max(self.active, self.max_active)
        time.sleep(.001)
        self.index += 1
        self.active -= 1
        if self.fail:
            raise RuntimeError('/private/host/' + CANARY)
        return self.snapshot()

    def finish(self):
        self.finished += 1
        return {'success': True, 'score': .75, 'step_count': self.index, 'terminated': False,
                'truncated': False, 'reason': '/host/' + CANARY, 'evidence_path': CANARY}


class Tools:
    def list(self):
        return [{'name': 'echo', 'description': 'public echo', 'input_schema': {'type': 'object'}},
                {'name': 'hidden', 'description': CANARY}]

    def call(self, name, arguments):
        return {'echo': arguments}


@pytest.fixture
def tmp_path():
    # macOS Unix socket paths are limited to 104 bytes; pytest default paths exceed it.
    with tempfile.TemporaryDirectory(prefix='ab-', dir='/tmp') as directory:
        yield Path(directory)


@pytest.fixture
def running(tmp_path):
    Client, Error, Service, Server, Profile, Resources = api()
    resources = Resources(max_resource_bytes=1024)
    resources.register(b'RGB', modality='rgb', profiles=('rgb','rgbd','privileged'), capture_step=0, resource_id='rgb')
    resources.register(b'DEPTH', modality='depth', profiles=('rgbd','privileged'), capture_step=0, resource_id='depth')
    backend = Backend()
    service = Service(backend, token='token', profile=Profile(observation='rgb', tools=('echo',)),
                      journal_path=tmp_path/'journal.sqlite', resources=resources, tools=Tools())
    server = Server(tmp_path/'run.sock', service)
    server.start()
    yield Client(str(tmp_path/'run.sock'), 'token'), backend, service, server, tmp_path
    server.close()
    service.close()


def raw(server, **changes):
    request = {'version': 1, 'id': 'raw-'+str(time.time_ns()), 'token': 'token', 'method': 'observe', 'params': {}}
    request.update(changes)
    with socket.socket(socket.AF_UNIX) as conn:
        conn.connect(str(server.socket_path))
        conn.sendall(json.dumps(request).encode()+b'\n')
        return json.loads(conn.makefile('rb').readline())


def test_public_calls_and_privacy(running):
    c, b, _, _, _ = running
    assert c.describe()['action_spec']['size'] == 16
    obs = c.observe()
    assert obs['step_index'] == 0 and obs['cameras'] == {} and 'privileged' not in obs
    image = c.observe(camera_ids=['top'])
    assert image['cameras']['top']['rgb_resource_id'] == 'rgb'
    assert 'depth_resource_id' not in image['cameras']['top']
    assert b.index == 0
    assert c.step(ACTION)['executed_steps'] == 1
    assert c.step_sequence([ACTION, ACTION])['executed_steps'] == 2
    assert c.tools.list() == {'tools':[{'name':'echo','description':'public echo','input_schema':{'type':'object'}}]}
    assert c.tools.call('echo', {'x': 1}) == {'echo': {'x': 1}}
    resource = c.get_resource('rgb')
    assert base64.b64decode(resource['data_base64']) == b'RGB'
    assert resource['capture_step'] == 0
    assert CANARY not in json.dumps([c.describe(), obs, image, c.finish()])
    assert c.finish()['score'] == .75 and b.finished == 1
    with pytest.raises(api()[1]) as e: c.step(ACTION)
    assert e.value.code == 'episode_closed'


def test_privileged_nested_whitelists(tmp_path):
    Client, _, Service, Server, Profile, _ = api()
    service = Service(Backend(), token='token', profile=Profile(observation='privileged'), journal_path=tmp_path/'j')
    server = Server(tmp_path/'s', service); server.start()
    try:
        obs = Client(str(tmp_path/'s'),'token').observe()
        assert obs['privileged']['pieces']['key']['position'] == [0,0,0]
        assert obs['privileged']['diagnostics'] == {'clearance_m': .01}
        assert CANARY not in json.dumps(obs)
    finally: server.close(); service.close()


@pytest.mark.parametrize('action', [[True]+[0]*15, [float('nan')]+[0]*15, [float('inf')]+[0]*15, [0]*15, [2]+[0]*15, 'bad'])
def test_invalid_actions_never_execute(running, action):
    c,b,_,_,_ = running
    with pytest.raises((api()[1], ValueError)): c.step(action)
    assert b.index == 0


@pytest.mark.parametrize('actions', [[], [ACTION]*31, [ACTION,[2]+[0]*15]])
def test_entire_batch_validated_before_execution(running, actions):
    c,b,_,_,_ = running
    with pytest.raises(api()[1]): c.step_sequence(actions)
    assert b.index == 0


def test_terminal_mid_batch_and_observe_clock(running):
    c,b,_,_,_ = running; b.terminal = 2
    result = c.step_sequence([ACTION]*5)
    assert result['executed_steps'] == 2 and result['observation']['terminated']
    assert c.observe()['simulation_time_s'] == 2/30
    with pytest.raises(api()[1]): c.step(ACTION)
    assert b.index == 2


def test_ids_reconnect_and_concurrent_serialization(running):
    c,b,_,server,p = running
    first = c.step(ACTION, request_id='once')
    c.close()
    new = api()[0](str(server.socket_path),'token')
    assert new.step(ACTION, request_id='once') == first and b.index == 1
    with pytest.raises(api()[1]) as e: new.step([.1]*16, request_id='once')
    assert e.value.code == 'request_id_conflict'
    def step(i): return api()[0](str(server.socket_path),'token').step(ACTION, request_id=f'parallel-{i}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(step, range(10)))
    assert b.index == 11 and b.max_active == 1
    assert sorted(r['observation']['step_index'] for r in results) == list(range(2,12))
    with sqlite3.connect(p/'journal.sqlite') as db:
        assert db.execute("select count(*) from events where kind='connection_closed'").fetchone()[0] > 0


@pytest.mark.parametrize('changes', [{'token':''},{'method':'reset'}, {'method':'observe','params':{'profile':'privileged'}},
                                    {'version':2}, {'version':True}, {'extra':'x'}, {'params':{'camera_ids':['unknown']}},
                                    {'params':{'camera_ids':'top'}}, {'id':True}])
def test_invalid_envelope_and_params(running, changes):
    _,b,_,server,_ = running
    result = raw(server, **changes)
    assert result['ok'] is False and CANARY not in json.dumps(result)
    assert b.index == 0


@pytest.mark.parametrize('resource', ['depth','../secret','/etc/passwd','missing'])
def test_resource_guessing_never_reads_or_escalates(running, resource):
    with pytest.raises(api()[1]) as e: running[0].get_resource(resource)
    assert e.value.code == 'resource_unavailable'


def test_tool_authorization(running):
    with pytest.raises(api()[1]) as e: running[0].tools.call('hidden', {})
    assert e.value.code == 'tool_unavailable'


def test_ambiguous_backend_failure_seals_without_replay(running):
    c,b,_,server,p = running; b.fail = True
    with pytest.raises(api()[1]) as e: c.step(ACTION,request_id='failed')
    assert e.value.code == 'internal_error' and CANARY not in str(e.value)
    with pytest.raises(api()[1]): c.step(ACTION, request_id='failed')
    with pytest.raises(api()[1]): c.step(ACTION)
    assert b.index == 1
    with sqlite3.connect(p/'journal.sqlite') as db:
        assert CANARY in db.execute('select detail from events where kind="backend_error"').fetchone()[0]


def test_durable_replay_and_pending_request_seals(tmp_path):
    Client,Error,Service,Server,Profile,_ = api(); b = Backend(); journal = tmp_path/'j'; path=tmp_path/'s'
    service = Service(b,token='token',profile=Profile(),journal_path=journal)
    server=Server(path,service); server.start()
    result=Client(str(path),'token').step(ACTION,request_id='durable')
    server.close(); service.close()
    service=Service(b,token='token',profile=Profile(),journal_path=journal)
    server=Server(path,service); server.start()
    try:
        assert Client(str(path),'token').step(ACTION,request_id='durable') == result and b.index == 1
    finally: server.close(); service.close()
    with sqlite3.connect(journal) as db:
        db.execute("insert into requests (id,digest,status,response) values ('pending','abc','pending',NULL)")
    service=Service(b,token='token',profile=Profile(),journal_path=journal)
    server=Server(path,service); server.start()
    try:
        with pytest.raises(Error) as e: Client(str(path),'token').step(ACTION)
        assert e.value.code == 'episode_closed' and b.index == 1
    finally: server.close(); service.close()


def test_rgbd_can_fetch_registered_depth_without_privileged_state(tmp_path):
    Client,_,Service,Server,Profile,Resources = api()
    resources=Resources(); resources.register(b'Z',modality='depth',profiles=('rgbd',),capture_step=4,resource_id='depth')
    service=Service(Backend(),token='token',profile=Profile(observation='rgbd'),journal_path=tmp_path/'j',resources=resources)
    server=Server(tmp_path/'s',service); server.start()
    try:
        c=Client(str(server.socket_path),'token')
        observation=c.observe(['top'])
        assert observation['cameras']['top']['depth_resource_id'] == 'depth'
        assert 'privileged' not in observation
        assert base64.b64decode(c.get_resource('depth')['data_base64']) == b'Z'
        assert c.get_resource('depth')['capture_step'] == 4
    finally: server.close(); service.close()


def test_resource_registration_is_immutable_and_bounded():
    Resources=api()[5]; store=Resources(max_resource_bytes=4,max_total_bytes=4)
    store.register(b'1234',modality='rgb',profiles=('rgb',),capture_step=0,resource_id='one',metadata={'host_path':CANARY})
    assert CANARY not in json.dumps(store.get('one','rgb'))
    for data, name in [(b'new','one'), (b'12345','large'), (b'x','over-budget')]:
        with pytest.raises(ValueError): store.register(data,modality='rgb',profiles=('rgb',),capture_step=1,resource_id=name)
    with pytest.raises(ValueError): store.register(b'x',modality='depth',profiles=('rgb',),capture_step=0)


def test_duplicate_json_keys_and_nonfinite_wire_rejected(running):
    _,b,_,server,_=running
    for data in [b'{"version":1,"version":1}\n', b'{"version":1,"id":"x","token":"token","method":"step","params":{"action":[NaN]}}\n']:
        with socket.socket(socket.AF_UNIX) as conn:
            conn.connect(str(server.socket_path)); conn.sendall(data)
            response=json.loads(conn.makefile('rb').readline())
            assert not response['ok']
    assert b.index == 0


def test_disconnected_pending_transport_does_not_reapply(running):
    _,b,_,server,_=running
    request={'version':1,'id':'lost-response','token':'token','method':'step','params':{'action':ACTION}}
    with socket.socket(socket.AF_UNIX) as conn:
        conn.connect(str(server.socket_path)); conn.sendall(json.dumps(request).encode()+b'\n')
        # Leave without receiving response: processing may finish after connection closes.
    c=api()[0](str(server.socket_path),'token')
    result=c.step(ACTION,request_id='lost-response')
    assert result['observation']['step_index']==1 and b.index==1


def test_missing_terminal_fields_seals_instead_of_running_full_batch(running):
    c,b,_,_,_=running
    original=b.step
    def malformed(action):
        result=original(action); del result['terminated']; return result
    b.step=malformed
    with pytest.raises(api()[1]) as e: c.step_sequence([ACTION]*3)
    assert e.value.code=='internal_error'
    with pytest.raises(api()[1]): c.step(ACTION)
    assert b.index==1


def test_transport_error_exposes_retry_id_and_never_auto_retries(tmp_path):
    Client=api()[0]
    from agentbench_sdk import TransportError
    with pytest.raises(TransportError) as e: Client(str(tmp_path/'missing'),'token').step(ACTION,request_id='retry-this')
    assert e.value.request_id=='retry-this'


def test_full_nested_physical_allowlists(running):
    from agentbench_platform.profiles import sanitize_snapshot, RunProfile
    raw=Backend().snapshot(['top'])
    physical=raw['privileged']
    physical['robot_bodies']={'wrist':{'position':[1,2,3],'logical_state':CANARY}}
    physical['jacobians']={'left':[[1,2,3]],'oracle':{'route':CANARY}}
    physical['contacts']=[{'body_a':'left','body_b':'key','force_n':.1,'route':CANARY}]
    physical['geometry']={'key':{'vertices':[[0,0,0]],'route':CANARY}}
    physical['physics']={'physics_hz':120,'oracle':{'route':CANARY}}
    public=sanitize_snapshot(raw,RunProfile(),['top'])
    assert public['privileged']['robot_bodies']['wrist']=={'position':[1,2,3]}
    assert public['privileged']['contacts']==[{'body_a':'left','body_b':'key','force_n':.1}]
    assert CANARY not in json.dumps(public)


def test_finished_summary_survives_service_restart(tmp_path):
    Client,Error,Service,Server,Profile,_=api(); b=Backend(); journal=tmp_path/'j'; path=tmp_path/'s'
    service=Service(b,token='token',profile=Profile(),journal_path=journal); server=Server(path,service); server.start()
    result=Client(str(path),'token').finish(); server.close(); service.close()
    service=Service(b,token='token',profile=Profile(),journal_path=journal); server=Server(path,service); server.start()
    try:
        assert Client(str(path),'token').finish()==result and b.finished==1
        with pytest.raises(Error): Client(str(path),'token').step(ACTION)
    finally: server.close(); service.close()


def test_sdk_rejects_nonfinite_response_numbers(tmp_path):
    from agentbench_sdk import Client, TransportError
    path=str(tmp_path/'untrusted')
    with socket.socket(socket.AF_UNIX) as listener:
        listener.bind(path); listener.listen()
        def reply():
            conn,_=listener.accept()
            with conn:
                request=json.loads(conn.makefile('rb').readline())
                conn.sendall(('{"version":1,"id":'+json.dumps(request['id'])+',"ok":true,"result":{"score":1e400}}\n').encode())
        thread=threading.Thread(target=reply); thread.start()
        try:
            with pytest.raises(TransportError): Client(path,'token').finish(request_id='bad-response')
        finally: thread.join()


def test_private_journal_permissions(running):
    journal=running[4]/'journal.sqlite'
    assert journal.stat().st_mode & 0o077 == 0


def test_sdk_and_platform_import_without_site_packages():
    import subprocess
    result=subprocess.run([sys.executable,'-I','-S','-c',
        "import sys; sys.path[:0]="+repr([str(ROOT/'source/agentbench_sdk'),str(ROOT/'source/agentbench_platform')])+"; import agentbench_sdk; import agentbench_platform.protocol; print('stdlib-only imports passed')"],capture_output=True,text=True)
    assert result.returncode==0, result.stderr
    assert result.stdout.strip()=='stdlib-only imports passed'


def test_built_wheels_exclude_caches_and_private_runtime_from_sdk(tmp_path):
    import subprocess
    import zipfile
    result=subprocess.run([sys.executable,'-m','pip','wheel','--no-cache-dir','--no-deps','--no-build-isolation',
                           '--wheel-dir',str(tmp_path), str(ROOT/'source/agentbench_sdk'),str(ROOT/'source/agentbench_platform')],capture_output=True,text=True)
    assert result.returncode==0, result.stdout+result.stderr
    for wheel in tmp_path.glob('*.whl'):
        files=zipfile.ZipFile(wheel).namelist()
        assert not any('__pycache__' in name or name.endswith('.pyc') for name in files)
        if wheel.name.startswith('agentbench_sdk'):
            assert not any('agentbench_platform' in name or 'baseline' in name for name in files)


def test_oversized_tool_result_returns_bounded_error_and_stable_replay(running):
    client,_,service,server,path=running
    from agentbench_platform.protocol import MAX_FRAME_BYTES

    class LargeTool(Tools):
        def __init__(self):
            self.calls=0

        def call(self, name, arguments):
            self.calls+=1
            return {'payload':'X'*MAX_FRAME_BYTES, 'private':CANARY}

    tool=LargeTool(); service.tools=tool
    request={'version':1,'id':'oversized','token':'token','method':'tools.call',
             'params':{'name':'echo','arguments':{}}}
    def wire_response():
        with socket.socket(socket.AF_UNIX) as conn:
            conn.connect(str(server.socket_path))
            conn.sendall(json.dumps(request).encode()+b'\n')
            payload=conn.makefile('rb').readline(MAX_FRAME_BYTES+1)
        assert len(payload)<512, 'Failure response retained the oversized success payload'
        assert payload.endswith(b'\n')
        return json.loads(payload)

    first=wire_response()
    assert first=={'version':1,'id':'oversized','ok':False,
                  'error':{'code':'internal_error','message':'The request failed. Contact the run owner.'}}
    assert wire_response()==first
    with pytest.raises(api()[1]) as error:
        client.tools.call('echo',{},request_id='oversized')
    assert error.value.code=='internal_error'
    assert tool.calls==1 and CANARY not in json.dumps(first)
    with sqlite3.connect(path/'journal.sqlite') as db:
        cached=db.execute('select response from requests where id="oversized"').fetchone()[0]
        assert len(cached.encode())<512 and json.loads(cached)==first


@pytest.mark.parametrize('summary',[
    None, {},
    {'success':True,'score':.5,'step_count':0,'terminated':False},
    {'success':1,'score':.5,'step_count':0,'terminated':False,'truncated':False},
    {'success':True,'score':[.5],'step_count':0,'terminated':False,'truncated':False},
    {'success':True,'score':True,'step_count':0,'terminated':False,'truncated':False},
    {'success':True,'score':float('nan'),'step_count':0,'terminated':False,'truncated':False},
    {'success':True,'score':float('inf'),'step_count':0,'terminated':False,'truncated':False},
    {'success':True,'score':.5,'step_count':[-1],'terminated':False,'truncated':False},
    {'success':True,'score':.5,'step_count':-.5,'terminated':False,'truncated':False},
    {'success':True,'score':.5,'step_count':-1,'terminated':False,'truncated':False},
    {'success':True,'score':.5,'step_count':1.5,'terminated':False,'truncated':False},
    {'success':True,'score':.5,'step_count':True,'terminated':False,'truncated':False},
    {'success':True,'score':.5,'step_count':0,'terminated':0,'truncated':False},
    {'success':True,'score':.5,'step_count':0,'terminated':False,'truncated':'false'},
])
def test_malformed_finish_is_sealed_with_valid_error_and_at_most_once(running,summary):
    client,backend,_,server,path=running
    original=backend.finish
    def malformed_finish():
        original()
        return summary
    backend.finish=malformed_finish
    first=raw(server,id='malformed-finish',method='finish',params={})
    assert first=={'version':1,'id':'malformed-finish','ok':False,
                  'error':{'code':'internal_error','message':'The request failed. Contact the run owner.'}}
    assert raw(server,id='malformed-finish',method='finish',params={})==first
    with pytest.raises(api()[1]) as replay:
        client.finish(request_id='malformed-finish')
    assert replay.value.code=='internal_error'
    with pytest.raises(api()[1]) as new_finish:
        client.finish(request_id='another-finish')
    assert new_finish.value.code=='episode_closed'
    with pytest.raises(api()[1]): client.step(ACTION)
    assert backend.finished==1 and backend.index==0
    with sqlite3.connect(path/'journal.sqlite') as db:
        assert db.execute('select value from state where key="finished"').fetchone() is None
        assert db.execute('select value from state where key="sealed"').fetchone()[0]=='true'


def test_terminal_lifecycle_waits_for_write_and_replays_without_backend(tmp_path):
    Client,Error,Service,Server,_,_=api()
    backend=Backend(terminal=1)
    service=Service(backend,token='token',journal_path=tmp_path/'j',finalize_on_terminal=True)
    # Calling the dispatcher alone cannot claim transport delivery.
    request=dict(version=1,id='terminal',token='token',method='step',params={'action':ACTION})
    response=service.handle(request)
    assert response['result']['observation']['terminated']
    assert not service.terminal_response_complete.is_set()
    server=Server(tmp_path/'s',service);server.start()
    try:
        client=Client(str(tmp_path/'s'),'token')
        assert client.step(ACTION,request_id='terminal')==response['result']
        assert service.terminal_response_complete.wait(1)
        assert service.terminal_response_delivered
        backend.step=lambda _:pytest.fail('terminal action reexecuted')
        backend.snapshot=lambda *_:pytest.fail('closed simulator observed')
        backend.finish=lambda:pytest.fail('finish must use durable public result')
        assert client.finish(request_id='finish')['step_count']==1
        assert client.finish(request_id='finish')==client.finish()
        assert client.step(ACTION,request_id='terminal')==response['result']
        for method in (lambda:client.step(ACTION),client.observe,lambda:client.tools.call('x',{})):
            with pytest.raises(Error) as exc:method()
            assert exc.value.code=='episode_closed'
    finally:server.close();service.close()


def test_replay_server_close_stops_existing_active_connection(tmp_path):
    _,_,Service,Server,_,_=api()
    service=Service(Backend(),token='token',journal_path=tmp_path/'j')
    server=Server(tmp_path/'s',service);server.start()
    active=threading.Event();stop=threading.Event()
    def stream():
        with socket.socket(socket.AF_UNIX) as conn:
            conn.connect(str(server.socket_path))
            with conn.makefile('rb') as reader:
                while not stop.is_set():
                    try:
                        conn.sendall(json.dumps(dict(version=1,id='cached',token='token',method='describe',params={})).encode()+b'\n')
                        if not reader.readline():break
                        active.set()
                    except OSError:break
    worker=threading.Thread(target=stream);worker.start()
    assert active.wait(2)
    closer=threading.Thread(target=server.close);closer.start();closer.join(.5)
    try:assert not closer.is_alive(), 'active cached retries must not extend the replay deadline indefinitely'
    finally:
        stop.set();worker.join(2);closer.join(2);service.close()
