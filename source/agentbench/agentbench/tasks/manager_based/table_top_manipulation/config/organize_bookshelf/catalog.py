# Copyright (c) 2025-2026, The DexVerse Project Developers.
# SPDX-License-Identifier: BSD-3-Clause
"""Object classes, the fixed slot layout and per-variant slot tables.

Every object is described by the axis-aligned box of its colliders at rest (``sizes``),
with the rigid-body origin at the centre of that box. The evaluator only ever sees these
boxes; the frame picture is the only visual-only part.

Display objects deliberately combine one small graspable feature with a bulky body that
blocks the obvious approach (a plant canopy over its pot, a lamp shade over its stem, a
globe over its neck). The crate has no handles and is held by its thin rim; the closed
boxes have no graspable feature at all, so every large object needs two arms. Trash
objects (crumpled paper, empty cans) belong in the waste bin beside the desk, not on the
hutch; the cans are DexVerse benchmark assets referenced from the bundled asset folder.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import torch

from .geometry import LEVEL_BIN, LEVEL_BOOKS, LEVEL_DISPLAY, LEVEL_LARGE

NONE, BOOK, TROPHY, FRAME, PLANT, CRATE, BOX, LAMP, GLOBE, TRASH = range(10)
CATEGORY_NAMES = {
    NONE: "none",
    BOOK: "book",
    TROPHY: "trophy",
    FRAME: "photo frame",
    PLANT: "potted plant",
    CRATE: "storage crate",
    BOX: "storage box",
    LAMP: "desk lamp",
    GLOBE: "globe",
    TRASH: "trash",
}
REQUIRED_LEVEL = {
    BOOK: LEVEL_BOOKS,
    TROPHY: LEVEL_DISPLAY,
    FRAME: LEVEL_DISPLAY,
    PLANT: LEVEL_DISPLAY,
    LAMP: LEVEL_DISPLAY,
    GLOBE: LEVEL_DISPLAY,
    CRATE: LEVEL_LARGE,
    BOX: LEVEL_LARGE,
    TRASH: LEVEL_BIN,
}
DISPLAY_CATEGORIES = (TROPHY, FRAME, PLANT, LAMP, GLOBE)
LARGE_CATEGORIES = (CRATE, BOX)
MAX_GRASP_WIDTH = 0.075
# Bundled DexVerse benchmark assets (the same folder the Kongming and Hanoi tasks use).
ASSET_DIR = Path(__file__).resolve().parents[5] / "assets" / "assets" / "debug_assets"


@dataclass(frozen=True)
class ObjectClass:
    name: str
    category: int
    sizes: tuple[float, float, float]  # collider AABB (x, y, z) at rest; origin at its centre
    mass: float
    color: tuple[float, float, float]
    flat_allowed: bool = False
    grasp_widths: tuple[float, ...] = ()  # empty: no single-gripper feature (two arms needed)
    bimanual: bool = False
    parts: tuple[tuple[str, object], ...] = ()  # builder parameters, see assets.py
    usd: str | None = None  # external USD asset (relative to ASSET_DIR) wrapped by the builder
    scale: tuple[float, float, float] = (1.0, 1.0, 1.0)  # applied to the external asset

    @property
    def required_level(self) -> int:
        return REQUIRED_LEVEL[self.category]

    @property
    def category_name(self) -> str:
        return CATEGORY_NAMES[self.category]

    def part(self, key: str):
        return dict(self.parts)[key]

    def usd_path(self) -> Path | None:
        return None if self.usd is None else ASSET_DIR / self.usd


# Books: (depth X, thickness Y, height Z). Thin enough for a top-edge pinch and short
# enough for the 0.24 m middle opening; six sizes with distinct covers so a scattered
# set reads as different books. ``book_m`` (red) is the packed-row book of the desk starts.
BOOKS = {
    "book_xs": ObjectClass("book_xs", BOOK, (0.110, 0.015, 0.160), 0.15, (0.36, 0.52, 0.30), True, (0.015,)),
    "book_s": ObjectClass("book_s", BOOK, (0.120, 0.020, 0.170), 0.20, (0.18, 0.35, 0.72), True, (0.020,)),
    "book_m": ObjectClass("book_m", BOOK, (0.125, 0.024, 0.180), 0.25, (0.72, 0.18, 0.12), True, (0.024,)),
    "book_l": ObjectClass("book_l", BOOK, (0.130, 0.027, 0.190), 0.30, (0.12, 0.48, 0.30), True, (0.027,)),
    "book_x": ObjectClass("book_x", BOOK, (0.130, 0.030, 0.200), 0.35, (0.85, 0.62, 0.15), True, (0.030,)),
    "book_w": ObjectClass("book_w", BOOK, (0.140, 0.036, 0.195), 0.40, (0.20, 0.20, 0.24), True, (0.036,)),
}

TROPHY_CLASS = ObjectClass(
    "trophy",
    TROPHY,
    (0.07, 0.07, 0.15),
    0.21,
    (0.85, 0.70, 0.20),
    grasp_widths=(0.06, 0.02),
    parts=(
        ("base", (0.07, 0.07, 0.015)),
        ("stem_radius", 0.010),
        ("stem_top", 0.10),
        ("cup_radius", 0.030),
        ("cup_height", 0.05),
    ),
)
FRAME_CLASS = ObjectClass(
    "frame",
    FRAME,
    (0.06, 0.14, 0.16),
    0.15,
    (0.25, 0.20, 0.18),
    grasp_widths=(0.02,),
    parts=(
        ("slab", (0.02, 0.14, 0.16)),
        ("foot", (0.10, 0.04, 0.015)),
    ),
)
# The canopy collides: the pot can only be reached from the side under the leaves.
PLANT_CLASS = ObjectClass(
    "plant",
    PLANT,
    (0.10, 0.10, 0.215),
    0.35,
    (0.70, 0.45, 0.30),
    grasp_widths=(0.06,),
    parts=(("pot_radius", 0.030), ("pot_height", 0.10), ("canopy_radius", 0.05), ("canopy_z", 0.165)),
)
# Desk lamp: a wide shade over a thin stem; the stem is the only pinchable part.
LAMP_CLASS = ObjectClass(
    "lamp",
    LAMP,
    (0.14, 0.14, 0.22),
    0.30,
    (0.30, 0.32, 0.36),
    grasp_widths=(0.016,),
    parts=(
        ("base_radius", 0.055),
        ("base_height", 0.012),
        ("stem_radius", 0.008),
        ("stem_top", 0.16),
        ("shade_radius", 0.07),
        ("shade_height", 0.06),
    ),
)
# Globe: a sphere over a short neck; the neck must be reached below the sphere.
GLOBE_CLASS = ObjectClass(
    "globe",
    GLOBE,
    (0.108, 0.108, 0.17),
    0.30,
    (0.25, 0.45, 0.70),
    grasp_widths=(0.016,),
    parts=(
        ("base_radius", 0.05),
        ("base_height", 0.012),
        ("neck_radius", 0.008),
        ("neck_height", 0.05),
        ("sphere_radius", 0.054),
    ),
)
# Open moving crate without handles: a free rigid body on the desk, 2 kg with 0.5 friction, so
# it can be pushed, slid or carried. Only the 1 cm rim is pinchable, and a single gripper on
# one end would swing it, so a carry takes both arms. Wide enough to hold the jumbled pile
# of a whole shelf's contents; it is slid under the first board rather than lowered in.
CRATE_CLASS = ObjectClass(
    "crate",
    CRATE,
    (0.22, 0.46, 0.20),
    2.0,
    (0.55, 0.42, 0.28),
    grasp_widths=(0.010,),
    bimanual=True,
    parts=(
        ("wall", 0.010),
        ("floor", 0.010),
        ("interior", (0.20, 0.44, 0.19)),
    ),
)
# Closed cardboard boxes: no feature at all; wider than the gripper in every direction, so
# each has to be squeezed between the two hands. Two sizes share the bottom layer.
BOX_S_CLASS = ObjectClass(
    "box_s", BOX, (0.18, 0.24, 0.14), 0.6, (0.74, 0.56, 0.36), bimanual=True, parts=(("label", (0.85, 0.30, 0.25)),)
)
BOX_L_CLASS = ObjectClass(
    "box_l", BOX, (0.18, 0.30, 0.17), 0.9, (0.70, 0.52, 0.33), bimanual=True, parts=(("label", (0.25, 0.45, 0.80)),)
)
# Trash: crumpled paper balls (procedural lumpy meshes) and empty drink cans from the
# DexVerse asset library, one of them crushed flat. All fit a single pinch.
PAPER_A_CLASS = ObjectClass("paper_a", TRASH, (0.076, 0.072, 0.064), 0.02, (0.92, 0.92, 0.88), grasp_widths=(0.06,))
PAPER_B_CLASS = ObjectClass("paper_b", TRASH, (0.070, 0.080, 0.060), 0.02, (0.90, 0.90, 0.85), grasp_widths=(0.06,))
CAN_CRUSHED_CLASS = ObjectClass(
    "can_crushed",
    TRASH,
    (0.070, 0.070, 0.061),
    0.03,
    (0.75, 0.75, 0.78),
    grasp_widths=(0.061, 0.070),
    usd="drink064/model_drink064.usd",
    scale=(1.0, 1.0, 0.5),
)
CAN_SLIM_CLASS = ObjectClass(
    "can_slim",
    TRASH,
    (0.043, 0.043, 0.117),
    0.03,
    (0.75, 0.75, 0.78),
    grasp_widths=(0.043,),
    usd="drink065/model_drink065.usd",
)
DISPLAY_CLASSES = {
    "trophy": TROPHY_CLASS,
    "frame": FRAME_CLASS,
    "plant": PLANT_CLASS,
    "lamp": LAMP_CLASS,
    "globe": GLOBE_CLASS,
}
LARGE_CLASSES = {"crate": CRATE_CLASS, "box_s": BOX_S_CLASS, "box_l": BOX_L_CLASS}
TRASH_CLASSES = {
    "paper_a": PAPER_A_CLASS,
    "paper_b": PAPER_B_CLASS,
    "can_crushed": CAN_CRUSHED_CLASS,
    "can_slim": CAN_SLIM_CLASS,
}
ALL_CLASSES = {**BOOKS, **DISPLAY_CLASSES, **LARGE_CLASSES, **TRASH_CLASSES}

# Fixed slot layout: observations, sensors and milestones are indexed by slot.
NUM_SLOTS = 19
BOOK_SLOTS = tuple(range(10))
DISPLAY_SLOTS = (10, 11, 12)
LARGE_SLOTS = (13, 14)
CRATE_SLOT = LARGE_SLOTS[0]  # the crate, when present, always occupies the first large slot
TRASH_SLOTS = (15, 16, 17, 18)
SLOT_NAMES = tuple(f"slot_{i}" for i in range(NUM_SLOTS))
SLOT_PRIMS = tuple(f"Slot{i}" for i in range(NUM_SLOTS))


@dataclass(frozen=True)
class SlotTable:
    classes: tuple

    @property
    def present(self) -> tuple[bool, ...]:
        return tuple(cls is not None for cls in self.classes)

    @property
    def category(self) -> tuple[int, ...]:
        return tuple(NONE if cls is None else cls.category for cls in self.classes)

    @property
    def required_level(self) -> tuple[int, ...]:
        return tuple(-1 if cls is None else cls.required_level for cls in self.classes)

    @property
    def sizes(self) -> tuple[tuple[float, float, float], ...]:
        return tuple((0.0, 0.0, 0.0) if cls is None else cls.sizes for cls in self.classes)

    @property
    def masses(self) -> tuple[float, ...]:
        return tuple(0.0 if cls is None else cls.mass for cls in self.classes)

    @property
    def flat_allowed(self) -> tuple[bool, ...]:
        return tuple(cls is not None and cls.flat_allowed for cls in self.classes)

    def names(self) -> tuple[str, ...]:
        return tuple("" if cls is None else cls.name for cls in self.classes)

    def present_indices(self) -> tuple[int, ...]:
        return tuple(i for i, cls in enumerate(self.classes) if cls is not None)

    def present_classes(self) -> tuple[ObjectClass, ...]:
        return tuple(cls for cls in self.classes if cls is not None)

    def slot_of(self, name: str) -> int:
        for i, cls in enumerate(self.classes):
            if cls is not None and cls.name == name:
                return i
        raise KeyError(name)

    @property
    def large(self) -> tuple[ObjectClass, ...]:
        return tuple(self.classes[slot] for slot in LARGE_SLOTS if self.classes[slot] is not None)

    @property
    def crate(self) -> ObjectClass | None:
        cls = self.classes[CRATE_SLOT]
        return cls if cls is not None and cls.category == CRATE else None

    @property
    def trash(self) -> tuple[ObjectClass, ...]:
        return tuple(self.classes[slot] for slot in TRASH_SLOTS if self.classes[slot] is not None)

    def count(self, category: int) -> int:
        return sum(1 for cls in self.classes if cls is not None and cls.category == category)

    def tensors(self, device="cpu") -> dict[str, torch.Tensor]:
        category = torch.tensor(self.category, dtype=torch.long, device=device)
        is_display = torch.zeros_like(category, dtype=torch.bool)
        for code in DISPLAY_CATEGORIES:
            is_display |= category == code
        return {
            "present": torch.tensor(self.present, dtype=torch.bool, device=device),
            "category": category,
            "required_level": torch.tensor(self.required_level, dtype=torch.long, device=device),
            "sizes": torch.tensor(self.sizes, dtype=torch.float32, device=device),
            "masses": torch.tensor(self.masses, dtype=torch.float32, device=device),
            "flat_allowed": torch.tensor(self.flat_allowed, dtype=torch.bool, device=device),
            "is_book": category == BOOK,
            "is_display": is_display,
            "is_frame": category == FRAME,
            "is_crate": category == CRATE,
            "is_large": (category == CRATE) | (category == BOX),
            "is_trash": category == TRASH,
        }


def _names(value) -> tuple[str, ...]:
    if value is None:
        return ()
    return (value,) if isinstance(value, str) else tuple(value)


def build_slot_table(books, display, large=None, trash=()) -> SlotTable:
    """Fixed per-variant object set.

    ``books``: 1-10 catalog names (repeats allowed); ``display``: up to 3 distinct display
    objects; ``large``: up to 2 large objects (a crate must come first and cannot share
    the bottom layer with a box); ``trash``: up to 4 trash objects (repeats allowed).
    """
    books, display, large, trash = _names(books), _names(display), _names(large), _names(trash)
    if not 1 <= len(books) <= len(BOOK_SLOTS):
        raise ValueError(f"books must name 1 to {len(BOOK_SLOTS)} catalog entries, got {books!r}")
    if any(name not in BOOKS for name in books):
        raise ValueError(f"books must be catalog names, got {books!r}")
    if len(display) > len(DISPLAY_SLOTS):
        raise ValueError(f"at most {len(DISPLAY_SLOTS)} display objects fit the top layer, got {display!r}")
    if len(set(display)) != len(display) or any(name not in DISPLAY_CLASSES for name in display):
        raise ValueError(f"display must be distinct names from {tuple(DISPLAY_CLASSES)}, got {display!r}")
    if len(large) > len(LARGE_SLOTS) or len(set(large)) != len(large) or any(n not in LARGE_CLASSES for n in large):
        raise ValueError(f"large must be up to {len(LARGE_SLOTS)} distinct names from {tuple(LARGE_CLASSES)}")
    if "crate" in large and large != ("crate",):
        raise ValueError("the crate is the only large object of a crate start")
    if len(trash) > len(TRASH_SLOTS) or any(name not in TRASH_CLASSES for name in trash):
        raise ValueError(f"trash must be up to {len(TRASH_SLOTS)} names from {tuple(TRASH_CLASSES)}, got {trash!r}")
    classes: list = [None] * NUM_SLOTS
    for slot, name in zip(BOOK_SLOTS, books):
        classes[slot] = BOOKS[name]
    for slot, name in zip(DISPLAY_SLOTS, display):
        classes[slot] = DISPLAY_CLASSES[name]
    for slot, name in zip(LARGE_SLOTS, large):
        classes[slot] = LARGE_CLASSES[name]
    for slot, name in zip(TRASH_SLOTS, trash):
        classes[slot] = TRASH_CLASSES[name]
    return SlotTable(tuple(classes))


def display_row_width(table: SlotTable, gap: float = 0.05, wall_margin: float = 0.02) -> float:
    """Shelf width needed to stand the display objects side by side with the rule gaps."""
    widths = [cls.sizes[1] for cls in table.present_classes() if cls.category in DISPLAY_CATEGORIES]
    if not widths:
        return 0.0
    return sum(widths) + gap * (len(widths) - 1) + 2 * wall_margin


def large_row_width(table: SlotTable, gap: float = 0.04, wall_margin: float = 0.02) -> float:
    """Shelf width needed to stand the large objects side by side on the bottom layer."""
    widths = [cls.sizes[1] for cls in table.large]
    if not widths:
        return 0.0
    return sum(widths) + gap * (len(widths) - 1) + 2 * wall_margin


def crate_interior_budget(table: SlotTable, book_gap: float = 0.003, item_gap: float = 0.025, margin: float = 0.015):
    """Crate-local Y length needed to line up the contents in a single packed row.

    This is the capacity check for the ``packed`` crate start mode; the default jumbled
    start drops the objects into the crate instead and needs only the footprint area.
    """
    books = [cls for cls in table.present_classes() if cls.category == BOOK]
    display = [cls for cls in table.present_classes() if cls.category in DISPLAY_CATEGORIES]
    total = 2 * margin
    if books:
        total += sum(cls.sizes[1] for cls in books) + book_gap * (len(books) - 1)
    for cls in display:
        total += item_gap + min(cls.sizes[0], cls.sizes[1])
    return total
