#!/usr/bin/env python3
"""Verify that Isaac Sim GPU physics refreshes ``physics:jointEnabled`` at runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ASSET = (
    REPO_ROOT
    / "source"
    / "agentbench"
    / "agentbench"
    / "assets"
    / "articulations"
    / "rubiks_cube"
    / "rubiks_cube.usda"
)
TARGET_CUBIE = "cubie_m1_m1_m1"
TARGET_JOINT = f"core_anchor_{TARGET_CUBIE}"
FREE_FALL_STEPS = 60
REATTACH_STEPS = 120


def close_simulation_app(simulation_app) -> None:
    """Use Isaac Sim's documented immediate shutdown for this short-lived gate."""

    simulation_app.close(wait_for_replicator=False, skip_cleanup=True)


def build_smoke_plan(
    asset: Path,
    *,
    mode: str = "layer",
    free_fall_steps: int = FREE_FALL_STEPS,
    reattach_steps: int = REATTACH_STEPS,
) -> dict[str, object]:
    if mode == "transport":
        return {
            "asset": str(asset),
            "mode": mode,
            "transactions": [
                "prepare_transport",
                "release_world_anchor",
                "reanchor_world",
                "finish_transport",
            ],
            "world_anchor_enabled_sequence": [True, False, True],
            "carrier_hinges_enabled_sequence": [True, False, False, True],
            "transport_locks_enabled_sequence": [False, True, True, False],
            "free_fall_steps": free_fall_steps,
            "reattach_steps": reattach_steps,
        }
    if mode != "layer":
        raise ValueError(f"unsupported smoke mode: {mode!r}")
    return {
        "asset": str(asset),
        "mode": mode,
        "cubie": TARGET_CUBIE,
        "joint": TARGET_JOINT,
        "joint_enabled_sequence": [True, False, True],
        "free_fall_steps": free_fall_steps,
        "reattach_steps": reattach_steps,
    }


def parse_args() -> tuple[argparse.Namespace, object]:
    from isaaclab.app import AppLauncher

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asset", type=Path, default=DEFAULT_ASSET)
    parser.add_argument("--mode", choices=("layer", "transport"), default="layer")
    parser.add_argument("--save-json", type=Path)
    parser.add_argument("--free-fall-steps", type=int, default=FREE_FALL_STEPS)
    parser.add_argument("--reattach-steps", type=int, default=REATTACH_STEPS)
    AppLauncher.add_app_launcher_args(parser)
    return parser.parse_args(), AppLauncher


