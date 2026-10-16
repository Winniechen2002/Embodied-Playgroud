"""Dependency-light solver extension point for Rubik's Cube state clients."""

from __future__ import annotations

from typing import Protocol
from pathlib import Path
import json
import os
import random
import subprocess
import sys

try:
    from .rubiks_cube_rules import CubeState
except ImportError:  # Loaded directly by dependency-light unit tests.
    from rubiks_cube_rules import CubeState


class CubeSolver(Protocol):
    """Return a symbolic solution without access to physical session internals."""

    def solve(self, state: CubeState) -> tuple[str, ...]: ...


SOLVED_FACELETS = "".join(face * 9 for face in "URFDLB")


def is_color_solved(state: CubeState) -> bool:
    """Ordinary cube completion ignores the axial spin of single-color centers."""
    return state.facelet_string() == SOLVED_FACELETS


def generate_scramble(length: int = 4, seed: int = 7) -> tuple[str, ...]:
    if type(length) is not int or not 0 <= length <= 100:
        raise ValueError("scramble length must be an integer between 0 and 100")
    if type(seed) is not int:
        raise ValueError("seed must be an integer")
    rng = random.Random(seed)
    moves = []
    for _ in range(length):
        faces = [face for face in "URFDLB" if not moves or face != moves[-1][0]]
        moves.append(rng.choice(faces) + rng.choice(("", "'", "2")))
    return tuple(moves)


def to_solver_facelets(state: CubeState) -> str:
    """Convert URFDLB face labels to cube-solver's ULFRBD color convention."""
    facelets = state.facelet_string()
    if len(facelets) != 54 or any(facelets.count(face) != 9 for face in "URFDLB"):
        raise ValueError("invalid cube facelets")
    colors = str.maketrans(dict(zip("URFDLB", "WRGYOB")))
    return "".join(facelets[9 * "URFDLB".index(face):9 * ("URFDLB".index(face) + 1)]
                   for face in "ULFRBD").translate(colors)


class KociembaSolver:
    """Bounded solver worker; its cwd isolates the library's relative table cache.

    No scramble or robot API is sent to the worker. The cache lock also prevents
    two first-time clients from concurrently writing the same generated tables.
    """

    def __init__(self, *, timeout_s: int = 10, cache_dir=None):
        if type(timeout_s) is not int or timeout_s <= 0:
            raise ValueError("solver timeout must be a positive integer")
        self.timeout_s = timeout_s
        self.cache_dir = Path(cache_dir or os.environ.get(
            "RUBIKS_SOLVER_CACHE", Path.home() / ".cache/agentbench/cube-solver-1.1.4"
        )).expanduser().resolve()
        self.last_report = None
        self._prepared = False

    def _worker(self, request, timeout):
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--worker"],
            input=json.dumps(request), text=True, capture_output=True,
            cwd=self.cache_dir, timeout=timeout, check=False,
        )
        if completed.returncode:
            raise RuntimeError(f"cube solver failed: {completed.stderr[-2000:]}")
        return json.loads(completed.stdout)

    def prepare(self):
        """Generate/load tables before a simulation is launched (15 minute cap)."""
        result = self._worker({"prepare": True}, 900)
        self._prepared = True
        return result

    def solve(self, state: CubeState) -> tuple[str, ...]:
        if is_color_solved(state):
            self.last_report = {"solution": [], "already_solved": True, "search_timed_out": False}
            return ()
        if not self._prepared:
            self.prepare()
        result = self._worker({"facelets": to_solver_facelets(state),
                               "timeout_s": self.timeout_s}, self.timeout_s + 30)
        moves = tuple(result["solution"])
        if not moves or not is_color_solved(state.apply_sequence(moves)):
            raise ValueError("solver solution failed independent cube-state replay")
        self.last_report = result
        return moves


def _worker_main():
    import fcntl
    import time
    from importlib.metadata import version
    from cube_solver import Cube, Kociemba

    if version("cube-solver") != "1.1.4":
        raise RuntimeError("cube-solver==1.1.4 is required")
    request = json.load(sys.stdin)
    with open("tables.lock", "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        solver = Kociemba()
    if request.get("prepare"):
        print(json.dumps({"ready": True, "version": "1.1.4"}))
        return
    started = time.monotonic()
    solution = solver.solve(Cube(repr=request["facelets"]), optimal=True,
                            max_length=30, timeout=request["timeout_s"])
    if solution is None:
        raise RuntimeError("no solution within solver search budget")
    print(json.dumps({"solution": str(solution).split(), "version": "1.1.4",
                      "search_timed_out": solver.terminated,
                      "search_wall_s": time.monotonic() - started}))


if __name__ == "__main__":
    _worker_main()
