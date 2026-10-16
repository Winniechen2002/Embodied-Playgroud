# Copyright (c) 2025-2026, The DexVerse Project Developers.
# SPDX-License-Identifier: BSD-3-Clause
"""Per-class placement rules evaluated in the shelf frame (tensor-only).

Books on the middle layer must form one tightly packed row anchored against a side wall.
Display objects on the top layer must stand apart from each other and from the walls, and
a photo frame must face outward. The large objects (crate or boxes) must stand upright on
the bottom layer, and a crate must be empty. Trash objects must lie inside the waste bin
beside the desk. ``slot_rules`` combines everything into a single per-environment
``valid`` flag; the environment turns that into success after a dwell. All inputs are
shelf-local and masked by the slot table's ``present`` flags.
"""

from __future__ import annotations

import math

import torch

from .geometry import (
    BIN_WALL,
    DEFAULT_LAYOUT,
    LEVEL_BIN,
    LEVEL_BOOKS,
    LEVEL_DISPLAY,
    LEVEL_LARGE,
    aabb,
    bin_membership,
    box_corners,
    centre_level,
    facing_flags,
    placement_flags,
    still_flags,
)

PACK_MAX_GAP = 0.006
PACK_ALIGN_DEGREES = 3.0
PACK_BACK_TOLERANCE = 0.015
DISPLAY_MIN_GAP = 0.05
DISPLAY_WALL_MARGIN = 0.02
WALL_ANCHORS = ("either", "negative_y", "positive_y")
FACING_DEGREES = 20.0


