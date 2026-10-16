# Copyright (c) 2025-2026, The DexVerse Project Developers.
# SPDX-License-Identifier: BSD-3-Clause
"""Dual-Franka bookshelf organization: five settings with four levels each, each with a Play twin.

The five original Gym IDs (one per setting) remain registered as aliases of the D3 levels.
"""

import gymnasium as gym

from .variants import ALIASES, BY_ID, VARIANTS, alias_cfg_class, alias_gym_id

_ENTRY = f"{__name__}.organize_bookshelf_env:OrganizeBookshelfEnv"
_CFG = f"{__name__}.organize_bookshelf_cfg"

for variant in VARIANTS:
    for play in (False, True):
        gym.register(
            id=variant.gym_id(play),
            entry_point=_ENTRY,
            disable_env_checker=True,
            kwargs={"env_cfg_entry_point": f"{_CFG}:{variant.cfg_class(play)}"},
        )
for alias, target in ALIASES.items():
    for play in (False, True):
        gym.register(
            id=alias_gym_id(alias, play),
            entry_point=_ENTRY,
            disable_env_checker=True,
            kwargs={"env_cfg_entry_point": f"{_CFG}:{BY_ID[target].cfg_class(play)}"},
        )
