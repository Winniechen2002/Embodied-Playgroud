# Copyright (c) 2025-2026, The DexVerse Project Developers.
# SPDX-License-Identifier: BSD-3-Clause
"""Reset samplers: table scatter, crate contents and misplaced objects (tensor-only).

``sample_layout`` is a rejection sampler over yawed footprints inside a rectangular region
with keep-out discs, a reach disc around the nearer robot base and a minimum separation.
It fails explicitly when a layout cannot be found, so an infeasible object set surfaces
as an error rather than as a silently overlapping scene.
"""

from __future__ import annotations

import math

import torch

from .catalog import BOOK, CRATE, CRATE_CLASS, CRATE_SLOT, FRAME, LARGE_SLOTS, SlotTable
from .geometry import BASE_KEEPOUT_RADIUS, DEFAULT_LAYOUT, RESET_REACH_RADIUS, ROBOT_BASES, TABLE_TOP, yawed_extents

SETTLE_LIFT = 0.0015
BOOK_START_MODES = ("mixed", "upright", "flat")
CRATE_BOOK_MODES = ("jumbled", "packed", "flat_stack")
JUMBLE_DROP_HEIGHT = 0.30  # above the crate floor; the simulator settles each object in turn
START_CONTAINERS = ("table", "crate", "shelf")
MISPLACED_WALL_GAP = 0.03  # a misplaced object keeps this clearance from walls and from objects on its layer
LARGE_YAW_HALF_RANGE = math.radians(15.0)  # long axis of crate and boxes stays across the desk
ROW_GAP = 0.003  # packed standing row of books on the desk
STACK_AFTER_ATTEMPTS = 24  # stacked desk starts: draws before an object is put down on top of others
CRATE_ITEM_YAW_HALF_RANGE = math.radians(5.0)  # contents are packed, so only a small jitter


def sample_modes(count, slots, mode, generator=None, device="cpu", exclude=()) -> torch.Tensor:
    """Per-slot flat flags; ``mixed`` keeps at least one flat and one upright book.

    ``exclude`` lists book slots that never lie flat (the packed standing row); the mixed
    rule then applies to the remaining books.
    """
    if mode not in BOOK_START_MODES:
        raise ValueError(f"book start mode must be one of {BOOK_START_MODES}, got {mode!r}")
    allowed = slots["flat_allowed"].to(device).clone()
    if len(exclude):
        allowed[list(exclude)] = False
    flat = torch.zeros((count, allowed.numel()), dtype=torch.bool, device=device)
    if mode == "flat":
        flat[:] = allowed
    elif mode == "mixed" and allowed.any():
        books = allowed.nonzero().flatten()
        draws = torch.rand((count, books.numel()), device=device, generator=generator) < 0.5
        if books.numel() >= 2:
            order = torch.rand((count, books.numel()), device=device, generator=generator).argsort(-1)
            draws[draws.all(-1), :] = False
            draws[(~draws).all(-1), :] = True
            draws = draws.gather(1, order)
            draws[draws.all(-1), 0] = False
            draws[(~draws).all(-1), 0] = True
        flat[:, books] = draws
    return flat


def footprint_half(sizes, flat) -> torch.Tensor:
    """Half extents of the resting footprint; flat books lie on a cover (depth x height)."""
    upright = sizes[..., :2] / 2
    flat_footprint = torch.stack((sizes[..., 0], sizes[..., 2]), -1) / 2
    return torch.where(flat[..., None], flat_footprint, upright)


def rest_height(sizes, flat) -> torch.Tensor:
    return torch.where(flat, sizes[..., 1], sizes[..., 2]) / 2


def quaternion_yaw_roll(yaw, flat) -> torch.Tensor:
    """wxyz quaternion for Rz(yaw) Rx(pi/2 if flat else 0)."""
    roll = torch.where(flat, torch.full_like(yaw, math.pi / 2), torch.zeros_like(yaw))
    cy, sy, cr, sr = (yaw / 2).cos(), (yaw / 2).sin(), (roll / 2).cos(), (roll / 2).sin()
    return torch.stack((cy * cr, cy * sr, sy * sr, sy * cr), -1)


