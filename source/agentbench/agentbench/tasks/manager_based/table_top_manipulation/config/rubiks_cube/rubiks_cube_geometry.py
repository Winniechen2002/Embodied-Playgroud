"""Dependency-light physical geometry shared by Rubik's Cube modules."""

from __future__ import annotations


CUBIE_SIZE_M = 0.023
CUBIE_GAP_M = 0.001
CUBIE_PITCH_M = 0.024
CUBE_SIZE_M = 0.071
STICKER_SIZE_M = 0.0195
STICKER_THICKNESS_M = 0.0004


def sticker_box_transform(
    face: str,
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    """Return cubie-local sticker-box center and full XYZ dimensions."""

    offset = CUBIE_SIZE_M * 0.5 + STICKER_THICKNESS_M * 0.5
    transforms = {
        "U": (
            (0.0, 0.0, offset),
            (STICKER_SIZE_M, STICKER_SIZE_M, STICKER_THICKNESS_M),
        ),
        "D": (
            (0.0, 0.0, -offset),
            (STICKER_SIZE_M, STICKER_SIZE_M, STICKER_THICKNESS_M),
        ),
        "F": (
            (0.0, -offset, 0.0),
            (STICKER_SIZE_M, STICKER_THICKNESS_M, STICKER_SIZE_M),
        ),
        "B": (
            (0.0, offset, 0.0),
            (STICKER_SIZE_M, STICKER_THICKNESS_M, STICKER_SIZE_M),
        ),
        "R": (
            (offset, 0.0, 0.0),
            (STICKER_THICKNESS_M, STICKER_SIZE_M, STICKER_SIZE_M),
        ),
        "L": (
            (-offset, 0.0, 0.0),
            (STICKER_THICKNESS_M, STICKER_SIZE_M, STICKER_SIZE_M),
        ),
    }
    try:
        return transforms[face]
    except KeyError as error:
        raise ValueError(f"unsupported sticker face: {face}") from error


__all__ = [
    "CUBIE_SIZE_M",
    "CUBIE_GAP_M",
    "CUBIE_PITCH_M",
    "CUBE_SIZE_M",
    "STICKER_SIZE_M",
    "STICKER_THICKNESS_M",
    "sticker_box_transform",
]
