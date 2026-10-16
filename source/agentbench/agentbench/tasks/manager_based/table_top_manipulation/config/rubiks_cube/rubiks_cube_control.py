"""Native control timing shared by the legacy demo and the benchmark adapter.

This module submits targets only. It contains no grasp or puzzle policy.
"""

def run_decimated_control_cycle(
    *,
    arm_target,
    finger_target,
    decimation: int,
    render_interval: int,
    physics_dt: float,
    submit_targets,
    apply_passive_detent,
    write_data_to_sim,
    sim_step,
    scene_update,
    refresh_active_turn_state,
    render,
    capture,
    observe_physics_step=None,
) -> None:
    """Hold one control target and detent evaluation across native physics steps."""

    if decimation < 1:
        raise ValueError("decimation must be positive")
    if render_interval != decimation:
        raise ValueError("render interval must equal decimation")
    submit_targets(arm_target, finger_target)
    apply_passive_detent()
    for _ in range(decimation):
        write_data_to_sim()
        sim_step(render=False)
        scene_update(dt=physics_dt)
        if observe_physics_step is not None:
            observe_physics_step()
    refresh_active_turn_state()
    render()
    capture()

