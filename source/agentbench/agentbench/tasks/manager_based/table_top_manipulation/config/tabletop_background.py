"""Shared native Hanoi-atlas scenery and tabletop task backgrounds.

The runtime and Hanoi atlas use the same original geometry and materials.
This module has no Isaac imports; standalone USD can audit the scene.
"""

from __future__ import annotations

import json

BACKGROUND_VERSION = 2
THEMES = ("laboratory", "workshop")
THEME_PRESETS = {"laboratory": (3, 13), "workshop": (5, 21)}


def initialize_root_pose(root, translation=None, orientation=None):
    """Initialize a new non-physical Xform with the canonical Isaac pose stack.

    Equivalent to the newer Lab helper for the empty room and puzzle parents;
    direct USD authoring also supports the pinned Lab 2.2 / Sim 4.5 runtime.
    """
    from pxr import Gf, UsdGeom

    position = (0.0, 0.0, 0.0) if translation is None else translation
    quaternion = (1.0, 0.0, 0.0, 0.0) if orientation is None else orientation
    xform = UsdGeom.Xformable(root)
    xform.AddTranslateOp(UsdGeom.XformOp.PrecisionDouble).Set(Gf.Vec3d(*position))
    xform.AddOrientOp(UsdGeom.XformOp.PrecisionDouble).Set(Gf.Quatd(float(quaternion[0]), Gf.Vec3d(*quaternion[1:])))
    xform.AddScaleOp(UsdGeom.XformOp.PrecisionDouble).Set(Gf.Vec3d(1.0, 1.0, 1.0))


