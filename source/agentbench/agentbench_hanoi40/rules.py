"""Geometry-aware five-ring state-transition monitor, no simulator dependency.

Keeps the shared 22 mm XY, 16 mm Z and 5 mm visible-shell thresholds.
A failure is latched; later recovery cannot turn it into a pass.
"""
import math
from .catalog import successors


class RuleFailure(RuntimeError):
    pass


class Monitor:
    def __init__(self, task, parameters):
        self.task=task; self.parameters=parameters; self.state=tuple(task.start)
        self.active=None; self.failure=None; self.moves=[]; self.steps=0; self.max_depth=0.
        self.stable_seconds=0.

    def fail(self, reason):
        if self.failure is None:
            self.failure={'reason':reason,'step':self.steps,'active':self.active}
        raise RuleFailure(self.failure['reason'])

    def expected(self, i, state=None):
        state=self.state if state is None else state; p=state[i]
        x,y=self.parameters['pegs'][p]
        z=.625+self.task.bases[p]+.0175+.035*sum(q==p for q in state[:i])
        return (x,y,z)

    def seated(self, position, expected):
        return math.hypot(position[0]-expected[0],position[1]-expected[1]) <= .022 and abs(position[2]-expected[2]) <= .016

    def begin(self, move):
        if self.failure: self.fail('already_failed')
        if self.active is not None: self.fail('overlapping_move')
        allowed={m:s for s,m in successors(self.state)}
        move=tuple(move)
        if move not in allowed: self.fail('illegal_top_or_size_or_source')
        self.active=move; self.next_state=allowed[move]
        self.stable_seconds=0.

    def check(self, positions, depth=0., covered_pairs=1, *, dt=0.):
        if self.failure: self.fail('already_failed')
        if not math.isfinite(dt) or dt < 0: self.fail('invalid_time_increment')
        self.steps+=1
        if len(positions)!=5 or any(len(p)!=3 or not all(math.isfinite(v) for v in p) for p in positions): self.fail('nonfinite_or_missing_pose')
        if not math.isfinite(depth) or depth<0 or covered_pairs<=0: self.fail('missing_shell_coverage')
        self.max_depth=max(self.max_depth,depth)
        if depth>.005: self.fail('visible_shell_penetration')
        moving=None if self.active is None else self.active[0]
        for i,p in enumerate(positions):
            if not -.7 < p[1] < .7 or not .1 < p[0] < 1.25 or not .55 < p[2] < 1.65:
                self.fail('object_outside_workspace')
            if i!=moving and not self.seated(p,self.expected(i)):
                self.fail('nonactive_ring_unseated')
        if moving is not None:
            p=positions[moving]
            for peg in range(3):
                candidate=list(self.state); candidate[moving]=peg
                if peg not in self.active[1:] and self.seated(p,self.expected(moving,candidate)):
                    self.fail('active_ring_on_undeclared_peg')
        settled = self.active is None and self.state == tuple(self.task.goal)
        settled = settled and all(self.seated(p,self.expected(i)) for i,p in enumerate(positions))
        self.stable_seconds = self.stable_seconds + dt if settled else 0.

    def end(self, positions):
        if self.failure: self.fail('already_failed')
        if self.active is None: self.fail('end_without_begin')
        self.check(positions)
        if not self.seated(positions[self.active[0]],self.expected(self.active[0],self.next_state)):
            self.fail('active_ring_not_seated_at_target')
        self.moves.append(self.active); self.state=self.next_state; self.active=None

    def result(self, positions):
        success=self.failure is None and self.active is None and self.state==tuple(self.task.goal)
        success=success and len(positions)==5 and all(self.seated(p,self.expected(i)) for i,p in enumerate(positions))
        success=success and self.stable_seconds + 1e-10 >= 1.
        return dict(task_success=success,first_failure=self.failure,completed_moves=len(self.moves),
                    state=list(self.state),goal=list(self.task.goal),physics_checks=self.steps,
                    max_visible_shell_penetration_m=self.max_depth, stable_seconds=self.stable_seconds)


class ObservedMonitor(Monitor):
    """Infer legal moves from measured poses; clients cannot assert begin/end events."""
    def observe(self, positions, depth=0., covered_pairs=1, *, dt):
        if self.failure: self.fail('already_failed')
        if len(positions)!=5 or any(len(p)!=3 or not all(math.isfinite(v) for v in p) for p in positions):
            self.fail('nonfinite_or_missing_pose')
        if not math.isfinite(dt) or dt<=0:self.fail('invalid_time_increment')
        if not math.isfinite(depth) or depth<0 or covered_pairs<=0:self.fail('missing_shell_coverage')
        self.steps+=1;self.max_depth=max(self.max_depth,depth)
        if depth>.005:self.fail('visible_shell_penetration')
        for p in positions:
            if not -.7<p[1]<.7 or not .1<p[0]<1.25 or not .55<p[2]<1.65:self.fail('object_outside_workspace')
        displaced=[i for i,p in enumerate(positions) if not self.seated(p,self.expected(i))]
        if self.active is None and displaced:
            if len(displaced)!=1:self.fail('multiple_rings_unseated')
            ring=displaced[0];source=self.state[ring]
            if any(q==source for q in self.state[ring+1:]):self.fail('non_top_ring_lifted')
            self.active=(ring,source,None);self.stable_seconds=0.
        if self.active is not None:
            ring,source,_=self.active
            if any(i!=ring for i in displaced):self.fail('nonactive_ring_unseated')
            if self.seated(positions[ring],self.expected(ring)):
                self.active=None  # Returned to source without committing a move.
            else:
                for destination in range(3):
                    if destination==source:continue
                    candidate=list(self.state);candidate[ring]=destination
                    if self.seated(positions[ring],self.expected(ring,candidate)):
                        move=(ring,source,destination)
                        if move not in {m for _,m in successors(self.state)}:self.fail('larger_on_smaller')
                        self.moves.append(move);self.state=tuple(candidate);self.active=None
                        break
        settled=self.active is None and self.state==tuple(self.task.goal)
        self.stable_seconds=self.stable_seconds+dt if settled else 0.
