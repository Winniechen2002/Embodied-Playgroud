"""Trusted v1 gateway: serialized execution, strict validation and durable replay.

One service owns one backend/run. Never create a backend when a client connects.
Runtime owner must keep service alive and enforce the episode wall-clock limit.
"""
import hashlib
import hmac
import json
import os
import socket
import socketserver
import time
import sqlite3
import threading
import traceback
from dataclasses import asdict
from pathlib import Path

from .profiles import RunProfile, number, sanitize_description, sanitize_snapshot, sanitize_result
from .resources import ResourceStore
from .native_storage import RuntimeStateGuard, RuntimeStateLost

MAX_FRAME_BYTES = 4 * 1024 * 1024
DEFAULT_MAX_CONNECTIONS = 16
DEFAULT_FRAME_TIMEOUT = 30.
# Fixed vocabulary and one first-event per code bound denial-storm storage.
REJECTION_CODES = frozenset(('invalid_request', 'unsupported_version', 'unauthorized',
    'invalid_action', 'unsupported_method', 'invalid_cameras', 'request_id_conflict',
    'episode_closed', 'resource_unavailable', 'tool_unavailable', 'tool_failed',
    'malformed_frame', 'oversize_frame', 'incomplete_frame', 'frame_timeout', 'admission_limit',
    'mechanism_unavailable', 'invalid_mechanism_command'))
MAX_COUNTER = 2**63 - 1