def main() -> int:
    args, app_launcher_cls = parse_args()
    asset = args.asset.expanduser().resolve()
    if not asset.is_file():
        raise FileNotFoundError(asset)

    simulation_app = app_launcher_cls(args).app
    try:
        import isaaclab.sim as sim_utils
        from isaaclab.assets import RigidObject, RigidObjectCfg
        from isaaclab.sim import SimulationContext
        from pxr import Sdf, UsdPhysics

        plan = build_smoke_plan(
            asset,
            mode=args.mode,
            free_fall_steps=args.free_fall_steps,
            reattach_steps=args.reattach_steps,
        )
        root_path = "/World/RubiksCube"
        cubie_path = f"{root_path}/Cubies/{TARGET_CUBIE}"
        joint_path = f"{root_path}/Joints/{TARGET_JOINT}"
        core_path = f"{root_path}/Mechanism/core"

        sim = SimulationContext(
            sim_utils.SimulationCfg(
                device=args.device,
                dt=1.0 / 120.0,
                gravity=(0.0, 0.0, -9.81),
            )
        )
        print(json.dumps({"progress": "spawn_asset", "asset": str(asset)}), flush=True)
        spawn_cfg = sim_utils.UsdFileCfg(usd_path=str(asset))
        spawn_cfg.func(root_path, spawn_cfg, translation=(0.0, 0.0, 1.0))
        cubie = RigidObject(RigidObjectCfg(prim_path=cubie_path, spawn=None))
        core = RigidObject(RigidObjectCfg(prim_path=core_path, spawn=None))
        print(json.dumps({"progress": "reset_begin"}), flush=True)
        sim.reset()
        cubie.update(sim.cfg.dt)
        core.update(sim.cfg.dt)
        print(json.dumps({"progress": "reset_complete"}), flush=True)

        def step_phase(name: str, count: int) -> None:
            started = time.monotonic()
            print(json.dumps({"progress": f"{name}_begin", "steps": count}), flush=True)
            for index in range(count):
                sim.step(render=False)
                cubie.update(sim.cfg.dt)
                core.update(sim.cfg.dt)
                if index == 0 or (index + 1) % 10 == 0 or index + 1 == count:
                    print(
                        json.dumps(
                            {
                                "progress": name,
                                "completed_steps": index + 1,
                                "elapsed_seconds": time.monotonic() - started,
                            }
                        ),
                        flush=True,
                    )

        if args.mode == "transport":
            hinge_paths = [f"{root_path}/Joints/carrier_hinge_{axis}" for axis in "xyz"]
            lock_paths = [
                f"{root_path}/Joints/carrier_transport_lock_{axis}" for axis in "xyz"
            ]
            world_anchor_path = f"{root_path}/Joints/world_core_anchor"
            hinges = [UsdPhysics.Joint.Get(sim.stage, path) for path in hinge_paths]
            locks = [UsdPhysics.Joint.Get(sim.stage, path) for path in lock_paths]
            world_anchor = UsdPhysics.Joint.Get(sim.stage, world_anchor_path)
            if not all(hinges) or not all(locks) or not world_anchor:
                raise RuntimeError("transport smoke is missing a hinge, lock, or world anchor")

            step_phase("anchored", 10)
            initial_core_position = core.data.root_pos_w[0].detach().cpu().tolist()
            initial_relative = (
                cubie.data.root_pos_w[0] - core.data.root_pos_w[0]
            ).detach().cpu().tolist()
            initial_states = {
                "world_anchor": bool(world_anchor.GetJointEnabledAttr().Get()),
                "hinges": [bool(joint.GetJointEnabledAttr().Get()) for joint in hinges],
                "locks": [bool(joint.GetJointEnabledAttr().Get()) for joint in locks],
            }

            with Sdf.ChangeBlock():
                for joint in hinges:
                    joint.GetJointEnabledAttr().Set(False)
                for joint in locks:
                    joint.GetJointEnabledAttr().Set(True)
            step_phase("transport_prepared", 10)
            prepared_states = {
                "hinges": [bool(joint.GetJointEnabledAttr().Get()) for joint in hinges],
                "locks": [bool(joint.GetJointEnabledAttr().Get()) for joint in locks],
            }

            world_anchor.GetJointEnabledAttr().Set(False)
            step_phase("transport_free_fall", args.free_fall_steps)
            dropped_core_position = core.data.root_pos_w[0].detach().cpu().tolist()
            released_state = bool(world_anchor.GetJointEnabledAttr().Get())

            world_anchor.GetJointEnabledAttr().Set(True)
            step_phase("transport_reattach", args.reattach_steps)
            reattached_core_position = core.data.root_pos_w[0].detach().cpu().tolist()
            final_relative = (
                cubie.data.root_pos_w[0] - core.data.root_pos_w[0]
            ).detach().cpu().tolist()

            with Sdf.ChangeBlock():
                for joint in locks:
                    joint.GetJointEnabledAttr().Set(False)
                for joint in hinges:
                    joint.GetJointEnabledAttr().Set(True)
            step_phase("transport_finished", 10)
            final_states = {
                "world_anchor": bool(world_anchor.GetJointEnabledAttr().Get()),
                "hinges": [bool(joint.GetJointEnabledAttr().Get()) for joint in hinges],
                "locks": [bool(joint.GetJointEnabledAttr().Get()) for joint in locks],
            }
            free_fall_drop_m = initial_core_position[2] - dropped_core_position[2]
            reattach_error_m = sum(
                (actual - expected) ** 2
                for actual, expected in zip(
                    reattached_core_position, initial_core_position, strict=True
                )
            ) ** 0.5
            internal_alignment_error_m = sum(
                (actual - expected) ** 2
                for actual, expected in zip(final_relative, initial_relative, strict=True)
            ) ** 0.5
            passed = (
                initial_states
                == {"world_anchor": True, "hinges": [True] * 3, "locks": [False] * 3}
                and prepared_states == {"hinges": [False] * 3, "locks": [True] * 3}
                and not released_state
                and final_states
                == {"world_anchor": True, "hinges": [True] * 3, "locks": [False] * 3}
                and free_fall_drop_m >= 0.02
                and reattach_error_m <= 0.01
                and internal_alignment_error_m <= 0.001
            )
            payload = {
                **plan,
                "initial_core_position_w": initial_core_position,
                "dropped_core_position_w": dropped_core_position,
                "reattached_core_position_w": reattached_core_position,
                "free_fall_drop_m": free_fall_drop_m,
                "reattach_error_m": reattach_error_m,
                "internal_alignment_error_m": internal_alignment_error_m,
                "initial_states": initial_states,
                "prepared_states": prepared_states,
                "released_world_anchor_state": released_state,
                "final_states": final_states,
                "used_direct_body_state": False,
                "passed": passed,
            }
            print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
            if args.save_json is not None:
                args.save_json.parent.mkdir(parents=True, exist_ok=True)
                args.save_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            return 0 if passed else 2

        joint = UsdPhysics.Joint.Get(sim.stage, joint_path)
        if not joint:
            raise RuntimeError(f"missing joint: {joint_path}")
        enabled_attr = joint.GetJointEnabledAttr()
        initial_enabled = bool(enabled_attr.Get())

        step_phase("anchored", 10)
        initial_position = cubie.data.root_pos_w[0].detach().cpu().tolist()

        enabled_attr.Set(False)
        step_phase("free_fall", args.free_fall_steps)
        dropped_position = cubie.data.root_pos_w[0].detach().cpu().tolist()
        disabled_state = bool(enabled_attr.Get())

        enabled_attr.Set(True)
        step_phase("reattach", args.reattach_steps)
        reattached_position = cubie.data.root_pos_w[0].detach().cpu().tolist()
        final_enabled = bool(enabled_attr.Get())

        free_fall_drop_m = initial_position[2] - dropped_position[2]
        reattach_error_m = sum(
            (actual - expected) ** 2
            for actual, expected in zip(reattached_position, initial_position, strict=True)
        ) ** 0.5
        passed = (
            initial_enabled
            and not disabled_state
            and final_enabled
            and free_fall_drop_m >= 0.02
            and reattach_error_m <= 0.01
        )
        payload = {
            **plan,
            "initial_position_w": initial_position,
            "dropped_position_w": dropped_position,
            "reattached_position_w": reattached_position,
            "free_fall_drop_m": free_fall_drop_m,
            "reattach_error_m": reattach_error_m,
            "initial_enabled": initial_enabled,
            "disabled_state": disabled_state,
            "final_enabled": final_enabled,
            "passed": passed,
        }
        print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
        if args.save_json is not None:
            args.save_json.parent.mkdir(parents=True, exist_ok=True)
            args.save_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        return 0 if passed else 2
    finally:
        close_simulation_app(simulation_app)


if __name__ == "__main__":
    raise SystemExit(main())
