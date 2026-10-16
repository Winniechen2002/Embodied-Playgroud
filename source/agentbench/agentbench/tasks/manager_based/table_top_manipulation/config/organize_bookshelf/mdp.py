# Copyright (c) 2025-2026, The DexVerse Project Developers.
# SPDX-License-Identifier: BSD-3-Clause
"""Isaac Lab glue for the bookshelf task: resets, state gathering, MDP terms.

All evaluation logic lives in the tensor-only modules (``rules``, ``geometry``); this
module only gathers simulator tensors into the slot layout and caches the per-step
verdict on the environment.
"""

from __future__ import annotations

import torch
from isaaclab.managers import ManagerTermBase
from isaaclab.sensors.camera.utils import create_pointcloud_from_depth
from isaaclab.utils.math import quat_apply, quat_conjugate, quat_mul

from . import geometry as g
from .catalog import BOOK, BOX, CRATE, CRATE_CLASS, CRATE_SLOT, NUM_SLOTS, SLOT_NAMES
from .rules import WALL_ANCHORS, in_crate, slot_rules
from .sampling import random_quaternion, sample_start
from .variants import BY_ID

HAND_BODIES = ("panda_hand", "panda_leftfinger", "panda_rightfinger")
ROBOTS = ("left_robot", "right_robot")
RELEASE_DISTANCE = 0.05
RELEASE_FORCE = 0.1
LIFT_HEIGHT = 0.025
# Physical validity (sticky per episode; any violation ends the episode and denies success).
ARM_SPEED_LIMITS = (2.175,) * 4 + (2.61,) * 3  # Franka Panda nominal joint speed limits, rad/s
SPEED_TOLERANCE = 1.10  # a violation is an arm joint faster than 110 % of its limit
PENETRATION_LIMIT = 0.005  # deeper object-to-hand or object-to-furniture contact penetration, m
VIOLATIONS = ("non_finite_state", "joint_speed", "penetration")


def _runtime(env):
    if not hasattr(env, "_bookshelf_state"):
        variant = BY_ID[env.cfg.variant_id]
        table = variant.slot_table()
        hand_ids = {}
        tcp_ids = {}
        for robot in ROBOTS:
            articulation = env.scene[robot]
            hand_ids[robot] = articulation.find_bodies(list(HAND_BODIES), preserve_order=True)[0]
            tcp_ids[robot] = articulation.find_bodies("panda_hand")[0][0]
        env._bookshelf_state = {
            "variant": variant,
            "layout": g.LAYOUTS[variant.layout],
            "table": table,
            "slots": table.tensors(env.device),
            "present_indices": table.present_indices(),
            "step": torch.full((env.num_envs,), -1, device=env.device, dtype=torch.long),
            "milestones": torch.zeros((env.num_envs, NUM_SLOTS, 3), device=env.device, dtype=torch.bool),
            "violations": torch.zeros((env.num_envs, len(VIOLATIONS)), device=env.device, dtype=torch.bool),
            "worst": torch.zeros((env.num_envs, 2), device=env.device),  # peak speed ratio, deepest penetration
            "hold": g.HoldCounter(env.num_envs, env.device),
            "start_bottom": torch.zeros((env.num_envs, NUM_SLOTS), device=env.device),
            "hand_ids": hand_ids,
            "tcp_ids": tcp_ids,
            "crate_interior": CRATE_CLASS.part("interior") if table.crate is not None else None,
            # Objects whose colliders fill their box exactly: their depth into the furniture is computed
            # geometrically too, since PhysX contact reports can omit a pair while the object touches another.
            "box_slots": [s for s in table.present_indices() if table.category[s] in BOX_EXACT_CATEGORIES],
            "furniture": tuple(
                torch.tensor(corner, dtype=torch.float32, device=env.device)
                for corner in zip(*g.furniture_boxes(g.LAYOUTS[variant.layout], with_bin=bool(table.trash)))
            ),
        }
    return env._bookshelf_state