def placement_order(sizes, active) -> list[int]:
    """Largest possible footprint first, so the crate or box is placed before the books."""
    area = sizes[:, 0] * torch.maximum(sizes[:, 1], sizes[:, 2])
    return [int(i) for i in area.argsort(descending=True) if bool(active[i])]


def sample_layout(
    count,
    sizes,
    flat,
    active,
    *,
    region,
    support_z,
    separation=0.020,
    margin=0.015,
    reach=None,
    keepouts=(),
    yaw_ranges=None,
    generator=None,
    device="cpu",
    max_rounds=32,
    max_attempts=256,
    stack_after=None,
    never_stack=(),
) -> torch.Tensor:
    """Sample resting poses ``(N, S, 7)`` for the ``active`` slots.

    ``sizes`` is ``(S, 3)``; ``flat`` and ``active`` are ``(N, S)`` or ``(S,)``. ``region`` is
    ``((x0, y0), (x1, y1))`` or a tuple of such boxes (chosen in proportion to their area);
    ``reach`` is ``(bases (B, 2), radius)``; ``keepouts`` are ``((x, y), radius)`` discs;
    ``yaw_ranges`` maps slot -> ``(centre, half_range)`` radians. Footprints keep
    ``separation`` apart unless ``stack_after`` is set: a slot (not in ``never_stack``) that
    finds no clear spot within that many draws is then put down on top of whatever already
    occupies its spot, raised above the highest overlapped object, for physics to settle.
    Poses of inactive slots are zero. Raises ``RuntimeError`` on exhaustion.
    """
    sizes = torch.as_tensor(sizes, dtype=torch.float32, device=device)
    slots = sizes.shape[0]
    flat = torch.as_tensor(flat, dtype=torch.bool, device=device).expand(count, slots)
    active = torch.as_tensor(active, dtype=torch.bool, device=device).expand(count, slots)
    regions = region if isinstance(region[0][0], (tuple, list)) else (region,)
    boxes = sizes.new_tensor(regions)  # (R, 2, 2)
    areas = (boxes[:, 1] - boxes[:, 0]).prod(-1).clamp_min(1e-9)
    bases = None if reach is None else sizes.new_tensor(reach[0])
    yaw_ranges = {} if yaw_ranges is None else yaw_ranges
    poses = torch.zeros((count, slots, 7), device=device)
    poses[..., 3] = 1.0
    order = placement_order(sizes, active.any(0))
    pending = torch.arange(count, device=device)
    for _ in range(max_rounds):
        if pending.numel() == 0:
            return poses
        n = pending.numel()
        centers = sizes.new_zeros(n, slots, 2)
        extents = sizes.new_zeros(n, slots, 2)
        tops = sizes.new_zeros(n, slots)
        failed = torch.zeros(n, dtype=torch.bool, device=device)
        placed_before: list[int] = []
        for slot in order:
            ids = torch.arange(n, device=device)[active[pending, slot]]
            stacking = stack_after is not None and slot not in never_stack
            for attempt in range(max_attempts):
                if ids.numel() == 0:
                    break
                if stacking and attempt >= stack_after:
                    break
                envs = pending[ids]
                if slot in yaw_ranges:
                    centre, half_range = yaw_ranges[slot]
                    yaw = centre + (torch.rand(len(ids), device=device, generator=generator) * 2 - 1) * half_range
                else:
                    yaw = (torch.rand(len(ids), device=device, generator=generator) * 2 - 1) * math.pi
                is_flat = flat[envs, slot]
                extent = yawed_extents(footprint_half(sizes[slot].expand(len(ids), -1), is_flat), yaw)
                choice = torch.multinomial(areas, len(ids), replacement=True, generator=generator)
                lo, hi = boxes[choice, 0], boxes[choice, 1]
                span = hi - lo - 2 * margin - 2 * extent
                fits = (span > 0).all(-1)
                xy = (
                    lo
                    + margin
                    + extent
                    + torch.rand((len(ids), 2), device=device, generator=generator) * span.clamp_min(0)
                )
                valid = fits
                if bases is not None:
                    distance = torch.linalg.vector_norm(xy[:, None, :] - bases[None], dim=-1).amin(-1)
                    valid &= distance <= reach[1]
                for centre_xy, radius in keepouts:
                    offset = torch.linalg.vector_norm(xy - sizes.new_tensor(centre_xy), dim=-1)
                    valid &= offset > radius + torch.linalg.vector_norm(extent, dim=-1)
                base = sizes.new_full((len(ids),), support_z)
                for prev in placed_before:
                    prev_active = active[envs, prev]
                    overlap = ((xy - centers[ids, prev]).abs() < extent + extents[ids, prev] + separation).all(-1)
                    overlap &= prev_active
                    if stacking and attempt >= stack_after - 1:
                        base = torch.where(overlap, torch.maximum(base, tops[ids, prev]), base)
                    else:
                        valid &= ~overlap
                accepted, env_ids = ids[valid], envs[valid]
                centers[accepted, slot], extents[accepted, slot] = xy[valid], extent[valid]
                height = rest_height(sizes[slot], is_flat[valid])
                poses[env_ids, slot, :2] = xy[valid]
                poses[env_ids, slot, 2] = base[valid] + height + SETTLE_LIFT
                poses[env_ids, slot, 3:] = quaternion_yaw_roll(yaw[valid], is_flat[valid])
                tops[accepted, slot] = base[valid] + 2 * height
                ids = ids[~valid]
            failed[ids] = True
            placed_before.append(slot)
        pending = pending[failed]
    if pending.numel() == 0:
        return poses
    raise RuntimeError(
        f"Could not place {pending.numel()} layouts without overlap; shrink the object set or widen the region."
    )


