"""Owner-only diagnostic conversion; never used to decide success or blame."""
from dataclasses import asdict, is_dataclass
import math
import traceback


def diagnostic_json(value):
    """Preserve native non-finite measurements explicitly without invalid JSON."""
    if is_dataclass(value):
        value = asdict(value)
    if hasattr(value, 'detach'):
        value = value.detach().cpu()
    if hasattr(value, 'tolist'):
        value = value.tolist()
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else {'nonfinite': repr(value)}
    if isinstance(value, dict):
        return {str(k): diagnostic_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [diagnostic_json(v) for v in value]
    raise TypeError(f'Unsupported diagnostic type: {type(value).__name__}')


def capture_diagnostics(read):
    # A diagnostic reader must not turn an otherwise valid outcome into an error.
    try:
        return dict(schema='private-failure-diagnostics-v1', attribution='unreviewed',
                    native=diagnostic_json(read()))
    except Exception:
        return dict(schema='private-failure-diagnostics-v1', attribution='unreviewed',
                    diagnostic_error=traceback.format_exc())


def _read_backend(backend):
    """Read held verdicts only; never call step, snapshot, score, or report updates."""
    evidence = {'backend_class': type(backend).__name__}
    for name in ('failure', 'steps', 'physics_steps', 'previous_action', 'control', 'physics', 'result'):
        if hasattr(backend, name):
            evidence[name] = getattr(backend, name)
    env = getattr(backend, 'env', None)
    if type(backend).__name__ == 'MarbleBackend':
        evidence['native_report'] = env.private_result()
    elif type(backend).__name__ == 'ManiSkillBackend':
        e = backend.e
        evidence.update(native_report=e.report,
            first_violation=getattr(e.oracle, 'first_violation', None),
            physics_step=e.physics_steps, simulation_time_s=e.physics_steps/e.sim_freq)
    elif type(backend).__name__ == 'IsaacEnvironmentBackend':
        evidence.update(physics_step=int(env._sim_step_counter)-backend.start_physics,
            simulation_time_s=max(0.,float(env.sim.current_time)-backend.start_time))
        monitor = backend.monitor
        if monitor is not None:
            evidence['monitor'] = {name: getattr(monitor, name) for name in
                ('failure', 'steps', 'active', 'state', 'moves', 'max_depth', 'stable_seconds')}
        if backend.task['family'] == 'pocket_cube':
            evidence.update(first_failure=env.terminal_guard.first_failure,
                max_shell_penetration_m=env._cube_max_shell_penetration,
                native_rule_failed=env.pocket_cube_rule_failed,
                active_face=env.pocket_cube_active_face, committed_turns=env._cube_committed_turns)
        if backend.task['family'] == 'bookshelf':
            from agentbench.tasks.manager_based.table_top_manipulation.config.organize_bookshelf.mdp import VIOLATIONS
            state = env._bookshelf_state
            evidence['bookshelf'] = dict(violation_names=list(VIOLATIONS),
                violations=state['violations'], peak_speed_ratio_and_penetration_m=state['worst'],
                milestones=state['milestones'], metrics=state.get('metrics'))
    return evidence


def capture_backend_diagnostics(backend):
    # Isaac tensors and native verdicts must be read on the owning simulator thread.
    from .native_backend import DispatchedBackend
    if isinstance(backend, DispatchedBackend):
        return capture_diagnostics(lambda: backend.dispatcher.call(
            lambda: diagnostic_json(_read_backend(backend.backend))))
    return capture_diagnostics(lambda: _read_backend(backend))
