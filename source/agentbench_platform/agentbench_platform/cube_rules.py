"""Load only deterministic cube mathematics; no task registration or physics."""
from functools import lru_cache
import importlib.util
from pathlib import Path
import sys


@lru_cache(maxsize=1)
def load_rules():
    spec=importlib.util.find_spec('agentbench')
    if spec is None or not spec.submodule_search_locations:raise ImportError('Cube mathematics source unavailable')
    path=Path(next(iter(spec.submodule_search_locations)))/'tasks/manager_based/table_top_manipulation/config/rubiks_cube/rubiks_cube_rules.py'
    module_spec=importlib.util.spec_from_file_location('_agentbench_symbolic_rules_v1',path)
    module=importlib.util.module_from_spec(module_spec)
    sys.modules[module_spec.name]=module
    module_spec.loader.exec_module(module)
    return module
