# Copyright (c) 2025-2026, The DexVerse Project Developers.
# SPDX-License-Identifier: BSD-3-Clause
"""Deterministic, cached procedural props for the bookshelf task (primitives only).

Every prop is a USD file with one rigid body whose origin is the centre of its collider
bounding box (``ObjectClass.sizes``), so the tensor evaluator can treat each object as
that box. Visual-only parts (book covers, the frame picture, box tape) carry no
collision. The drink cans wrap DexVerse library assets by reference (convex-hull
colliders from the asset, our own rigid body and mass); the crumpled paper balls are
lumpy convex meshes. Files are published atomically into a cache keyed by the catalog
signature.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import tempfile
from pathlib import Path

from .catalog import (
    ALL_CLASSES,
    BOOKS,
    CRATE_CLASS,
    FRAME_CLASS,
    GLOBE_CLASS,
    LAMP_CLASS,
    LARGE_CLASSES,
    PLANT_CLASS,
    TRASH_CLASSES,
    TROPHY_CLASS,
)
from .geometry import (
    BIN_HEIGHT,
    BIN_INNER,
    BIN_WALL,
    LAYOUTS,
    SHELF_BOARD_THICKNESS,
    TABLE_LEG_INSET,
    TABLE_LEG_SIZE,
    TABLE_THICKNESS,
    TABLE_TOP,
)

ASSET_VERSION = 9
TEXTURE_VERSION = 2
# Procedural wood: light oak planks for the desk top, darker walnut for blockers and legs.
WOOD_TEXTURES = {
    "wood_oak": {"light": (0.80, 0.63, 0.42), "dark": (0.55, 0.37, 0.21), "planks": 4, "rings": 6, "seed": 3},
    "wood_walnut": {"light": (0.52, 0.35, 0.22), "dark": (0.30, 0.19, 0.11), "planks": 1, "rings": 9, "seed": 11},
}
WOOD_TILE = (0.80, 0.40)  # metres covered by one texture repeat along the grain and across it
BIN_COLOR = (0.22, 0.23, 0.25)
SHELF_COLOR = (0.46, 0.30, 0.18)
PAGE_COLOR = (0.88, 0.84, 0.72)


def asset_signature() -> dict:
    return {
        "version": ASSET_VERSION,
        "classes": {
            name: {
                "sizes": cls.sizes,
                "mass": cls.mass,
                "color": cls.color,
                "parts": cls.parts,
                "usd": cls.usd,
                "scale": cls.scale,
            }
            for name, cls in ALL_CLASSES.items()
        },
        "shelf": {
            "floors": {name: layout.floors for name, layout in LAYOUTS.items()},
            "heights": {name: layout.shelf_height for name, layout in LAYOUTS.items()},
            "inner_widths": {name: layout.shelf_inner_width for name, layout in LAYOUTS.items()},
            "inner_depths": {name: layout.shelf_inner_depth for name, layout in LAYOUTS.items()},
            "board": SHELF_BOARD_THICKNESS,
        },
        "bin": {"inner": BIN_INNER, "wall": BIN_WALL},
        "layouts": {name: dataclasses.asdict(layout) for name, layout in LAYOUTS.items()},
        "textures": {"version": TEXTURE_VERSION, "wood": WOOD_TEXTURES, "tile": WOOD_TILE},
    }


def cache_directory(output_dir: Path | None = None) -> Path:
    key = hashlib.sha256(json.dumps(asset_signature(), sort_keys=True).encode()).hexdigest()[:16]
    root = Path(output_dir) if output_dir is not None else Path(tempfile.gettempdir()) / "agentbench_bookshelf"
    return root / key


def build_assets(output_dir: Path | None = None) -> dict:
    """Create the USD props once per signature and return a manifest of their paths."""
    from pxr import Gf, Sdf, Usd, UsdGeom, UsdPhysics, UsdShade

    directory = cache_directory(output_dir)
    directory.mkdir(parents=True, exist_ok=True)

    def build(name, mass, kinematic, populate, center_of_mass=None, friction=None):
        target = directory / f"{name}.usda"
        if target.exists():
            return str(target)
        fd, temporary = tempfile.mkstemp(suffix=".usda", dir=directory)
        os.close(fd)
        stage = Usd.Stage.CreateNew(temporary)
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
        UsdGeom.SetStageMetersPerUnit(stage, 1.0)
        root = UsdGeom.Xform.Define(stage, "/Prop").GetPrim()
        stage.SetDefaultPrim(root)
        body = UsdPhysics.RigidBodyAPI.Apply(root)
        body.CreateKinematicEnabledAttr(kinematic)
        mass_api = UsdPhysics.MassAPI.Apply(root)
        mass_api.CreateMassAttr(mass)
        if center_of_mass is not None:
            mass_api.CreateCenterOfMassAttr(Gf.Vec3f(*center_of_mass))
        physics_mat = UsdShade.Material.Define(stage, "/Prop/Looks/Physics")
        physics = UsdPhysics.MaterialAPI.Apply(physics_mat.GetPrim())
        static, dynamic = friction if friction is not None else ((0.5, 0.4) if kinematic else (0.55, 0.44))
        physics.CreateStaticFrictionAttr(static)
        physics.CreateDynamicFrictionAttr(dynamic)
        physics.CreateRestitutionAttr(0.0)

        def finish(prim, label, color, collision, visible):
            if collision:
                UsdPhysics.CollisionAPI.Apply(prim)
                UsdShade.MaterialBindingAPI.Apply(prim).Bind(physics_mat, materialPurpose="physics")
            if not visible:
                UsdGeom.Imageable(prim).CreateVisibilityAttr(UsdGeom.Tokens.invisible)
            material = UsdShade.Material.Define(stage, f"/Prop/Looks/{label}")
            shader = UsdShade.Shader.Define(stage, f"/Prop/Looks/{label}/Surface")
            shader.CreateIdAttr("UsdPreviewSurface")
            shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*color))
            shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.8)
            material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
            UsdShade.MaterialBindingAPI.Apply(prim).Bind(material)

        def box(label, pos, size, color, collision=True, visible=True):
            cube = UsdGeom.Cube.Define(stage, f"/Prop/{label}")
            cube.CreateSizeAttr(1.0)
            cube.AddTranslateOp().Set(Gf.Vec3d(*pos))
            cube.AddScaleOp().Set(Gf.Vec3f(*size))
            finish(cube.GetPrim(), label, color, collision, visible)

        def cylinder(label, pos, radius, height, color, axis="Z", collision=True, visible=True):
            shape = UsdGeom.Cylinder.Define(stage, f"/Prop/{label}")
            shape.CreateRadiusAttr(radius)
            shape.CreateHeightAttr(height)
            shape.CreateAxisAttr(axis)
            shape.AddTranslateOp().Set(Gf.Vec3d(*pos))
            finish(shape.GetPrim(), label, color, collision, visible)

        def sphere(label, pos, radius, color, collision=False):
            shape = UsdGeom.Sphere.Define(stage, f"/Prop/{label}")
            shape.CreateRadiusAttr(radius)
            shape.AddTranslateOp().Set(Gf.Vec3d(*pos))
            finish(shape.GetPrim(), label, color, collision, True)

        def mesh(label, points, faces, color):
            """Closed triangle mesh with a convex-hull collider."""
            shape = UsdGeom.Mesh.Define(stage, f"/Prop/{label}")
            shape.CreatePointsAttr([Gf.Vec3f(*p) for p in points])
            shape.CreateFaceVertexCountsAttr([3] * len(faces))
            shape.CreateFaceVertexIndicesAttr([int(i) for face in faces for i in face])
            shape.CreateSubdivisionSchemeAttr("none")
            finish(shape.GetPrim(), label, color, True, True)
            UsdPhysics.MeshCollisionAPI.Apply(shape.GetPrim()).CreateApproximationAttr("convexHull")

        def reference(label, usd_path, translate, scale):
            """Reference an external asset; its nested rigid body and mass are stripped."""
            xform = UsdGeom.Xform.Define(stage, f"/Prop/{label}")
            xform.AddTranslateOp().Set(Gf.Vec3d(*translate))
            xform.AddScaleOp().Set(Gf.Vec3f(*scale))
            xform.GetPrim().GetReferences().AddReference(str(usd_path))
            for prim in Usd.PrimRange(xform.GetPrim()):
                if prim.HasAPI(UsdPhysics.RigidBodyAPI):
                    prim.RemoveAPI(UsdPhysics.RigidBodyAPI)
                if prim.HasAPI(UsdPhysics.MassAPI):
                    prim.RemoveAPI(UsdPhysics.MassAPI)
                if prim.HasAPI(UsdPhysics.CollisionAPI):
                    UsdShade.MaterialBindingAPI.Apply(prim).Bind(physics_mat, materialPurpose="physics")

        textured = {}

        def wood_material(texture):
            """UsdPreviewSurface reading a wood texture through the mesh's ``st`` primvar."""
            if texture not in textured:
                path = f"/Prop/Looks/{texture}"
                material = UsdShade.Material.Define(stage, path)
                reader = UsdShade.Shader.Define(stage, f"{path}/StReader")
                reader.CreateIdAttr("UsdPrimvarReader_float2")
                reader.CreateInput("varname", Sdf.ValueTypeNames.Token).Set("st")
                image = UsdShade.Shader.Define(stage, f"{path}/Wood")
                image.CreateIdAttr("UsdUVTexture")
                image.CreateInput("file", Sdf.ValueTypeNames.Asset).Set(f"./{texture}.png")
                image.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("repeat")
                image.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("repeat")
                image.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(reader.ConnectableAPI(), "result")
                image.CreateOutput("rgb", Sdf.ValueTypeNames.Float3)
                surface = UsdShade.Shader.Define(stage, f"{path}/Surface")
                surface.CreateIdAttr("UsdPreviewSurface")
                surface.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(
                    image.ConnectableAPI(), "rgb"
                )
                surface.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.55)
                material.CreateSurfaceOutput().ConnectToSource(surface.ConnectableAPI(), "surface")
                textured[texture] = material
            return textured[texture]

        def panel(label, pos, size, texture):
            """A box collider (invisible) under a UV-mapped, wood-textured box mesh."""
            box(f"{label}Collision", pos, size, (0.5, 0.5, 0.5), visible=False)
            points, counts, indices, uvs, normals = _box_mesh(pos, size)
            shape = UsdGeom.Mesh.Define(stage, f"/Prop/{label}")
            shape.CreatePointsAttr([Gf.Vec3f(*v) for v in points])
            shape.CreateFaceVertexCountsAttr(counts)
            shape.CreateFaceVertexIndicesAttr(indices)
            shape.CreateSubdivisionSchemeAttr("none")
            shape.CreateNormalsAttr([Gf.Vec3f(*n) for n in normals])
            shape.SetNormalsInterpolation(UsdGeom.Tokens.faceVarying)
            st = UsdGeom.PrimvarsAPI(shape).CreatePrimvar(
                "st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.faceVarying
            )
            st.Set([Gf.Vec2f(*uv) for uv in uvs])
            UsdShade.MaterialBindingAPI.Apply(shape.GetPrim()).Bind(wood_material(texture))

        populate(box, cylinder, sphere, mesh, reference, panel)
        stage.GetRootLayer().Save()
        os.replace(temporary, target)
        return str(target)

    props = {}
    for name, cls in BOOKS.items():
        props[name] = build(name, cls.mass, False, _book_populate(cls))
    props["trophy"] = build(
        "trophy", TROPHY_CLASS.mass, False, _trophy_populate(TROPHY_CLASS), center_of_mass=(0.0, 0.0, -0.02)
    )
    props["frame"] = build(
        "frame", FRAME_CLASS.mass, False, _frame_populate(FRAME_CLASS), center_of_mass=(-0.005, 0.0, -0.03)
    )
    props["plant"] = build(
        "plant", PLANT_CLASS.mass, False, _plant_populate(PLANT_CLASS), center_of_mass=(0.0, 0.0, -0.06)
    )
    props["lamp"] = build("lamp", LAMP_CLASS.mass, False, _lamp_populate(LAMP_CLASS), center_of_mass=(0.0, 0.0, -0.07))
    props["globe"] = build(
        "globe", GLOBE_CLASS.mass, False, _globe_populate(GLOBE_CLASS), center_of_mass=(0.0, 0.0, -0.03)
    )
    props["crate"] = build("crate", CRATE_CLASS.mass, False, _crate_populate(CRATE_CLASS))
    for name, cls in LARGE_CLASSES.items():
        if name != "crate":
            props[name] = build(name, cls.mass, False, _box_populate(cls))
    for name, cls in TRASH_CLASSES.items():
        if cls.usd is not None:
            props[name] = build(name, cls.mass, False, _can_populate(cls))
        else:
            props[name] = build(name, cls.mass, False, _paper_populate(cls))
    props["bin"] = build("bin", 5.0, True, _bin_populate())
    shelves = {name: build(f"shelf_{name}", 40.0, True, _shelf_populate(layout)) for name, layout in LAYOUTS.items()}
    textures = {name: _write_wood_texture(directory / f"{name}.png", **spec) for name, spec in WOOD_TEXTURES.items()}
    desks = {
        name: build(f"desk_{name}", 60.0, True, _desk_populate(layout), friction=(0.6, 0.5))
        for name, layout in LAYOUTS.items()
    }
    manifest = {
        **asset_signature(),
        "props": props,
        "shelves": shelves,
        "shelf": shelves["centered"],
        "desks": desks,
        "textures": textures,
        "directory": str(directory),
    }
    fd, temporary = tempfile.mkstemp(suffix=".json", dir=directory)
    with os.fdopen(fd, "w") as stream:
        json.dump(manifest, stream, indent=2)
    os.replace(temporary, directory / "manifest.json")
    return manifest