def compose(parent: torch.Tensor, local: torch.Tensor) -> torch.Tensor:
    """Compose ``(N, 7)`` parent poses with ``(N, S, 7)`` local poses (wxyz quaternions)."""
    pw, px, py, pz = parent[:, None, 3:].unbind(-1)
    lw, lx, ly, lz = local[..., 3:].unbind(-1)
    quat = torch.stack(
        (
            pw * lw - px * lx - py * ly - pz * lz,
            pw * lx + px * lw + py * lz - pz * ly,
            pw * ly - px * lz + py * lw + pz * lx,
            pw * lz + px * ly - py * lx + pz * lw,
        ),
        -1,
    )
    q = parent[:, None, 3:]
    v = local[..., :3]
    t = 2 * torch.cross(q[..., 1:], v, dim=-1)
    rotated = v + q[..., :1] * t + torch.cross(q[..., 1:], t, dim=-1)
    return torch.cat((parent[:, None, :3] + rotated, quat), -1)


def pack_row(
    count,
    sizes,
    members,
    yaw_ranges,
    *,
    y_start,
    y_end,
    x_half,
    support_z,
    margin,
    min_gap,
    generator=None,
    device="cpu",
) -> torch.Tensor:
    """Random-order row of upright boxes along Y between ``y_start`` and ``y_end``.

    Objects are laid out like a packed crate: the free slack is split randomly into the
    gaps, so every member always fits when the capacity budget holds. Returns local
    poses ``(N, S, 7)``; non-members are zero. Raises ``RuntimeError`` when the row does
    not fit.
    """
    slots = sizes.shape[0]
    poses = torch.zeros((count, slots, 7), device=device)
    poses[..., 3] = 1.0
    index = torch.as_tensor(members, dtype=torch.bool, device=device).nonzero().flatten()
    k = index.numel()
    if k == 0:
        return poses
    centres = sizes.new_tensor([yaw_ranges.get(int(i), (0.0, 0.0))[0] for i in index])
    half_ranges = sizes.new_tensor([yaw_ranges.get(int(i), (0.0, CRATE_ITEM_YAW_HALF_RANGE))[1] for i in index])
    yaw = centres + (torch.rand((count, k), device=device, generator=generator) * 2 - 1) * half_ranges
    extents = yawed_extents((sizes[index, :2] / 2).expand(count, -1, -1), yaw)
    order = torch.rand((count, k), device=device, generator=generator).argsort(-1)
    sorted_extents = extents.gather(1, order[..., None].expand(-1, -1, 2))
    widths = 2 * sorted_extents[..., 1]
    slack = (y_end - y_start) - 2 * margin - widths.sum(-1) - (k - 1) * min_gap
    x_span = x_half - margin - sorted_extents[..., 0]
    if (slack < 0).any() or (x_span < 0).any():
        raise RuntimeError("Crate contents do not fit the interior; shrink the object set.")
    weights = torch.rand((count, k + 1), device=device, generator=generator)
    gaps = (
        weights
        / weights.sum(-1, keepdim=True)
        * slack[:, None]
        * torch.rand((count, 1), device=device, generator=generator)
    )
    cursor = y_start + margin + gaps[:, 0]
    y = torch.zeros((count, k), device=device)
    for j in range(k):
        y[:, j] = cursor + sorted_extents[:, j, 1]
        cursor = cursor + widths[:, j] + min_gap + gaps[:, j + 1]
    x = (torch.rand((count, k), device=device, generator=generator) * 2 - 1) * x_span
    slot_ids = index[order]
    rows = torch.arange(count, device=device)[:, None].expand(-1, k)
    poses[rows, slot_ids, 0] = x
    poses[rows, slot_ids, 1] = y
    poses[rows, slot_ids, 2] = support_z + sizes[slot_ids, 2] / 2 + SETTLE_LIFT
    poses[rows, slot_ids, 3:] = quaternion_yaw_roll(yaw.gather(1, order), torch.zeros_like(x, dtype=torch.bool))
    return poses


