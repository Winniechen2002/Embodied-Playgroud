"""Trusted robot definitions for both simulator execution and offline evidence."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import runpy
from typing import Sequence


# Importing agentbench's package registers simulator tasks. Load just the shared
# data module, as the existing standalone Rubik tools do for their pure modules.
_NAMES = runpy.run_path(str(Path(__file__).resolve().parents[5] / "sharpa_joint_names.py"))


@dataclass(frozen=True)
class EmbodimentSpec:
    name: str
    task_id: str
    palm_body_name: str
    motion_joint_names: tuple[str, ...]
    finger_joint_names: tuple[str, ...]
    contact_body_names: tuple[str, ...]
    joint_units: tuple[str, ...]
    action_dim: int

    @property
    def joint_names(self) -> tuple[str, ...]:
        return self.motion_joint_names + self.finger_joint_names


_SPECS = {
    "franka-panda": EmbodimentSpec(
        name="franka-panda", task_id="Agentbench-RubiksCube-FrankaPanda-Play-v0",
        palm_body_name="panda_hand",
        motion_joint_names=tuple(f"panda_joint{i}" for i in range(1, 8)),
        finger_joint_names=("panda_finger_joint1", "panda_finger_joint2"),
        contact_body_names=("panda_leftfinger", "panda_rightfinger"),
        joint_units=("rad",) * 7 + ("m",) * 2, action_dim=8,
    ),
    "floating-sharpa-right": EmbodimentSpec(
        name="floating-sharpa-right", task_id="Agentbench-RubiksCube-FloatingSharpaRight-Play-v0",
        palm_body_name=_NAMES["SHARPA_PALM_BODY_NAME"],
        motion_joint_names=tuple(_NAMES["SHARPA_MOTION_JOINT_NAMES"]),
        finger_joint_names=tuple(_NAMES["SHARPA_FINGER_JOINT_NAMES"]),
        contact_body_names=tuple(_NAMES["SHARPA_CONTACT_BODY_NAMES"]),
        joint_units=("m",) * 3 + ("rad",) * 25, action_dim=28,
    ),
}


def get_embodiment(name: str) -> EmbodimentSpec:
    if not isinstance(name, str) or name not in _SPECS:
        raise ValueError(f"unknown embodiment: {name!r}")
    return _SPECS[name]


def _unique_names(values: Sequence[str], label: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{label} must be a sequence of names")
    names = tuple(values)
    if not names or not all(isinstance(name, str) and name for name in names):
        raise ValueError(f"{label} must contain nonempty names")
    if len(set(names)) != len(names):
        raise ValueError(f"{label} contains duplicate names")
    return names


def validate_robot_mapping(
    spec: EmbodimentSpec, *, joint_names: Sequence[str], body_names: Sequence[str],
) -> dict[str, object]:
    """Resolve ordered command/evidence indices from one actual articulation."""
    if not isinstance(spec, EmbodimentSpec) or get_embodiment(spec.name) != spec:
        raise ValueError("robot mapping requires a trusted embodiment definition")
    joints = _unique_names(joint_names, "joint_names")
    bodies = _unique_names(body_names, "body_names")
    missing = set(spec.joint_names) - set(joints)
    extra = set(joints) - set(spec.joint_names)
    if missing or extra:
        raise ValueError(f"robot joint mapping mismatch: missing={sorted(missing)}, extra={sorted(extra)}")
    missing_bodies = {spec.palm_body_name, *spec.contact_body_names} - set(bodies)
    if missing_bodies:
        raise ValueError(f"robot body mapping missing: {sorted(missing_bodies)}")
    return {
        "motion_joint_ids": tuple(joints.index(name) for name in spec.motion_joint_names),
        "finger_joint_ids": tuple(joints.index(name) for name in spec.finger_joint_names),
        "contact_body_ids": tuple(bodies.index(name) for name in spec.contact_body_names),
        "palm_body_id": bodies.index(spec.palm_body_name),
    }