BOX_EXACT_CATEGORIES = (BOOK, BOX, CRATE)
SETTLE_SUBSTEPS_PER_DROP = 30
SETTLE_SUBSTEPS_FINAL = 60
SETTLE_SUBSTEPS_MAX = 480
SETTLE_STILL_SPEED = 0.004  # m/s; slower piles can still creep a few centimetres over an episode
SETTLE_STILL_ANGULAR = 0.05  # rad/s
SETTLE_STILL_SUBSTEPS = 12  # 0.1 s of stillness: a pile that pauses before toppling is not done
SETTLE_FINAL_STILL = 60  # the last settle of a pile waits for 0.5 s of stillness: a balanced object may still tip
SETTLE_FINAL_CAP = 960
PARK_HEIGHT = 0.70  # objects waiting for their drop are held this far above the crate floor
SETTLE_SUBSTEPS_PER_DROP_MAX = 120
MAX_JUMBLE_RETRIES = 3  # whole-layout retries when the settled pile still spills out
MAX_DESK_RETRIES = 8  # resamples of a stacked desk start whose settled pile dropped an object
MAX_REDROPS = 3  # per-drop rounds that re-drop every content object knocked out of the crate


def _hold_robots(env, ids):
    """Target the home pose for the environments being reset; other environments keep their targets."""
    for robot in ROBOTS:
        articulation = env.scene[robot]
        default = articulation.data.default_joint_pos[ids]
        articulation.set_joint_position_target(default, env_ids=ids)
        articulation.set_joint_velocity_target(torch.zeros_like(default), env_ids=ids)


def _settle(
    env, ids, substeps, held=(), until_still=None, cap=SETTLE_SUBSTEPS_MAX, still_substeps=SETTLE_STILL_SUBSTEPS
):
    """Advance physics without actions; ``held`` re-pins (slot, env_ids, poses) every substep.

    With ``until_still`` (a list of slots) the loop runs at least ``substeps`` and stops once
    every listed object in ``ids`` has moved slower than ``SETTLE_STILL_SPEED`` for
    ``still_substeps`` consecutive substeps (and turned slower than
    ``SETTLE_STILL_ANGULAR``), or at ``cap``.
    """
    zeros = {}
    still_for = 0
    for step in range(cap if until_still else substeps):
        _hold_robots(env, ids)
        for slot, held_ids, poses in held:
            if slot not in zeros:
                zeros[slot] = torch.zeros((len(held_ids), 6), device=env.device)
            env.scene[SLOT_NAMES[slot]].write_root_pose_to_sim(poses, env_ids=held_ids)
            env.scene[SLOT_NAMES[slot]].write_root_velocity_to_sim(zeros[slot], env_ids=held_ids)
        env.scene.write_data_to_sim()
        env.sim.step(render=False)
        env.scene.update(dt=env.physics_dt)
        if until_still:
            data = [env.scene[SLOT_NAMES[s]].data for s in until_still]
            linear = torch.stack([torch.linalg.vector_norm(d.root_lin_vel_w[ids], dim=-1) for d in data], -1)
            angular = torch.stack([torch.linalg.vector_norm(d.root_ang_vel_w[ids], dim=-1) for d in data], -1)
            still = (linear < SETTLE_STILL_SPEED).all() and (angular < SETTLE_STILL_ANGULAR).all()
            still_for = still_for + 1 if still else 0
            if step + 1 >= substeps and still_for >= still_substeps:
                break


def _settle_final(env, ids, slots):
    """Settle a fallen pile until it has been still for a long window, so a slowly tipping object finishes."""
    _settle(env, ids, SETTLE_SUBSTEPS_FINAL, until_still=slots, cap=SETTLE_FINAL_CAP, still_substeps=SETTLE_FINAL_STILL)


def _write_poses(env, ids, poses, slots):
    zeros = torch.zeros((len(ids), 6), device=env.device)
    for slot in slots:
        pose = poses[:, slot].clone()
        pose[:, :3] += env.scene.env_origins[ids]
        env.scene[SLOT_NAMES[slot]].write_root_pose_to_sim(pose, env_ids=ids)
        env.scene[SLOT_NAMES[slot]].write_root_velocity_to_sim(zeros, env_ids=ids)


def _crate_contents(env, ids, contents):
    """Content slots that currently sit inside the crate footprint (pile allowance included)."""
    slots = _runtime(env)["slots"]
    pos, quat, _, _ = object_data(env)
    local = pos[ids] - env.scene.env_origins[ids, None, :]
    return in_crate(
        local,
        g.rotation_matrix(quat[ids]),
        slots["sizes"],
        slots["present"].expand(len(ids), -1),
        CRATE_SLOT,
        CRATE_CLASS.part("interior"),
        float(slots["sizes"][CRATE_SLOT, 2]),
    )