def sample_crate_contents(
    count, sizes, slots, crate_pose, *, crate_books="packed", margin=0.004, min_gap=0.006, generator=None, device="cpu"
):
    """Poses of the non-crate present slots standing inside the crate (world frame).

    Contents form one packed row along the crate's long axis in random order. Books stand
    upright with their covers along that axis; a frame stands sideways (its width along
    the short axis); all objects carry a small yaw jitter. ``flat_stack`` lies the books
    flat in one stack at the -Y end and packs the other objects beside it.
    """
    if crate_books not in ("packed", "flat_stack"):
        raise ValueError(f"crate_books must be packed or flat_stack here, got {crate_books!r}")
    interior = CRATE_CLASS.part("interior")
    floor_z = -CRATE_CLASS.sizes[2] / 2 + CRATE_CLASS.part("floor")
    category = slots["category"].to(device)
    present = slots["present"].to(device).clone()
    present[CRATE_SLOT] = False
    is_book = (category == BOOK) & present
    yaw_ranges = {int(i): (math.pi / 2, CRATE_ITEM_YAW_HALF_RANGE) for i in (category == FRAME).nonzero().flatten()}
    flat = torch.zeros((count, sizes.shape[0]), dtype=torch.bool, device=device)
    y_start = -interior[1] / 2
    members = present.clone()
    if crate_books == "flat_stack" and is_book.any():
        books = is_book.nonzero().flatten()
        stack_length = float(sizes[books, 2].amax())
        members[books] = False
        y_start = -interior[1] / 2 + 2 * margin + stack_length + min_gap
    local = pack_row(
        count,
        sizes,
        members,
        yaw_ranges,
        y_start=y_start,
        y_end=interior[1] / 2,
        x_half=interior[0] / 2,
        support_z=floor_z,
        margin=margin,
        min_gap=min_gap,
        generator=generator,
        device=device,
    )
    if crate_books == "flat_stack" and is_book.any():
        height = floor_z
        for slot in books[sizes[books, 2].argsort(descending=True)]:
            thickness = float(sizes[slot, 1])
            local[:, slot, :3] = torch.tensor(
                (0.0, -interior[1] / 2 + margin + stack_length / 2, height + thickness / 2 + SETTLE_LIFT), device=device
            )
            local[:, slot, 3:] = quaternion_yaw_roll(
                torch.zeros(count, device=device), torch.ones(count, dtype=torch.bool, device=device)
            )
            height += thickness + SETTLE_LIFT
            flat[:, slot] = True
    return compose(crate_pose, local), flat