class Rejection(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message


def _reject(code='invalid_request', message='Invalid request.'):
    raise Rejection(code, message)


def _no_constant(_):
    raise ValueError('Non-finite JSON')


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate key')
        result[key] = value
    return result


def _json(value):
    return json.dumps(value, allow_nan=False, separators=(',', ':'), sort_keys=True)


def _valid_json(value, depth=0):
    if depth > 32:
        return False
    if value is None or type(value) in (str, bool):
        return True
    if type(value) in (int, float):
        return number(value)
    if isinstance(value, list):
        return all(_valid_json(v, depth+1) for v in value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and _valid_json(v, depth+1) for k, v in value.items())
    return False


class ProtocolService:
    def __init__(self, backend, *, token, profile=None, journal_path, resources=None, tools=None,
                 finalize_on_terminal=False, storage_guard=None):
        if not isinstance(token, str) or not token:
            raise ValueError('A nonempty token is required')
        self.backend = backend
        self._token = token
        self._profile = profile or RunProfile()
        self.resources = resources if resources is not None else ResourceStore()
        self.tools = tools
        self.finalize_on_terminal = finalize_on_terminal
        self.request_inflight = threading.Event()
        self.terminal_response_pending = threading.Event()
        self.terminal_response_complete = threading.Event()
        self.terminal_response_delivered = False
        self._terminal_response = None
        self._lock = threading.RLock()
        self._audit_failed = False
        self._storage_interrupted = False
        self._compliance_path = Path(journal_path).with_name('protocol-compliance.json')
        # The journal contains private traceback/evidence. Create it privately before SQLite opens WAL.
        fd = os.open(journal_path, os.O_CREAT | os.O_RDWR, 0o600)
        os.fchmod(fd, 0o600)
        os.close(fd)
        self._db = sqlite3.connect(journal_path, check_same_thread=False)
        self._db.execute('PRAGMA journal_mode=WAL')
        self._db.execute('PRAGMA synchronous=FULL')
        self._db.executescript('''
            CREATE TABLE IF NOT EXISTS requests (id TEXT PRIMARY KEY, digest TEXT NOT NULL,
              status TEXT NOT NULL, response TEXT);
            CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS compliance (code TEXT PRIMARY KEY, count INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS events (sequence INTEGER PRIMARY KEY AUTOINCREMENT,
              kind TEXT NOT NULL, detail TEXT NOT NULL);
        ''')
        identity = _json({'profile': asdict(self._profile), 'token_sha256': hashlib.sha256(token.encode()).hexdigest()})
        old = self._state('identity')
        if old is not None and old != identity:
            self._db.close()
            raise ValueError('Journal belongs to a different run configuration')
        self._set_state('identity', identity)
        self._audit_failed = self._state('audit_failed') == 'true'
        self._description = sanitize_description(backend.describe(), self._profile)
        spec = self._description['action_spec']
        self._action_size = spec.get('size')
        self._low, self._high = spec.get('low'), spec.get('high')
        if (type(self._action_size) is not int or self._action_size < 1
                or not isinstance(self._low, (list, tuple)) or not isinstance(self._high, (list, tuple))
                or len(self._low) != self._action_size or len(self._high) != self._action_size
                or not all((a is None or number(a)) and (b is None or number(b)) and (a is None or b is None or a <= b) for a, b in zip(self._low, self._high))):
            self._db.close()
            raise ValueError('Backend supplied invalid action bounds')
        self._camera_ids = frozenset(self._description['cameras'])
        if self._db.execute("SELECT 1 FROM requests WHERE status='pending' LIMIT 1").fetchone():
            self._set_state('sealed', 'true')
            self._event('ambiguous_pending', 'Pending request found on service startup; episode sealed.')
        self._db.commit()
        self._persist_compliance()
        self.storage_guard = storage_guard or RuntimeStateGuard(Path(journal_path).parent)
        self.storage_guard.protect(Path(journal_path).parent)
        self.storage_guard.protect(journal_path)
        for suffix in ('-wal', '-shm'):
            self.storage_guard.protect(str(journal_path)+suffix, live=True)

    @property
    def profile(self):
        return self._profile

    def _state(self, key):
        row = self._db.execute('SELECT value FROM state WHERE key=?', (key,)).fetchone()
        return row[0] if row else None

    def _set_state(self, key, value):
        self._db.execute('INSERT OR REPLACE INTO state VALUES (?,?)', (key, value))

    def _event(self, kind, detail):
        self._db.execute('INSERT INTO events (kind,detail) VALUES (?,?)', (kind, detail))

    def compliance_summary(self):
        with self._lock:
            counts = dict(self._db.execute('SELECT code,count FROM compliance'))
            rejected = {code: count for code, count in counts.items() if code in REJECTION_CODES}
            return dict(version=1, scope='gateway_rejections_only', compliant=not rejected and not self._audit_failed,
                        rejections=rejected, connections_closed=counts.get('connection_closed', 0),
                        counters_saturated=any(count == MAX_COUNTER for count in counts.values()),
                        audit_failed=self._audit_failed)

    def _persist_compliance(self):
        # Separate from the immutable physical final so replay-grace denials remain represented.
        path = self._compliance_path.with_suffix('.json.tmp')
        fd = os.open(path, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o600)
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, 'w') as stream:
            stream.write(_json(self.compliance_summary()) + '\n')
            stream.flush(); os.fsync(stream.fileno())
        os.replace(path, self._compliance_path)
        fd = os.open(self._compliance_path.parent, os.O_RDONLY)
        try: os.fsync(fd)
        finally: os.close(fd)

    def _count(self, code):
        old = self._db.execute('SELECT count FROM compliance WHERE code=?', (code,)).fetchone()
        self._db.execute('INSERT OR REPLACE INTO compliance VALUES (?,?)',
                         (code, min(MAX_COUNTER, (old[0] if old else 0) + 1)))
        return old is None

    def _audit_failure(self):
        self._audit_failed = True
        try:
            self._set_state('sealed', 'true')
            self._set_state('audit_failed', 'true')
            self._db.commit()
        except sqlite3.Error:
            pass  # The in-memory guard also fails closed when the database cannot write.

    def _interrupt_storage(self):
        if self._storage_interrupted: return
        self._storage_interrupted = True
        self._audit_failed = True
        # Never touch the lost SQLite connection again. The native backend owns
        # a separate durable physical journal and seals its executed prefix.
        try: getattr(self.backend, 'abort', self.backend.finish)()
        except Exception: pass  # The guard remains latched even if finalization fails.

    def poll_storage(self):
        """Owner-thread idle check; never block a worker awaiting native dispatch."""
        if not self._lock.acquire(blocking=False): return True
        try:
            try: self.storage_guard.check()
            except RuntimeStateLost:
                self._interrupt_storage()
                return False
            return True
        finally: self._lock.release()

    def record_rejection(self, code, request=None, *, frame=None):
        if code not in REJECTION_CODES: raise ValueError('Unsupported rejection audit code')
        with self._lock:
            try:
                if not self.poll_storage(): return
                if self._count(code):
                    detail = {'code': code}
                    if isinstance(request, dict):
                        # Hash identity only; never store raw tokens, IDs, methods or payloads.
                        identity = request.get('id')
                        if isinstance(identity, str) and len(identity) <= 128:
                            detail['id_sha256'] = hashlib.sha256(identity.encode()).hexdigest()
                        if _valid_json(request):
                            payload = {key: value for key, value in request.items() if key != 'token'}
                            detail['payload_sha256'] = hashlib.sha256(_json(payload).encode()).hexdigest()
                    if frame is not None:
                        detail['frame_sha256'] = hashlib.sha256(frame).hexdigest()
                    self._event('protocol_rejection', _json(detail))
                self._db.commit()
                self._persist_compliance()
            except Exception:
                self._audit_failure()
                raise

    def connection_closed(self):
        with self._lock:
            try:
                if not self.poll_storage(): return
                if self._count('connection_closed'):
                    self._event('connection_closed', 'Client connection closed; episode retained.')
                self._db.commit()
                self._persist_compliance()
            except Exception:
                self._audit_failure()
                raise

    def response_completed(self, response, *, delivered):
        """Transport acknowledgment, called only after sendall/flush or a failed write."""
        with self._lock:
            if self._terminal_response == response and not self.terminal_response_complete.is_set():
                self.terminal_response_delivered = delivered
                self.terminal_response_complete.set()

    def close(self):
        with self._lock:
            try:
                if self.poll_storage(): self._persist_compliance()
            finally: self._db.close()

    def _envelope(self, request):
        if not isinstance(request, dict) or set(request) != {'version','id','token','method','params'}:
            _reject()
        if type(request['version']) is not int or request['version'] != 1:
            _reject('unsupported_version', 'Unsupported protocol version.')
        if not isinstance(request['id'], str) or not 1 <= len(request['id']) <= 128:
            _reject()
        token = request['token']
        if not isinstance(token, str) or not hmac.compare_digest(token.encode(), self._token.encode()):
            _reject('unauthorized', 'Authentication required.')
        if not isinstance(request['method'], str) or not isinstance(request['params'], dict) or not _valid_json(request):
            _reject()

    def _action(self, action):
        if (not isinstance(action, list) or len(action) != self._action_size
                or not all(number(v) and (lo is None or lo <= v) and (hi is None or v <= hi) for v, lo, hi in zip(action, self._low, self._high))):
            _reject('invalid_action', 'Action must contain finite numbers within the declared bounds.')

    def _params(self, method, params):
        expected = {'describe': set(), 'observe': {'camera_ids'}, 'step': {'action'},
                    'step_sequence': {'actions'}, 'finish': set(), 'get_resource': {'resource_id'},
                    'tools.list': set(), 'tools.call': {'name','arguments'},
                    'mechanism.command': {'name','arguments'}}
        if method not in expected:
            _reject('unsupported_method', 'Unsupported method.')
        if method == 'observe' and not params:
            params = {'camera_ids': []}
        if set(params) != expected[method]:
            _reject()
        if method == 'observe':
            ids = params['camera_ids']
            if (not isinstance(ids, list) or not all(isinstance(i, str) for i in ids)
                    or len(set(ids)) != len(ids) or not set(ids) <= self._camera_ids):
                _reject('invalid_cameras', 'Unknown or invalid camera selection.')
        elif method == 'step':
            self._action(params['action'])
        elif method == 'step_sequence':
            actions = params['actions']
            if not isinstance(actions, list) or not 1 <= len(actions) <= 30:
                _reject('invalid_action', 'A sequence must contain 1 through 30 actions.')
            for action in actions:
                self._action(action)
        elif method == 'get_resource':
            if not isinstance(params['resource_id'], str):
                _reject()
        elif method == 'tools.call':
            if not isinstance(params['name'], str) or not isinstance(params['arguments'], dict):
                _reject()
        elif method == 'mechanism.command':
            if 'mechanism' not in self._description or not callable(getattr(self.backend, 'mechanism', None)):
                _reject('mechanism_unavailable', 'Mechanism unavailable.')
            from .mechanisms import validate_command
            try:
                validate_command(params['name'], params['arguments'])
            except ValueError:
                _reject('invalid_mechanism_command', 'Invalid mechanism command.')
        return params

    def handle(self, request):
        with self._lock:
            self.request_inflight.set()
            try:
                return self._handle(request)
            finally:
                self.request_inflight.clear()

    def _handle(self, request):
        request_id = request.get('id') if isinstance(request, dict) and isinstance(request.get('id'), str) and len(request['id']) <= 128 else None
        response = {'version': 1, 'id': request_id, 'ok': False}
        with self._lock:
            pending = False
            try:
                self._envelope(request)
                self.storage_guard.check()
                if self._audit_failed:
                    return dict(response, error={'code':'internal_error','message':'The request failed. Contact the run owner.'})
                method = request['method']
                params = self._params(method, request['params'])
                # Authentication is checked on EVERY retry. Token is not recorded.
                digest = hashlib.sha256(_json({'version':1,'method':method,'params':params}).encode()).hexdigest()
                old = self._db.execute('SELECT digest,status,response FROM requests WHERE id=?', (request_id,)).fetchone()
                if old:
                    if old[0] != digest:
                        _reject('request_id_conflict', 'Request ID was already used with different content.')
                    if old[1] == 'completed':
                        return json.loads(old[2])
                    _reject('episode_closed', 'Episode sealed after an ambiguous request.')
                self._db.execute('INSERT INTO requests VALUES (?,?,?,NULL)', (request_id,digest,'pending'))
                if method in ('step', 'step_sequence', 'mechanism.command'):
                    # Private evidence for the final action/batch, including crashes.
                    self._set_state('last_control_request', _json(dict(
                        method=method, params=params, request_digest=digest,
                        received_at_unix_s=time.time())))
                self._db.commit()  # Must precede any backend/plugin action.
                pending = True
                result = self._dispatch(method, params)
                self.storage_guard.check()
                if not _valid_json(result):
                    raise ValueError('Backend returned invalid public JSON')
                success = {'version': 1, 'id': request_id, 'ok': True, 'result': result}
                encoded = _json(success)
                if len(encoded.encode()) + 1 > MAX_FRAME_BYTES:
                    raise ValueError('Response exceeds transport limit')
                # Publish success only after validation; failures retain the fixed error envelope.
                response = success
            except RuntimeStateLost:
                self._interrupt_storage()
                response['error'] = {'code':'internal_error','message':'The request failed. Contact the run owner.'}
                if self.finalize_on_terminal and self._terminal_response is None:
                    self._terminal_response = response
                    self.terminal_response_pending.set()
                return response
            except Rejection as exc:
                self.record_rejection(exc.code, request)
                response['error'] = {'code':exc.code,'message':exc.message}
            except Exception:
                self._event('backend_error', traceback.format_exc())
                if pending:
                    self._set_state('sealed','true')
                    if self.finalize_on_terminal:
                        try:
                            self._finish(abort=True)
                        except Exception:
                            self._event('finalization_error', traceback.format_exc())
                response['error'] = {'code':'internal_error','message':'The request failed. Contact the run owner.'}
            if pending:
                self._db.execute("UPDATE requests SET status='completed',response=? WHERE id=?", (_json(response),request_id))
            self._db.commit()
            if (self.finalize_on_terminal and self._terminal_response is None
                    and (self._state('finished') or self._state('sealed'))):
                self._terminal_response = response
                self.terminal_response_pending.set()
            return response

    def _snapshot(self, camera_ids=()):
        return sanitize_snapshot(self.backend.snapshot(camera_ids), self.profile, camera_ids)

    def _dispatch(self, method, params):
        self.storage_guard.check()
        if (self.finalize_on_terminal and (self._state('finished') or self._state('sealed'))
                and method != 'finish'):
            _reject('episode_closed', 'Episode is closed.')
        if method == 'describe':
            return self._description
        if method == 'observe':
            return self._snapshot(params['camera_ids'])
        if method == 'mechanism.command':
            if self._state('sealed') or self._state('finished'):
                _reject('episode_closed', 'Episode is closed.')
            snapshot = self._snapshot()
            if snapshot['terminated'] or snapshot['truncated']:
                _reject('episode_closed', 'Episode is closed.')
            from .mechanisms import public_reply
            # Pending request is durably committed before this single mutation.
            # Expected physical precondition failures return accepted=False; no
            # caller-provided proof or raw native diagnostic crosses the gateway.
            self.storage_guard.check()
            return public_reply(self.backend.mechanism(params['name'], params['arguments']))
        if method in ('step','step_sequence'):
            if self._state('sealed') or self._state('finished'):
                _reject('episode_closed', 'Episode is closed.')
            snapshot = self._snapshot()
            if snapshot.get('terminated') or snapshot.get('truncated'):
                _reject('episode_closed', 'Episode is closed.')
            actions = [params['action']] if method == 'step' else params['actions']
            executed = 0
            for action in actions:
                self.storage_guard.check()
                raw = self.backend.step(action)
                self.storage_guard.check()
                executed += 1
                snapshot = sanitize_snapshot(raw, self.profile)
                if snapshot.get('terminated') or snapshot.get('truncated'):
                    if self.finalize_on_terminal:
                        self._finish()
                    break
            return {'executed_steps':executed, 'observation':snapshot}
        if method == 'finish':
            old = self._state('finished')
            if old:
                return json.loads(old)
            if self._state('sealed'):
                _reject('episode_closed', 'Episode is sealed.')
            return self._finish()
        if method == 'get_resource':
            try:
                return self.resources.get(params['resource_id'], self.profile.observation)
            except KeyError:
                _reject('resource_unavailable','Resource unavailable.')
        if method == 'tools.list':
            if self.tools is None:
                return {'tools': []}
            from .plugins import public_descriptor
            return {'tools': [public_descriptor(item) for item in self.tools.list()
                    if item.get('name') in self.profile.tools]}
        if method == 'tools.call':
            if self.tools is None or params['name'] not in self.profile.tools:
                _reject('tool_unavailable','Tool unavailable.')
            if params['name'] not in {item.get('name') for item in self.tools.list()}:
                _reject('tool_unavailable','Tool unavailable.')
            # A trusted tool receives public inputs only. Tool implementation defines its public output schema.
            from .plugins import ToolFailure
            try:
                return self.tools.call(params['name'], params['arguments'])
            except ToolFailure:
                _reject('tool_failed','Tool input or inference failed; contact run owner.')
        _reject('unsupported_method','Unsupported method.')

    def _finish(self, *, abort=False):
        old = self._state('finished')
        if old:
            return json.loads(old)
        finalize = getattr(self.backend, 'abort', self.backend.finish) if abort else self.backend.finish
        raw = finalize()
        result = sanitize_result(raw)
        from .failure_diagnostics import capture_diagnostics, capture_backend_diagnostics
        self._set_state('private_final_result', _json(dict(
            captured_at_unix_s=time.time(), abort=abort,
            evidence=capture_diagnostics(lambda: raw),
            backend_diagnostics=capture_backend_diagnostics(self.backend))))
        self._set_state('finished', _json(result))
        return result


