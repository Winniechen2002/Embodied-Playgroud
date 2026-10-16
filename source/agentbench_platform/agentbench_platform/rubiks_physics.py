"""Load dependency-light Rubik measurement code without the Isaac task registry."""
from functools import lru_cache
import importlib
import importlib.machinery
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace


@lru_cache(maxsize=1)
def load_physics():
    # Looking up the top-level spec does not execute agentbench/__init__.py,
    # whose normal behavior registers all simulation tasks and imports Isaac.
    spec = importlib.util.find_spec('agentbench')
    if spec is None or not spec.submodule_search_locations:
        raise ImportError('Install the agentbench physics sources for independent Rubik evaluation')
    directory = Path(next(iter(spec.submodule_search_locations)))/'tasks/manager_based/table_top_manipulation/config/rubiks_cube'
    if not (directory/'rubiks_cube_native_observation.py').is_file():
        raise ImportError('Rubik measurement sources are missing')
    name = '_agentbench_rubiks_physics_v1'
    if name not in sys.modules:
        package = ModuleType(name)
        package.__path__ = [str(directory)]
        package.__spec__ = importlib.machinery.ModuleSpec(name,loader=None,is_package=True)
        sys.modules[name] = package
    modules = {key:importlib.import_module(name+'.rubiks_cube_'+suffix) for key,suffix in (
        ('native','native_observation'),('events','measured_events'),('terminal','terminal'),
        ('constraints','constraint_audit'),('rules','rules'))}
    return SimpleNamespace(**modules)
