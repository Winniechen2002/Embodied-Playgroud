"""Private terminal evidence survives sanitization without changing outcomes."""
import json
import sqlite3
from types import SimpleNamespace

import pytest

from test_protocol import Backend, ACTION, api
from agentbench_platform.failure_diagnostics import capture_diagnostics


@pytest.mark.parametrize('observation', ['rgb', 'rgbd', 'privileged'])
def test_terminal_evidence_private_durable_and_replayed_once(tmp_path, observation):
    _, _, Service, _, Profile, _ = api()
    class Failed(Backend):
        def finish(self):
            self.finished += 1
            return dict(success=False, score=0., step_count=self.index,
                        terminated=True, truncated=False,
                        private_diagnostics={'reason': 'PRIVATE_REASON', 'depth_m': .006})
    backend = Failed(terminal=1)
    path = tmp_path/'journal.sqlite'
    service = Service(backend, token='SECRET_TOKEN', profile=Profile(observation=observation),
                      journal_path=path, finalize_on_terminal=True)
    def call(ident, method, params):
        return service.handle(dict(version=1, id=ident, token='SECRET_TOKEN', method=method, params=params))
    try:
        first = call('step', 'step_sequence', {'actions': [ACTION]*3})
        assert first['ok'] and first['result']['executed_steps'] == 1
        result = call('finish', 'finish', {})
        assert result['ok'] and result['result']['success'] is False
        assert call('finish', 'finish', {}) == result and backend.finished == 1
        assert 'PRIVATE_REASON' not in json.dumps([first, result])
    finally:
        service.close()
    with sqlite3.connect(path) as db:
        states = {key: json.loads(value) for key, value in db.execute('select key,value from state')}
    assert states['private_final_result']['evidence']['native']['private_diagnostics']['reason'] == 'PRIVATE_REASON'
    assert states['last_control_request']['params']['actions'] == [ACTION]*3
    assert 'SECRET_TOKEN' not in json.dumps(states)
    assert path.stat().st_mode & 0o777 == 0o600


def test_failed_step_preserves_request_and_traceback(tmp_path):
    _, _, Service, _, _, _ = api()
    service = Service(Backend(fail=True), token='t', journal_path=tmp_path/'journal', finalize_on_terminal=True)
    try:
        reply = service.handle(dict(version=1, id='fail', token='t', method='step', params={'action': ACTION}))
        assert not reply['ok'] and 'PRIVATE_ROUTE_CANARY' not in json.dumps(reply)
        assert json.loads(service._state('last_control_request'))['params']['action'] == ACTION
        assert service._db.execute("select detail from events where kind='backend_error'").fetchone()
        assert json.loads(service._state('private_final_result'))['abort'] is True
    finally:
        service.close()


def test_capture_marks_nonfinite_and_reader_errors():
    evidence = capture_diagnostics(lambda: {'depth': float('nan')})
    assert evidence['native']['depth'] == {'nonfinite': 'nan'}
    json.dumps(evidence, allow_nan=False)
    def broken():
        raise RuntimeError('read failure')
    assert 'read failure' in capture_diagnostics(broken)['diagnostic_error']


def test_dispatched_diagnostics_read_on_owner_thread():
    from concurrent.futures import ThreadPoolExecutor
    import threading
    from agentbench_platform.native_backend import MainThreadDispatcher, DispatchedBackend
    from agentbench_platform.failure_diagnostics import capture_backend_diagnostics
    owner = threading.get_ident()
    class Native:
        @property
        def result(self):
            assert threading.get_ident() == owner
            return {'failure_reasons': ['forbidden_contact']}
    dispatcher = MainThreadDispatcher()
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(capture_backend_diagnostics, DispatchedBackend(Native(), dispatcher))
            while not future.done():
                dispatcher.pump(timeout=.05)
            assert future.result()['native']['result']['failure_reasons'] == ['forbidden_contact']
    finally:
        dispatcher.close()


def test_native_verdict_readers_keep_details_without_rescoring():
    from agentbench_platform.failure_diagnostics import capture_backend_diagnostics
    from agentbench_platform.environment_backend import MarbleBackend, IsaacEnvironmentBackend
    from agentbench_platform.maniskill_backend import ManiSkillBackend
    marble = MarbleBackend.__new__(MarbleBackend)
    marble._result = None; marble.terminated = True; marble.truncated = False
    marble.env = SimpleNamespace(success=False, control_steps=9,
        private_result=lambda: {'failure': 'protected_target_hit', 'protected_hits': [2]})
    result = capture_backend_diagnostics(marble)
    assert result['native']['native_report']['protected_hits'] == [2]
    isaac = IsaacEnvironmentBackend.__new__(IsaacEnvironmentBackend)
    isaac._result = None; isaac.success = False; isaac.failure = {'reason': 'non_top_ring_lifted', 'step': 17}
    isaac.steps = 3; isaac.terminated = True; isaac.truncated = False
    isaac.env = SimpleNamespace(_sim_step_counter=17, sim=SimpleNamespace(current_time=.2))
    isaac.monitor = None
    isaac.start_physics = 0; isaac.start_time = 0.; isaac.previous_action = []; isaac.task = {'family': 'hanoi_panda'}
    result = capture_backend_diagnostics(isaac)
    assert result['native']['failure']['step'] == 17
    mani = ManiSkillBackend.__new__(ManiSkillBackend)
    mani._result = None; mani.steps = 3; mani.terminated = True; mani.truncated = False; mani.previous_action = []
    mani.e = SimpleNamespace(report={'success': False, 'violations': ['protected:book']},
        oracle=SimpleNamespace(first_violation={'reason': 'protected:book', 'physics_step': 12}), physics_steps=15, sim_freq=120)
    result = capture_backend_diagnostics(mani)
    assert result['native']['first_violation']['physics_step'] == 12
