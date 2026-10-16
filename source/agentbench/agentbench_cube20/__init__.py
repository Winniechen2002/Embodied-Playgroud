"""Opt-in: ten matched pocket-cube tasks on ALOHA and Sharpa."""

def register():
    import gymnasium as gym
    from .catalog import ENTRIES
    for task,robot in ENTRIES:
        ident = f'Agentbench-Cube20-{task.id}-Dual{robot.title()}-v0'
        if ident not in gym.registry:
            gym.register(ident, entry_point='agentbench_cube20.native:make',
                         kwargs={'task_id': task.id, 'robot': robot}, disable_env_checker=True)
