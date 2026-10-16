# Copyright (c) 2025-2026, The DexVerse Project Developers.
# SPDX-License-Identifier: BSD-3-Clause
"""Tensor-only geometry for the dual-Franka bookshelf task (no simulator imports).

World frame: +X points from the robots toward the shelf, +Y runs across the table and
z = 0 is the ground. The shelf-local frame shares the world orientation, so shelf-local
+X is "into the shelf", +Y is "across the shelf" and +Z is up. All lengths are metres.

The scene is a desk with a hutch: the shelf unit stands on the far part of the table
top (its bottom layer is the table surface under the first board) and the two arms stand
on pedestals just beyond the near table edge. The numbers are pinned by a numeric Panda
reach audit (``tests/organize_bookshelf/test_layout.py``): each arm covers its own half
of every layer and both reach the centre; far-side targets need the other arm.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch

# ---------------------------------------------------------------------------
# Desk with a hutch: the shelf unit stands on the far part of the desk top, and the two
# arms stand on pedestals just beyond the near desk edge. The layouts share the robot
# placement and the hutch front, and differ in desk width, hutch size and layer heights,
# blocker height and where the hutch and the crate stand (see ``Layout``).
# ---------------------------------------------------------------------------
TABLE_TOP = 0.56
TABLE_THICKNESS = 0.04
TABLE_NEAR_X = -0.26  # near desk edge; the far edge depends on the layout's hutch depth
BLOCKER_THICKNESS = 0.02  # raised wooden blockers along the open desk edges keep objects on the desk
TABLE_LEG_SIZE = 0.06
TABLE_LEG_INSET = 0.12  # legs inset from every edge: a finger can pass under any free edge
PEDESTAL_SIZE = 0.20
ROBOT_BASE_HEIGHT = 0.80
# Left and right bases on pedestals 0.18 m behind the near desk edge, yaw 0. Standing this far
# back and 0.24 m above the desk keeps the arms extended rather than folded over the near
# edge; the reach audit pins the hutch distance that this placement can still serve.
ROBOT_BASES = ((-0.40, -0.36), (-0.40, 0.36))
BASE_KEEPOUT_RADIUS = 0.08  # no object sampling inside this disc around a base (pedestals stand off the desk)
RESET_REACH_RADIUS = 0.80  # accept a reset pose within this radius of the nearer base
TCP_OFFSET = (0.0, 0.0, 0.1034)  # panda_hand frame -> tool centre point

# Hutch (three layers; the bottom layer is the desk surface under the first board). The
# front face stays at the same distance from the arms in every layout; a shallower hutch
# therefore means a shallower desk, not a longer reach.
SHELF_FRONT_X = 0.20
HUTCH_FRONT_X = SHELF_FRONT_X
SHELF_BOARD_THICKNESS = 0.02
# Clear height above each floor: large object / books / display. The full hutch's top opening
# leaves room for a vertical hand over a 0.15 m object (hand plus wrist reach 0.21 m above the
# tool centre point, checked by the reach audit); the books-only hutch has three equal layers.
FULL_OPENINGS = (0.32, 0.24, 0.36)
BOOK_OPENINGS = (0.24, 0.24, 0.24)
SHELF_QUAT = (1.0, 0.0, 0.0, 0.0)
NUM_LEVELS = 3
LEVEL_LARGE, LEVEL_BOOKS, LEVEL_DISPLAY = 0, 1, 2
LEVEL_BIN = 3  # pseudo-level of trash objects: inside the waste bin beside the desk, not on the hutch
LEVEL_NAMES = ("bottom", "middle", "top")
PLACE_NAMES = LEVEL_NAMES + ("bin",)
SIDE_STRIP_MAX_X = 0.36  # desk beside the hutch is usable for resets up to here (reach)

# Waste bin: an open box standing on the floor against the desk's negative-y side edge, rim
# just below the desk top, so trash can be dropped in from above or slid over the edge.
BIN_WALL = 0.02  # also the floor thickness: objects inside rest well above the ground-contact test
BIN_INNER = (0.30, 0.30, 0.48)  # interior depth (x), width (y) and height
BIN_HEIGHT = BIN_INNER[2] + BIN_WALL
BIN_OUTER = (BIN_INNER[0] + 2 * BIN_WALL, BIN_INNER[1] + 2 * BIN_WALL, BIN_HEIGHT)
BIN_X = -0.15  # bin centre along the desk depth, toward the arms
BIN_PILE_ALLOWANCE = 0.10  # trash may stand this far above the rim and still count as inside


@dataclass(frozen=True)
class Layout:
    """Desk size, hutch size and placement, layer heights and blockers; the robots are shared."""

    name: str
    table_half_width: float
    shelf_inner_width: float
    shelf_center_y: float
    crate_region: tuple  # ((x0, y0), (x1, y1)) for the crate's resting pose on the desk
    shelf_inner_depth: float = 0.24
    openings: tuple = FULL_OPENINGS
    blocker_height: float = 0.12  # above the desk top

    @property
    def floors(self):
        """Top faces of the three floors; the bottom layer is the desk surface."""
        floors, z = [], TABLE_TOP
        for opening in self.openings:
            floors.append(z)
            z += opening + SHELF_BOARD_THICKNESS
        return tuple(floors)

    @property
    def shelf_height(self):
        """Absolute top of the hutch (top face of its top board)."""
        return self.floors[-1] + self.openings[-1] + SHELF_BOARD_THICKNESS

    @property
    def shelf_outer_depth(self):
        return self.shelf_inner_depth + SHELF_BOARD_THICKNESS

    @property
    def table_x(self):
        """Desk depth: the hutch's back panel is flush with the far edge."""
        return (TABLE_NEAR_X, SHELF_FRONT_X + self.shelf_outer_depth)

    @property
    def table_bounds(self):
        return ((self.table_x[0], -self.table_half_width), (self.table_x[1], self.table_half_width))

    @property
    def blockers(self):
        """Env-local boxes of the raised wooden blockers standing on the desk top.

        One blocker runs along each side edge, from the near edge to the hutch front where the
        hutch reaches that side of the desk and over the full depth where the desk continues
        beside it. Where the hutch covers only part of the far edge, a back blocker closes the
        rest of it. The near edge, toward the arms, stays open.
        """
        top = TABLE_TOP + self.blocker_height
        half, t = self.table_half_width, BLOCKER_THICKNESS
        x0, x1 = self.table_x
        low, high = self.hutch_y
        boxes = []
        for sign, hutch_edge in ((-1, low), (1, high)):
            covered = abs(abs(hutch_edge) - half) < 0.01
            end = SHELF_FRONT_X if covered else x1
            y = (-half, -half + t) if sign < 0 else (half - t, half)
            boxes.append(((x0, y[0], TABLE_TOP), (end, y[1], top)))
        for y0, y1 in ((-half, low), (high, half)):
            if y1 - y0 > 0.01:
                boxes.append(((x1 - t, y0, TABLE_TOP), (x1, y1, top)))
        return tuple(boxes)

    @property
    def shelf_outer_width(self):
        return self.shelf_inner_width + 2 * SHELF_BOARD_THICKNESS

    @property
    def shelf_pos(self):
        # Shelf prop origin: front face, hutch centre line, ground.
        return (SHELF_FRONT_X, self.shelf_center_y, 0.0)

    @property
    def hutch_y(self):
        return (self.shelf_center_y - self.shelf_outer_width / 2, self.shelf_center_y + self.shelf_outer_width / 2)

    @property
    def cavity_mins(self):
        return tuple((0.0, -self.shelf_inner_width / 2, floor) for floor in self.floors)

    @property
    def cavity_maxs(self):
        return tuple(
            (self.shelf_inner_depth, self.shelf_inner_width / 2, floor + opening)
            for floor, opening in zip(self.floors, self.openings)
        )

    @property
    def bin_pos(self):
        """Bin prop origin (centre of its outer box footprint, on the ground), env-local."""
        return (BIN_X, -(self.table_half_width + 0.01 + BIN_OUTER[1] / 2), 0.0)

    @property
    def bin_mins(self):
        x, y, _ = self.bin_pos
        return (x - BIN_INNER[0] / 2, y - BIN_INNER[1] / 2, BIN_WALL)

    @property
    def bin_maxs(self):
        x, y, _ = self.bin_pos
        return (x + BIN_INNER[0] / 2, y + BIN_INNER[1] / 2, BIN_HEIGHT)

    @property
    def table_regions(self):
        """Reset regions inside the blockers: the strip in front of the hutch plus free desk beside it."""
        half = self.table_half_width - BLOCKER_THICKNESS
        regions = [((self.table_x[0], -half), (HUTCH_FRONT_X - 0.01, half))]
        low, high = self.hutch_y
        if low - 0.02 - (-half) >= 0.15:
            regions.append(((HUTCH_FRONT_X, -half), (SIDE_STRIP_MAX_X, low - 0.02)))
        if half - (high + 0.02) >= 0.15:
            regions.append(((HUTCH_FRONT_X, high + 0.02), (SIDE_STRIP_MAX_X, half)))
        return tuple(regions)


