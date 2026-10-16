"""Isaac Lab adapter for the shared visual-only tabletop backgrounds."""

import isaaclab.sim as sim_utils
from isaaclab.assets import AssetBaseCfg
from isaaclab.utils import configclass

from .tabletop_background import (
    BACKGROUND_VERSION,
    author_background,
    initialize_root_pose,
)


def spawn_tabletop_background(prim_path, cfg, translation=None, orientation=None, **kwargs):
    """Create the room once per environment; resets need no background events."""
    from pxr import UsdGeom

    del kwargs
    if cfg.background_version != BACKGROUND_VERSION:
        raise ValueError("Background configuration and implementation versions differ")
    stage = sim_utils.get_current_stage()
    parent_expression, name = prim_path.rsplit("/", 1)
    parents = sim_utils.find_matching_prim_paths(parent_expression)
    if not parents:
        raise RuntimeError(f"No environment matches background path: {prim_path}")
    first = None
    for parent in parents:
        path = f"{parent}/{name}"
        existed = bool(stage.GetPrimAtPath(path))
        root = author_background(stage, path, theme=cfg.theme, table_center=cfg.table_center, table_size=cfg.table_size)
        if not existed:
            initialize_root_pose(root, translation=translation, orientation=orientation)
        if not cfg.visible:
            UsdGeom.Imageable(root).MakeInvisible()
        if first is None:
            first = root
    return first


@configclass
class TabletopBackgroundSpawnerCfg(sim_utils.SpawnerCfg):
    func = spawn_tabletop_background
    theme: str = "laboratory"
    background_version: int = BACKGROUND_VERSION
    table_center: tuple[float, float, float] = (0.5, 0.0, 0.35)
    table_size: tuple[float, float, float] = (1.0, 1.2, 0.5)


def background_asset_cfg(theme, table_center, table_size):
    """Set scene.background=None before construction to omit the room entirely."""
    return AssetBaseCfg(
        prim_path="{ENV_REGEX_NS}/Background",
        spawn=TabletopBackgroundSpawnerCfg(theme=theme, table_center=table_center, table_size=table_size),
    )