def random_quaternion(count, generator=None, device="cpu") -> torch.Tensor:
    """Uniformly random unit quaternions (wxyz)."""
    u = torch.rand((count, 3), device=device, generator=generator)
    a, b = torch.sqrt(1 - u[:, 0]), torch.sqrt(u[:, 0])
    theta, phi = 2 * math.pi * u[:, 1], 2 * math.pi * u[:, 2]
    return torch.stack((b * phi.cos(), a * theta.sin(), a * theta.cos(), b * phi.sin()), -1)


def sample_crate_jumble(count, sizes, slots, crate_pose, *, margin=0.05, generator=None, device="cpu"):
    """Pre-settle poses for a jumbled crate: every content object at a random orientation.

    Each object is placed above the crate floor inside the interior footprint; the
    environment drops them one by one in ``drop_order`` and lets physics settle, so the
    episode starts from a different fallen pile every time. Returns world poses
    ``(N, S, 7)`` (identity for non-contents) and ``drop_order`` ``(N, K)`` of content slots.
    """
    interior = CRATE_CLASS.part("interior")
    floor_z = -CRATE_CLASS.sizes[2] / 2 + CRATE_CLASS.part("floor")
    present = slots["present"].to(device).clone()
    present[CRATE_SLOT] = False
    contents = present.nonzero().flatten()
    k = contents.numel()
    local = torch.zeros((count, sizes.shape[0], 7), device=device)
    local[..., 3] = 1.0
    if k:
        span = sizes.new_tensor((interior[0] / 2 - margin, interior[1] / 2 - margin)).clamp_min(0.0)
        xy = (torch.rand((count, k, 2), device=device, generator=generator) * 2 - 1) * span
        local[:, contents, :2] = xy
        local[:, contents, 2] = floor_z + JUMBLE_DROP_HEIGHT
        local[:, contents, 3:] = random_quaternion(count * k, generator, device).reshape(count, k, 4)
    order = torch.rand((count, k), device=device, generator=generator).argsort(-1)
    drop_order = contents[order] if k else torch.zeros((count, 0), dtype=torch.long, device=device)
    return compose(crate_pose, local), drop_order


def misplaced_pose(
    count,
    slot,
    level,
    sizes,
    *,
    aligned=False,
    blocked=None,
    generator=None,
    device="cpu",
    layout=DEFAULT_LAYOUT,
    max_attempts=64,
) -> torch.Tensor:
    """Env-local pose ``(N, 7)`` of one object standing upright on a (wrong) shelf layer.

    ``aligned`` objects (books, the frame) face out of the hutch within 10 degrees; others
    get a random yaw and are kept clear of the walls by their footprint diagonal.
    ``blocked`` is ``(N, K, 2)`` shelf-local y intervals already occupied on that layer
    (pre-shelved or earlier misplaced objects); the object keeps ``MISPLACED_WALL_GAP``
    from them. Raises ``RuntimeError`` when no free spot is found.
    """
    depth, width, height = (float(v) for v in sizes[slot])
    lo, hi = layout.cavity_mins[level], layout.cavity_maxs[level]
    half_range = math.radians(10.0) if aligned else math.pi
    reach_y = (
        (math.cos(half_range) * width + math.sin(half_range) * depth) / 2 if aligned else math.hypot(depth, width) / 2
    )
    reach_x = (
        (math.cos(half_range) * depth + math.sin(half_range) * width) / 2 if aligned else math.hypot(depth, width) / 2
    )
    y_half = (hi[1] - lo[1]) / 2 - reach_y - MISPLACED_WALL_GAP
    if y_half <= 0:
        raise RuntimeError(f"slot {slot} does not fit on level {level}")
    x = (
        lo[0]
        + 0.02
        + reach_x
        + torch.rand(count, device=device, generator=generator) * max(hi[0] - lo[0] - 0.04 - 2 * reach_x, 0.0) * 0.5
    )
    y = torch.zeros(count, device=device)
    pending = torch.arange(count, device=device)
    for _ in range(max_attempts):
        if pending.numel() == 0:
            break
        candidate = (torch.rand(pending.numel(), device=device, generator=generator) * 2 - 1) * y_half
        ok = torch.ones_like(candidate, dtype=torch.bool)
        if blocked is not None and blocked.shape[1]:
            spans = blocked[pending]
            clear = (candidate[:, None] + reach_y + MISPLACED_WALL_GAP <= spans[..., 0]) | (
                candidate[:, None] - reach_y - MISPLACED_WALL_GAP >= spans[..., 1]
            )
            ok = clear.all(-1)
        y[pending[ok]] = candidate[ok]
        pending = pending[~ok]
    if pending.numel():
        raise RuntimeError(f"no free spot for slot {slot} on level {level} in {pending.numel()} layouts")
    z = torch.full((count,), lo[2] + height / 2 + SETTLE_LIFT, device=device)
    yaw = (torch.rand(count, device=device, generator=generator) * 2 - 1) * half_range
    pose = torch.cat(
        (torch.stack((x, y, z), -1), quaternion_yaw_roll(yaw, torch.zeros(count, dtype=torch.bool, device=device))), -1
    )
    pose[:, :3] += pose.new_tensor(layout.shelf_pos)
    return pose


