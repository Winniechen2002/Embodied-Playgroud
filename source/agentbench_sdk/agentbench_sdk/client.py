"""Bounded JSON-only Unix socket client. No simulation dependencies or retries."""
import json
import math
import socket
import uuid

MAX_FRAME_BYTES = 4 * 1024 * 1024


class ProtocolError(RuntimeError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


class TransportError(RuntimeError):
    """Outcome may be ambiguous: retry only with the SAME request ID and content."""
    def __init__(self, request_id):
        self.request_id = request_id
        super().__init__('Connection failed; outcome unknown. Retry with the same request ID.')


def _no_constant(value):
    raise ValueError('Non-finite JSON number')


def _finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError('Non-finite JSON number')
    return number


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key')
        result[key] = value
    return result


class Client:
    def __init__(self, socket_path, token, *, timeout=30.0):
        self.socket_path = socket_path
        self.token = token
        self.timeout = timeout
        self.tools = _Tools(self)
        self.mechanism = _Mechanism(self)

    def _call(self, method, params, request_id=None):
        request_id = str(uuid.uuid4()) if request_id is None else request_id
        request = dict(version=1, id=request_id, token=self.token, method=method, params=params)
        frame = json.dumps(request, allow_nan=False, separators=(',', ':')).encode() + b'\n'
        if len(frame) > MAX_FRAME_BYTES:
            raise ValueError('Request too large')
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as conn:
                conn.settimeout(self.timeout)
                conn.connect(self.socket_path)
                conn.sendall(frame)
                with conn.makefile('rb') as reader:
                    payload = reader.readline(MAX_FRAME_BYTES + 1)
            if not payload or len(payload) > MAX_FRAME_BYTES or not payload.endswith(b'\n'):
                raise ValueError('Invalid response frame')
            response = json.loads(payload, parse_constant=_no_constant, parse_float=_finite_float, object_pairs_hook=_unique_pairs)
            if (not isinstance(response, dict) or type(response.get('version')) is not int
                    or response['version'] != 1 or response.get('id') != request_id
                    or type(response.get('ok')) is not bool):
                raise ValueError('Invalid response envelope')
            expected = {'version', 'id', 'ok', 'result' if response['ok'] else 'error'}
            if set(response) != expected:
                raise ValueError('Invalid response fields')
            if not response['ok']:
                error = response['error']
                if (not isinstance(error, dict) or set(error) != {'code', 'message'}
                        or not all(isinstance(v, str) for v in error.values())):
                    raise ValueError('Invalid error envelope')
                raise ProtocolError(error['code'], error['message'])
            return response['result']
        except (OSError, ValueError, UnicodeError, RecursionError) as exc:
            raise TransportError(request_id) from exc

    def describe(self, *, request_id=None):
        return self._call('describe', {}, request_id)

    def observe(self, camera_ids=(), *, request_id=None):
        return self._call('observe', {'camera_ids': list(camera_ids) if isinstance(camera_ids, (tuple, list)) else camera_ids}, request_id)

    def step(self, action, *, request_id=None):
        return self._call('step', {'action': action}, request_id)

    def step_sequence(self, actions, *, request_id=None):
        return self._call('step_sequence', {'actions': actions}, request_id)

    def finish(self, *, request_id=None):
        return self._call('finish', {}, request_id)

    def get_resource(self, resource_id, *, request_id=None):
        return self._call('get_resource', {'resource_id': resource_id}, request_id)

    def close(self):
        """Each call owns its connection; closing a client never resets the run."""

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


class _Tools:
    def __init__(self, client):
        self._client = client

    def list(self, *, request_id=None):
        return self._client._call('tools.list', {}, request_id)

    def call(self, name, arguments, *, request_id=None):
        return self._client._call('tools.call', {'name': name, 'arguments': arguments}, request_id)


class _Mechanism:
    def __init__(self, client):
        self._client = client

    def command(self, name, arguments, *, request_id=None):
        return self._client._call('mechanism.command', {'name': name, 'arguments': arguments}, request_id)