def _book_populate(cls):
    depth, thickness, height = cls.sizes
    color = cls.color

    def populate(box, cylinder, sphere, mesh, reference, panel):
        box("Collision", (0, 0, 0), cls.sizes, color, visible=False)
        box("Pages", (0.001, 0, 0), (depth - 0.004, thickness - 0.004, height - 0.004), PAGE_COLOR, collision=False)
        for sign, label in ((-1, "CoverBack"), (1, "CoverFront")):
            box(label, (0, sign * (thickness / 2 - 0.001), 0), (depth, 0.002, height), color, collision=False)
        box("Spine", (-depth / 2 + 0.001, 0, 0), (0.002, thickness, height), color, collision=False)
        box(
            "Label",
            (-depth / 2 - 0.0001, 0, height * 0.2),
            (0.0002, thickness * 0.65, height * 0.22),
            PAGE_COLOR,
            collision=False,
        )

    return populate


def _trophy_populate(cls):
    base = cls.part("base")
    stem_radius, stem_top = cls.part("stem_radius"), cls.part("stem_top")
    cup_radius, cup_height = cls.part("cup_radius"), cls.part("cup_height")
    bottom = -cls.sizes[2] / 2
    dark = (0.25, 0.22, 0.20)

    def populate(box, cylinder, sphere, mesh, reference, panel):
        box("Base", (0, 0, bottom + base[2] / 2), base, dark)
        stem_height = stem_top - base[2]
        cylinder("Stem", (0, 0, bottom + base[2] + stem_height / 2), stem_radius, stem_height, cls.color)
        cylinder("Cup", (0, 0, bottom + stem_top + cup_height / 2), cup_radius, cup_height, cls.color)

    return populate


