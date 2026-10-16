"""Opt-in MuJoCo environments, importable without starting Isaac Sim."""
from gymnasium.envs.registration import register, registry
from .scene import LEVELS, MODES

ENV_IDS=[]
for level in LEVELS:
    for mode in MODES:
        for observation in ('state','vision'):
            suffix='-Vision' if observation=='vision' else ''
            name=f'Agentbench-Marble-{level.title()}-{mode.title()}-FrankaPanda{suffix}-v0'
            if name not in registry:
                register(id=name,entry_point='agentbench_mujoco.env:FrankaMarbleEnv',
                         kwargs=dict(level=level,initial_mode=mode,observation_mode=observation))
            ENV_IDS.append(name)

DUAL_ENV_IDS=[]
for level in LEVELS:
    for mode in MODES:
        for observation in ('state','vision'):
            suffix='-Vision' if observation=='vision' else ''
            name=f'Agentbench-Marble-{level.title()}-{mode.title()}-DualFrankaPanda{suffix}-v0'
            if name not in registry:
                register(id=name,entry_point='agentbench_mujoco.env:FrankaMarbleEnv',
                         kwargs=dict(level=level,initial_mode=mode,observation_mode=observation,dual_arm=True))
            DUAL_ENV_IDS.append(name)

from .campaign_scene import SCENARIOS,TIERS,REDESIGNED,BENCHMARK_SCENARIOS,MULTILEVEL_SCENARIOS,DEFENSE_SCENARIOS,ATLAS_SCENARIOS,OBSERVATION_SCHEMA_VERSION,scenario_names
CAMPAIGN_ENV_IDS=[]
for scenario in SCENARIOS:
    for mode in MODES:
        for observation in ('state','vision'):
            label=''.join(part.title() for part in scenario.split('_'))
            suffix='-Vision' if observation=='vision' else ''
            name=f'Agentbench-Marble-{label}-{mode.title()}-DualFrankaCampaign{suffix}-v0'
            if name not in registry:
                register(id=name,entry_point='agentbench_mujoco.campaign_env:FrankaCampaignEnv',
                         kwargs=dict(scenario=scenario,initial_mode=mode,observation_mode=observation))
            CAMPAIGN_ENV_IDS.append(name)

__all__=['ENV_IDS','DUAL_ENV_IDS','CAMPAIGN_ENV_IDS','LEVELS','MODES','SCENARIOS','TIERS','REDESIGNED','BENCHMARK_SCENARIOS','MULTILEVEL_SCENARIOS','DEFENSE_SCENARIOS','ATLAS_SCENARIOS','OBSERVATION_SCHEMA_VERSION','scenario_names']