def _drop_jumble(env, ids, poses, drop_order, contents):
    """Drop the crate contents one at a time into the crate and let them settle.

    Objects waiting for their turn are pinned above the crate every substep; each object
    is released just above the current pile so it never spawns inside another object.
    After every drop, any content object that has left the crate footprint (the new one
    bouncing out, or an earlier one knocked out) is dropped again at a fresh random
    orientation, for up to ``MAX_REDROPS`` rounds.
    """
    origins = env.scene.env_origins[ids]
    sizes = _runtime(env)["slots"]["sizes"]
    half_diagonal = 0.5 * torch.linalg.vector_norm(sizes, dim=-1)
    park = poses.clone()
    park[:, :, 2] += PARK_HEIGHT
    contents_tensor = torch.as_tensor(contents, device=env.device)

    def pile_top(resting):
        """Highest collider point of the objects flagged in ``resting`` (N, C); -inf when none."""
        if not resting.any():
            return torch.full((len(ids),), -float("inf"), device=env.device)
        pos, quat, _, _ = object_data(env)
        upper = g.aabb(pos[ids], g.rotation_matrix(quat[ids]), sizes)[1][..., 2]
        return upper[:, contents].masked_fill(~resting, -float("inf")).amax(-1)

    def release(to_drop, top):
        for index, slot in enumerate(contents):
            chosen = to_drop[:, index]
            if chosen.any():
                pose = poses[chosen, slot].clone()
                pose[:, :3] += origins[chosen]
                pose[:, 2] = torch.maximum(pose[:, 2], top[chosen] + half_diagonal[slot] + 0.02)
                env.scene[SLOT_NAMES[slot]].write_root_pose_to_sim(pose, env_ids=ids[chosen])
                env.scene[SLOT_NAMES[slot]].write_root_velocity_to_sim(
                    torch.zeros((int(chosen.sum()), 6), device=env.device), env_ids=ids[chosen]
                )

    dropped = torch.zeros((len(ids), len(contents)), dtype=torch.bool, device=env.device)
    for rank in range(drop_order.shape[1]):
        held = []
        for slot in contents:
            waiting = (drop_order[:, rank + 1 :] == slot).any(-1)
            if waiting.any():
                pose = park[waiting, slot].clone()
                pose[:, :3] += origins[waiting]
                held.append((slot, ids[waiting], pose))
        to_drop = drop_order[:, rank, None] == contents_tensor
        for attempt in range(MAX_REDROPS + 1):
            release(to_drop, pile_top(dropped & ~to_drop))
            dropped |= to_drop
            _settle(
                env,
                ids,
                SETTLE_SUBSTEPS_PER_DROP,
                held=held,
                until_still=list(contents),
                cap=SETTLE_SUBSTEPS_PER_DROP_MAX,
            )
            to_drop = dropped & ~_crate_contents(env, ids, contents)[:, contents]
            if not to_drop.any() or attempt == MAX_REDROPS:
                break
            rows, columns = to_drop.nonzero(as_tuple=True)
            poses[rows, contents_tensor[columns], 3:] = random_quaternion(len(rows), device=env.device)
    _settle_final(env, ids, list(contents))
    zeros = torch.zeros((len(ids), 6), device=env.device)
    for slot in contents:
        env.scene[SLOT_NAMES[slot]].write_root_velocity_to_sim(zeros, env_ids=ids)


