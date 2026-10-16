"""Run-owned local socket/SQLite storage with explicit durable evidence export."""
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile
import stat

from .native_backend import runtime_socket_path


class RuntimeStateLost(RuntimeError):
    """Run-owned state is missing or replaced; this episode cannot resume."""


class RuntimeStateGuard:
    def __init__(self, directory, *, on_loss=None):
        self.identities = {}
        self.live_paths = set()
        self.on_loss = on_loss
        self.loss = None
        self.protect(directory)

    @staticmethod
    def _identity(path):
        value = path.lstat()
        if stat.S_ISLNK(value.st_mode):
            raise OSError('Runtime state became a symlink')
        return value.st_dev, value.st_ino, stat.S_IFMT(value.st_mode)

    def protect(self, path, *, live=False):
        path = Path(path).absolute()
        self.check()
        self.identities[path] = self._identity(path)
        if live: self.live_paths.add(path)

    def release(self, path):
        """Owner lifecycle only: an expected socket close is not state loss."""
        path = Path(path).absolute()
        self.identities.pop(path, None)
        self.live_paths.discard(path)

    def check(self, *, include_live=True):
        if self.loss is None:
            for path, expected in self.identities.items():
                if not include_live and path in self.live_paths: continue
                try: same = self._identity(path) == expected
                except OSError: same = False
                if not same:
                    self.loss = dict(reason='local_state_lost', path=str(path))
                    if self.on_loss:
                        try: self.on_loss(self.loss)
                        except OSError as exc:
                            # Reporting failure must not mask loss and bypass
                            # the protocol's native-prefix finalization path.
                            self.loss['report_error'] = type(exc).__name__
                    break
        if self.loss is not None:
            raise RuntimeStateLost('Run-owned runtime state was lost or replaced')


class RuntimeStorage:
    def __init__(self, repository, output, *, local_root=None):
        self.output = Path(output)
        self.local_directory = None
        if local_root is None:
            self.socket_path = runtime_socket_path(repository, output)
            self.sqlite_path = self.output/'private/requests.sqlite'
            self.socket_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            self.guard = RuntimeStateGuard(self.socket_path.parent, on_loss=self._interrupt)
            return
        root = Path(local_root).absolute()
        if root.is_symlink():
            raise ValueError('Local runtime root must not be a symlink')
        root.mkdir(mode=0o700, parents=True, exist_ok=True)
        stat = root.stat()
        if stat.st_uid != os.getuid() or stat.st_mode & 0o022:
            raise ValueError('Local runtime root must be owned and not writable by others')
        identity = hashlib.sha256(str(self.output.resolve()).encode()).hexdigest()[:16]
        self.local_directory = root/identity
        self.socket_path = self.local_directory/'native.sock'
        if len(os.fsencode(self.socket_path)) >= 104:
            raise ValueError('Local runtime socket path is too long')
        self.local_directory.mkdir(mode=0o700, exist_ok=False)
        self.sqlite_path = self.local_directory/'requests.sqlite'
        self.guard = RuntimeStateGuard(self.local_directory, on_loss=self._interrupt)
        self._record('active')

    def _record(self, state, **extra):
        path = self.output/'runtime-state.json'
        temporary = path.with_suffix('.json.tmp')
        with temporary.open('w') as stream:
            stream.write(json.dumps(dict(
            state=state, socket=str(self.socket_path), sqlite=str(self.sqlite_path),
            local_state_loss_policy='interrupt; never automatically resume or replay actions', **extra),indent=2)+'\n')
            stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
        fd = os.open(self.output, os.O_RDONLY)
        try: os.fsync(fd)
        finally: os.close(fd)

    def _interrupt(self, loss):
        self._record('interrupted', archive_complete=False, **loss)

    def archive(self):
        """Call after protocol shutdown; keep owned originals for crash diagnosis."""
        if self.local_directory is None:
            return
        try:
            # WAL/SHM and socket removal are expected after their owners close.
            self.guard.check(include_live=False)
            if not self.sqlite_path.exists():
                # Initialization can fail before ProtocolService creates a DB.
                # A previously protected DB would already have failed above.
                self._record('not_started', archive_complete=False, reason='request_journal_not_created')
                return
        except RuntimeStateLost:
            return
        destination = self.output/'private'
        destination.mkdir(mode=0o700, exist_ok=True)
        copied = []
        if self.sqlite_path.exists():
            target = destination/'requests.sqlite'
            if target.exists():
                raise FileExistsError('Refusing to replace archived request journal')
            # A SQLite backup is itself a writable database, with locking and
            # many page-sized I/O operations. Keep it local too; PFS receives
            # only a closed, verified standalone file via a sequential copy.
            with tempfile.TemporaryDirectory(prefix='archive-',dir=self.local_directory) as temporary:
                local=Path(temporary)/'requests.sqlite'
                with closing(sqlite3.connect(self.sqlite_path.as_uri()+'?mode=ro',uri=True)) as source:
                    with closing(sqlite3.connect(local)) as backup:
                        source.backup(backup)
                        backup.execute('PRAGMA journal_mode=DELETE')
                        if backup.execute('PRAGMA integrity_check').fetchall()!=[('ok',)]:
                            raise RuntimeError('Invalid local request backup')
                with local.open('rb') as inp,target.open('xb') as out:
                    shutil.copyfileobj(inp,out,length=1024*1024)
                    out.flush();os.fsync(out.fileno())
            target.chmod(0o600); copied.append(target.name)
        compliance = self.sqlite_path.with_name('protocol-compliance.json')
        if compliance.exists():
            target = destination/compliance.name
            if target.exists():
                raise FileExistsError('Refusing to replace archived protocol report')
            shutil.copyfile(compliance, target);target.chmod(0o600);copied.append(target.name)
        self._record('archived', archive_complete=True, files=copied)
