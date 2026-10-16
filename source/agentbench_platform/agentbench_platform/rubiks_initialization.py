"""Trusted, bounded post-reset settling; no additional reset or hidden attempt."""
from collections import deque
from copy import deepcopy
import math

from .rubiks_physics import load_physics
from .rubiks_scoring import RubiksScorer, contact_pair
from .native_clock import period_from_samples,check_elapsed


def _max_initial_contact_force(row, names):
    """Read the native contact layout for either Panda or five-sensor Sharpa."""
    contacts = row.get('finger_contacts') if isinstance(row, dict) else None
    if isinstance(contacts, list) and len(contacts) == 5:
        forces = []
        for contact in contacts:
            vectors = contact.get('forces_w') if isinstance(contact, dict) else None
            if not isinstance(vectors, list) or not vectors:
                raise ValueError('Incomplete Sharpa contacts')
            for vector in vectors:
                if not isinstance(vector, (list, tuple)) or len(vector) != 3:
                    raise ValueError('Incomplete Sharpa contact force vector')
                values = [float(value) for value in vector]
                if not all(math.isfinite(value) for value in values):
                    raise ValueError('Nonfinite Sharpa contact force')
                forces.append(math.sqrt(sum(value * value for value in values)))
        return max(forces, default=0.)
    return max(contact_pair(row, names))


def initialize_rubiks(state, spec, journal, *, mode, target_sequence=None, max_controls=3600,
                      scorer_factory=None):
    if type(max_controls) is not int or not 16 <= max_controls <= 3600:
        raise ValueError('Initialization must allow 16..3600 controls (at most 120 sim seconds)')
    if not state.reset_done:
        raise RuntimeError('One native reset is required before settling')
    physics = load_physics()
    start = state.env.sim.current_time_step_index
    start_time = state.env.sim.current_time
    journal.write('initialization_begin',dict(after_step=start,native_time_s=start_time,max_controls=max_controls))
    window = deque(maxlen=64)
    index = 0
    last_error = None
    clock_period = None
    def collect():
        nonlocal index,clock_period
        row = state.physical(0, 0)
        index += 1
        journal.write('initialization_substep',dict(index=index,snapshot=row))
        native = physics.native.NativeCubeSample(**row['native'])
        if native.native_step != start+index:
            raise ValueError('Incomplete native initialization sampling')
        if clock_period is None:
            clock_period=period_from_samples(start,start_time,native.native_step,native.native_time_s)
        check_elapsed(native.native_time_s,start_time,index,clock_period)
        names = tuple(sorted(n for n in native.body_names if n.startswith('cubie_')))
        if _max_initial_contact_force(row, names) > 20.:
            raise ValueError('Excessive contact force during initialization')
        window.append(deepcopy(row))
    state.install_hook(collect)
    try:
        for _ in range(max_controls):
            neutral = state.neutral_action() if callable(getattr(state, 'neutral_action', None)) else [0.]*7+[1.]
            state.apply(neutral)
            if len(window) < 64:
                continue
            try:
                factory = scorer_factory or RubiksScorer
                scorer = factory(mode,spec,list(window),initialization_after_step=start,
                                 target_sequence=target_sequence)
            except ValueError as exc:
                last_error = str(exc)
                continue
            journal.write('initialization',dict(after_step=start,samples=list(window),
                initialization_substeps=index,validation=scorer.initialization))
            return scorer
        raise RuntimeError('Rubik initialization budget exhausted: '+str(last_error))
    finally:
        state.install_hook(None)