def reset_objects(env, env_ids):
    """Sample a fresh start layout for ``env_ids`` and clear their task bookkeeping.

    Jumbled crate starts drop the contents into the crate and settle them with physics,
    which advances the simulation for every environment by a fraction of a second.
    """
    state = _runtime(env)
    ids = (
        torch.arange(env.num_envs, device=env.device)
        if env_ids is None
        else torch.as_tensor(env_ids, device=env.device)
    )
    variant = state["variant"]
    slots = state["slots"]
    misplaced = variant.misplaced_slots()
    misplaced_set = {slot for slot, _ in misplaced}
    retries = MAX_JUMBLE_RETRIES if variant.start_container == "crate" else MAX_DESK_RETRIES
    for attempt in range(retries + 1):
        poses, _, drop_order = sample_start(
            len(ids),
            slots,
            start_container=variant.start_container,
            book_start_mode=variant.book_start_mode,
            crate_books=variant.crate_books,
            misplaced=misplaced,
            row=variant.row_slots(),
            table=state["table"],
            stacking=variant.stacked_start,
            device=env.device,
            layout=state["layout"],
        )
        if drop_order is None:
            _write_poses(env, ids, poses, state["present_indices"])
            if variant.stacked_start:
                # Objects put down on top of others fall into a pile; settle before the episode starts.
                _settle_final(env, ids, list(state["present_indices"]))
                zeros = torch.zeros((len(ids), 6), device=env.device)
                for slot in state["present_indices"]:
                    env.scene[SLOT_NAMES[slot]].write_root_velocity_to_sim(zeros, env_ids=ids)
                # A pile can topple over the open near edge; such a start is lost before the episode begins.
                fallen = objects_lost(env)[ids]
                if fallen.any():
                    if attempt == retries:
                        raise RuntimeError(f"stacked desk start lost an object in {retries + 1} attempts")
                    ids = ids[fallen]
                    continue
            break
        contents = [s for s in state["present_indices"] if s != CRATE_SLOT and s not in misplaced_set]
        static = [s for s in state["present_indices"] if s not in contents]
        _write_poses(env, ids, poses, static)
        _drop_jumble(env, ids, poses, drop_order, contents)
        escaped = ~_crate_contents(env, ids, contents)[:, contents].all(-1)
        if not escaped.any() or attempt == MAX_JUMBLE_RETRIES:
            break
        ids = ids[escaped]
    pos, quat, _, _ = object_data(env)
    ids = (
        torch.arange(env.num_envs, device=env.device)
        if env_ids is None
        else torch.as_tensor(env_ids, device=env.device)
    )
    local = pos[ids] - env.scene.env_origins[ids, None, :]
    lower, _ = g.aabb(local, g.rotation_matrix(quat[ids]), slots["sizes"])
    state["start_bottom"][ids] = lower[..., 2]
    state["step"][ids] = -1
    state["milestones"][ids] = False
    for slot, _ in misplaced:
        # Already on a shelf layer: do not pay an "inserted" milestone for the wrong layer.
        state["milestones"][ids, slot, 1] = True
    for slot in variant.preshelved_slots():
        # Starts in its place: no milestone reward for what was never done.
        state["milestones"][ids, slot] = True
    state["hold"].reset(ids)
    state["violations"][ids] = False
    state["worst"][ids] = 0.0


def object_data(env):
    """World poses and velocities per slot ``(N, S, ...)``; absent slots are zero/identity."""
    state = _runtime(env)
    count = env.num_envs
    pos = torch.zeros((count, NUM_SLOTS, 3), device=env.device)
    quat = torch.zeros((count, NUM_SLOTS, 4), device=env.device)
    quat[..., 0] = 1.0
    lin = torch.zeros_like(pos)
    ang = torch.zeros_like(pos)
    for slot in state["present_indices"]:
        data = env.scene[SLOT_NAMES[slot]].data
        pos[:, slot] = data.root_pos_w
        quat[:, slot] = data.root_quat_w
        lin[:, slot] = data.root_lin_vel_w
        ang[:, slot] = data.root_ang_vel_w
    return pos, quat, lin, ang


def hand_filter_columns(env, slot):
    """Indices of the hand and finger bodies among the filters of a slot's contact sensor.

    The sensors also filter the furniture (for the penetration audit), and PhysX does not
    keep the configured filter order, so the hand columns are found by their prim paths.
    """
    cache = _runtime(env).setdefault("hand_columns", {})
    if slot not in cache:
        paths = env.scene[f"slot_contact_{slot}"].contact_physx_view.filter_paths
        if paths and isinstance(paths[0], (list, tuple)):
            paths = paths[0]
        columns = [i for i, path in enumerate(paths) if any(f"Panda/{body}" in path for body in HAND_BODIES)]
        if len(columns) != len(ROBOTS) * len(HAND_BODIES):
            raise RuntimeError(f"expected {len(ROBOTS) * len(HAND_BODIES)} hand filters, found {list(paths)}")
        cache[slot] = torch.tensor(columns, device=env.device)
    return cache[slot]


