"""LFS materialization must not hide genuine checkout changes."""
import hashlib
from pathlib import Path
import subprocess

import pytest

from agentbench_platform.source_checkout import git_identity


@pytest.fixture
def checkout(tmp_path):
    root = tmp_path / 'checkout'
    root.mkdir()
    command = ['git', '-c', 'filter.lfs.process=', '-c', 'filter.lfs.clean=',
               '-c', 'filter.lfs.required=false', '-C', str(root)]

    def git(*args):
        return subprocess.check_output(command + list(args), stderr=subprocess.STDOUT)

    git('init')
    (root / '.gitattributes').write_text('*.bin filter=lfs -text\n')
    payload = b'native asset contents\n'
    pointer = ('version https://git-lfs.github.com/spec/v1\n'
               f'oid sha256:{hashlib.sha256(payload).hexdigest()}\nsize {len(payload)}\n')
    (root / 'asset with spaces.bin').write_text(pointer)
    (root / 'source.py').write_text('value = 1\n')
    git('add', '.')
    git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
        'commit', '-m', 'fixture')
    (root / 'asset with spaces.bin').write_bytes(payload)
    return root, git


def test_materialized_lfs_file_is_ignored(checkout):
    root, _ = checkout
    result = git_identity(root)
    assert result['clean']
    assert result['ignored_materialized_lfs'] == ['asset with spaces.bin']


@pytest.mark.parametrize('change', ['asset', 'source', 'staged', 'deleted', 'untracked'])
def test_real_changes_are_not_ignored(checkout, change):
    root, git = checkout
    if change == 'asset':
        # Same byte count, different contents: size alone must not be enough.
        asset = root / 'asset with spaces.bin'
        asset.write_bytes(b'x' * asset.stat().st_size)
    elif change == 'deleted':
        (root / 'asset with spaces.bin').unlink()
    elif change == 'untracked':
        (root / 'new.py').write_text('value = 2\n')
    else:
        (root / 'source.py').write_text('value = 2\n')
        if change == 'staged':
            git('add', 'source.py')
    with pytest.raises(RuntimeError, match='Checkout is not clean'):
        git_identity(root)
