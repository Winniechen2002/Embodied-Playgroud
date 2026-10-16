"""Portable asset and writable-cache locations; no site-specific path fallback."""
from pathlib import Path
import os
PACKAGE_ROOT=Path(__file__).resolve().parents[1]
CACHE_ROOT=Path(os.environ.get('AGENTBENCH_MANISKILL_CACHE',Path.home()/'.cache/agentbench_maniskill'))
ASSET_ROOT=Path(os.environ.get('AGENTBENCH_MANISKILL_ASSETS',CACHE_ROOT/'assets_v1')).expanduser().resolve()
PREVIOUS=ASSET_ROOT/'scenes'
LEGACY=ASSET_ROOT/'robot_library'
YCB=ASSET_ROOT/'ycb'
PREPARED=PREVIOUS/'prepared'
ARTICULATED=PREVIOUS/'articulated'
NATIVE_ROOT=ASSET_ROOT/'native_robots'
