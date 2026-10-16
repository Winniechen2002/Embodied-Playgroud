"""Fail-closed terminal guard, independent of the controller and native reward."""
from dataclasses import dataclass
import math
from .catalog import BY_ID,State,moves

@dataclass
class TerminalGuard:
    task_id: str
    initial_fingerprint: str
    stable_seconds: float = 0.
    first_failure: str | None = None

    def update(self, *, state, angles, speeds, active_face, committed_turns,
               native_failed, penetration_m, fingerprint, dt, physical_goal_matches=True):
        numbers=list(angles)+list(speeds)+[penetration_m,dt]
        reason=None
        if len(angles)!=6 or len(speeds)!=6 or not all(math.isfinite(x) for x in numbers) or dt<=0:
            reason='invalid_measurement'
        elif native_failed:reason='native_rule_failure'
        elif penetration_m>.00025:reason='visible_shell_penetration'
        elif fingerprint!=self.initial_fingerprint:reason='fixed_environment_changed'
        try:
            if len(state)!=16 or any(not math.isfinite(x) or x!=int(x) for x in state):
                raise ValueError('State entries must be exact integers')
            actual=State.from_vector(state)
        except (ValueError,TypeError):actual=None;reason=reason or 'invalid_state'
        if reason is not None and self.first_failure is None:self.first_failure=reason
        task=BY_ID[self.task_id]
        settled=(physical_goal_matches and actual==task.goal and active_face==-1 and committed_turns==len(moves(task.transition))
                 and all(abs(a-round(a/(math.pi/2))*(math.pi/2))<=math.radians(1) for a in angles)
                 and all(abs(v)<.05 for v in speeds) and self.first_failure is None)
        self.stable_seconds=self.stable_seconds+dt if settled else 0.
        return self.stable_seconds+1e-10>=1.