def contact_forces(env):
    """Filtered object-to-hand contact force magnitude per slot ``(N, S)``."""
    state = _runtime(env)
    forces = torch.zeros((env.num_envs, NUM_SLOTS), device=env.device)
    for slot in state["present_indices"]:
        matrix = env.scene[f"slot_contact_{slot}"].data.force_matrix_w
        if matrix is None:
            raise RuntimeError("Object-to-hand filtered contact reporting is unavailable.")
        hands = matrix.index_select(2, hand_filter_columns(env, slot))
        forces[:, slot] = torch.linalg.vector_norm(hands, dim=-1).flatten(1).sum(-1)
    return forces


def furniture_penetration(env):
    """Deepest geometric penetration ``(N,)`` of the box-shaped objects into the furniture colliders.

    Books, the closed boxes and the crate fill their collider box exactly, so their depth into
    the desk, its legs and blockers, the hutch boards and the bin follows from the poses alone.
    """
    state = _runtime(env)
    slots = state["box_slots"]
    if not slots:
        return torch.zeros(env.num_envs, device=env.device)
    pos, quat, _, _ = object_data(env)
    local = pos[:, slots] - env.scene.env_origins[:, None, :]
    lower, upper = state["furniture"]
    depth = g.box_penetration(local, g.rotation_matrix(quat[:, slots]), state["slots"]["sizes"][slots], lower, upper)
    return depth.flatten(1).amax(-1)


def contact_penetration(env):
    """Deepest penetration ``(N,)`` between any object and the hands or the furniture (0 when none).

    Reads the separation of every contact point PhysX reports between each object and its
    sensor's filter bodies (both arms' hands and fingers, the desk, the hutch and the bin)
    at the last physics substep, and takes the larger of that and ``furniture_penetration``.
    Contacts between two objects are not measured.
    """
    state = _runtime(env)
    deepest = furniture_penetration(env)
    for slot in state["present_indices"]:
        view = env.scene[f"slot_contact_{slot}"].contact_physx_view
        _, _, _, separation, counts, starts = view.get_contact_data(dt=env.physics_dt)
        counts, starts = counts.reshape(env.num_envs, -1), starts.reshape(env.num_envs, -1)
        flat_counts = counts.reshape(-1).long()
        total = int(flat_counts.sum())
        if total == 0:
            continue
        pairs = torch.repeat_interleave(torch.arange(flat_counts.numel(), device=env.device), flat_counts)
        offsets = torch.arange(total, device=env.device) - (flat_counts.cumsum(0) - flat_counts)[pairs]
        values = separation.reshape(-1)[starts.reshape(-1).long()[pairs] + offsets].to(deepest.device)
        rows = pairs // counts.shape[1]
        depth = torch.zeros(env.num_envs, device=env.device).scatter_reduce(
            0, rows, (-values).clamp_min(0), reduce="amax"
        )
        deepest = torch.maximum(deepest, depth)
    return deepest


def joint_speed_ratio(env):
    """Largest arm joint speed relative to its nominal limit ``(N,)`` over both arms."""
    limits = torch.tensor(ARM_SPEED_LIMITS, device=env.device)
    ratios = [env.scene[robot].data.joint_vel[:, :7].abs() / limits for robot in ROBOTS]
    return torch.cat(ratios, -1).amax(-1)


def _update_violations(env, fresh):
    """Accumulate sticky physical-validity violations for the environments that stepped."""
    state = _runtime(env)
    pos, quat, lin, ang = object_data(env)
    robot_state = torch.cat([env.scene[robot].data.joint_pos for robot in ROBOTS], -1)
    finite = torch.isfinite(torch.cat((pos, quat, lin, ang), -1)).flatten(1).all(-1)
    finite &= torch.isfinite(robot_state).all(-1)
    speed = joint_speed_ratio(env)
    depth = contact_penetration(env)
    now = torch.stack((~finite, speed > SPEED_TOLERANCE, depth > PENETRATION_LIMIT), -1) & fresh[:, None]
    state["violations"] |= now
    worst = torch.stack((speed, depth), -1)
    state["worst"] = torch.where(fresh[:, None], torch.maximum(state["worst"], worst), state["worst"])