def shelf_start_poses(count, table: SlotTable, misplaced_slots, *, generator=None, device="cpu", layout=DEFAULT_LAYOUT):
    """Env-local poses ``(N, S, 7)`` of every non-misplaced object already in its place.

    The pre-shelved objects stand in the authored goal layout of the remaining set (books
    packed against a wall chosen at random per environment, display objects centred).
    """
    from .rules import goal_layout

    remaining = SlotTable(tuple(None if slot in misplaced_slots else cls for slot, cls in enumerate(table.classes)))
    shelf = torch.tensor(layout.shelf_pos, device=device)
    walls = []
    for wall in (-1, 1):
        pos, _ = goal_layout(remaining, wall, device=device, layout=layout)
        walls.append(pos + shelf)
    pick = torch.rand(count, device=device, generator=generator) < 0.5
    pos = torch.where(pick[:, None, None], walls[0][None], walls[1][None])
    poses = torch.zeros((count, len(table.classes), 7), device=device)
    poses[..., 3] = 1.0
    poses[..., :3] = pos
    poses[..., 2] += SETTLE_LIFT
    return poses


def _occupied(poses, sizes, slots, shelf_y):
    """Shelf-local y intervals ``(N, K, 2)`` covered by the given objects at any yaw."""
    if not slots:
        return torch.zeros((poses.shape[0], 0, 2), device=poses.device)
    centres = poses[:, list(slots), 1] - shelf_y
    footprint = sizes[list(slots), :2].to(poses.device)
    half = torch.linalg.vector_norm(footprint, dim=-1) / 2  # any yaw
    return torch.stack((centres - half, centres + half), -1)