def _frame_populate(cls):
    slab = cls.part("slab")
    foot = cls.part("foot")
    bottom = -cls.sizes[2] / 2
    slab_height = cls.sizes[2] - foot[2]

    def populate(box, cylinder, sphere, mesh, reference, panel):
        box("Foot", (0, 0, bottom + foot[2] / 2), (cls.sizes[0], foot[1], foot[2]), cls.color)
        slab_x = -cls.sizes[0] / 2 + 0.01 + slab[0] / 2
        box("Slab", (slab_x, 0, bottom + foot[2] + slab_height / 2), (slab[0], slab[1], slab_height), cls.color)
        box(
            "Picture",
            (slab_x - slab[0] / 2 - 0.0001, 0, bottom + foot[2] + slab_height / 2),
            (0.0002, slab[1] - 0.02, slab_height - 0.02),
            (0.55, 0.70, 0.85),
            collision=False,
        )

    return populate


def _plant_populate(cls):
    pot_radius, pot_height = cls.part("pot_radius"), cls.part("pot_height")
    canopy_radius, canopy_z = cls.part("canopy_radius"), cls.part("canopy_z")
    bottom = -cls.sizes[2] / 2
    green = (0.20, 0.55, 0.22)

    def populate(box, cylinder, sphere, mesh, reference, panel):
        cylinder("Pot", (0, 0, bottom + pot_height / 2), pot_radius, pot_height, cls.color)
        cylinder(
            "Soil", (0, 0, bottom + pot_height - 0.004), pot_radius - 0.003, 0.004, (0.25, 0.18, 0.12), collision=False
        )
        cylinder("Stem", (0, 0, bottom + pot_height + 0.03), 0.006, 0.06, (0.35, 0.28, 0.15), collision=False)
        # The canopy collides: it blocks a top-down approach to the pot.
        for i, (dx, dy) in enumerate(((0.0, 0.0), (0.01, 0.0), (-0.01, 0.0))):
            sphere(f"Canopy{i}", (dx, dy, bottom + canopy_z - 0.005 * i), canopy_radius, green, collision=i == 0)

    return populate