def hand_points(env):
    """Hand, finger and tool-centre-point positions of both arms ``(N, 8, 3)`` in world frame."""
    state = _runtime(env)
    points = []
    offset = torch.tensor(g.TCP_OFFSET, device=env.device)
    for robot in ROBOTS:
        data = env.scene[robot].data
        points.append(data.body_pos_w[:, state["hand_ids"][robot]])
        hand = state["tcp_ids"][robot]
        tcp = data.body_pos_w[:, hand] + quat_apply(data.body_quat_w[:, hand], offset.expand(env.num_envs, -1))
        points.append(tcp[:, None, :])
    return torch.cat(points, 1)


def released_flags(env, pos, rot, sizes):
    """No filtered hand contact and every hand point clear of the object's box."""
    points = hand_points(env)
    local = torch.einsum("nsji,nspj->nspi", rot, points[:, None, :, :] - pos[:, :, None, :])
    distance = torch.linalg.vector_norm((local.abs() - sizes[None, :, None, :] / 2).clamp_min(0), dim=-1)
    return (distance.amin(-1) > RELEASE_DISTANCE) & (contact_forces(env) < RELEASE_FORCE)


def current_state(env):
    """Evaluate every slot once per step and cache the verdict on the environment."""
    state = _runtime(env)
    step = env.episode_length_buf
    fresh = state["step"] != step
    if not fresh.any() and "metrics" in state:
        return state["metrics"]
    slots = state["slots"]
    sizes = slots["sizes"]
    pos, quat, lin, ang = object_data(env)
    shelf = env.scene["shelf"].data
    frame = g.rotation_matrix(shelf.root_quat_w)
    local = torch.einsum("nji,nsj->nsi", frame, pos - shelf.root_pos_w[:, None, :])
    rot = g.rotation_matrix(quat)
    local_rot = torch.einsum("nji,nsjk->nsik", frame, rot)
    released = released_flags(env, pos, rot, sizes)
    metrics = slot_rules(
        local,
        local_rot,
        lin,
        ang,
        released,
        slots,
        wall_anchor=state["variant"].wall_anchor,
        crate_interior=state["crate_interior"],
        layout=state["layout"],
    )
    _update_violations(env, fresh)
    violated = state["violations"].any(-1)
    success = state["hold"].update(metrics["valid"] & ~violated, step, env.step_dt)
    lower, _ = g.aabb(pos - env.scene.env_origins[:, None, :], rot, sizes)
    lifted = (lower[..., 2] > state["start_bottom"] + LIFT_HEIGHT) & slots["present"]
    milestones = state["milestones"]
    old = milestones.clone()
    milestones[:, :, 0] |= lifted & fresh[:, None]
    milestones[:, :, 1] |= metrics["inserted"] & fresh[:, None]
    milestones[:, :, 2] |= metrics["placed"] & fresh[:, None]
    metrics.update(
        {
            "success": success,
            "violations": state["violations"].clone(),
            "physics_violation": violated,
            "delta": (milestones.float() - old.float()).sum(dim=(1, 2)),
            "released": released,
            "local_pos": local,
            "local_rot": local_rot,
            "lifted": lifted,
        }
    )
    state["metrics"] = metrics
    state["step"] = step.clone()
    return metrics


def task_success(env):
    return current_state(env)["success"]


def physics_violation(env):
    """Termination: the episode broke a physical-validity rule (see ``VIOLATIONS``)."""
    return current_state(env)["physics_violation"]


