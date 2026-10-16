#!/usr/bin/env python3
"""Generate handled Hanoi ring USD meshes for the Hanoi task."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "source" / "agentbench" / "agentbench" / "assets" / "assets" / "hanoi_rings"

RING_HEIGHT = 0.035
PEG_RADIUS = 0.016
PEG_CLEARANCE = 0.022
RING_INNER_RADIUS = PEG_RADIUS + PEG_CLEARANCE
HANDLE_NECK_LENGTH = 0.022
HANDLE_STEM_LENGTH = 0.020
HANDLE_FLANGE_OVERHANG = 0.0
HANDLE_OVERLAP = 0.002
HANDLE_NECK_WIDTH = 0.024
HANDLE_STEM_WIDTH = 0.030
HANDLE_FLANGE_WIDTH = 0.030
HANDLE_HOOK_SPLIT_Z = 0.006
HANDLE_Z_MIN = -RING_HEIGHT * 0.5
HANDLE_Z_MAX = RING_HEIGHT * 0.5
SEGMENTS = 16

RINGS = [
    ("RingXLarge", 0.102, (0.86, 0.18, 0.13), (1.0, 0.0)),
    ("RingLarge", 0.091, (0.95, 0.54, 0.12), (0.0, -1.0)),
    ("RingMedium", 0.080, (0.12, 0.42, 0.88), (1.0, 0.0)),
    ("RingSmall", 0.069, (0.10, 0.62, 0.28), (-1.0, 0.0)),
    ("RingXSmall", 0.058, (0.58, 0.25, 0.82), (1.0, 0.0)),
]


def _segment_points(outer_radius: float, inner_radius: float, index: int) -> list[tuple[float, float, float]]:
    half_h = RING_HEIGHT * 0.5
    theta0 = 2.0 * math.pi * index / SEGMENTS
    theta1 = 2.0 * math.pi * (index + 1) / SEGMENTS

    def point(radius: float, theta: float, z: float) -> tuple[float, float, float]:
        return (radius * math.cos(theta), radius * math.sin(theta), z)

    return [
        point(outer_radius, theta0, half_h),
        point(outer_radius, theta1, half_h),
        point(inner_radius, theta1, half_h),
        point(inner_radius, theta0, half_h),
        point(outer_radius, theta0, -half_h),
        point(outer_radius, theta1, -half_h),
        point(inner_radius, theta1, -half_h),
        point(inner_radius, theta0, -half_h),
    ]


def _segment_mesh(name: str, points: list[tuple[float, float, float]]) -> str:
    counts = [3] * 12
    indices = [
        0, 1, 2, 0, 2, 3,  # top
        7, 6, 5, 7, 5, 4,  # bottom
        4, 5, 1, 4, 1, 0,  # outer face
        5, 6, 2, 5, 2, 1,  # side face
        6, 7, 3, 6, 3, 2,  # inner face
        7, 4, 0, 7, 0, 3,  # side face
    ]
    return f'''
    def Mesh "{name}"
    {{
        int[] faceVertexCounts = [{", ".join(str(value) for value in counts)}]
        int[] faceVertexIndices = [{", ".join(str(value) for value in indices)}]
        point3f[] points = [
            {_format_vec3(points)}
        ]
        uniform token subdivisionScheme = "none"
        rel material:binding = </HanoiRing/Looks/RingMaterial>
    }}
'''


def _box_mesh(name: str, points: list[tuple[float, float, float]]) -> str:
    counts = [3] * 12
    indices = [
        0, 1, 2, 0, 2, 3,  # top
        7, 6, 5, 7, 5, 4,  # bottom
        4, 5, 1, 4, 1, 0,  # -X face
        5, 6, 2, 5, 2, 1,  # outer radial face
        6, 7, 3, 6, 3, 2,  # +X face
        7, 4, 0, 7, 0, 3,  # inner radial face
    ]
    return f'''
    def Mesh "{name}"
    {{
        int[] faceVertexCounts = [{", ".join(str(value) for value in counts)}]
        int[] faceVertexIndices = [{", ".join(str(value) for value in indices)}]
        point3f[] points = [
            {_format_vec3(points)}
        ]
        uniform token subdivisionScheme = "none"
        rel material:binding = </HanoiRing/Looks/RingMaterial>
    }}
'''


def _norm2(vec: tuple[float, float]) -> tuple[float, float]:
    length = math.hypot(vec[0], vec[1])
    if length < 1.0e-8:
        return (0.0, -1.0)
    return (vec[0] / length, vec[1] / length)


def _oriented_box_points(
    inner_radius: float,
    outer_radius: float,
    width: float,
    radial_xy: tuple[float, float],
    z_min: float,
    z_max: float,
) -> list[tuple[float, float, float]]:
    """Create an XY-oriented box that spans along a ring radial direction."""
    half_w = width * 0.5
    radial = _norm2(radial_xy)
    tangent = (-radial[1], radial[0])

    def point(radius: float, tangent_sign: float, z: float) -> tuple[float, float, float]:
        return (
            radial[0] * radius + tangent[0] * half_w * tangent_sign,
            radial[1] * radius + tangent[1] * half_w * tangent_sign,
            z,
        )

    return [
        point(inner_radius, -1.0, z_max),
        point(outer_radius, -1.0, z_max),
        point(outer_radius, 1.0, z_max),
        point(inner_radius, 1.0, z_max),
        point(inner_radius, -1.0, z_min),
        point(outer_radius, -1.0, z_min),
        point(outer_radius, 1.0, z_min),
        point(inner_radius, 1.0, z_min),
    ]


def _handle_meshes(outer_radius: float, radial_xy: tuple[float, float]) -> str:
    neck_inner = outer_radius - HANDLE_OVERLAP
    neck_outer = outer_radius + HANDLE_NECK_LENGTH
    stem_outer = neck_outer + HANDLE_STEM_LENGTH
    flange_outer = stem_outer + HANDLE_FLANGE_OVERHANG
    return "".join(
        [
            _box_mesh(
                "HandleNeck",
                _oriented_box_points(
                    neck_inner,
                    neck_outer,
                    HANDLE_NECK_WIDTH,
                    radial_xy,
                    HANDLE_Z_MIN,
                    HANDLE_Z_MAX,
                ),
            ),
            _box_mesh(
                "HandleStem",
                _oriented_box_points(
                    neck_outer,
                    stem_outer,
                    HANDLE_STEM_WIDTH,
                    radial_xy,
                    HANDLE_Z_MIN,
                    HANDLE_Z_MAX,
                ),
            ),
            _box_mesh(
                "HandleFlange",
                _oriented_box_points(
                    stem_outer,
                    flange_outer,
                    HANDLE_FLANGE_WIDTH,
                    radial_xy,
                    HANDLE_Z_MIN,
                    HANDLE_Z_MAX,
                ),
            ),
        ]
    )


def _format_vec3(values: list[tuple[float, float, float]]) -> str:
    return ",\n            ".join(f"({x:.6f}, {y:.6f}, {z:.6f})" for x, y, z in values)


def _write_ring(
    name: str,
    outer_radius: float,
    color: tuple[float, float, float],
    radial_xy: tuple[float, float],
) -> None:
    inner_radius = RING_INNER_RADIUS
    if inner_radius >= outer_radius:
        raise ValueError(f"{name} inner radius {inner_radius} must be smaller than outer radius {outer_radius}.")
    segment_meshes = "".join(
        _segment_mesh(f"RingSegment_{index:02d}", _segment_points(outer_radius, inner_radius, index))
        for index in range(SEGMENTS)
    )
    handle_meshes = _handle_meshes(outer_radius, radial_xy)
    usd = f'''#usda 1.0
(
    defaultPrim = "HanoiRing"
    metersPerUnit = 1
    upAxis = "Z"
)

def Xform "HanoiRing"
{{
{segment_meshes}
{handle_meshes}

    def Scope "Looks"
    {{
        def Material "RingMaterial"
        {{
            token outputs:surface.connect = </HanoiRing/Looks/RingMaterial/PreviewSurface.outputs:surface>

            def Shader "PreviewSurface"
            {{
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor = ({color[0]:.6f}, {color[1]:.6f}, {color[2]:.6f})
                float inputs:roughness = 0.55
                token outputs:surface
            }}
        }}
    }}
}}
'''
    (ASSET_DIR / f"{name}.usda").write_text(usd, encoding="utf-8")


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for name, outer_radius, color, radial_xy in RINGS:
        _write_ring(name, outer_radius, color, radial_xy)


if __name__ == "__main__":
    main()
