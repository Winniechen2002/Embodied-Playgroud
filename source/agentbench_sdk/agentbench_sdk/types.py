"""Documentation types for v1 JSON contracts; client methods return dictionaries."""
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ActionSpec:
    size: int
    low: list[float | None]
    high: list[float | None]
    names: list[str] = field(default_factory=list)
    semantics: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class TaskSpec:
    task: dict[str, Any]
    action_spec: dict[str, Any]
    robots: dict[str, Any] = field(default_factory=dict)
    cameras: dict[str, Any] = field(default_factory=dict)
    goal: dict[str, Any] = field(default_factory=dict)
    version: int = 1

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Observation:
    step_index: int
    simulation_time_s: float
    robots: dict[str, Any]
    cameras: dict[str, Any]
    terminated: bool
    truncated: bool
    privileged: dict[str, Any] | None = None

    def to_dict(self) -> dict:
        result = asdict(self)
        if self.privileged is None:
            del result['privileged']
        return result


@dataclass(frozen=True)
class EpisodeResult:
    success: bool
    score: float
    step_count: int
    terminated: bool
    truncated: bool
    version: int = 1

    def to_dict(self) -> dict:
        return asdict(self)