def episode_report(env, env_id: int = 0) -> dict:
    """JSON-serializable evaluation record of one environment's current episode state."""
    state = _runtime(env)
    metrics = current_state(env)
    table = state["table"]
    names = table.names()
    objects = []
    for slot in state["present_indices"]:
        cls = table.classes[slot]
        required = g.PLACE_NAMES[cls.required_level]
        level = int(metrics["level"][env_id, slot])
        objects.append(
            {
                "slot": slot,
                "name": names[slot],
                "category": cls.category_name,
                "required": required,
                "current": (
                    "bin" if bool(metrics["in_bin"][env_id, slot]) else g.PLACE_NAMES[level] if level >= 0 else None
                ),
                "placed": bool(metrics["placed"][env_id, slot]),
                "wrong_level": bool(metrics["wrong_level"][env_id, slot]),
                "in_crate": bool(metrics["in_crate"][env_id, slot]),
                "released": bool(metrics["released"][env_id, slot]),
                "milestones": {
                    key: bool(state["milestones"][env_id, slot, index])
                    for index, key in enumerate(("lifted", "inserted", "placed"))
                },
            }
        )
    placed = sum(item["placed"] for item in objects)
    # Current values of the termination conditions (the termination manager's get_term returns
    # the term that ended the previous episode, not the current step).
    terms = {
        "success": bool(metrics["success"][env_id]),
        "object_lost": bool(objects_lost(env)[env_id]),
        "physics_violation": bool(metrics["physics_violation"][env_id]),
        "time_out": bool(env.episode_length_buf[env_id] >= env.max_episode_length),
    }
    return {
        "variant": state["variant"].id,
        "elapsed_s": round(float(env.episode_length_buf[env_id]) * env.step_dt, 4),
        "success": bool(metrics["success"][env_id]),
        "valid_layout": bool(metrics["valid"][env_id]),
        "dwell_s": round(float(state["hold"].elapsed[env_id]), 4),
        "placed": placed,
        "objects_total": len(objects),
        "placed_fraction": placed / max(len(objects), 1),
        "wrong_level": sum(item["wrong_level"] for item in objects),
        "rules": {
            "books_packed": bool(metrics["packed"][env_id]),
            "packed_wall": int(metrics["packed_wall"][env_id]),
            "packing_gap_m": round(float(metrics["packed_gap"][env_id]), 5),
            "display_spaced": bool(metrics["spaced"][env_id]),
            "display_separation_m": round(float(metrics["separation"][env_id]), 5),
            "crate_empty": bool(metrics["crate_empty"][env_id]),
        },
        "violations": {key: bool(state["violations"][env_id, i]) for i, key in enumerate(VIOLATIONS)},
        "peak_joint_speed_ratio": round(float(state["worst"][env_id, 0]), 4),
        "deepest_penetration_m": round(float(state["worst"][env_id, 1]), 5),
        "terminations": terms,
        "objects": objects,
    }


def objects_lost(env):
    state = _runtime(env)
    pos, quat, _, _ = object_data(env)
    local = pos - env.scene.env_origins[:, None, :]
    # Only a scene with a bin has a floor beside the desk; elsewhere that patch of ground is ground.
    layout = state["layout"] if state["table"].trash else None
    return g.lost_flags(local, g.rotation_matrix(quat), state["slots"]["sizes"], state["slots"]["present"], layout)


def milestone_reward(env):
    return current_state(env)["delta"]


def success_reward(env):
    return task_success(env).float()


def task_state(env):
    """Shelf-relative pose of every slot: ``(N, S * 7)``."""
    pos, quat, _, _ = object_data(env)
    shelf = env.scene["shelf"].data
    frame = g.rotation_matrix(shelf.root_quat_w)
    local = torch.einsum("nji,nsj->nsi", frame, pos - shelf.root_pos_w[:, None, :])
    shelf_quat = shelf.root_quat_w[:, None, :].expand_as(quat)
    relative = quat_mul(quat_conjugate(shelf_quat), quat)
    return torch.cat((local, relative), -1).flatten(1)


def task_velocities(env):
    _, _, lin, ang = object_data(env)
    return torch.cat((lin, ang), -1).flatten(1)


def task_progress(env):
    state = _runtime(env)
    metrics = current_state(env)
    return torch.cat(
        (
            state["milestones"].float().flatten(1),
            metrics["placed"].float(),
            metrics["released"].float(),
            metrics["level"].float(),
            metrics["wrong_level"].float(),
            metrics["in_crate"].float(),
            metrics["in_bin"].float(),
            state["violations"].float(),
            metrics["packed"][:, None].float(),
            metrics["spaced"][:, None].float(),
            metrics["crate_empty"][:, None].float(),
            metrics["packed_gap"][:, None],
            metrics["separation"][:, None],
            state["hold"].elapsed[:, None],
        ),
        -1,
    )