def _lamp_populate(cls):
    base_radius, base_height = cls.part("base_radius"), cls.part("base_height")
    stem_radius, stem_top = cls.part("stem_radius"), cls.part("stem_top")
    shade_radius, shade_height = cls.part("shade_radius"), cls.part("shade_height")
    bottom = -cls.sizes[2] / 2
    metal = (0.30, 0.30, 0.32)

    def populate(box, cylinder, sphere, mesh, reference, panel):
        cylinder("Base", (0, 0, bottom + base_height / 2), base_radius, base_height, metal)
        stem_height = stem_top - base_height
        cylinder("Stem", (0, 0, bottom + base_height + stem_height / 2), stem_radius, stem_height, metal)
        cylinder("Shade", (0, 0, bottom + stem_top + shade_height / 2), shade_radius, shade_height, cls.color)
        sphere("Bulb", (0, 0, bottom + stem_top + 0.02), 0.015, (1.0, 0.95, 0.7), collision=False)

    return populate


def _globe_populate(cls):
    base_radius, base_height = cls.part("base_radius"), cls.part("base_height")
    neck_radius, neck_height = cls.part("neck_radius"), cls.part("neck_height")
    sphere_radius = cls.part("sphere_radius")
    bottom = -cls.sizes[2] / 2
    metal = (0.30, 0.30, 0.32)

    def populate(box, cylinder, sphere, mesh, reference, panel):
        cylinder("Base", (0, 0, bottom + base_height / 2), base_radius, base_height, metal)
        cylinder("Neck", (0, 0, bottom + base_height + neck_height / 2), neck_radius, neck_height, metal)
        sphere(
            "Sphere",
            (0, 0, bottom + base_height + neck_height + sphere_radius),
            sphere_radius,
            cls.color,
            collision=True,
        )

    return populate


