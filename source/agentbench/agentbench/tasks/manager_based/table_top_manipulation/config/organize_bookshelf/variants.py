# Copyright (c) 2025-2026, The DexVerse Project Developers.
# SPDX-License-Identifier: BSD-3-Clause
"""Authored task levels: five settings with four levels each, instructions and metadata.

A *setting* fixes the theme of a task (books only, a full hutch, unpacking a crate,
correcting misplaced objects, clearing trash). Within a setting the levels D1 to D4 grade
the workload and the disorder of the start; D3 is the original variant of each setting.
Every level is a fixed task definition; random seeds only vary its start state.

The metadata produced by ``Variant.record()`` describes authored task demands only; it is
not an empirical difficulty ranking (``grading_basis``). The instruction text is static
per level because the object set is fixed per level; misplaced objects are deliberately
not mentioned so that an agent must notice them.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass

from . import geometry
from .catalog import BOOK_SLOTS, LARGE_SLOTS, SlotTable, build_slot_table, display_row_width, large_row_width
from .sampling import BOOK_START_MODES, CRATE_BOOK_MODES

VERSION = 1
GYM_PREFIX = "Agentbench-OrganizeBookshelf-DualFranka"
GRADING_BASIS = "authored_task_demands_not_empirical_rank"
SETTINGS = ("BooksTable", "ShelfTable", "ShelfCrate", "ShelfCrateFix", "TableClean")
LEVELS = (1, 2, 3, 4)
START_CONTAINERS = ("table", "crate", "shelf")
WALL_ANCHORS = ("either", "negative_y", "positive_y")
# Episode time limit: a base, a share per object that does not start in its place, extra for
# two-arm objects (boxes, the crate) and for unpacking a crate, rounded up to 10 s.
TIME_BASE_S = 30.0
TIME_PER_OBJECT_S = 20.0
TIME_PER_TWO_ARM_OBJECT_S = 30.0
TIME_CRATE_START_S = 60.0
ACTION_SCHEMA = {
    "dims": 16,
    "order": ["left_arm[7]", "left_gripper", "right_arm[7]", "right_gripper"],
    "arm_action": "joint_position_offset_from_default",
    "arm_action_scale": 0.5,
    "gripper_action": "binary_symmetric_position",
    "gripper_open_half_width_m": 0.04,
    "gripper_closed_half_width_m": 0.0,
    "control_hz": 30,
}
LAYER_RULES = {
    "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
    "middle": "the books, standing upright and packed tightly together against one side wall",
    "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; "
    "a photo frame faces outward",
    "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
}
DISPLAY_LABELS = {
    "trophy": "trophy",
    "frame": "photo frame",
    "plant": "potted plant",
    "lamp": "desk lamp",
    "globe": "globe",
}
WALL_PHRASES = {
    "either": "against one side wall",
    "negative_y": "against the left side wall",
    "positive_y": "against the right side wall",
}


def _join(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def _plural(count: int, singular: str, plural: str | None = None) -> str:
    plural = plural or singular + "s"
    return f"{count} {plural}" if count != 1 else f"a {singular}" if singular[0] not in "aeiou" else f"an {singular}"


@dataclass(frozen=True)
class Variant:
    setting: str
    level: int
    name: str
    start_container: str  # "table" | "crate" | "shelf"
    books: tuple[str, ...]
    display: tuple[str, ...]
    large: tuple[str, ...]  # catalog names of the bottom-layer objects: ("crate",), boxes, or ()
    book_start_mode: str = "mixed"
    crate_books: str = "jumbled"
    wall_anchor: str = "either"
    misplaced: tuple[tuple[str, int], ...] = ()  # (object name, wrong layer) pairs
    layout: str = "centered"  # geometry.LAYOUTS key
    row_books: int = 0  # the first ``row_books`` books (one size) start packed standing in a row
    trash: tuple[str, ...] = ()  # trash objects that belong in the waste bin
    stacked_start: bool = False  # desk objects may start on top of each other (physics settles the desk)
    manipulation_demands: tuple[str, ...] = ()
    scenario_demands: tuple[str, ...] = ()

    def __post_init__(self):
        if isinstance(self.large, str) or self.large is None:
            object.__setattr__(self, "large", () if self.large is None else (self.large,))
        if self.misplaced and isinstance(self.misplaced[0], str):
            object.__setattr__(self, "misplaced", (tuple(self.misplaced),))
        object.__setattr__(self, "misplaced", tuple(tuple(pair) for pair in self.misplaced))
        if self.setting not in SETTINGS and not self.setting.startswith("Test"):
            raise ValueError(f"unknown setting {self.setting!r}")
        if self.level not in LEVELS:
            raise ValueError(f"{self.id}: level must be one of {LEVELS}")
        if self.start_container not in START_CONTAINERS:
            raise ValueError(f"{self.id}: unknown start container {self.start_container!r}")
        if (self.start_container == "crate") != ("crate" in self.large):
            raise ValueError(f"{self.id}: the open crate is used exactly when objects start inside it")
        if self.book_start_mode not in BOOK_START_MODES or self.crate_books not in CRATE_BOOK_MODES:
            raise ValueError(f"{self.id}: unknown start mode")
        if self.wall_anchor not in WALL_ANCHORS:
            raise ValueError(f"{self.id}: unknown wall anchor {self.wall_anchor!r}")
        if self.layout not in geometry.LAYOUTS:
            raise ValueError(f"{self.id}: unknown layout {self.layout!r}")
        if not 0 <= self.row_books <= len(self.books) or len(set(self.books[: self.row_books])) > 1:
            raise ValueError(f"{self.id}: row books must be a leading run of identical catalog names")
        if (self.row_books or self.stacked_start) and self.start_container != "table":
            raise ValueError(f"{self.id}: a packed row and stacked starts only apply to desk starts")
        if self.trash and self.start_container != "table":
            raise ValueError(f"{self.id}: trash objects only appear in desk starts")
        if self.start_container == "shelf":
            if self.large or not self.misplaced:
                raise ValueError(f"{self.id}: a shelf start has no large objects and at least one misplaced object")
        table = self.slot_table()
        width = self.geometry().shelf_inner_width
        if display_row_width(table) > width or large_row_width(table) > width:
            raise ValueError(f"{self.id}: the display or large objects do not fit their layer with the rule gaps")
        seen = set()
        for name, level in self.misplaced:
            slot = self._slot_of(name)
            cls = table.classes[slot]
            if slot in LARGE_SLOTS or slot in seen:
                raise ValueError(
                    f"{self.id}: misplaced object {name!r} must be a distinct book, display object or trash"
                )
            if level == cls.required_level or not 0 <= level < geometry.NUM_LEVELS:
                raise ValueError(f"{self.id}: misplaced level {level} must be a different shelf layer")
            seen.add(slot)

    @property
    def id(self) -> str:
        return f"{self.setting}D{self.level}"

    @property
    def order(self) -> tuple[int, int]:
        return (SETTINGS.index(self.setting) + 1 if self.setting in SETTINGS else 0, self.level)

    def _slot_of(self, name: str) -> int:
        try:
            return self.slot_table().slot_of(name)
        except KeyError:
            raise ValueError(f"{self.id}: {name!r} is not part of the object set") from None

    def slot_table(self) -> SlotTable:
        return build_slot_table(self.books, self.display, self.large, self.trash)

    def geometry(self) -> geometry.Layout:
        return geometry.LAYOUTS[self.layout]

    def row_slots(self) -> tuple[int, ...]:
        return tuple(BOOK_SLOTS[: self.row_books])

    def misplaced_slots(self) -> tuple[tuple[int, int], ...]:
        """``(slot, wrong layer)`` for every object that starts on a wrong shelf layer."""
        return tuple((self._slot_of(name), level) for name, level in self.misplaced)

    def preshelved_slots(self) -> tuple[int, ...]:
        """Slots that start correctly placed: every non-misplaced object of a shelf start."""
        if self.start_container != "shelf":
            return ()
        misplaced = {slot for slot, _ in self.misplaced_slots()}
        return tuple(slot for slot in self.slot_table().present_indices() if slot not in misplaced)

    def workload(self) -> dict:
        """Objects that do not start in their place, and the two-arm objects among them."""
        table = self.slot_table()
        moving = [slot for slot in table.present_indices() if slot not in self.preshelved_slots()]
        two_arm = sum(1 for slot in moving if table.classes[slot].bimanual)
        return {"objects_to_place": len(moving), "two_arm_objects": two_arm}

    @property
    def episode_length_s(self) -> float:
        work = self.workload()
        seconds = (
            TIME_BASE_S
            + TIME_PER_OBJECT_S * work["objects_to_place"]
            + TIME_PER_TWO_ARM_OBJECT_S * work["two_arm_objects"]
            + (TIME_CRATE_START_S if self.start_container == "crate" else 0.0)
        )
        return float(math.ceil(seconds / 10.0) * 10)

    def gym_id(self, play: bool = False) -> str:
        return f"{GYM_PREFIX}-{self.id}{'-Play' if play else ''}-v0"

    def cfg_class(self, play: bool = False) -> str:
        return f"OrganizeBookshelf{self.id}EnvCfg{'_PLAY' if play else ''}"

    def trash_counts(self) -> tuple[int, int]:
        """(crumpled paper balls, drink cans)."""
        papers = sum(1 for name in self.trash if name.startswith("paper"))
        return papers, len(self.trash) - papers

    def object_labels(self) -> list[str]:
        labels = []
        if self.books:
            labels.append(f"{len(self.books)} books" if len(self.books) > 1 else "1 book")
        labels += [f"a {DISPLAY_LABELS[name]}" for name in self.display]
        if self.large == ("crate",):
            labels.append("a storage crate")
        elif len(self.large) == 1:
            labels.append("a storage box")
        elif self.large:
            labels.append(f"{len(self.large)} storage boxes of different sizes")
        if self.trash:
            papers, cans = self.trash_counts()
            parts = []
            if papers:
                parts.append(_plural(papers, "crumpled paper ball"))
            if cans:
                parts.append(_plural(cans, "empty drink can"))
            labels.append(f"{len(self.trash)} pieces of trash ({' and '.join(parts)})")
        return labels

    def instruction(self) -> str:
        sentences = ["Organize the shelf in front of you."]
        if self.large == ("crate",):
            sentences.append(
                "Bottom layer: the storage crate, emptied first, standing upright on the desk under the first board."
            )
            sentences.append("The crate has no handles: hold it by its rim with both arms, or slide it over the desk.")
        elif len(self.large) == 1:
            sentences.append("Bottom layer: the storage box, standing upright on the desk under the first board.")
            sentences.append("The box has no handles or lid features: carry it between both hands.")
        elif self.large:
            sentences.append(
                f"Bottom layer: the {len(self.large)} storage boxes, standing upright side by side on the desk "
                "under the first board."
            )
            sentences.append("The boxes have no handles or lid features: carry each between both hands.")
        if self.books:
            count = f"the {len(self.books)} books" if len(self.books) > 1 else "the book"
            sentences.append(
                f"Middle layer: {count}, standing upright and packed tightly together "
                f"{WALL_PHRASES[self.wall_anchor]}."
            )
        if self.display:
            facing = " The photo frame must face outward." if "frame" in self.display else ""
            sentences.append(
                f"Top layer: the {_join([DISPLAY_LABELS[name] for name in self.display])}, standing upright, "
                f"at least 5 cm apart and 2 cm from the side walls.{facing}"
            )
        if self.trash:
            sentences.append(
                "Trash: the crumpled paper balls and the empty drink cans go into the waste bin standing on the "
                "floor beside the desk's left edge; nothing else goes into the bin."
            )
        sentences.append(f"Objects present: {_join(self.object_labels())}.")
        if self.layout == "offset" and "crate" in self.large:
            sentences.append("The shelf stands on the left half of the desk and the crate on the right half.")
        if self.start_container == "crate":
            if self.crate_books == "jumbled":
                sentences.append(
                    "All objects start jumbled inside the storage crate on the desk, as they fell during the move."
                )
            else:
                sentences.append("All objects start inside the storage crate on the desk.")
        elif self.start_container == "shelf":
            sentences.append("All objects start on the shelf.")
        elif self.row_books:
            scattered = len(self.books) - self.row_books
            piled = ", some on top of each other" if self.stacked_start else ""
            sentences.append(
                f"{self.row_books} books start standing packed together in a row on the desk; the other "
                f"{scattered} books and the remaining objects lie scattered on the desk{piled}."
            )
        else:
            piled = ", some on top of each other" if self.stacked_start else ""
            sentences.append(f"All objects start scattered on the desk{piled}.")
        sentences.append("The task is complete once every object rests released and still in its place.")
        return " ".join(sentences)

    def layers_used(self) -> list[str]:
        used = []
        if self.large:
            used.append("bottom")
        if self.books:
            used.append("middle")
        if self.display:
            used.append("top")
        if self.trash:
            used.append("bin")
        return used

    def record(self) -> dict:
        table = self.slot_table()
        misplaced = [
            {"object": name, "slot": slot, "level": level}
            for (name, _), (slot, level) in zip(self.misplaced, self.misplaced_slots())
        ]
        work = self.workload()
        return {
            "version": VERSION,
            "variant_id": self.id,
            "setting": self.setting,
            "level": f"D{self.level}",
            "name": self.name,
            "order": list(self.order),
            "environment_id": self.gym_id(),
            "play_environment_id": self.gym_id(play=True),
            "start_container": self.start_container,
            "object_set": {
                "books": list(self.books),
                "display": list(self.display),
                "large": list(self.large),
                "trash": list(self.trash),
                "slots": list(table.names()),
            },
            "book_start_mode": self.book_start_mode,
            "crate_books": self.crate_books,
            "wall_anchor": self.wall_anchor,
            "misplaced": misplaced,
            "preshelved_slots": list(self.preshelved_slots()),
            "layout": self.layout,
            "row_books": self.row_books,
            "stacked_start": self.stacked_start,
            "episode_length_s": self.episode_length_s,
            "time_limit_basis": {
                "base_s": TIME_BASE_S,
                "per_object_s": TIME_PER_OBJECT_S,
                "per_two_arm_object_s": TIME_PER_TWO_ARM_OBJECT_S,
                "crate_start_s": TIME_CRATE_START_S,
                **work,
            },
            "layer_rules": dict(LAYER_RULES),
            "instruction": self.instruction(),
            "difficulty_axes": {
                "level": f"D{self.level}",
                "manipulation": list(self.manipulation_demands),
                "scenario": list(self.scenario_demands),
                "object_count": len(table.present_indices()),
                "objects_to_place": work["objects_to_place"],
                "layers_used": self.layers_used(),
                "ordering_dependency": self.start_container == "crate",
                "correction_required": bool(self.misplaced),
                "misplaced_count": len(self.misplaced),
                "hand_over_required": self.layout == "offset" and self.start_container == "crate",
                "trash_disposal": bool(self.trash),
                "stacked_start": self.stacked_start,
                "named_wall": self.wall_anchor != "either",
            },
            "grading_basis": GRADING_BASIS,
            "action_schema": dict(ACTION_SCHEMA),
            "control_sha256": _sha(ACTION_SCHEMA),
            "object_set_sha256": _sha(physical_signature(table, self.geometry())),
        }


def _sha(payload) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def physical_signature(table: SlotTable, layout: geometry.Layout = geometry.DEFAULT_LAYOUT) -> dict:
    """Layout constants and present object specs that define the physical task."""
    return {
        "layout": layout.name,
        "table_top": geometry.TABLE_TOP,
        "table_bounds": layout.table_bounds,
        "robot_bases": geometry.ROBOT_BASES,
        "robot_base_height": geometry.ROBOT_BASE_HEIGHT,
        "shelf_pos": layout.shelf_pos,
        "shelf_floors": layout.floors,
        "shelf_openings": layout.openings,
        "shelf_inner": (layout.shelf_inner_width, layout.shelf_inner_depth),
        "blockers": layout.blockers,
        "bin": (layout.bin_pos, geometry.BIN_INNER) if table.trash else None,
        "objects": [
            {
                "name": cls.name,
                "category": cls.category,
                "sizes": cls.sizes,
                "mass": cls.mass,
                "parts": cls.parts,
                "usd": cls.usd,
                "scale": cls.scale,
            }
            for cls in table.present_classes()
        ],
    }


# ---------------------------------------------------------------------------
# Demand labels (defined in env/organize_bookshelf/DIFFICULTY.md)
# ---------------------------------------------------------------------------
_PICK = ("pinch_grasp", "shelf_insertion", "row_packing")
_DESK = ("flat_book_regrasp", "topple_or_pull_from_packed_row", "unstack_piles")
_DISPLAY = ("spaced_placement", "frame_orientation", "occluded_grasp_feature", "high_shelf_reach")
_CRATE = ("pinch_from_crate", "bimanual_rim_carry", "hand_over_between_arms", "low_shelf_reach")
_PILE = ("clear_obstructing_objects",)
_BOOKS = ("book_m",) * 3 + ("book_xs", "book_s", "book_l", "book_x", "book_w")  # D3 desk books
_BOOKS_TEN = ("book_m",) * 5 + ("book_xs", "book_s", "book_l", "book_x", "book_w")
_CRATE_BOOKS = ("book_xs", "book_s", "book_m", "book_l", "book_x")
_TRASH = ("paper_a", "paper_b", "can_crushed", "can_slim")
_BOXES = ("box_s", "box_l")
L, B, T = geometry.LEVEL_LARGE, geometry.LEVEL_BOOKS, geometry.LEVEL_DISPLAY

VARIANTS = (
    # ---------------------------------------------------------------- books only
    Variant(
        "BooksTable", 1, "Three upright books onto the middle shelf", "table",
        ("book_s", "book_m", "book_l"), (), (), book_start_mode="upright", layout="books",
        manipulation_demands=_PICK, scenario_demands=("single_layer_rule",),
    ),
    Variant(
        "BooksTable", 2, "Five books, some lying flat", "table",
        ("book_xs", "book_s", "book_m", "book_l", "book_x"), (), (), layout="books",
        manipulation_demands=_PICK + ("flat_book_regrasp",), scenario_demands=("single_layer_rule",),
    ),
    Variant(
        "BooksTable", 3, "Books onto the middle shelf", "table",
        _BOOKS, (), (), layout="books", row_books=3, stacked_start=True,
        manipulation_demands=_PICK + _DESK, scenario_demands=("single_layer_rule",),
    ),
    Variant(
        "BooksTable", 4, "Ten books against a named wall", "table",
        _BOOKS_TEN, (), (), layout="books", row_books=5, stacked_start=True, wall_anchor="negative_y",
        manipulation_demands=_PICK + _DESK, scenario_demands=("single_layer_rule", "named_wall_anchor"),
    ),
    # ---------------------------------------------------------------- full hutch from the desk
    Variant(
        "ShelfTable", 1, "Books, a trophy and one box", "table",
        ("book_s", "book_m", "book_l", "book_x"), ("trophy",), ("box_s",), book_start_mode="upright",
        manipulation_demands=_PICK + ("high_shelf_reach", "low_shelf_reach", "bimanual_squeeze_carry"),
        scenario_demands=("layer_rules", "object_classification"),
    ),
    Variant(
        "ShelfTable", 2, "Books, three display objects and two boxes", "table",
        ("book_m",) * 3 + ("book_s", "book_l", "book_x"), ("trophy", "frame", "lamp"), _BOXES, row_books=3,
        manipulation_demands=_PICK
        + ("flat_book_regrasp", "topple_or_pull_from_packed_row")
        + _DISPLAY
        + ("low_shelf_reach", "bimanual_squeeze_carry"),
        scenario_demands=("layer_rules", "object_classification"),
    ),
    Variant(
        "ShelfTable", 3, "Organize a full desk hutch from the desk", "table",
        _BOOKS, ("trophy", "frame", "lamp"), _BOXES, row_books=3, stacked_start=True,
        manipulation_demands=_PICK + _DESK + _DISPLAY + ("low_shelf_reach", "bimanual_squeeze_carry"),
        scenario_demands=("layer_rules", "object_classification"),
    ),
    Variant(
        "ShelfTable", 4, "A crowded desk with flat books and awkward display objects", "table",
        _BOOKS_TEN, ("frame", "lamp", "globe"), _BOXES, book_start_mode="flat", row_books=5, stacked_start=True,
        manipulation_demands=_PICK + _DESK + _DISPLAY + ("low_shelf_reach", "bimanual_squeeze_carry"),
        scenario_demands=("layer_rules", "object_classification"),
    ),
    # ---------------------------------------------------------------- unpack a moving crate
    Variant(
        "ShelfCrate", 1, "Unpack a neatly packed crate", "crate",
        ("book_s", "book_m"), ("trophy",), ("crate",), crate_books="packed", layout="offset",
        manipulation_demands=_PICK + ("high_shelf_reach",) + _CRATE,
        scenario_demands=("layer_rules", "object_classification", "ordering_crate_before_shelf"),
    ),
    Variant(
        "ShelfCrate", 2, "Unpack a small jumbled crate", "crate",
        ("book_s", "book_m", "book_l"), ("trophy", "frame"), ("crate",), layout="offset",
        manipulation_demands=_PICK
        + ("flat_book_regrasp", "spaced_placement", "frame_orientation", "high_shelf_reach")
        + _CRATE
        + _PILE,
        scenario_demands=("layer_rules", "object_classification", "ordering_crate_before_shelf", "random_pile_planning"),
    ),
    Variant(
        "ShelfCrate", 3, "Unpack a jumbled moving crate onto the hutch", "crate",
        _CRATE_BOOKS, ("plant", "frame", "globe"), ("crate",), layout="offset",
        manipulation_demands=_PICK + ("flat_book_regrasp",) + _DISPLAY + _CRATE + _PILE,
        scenario_demands=("layer_rules", "object_classification", "ordering_crate_before_shelf", "random_pile_planning"),
    ),
    Variant(
        "ShelfCrate", 4, "Unpack a full crate against a named wall", "crate",
        ("book_xs", "book_s", "book_m", "book_m", "book_l", "book_x", "book_w"),
        ("plant", "frame", "globe"),
        ("crate",),
        layout="offset",
        wall_anchor="positive_y",
        manipulation_demands=_PICK + ("flat_book_regrasp",) + _DISPLAY + _CRATE + _PILE,
        scenario_demands=(
            "layer_rules",
            "object_classification",
            "ordering_crate_before_shelf",
            "random_pile_planning",
            "named_wall_anchor",
        ),
    ),
    # ---------------------------------------------------------------- correct misplaced objects
    Variant(
        "ShelfCrateFix", 1, "One book on the wrong layer of a tidy shelf", "shelf",
        ("book_s", "book_m", "book_l", "book_x"), ("trophy", "frame"), (), misplaced=(("book_m", T),),
        layout="offset",
        manipulation_demands=_PICK + ("high_shelf_reach",),
        scenario_demands=("layer_rules", "object_classification", "misplaced_object_correction"),
    ),
    Variant(
        "ShelfCrateFix", 2, "Unpack a packed crate and correct a misplaced globe", "crate",
        ("book_s", "book_m", "book_l"), ("plant", "globe"), ("crate",), crate_books="packed",
        misplaced=(("globe", B),), layout="offset",
        manipulation_demands=_PICK + ("spaced_placement", "occluded_grasp_feature", "high_shelf_reach") + _CRATE,
        scenario_demands=(
            "layer_rules",
            "object_classification",
            "ordering_crate_before_shelf",
            "misplaced_object_correction",
        ),
    ),
    Variant(
        "ShelfCrateFix", 3, "Unpack the crate and correct a misplaced globe", "crate",
        _CRATE_BOOKS, ("plant", "frame", "globe"), ("crate",), misplaced=(("globe", B),), layout="offset",
        manipulation_demands=_PICK + ("flat_book_regrasp",) + _DISPLAY + _CRATE + _PILE,
        scenario_demands=(
            "layer_rules",
            "object_classification",
            "ordering_crate_before_shelf",
            "random_pile_planning",
            "misplaced_object_correction",
        ),
    ),
    Variant(
        "ShelfCrateFix", 4, "Unpack the crate and correct two misplaced objects", "crate",
        _CRATE_BOOKS, ("plant", "frame", "globe"), ("crate",), misplaced=(("globe", B), ("book_l", T)),
        layout="offset",
        manipulation_demands=_PICK + ("flat_book_regrasp",) + _DISPLAY + _CRATE + _PILE,
        scenario_demands=(
            "layer_rules",
            "object_classification",
            "ordering_crate_before_shelf",
            "random_pile_planning",
            "misplaced_object_correction",
            "multiple_misplaced_objects",
        ),
    ),
    # ---------------------------------------------------------------- organize and throw the trash away
    Variant(
        "TableClean", 1, "Three books and two pieces of trash", "table",
        ("book_s", "book_m", "book_l"), (), (), book_start_mode="upright", trash=("paper_a", "can_slim"),
        manipulation_demands=_PICK + ("drop_into_bin", "irregular_object_grasp"),
        scenario_demands=("single_layer_rule", "trash_disposal", "distractor_objects"),
    ),
    Variant(
        "TableClean", 2, "Books, display objects and four pieces of trash", "table",
        ("book_s", "book_m", "book_l", "book_x"), ("trophy", "frame"), (), trash=_TRASH,
        manipulation_demands=_PICK
        + ("flat_book_regrasp", "spaced_placement", "frame_orientation", "high_shelf_reach")
        + ("drop_into_bin", "irregular_object_grasp"),
        scenario_demands=("layer_rules", "object_classification", "trash_disposal", "distractor_objects"),
    ),
    Variant(
        "TableClean", 3, "Organize the hutch and throw the trash away", "table",
        _BOOKS[:7], ("trophy", "frame", "lamp"), _BOXES, row_books=3, stacked_start=True, trash=_TRASH,
        manipulation_demands=_PICK
        + _DESK
        + _DISPLAY
        + ("low_shelf_reach", "bimanual_squeeze_carry", "drop_into_bin", "irregular_object_grasp"),
        scenario_demands=("layer_rules", "object_classification", "trash_disposal", "distractor_objects"),
    ),
    Variant(
        "TableClean", 4, "Organize the hutch with trash already hidden on it", "table",
        _BOOKS[:7], ("trophy", "frame", "lamp"), _BOXES, row_books=3, stacked_start=True, trash=_TRASH,
        misplaced=(("paper_b", B), ("can_crushed", T)),
        manipulation_demands=_PICK
        + _DESK
        + _DISPLAY
        + ("low_shelf_reach", "bimanual_squeeze_carry", "drop_into_bin", "irregular_object_grasp"),
        scenario_demands=(
            "layer_rules",
            "object_classification",
            "trash_disposal",
            "distractor_objects",
            "misplaced_object_correction",
            "multiple_misplaced_objects",
        ),
    ),
)  # fmt: skip
BY_ID = {variant.id: variant for variant in VARIANTS}
# The five original variants are the D3 levels; their names stay valid as aliases.
ALIASES = {setting: f"{setting}D3" for setting in SETTINGS}
BY_ID.update({alias: BY_ID[target] for alias, target in ALIASES.items()})


def levels(setting: str) -> tuple[Variant, ...]:
    """The four levels of one setting, D1 to D4."""
    return tuple(variant for variant in VARIANTS if variant.setting == setting)


def alias_gym_id(alias: str, play: bool = False) -> str:
    return f"{GYM_PREFIX}-{alias}{'-Play' if play else ''}-v0"


def alias_cfg_class(alias: str, play: bool = False) -> str:
    return f"OrganizeBookshelf{alias}EnvCfg{'_PLAY' if play else ''}"
