"""Runs only inside the disposable, offline image build filesystem."""
from pathlib import Path
import importlib.metadata
import shutil
import subprocess

subprocess.run(['python3','-m','pip','install','--no-index','--no-cache-dir','--require-hashes',
                '--find-links=/build/wheels','-r','/build/requirements.lock'],check=True)
assert importlib.metadata.version('cube-solver')=='1.1.4'
shutil.copytree('/build/runtime','/opt/worker')
root=Path('/opt/worker')
for path in [root,*root.rglob('*')]:path.chmod(0o755 if path.is_dir() else 0o644)
shutil.rmtree('/build')
