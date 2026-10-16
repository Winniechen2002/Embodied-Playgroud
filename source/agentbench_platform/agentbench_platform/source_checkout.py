"""Read-only checkout validation with an ignore rule for materialized LFS files."""
import hashlib
import os
from pathlib import Path
import re
import subprocess


def git_identity(path):
    path = Path(path).resolve()
    command = ['git', '-c', 'filter.lfs.process=', '-c', 'filter.lfs.clean=',
               '-c', 'filter.lfs.required=false', '-C', str(path)]
    environment = dict(os.environ, GIT_OPTIONAL_LOCKS='0')

    def git(*args):
        return subprocess.check_output(command + list(args), env=environment)

    entries = iter(git('status', '--porcelain=v1', '-z').split(b'\0'))
    changed = []
    ignored = []
    for entry in entries:
        if not entry:
            continue
        status, name = entry[:2], os.fsdecode(entry[3:])
        if b'R' in status or b'C' in status:
            next(entries)  # -z includes the original path after a rename/copy.
        target = path / name
        # Ignore only a working-tree expansion of an unchanged index pointer.
        # Staged edits, missing assets, symlinks and changed bytes remain dirty.
        if status == b' M' and target.is_file() and not target.is_symlink():
            pointer = git('show', ':' + name)
            match = re.fullmatch(
                rb'version https://git-lfs.github.com/spec/v1\n'
                rb'oid sha256:([0-9a-f]{64})\nsize ([0-9]+)\n?', pointer)
            if match and target.stat().st_size == int(match[2]):
                digest = hashlib.sha256()
                with target.open('rb') as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                        digest.update(chunk)
                if digest.hexdigest().encode() == match[1]:
                    ignored.append(name)
                    continue
        changed.append(name)
    if changed:
        raise RuntimeError('Checkout is not clean: ' + str(path) + ': ' + ', '.join(changed))
    return dict(path=str(path), revision=git('rev-parse', 'HEAD').decode().strip(),
                clean=True, ignored_materialized_lfs=ignored)