def sample_start(
    count,
    slots,
    *,
    start_container="table",
    book_start_mode="mixed",
    crate_books="jumbled",
    misplaced=(),
    row=(),
    stacking=False,
    table=None,
    generator=None,
    device="cpu",
    layout=DEFAULT_LAYOUT,
):
    """Env-local start poses ``(N, S, 7)``, flat flags ``(N, S)`` and a drop order.

    ``misplaced`` lists ``(slot, level)`` pairs (or one pair) for objects pre-placed on a
    wrong shelf layer; they are excluded from the table or crate sampling. A ``shelf``
    start (which needs the ``table``) stands every other object in its place. ``row`` lists book slots of one size that
    start standing packed together in a row on the desk (table starts only). With
    ``stacking`` a desk object that finds no clear spot is put down on top of others (the
    environment then settles the desk with physics); the row and the large objects always
    stand on the desk itself. The drop order is ``None`` unless the crate contents are
    jumbled, in which case the content poses are pre-settle poses that the environment
    must drop in that order and settle with physics.
    """
    if crate_books not in CRATE_BOOK_MODES:
        raise ValueError(f"crate_books must be one of {CRATE_BOOK_MODES}, got {crate_books!r}")
    if start_container not in START_CONTAINERS:
        raise ValueError(f"start_container must be one of {START_CONTAINERS}, got {start_container!r}")
    sizes = slots["sizes"].to(device)
    present = slots["present"].to(device).clone()
    category = slots["category"].to(device)
    if misplaced and isinstance(misplaced[0], int):
        misplaced = (tuple(misplaced),)
    misplaced = tuple(tuple(pair) for pair in (misplaced or ()))
    for slot, _ in misplaced:
        present[slot] = False
    keepouts = tuple((base, BASE_KEEPOUT_RADIUS) for base in ROBOT_BASES)
    reach = (ROBOT_BASES, RESET_REACH_RADIUS)
    large_yaw = {slot: (0.0, LARGE_YAW_HALF_RANGE) for slot in LARGE_SLOTS}
    drop_order = None
    if start_container == "shelf":
        if table is None:
            raise ValueError("a shelf start needs the slot table")
        poses = shelf_start_poses(
            count, table, {slot for slot, _ in misplaced}, generator=generator, device=device, layout=layout
        )
        flat = torch.zeros((count, sizes.shape[0]), dtype=torch.bool, device=device)
    elif start_container == "table":
        row = tuple(int(s) for s in row if present[int(s)])
        flat = sample_modes(count, slots, book_start_mode, generator, device, exclude=row)
        flat &= present
        active = present.clone()
        row_sizes = sizes.clone()
        if row:
            flat[:, list(row)] = False
            thickness = float(sizes[row[0], 1])
            row_sizes[row[0], 1] = len(row) * thickness + (len(row) - 1) * ROW_GAP
            active[list(row[1:])] = False
        poses = sample_layout(
            count,
            row_sizes,
            flat,
            active,
            region=layout.table_regions,
            support_z=TABLE_TOP,
            reach=reach,
            keepouts=keepouts,
            yaw_ranges=large_yaw,
            generator=generator,
            device=device,
            stack_after=STACK_AFTER_ATTEMPTS if stacking else None,
            never_stack=set(row[:1]) | set(LARGE_SLOTS),
        )
        if row:
            lead = poses[:, row[0]].clone()
            yaw = 2 * torch.atan2(lead[:, 6], lead[:, 3])
            length = float(row_sizes[row[0], 1])
            for k, slot in enumerate(row):
                offset = -length / 2 + thickness / 2 + k * (thickness + ROW_GAP)
                poses[:, slot, 0] = lead[:, 0] - yaw.sin() * offset
                poses[:, slot, 1] = lead[:, 1] + yaw.cos() * offset
                poses[:, slot, 2] = lead[:, 2]
                poses[:, slot, 3:] = lead[:, 3:]
    else:
        if int(category[CRATE_SLOT]) != CRATE:
            raise ValueError("crate start requires the open crate in the first large slot")
        crate_only = torch.zeros_like(present)
        crate_only[CRATE_SLOT] = True
        flat = torch.zeros((count, sizes.shape[0]), dtype=torch.bool, device=device)
        poses = sample_layout(
            count,
            sizes,
            flat,
            crate_only,
            region=layout.crate_region,
            support_z=TABLE_TOP,
            reach=reach,
            keepouts=keepouts,
            yaw_ranges=large_yaw,
            generator=generator,
            device=device,
        )
        contents = {**slots, "present": present}
        if crate_books == "jumbled":
            inside, drop_order = sample_crate_jumble(
                count, sizes, contents, poses[:, CRATE_SLOT], generator=generator, device=device
            )
        else:
            inside, flat = sample_crate_contents(
                count,
                sizes,
                contents,
                poses[:, CRATE_SLOT],
                crate_books=crate_books,
                generator=generator,
                device=device,
            )
        mask = present.clone()
        mask[CRATE_SLOT] = False
        poses[:, mask] = inside[:, mask]
    shelf_y = layout.shelf_pos[1]
    taken = {}  # level -> slots standing on it
    if start_container == "shelf":
        for level in range(len(layout.floors)):
            taken[level] = [
                slot
                for slot in range(sizes.shape[0])
                if bool(present[slot]) and int(slots["required_level"][slot]) == level
            ]
    for slot, level in misplaced:
        others = taken.setdefault(level, [])
        poses[:, slot] = misplaced_pose(
            count,
            slot,
            level,
            sizes,
            aligned=int(category[slot]) in (BOOK, FRAME),
            blocked=_occupied(poses, sizes, others, shelf_y),
            generator=generator,
            device=device,
            layout=layout,
        )
        others.append(slot)
    return poses, flat, drop_order
