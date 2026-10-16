# Copyright (c) 2025-2026, The DexVerse Project Developers.
# SPDX-License-Identifier: BSD-3-Clause
"""Thin environment subclass: action validation, instruction in ``extras``, substep hook.

The platform's native backend installs ``benchmark_substep_hook`` on the environment and
expects it to run after every physics substep (see ``kongming_lock_env.py``). When the
hook is absent, physical validity is still audited after every substep. Every action is
validated first: a batch with the wrong shape, a non-finite entry or an entry outside the
per-component bounds of ``action_bounds()`` raises ``ValueError`` without advancing time.
"""

from __future__ import annotations

import torch
from isaaclab.envs import ManagerBasedRLEnv

from .mdp import describe_rules, episode_report
from .variants import BY_ID, VERSION

ARM_SCALE = 0.5  # JointPositionActionCfg scale
ACTION_TOLERANCE = 1e-5
ACTION_NAMES = (
    tuple(f"left_panda_joint{i}" for i in range(1, 8))
    + ("left_gripper",)
    + tuple(f"right_panda_joint{i}" for i in range(1, 8))
    + ("right_gripper",)
)


class OrganizeBookshelfEnv(ManagerBasedRLEnv):
    def __init__(self, cfg, render_mode=None, **kwargs):
        self.final_reports = {}  # env id -> report of its last finished episode, kept across the auto-reset
        super().__init__(cfg, render_mode, **kwargs)
        self._annotate_extras()

    def _reset_idx(self, env_ids):
        """Store the report of every episode that ends, before the reset clears its state."""
        if hasattr(self, "_bookshelf_state"):
            for env_id in torch.as_tensor(env_ids).reshape(-1).tolist():
                if int(self.episode_length_buf[env_id]) > 0:
                    self.final_reports[env_id] = episode_report(self, env_id)
        super()._reset_idx(env_ids)

    def _annotate_extras(self):
        self.extras["instruction"] = self.cfg.task_instruction
        self.extras["variant"] = self.cfg.variant_id

    def reset(self, *args, **kwargs):
        observations, extras = super().reset(*args, **kwargs)
        self._annotate_extras()
        return observations, extras

    def action_bounds(self) -> tuple[torch.Tensor, torch.Tensor]:
        """Per-component action bounds ``(16,)``: arm entries reach exactly the joint limits.

        An arm entry ``a`` sets the joint target ``default + 0.5 * a``, so its bounds are
        ``(limit - default) / 0.5`` for the lower and upper joint limit; gripper entries are
        in [-1, 1]. Both arms start from mirrored home poses, so their bounds differ.
        """
        if not hasattr(self, "_action_bounds"):
            low, high = [], []
            for robot in ("left_robot", "right_robot"):
                articulation = self.scene[robot]
                limits = articulation.data.joint_pos_limits[0, :7]
                default = articulation.data.default_joint_pos[0, :7]
                low += [(limits[:, 0] - default) / ARM_SCALE, torch.full((1,), -1.0, device=self.device)]
                high += [(limits[:, 1] - default) / ARM_SCALE, torch.full((1,), 1.0, device=self.device)]
            self._action_bounds = (torch.cat(low), torch.cat(high))
        return self._action_bounds

    def validate_action(self, action) -> torch.Tensor:
        """Return the action as a tensor, or raise ``ValueError`` without advancing time."""
        action = torch.as_tensor(action, device=self.device, dtype=torch.float32)
        expected = (self.num_envs, self.action_manager.total_action_dim)
        if tuple(action.shape) != expected:
            raise ValueError(f"action must have shape {expected}, got {tuple(action.shape)}")
        if not torch.isfinite(action).all():
            raise ValueError("action contains non-finite values")
        low, high = self.action_bounds()
        outside = (action < low - ACTION_TOLERANCE) | (action > high + ACTION_TOLERANCE)
        if outside.any():
            env, index = outside.nonzero()[0].tolist()
            raise ValueError(
                f"action[{env}, {index}] ({ACTION_NAMES[index]}) = {float(action[env, index]):.4f} is outside "
                f"[{float(low[index]):.4f}, {float(high[index]):.4f}]"
            )
        return action

    def report(self, env_id: int = 0) -> dict:
        """Evaluation record of one environment: success, per-object outcomes, rule and validity checks."""
        return episode_report(self, env_id)

    def step(self, action):
        action = self.validate_action(action)
        hook = getattr(self, "benchmark_substep_hook", None)
        result = self._step_with_hook(action, hook)
        self._annotate_extras()
        return result

    def _step_with_hook(self, action, hook):
        """``ManagerBasedRLEnv.step`` with ``hook()`` after every physics substep."""
        self.action_manager.process_action(action.to(self.device))
        self.recorder_manager.record_pre_step()
        is_rendering = self.sim.has_gui() or self.sim.has_rtx_sensors()
        for _ in range(self.cfg.decimation):
            self._sim_step_counter += 1
            self.action_manager.apply_action()
            self.scene.write_data_to_sim()
            self.sim.step(render=False)
            self.recorder_manager.record_post_physics_decimation_step()
            if self._sim_step_counter % self.cfg.sim.render_interval == 0 and is_rendering:
                self.sim.render()
            self.scene.update(dt=self.physics_dt)
            # Inspect the measured state at EVERY physics substep, even without
            # a platform observer. A transient violation is sticky until reset.
            from .mdp import _update_violations, _runtime
            _update_violations(self, torch.ones(self.num_envs, dtype=torch.bool, device=self.device))
            _runtime(self).pop('metrics', None)
            if hook is not None:
                hook()
            if getattr(self, 'benchmark_stop_requested', False):
                break
        self.episode_length_buf += 1
        self.common_step_counter += 1
        self.reset_buf = self.termination_manager.compute()
        self.reset_terminated = self.termination_manager.terminated
        self.reset_time_outs = self.termination_manager.time_outs
        self.reward_buf = self.reward_manager.compute(dt=self.step_dt)
        if len(self.recorder_manager.active_terms) > 0:
            self.obs_buf = self.observation_manager.compute()
            self.recorder_manager.record_post_step()
        reset_env_ids = self.reset_buf.nonzero(as_tuple=False).squeeze(-1)
        if len(reset_env_ids) > 0 and not getattr(self, 'benchmark_disable_auto_reset', False):
            self.recorder_manager.record_pre_reset(reset_env_ids)
            self._reset_idx(reset_env_ids)
            if self.sim.has_rtx_sensors() and self.cfg.rerender_on_reset:
                self.sim.render()
            self.recorder_manager.record_post_reset(reset_env_ids)
        self.command_manager.compute(dt=self.step_dt)
        if "interval" in self.event_manager.available_modes:
            self.event_manager.apply(mode="interval", dt=self.step_dt)
        self.obs_buf = self.observation_manager.compute(update_history=True)
        return self.obs_buf, self.reward_buf, self.reset_terminated, self.reset_time_outs, self.extras

    def describe(self) -> dict:
        """Static task description: instruction, action semantics, robots, slots, rules."""
        variant = BY_ID[self.cfg.variant_id]
        table = variant.slot_table()
        robots = {}
        for side, name in (("left", "left_robot"), ("right", "right_robot")):
            articulation = self.scene[name]
            robots[side] = {
                "base_pos": list(articulation.cfg.init_state.pos),
                "base_rot_wxyz": list(articulation.cfg.init_state.rot),
                "joint_names": list(articulation.joint_names),
                "default_joint_pos": articulation.data.default_joint_pos[0].tolist(),
                "joint_pos_limits": articulation.data.joint_pos_limits[0].tolist(),
            }
        arm_semantics = "joint target = default + 0.5 * a radians; the bounds reach exactly the joint limits"
        gripper_semantics = "a < 0 closes both fingers to 0.0 m, otherwise opens them to 0.04 m"
        low, high = self.action_bounds()
        action_spec = [
            {
                "index": index,
                "name": name,
                "low": round(float(low[index]), 6),
                "high": round(float(high[index]), 6),
                "semantics": gripper_semantics if name.endswith("gripper") else arm_semantics,
            }
            for index, name in enumerate(ACTION_NAMES)
        ]
        return {
            # Public task metadata: nothing here names the level, which would reveal misplaced objects.
            "task": {
                "id": f"organize-bookshelf-v{VERSION}",
                "name": "Bookshelf organization",
                "description": self.cfg.task_instruction,
                "instruction_version": VERSION,
                "max_steps": int(self.max_episode_length),
                "time_limit_s": float(self.cfg.episode_length_s),
                "control_hz": round(1.0 / self.step_dt, 3),
            },
            "action_spec": action_spec,
            "robots": robots,
            "slots": {
                "names": list(table.names()),
                "present": list(table.present),
                "category": list(table.category),
                "required_level": list(table.required_level),
                "sizes": [list(size) for size in table.sizes],
            },
            "goal": describe_rules(variant.wall_anchor, variant.geometry()),
            "metadata": variant.record(),
        }