_FRONT_STRIP = ((-0.20, -0.40), (HUTCH_FRONT_X - 0.02, 0.40))
LAYOUTS = {
    # Books only: a 1.0 m desk with 0.24 m blockers and a lower bookcase of three equal
    # 0.24 m layers spanning the whole back edge.
    "books": Layout("books", 0.50, 0.96, 0.0, _FRONT_STRIP, 0.20, BOOK_OPENINGS, 0.24),
    # Desk organization: a 1.5 m desk whose shallow (0.20 m) hutch spans the whole back edge.
    "centered": Layout("centered", 0.75, 1.46, 0.0, _FRONT_STRIP, 0.20),
    # Relocation: a 1.4 m desk, a 0.24 m deep hutch on the left half and the crate on the right
    # half, so objects are picked on the right and placed on the left (a hand-over between the
    # arms). A back blocker closes the far edge beside the hutch.
    "offset": Layout("offset", 0.70, 0.62, -0.37, ((-0.20, 0.04), (0.36, 0.66)), 0.24),
}
DEFAULT_LAYOUT = LAYOUTS["centered"]
# Default-layout aliases kept for the tests and scripts that only need one layout.
SHELF_OPENINGS = DEFAULT_LAYOUT.openings
SHELF_FLOORS = DEFAULT_LAYOUT.floors
SHELF_HEIGHT = DEFAULT_LAYOUT.shelf_height
TABLE_X = DEFAULT_LAYOUT.table_x
SHELF_INNER_DEPTH = DEFAULT_LAYOUT.shelf_inner_depth
SHELF_OUTER_DEPTH = DEFAULT_LAYOUT.shelf_outer_depth
TABLE_BOUNDS = DEFAULT_LAYOUT.table_bounds
SHELF_INNER_WIDTH = DEFAULT_LAYOUT.shelf_inner_width
SHELF_OUTER_WIDTH = DEFAULT_LAYOUT.shelf_outer_width
SHELF_POS = DEFAULT_LAYOUT.shelf_pos
CAVITY_MINS = DEFAULT_LAYOUT.cavity_mins
CAVITY_MAXS = DEFAULT_LAYOUT.cavity_maxs
TABLE_REGIONS = DEFAULT_LAYOUT.table_regions
TABLE_REGION = TABLE_REGIONS[0]
CRATE_REGION = DEFAULT_LAYOUT.crate_region