def _crate_populate(cls):
    wall, floor = cls.part("wall"), cls.part("floor")
    depth, width, height = cls.sizes
    bottom = -height / 2
    inner_x = depth - 2 * wall

    def populate(box, cylinder, sphere, mesh, reference, panel):
        box("Floor", (0, 0, bottom + floor / 2), (depth, width, floor), cls.color)
        for sign, label in ((-1, "WallNegX"), (1, "WallPosX")):
            box(label, (sign * (depth / 2 - wall / 2), 0, 0), (wall, width, height), cls.color)
        for sign, label in ((-1, "WallNegY"), (1, "WallPosY")):
            box(label, (0, sign * (width / 2 - wall / 2), 0), (inner_x, wall, height), cls.color)

    return populate


def _box_populate(cls):
    depth, width, height = cls.sizes
    cardboard = cls.color
    tape = (0.80, 0.72, 0.52)
    seam = (0.35, 0.26, 0.16)
    label_color = cls.part("label")

    def populate(box, cylinder, sphere, mesh, reference, panel):
        box("Body", (0, 0, 0), (depth, width, height), cardboard)
        top = height / 2 + 0.0004
        # Packing tape across the lid and down the two short faces, plus the flap seams.
        box("TapeTop", (0, 0, top), (0.035, width + 0.0008, 0.0008), tape, collision=False)
        for sign, label in ((-1, "TapeNegY"), (1, "TapePosY")):
            box(label, (0, sign * (width / 2 + 0.0004), 0), (0.035, 0.0008, height + 0.0008), tape, collision=False)
        for sign, label in ((-1, "SeamNegX"), (1, "SeamPosX")):
            box(label, (sign * depth * 0.25, 0, top), (0.003, width * 0.9, 0.0008), seam, collision=False)
        box(
            "Label",
            (-depth / 2 - 0.0004, width * 0.15, 0.0),
            (0.0008, width * 0.35, height * 0.35),
            (0.95, 0.95, 0.9),
            collision=False,
        )
        box(
            "LabelMark",
            (-depth / 2 - 0.0008, width * 0.15, height * 0.08),
            (0.0008, width * 0.25, height * 0.12),
            label_color,
            collision=False,
        )

    return populate


