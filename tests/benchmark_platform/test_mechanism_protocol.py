"""Mechanism requests are audited mutations, not controller-provided evidence."""
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'source/agentbench_platform'), str(ROOT/'source/agentbench_sdk')]
from test_protocol import Backend, CANARY, tmp_path  # short real Unix-socket paths


class CubeBackend(Backend):
    def __init__(self):
        super().__init__()
        self.commands = []
        self.epoch = 0

    def describe(self):
        result = super().describe()
        result['task'] = dict(id='cube', family='rubiks_cube', mode='solve')
        result['action_spec'] = dict(size=8, low=[-1.]*8, high=[1.]*8)
        result['mechanism'] = dict(version='hybrid_fixture_v1', private_route=CANARY)
        return result

    def snapshot(self, camera_ids=()):
        result = super().snapshot(camera_ids)
        result['mechanism'] = dict(state='idle', epoch=self.epoch, measured_force=CANARY)
        return result

    def mechanism(self, name, arguments):
        self.commands.append((name, arguments))
        self.epoch += 1
        return dict(accepted=True, state='turning', epoch=self.epoch, private_force=CANARY)


def request(method, params, identifier='command-1'):
    return dict(version=1, id=identifier, token='token', method=method, params=params)


def service(tmp_path, backend=None):
    from agentbench_platform.protocol import ProtocolService
    from agentbench_platform.profiles import RunProfile
    backend = backend or CubeBackend()
    return backend, ProtocolService(backend, token='token', profile=RunProfile(observation='rgb'),
                                    journal_path=tmp_path/'requests.sqlite')


def test_mechanism_command_replay_is_once_and_does_not_advance_physics(tmp_path):
    backend, gateway = service(tmp_path)
    command = request('mechanism.command', dict(name='turn.begin', arguments={'move': 'U'}))
    try:
        reply = gateway.handle(command)
        assert reply['ok'], reply
        assert reply['result'] == dict(accepted=True, state='turning', epoch=1)
        assert gateway.handle(command) == reply
        assert backend.commands == [('turn.begin', {'move': 'U'})]
        assert backend.index == 0
        assert CANARY not in json.dumps(reply)
        conflict = gateway.handle(request('mechanism.command', dict(name='turn.begin', arguments={'move': 'R'})))
        assert conflict['error']['code'] == 'request_id_conflict'
        assert len(backend.commands) == 1
    finally:
        gateway.close()


@pytest.mark.parametrize('name,args', [
    ('turn.begin', {'move': 'U', 'passed': True}),
    ('turn.begin', {'move': 'U2'}),
    ('transport.attach', {'frame': [[1, 0, 0]]}),
    ('mark_grasped', {}),
    ('set_cube_state', {'facelets': 'solved'}),
])
def test_illegal_proof_or_unsupported_operation_never_reaches_backend(tmp_path, name, args):
    backend, gateway = service(tmp_path)
    try:
        reply = gateway.handle(request('mechanism.command', dict(name=name, arguments=args)))
        assert not reply['ok']
        assert backend.commands == [] and backend.index == 0
    finally:
        gateway.close()


def test_closed_episode_and_legacy_task_reject_mechanism_mutations(tmp_path):
    backend, gateway = service(tmp_path)
    try:
        gateway.handle(request('finish', {}, 'finish'))
        reply = gateway.handle(request('mechanism.command', dict(name='turn.begin', arguments={'move': 'U'})))
        assert reply['error']['code'] == 'episode_closed'
        assert not backend.commands
    finally:
        gateway.close()
    folder = tmp_path/'legacy'; folder.mkdir()
    _, gateway = service(folder, Backend())
    try:
        reply = gateway.handle(request('mechanism.command', dict(name='turn.begin', arguments={'move': 'U'})))
        assert not reply['ok']
    finally:
        gateway.close()


def test_real_sdk_exposes_frozen_contract_and_filters_mechanism_state(tmp_path):
    from agentbench_sdk import Client
    from agentbench_platform.protocol import ProtocolServer
    backend, gateway = service(tmp_path)
    server = ProtocolServer(tmp_path/'s', gateway)
    server.start()
    try:
        client = Client(str(tmp_path/'s'), 'token')
        spec = client.describe()
        assert spec['task']['family'] == 'rubiks_cube'
        assert spec['mechanism']['version'] == 'hybrid_fixture_v1'
        assert 'turn.begin' in spec['mechanism']['commands']
        assert CANARY not in json.dumps(spec)
        assert client.observe()['mechanism'] == dict(state='idle', epoch=0)
        assert client.mechanism.command('turn.begin', {'move': 'U'})['accepted']
        assert client.observe()['step_index'] == 0
        assert client.step([0.]*8)['observation']['step_index'] == 1
        assert len(backend.commands) == 1
    finally:
        server.close(); gateway.close()