# Workspace crop for point clouds and the "lost" envelope (env-local frame, widest desk plus bin).
WORKSPACE_BOUNDS = ((-0.70, -1.1, 0.0), (0.70, 1.1, 1.70))
LOST_BOUNDS = ((-1.2, -1.4, -0.05), (1.2, 1.4, 2.0))
GROUND_CONTACT_Z = 0.008

# ---------------------------------------------------------------------------
# Evaluation tolerances
# ---------------------------------------------------------------------------
CONTAINMENT_TOLERANCE = 0.002
SUPPORT_TOLERANCE = 0.004
UPRIGHT_DEGREES = 10.0
STILL_LINEAR = 0.03
STILL_ANGULAR = 0.15
HOLD_SECONDS = 0.5


def rotation_matrix(q: torch.Tensor) -> torch.Tensor:
    """Normalized wxyz quaternion to rotation matrix; supports arbitrary batch dims."""
    q = q / torch.linalg.vector_norm(q, dim=-1, keepdim=True).clamp_min(1e-12)
    w, x, y, z = q.unbind(-1)
    flat = torch.stack(
        (
            1 - 2 * (y * y + z * z),
            2 * (x * y - w * z),
            2 * (x * z + w * y),
            2 * (x * y + w * z),
            1 - 2 * (x * x + z * z),
            2 * (y * z - w * x),
            2 * (x * z - w * y),
            2 * (y * z + w * x),
            1 - 2 * (x * x + y * y),
        ),
        -1,
    )
    return flat.reshape(*q.shape[:-1], 3, 3)


