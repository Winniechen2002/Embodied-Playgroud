#!/usr/bin/env python3
"""Check the allowlist documentation and Level 0-3 capability contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULE_NAMES = (
    "rules.md",
    "rules_model_only.md",
    "Vision_rules.md",
    "rules_grasp.md",
    "rules_privileged.md",
)
LEVEL_PROFILES = {
    "Level 0": "rules_model_only.md",
    "Level 1": "Vision_rules.md",
    "Level 2": "rules_grasp.md",
    "Level 3": "rules_privileged.md",
}
REQUIRED_DOCS = {
    "Stream3D": "docs/tools/stream3d/README.md",
    "SAM 3D Objects": "docs/tools/sam-3d-objects/README.md",
    "RSL-RL": "docs/tools/rsl-rl/README.md",
    "Optuna": "docs/tools/optuna/README.md",
}
SCENARIOS = {
    "Level 0 permits code with basic dependencies": (
        "rules_model_only.md",
        "Level 0 permits Python code, the standard library, NumPy and Pillow.",
    ),
    "Level 0 grants no gateway tools": (
        "rules_model_only.md",
        "Level 0 has no gateway tool grants.",
    ),
    "proxy state/contact/reward is allowed": (
        "Vision_rules.md",
        "complete proxy object state, contacts, dynamics, and a custom proxy reward",
    ),
    "original hidden state/evaluator reward is rejected": (
        "Vision_rules.md",
        "hidden state, contacts, original reward, evaluator diagnostics",
    ),
    "TRELLIS.2 backend is rejected": (
        "Vision_rules.md",
        "TRELLIS.2 checkpoints, and the TRELLIS runner scripts",
    ),
    "privileged policy observations are removed": (
        "Vision_rules.md",
        "observation adapter that removes all proxy-only state",
    ),
    "same-episode RGB proxy correction is allowed": (
        "Vision_rules.md",
        "Use later legal RGB, proprioception, and the agent's own action history",
    ),
    "extra resets and episodes are not granted": (
        "rules_grasp.md",
        "Extra original-simulator resets or additional episodes are not granted",
    ),
    "Level 1 reconstructs a proxy for RL": (
        "Vision_rules.md",
        "build a new proxy simulation from observations collected in the current evaluation episode",
    ),
    "Level 2 adds pretrained grasp models": (
        "rules_grasp.md",
        "additionally grants pretrained grasp-generation models",
    ),
    "Level 3 reads explicitly exposed privileged fields": (
        "rules_privileged.md",
        "read access to privileged fields explicitly exposed by the selected interface",
    ),
    "Level 3 privileged access remains read-only": (
        "rules_privileged.md",
        "Read Access Is Not Write Access",
    ),
}

LANGUAGE_SUFFIXES = ("", ".en", ".zh-CN")
LOCAL_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
# Only shared capability rules are scanned. Environment curriculum levels and
# unrelated mathematical names such as l0 are outside this contract.
RETIRED_LEVEL = re.compile(
    r"\bL4\b|\bLevels?\s+(?:[0-3]\s*(?:[-–—/,]|and)\s*)?4\b"
    r"|\b4\s*级|等级\s*4",
    re.IGNORECASE,
)


def edition(name: str, suffix: str) -> str:
    return str(Path(name).with_suffix(f"{suffix}.md"))


def check_policy(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    texts: dict[str, str] = {}
    for name in RULE_NAMES:
        for suffix in LANGUAGE_SUFFIXES:
            filename = edition(name, suffix)
            path = root / filename
            if not path.is_file():
                errors.append(f"missing level/shared rule document: {filename}")
                texts[filename] = ""
                continue
            texts[filename] = path.read_text(encoding="utf-8")
            if not texts[filename].strip():
                errors.append(f"empty level/shared rule document: {filename}")

    normalized_texts = {
        filename: " ".join(text.split()) for filename, text in texts.items()
    }
    global_rules = texts["rules.md"]

    for suffix in LANGUAGE_SUFFIXES:
        filename = edition("rules.md", suffix)
        profile_rows = re.findall(
            r"^\|\s*(Level\s+\d+)\s*\|([^\n]+)$", texts[filename], re.MULTILINE
        )
        if sorted(level for level, _ in profile_rows) != sorted(LEVEL_PROFILES):
            errors.append(f"{filename} must define exactly Level 0, Level 1, Level 2, and Level 3")
        for level, relative in LEVEL_PROFILES.items():
            rows = [row for row_level, row in profile_rows if row_level == level]
            # An untranslated compatibility entry or the matching edition is
            # valid. Either must still point to the correct capability profile.
            targets = {edition(relative, language) for language in LANGUAGE_SUFFIXES}
            if not any(targets.intersection(LOCAL_LINK.findall(row)) for row in rows):
                errors.append(f"{filename} does not link {level} to {relative}")

        tool_rows = re.findall(r"^\|\s*(\d+)\s*\|([^\n]+)$", texts[filename], re.MULTILINE)
        for minimum, row in tool_rows:
            if "docs/tools/" in row and minimum not in {"1", "2"}:
                errors.append(f"tool allowlist grants unsupported minimum level: {minimum} in {filename}")

    for tool, relative in REQUIRED_DOCS.items():
        doc = root / relative
        targets = {edition(relative, language) for language in LANGUAGE_SUFFIXES}
        if tool not in global_rules or not targets.intersection(LOCAL_LINK.findall(global_rules)):
            errors.append(f"rules.md does not index {tool} at {relative}")
        if not doc.is_file() or not doc.read_text(encoding="utf-8").strip():
            errors.append(f"missing or empty documentation: {relative}")

    for filename, text in texts.items():
        rule_file = root / filename
        for target in LOCAL_LINK.findall(text):
            if "://" in target or target.startswith("#"):
                continue
            relative_target = target.split("#", maxsplit=1)[0]
            if not (rule_file.parent / relative_target).resolve().exists():
                errors.append(f"broken local link in {rule_file.name}: {target}")
        if RETIRED_LEVEL.search(text):
            errors.append(f"retired capability level remains in {filename}")

    for label, (filename, required_text) in SCENARIOS.items():
        if required_text not in normalized_texts[filename]:
            errors.append(f"policy scenario not documented: {label}")

    all_rules = "\n".join(texts.values())
    obsolete_rule_names = (
        "rules_" + "kinematics.md",
        "rules_" + "planning.md",
    )
    for forbidden in obsolete_rule_names:
        if forbidden in all_rules:
            errors.append(f"obsolete rule-file reference found: {forbidden}")

    for suffix in LANGUAGE_SUFFIXES:
        retired_name = edition("rules_" + "policy.md", suffix)
        if (root / retired_name).exists():
            errors.append(f"retired capability profile still exists: {retired_name}")
        if retired_name in all_rules:
            errors.append(f"retired capability profile reference found: {retired_name}")

    if not re.search(r"must not use online search", global_rules, re.IGNORECASE):
        errors.append("rules.md no longer prohibits online tool discovery")

    return errors


def main() -> int:
    errors = check_policy()
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        print(f"FAILED: {len(errors)} policy/documentation error(s)", file=sys.stderr)
        return 1
    print(
        f"PASS: {len(LEVEL_PROFILES)} level profiles, {len(REQUIRED_DOCS)} tool "
        f"docs, and {len(SCENARIOS)} policy scenarios"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
