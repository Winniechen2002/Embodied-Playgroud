"""Regression checks for the capability-documentation validator's boundaries."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_tool_policy_docs import (
    LANGUAGE_SUFFIXES,
    LEVEL_PROFILES,
    REQUIRED_DOCS,
    RULE_NAMES,
    SCENARIOS,
    check_policy,
    edition,
)


class ToolPolicyDocsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        texts = {name: f"# {name}\n" for name in RULE_NAMES}
        for filename, required_text in SCENARIOS.values():
            texts[filename] += f"\n{required_text}\n"
        texts["rules.md"] += "\nThe agent must not use online search.\n\n"
        texts["rules.md"] += "| Level | Capability | Profile |\n| --- | --- | --- |\n"
        for level, profile in LEVEL_PROFILES.items():
            texts["rules.md"] += f"| {level} | Capability | [Profile]({profile}) |\n"
        texts["rules.md"] += "\n| Minimum level | Tools |\n| --- | --- |\n"
        for tool, relative in REQUIRED_DOCS.items():
            texts["rules.md"] += f"| 1 | [{tool}]({relative}) |\n"
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {tool}\n", encoding="utf-8")
        for name, text in texts.items():
            for suffix in LANGUAGE_SUFFIXES:
                (self.root / edition(name, suffix)).write_text(text, encoding="utf-8")

    def append(self, name: str, text: str) -> None:
        with (self.root / name).open("a", encoding="utf-8") as stream:
            stream.write(f"\n{text}\n")

    def replace(self, name: str, before: str, after: str) -> None:
        path = self.root / name
        text = path.read_text(encoding="utf-8")
        self.assertIn(before, text)
        path.write_text(text.replace(before, after), encoding="utf-8")

    def test_valid_contract(self) -> None:
        self.assertEqual(check_policy(self.root), [])

    def test_default_page_can_link_to_english_editions(self) -> None:
        self.replace("rules.md", "[Profile](rules_model_only.md)", "[Profile](rules_model_only.en.md)")
        self.replace("rules.md", "(docs/tools/stream3d/README.md)", "(docs/tools/stream3d/README.en.md)")
        original = self.root / "docs/tools/stream3d/README.md"
        original.with_name("README.en.md").write_text(original.read_text(), encoding="utf-8")
        self.assertEqual(check_policy(self.root), [])

    def test_missing_model_only_profile_reports_error_without_crashing(self) -> None:
        (self.root / "rules_model_only.md").unlink()
        self.assertTrue(any("missing level/shared rule document: rules_model_only.md" in error
                            for error in check_policy(self.root)))

    def test_new_profile_link_must_point_to_the_model_only_document(self) -> None:
        self.replace("rules.md", "[Profile](rules_model_only.md)", "[Profile](Vision_rules.md)")
        self.assertIn("rules.md does not link Level 0 to rules_model_only.md", check_policy(self.root))

    def test_level_zero_cannot_disappear_from_the_contract(self) -> None:
        self.replace("rules.md", "| Level 0 |", "| Level 4 |")
        self.assertTrue(any("must define exactly Level 0" in error for error in check_policy(self.root)))

    def test_tool_allowlist_cannot_grant_tools_at_level_zero(self) -> None:
        self.replace("rules.md", "| 1 | [Stream3D]", "| 0 | [Stream3D]")
        self.assertIn("tool allowlist grants unsupported minimum level: 0 in rules.md", check_policy(self.root))

    def test_translated_profile_table_must_match_the_current_levels(self) -> None:
        self.replace("rules.zh-CN.md", "| Level 0 |", "| Level 2 |")
        self.assertTrue(any("rules.zh-CN.md must define exactly Level 0" in error
                            for error in check_policy(self.root)))

    def test_translated_rule_links_are_checked(self) -> None:
        self.append("rules.zh-CN.md", "[模型直控](missing_model_only.zh-CN.md)")
        self.assertTrue(any("broken local link in rules.zh-CN.md" in error
                            for error in check_policy(self.root)))

    def test_translations_cannot_retain_the_removed_capability_level(self) -> None:
        self.append("rules_grasp.zh-CN.md", "L4")
        self.assertIn("retired capability level remains in rules_grasp.zh-CN.md", check_policy(self.root))

    def test_retired_profile_is_rejected_even_without_links(self) -> None:
        (self.root / "rules_policy.en.md").write_text("# Old profile\n", encoding="utf-8")
        self.assertIn("retired capability profile still exists: rules_policy.en.md", check_policy(self.root))

    def test_curriculum_levels_and_mathematical_l0_are_out_of_scope(self) -> None:
        (self.root / "curriculum.md").write_text("# Bird curriculum Level 4\n", encoding="utf-8")
        self.append("Vision_rules.md", "Use the l0 notation for this mathematical variable.")
        self.assertEqual(check_policy(self.root), [])


if __name__ == "__main__":
    unittest.main()
