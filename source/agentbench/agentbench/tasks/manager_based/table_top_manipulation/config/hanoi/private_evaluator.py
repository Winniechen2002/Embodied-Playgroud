"""Sealed, task-only Hanoi evaluator. This module never generates trajectories.

The simulator worker owns this object. Agent clients must communicate through
the JSONL entry point, rather than sharing this object's Python process.
"""
from __future__ import annotations

import copy
import math

from .hanoi_rules import (ActiveMove, HanoiRuleMonitor, PEG_NAMES, RINGS_BOTTOM_TO_TOP,
                          is_hanoi_target_state, normalize_target_state)
from .visible_shells import MAX_VISIBLE_SHELL_PENETRATION

DEFAULT_TARGET = {'left': [], 'middle': [], 'right': list(RINGS_BOTTOM_TO_TOP)}


def _json_finite(value):
    """Invalid poses remain explicit failures; serialize non-finite fields as null."""
    if isinstance(value, dict):
        return {key: _json_finite(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_finite(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


class PhysicalRuleTermination(RuntimeError):
    """A state-free terminal signal, safe to cross the agent boundary."""


class PrivateHanoiEvaluator:
    def __init__(self, positions, fingerprint: str, shell_audit: dict, target=None):
        self._target = normalize_target_state(DEFAULT_TARGET if target is None else target)
        flat = [ring for stack in self._target.values() for ring in stack]
        if sorted(flat) != sorted(RINGS_BOTTOM_TO_TOP):
            raise ValueError('Target must contain each of the five rings exactly once')
        for stack in self._target.values():
            if stack != sorted(stack, key=RINGS_BOTTOM_TO_TOP.index):
                raise ValueError('Target must place larger rings below smaller rings')
        self._fingerprint = fingerprint
        # Do not latch target success while the agent still executes a move.
        self._monitor = HanoiRuleMonitor(positions)
        self._first_failure = None
        self._ended = False
        self._steps = 0
        self._moves = 0
        self._audits = []
        self._check(positions, fingerprint, shell_audit, 'initial')

    def _fail(self, reason, label, details=None):
        if self._first_failure is None:
            self._first_failure = {'reason': reason, 'physics_step': self._steps,
                'trajectory_label': label, 'details': copy.deepcopy(details),
                'state_snapshot': self._monitor.prev_state.to_dict()}

    def _guard(self):
        if self._ended:
            raise RuntimeError('Evaluation already ended')
        if self._first_failure is not None:
            raise PhysicalRuleTermination('Task terminated')

    def _check(self, positions, fingerprint, shell_audit, label):
        if self._first_failure is not None:
            return
        if fingerprint != self._fingerprint:
            self._fail('environment_fingerprint_changed', label)
            return
        depth = shell_audit.get('penetration_depth_m')
        if (not isinstance(depth, (int, float)) or not math.isfinite(depth) or depth < 0
                or shell_audit.get('covered_pairs', 0) <= 0
                or (depth > 0 and not shell_audit.get('pair'))):
            self._fail('invalid_or_missing_shell_audit', label)
            return
        record = {'physics_step': self._steps, 'trajectory_label': label,
                  **copy.deepcopy(shell_audit), 'tolerance_m': MAX_VISIBLE_SHELL_PENETRATION}
        self._audits.append(record)
        if depth > MAX_VISIBLE_SHELL_PENETRATION:
            self._fail('visible_shell_penetration', label, record)
            return
        result = self._monitor.update(positions)
        if result.status == 'fail':
            self._fail(result.reason, label, result.to_dict())

    def ensure_running(self):
        """Return no privileged values; hard failure only raises a terminal signal."""
        self._guard()

    def begin_move(self, ring, source_peg, target_peg):
        self._guard()
        if self._monitor.active_move is not None:
            self._fail('overlapping_move_declarations', 'begin_move')
        elif source_peg not in PEG_NAMES or target_peg not in PEG_NAMES or source_peg == target_peg:
            self._fail('invalid_move_declaration', 'begin_move')
        else:
            try:
                result = self._monitor.begin_move(ActiveMove(ring, source_peg, target_peg))
                if result.status == 'fail':
                    self._fail(result.reason, 'begin_move', result.to_dict())
            except (KeyError, ValueError):
                self._fail('invalid_move_declaration', 'begin_move')
        self._guard()

    def end_move(self):
        self._guard()
        if self._monitor.active_move is None:
            self._fail('end_without_active_move', 'end_move')
        else:
            result = self._monitor.end_move()
            if result.status == 'fail':
                self._fail(result.reason, 'end_move', result.to_dict())
            else:
                self._moves += 1
        self._guard()

    def after_physics_step(self, positions, fingerprint, shell_audit, label):
        self._guard()
        self._steps += 1
        self._check(positions, fingerprint, shell_audit, label)
        self._guard()

    def abort(self, reason='execution_aborted'):
        if not self._ended:
            self._fail(reason, 'abort')

    def end_trajectory_and_disclose(self, positions, fingerprint, shell_audit) -> dict:
        if self._ended:
            raise RuntimeError('Result already disclosed')
        self._check(positions, fingerprint, shell_audit, 'finish')
        self._ended = True  # Seal execution before exposing any result.
        matched = is_hanoi_target_state(positions, self._target)
        success = self._first_failure is None and self._monitor.active_move is None and matched
        reason = None if success else (self._first_failure or {}).get('reason',
            'unfinished_active_move' if self._monitor.active_move is not None else 'target_not_reached')
        return _json_finite({'status': 'success' if success else 'fail', 'task': 'franka_hanoi',
                'task_success': success, 'target_state_matched': matched,
                'target_state': copy.deepcopy(self._target), 'completed_moves': self._moves,
                'physics_steps': self._steps, 'first_failure': copy.deepcopy(self._first_failure),
                'initial_environment_fingerprint': self._fingerprint,
                'final_environment_fingerprint': fingerprint,
                'hanoi_rule_result': {'status': 'success' if success else 'fail', 'reason': reason},
                'penetration_tolerance_m': MAX_VISIBLE_SHELL_PENETRATION,
                'penetration_tolerance_source': 'env/hanoi_task.md#penetration-scoring',
                'max_visible_shell_penetration_m': max(
                    (entry['penetration_depth_m'] for entry in self._audits), default=0.0),
                'penetration_audit': copy.deepcopy(self._audits),
                'method_compliance': 'separate_method_audit_required'})


def run_physics_substeps(count, step, audit):
    """Audit immediately after *each* substep. An exception prevents the next one."""
    for _ in range(count):
        step()
        audit()