def author_hanoi_room(stage, root_path, group, task_number):
    """Author clean, spatially separated factory/laboratory scenery in USD."""
    from pxr import Gf, Sdf, Usd, UsdGeom, UsdPhysics, UsdShade

    root = root_path
    UsdGeom.Xform.Define(stage, root)
    palettes = [
        ((0.09, 0.24, 0.29), (0.19, 0.63, 0.61)),
        ((0.24, 0.22, 0.35), (0.71, 0.55, 0.31)),
        ((0.18, 0.25, 0.33), (0.95, 0.62, 0.19)),
        ((0.18, 0.29, 0.35), (0.34, 0.72, 0.90)),
        ((0.23, 0.25, 0.30), (0.50, 0.73, 0.52)),
        ((0.31, 0.23, 0.21), (0.89, 0.61, 0.37)),
        ((0.19, 0.27, 0.30), (0.29, 0.64, 0.73)),
        ((0.24, 0.28, 0.21), (0.80, 0.68, 0.37)),
        ((0.23, 0.24, 0.34), (0.61, 0.59, 0.82)),
        ((0.20, 0.28, 0.31), (0.33, 0.76, 0.67)),
    ]
    wall, accent = palettes[group]
    colors = dict(
        wall=wall,
        accent=accent,
        cream=(0.69, 0.73, 0.72),
        dark=(0.045, 0.066, 0.082),
        floor=(0.29, 0.34, 0.36),
        seam=(0.22, 0.27, 0.29),
        blue=(0.18, 0.41, 0.53),
        screen=(0.025, 0.13, 0.18),
        yellow=(0.91, 0.67, 0.18),
        grey=(0.41, 0.47, 0.49),
    )
    materials = {}
    for name, color in colors.items():
        mat = UsdShade.Material.Define(stage, root + "/Materials/" + name)
        sh = UsdShade.Shader.Define(stage, mat.GetPath().AppendChild("Shader"))
        sh.CreateIdAttr("UsdPreviewSurface")
        sh.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*color))
        sh.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.65)
        if name == "screen":
            sh.CreateInput("emissiveColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.045, 0.25, 0.30))
        mat.CreateSurfaceOutput().ConnectToSource(sh.ConnectableAPI(), "surface")
        materials[name] = mat

    def box(name, pos, size, material="cream"):
        obj = UsdGeom.Cube.Define(stage, root + "/" + name)
        obj.CreateSizeAttr(1)
        obj.AddTranslateOp().Set(Gf.Vec3d(*pos))
        obj.AddScaleOp().Set(Gf.Vec3f(*size))
        UsdShade.MaterialBindingAPI.Apply(obj.GetPrim()).Bind(materials[material])
        return obj

    def cylinder(name, pos, radius, height, material="grey", axis="Z"):
        obj = UsdGeom.Cylinder.Define(stage, root + "/" + name)
        obj.CreateRadiusAttr(radius)
        obj.CreateHeightAttr(height)
        obj.CreateAxisAttr(axis)
        obj.AddTranslateOp().Set(Gf.Vec3d(*pos))
        UsdShade.MaterialBindingAPI.Apply(obj.GetPrim()).Bind(materials[material])
        return obj

    # All scenery is behind the task table (x < -0.12 or y > 1.1), or
    # below its base. It does not enter the rings' manipulation volume.
    box("Floor", (0, 0, 0.004), (8, 8, 0.008), "floor")
    for i in range(-6, 7):
        box("FloorX" + str(i + 6), (i * 0.65, 0, 0.010), (0.008, 8, 0.003), "seam")
        box("FloorY" + str(i + 6), (0, i * 0.65, 0.010), (8, 0.008, 0.003), "seam")
    box("BackWall", (-1.05, 0.2, 1.65), (0.06, 6, 3.3), "wall")
    box("SideWall", (0.30, 2.1, 1.65), (2.7, 0.06, 3.3), "wall")
    box("BackBase", (-1.009, 0.2, 0.11), (0.025, 6, 0.18), "dark")
    box("AccentBand", (-1.008, 0.25, 1.12), (0.027, 6, 0.035), "accent")
    # Lit wall panels and ventilation ribs give scale without fake task text.
    for j, y in enumerate((-1.35, -0.15, 1.05)):
        box("PanelFrame" + str(j), (-0.995, y, 1.87), (0.065, 1.00, 0.82), "dark")
        box("Panel" + str(j), (-0.953, y, 1.87), (0.025, 0.91, 0.73), "cream")
        box("PanelMullion" + str(j), (-0.935, y, 1.87), (0.016, 0.018, 0.73), "wall")
        box("PanelCross" + str(j), (-0.933, y, 1.87), (0.016, 0.91, 0.018), "wall")
    # Rear storage line; different details express ten scene families.
    for j, y in enumerate((-0.75, 0.05, 0.85)):
        box("Cabinet" + str(j), (-0.69, y, 0.42), (0.48, 0.69, 0.81), "grey")
        box("CabinetTop" + str(j), (-0.67, y, 0.84), (0.55, 0.74, 0.05), "dark")
        for k in range(3):
            box("Drawer" + str(j) + "_" + str(k), (-0.439, y, 0.19 + k * 0.23), (0.022, 0.625, 0.18), "cream")
            box("Handle" + str(j) + "_" + str(k), (-0.418, y, 0.20 + k * 0.23), (0.02, 0.24, 0.02), "dark")
    if group in (0, 1, 7):
        # Parts store, display shelves and warehouse packing bins.
        for i, y in enumerate((-0.75, 0.05, 0.85)):
            for h in range(2):
                box(
                    "Bin" + str(i) + "_" + str(h),
                    (-0.67, y + (0.16 if h else -0.16), 0.96),
                    (0.32, 0.27, 0.18),
                    "accent" if h == 0 else "blue",
                )
        for i, y in enumerate((-1.13, 1.21)):
            box("RackPost" + str(i), (-0.88, y, 1.25), (0.045, 0.045, 1.3), "dark")
        box("RackShelf", (-0.78, 0.04, 1.49), (0.36, 2.43, 0.035), "grey")
        for i in range(6):
            box(
                "UpperParcel" + str(i),
                (-0.78, -0.93 + i * 0.38, 1.61),
                (0.28, 0.29, 0.22),
                "accent" if i % 2 else "cream",
            )
    elif group in (2, 8):
        # Machining and tall-column assembly station.
        for i in range(7):
            cylinder(
                "AssemblyPart" + str(i),
                (-0.69, -0.95 + i * 0.30, 1.01 + i % 3 * 0.06),
                0.052,
                0.28 + i % 3 * 0.12,
                "accent" if i % 2 else "grey",
            )
        box("DiagramBoard", (-0.925, 0.2, 1.51), (0.036, 0.94, 0.43), "dark")
        for i in range(6):
            box("DiagramLine" + str(i), (-0.899, -0.15 + i * 0.13, 1.51), (0.012, 0.018, 0.20 + i % 3 * 0.04), "accent")
    elif group in (3, 4, 9):
        # Precision lab with electronic measuring instruments.
        box("Instrument", (-0.66, -0.65, 1.02), (0.32, 0.55, 0.30), "cream")
        box("InstrumentScreen", (-0.490, -0.69, 1.04), (0.02, 0.33, 0.17), "screen")
        for i in range(3):
            cylinder("InstrumentKnob" + str(i), (-0.481, -0.43 + i * 0.075, 0.99), 0.023, 0.027, "accent", "X")
        cylinder("SampleDish", (-0.67, 0.22, 0.9), 0.16, 0.06, "grey")
        for i in range(4):
            cylinder("Specimen" + str(i), (-0.68, 0.58 + i * 0.14, 0.99), 0.038, 0.24, "accent" if i % 2 else "cream")
        box("ControlBoard", (-0.919, 0.35, 1.54), (0.046, 0.90, 0.48), "dark")
        box("ControlScreen", (-0.89, 0.35, 1.54), (0.015, 0.80, 0.38), "screen")
        for i in range(4):
            box("SignalLine" + str(i), (-0.879, 0.08 + i * 0.16, 1.54), (0.01, 0.06, 0.10 + i * 0.03), "accent")
    else:
        # Materials and maintenance workshop.
        box("Toolboard", (-0.938, 0.10, 1.45), (0.05, 1.75, 0.66), "dark")
        for i in range(9):
            y = -0.66 + i * 0.19
            cylinder("ToolPin" + str(i), (-0.895, y, 1.60), 0.018, 0.10, "grey", "X")
            box("ToolStem" + str(i), (-0.863, y, 1.42), (0.035, 0.035, 0.30), "accent" if i % 2 else "cream")
        for i in range(4):
            box(
                "MaterialSample" + str(i),
                (-0.65, -0.82 + i * 0.42, 0.93),
                (0.32, 0.29, 0.13),
                "accent" if i % 2 else "blue",
            )
    # Distinct, restrained side-panel bars for each task in a four-task group.
    for i in range(1 + (task_number - 1) % 4):
        box("SideMarker" + str(i), (0.15 + i * 0.19, 2.055, 1.34), (0.12, 0.028, 0.52), "accent")
    prims = list(Usd.PrimRange(stage.GetPrimAtPath(root)))
    assert not any(p.HasAPI(UsdPhysics.CollisionAPI) or p.HasAPI(UsdPhysics.RigidBodyAPI) for p in prims)
    return dict(
        path=root, prim_count=len(prims), collision_prim_count=0, rigid_body_prim_count=0, palette_group=group + 1
    )


def author_background(stage, root_path, *, theme, table_center, table_size):
    """Spawn the selected colleague preset once, without physical APIs."""
    from pxr import Sdf

    if theme not in THEME_PRESETS:
        raise ValueError(f"Unknown tabletop background theme: {theme}")
    if len(table_center) != 3 or len(table_size) != 3 or any(v <= 0 for v in table_size):
        raise ValueError("Background requires a three-dimensional table center and positive size")
    group, task_number = THEME_PRESETS[theme]
    request = json.dumps(
        dict(version=BACKGROUND_VERSION, theme=theme, table_center=list(table_center), table_size=list(table_size)),
        sort_keys=True,
    )
    existing = stage.GetPrimAtPath(root_path)
    if existing:
        if existing.GetAttribute("background:configuration").Get() != request:
            raise ValueError(f"Background root already exists with different configuration: {root_path}")
        return existing
    author_hanoi_room(stage, root_path, group, task_number)
    root = stage.GetPrimAtPath(root_path)
    root.CreateAttribute("background:configuration", Sdf.ValueTypeNames.String).Set(request)
    root.CreateAttribute("background:theme", Sdf.ValueTypeNames.String).Set(theme)
    root.CreateAttribute("background:version", Sdf.ValueTypeNames.Int).Set(BACKGROUND_VERSION)
    root.CreateAttribute("background:preset", Sdf.ValueTypeNames.String).Set(f"H{task_number:02d}")
    return root
