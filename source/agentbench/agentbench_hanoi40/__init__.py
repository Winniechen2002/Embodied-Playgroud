"""Opt-in native Isaac Lab Hanoi40 registry; importing the catalog is CPU-safe."""
from .catalog import TASKS, BY_ID, shortest_distance


def register():
    import gymnasium as gym
    for task in TASKS:
        ident=task.record()['environment_id']
        if ident not in gym.registry:
            gym.register(ident,entry_point='agentbench_hanoi40:make',disable_env_checker=True,
                         kwargs={'task_id':task.id})


def make(task_id,seed=0,split='nominal',**kwargs):
    from isaaclab.envs import ManagerBasedEnv
    from .isaac_cfg import build_cfg
    return ManagerBasedEnv(build_cfg(task_id,seed,split,**kwargs))


def register_sharpa():
    """Register the 40 FR3 + Sharpa variants without changing existing IDs."""
    import gymnasium as gym
    from .sharpa import TASKS as SHARPA_TASKS
    for task in SHARPA_TASKS:
        ident=task.record()['environment_id']
        if ident not in gym.registry:
            gym.register(ident,entry_point='agentbench_hanoi40:make',disable_env_checker=True,
                         kwargs={'task_id':task.id,'robot':'sharpa'})


def register_sharpa_no_arm():
    """Register matched full-scale tasks with the native 28-action floating hand."""
    import gymnasium as gym
    from .sharpa_no_arm import TASKS as NO_ARM_TASKS
    for task in NO_ARM_TASKS:
        ident=task.record()['environment_id']
        if ident not in gym.registry:
            gym.register(ident,entry_point='agentbench_hanoi40:make',disable_env_checker=True,
                         kwargs={'task_id':task.id,'robot':'sharpa_no_arm'})