def box_corners(pos: torch.Tensor, rot: torch.Tensor, sizes: torch.Tensor) -> torch.Tensor:
    """Eight world corners of boxes centred at ``pos`` with full extents ``sizes``.

    ``sizes`` may be ``(S, 3)`` shared across the batch or ``(N, S, 3)``.
    """
    signs = pos.new_tensor(
        [
            (-1, -1, -1),
            (-1, -1, 1),
            (-1, 1, -1),
            (-1, 1, 1),
            (1, -1, -1),
            (1, -1, 1),
            (1, 1, -1),
            (1, 1, 1),
        ]
    )
    local = signs * sizes.unsqueeze(-2) / 2
    return pos.unsqueeze(-2) + torch.einsum("...ij,...kj->...ki", rot, local)


def aabb(pos: torch.Tensor, rot: torch.Tensor, sizes: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Axis-aligned bounds ``(lower, upper)`` of rotated boxes."""
    corners = box_corners(pos, rot, sizes)
    return corners.amin(-2), corners.amax(-2)


def _centered(center, size):
    return (
        tuple(c - s / 2 for c, s in zip(center, size)),
        tuple(c + s / 2 for c, s in zip(center, size)),
    )


def furniture_boxes(layout: Layout = None, with_bin: bool = False) -> tuple:
    """Env-local ``(lower, upper)`` corners of every furniture collider box.

    The desk top, its legs and blockers, the hutch panels and boards, and the waste bin's
    floor and walls, exactly as ``assets.py`` builds them (a test pins the two together).
    """
    layout = layout or DEFAULT_LAYOUT
    boxes = []
    (x0, y0), (x1, y1) = layout.table_bounds
    top = ((x0 + x1) / 2, (y0 + y1) / 2, TABLE_TOP - TABLE_THICKNESS / 2)
    boxes.append(_centered(top, (x1 - x0, y1 - y0, TABLE_THICKNESS)))
    leg_height = TABLE_TOP - TABLE_THICKNESS
    for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        x = top[0] + sx * ((x1 - x0) / 2 - TABLE_LEG_INSET)
        y = top[1] + sy * ((y1 - y0) / 2 - TABLE_LEG_INSET)
        boxes.append(_centered((x, y, leg_height / 2), (TABLE_LEG_SIZE, TABLE_LEG_SIZE, leg_height)))
    boxes.extend(layout.blockers)
    t = SHELF_BOARD_THICKNESS
    depth, width = layout.shelf_inner_depth, layout.shelf_inner_width
    base, roof = layout.floors[0], layout.shelf_height
    height = roof - base
    ox, oy, oz = layout.shelf_pos
    shelf = [((depth + t) / 2, sign * (width / 2 + t / 2), base + height / 2, depth + t, t, height) for sign in (-1, 1)]
    shelf.append((depth + t / 2, 0.0, base + height / 2, t, width + 2 * t, height))
    shelf += [(depth / 2, 0.0, floor - t / 2, depth, width, t) for floor in (*layout.floors[1:], roof)]
    for cx, cy, cz, sx, sy, sz in shelf:
        boxes.append(_centered((ox + cx, oy + cy, oz + cz), (sx, sy, sz)))
    if with_bin:
        bx, by, bz = layout.bin_pos
        outer_x, outer_y = BIN_OUTER[0], BIN_OUTER[1]
        parts = [(0.0, 0.0, BIN_WALL / 2, outer_x, outer_y, BIN_WALL)]
        parts += [
            (s * (outer_x / 2 - BIN_WALL / 2), 0.0, BIN_HEIGHT / 2, BIN_WALL, outer_y, BIN_HEIGHT) for s in (-1, 1)
        ]
        parts += [
            (0.0, s * (outer_y / 2 - BIN_WALL / 2), BIN_HEIGHT / 2, BIN_INNER[0], BIN_WALL, BIN_HEIGHT) for s in (-1, 1)
        ]
        for cx, cy, cz, sx, sy, sz in parts:
            boxes.append(_centered((bx + cx, by + cy, bz + cz), (sx, sy, sz)))
    return tuple(boxes)


def box_penetration(
    pos: torch.Tensor, rot: torch.Tensor, sizes: torch.Tensor, lower: torch.Tensor, upper: torch.Tensor
) -> torch.Tensor:
    """Penetration depth ``(N, S, B)`` of oriented boxes into axis-aligned boxes.

    Separating-axis test over the 15 axes of a box pair: the depth is the smallest overlap
    along any axis, the distance one box must move to clear the other, and 0 when the boxes
    are apart or touching. ``pos (N, S, 3)``, ``rot (N, S, 3, 3)``, ``sizes (S, 3)`` or
    ``(N, S, 3)``, ``lower``/``upper (B, 3)``.
    """
    half = (sizes / 2).expand(pos.shape[0], -1, -1)
    centre = (lower + upper) / 2
    extent = (upper - lower) / 2
    world = torch.eye(3, dtype=pos.dtype, device=pos.device).expand(*pos.shape[:2], 3, 3)
    body = rot.transpose(-1, -2)  # rows are the box axes in world coordinates
    crosses = torch.linalg.cross(
        world[..., :, None, :].expand(-1, -1, 3, 3, 3), body[..., None, :, :].expand(-1, -1, 3, 3, 3)
    )
    axes = torch.cat((world, body, crosses.flatten(2, 3)), -2)  # (N, S, 15, 3)
    norm = torch.linalg.vector_norm(axes, dim=-1)
    valid = norm > 1e-6
    axes = axes / norm.clamp_min(1e-9)[..., None]
    radius_box = (torch.einsum("nsad,nsdi->nsai", axes, rot).abs() * half[..., None, :]).sum(-1)  # (N, S, 15)
    radius_furniture = torch.einsum("nsad,bd->nsab", axes.abs(), extent)  # (N, S, 15, B)
    offset = pos[..., None, :] - centre  # (N, S, B, 3)
    distance = torch.einsum("nsad,nsbd->nsab", axes, offset).abs()
    overlap = radius_box[..., None] + radius_furniture - distance
    overlap = torch.where(valid[..., None], overlap, torch.full_like(overlap, float("inf")))
    return overlap.amin(-2).clamp_min(0.0)


def yawed_extents(half_xy: torch.Tensor, yaw: torch.Tensor) -> torch.Tensor:
    """Half extents of the XY bounding box of a yawed rectangle with half sides ``half_xy``."""
    c, s = yaw.cos().abs(), yaw.sin().abs()
    return torch.stack(
        (c * half_xy[..., 0] + s * half_xy[..., 1], s * half_xy[..., 0] + c * half_xy[..., 1]),
        -1,
    )


def shelf_membership(pos: torch.Tensor, rot: torch.Tensor, sizes: torch.Tensor, layout: Layout = DEFAULT_LAYOUT):
    """Return corners and the supporting compartment index, or -1 outside all levels.

    Inputs are shelf-local. A box belongs to a level when all eight corners lie inside
    that cavity (2 mm tolerance) and its lowest corner rests on the floor board (4 mm).
    """
    corners = box_corners(pos, rot, sizes)
    lower, upper = corners.amin(-2), corners.amax(-2)
    cavity_min, cavity_max = pos.new_tensor(layout.cavity_mins), pos.new_tensor(layout.cavity_maxs)
    inside = (
        (lower[..., None, :] >= cavity_min - CONTAINMENT_TOLERANCE)
        & (upper[..., None, :] <= cavity_max + CONTAINMENT_TOLERANCE)
    ).all(-1)
    supported = (lower[..., 2, None] - cavity_min[:, 2]).abs() <= SUPPORT_TOLERANCE
    eligible = inside & supported
    level = torch.where(eligible.any(-1), eligible.int().argmax(-1), -1)
    return corners, level


def centre_level(pos: torch.Tensor, layout: Layout = DEFAULT_LAYOUT) -> torch.Tensor:
    """Compartment whose cavity contains the object centre, or -1 (shelf-local positions).

    Used for trash, whose lumpy meshes make the corners of its rule box a poor guide to
    where it rests; like the bin rule, it judges trash by its centre.
    """
    cavity_min, cavity_max = pos.new_tensor(layout.cavity_mins), pos.new_tensor(layout.cavity_maxs)
    inside = ((pos[..., None, :] >= cavity_min) & (pos[..., None, :] <= cavity_max)).all(-1)
    return torch.where(inside.any(-1), inside.int().argmax(-1), -1)


def bin_membership(pos: torch.Tensor, layout: Layout = DEFAULT_LAYOUT, shelf_local: bool = True) -> torch.Tensor:
    """Objects whose centre lies inside the waste bin's interior footprint, up to a pile above the rim.

    ``pos`` is shelf-local by default (the evaluator's frame); the bin bounds are env-local.
    """
    lo, hi = pos.new_tensor(layout.bin_mins), pos.new_tensor(layout.bin_maxs)
    if shelf_local:
        shelf = pos.new_tensor(layout.shelf_pos)
        lo, hi = lo - shelf, hi - shelf
    hi = hi + pos.new_tensor((0.0, 0.0, BIN_PILE_ALLOWANCE))
    return ((pos >= lo) & (pos <= hi)).all(-1)


def upright_flags(rot: torch.Tensor, max_degrees: float = UPRIGHT_DEGREES) -> torch.Tensor:
    """Object +Z within ``max_degrees`` of shelf +Z."""
    return rot[..., 2, 2] >= math.cos(math.radians(max_degrees))


def yaw_aligned_flags(rot: torch.Tensor, max_degrees: float = UPRIGHT_DEGREES) -> torch.Tensor:
    """Object +Y (book thickness axis) parallel or anti-parallel to shelf +Y."""
    return rot[..., 1, 1].abs() >= math.cos(math.radians(max_degrees))


def facing_flags(rot: torch.Tensor, max_degrees: float = 20.0) -> torch.Tensor:
    """Object -X (picture side of a frame) within ``max_degrees`` of shelf -X (outward)."""
    return rot[..., 0, 0] >= math.cos(math.radians(max_degrees))


def still_flags(lin_vel: torch.Tensor, ang_vel: torch.Tensor) -> torch.Tensor:
    return (torch.linalg.vector_norm(lin_vel, dim=-1) < STILL_LINEAR) & (
        torch.linalg.vector_norm(ang_vel, dim=-1) < STILL_ANGULAR
    )


def placement_flags(
    pos: torch.Tensor,
    rot: torch.Tensor,
    lin_vel: torch.Tensor,
    ang_vel: torch.Tensor,
    released: torch.Tensor,
    sizes: torch.Tensor,
    required_level: torch.Tensor,
    yaw_mask: torch.Tensor | None = None,
    layout: Layout = DEFAULT_LAYOUT,
) -> dict:
    """Current shelf occupancy per slot (shelf frame), independent of milestone history.

    ``yaw_mask`` selects slots (books) that must also have their covers parallel to the
    side walls. ``required_level`` is ``(S,)`` or ``(N, S)`` with -1 for absent slots.
    """
    corners, level = shelf_membership(pos, rot, sizes, layout)
    upright = upright_flags(rot)
    aligned = upright if yaw_mask is None else upright & (yaw_aligned_flags(rot) | ~yaw_mask)
    required = torch.as_tensor(required_level, device=pos.device).expand_as(level)
    inserted = (level >= 0) & aligned
    correct = level == required
    return {
        "corners": corners,
        "level": level,
        "upright": upright,
        "inserted": inserted,
        "correct_level": correct,
        "wrong_level": (level >= 0) & ~correct,
        "placed": inserted & correct & still_flags(lin_vel, ang_vel) & released,
    }


def lost_flags(
    pos: torch.Tensor, rot: torch.Tensor, sizes: torch.Tensor, present: torch.Tensor, layout: Layout | None = None
) -> torch.Tensor:
    """Failure when any present object leaves the workspace or touches the ground.

    Inputs are env-local. With a ``layout`` the ground test skips objects standing over the
    bin's interior footprint: they rest on the bin floor, and the box bottom of a tumbling
    lumpy object can dip below the floor level without the object being on the ground.
    """
    lo, hi = pos.new_tensor(LOST_BOUNDS)
    outside = ((pos < lo) | (pos > hi) | ~torch.isfinite(pos)).any(-1)
    bottom = box_corners(pos, rot, sizes)[..., 2].amin(-1)
    grounded = bottom < GROUND_CONTACT_Z
    if layout is not None:
        bin_lo, bin_hi = pos.new_tensor(layout.bin_mins[:2]), pos.new_tensor(layout.bin_maxs[:2])
        over_bin = ((pos[..., :2] >= bin_lo) & (pos[..., :2] <= bin_hi)).all(-1)
        grounded &= ~over_bin
    present = torch.as_tensor(present, device=pos.device).expand_as(outside)
    return ((outside | grounded) & present).any(-1)


class HoldCounter:
    """One update per step; explicit subset reset handles repeated reset at step zero."""

    def __init__(self, count, device, duration=HOLD_SECONDS):
        self.elapsed = torch.zeros(count, device=device)
        self.last_step = torch.full((count,), -1, dtype=torch.long, device=device)
        self.duration = duration

    def reset(self, ids):
        self.elapsed[ids] = 0
        self.last_step[ids] = -1

    def update(self, valid, step, dt):
        new = step != self.last_step
        self.elapsed = torch.where(new & valid, self.elapsed + dt, torch.where(new, 0.0, self.elapsed))
        self.last_step = step.clone()
        return self.elapsed >= self.duration - 1e-6