def _paper_populate(cls):
    """Crumpled paper ball: an icosphere with deterministic radial noise, rescaled to the catalog box."""
    import math
    import random

    def icosphere(subdivisions):
        t = (1 + math.sqrt(5)) / 2
        verts = [
            (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t),
            (0, -1, -t), (0, 1, -t), (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1),
        ]  # fmt: skip
        faces = [
            (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2),
            (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5),
            (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1),
        ]  # fmt: skip
        verts = [tuple(v / math.sqrt(sum(c * c for c in vert)) for v in vert) for vert in verts]
        for _ in range(subdivisions):
            cache = {}
            new_faces = []

            def midpoint(a, b):
                key = (min(a, b), max(a, b))
                if key not in cache:
                    m = tuple((verts[a][i] + verts[b][i]) / 2 for i in range(3))
                    norm = math.sqrt(sum(c * c for c in m))
                    verts.append(tuple(c / norm for c in m))
                    cache[key] = len(verts) - 1
                return cache[key]

            for a, b, c in faces:
                ab, bc, ca = midpoint(a, b), midpoint(b, c), midpoint(c, a)
                new_faces += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
            faces = new_faces
        return verts, faces

    rng = random.Random(cls.name)
    verts, faces = icosphere(2)
    lumpy = [tuple(c * (0.78 + 0.22 * rng.random()) for c in vert) for vert in verts]
    lo = [min(v[i] for v in lumpy) for i in range(3)]
    hi = [max(v[i] for v in lumpy) for i in range(3)]
    points = [tuple((v[i] - (lo[i] + hi[i]) / 2) * cls.sizes[i] / (hi[i] - lo[i]) for i in range(3)) for v in lumpy]

    def populate(box, cylinder, sphere, mesh, reference, panel):
        mesh("Paper", points, faces, cls.color)

    return populate


def _can_populate(cls):
    """A DexVerse drink can, scaled (crushed) and lowered so its box centre is the body origin."""

    def populate(box, cylinder, sphere, mesh, reference, panel):
        reference("Can", cls.usd_path(), (0.0, 0.0, -cls.sizes[2] / 2), cls.scale)

    return populate