def mirror_y(pos: torch.Tensor, rot: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Reflect poses across the shelf's centre plane; symmetric boxes keep their shape."""
    flip = pos.new_tensor((1.0, -1.0, 1.0))
    return pos * flip, flip[:, None] * rot * flip[None, :]


def _packed_row(pos, rot, sizes, members, max_gap, wall_y):
    """Check one row of boxes packed against the wall at ``wall_y`` (negative side).

    Generalizes the three-book check: consecutive Y-sorted members must touch cover to
    cover (gap within [-2 mm, ``max_gap``]), the first member's cover must touch the wall,
    all members must be aligned within 3 degrees, and their backs or their fronts within
    15 mm (books of different depths line up on one side).
    """
    count, slots = pos.shape[:2]
    order = pos[..., 1].masked_fill(~members, float("inf")).argsort(-1)
    active = members.gather(1, order)
    p = pos.gather(1, order[..., None].expand(-1, -1, 3))
    r = rot.gather(1, order[..., None, None].expand(-1, -1, 3, 3))
    h = sizes.expand(count, -1, -1).gather(1, order[..., None].expand(-1, -1, 3)) / 2
    n = r[..., :, 1] * torch.where(r[..., 1, 1] >= 0, 1.0, -1.0)[..., None]
    cos_align = math.cos(math.radians(PACK_ALIGN_DEGREES))
    aligned = (((r[..., 2, 2] >= cos_align) & (r[..., 1, 1].abs() >= cos_align)) | ~active).all(-1)
    # Full wall-side cover of the first member must be near the wall.
    wall_local = p.new_tensor([[-1, 0, -1], [-1, 0, 1], [1, 0, -1], [1, 0, 1]])[None] * h[:, 0, None, :]
    wall_local[:, :, 1] = -torch.sign(r[:, 0, 1, 1])[:, None] * h[:, 0, 1, None]
    wall = p[:, 0, None, :] + torch.einsum("nij,nkj->nki", r[:, 0], wall_local)
    wall_gap = wall[..., 1] - wall_y
    packed = aligned & ((wall_gap >= -0.002) & (wall_gap <= max_gap)).all(-1)
    max_pair_gap = pos.new_zeros(count)
    for a in range(slots - 1):
        b = a + 1
        # Central 60% of shared depth/height; reject staggering with small overlap.
        lo = torch.maximum(p[:, a, (0, 2)] - 0.6 * h[:, a, (0, 2)], p[:, b, (0, 2)] - 0.6 * h[:, b, (0, 2)])
        hi = torch.minimum(p[:, a, (0, 2)] + 0.6 * h[:, a, (0, 2)], p[:, b, (0, 2)] + 0.6 * h[:, b, (0, 2)])
        pair_ok = ((hi - lo) >= 0.5 * torch.minimum(h[:, a, (0, 2)], h[:, b, (0, 2)])).all(-1)
        xz = torch.stack((lo, torch.stack((lo[:, 0], hi[:, 1]), -1), torch.stack((hi[:, 0], lo[:, 1]), -1), hi), 1)
        surfaces = []
        for i, sign in ((a, 1), (b, -1)):
            y = p[:, i, 1, None] + (
                sign * h[:, i, 1, None]
                - n[:, i, 0, None] * (xz[:, :, 0] - p[:, i, 0, None])
                - n[:, i, 2, None] * (xz[:, :, 1] - p[:, i, 2, None])
            ) / n[:, i, 1, None].clamp_min(1e-6)
            points = torch.stack((xz[:, :, 0], y, xz[:, :, 1]), -1)
            local = torch.einsum("nji,nkj->nki", r[:, i], points - p[:, i, None, :])
            pair_ok &= (local[:, :, (0, 2)].abs() <= h[:, i, None, (0, 2)] + 0.002).all(dim=(-1, -2))
            surfaces.append(y)
        gap = surfaces[1] - surfaces[0]
        max_pair_gap = torch.maximum(max_pair_gap, torch.where(active[:, b], gap.amax(-1), 0.0))
        pair_ok &= ((gap >= -0.002) & (gap <= max_gap)).all(-1)
        packed &= pair_ok | ~active[:, b]
    corners = box_corners(p, r, h * 2)
    # Books of different depths line up either at the back or at the front of the row.
    spreads = []
    for edge in (corners[..., 0].amax(-1), corners[..., 0].amin(-1)):
        spreads.append(
            edge.masked_fill(~active, -float("inf")).amax(-1) - edge.masked_fill(~active, float("inf")).amin(-1)
        )
    packed &= (spreads[0] <= PACK_BACK_TOLERANCE) | (spreads[1] <= PACK_BACK_TOLERANCE)
    occupied = active.any(-1)
    gap = torch.where(occupied, torch.maximum(max_pair_gap, wall_gap.amax(-1)), 0.0)
    return packed | ~occupied, gap


def packed_row(
    pos, rot, sizes, members, *, max_gap=PACK_MAX_GAP, anchor="either", level=LEVEL_BOOKS, layout=DEFAULT_LAYOUT
):
    """Books in ``members`` form one packed row against a side wall of ``level``.

    Returns ``(packed, gap, wall)`` where ``wall`` is -1 or +1 for the anchoring wall and 0
    when the row is not packed (or empty). ``anchor`` selects which walls are acceptable.
    """
    if anchor not in WALL_ANCHORS:
        raise ValueError(f"anchor must be one of {WALL_ANCHORS}, got {anchor!r}")
    sizes = sizes if sizes.dim() == 3 else sizes.expand(pos.shape[0], -1, -1)
    neg_ok, neg_gap = _packed_row(pos, rot, sizes, members, max_gap, layout.cavity_mins[level][1])
    mirrored_pos, mirrored_rot = mirror_y(pos, rot)
    pos_ok, pos_gap = _packed_row(mirrored_pos, mirrored_rot, sizes, members, max_gap, -layout.cavity_maxs[level][1])
    occupied = members.any(-1)
    if anchor == "negative_y":
        pos_ok = ~occupied
    elif anchor == "positive_y":
        neg_ok = ~occupied
    packed = neg_ok | pos_ok
    wall = torch.where(occupied & neg_ok, -1, torch.where(occupied & pos_ok, 1, 0))
    gap = torch.where(neg_ok, neg_gap, torch.where(pos_ok, pos_gap, torch.minimum(neg_gap, pos_gap)))
    return packed, gap, wall


def footprint_separation(pos, rot, sizes):
    """Pairwise separation ``(N, S, S)`` between the horizontal footprints of upright boxes.

    Separating-axis distance over both rectangles' in-plane axes: exact when the closest
    features are edge to edge or edge to vertex, a lower bound otherwise. Negative values
    mean the footprints overlap.
    """
    count, slots = pos.shape[:2]
    centers = pos[..., :2]
    axes = rot[..., :2, :2]
    axes = axes / torch.linalg.vector_norm(axes, dim=-2, keepdim=True).clamp_min(1e-6)
    half = (sizes[..., :2] / 2).expand(count, -1, -1)
    delta = centers[:, None, :, :] - centers[:, :, None, :]  # (N, S, S, 2) from i to j
    separations = []
    for owner in (0, 1):
        for column in (0, 1):
            unit = axes[..., :, column]  # (N, S, 2)
            unit = unit[:, :, None, :] if owner == 0 else unit[:, None, :, :]
            unit = unit.expand(count, slots, slots, 2)
            extent_i = (torch.einsum("nijr,nirc->nijc", unit, axes).abs() * half[:, :, None, :]).sum(-1)
            extent_j = (torch.einsum("nijr,njrc->nijc", unit, axes).abs() * half[:, None, :, :]).sum(-1)
            separations.append((delta * unit).sum(-1).abs() - extent_i - extent_j)
    return torch.stack(separations, -1).amax(-1)


def spaced_row(
    pos,
    rot,
    sizes,
    members,
    *,
    min_gap=DISPLAY_MIN_GAP,
    wall_margin=DISPLAY_WALL_MARGIN,
    level=LEVEL_DISPLAY,
    layout=DEFAULT_LAYOUT,
):
    """Display objects in ``members`` are separated from each other and from the side walls.

    Pair separation is the footprint distance (objects may also sit one behind the other);
    wall margins use the bounding box. Returns ``(spaced, min_separation)`` where the
    separation is the smallest pair gap or wall margin among members (0 when empty).
    """
    lower, upper = aabb(pos, rot, sizes)
    cavity_min, cavity_max = layout.cavity_mins[level], layout.cavity_maxs[level]
    wall_margins = torch.minimum(lower[..., 1] - cavity_min[1], cavity_max[1] - upper[..., 1])
    wall_ok = ((wall_margins >= wall_margin - 1e-6) | ~members).all(-1)
    separation = footprint_separation(pos, rot, sizes)
    pairs = members[:, :, None] & members[:, None, :] & ~torch.eye(pos.shape[1], dtype=torch.bool, device=pos.device)
    pair_ok = ((separation >= min_gap - 1e-6) | ~pairs).all(dim=(-1, -2))
    inf = float("inf")
    smallest = torch.minimum(
        separation.masked_fill(~pairs, inf).amin(dim=(-1, -2)),
        wall_margins.masked_fill(~members, inf).amin(-1),
    )
    smallest = torch.where(members.any(-1), smallest, torch.zeros_like(smallest))
    return wall_ok & pair_ok, smallest


CRATE_PILE_ALLOWANCE = 0.12  # a jumbled pile may stand this far above the rim and still count as inside


def in_crate(pos, rot, sizes, present, crate_slot, interior, crate_height):
    """Objects whose centre lies inside the crate's interior footprint, up to a pile above the rim."""
    crate_pos, crate_rot = pos[:, crate_slot], rot[:, crate_slot]
    relative = torch.einsum("nji,nsj->nsi", crate_rot, pos - crate_pos[:, None, :])
    inside = (
        (relative[..., 0].abs() <= interior[0] / 2)
        & (relative[..., 1].abs() <= interior[1] / 2)
        & (relative[..., 2] < crate_height / 2 + CRATE_PILE_ALLOWANCE)
        & (relative[..., 2] > -crate_height / 2 - 0.02)
    )
    inside &= present
    inside[:, crate_slot] = False
    return inside & present[:, crate_slot, None]


def slot_rules(
    pos, rot, lin_vel, ang_vel, released, slots, *, wall_anchor="either", crate_interior=None, layout=DEFAULT_LAYOUT
):
    """Evaluate every present slot against its class rule; see the module docstring."""
    present, sizes = slots["present"], slots["sizes"]
    present = present.expand(pos.shape[0], -1)
    placement = placement_flags(
        pos, rot, lin_vel, ang_vel, released, sizes, slots["required_level"], slots["is_book"], layout=layout
    )
    level = placement["level"]
    trash = slots["is_trash"].expand_as(present)
    if trash.any():
        # Trash is placed inside the bin, not on the hutch: orientation is free, and a trash
        # object whose centre is inside a compartment counts as a wrong level.
        binned = bin_membership(pos, layout) & trash & present
        level = torch.where(trash, centre_level(pos, layout), level)
        placement["level"] = level
        still = still_flags(lin_vel, ang_vel)
        placement["inserted"] = torch.where(trash, binned, placement["inserted"])
        placement["correct_level"] = torch.where(trash, binned, placement["correct_level"])
        placement["wrong_level"] = torch.where(trash, level >= 0, placement["wrong_level"])
        placement["placed"] = torch.where(trash, binned & still & released, placement["placed"])
    else:
        binned = torch.zeros_like(present)
    facing = facing_flags(rot, FACING_DEGREES) | ~slots["is_frame"]
    if slots["is_crate"].any() and crate_interior is not None:
        crate_slot = int(slots["is_crate"].nonzero()[0])
        contents = in_crate(pos, rot, sizes, present, crate_slot, crate_interior, float(sizes[crate_slot, 2]))
    else:
        contents = torch.zeros_like(present)
    crate_empty = ~contents.any(-1)
    rule_ok = placement["placed"] & facing & (crate_empty[:, None] | ~slots["is_crate"])
    packed, gap, wall = packed_row(
        pos, rot, sizes, present & slots["is_book"] & (level == LEVEL_BOOKS), anchor=wall_anchor, layout=layout
    )
    spaced, separation = spaced_row(
        pos, rot, sizes, present & slots["is_display"] & (level == LEVEL_DISPLAY), layout=layout
    )
    valid = (rule_ok | ~present).all(-1) & packed & spaced & crate_empty
    return {
        **placement,
        "facing": facing,
        "in_bin": binned,
        "in_crate": contents,
        "crate_empty": crate_empty,
        "rule_ok": rule_ok,
        "packed": packed,
        "packed_gap": gap,
        "packed_wall": wall,
        "spaced": spaced,
        "separation": separation,
        "valid": valid,
    }


def goal_layout(
    table, wall=-1, device="cpu", book_gap=0.003, front_margin=0.02, display_gap=0.065, layout=DEFAULT_LAYOUT
):
    """An authored valid shelf-local layout for a slot table: books packed from ``wall``.

    Display objects stand near the front of the top layer, centred as a row with
    ``display_gap`` between their boxes, the frame facing outward; the large objects stand
    side by side at the front of the bottom layer; trash objects rest on the bin floor.
    Used by tests and by the simulator smoke script as a teleport-to-success target.
    """
    tensors = table.tensors(device)
    sizes = tensors["sizes"]
    pos = torch.zeros(len(table.classes), 3, device=device)
    rot = torch.eye(3, device=device).repeat(len(table.classes), 1, 1)
    cursor = layout.cavity_mins[LEVEL_BOOKS][1] if wall < 0 else layout.cavity_maxs[LEVEL_BOOKS][1]
    first_book = True
    display_slots = [
        slot for slot, cls in enumerate(table.classes) if cls is not None and cls.required_level == LEVEL_DISPLAY
    ]
    row_width = sum(float(sizes[slot, 1]) for slot in display_slots) + display_gap * max(len(display_slots) - 1, 0)
    station = -row_width / 2
    stations = {}
    for slot in display_slots:
        width = float(sizes[slot, 1])
        stations[slot] = station + width / 2
        station += width + display_gap
    large_slots = [
        slot for slot, cls in enumerate(table.classes) if cls is not None and cls.required_level == LEVEL_LARGE
    ]
    large_width = sum(float(sizes[slot, 1]) for slot in large_slots) + 0.06 * max(len(large_slots) - 1, 0)
    station = -large_width / 2
    for slot in large_slots:
        width = float(sizes[slot, 1])
        stations[slot] = station + width / 2
        station += width + 0.06
    bin_floor = pos.new_tensor(layout.bin_pos) - pos.new_tensor(layout.shelf_pos)
    trash_index = 0
    for slot, cls in enumerate(table.classes):
        if cls is None:
            continue
        depth, width, height = sizes[slot].tolist()
        level = cls.required_level
        floor = layout.cavity_mins[level][2] if level < len(layout.cavity_mins) else 0.0
        if level == LEVEL_BOOKS:
            cursor += -wall * (width / 2 + (0.0 if first_book else book_gap))
            first_book = False
            pos[slot] = torch.tensor((front_margin + depth / 2, cursor, floor + height / 2))
            cursor += -wall * (width / 2)
        elif level == LEVEL_DISPLAY:
            pos[slot] = torch.tensor((front_margin + depth / 2, stations[slot], floor + height / 2))
        elif level == LEVEL_LARGE:
            x = min(front_margin + depth / 2, layout.shelf_inner_depth / 2)
            pos[slot] = torch.tensor((x, stations[slot], floor + height / 2))
        elif level == LEVEL_BIN:
            corner = ((-1, -1), (1, -1), (-1, 1), (1, 1))[trash_index % 4]
            trash_index += 1
            pos[slot] = bin_floor + torch.tensor((0.065 * corner[0], 0.065 * corner[1], BIN_WALL + height / 2 + 0.002))
    return pos, rot