class _Handler(socketserver.StreamRequestHandler):
    def _frame(self, buffer):
        deadline = time.monotonic() + self.server.frame_timeout
        while True:
            newline = buffer.find(b'\n')
            if newline >= 0:
                data = bytes(buffer[:newline+1]); del buffer[:newline+1]
                if len(data) > MAX_FRAME_BYTES: return data, 'oversize_frame'
                return data, None
            if len(buffer) > MAX_FRAME_BYTES: return bytes(buffer), 'oversize_frame'
            remaining = deadline - time.monotonic()
            if remaining <= 0: return bytes(buffer), 'frame_timeout'
            self.request.settimeout(remaining)
            try: data = self.request.recv(min(65536, MAX_FRAME_BYTES + 1 - len(buffer)))
            except TimeoutError: return bytes(buffer), 'frame_timeout'
            if not data: return bytes(buffer), 'incomplete_frame' if buffer else None
            buffer.extend(data)

    def handle(self):
        buffer = bytearray()
        try:
            while not self.server.stopping:
                data, code = self._frame(buffer)
                if self.server.stopping or (not data and code is None): break
                if code:
                    self.server.service.record_rejection(code, frame=data)
                    response = {'version':1,'id':None,'ok':False,'error':{'code':'invalid_request','message':'Invalid request.'}}
                else:
                    try:
                        request = json.loads(data, parse_constant=_no_constant, object_pairs_hook=_unique_pairs)
                    except (ValueError, UnicodeError, RecursionError):
                        self.server.service.record_rejection('malformed_frame', frame=data)
                        response = {'version':1,'id':None,'ok':False,'error':{'code':'invalid_request','message':'Invalid request.'}}
                    else:
                        response = self.server.service.handle(request)
                delivered = False
                try:
                    self.request.settimeout(self.server.frame_timeout)
                    self.wfile.write((_json(response)+'\n').encode())
                    self.wfile.flush()
                    delivered = True
                finally:
                    self.server.service.response_completed(response, delivered=delivered)
                if code: break
        except (OSError, TimeoutError):
            pass
        finally:
            self.server.service.connection_closed()


