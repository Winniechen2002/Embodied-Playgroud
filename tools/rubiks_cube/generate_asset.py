#!/usr/bin/env python3
"""Generate the reviewable native USD source for the hybrid 3x3 Rubik's Cube."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import importlib.util
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
RUBIKS_GEOMETRY_PATH = (
    REPO_ROOT
    / "source"
    / "agentbench"
    / "agentbench"
    / "tasks"
    / "manager_based"
    / "table_top_manipulation"
    / "config"
    / "rubiks_cube"
    / "rubiks_cube_geometry.py"
)


def _load_rubiks_geometry():
    existing = sys.modules.get("rubiks_cube_geometry")
    if existing is not None:
        return existing
    spec = importlib.util.spec_from_file_location(
        "rubiks_cube_geometry", RUBIKS_GEOMETRY_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"cannot load Rubik's Cube geometry from {RUBIKS_GEOMETRY_PATH}"
        )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_RUBIKS_GEOMETRY = _load_rubiks_geometry()
_GEOMETRY_EXPORTS = frozenset(_RUBIKS_GEOMETRY.__all__)


def __getattr__(name: str):
    if name in _GEOMETRY_EXPORTS:
        return getattr(_RUBIKS_GEOMETRY, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


CUBIE_MASS_KG = 0.099 / 26.0
CORE_MASS_KG = 0.010
WORLD_ANCHOR_MASS_KG = 0.010
CARRIER_MASS_KG = CUBIE_MASS_KG
RIGID_BODY_LINEAR_DAMPING = 0.05
RIGID_BODY_ANGULAR_DAMPING = 0.2
CARRIER_AXES = ("X", "Y", "Z")

DEFAULT_OUTPUT = (
    REPO_ROOT
    / "source"
    / "agentbench"
    / "agentbench"
    / "assets"
    / "articulations"
    / "rubiks_cube"
    / "rubiks_cube.usda"
)

FACE_COLORS = {
    "U": ("white", (0.95, 0.95, 0.95)),
    "D": ("yellow", (1.0, 0.82, 0.02)),
    "F": ("green", (0.02, 0.55, 0.12)),
    "B": ("blue", (0.02, 0.20, 0.85)),
    "R": ("red", (0.85, 0.03, 0.03)),
    "L": ("orange", (1.0, 0.32, 0.02)),
}


def _coord_label(value: int) -> str:
    return {-1: "m1", 0: "z0", 1: "p1"}[value]


@dataclass(frozen=True)
class StickerSpec:
    face: str
    color_name: str
    rgb: tuple[float, float, float]


@dataclass(frozen=True)
class CubieSpec:
    grid_position: tuple[int, int, int]
    prim_name: str
    kind: str
    world_position: tuple[float, float, float]
    stickers: tuple[StickerSpec, ...]


def _stickers_for(position: tuple[int, int, int]) -> tuple[StickerSpec, ...]:
    x, y, z = position
    faces = []
    if z == 1:
        faces.append("U")
    if z == -1:
        faces.append("D")
    if y == -1:
        faces.append("F")
    if y == 1:
        faces.append("B")
    if x == 1:
        faces.append("R")
    if x == -1:
        faces.append("L")
    return tuple(StickerSpec(face, *FACE_COLORS[face]) for face in faces)


def cubie_specs() -> tuple[CubieSpec, ...]:
    specs = []
    for z in (-1, 0, 1):
        for y in (-1, 0, 1):
            for x in (-1, 0, 1):
                position = (x, y, z)
                if position == (0, 0, 0):
                    continue
                stickers = _stickers_for(position)
                specs.append(
                    CubieSpec(
                        grid_position=position,
                        prim_name="cubie_" + "_".join(_coord_label(value) for value in position),
                        kind={1: "center", 2: "edge", 3: "corner"}[len(stickers)],
                        world_position=tuple(
                            value * _RUBIKS_GEOMETRY.CUBIE_PITCH_M
                            for value in position
                        ),
                        stickers=stickers,
                    )
                )
    return tuple(specs)


def mechanism_manifest() -> dict[str, object]:
    return {
        "rigid_body_count": 2 + len(CARRIER_AXES) + len(cubie_specs()),
        "carrier_axes": CARRIER_AXES,
        "revolute_joint_count": len(CARRIER_AXES),
        "core_anchor_count": len(cubie_specs()),
        "carrier_attachment_count": len(CARRIER_AXES) * len(cubie_specs()),
        "world_anchor_count": 1,
        "carrier_transport_lock_count": len(CARRIER_AXES),
        "has_joint_limits": False,
        "has_joint_drives": False,
        "exclude_joints_from_articulation": True,
    }


def _fmt_vector(values: tuple[float, float, float]) -> str:
    return "(" + ", ".join(f"{value:.7f}" for value in values) + ")"


def _rigid_body_header(name: str) -> list[str]:
    return [
        f'        def Xform "{name}" (',
        '            prepend apiSchemas = ["PhysicsRigidBodyAPI", "PhysicsMassAPI", "PhysxRigidBodyAPI"]',
        "        )",
        "        {",
        "            bool physics:rigidBodyEnabled = true",
        f"            float physxRigidBody:linearDamping = {RIGID_BODY_LINEAR_DAMPING}",
        f"            float physxRigidBody:angularDamping = {RIGID_BODY_ANGULAR_DAMPING}",
    ]


def _joint_common(*, enabled: bool) -> list[str]:
    return [
        "            bool physics:collisionEnabled = false",
        "            bool physics:excludeFromArticulation = true",
        f"            bool physics:jointEnabled = {'true' if enabled else 'false'}",
        "            point3f physics:localPos1 = (0, 0, 0)",
        "            quatf physics:localRot0 = (1, 0, 0, 0)",
        "            quatf physics:localRot1 = (1, 0, 0, 0)",
    ]


def build_usda() -> str:
    lines = [
        "#usda 1.0",
        "(",
        '    defaultPrim = "RubiksCube"',
        "    metersPerUnit = 1",
        '    upAxis = "Z"',
        ")",
        "",
        'def Xform "RubiksCube" (',
        '    kind = "component"',
        ")",
        "{",
        '    def Scope "Materials"',
        "    {",
        '        def Material "cubie_physics_material" (',
        '            prepend apiSchemas = ["PhysicsMaterialAPI"]',
        "        )",
        "        {",
        "            float physics:staticFriction = 2",
        "            float physics:dynamicFriction = 1.5",
        "            float physics:restitution = 0",
        "        }",
        "    }",
        "",
        '    def Scope "Mechanism"',
        "    {",
        *_rigid_body_header("world_anchor"),
        "            bool physics:kinematicEnabled = true",
        f"            float physics:mass = {WORLD_ANCHOR_MASS_KG:.9f}",
        "            double3 xformOp:translate = (0, 0, 0)",
        '            uniform token[] xformOpOrder = ["xformOp:translate"]',
        "        }",
        *_rigid_body_header("core"),
        "            bool physics:kinematicEnabled = false",
        f"            float physics:mass = {CORE_MASS_KG:.9f}",
        "            double3 xformOp:translate = (0, 0, 0)",
        '            uniform token[] xformOpOrder = ["xformOp:translate"]',
        "        }",
    ]
    for axis in CARRIER_AXES:
        lines.extend(
            [
                *_rigid_body_header(f"carrier_{axis.lower()}"),
                "            bool physics:kinematicEnabled = false",
                f"            float physics:mass = {CARRIER_MASS_KG:.9f}",
                "            double3 xformOp:translate = (0, 0, 0)",
                '            uniform token[] xformOpOrder = ["xformOp:translate"]',
                "        }",
            ]
        )
    lines.extend(["    }", "", '    def Scope "Cubies"', "    {"])
    for cubie in cubie_specs():
        lines.extend(
            [
                *_rigid_body_header(cubie.prim_name),
                "            bool physics:kinematicEnabled = false",
                f"            float physics:mass = {CUBIE_MASS_KG:.9f}",
                f"            double3 xformOp:translate = {_fmt_vector(cubie.world_position)}",
                '            uniform token[] xformOpOrder = ["xformOp:translate"]',
                "",
                '            def Cube "body" (',
                '                prepend apiSchemas = ["PhysicsCollisionAPI"]',
                "            )",
                "            {",
                f"                double size = {_RUBIKS_GEOMETRY.CUBIE_SIZE_M:.7f}",
                "                color3f[] primvars:displayColor = [(0.015, 0.015, 0.015)]",
                "                rel material:binding:physics = </RubiksCube/Materials/cubie_physics_material> (",
                '                    bindMaterialAs = "weakerThanDescendants"',
                "                )",
                "            }",
            ]
        )
        for sticker in cubie.stickers:
            translation, scale = _RUBIKS_GEOMETRY.sticker_box_transform(
                sticker.face
            )
            lines.extend(
                [
                    "",
                    f'            def Cube "sticker_{sticker.face}"',
                    "            {",
                    "                double size = 1",
                    f"                color3f[] primvars:displayColor = [{_fmt_vector(sticker.rgb)}]",
                    f"                double3 xformOp:translate = {_fmt_vector(translation)}",
                    f"                double3 xformOp:scale = {_fmt_vector(scale)}",
                    '                uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]',
                    "            }",
                ]
            )
        lines.extend(["        }", ""])
    lines.extend(
        [
            "    }",
            "",
            '    def Scope "Joints"',
            "    {",
            '        def PhysicsFixedJoint "world_core_anchor"',
            "        {",
            '            rel physics:body0 = </RubiksCube/Mechanism/world_anchor>',
            '            rel physics:body1 = </RubiksCube/Mechanism/core>',
            "            point3f physics:localPos0 = (0, 0, 0)",
            *_joint_common(enabled=True),
            "        }",
            "",
        ]
    )
    for axis in CARRIER_AXES:
        lower = axis.lower()
        lines.extend(
            [
                f'        def PhysicsRevoluteJoint "carrier_hinge_{lower}"',
                "        {",
                f'            rel physics:body0 = </RubiksCube/Mechanism/core>',
                f'            rel physics:body1 = </RubiksCube/Mechanism/carrier_{lower}>',
                f'            uniform token physics:axis = "{axis}"',
                "            point3f physics:localPos0 = (0, 0, 0)",
                *_joint_common(enabled=True),
                "        }",
                "",
            ]
        )
    for axis in CARRIER_AXES:
        lower = axis.lower()
        lines.extend(
            [
                f'        def PhysicsFixedJoint "carrier_transport_lock_{lower}"',
                "        {",
                '            rel physics:body0 = </RubiksCube/Mechanism/core>',
                f'            rel physics:body1 = </RubiksCube/Mechanism/carrier_{lower}>',
                "            point3f physics:localPos0 = (0, 0, 0)",
                *_joint_common(enabled=False),
                "        }",
                "",
            ]
        )
    for cubie in cubie_specs():
        cubie_path = f"</RubiksCube/Cubies/{cubie.prim_name}>"
        lines.extend(
            [
                f'        def PhysicsFixedJoint "core_anchor_{cubie.prim_name}"',
                "        {",
                '            rel physics:body0 = </RubiksCube/Mechanism/core>',
                f"            rel physics:body1 = {cubie_path}",
                f"            point3f physics:localPos0 = {_fmt_vector(cubie.world_position)}",
                *_joint_common(enabled=True),
                "        }",
                "",
            ]
        )
    for axis in CARRIER_AXES:
        lower = axis.lower()
        for cubie in cubie_specs():
            cubie_path = f"</RubiksCube/Cubies/{cubie.prim_name}>"
            lines.extend(
                [
                    f'        def PhysicsFixedJoint "carrier_attachment_{lower}_{cubie.prim_name}"',
                    "        {",
                    f'            rel physics:body0 = </RubiksCube/Mechanism/carrier_{lower}>',
                    f"            rel physics:body1 = {cubie_path}",
                    f"            point3f physics:localPos0 = {_fmt_vector(cubie.world_position)}",
                    *_joint_common(enabled=False),
                    "        }",
                    "",
                ]
            )
    lines.extend(["    }", "}", ""])
    return "\n".join(lines)


def write_or_check(output: Path, *, check: bool) -> int:
    expected = build_usda()
    if check:
        if not output.exists() or output.read_text() != expected:
            print(f"out of date: {output}")
            return 1
        print(f"up to date: {output}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(expected)
    print(output)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="Fail if the checked-in USDA differs")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return write_or_check(args.output, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
