"""Environment-owned physical shapes and neutral data types; no solved route."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from itertools import product
from collections import Counter
from pathlib import Path
from typing import Iterable, Mapping, Sequence
import json
import numpy as np
GRID_CELL_M = .025
BAR_LENGTH_CELLS = 8
BAR_WIDTH_CELLS = 2
TABLE_TOP_Z = .60
LOCK_CENTER_XY = np.array((.70, 0.), dtype=np.float64)
PIECE_NAMES = ('frame_x0', 'frame_x1', 'frame_y0', 'frame_y1', 'frame_z0', 'key')
AXES = ('x', 'y', 'z')
Cell = tuple[int, int, int]
SPEC_PATH = Path(__file__).with_name('shape_v1.json')
class TaskMode(str, Enum):
    """Direction of the eventual manipulation task."""

    DISASSEMBLE = "disassemble"
    ASSEMBLE = "assemble"

class AssemblyPhase(str, Enum):
    """Episode-level progress, separate from the manipulation waypoint phase."""

    DISASSEMBLED = "disassembled"
    ASSEMBLY_IN_PROGRESS = "assembly_in_progress"
    ASSEMBLED = "assembled"
    FAILED = "failed"

class LockPhase(str, Enum):
    """Observable phases shared by the disassembly and future assembly tasks."""

    ASSEMBLED = "assembled"
    APPROACH = "approach"
    GRASP = "grasp"
    STABILIZE = "stabilize"
    SLIDE = "slide"
    LIFT = "lift"
    TRANSPORT = "transport"
    PLACE = "place"
    RELEASE = "release"
    DISASSEMBLED = "disassembled"
    FAILED = "failed"

@dataclass(frozen=True)
class PieceSpec:
    """One rigid wood piece represented by occupied lattice cells.

    ``origin`` is the grid coordinate of the local bar's longitudinal cell 0.
    The generated USD is centred around the local bar bounding box, so the
    world pose is derived from this origin and the axis.
    """

    name: str
    family: str
    axis: str
    origin: Cell
    cells: tuple[Cell, ...]
    assembly_position: tuple[float, float, float]
    assembly_quat_wxyz: tuple[float, float, float, float]
    target_position: tuple[float, float, float]
    target_quat_wxyz: tuple[float, float, float, float]

    def __post_init__(self) -> None:
        if self.axis not in AXES:
            raise ValueError(f"unsupported piece axis: {self.axis}")
        if not self.cells:
            raise ValueError(f"piece {self.name} has no cells")
        if len(set(self.cells)) != len(self.cells):
            raise ValueError(f"piece {self.name} has duplicate cells")

@dataclass
class PuzzleState:
    """Logical state reconstructed from measured rigid-body poses."""

    mode: TaskMode = TaskMode.DISASSEMBLE
    phase: LockPhase = LockPhase.ASSEMBLED
    removed: list[str] = field(default_factory=list)
    placed: list[str] = field(default_factory=list)
    assembled: list[str] = field(default_factory=list)
    active_piece: str | None = None
    move_index: int = 0
    failure_reason: str | None = None

    def copy(self) -> "PuzzleState":
        return PuzzleState(
            mode=self.mode,
            phase=self.phase,
            removed=list(self.removed),
            placed=list(self.placed),
            assembled=list(self.assembled),
            active_piece=self.active_piece,
            move_index=self.move_index,
            failure_reason=self.failure_reason,
        )

def _axis_index(axis: str) -> int:
    return AXES.index(axis)

def _local_bar_cells(axis: str, origin: Cell) -> tuple[Cell, ...]:
    """Return a complete 8x2x2 bar before shared cells are assigned."""

    axis_index = _axis_index(axis)
    cross_axes = [index for index in range(3) if index != axis_index]
    cells: list[Cell] = []
    for longitudinal in range(BAR_LENGTH_CELLS):
        for cross0, cross1 in product(range(BAR_WIDTH_CELLS), repeat=2):
            value = list(origin)
            value[axis_index] += longitudinal
            value[cross_axes[0]] += cross0
            value[cross_axes[1]] += cross1
            cells.append(tuple(value))
    return tuple(cells)

def _quaternion_for_axis(axis: str) -> tuple[float, float, float, float]:
    half = float(np.sqrt(0.5))
    if axis == "x":
        return (1.0, 0.0, 0.0, 0.0)
    if axis == "y":
        return (half, 0.0, 0.0, half)
    if axis == "z":
        return (half, 0.0, -half, 0.0)
    raise ValueError(axis)

def _grid_to_world(origin: Cell, axis: str, *, center_xy: Sequence[float] = LOCK_CENTER_XY) -> tuple[float, float, float]:
    """World position of the centred local USD asset."""

    axis_index = _axis_index(axis)
    cross_axes = [index for index in range(3) if index != axis_index]
    local_center = np.zeros(3, dtype=np.float64)
    local_center[axis_index] = (BAR_LENGTH_CELLS - 1) * 0.5
    local_center[cross_axes] = (BAR_WIDTH_CELLS - 1) * 0.5
    grid_position = np.asarray(origin, dtype=np.float64) + local_center
    world = np.array((center_xy[0], center_xy[1], TABLE_TOP_Z), dtype=np.float64)
    world += grid_position * GRID_CELL_M
    world += GRID_CELL_M * 0.5
    world[2] += GRID_CELL_M * (BAR_LENGTH_CELLS * 0.5)
    return tuple(float(value) for value in world)

def _target_positions() -> dict[str, tuple[float, float, float]]:
    """Versioned parking poses include clearance for the robot grippers."""
    raw=json.loads(SPEC_PATH.read_text())
    return {name:tuple(value) for name,value in raw['parking_positions_m'].items()}

def _is_6_connected(cells: Iterable[Cell]) -> bool:
    """Return whether occupied voxels form one face-connected rigid piece."""

    cells = set(cells)
    if not cells:
        return False
    pending = [next(iter(cells))]
    seen = set(pending)
    while pending:
        current = pending.pop()
        for axis in range(3):
            for direction in (-1, 1):
                delta = [0, 0, 0]
                delta[axis] = direction
                delta = tuple(delta)
                neighbour = tuple(current[index] + delta[index] for index in range(3))
                if neighbour in cells and neighbour not in seen:
                    seen.add(neighbour)
                    pending.append(neighbour)
    return len(seen) == len(cells)

def _valid_assembly_cells(pieces: Sequence[PieceSpec]) -> tuple[Cell, ...]:
    cells: list[Cell] = []
    for piece in pieces:
        cells.extend(piece.cells)
    if len(cells) != len(set(cells)):
        raise ValueError("assembled puzzle contains overlapping cells")
    return tuple(sorted(set(cells)))

def local_voxel_indices(piece: PieceSpec) -> tuple[Cell, ...]:
    """Integer cells in the USD stock frame: long X, two-cell Y and Z."""
    cells = []
    for cell in piece.cells:
        x, y, z = (cell[i] - piece.origin[i] for i in range(3))
        cells.append((x, y, z) if piece.axis == "x" else
                     (y, 1-x, z) if piece.axis == "y" else (z, y, 1-x))
    return tuple(sorted(cells))

def maximal_cuboids(piece: PieceSpec) -> tuple[tuple[Cell, Cell], ...]:
    """Overlapping maximal boxes exactly cover the occupied lattice cells.

    Overlap inside a single rigid body preserves solid joints between the
    narrow spine and wider ends after the external fit clearance is applied.
    """
    cells = set(local_voxel_indices(piece))
    ranges = [range(min(c[i] for c in cells), max(c[i] for c in cells)+1) for i in range(3)]
    def contained(lo, hi):
        return all(c in cells for c in product(*(range(lo[i], hi[i]+1) for i in range(3))))
    boxes = []
    for intervals in product(*[tuple((a,b) for a in values for b in values if a<=b) for values in ranges]):
        lo, hi = tuple(v[0] for v in intervals), tuple(v[1] for v in intervals)
        if not contained(lo, hi):
            continue
        maximal = True
        for axis in range(3):
            for sign in (-1, 1):
                a, b = list(lo), list(hi)
                if sign < 0: a[axis] -= 1
                else: b[axis] += 1
                if contained(a, b): maximal = False
        if maximal: boxes.append((lo,hi))
    return tuple(sorted(boxes))

def collision_boxes(piece: PieceSpec, inset_m: float | None = None):
    """Local centers and half extents shared by USD, runtime and evaluator."""
    inset = float(CANONICAL_SPEC.metadata['collision_inset_m'] if inset_m is None else inset_m)
    if not 0 <= inset < GRID_CELL_M/2:
        raise ValueError('collision inset must preserve positive box dimensions')
    boxes = np.asarray(maximal_cuboids(piece), dtype=float)
    centers = ((boxes[:,0]+boxes[:,1])/2-np.array([3.5,.5,.5]))*GRID_CELL_M
    half = (boxes[:,1]-boxes[:,0]+1)*GRID_CELL_M/2-inset
    return centers, half

def translate_cells(cells: Iterable[Cell], offset: Cell) -> set[Cell]:
    return {tuple(c[i] + offset[i] for i in range(3)) for c in cells}

@dataclass(frozen=True)
class ShapeSpec:
    name: str
    version: str
    cell_size_m: float
    pieces: tuple[PieceSpec, ...]
    assembly_occupancy: tuple[Cell, ...]
    metadata: Mapping[str, object]
    @property
    def piece_names(self): return tuple(p.name for p in self.pieces)
    def piece(self, name): return next(p for p in self.pieces if p.name == name)


def build_shape_spec():
    raw = json.loads(SPEC_PATH.read_text())
    targets = _target_positions()
    pieces = tuple(PieceSpec(name=r['name'], family=r['family'], axis=r['axis'], origin=tuple(r['origin']),
        cells=tuple(map(tuple, r['cells'])), assembly_position=_grid_to_world(tuple(r['origin']), r['axis']),
        assembly_quat_wxyz=_quaternion_for_axis(r['axis']), target_position=targets[r['name']],
        target_quat_wxyz=tuple(raw['parking_quaternions_wxyz'][r['name']])) for r in raw['pieces'])
    return ShapeSpec(raw['name'], raw['version'], GRID_CELL_M, pieces, _valid_assembly_cells(pieces), raw)

CANONICAL_SPEC = build_shape_spec()

# Pure-module importers (asset tools/reference policies) must share enum identity
# with the registered Isaac package without importing task registration itself.
import sys as _sys
_shared_name = '_agentbench_kongming_physical_shapes'
_shared = _sys.modules.setdefault(_shared_name, _sys.modules[__name__])
if _shared is not _sys.modules[__name__]:
    globals().update({k: v for k, v in vars(_shared).items() if not k.startswith('__')})