class _SocketServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = False
    block_on_close = True
    stopping = False

    def __init__(self, *args, max_connections, frame_timeout, **kwargs):
        self._slots = threading.BoundedSemaphore(max_connections)
        self._connections = set()
        self._connections_lock = threading.Lock()
        self.frame_timeout = frame_timeout
        super().__init__(*args, **kwargs)

    @property
    def active_connections(self):
        with self._connections_lock: return len(self._connections)

    def process_request(self, request, client_address):
        if not self._slots.acquire(blocking=False):
            try: self.service.record_rejection('admission_limit')
            finally: self.shutdown_request(request)
            return
        with self._connections_lock: self._connections.add(request)
        try: super().process_request(request, client_address)
        except BaseException:
            self._release(request)
            self.shutdown_request(request)
            raise

    def _release(self, request):
        with self._connections_lock: self._connections.discard(request)
        self._slots.release()

    def process_request_thread(self, request, client_address):
        try: super().process_request_thread(request, client_address)
        finally: self._release(request)

    def close_connections(self):
        with self._connections_lock:
            for request in self._connections:
                try: request.shutdown(socket.SHUT_RDWR)
                except OSError: pass


class ProtocolServer:
    def __init__(self, socket_path, service, *, max_connections=DEFAULT_MAX_CONNECTIONS,
                 frame_timeout=DEFAULT_FRAME_TIMEOUT):
        if type(max_connections) is not int or not 1 <= max_connections <= 64:
            raise ValueError('Native connection cap must be 1 through 64')
        if not number(frame_timeout) or not 0 < frame_timeout <= 30:
            raise ValueError('Native frame timeout must be positive and at most 30 seconds')
        self.socket_path = Path(socket_path)
        self.service = service
        self.max_connections, self.frame_timeout = max_connections, frame_timeout
        self._server = None
        self._thread = None
        self._socket_identity = None

    def start(self):
        if self._server is not None:
            raise RuntimeError('Server already started')
        self._server = _SocketServer(str(self.socket_path), _Handler,
            max_connections=self.max_connections, frame_timeout=self.frame_timeout)
        self._server.service = self.service
        self._socket_identity = RuntimeStateGuard._identity(self.socket_path)
        try:
            os.chmod(self.socket_path, 0o600)
            self.service.storage_guard.protect(self.socket_path, live=True)
            thread = threading.Thread(target=self._server.serve_forever, kwargs={'poll_interval':.05}, daemon=True)
            thread.start()
            self._thread = thread
        except BaseException:
            self.close()
            raise

    def close(self):
        if self._server is not None:
            self._server.stopping = True
            if self._thread is not None: self._server.shutdown()
            self._server.close_connections()
            self._server.server_close()
            if self._thread is not None: self._thread.join()
            try: same = RuntimeStateGuard._identity(self.socket_path) == self._socket_identity
            except OSError: same = False
            if same: self.socket_path.unlink()
            self.service.storage_guard.release(self.socket_path)
            self._server = None
            self._thread = None