def _bin_populate():
    """Open waste bin standing on the ground: floor plus four walls, origin at the floor centre."""

    def populate(box, cylinder, sphere, mesh, reference, panel):
        depth, width = BIN_INNER[0] + 2 * BIN_WALL, BIN_INNER[1] + 2 * BIN_WALL
        box("Floor", (0, 0, BIN_WALL / 2), (depth, width, BIN_WALL), BIN_COLOR)
        for sign, label in ((-1, "WallNegX"), (1, "WallPosX")):
            box(label, (sign * (depth / 2 - BIN_WALL / 2), 0, BIN_HEIGHT / 2), (BIN_WALL, width, BIN_HEIGHT), BIN_COLOR)
        for sign, label in ((-1, "WallNegY"), (1, "WallPosY")):
            box(
                label,
                (0, sign * (width / 2 - BIN_WALL / 2), BIN_HEIGHT / 2),
                (BIN_INNER[0], BIN_WALL, BIN_HEIGHT),
                BIN_COLOR,
            )

    return populate


def _shelf_populate(layout):
    def populate(box, cylinder, sphere, mesh, reference, panel):
        t = SHELF_BOARD_THICKNESS
        depth, width = layout.shelf_inner_depth, layout.shelf_inner_width
        floors, top = layout.floors, layout.shelf_height
        base = floors[0]  # the hutch stands on the desk top; the bottom layer is the desk surface
        height = top - base
        outer_width = width + 2 * t
        # Origin: front face, hutch centre line, ground. Two side panels and the back panel rise
        # from the desk top; the middle and top floors and the top board span between them.
        for sign, label in ((-1, "SideNegY"), (1, "SidePosY")):
            box(
                label,
                ((depth + t) / 2, sign * (width / 2 + t / 2), base + height / 2),
                (depth + t, t, height),
                SHELF_COLOR,
            )
        box("Back", (depth + t / 2, 0, base + height / 2), (t, outer_width, height), SHELF_COLOR)
        for level, floor in enumerate(floors[1:], start=1):
            box(f"Floor{level}", (depth / 2, 0, floor - t / 2), (depth, width, t), SHELF_COLOR)
        box("Top", (depth / 2, 0, top - t / 2), (depth, width, t), SHELF_COLOR)

    return populate


def _desk_populate(layout):
    """Desk in env-local coordinates: oak top, walnut legs and blockers, each a box collider."""

    def populate(box, cylinder, sphere, mesh, reference, panel):
        (x0, y0), (x1, y1) = layout.table_bounds
        top = (x0 + x1) / 2, (y0 + y1) / 2, TABLE_TOP - TABLE_THICKNESS / 2
        panel("Top", top, (x1 - x0, y1 - y0, TABLE_THICKNESS), "wood_oak")
        leg_height = TABLE_TOP - TABLE_THICKNESS
        for index, (sx, sy) in enumerate(((1, 1), (1, -1), (-1, 1), (-1, -1))):
            x = top[0] + sx * ((x1 - x0) / 2 - TABLE_LEG_INSET)
            y = top[1] + sy * ((y1 - y0) / 2 - TABLE_LEG_INSET)
            panel(f"Leg{index}", (x, y, leg_height / 2), (TABLE_LEG_SIZE, TABLE_LEG_SIZE, leg_height), "wood_walnut")
        for index, (lo, hi) in enumerate(layout.blockers):
            centre = tuple((a + b) / 2 for a, b in zip(lo, hi))
            panel(f"Blocker{index}", centre, tuple(b - a for a, b in zip(lo, hi)), "wood_walnut")

    return populate


