"""Maintainer process boundary for an episode's hard wall-clock deadline."""
import json
import os
from pathlib import Path
import signal
import subprocess
import time


def _stop(child):
    try:os.killpg(child.pid,signal.SIGTERM)
    except ProcessLookupError:pass
    try:child.wait(timeout=5.)
    except subprocess.TimeoutExpired:
        try:os.killpg(child.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        child.wait()


def supervise(command, *, seconds, output, environment=None):
    start=time.monotonic()
    child=subprocess.Popen(command,env=environment,start_new_session=True)
    try:
        return child.wait(timeout=seconds)
    except subprocess.TimeoutExpired:
        _stop(child)
        directory=Path(output);directory.mkdir(parents=True,exist_ok=True)
        (directory/'supervisor-result.private.json').write_text(json.dumps(dict(
            outcome='invalid',reason='wall_timeout',wall_seconds=time.monotonic()-start,
            configured_wall_seconds=seconds,child_returncode=child.returncode),indent=2)+'\n')
        return 124
    except BaseException:
        if child.poll() is None:
            _stop(child)
        raise
