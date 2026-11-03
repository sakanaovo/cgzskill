"""Regression tests for local validation and version-management tooling."""

import argparse
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_script(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_script("validate_skills", ".github/scripts/validate_skills.py")
bump = load_script("bump", "scripts/bump.py")


class FrontmatterTests(unittest.TestCase):
    def test_description_can_contain_triple_hyphens(self):
        for description in ('"before --- after"', 'before --- after'):
            with self.subTest(description=description):
                parsed = validator.parse_frontmatter(
                    f"---\nname: example\ndescription: {description}\n---\nBody\n"
                )
                self.assertIsNotNone(parsed)
                self.assertEqual(parsed[0]["description"], "before --- after")
                self.assertEqual(parsed[1], "\nBody\n")

    def test_inline_hyphens_are_not_a_closing_delimiter(self):
        self.assertIsNone(validator.parse_frontmatter(
            "---\nname: example\ndescription: before --- after\n"
        ))

    def test_opening_delimiter_must_occupy_its_own_line(self):
        self.assertIsNone(validator.parse_frontmatter(
            "---name: example\ndescription: example\n---\nBody\n"
        ))

    def test_crlf_and_body_horizontal_rule_are_preserved(self):
        parsed = validator.parse_frontmatter(
            "---\r\nname: example\r\ndescription: example\r\n---\r\nBody\r\n---\r\n"
        )
        self.assertEqual(parsed, (
            {"name": "example", "description": "example"},
            "\r\nBody\r\n---\r\n",
        ))

    def test_malformed_yaml_and_non_mapping_are_rejected(self):
        for header in ("name: [", "- example"):
            with self.subTest(header=header):
                self.assertIsNone(validator.parse_frontmatter(f"---\n{header}\n---\n"))


class BumpTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.marketplace = root / "marketplace.json"
        self.changelog = root / "CHANGELOG.md"
        self.marketplace.write_text(json.dumps({
            "metadata": {"version": "1.2.0"},
            "plugins": [{"name": "example", "version": "1.0.0"}],
        }) + "\n", encoding="utf-8")
        for name, path in (("MARKETPLACE", self.marketplace), ("CHANGELOG", self.changelog)):
            patcher = patch.object(bump, name, path)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.args = argparse.Namespace(plugin="example", kind="patch", note="Fix example")

    def test_missing_unreleased_heading_does_not_modify_either_file(self):
        self.changelog.write_text("# Changelog\n\n## [1.2.0]\n", encoding="utf-8")
        before = (self.marketplace.read_bytes(), self.changelog.read_bytes())
        with self.assertRaisesRegex(SystemExit, "missing.*Unreleased"):
            bump.cmd_bump(self.args)
        self.assertEqual((self.marketplace.read_bytes(), self.changelog.read_bytes()), before)

    def test_successful_bump_updates_both_documents(self):
        self.changelog.write_text(
            "# Changelog\n\n## [Unreleased]\n\n---\n\n## [1.2.0]\n", encoding="utf-8"
        )
        with contextlib.redirect_stdout(io.StringIO()):
            bump.cmd_bump(self.args)
        data = json.loads(self.marketplace.read_text(encoding="utf-8"))
        self.assertEqual(data["plugins"][0]["version"], "1.0.1")
        self.assertEqual(data["metadata"]["version"], "1.2.1")
        entries = bump.parse_unreleased_bullets(self.changelog.read_text(encoding="utf-8"))
        self.assertEqual(entries, [{
            "plugin": "example", "old": "1.0.0", "new": "1.0.1",
            "kind": "patch", "note": "Fix example",
        }])


class DailyRecapContractTests(unittest.TestCase):
    def test_output_path_is_consistent(self):
        paths = (
            "skills/cgz-daily-recap/SKILL.md",
            "skills/cgz-daily-recap/references/recap-spec.md",
            "skills/cgz-daily-recap/agents/openai.yaml",
            "skills/cgz-init/SKILL.md",
            "skills/cgz-init/assets/AGENTS.md.template",
            "README.md",
            "docs/ai-self-evolution-architecture.md",
            ".claude-plugin/marketplace.json",
        )
        for path in paths:
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("docs/daily/YYYY-MM-DD-<record_id>.md", text)
                self.assertNotIn("${obsidian_vault}", text)
                self.assertNotIn("{{OBSIDIAN_VAULT}}", text)

    def test_init_template_has_no_external_app_configuration(self):
        text = (ROOT / "skills/cgz-init/assets/AGENTS.md.template").read_text(encoding="utf-8")
        self.assertNotIn("obsidian", text.lower())
        self.assertNotIn("vault", text.lower())

    def test_daily_recap_uses_target_date_consistently(self):
        for path in (
            "skills/cgz-daily-recap/SKILL.md",
            "skills/cgz-daily-recap/references/recap-spec.md",
        ):
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("目标复盘日期", text)
                self.assertIn("默认今天", text)
                self.assertNotIn("文件名含今天日期", text)
                self.assertNotIn("不在当天日期的归档", text)

    def test_daily_recap_respects_project_archive_routing(self):
        for path in (
            "skills/cgz-daily-recap/SKILL.md",
            "skills/cgz-daily-recap/references/recap-spec.md",
        ):
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("归档目录、索引或单文件", text)
                self.assertIn("无资料", text)
                self.assertIn("全盘搜索", text)
                self.assertNotIn("禁止读 archives 之外", text)

    def test_readme_does_not_install_only_the_entry_file(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("cat skills/cgz-focused-discussion/SKILL.md >>", text)
        self.assertIn("保留完整 skill 目录", text)

    def test_daily_recap_uses_plain_markdown(self):
        for path in (
            "skills/cgz-daily-recap/SKILL.md",
            "skills/cgz-daily-recap/references/recap-spec.md",
        ):
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                self.assertNotIn("[[", text)
                self.assertIn("../ai-lessons.md", text)


if __name__ == "__main__":
    unittest.main()