def _box_mesh(pos, size):
    """Points, face counts, indices, face-varying UVs and normals of an axis-aligned box.

    UVs are in metres divided by ``WOOD_TILE``, with the grain (texture u) along the longest
    in-plane axis of every face, so the wood keeps its scale and runs along each board.
    """
    half = [s / 2 for s in size]
    points, counts, indices, uvs, normals = [], [], [], [], []
    for axis in range(3):
        for sign in (-1, 1):
            u_axis, v_axis = [a for a in range(3) if a != axis]
            if size[v_axis] > size[u_axis]:
                u_axis, v_axis = v_axis, u_axis
            corners = []
            for du, dv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                corner = [0.0, 0.0, 0.0]
                corner[axis] = sign * half[axis]
                corner[u_axis] = du * half[u_axis]
                corner[v_axis] = dv * half[v_axis]
                corners.append(corner)
            # Counter-clockwise when seen from outside along the face normal.
            normal = [0.0, 0.0, 0.0]
            normal[axis] = float(sign)
            edge_a = [corners[1][i] - corners[0][i] for i in range(3)]
            edge_b = [corners[2][i] - corners[0][i] for i in range(3)]
            cross = [
                edge_a[1] * edge_b[2] - edge_a[2] * edge_b[1],
                edge_a[2] * edge_b[0] - edge_a[0] * edge_b[2],
                edge_a[0] * edge_b[1] - edge_a[1] * edge_b[0],
            ]
            if sum(c * n for c, n in zip(cross, normal)) < 0:
                corners.reverse()
            start = len(points)
            for corner in corners:
                points.append(tuple(pos[i] + corner[i] for i in range(3)))
                uvs.append(
                    ((pos[u_axis] + corner[u_axis]) / WOOD_TILE[0], (pos[v_axis] + corner[v_axis]) / WOOD_TILE[1])
                )
                normals.append(tuple(normal))
            counts.append(4)
            indices += [start, start + 1, start + 2, start + 3]
    return points, counts, indices, uvs, normals


def _write_wood_texture(path, light, dark, planks, rings, seed, width=1024, height=512):
    """Tileable procedural wood grain written as an 8-bit RGB PNG (numpy and zlib only)."""
    import struct
    import zlib

    import numpy as np

    path = Path(path)
    if path.exists():
        return str(path)
    rng = np.random.default_rng(seed)
    u = np.arange(width)[None, :] / width
    v = np.arange(height)[:, None] / height

    def waves(count, max_u, max_v, scale):
        """Sum of sines with integer frequencies, so the pattern tiles in both directions."""
        total = np.zeros((height, width))
        for _ in range(count):
            fu, fv = int(rng.integers(1, max_u + 1)), int(rng.integers(0, max_v + 1))
            total += np.sin(2 * np.pi * (fu * u + fv * v) + rng.uniform(0, 2 * np.pi)) / (fu + fv)
        return scale * total / count

    plank_index = (np.floor(v * planks) % planks).astype(int)
    offsets = rng.uniform(0, 1, planks)[plank_index]  # each plank cut from a different part of the log
    warp = waves(12, 3, 2, 1.2) + waves(18, 9, 4, 0.35)
    phase = (v * rings * planks + warp + offsets) % 1.0
    grain = (np.abs(phase - 0.5) * 2) ** 8  # thin dark late-wood lines
    streak_rows = np.convolve(rng.normal(0, 1, height), np.ones(3) / 3, mode="same")[:, None]
    streaks = streak_rows * (0.75 + 0.25 * np.cos(2 * np.pi * u))
    mix = np.clip(0.55 * grain + 0.10 * streaks + 0.25 * (waves(6, 2, 1, 1.0) + 0.5), 0, 1)
    light, dark = np.array(light), np.array(dark)
    rgb = light[None, None, :] * (1 - mix[..., None]) + dark[None, None, :] * mix[..., None]
    if planks > 1:
        rgb *= rng.uniform(0.92, 1.06, planks)[plank_index[:, 0]][:, None, None]
        phase = (v[:, 0] * planks) % 1.0
        seam = (phase < 1.5 * planks / height) | (phase > 1 - 1.5 * planks / height)
        rgb[seam] *= 0.55
    pixels = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    raw = b"".join(b"\x00" + row.tobytes() for row in pixels)

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    fd, temporary = tempfile.mkstemp(suffix=".png", dir=path.parent)
    with os.fdopen(fd, "wb") as stream:
        stream.write(png)
    os.replace(temporary, path)
    return str(path)
