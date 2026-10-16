"""Maintainer-selected container engine, with no ambient backend fallback.

Storage and OCI runtime overrides are local deployment inputs, never guest
arguments. Carry the storage configuration in argv so tool workers can retain
their deliberately empty environment. Cgroup limits are explicitly disclosed;
disabling them never disables namespace, mount, user or capability isolation.
"""
from dataclasses import dataclass
import hashlib
from pathlib import Path


@dataclass(frozen=True)
class ContainerEngine:
    kind: str = 'docker'
    storage_conf: Path | None = None
    containers_conf: Path | None = None
    runtime: Path | None = None
    cgroups: bool = True
    proc_mode: str = 'standard'

    def __post_init__(self):
        if (self.kind not in ('docker', 'podman') or type(self.cgroups) is not bool
                or self.proc_mode not in ('standard', 'empty')):
            raise ValueError('Invalid container engine')
        if self.kind == 'docker' and (self.storage_conf is not None or self.containers_conf is not None or self.runtime is not None or not self.cgroups or self.proc_mode != 'standard'):
            raise ValueError('Podman deployment options require the podman engine')
        for field in ('storage_conf', 'containers_conf', 'runtime'):
            value = getattr(self, field)
            if value is not None:
                path = Path(value)
                if not path.is_absolute() or any(c in str(path) for c in ('\n', '\r', '\0')):
                    raise ValueError('Container deployment paths must be absolute')
                if path.is_symlink() or not path.is_file():
                    raise ValueError('Container deployment input must be a regular file')
                object.__setattr__(self, field, path)

    def command(self, *arguments):
        prefix = []
        if self.storage_conf is not None:
            prefix.append('CONTAINERS_STORAGE_CONF='+str(self.storage_conf))
        if self.containers_conf is not None:
            prefix.append('CONTAINERS_CONF='+str(self.containers_conf))
        if prefix:
            prefix.insert(0, 'env')
        prefix.append(self.kind)
        if self.kind == 'podman':
            prefix += ['--cgroup-manager=cgroupfs', '--events-backend=file']
            if self.runtime is not None:
                prefix += ['--runtime', str(self.runtime)]
        return prefix + list(arguments)

    def create_options(self):
        if self.kind == 'docker':
            return []
        options = ['--userns=keep-id'] + ([] if self.cgroups else ['--cgroups=disabled'])
        if self.proc_mode == 'empty':
            options += ['--tmpfs', '/proc:ro,nosuid,nodev,noexec,size=4k']
        return options

    def resource_options(self, *, memory='4g'):
        if not self.cgroups:
            return []
        return ['--pids-limit', '128', '--memory', memory, '--cpus', '2']

    def owns_name(self, actual, expected):
        return actual == '/'+expected or (self.kind == 'podman' and actual == expected)

    def manifest(self):
        result = dict(kind=self.kind, cgroup_limits=self.cgroups, proc_mode=self.proc_mode)
        for field in ('storage_conf', 'containers_conf', 'runtime'):
            path = getattr(self, field)
            if path is not None:
                result[field+'_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        return result


def add_container_arguments(parser):
    parser.add_argument('--container-engine', choices=('docker', 'podman'), default='docker')
    parser.add_argument('--container-storage-conf', type=Path, help='Trusted project-local Podman storage.conf')
    parser.add_argument('--container-config', type=Path, help='Trusted project-local containers.conf')
    parser.add_argument('--container-runtime', type=Path, help='Trusted project-local OCI runtime executable')
    parser.add_argument('--container-cgroups', choices=('enabled', 'disabled'), default='enabled',
                        help='Explicit deployment capability; never inferred from a failed launch')
    parser.add_argument('--container-proc-mode', choices=('standard', 'empty'), default='standard',
                        help='Podman: empty read-only /proc; preserves private PID/network namespaces')


def engine_from_args(args):
    return ContainerEngine(args.container_engine, storage_conf=args.container_storage_conf,
                           containers_conf=args.container_config, runtime=args.container_runtime,
                           cgroups=args.container_cgroups == 'enabled',
                           proc_mode=getattr(args, 'container_proc_mode', 'standard'))
