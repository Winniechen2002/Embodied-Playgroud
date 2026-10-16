"""Scoped bootstrap for run_isaac_binary.sh and its Python child processes.

Kit's extensions prepend their bundled Python dependencies during startup.
Load the explicitly resolved runtime libraries first, without editing Kit.
This directory is added to PYTHONPATH only by the binary-runtime launcher.
"""
import os

if os.environ.get('AGENTBENCH_ISAAC_BINARY') == '1':
    import sys
    from pathlib import Path
    try:
        import fastapi
        import starlette
        import torch
        prefix = Path(sys.prefix).resolve()
        for module in (fastapi, starlette, torch):
            if not Path(module.__file__).resolve().is_relative_to(prefix):
                raise RuntimeError('Unexpected bundled dependency: ' + module.__name__)
    except Exception as exc:
        # Python ignores ordinary sitecustomize exceptions; a bad runtime must
        # stop before opening the simulator instead of silently falling back.
        raise SystemExit('Isaac binary runtime bootstrap failed: ' + str(exc)) from exc