def task_goal(env):
    """Static goal description: shelf pose, cavities, bin bounds, wall anchor and per-slot object specs."""
    state = _runtime(env)
    slots = state["slots"]
    shelf = env.scene["shelf"].data
    pose = torch.cat((shelf.root_pos_w - env.scene.env_origins, shelf.root_quat_w), -1)
    layout = state["layout"]
    cavities = pose.new_tensor(tuple((*lo, *hi) for lo, hi in zip(layout.cavity_mins, layout.cavity_maxs))).flatten()
    shelf_pos = pose.new_tensor(layout.shelf_pos)
    bin_bounds = torch.cat((pose.new_tensor(layout.bin_mins) - shelf_pos, pose.new_tensor(layout.bin_maxs) - shelf_pos))
    anchor = {"negative_y": -1.0, "either": 0.0, "positive_y": 1.0}[state["variant"].wall_anchor]
    per_slot = torch.cat(
        (
            slots["present"].float()[:, None],
            slots["category"].float()[:, None],
            slots["required_level"].float()[:, None],
            slots["sizes"],
        ),
        -1,
    ).flatten()
    static = torch.cat((cavities, bin_bounds, pose.new_tensor((anchor,)), per_slot))
    return torch.cat((pose, static.expand(env.num_envs, -1)), -1)


class workspace_point_cloud(ManagerTermBase):
    """Crop the fused depth point cloud to the task workspace in env-local bounds."""

    def __call__(self, env, sensor_cfgs, num_points=4096):
        result = torch.zeros((env.num_envs, num_points, 3), device=env.device)
        lo, hi = result.new_tensor(g.WORKSPACE_BOUNDS)
        for e in range(env.num_envs):
            views = []
            for cfg in sensor_cfgs:
                cam = env.scene[cfg.name]
                points = create_pointcloud_from_depth(
                    intrinsic_matrix=cam.data.intrinsic_matrices[e],
                    depth=cam.data.output["distance_to_image_plane"][e].squeeze(-1),
                    position=cam.data.pos_w[e],
                    orientation=cam.data.quat_w_ros[e],
                    device=env.device,
                ).reshape(-1, 3)
                p = points - env.scene.env_origins[e]
                mask = torch.isfinite(p).all(-1) & ((p >= lo) & (p <= hi)).all(-1)
                views.append(points[mask])
            points = torch.cat(views, 0)
            if len(points):
                ids = torch.randperm(len(points), device=env.device)[:num_points]
                if len(ids) < num_points:
                    ids = torch.cat((ids, torch.randint(len(points), (num_points - len(ids),), device=env.device)))
                result[e] = points[ids]
        return result.flatten(1)


def action_rate_l2_clamped(env):
    return torch.square(env.action_manager.action - env.action_manager.prev_action).sum(-1).clamp(0, 1000)


def action_l2_clamped(env):
    return torch.square(env.action_manager.action).sum(-1).clamp(0, 1000)


def describe_rules(wall_anchor: str, layout: g.Layout = g.DEFAULT_LAYOUT) -> dict:
    """Goal rules and tolerances as plain data for ``describe()``."""
    from . import rules

    if wall_anchor not in WALL_ANCHORS:
        raise ValueError(wall_anchor)
    return {
        "layout": layout.name,
        "levels": dict(zip(g.LEVEL_NAMES, zip(layout.cavity_mins, layout.cavity_maxs))),
        "bin": {"position": layout.bin_pos, "interior": g.BIN_INNER, "pile_allowance_m": g.BIN_PILE_ALLOWANCE},
        "containment_tolerance_m": g.CONTAINMENT_TOLERANCE,
        "support_tolerance_m": g.SUPPORT_TOLERANCE,
        "upright_degrees": g.UPRIGHT_DEGREES,
        "still_linear_mps": g.STILL_LINEAR,
        "still_angular_radps": g.STILL_ANGULAR,
        "hold_seconds": g.HOLD_SECONDS,
        "book_pack_max_gap_m": rules.PACK_MAX_GAP,
        "book_pack_align_degrees": rules.PACK_ALIGN_DEGREES,
        "book_wall_anchor": wall_anchor,
        "display_min_gap_m": rules.DISPLAY_MIN_GAP,
        "display_wall_margin_m": rules.DISPLAY_WALL_MARGIN,
        "frame_facing_degrees": rules.FACING_DEGREES,
        "release_distance_m": RELEASE_DISTANCE,
        "release_force_n": RELEASE_FORCE,
        "validity": {
            "arm_speed_limits_radps": ARM_SPEED_LIMITS,
            "speed_tolerance": SPEED_TOLERANCE,
            "penetration_limit_m": PENETRATION_LIMIT,
            "violations": VIOLATIONS,
        },
    }
