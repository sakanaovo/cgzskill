"""Static documentation contracts, not an agent/runtime concurrency test.

These tests parse templates and guard explicit safety instructions. They do not
execute initialization, generate identities, archive a session, or merge Git.
"""

import json
import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
INIT = "skills/cgz-init"
ARCHIVE = "skills/cgz-archive-session"
DAILY = "skills/cgz-daily-recap"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def record_schema(path):
    for block in re.findall(r"```yaml\n(.*?)\n```", read(path), re.DOTALL):
        # The example is Markdown frontmatter, not a multi-document YAML stream.
        lines = block.splitlines()
        if lines and lines[0] == "---" and lines[-1] == "---":
            block = "\n".join(lines[1:-1])
        parsed = yaml.safe_load(block)
        if isinstance(parsed, dict) and "record_id" in parsed:
            return parsed
    raise AssertionError(f"No YAML record schema in {path}")


class TeamContractTests(unittest.TestCase):
    def test_identity_template_is_json_with_only_local_identity_fields(self):
        data = json.loads(read(f"{INIT}/assets/local.json.template"))
        self.assertEqual(set(data), {"author_alias", "author_id", "document_language"})
        self.assertEqual(data["document_language"], "{{DOCUMENT_LANGUAGE}}")
        self.assertEqual(data["author_alias"], "{{AUTHOR_ALIAS}}")
        self.assertEqual(data["author_id"], "{{AUTHOR_ID}}")

    def test_init_confirms_alias_and_does_not_collect_email(self):
        text = read(f"{INIT}/SKILL.md") + read(f"{INIT}/references/init-spec.md")
        for requirement in ("确认作者别名", "git user.name", "只作候选", "不取邮箱", "不采集邮箱"):
            self.assertIn(requirement, text)
        self.assertIn("JSON 序列化", text)
        self.assertIn("禁止用日期、别名、邮箱或主机名推导", text)

    def test_init_ignores_only_the_exact_identity_path(self):
        text = read(f"{INIT}/references/init-spec.md")
        self.assertIn("`/.cgz/local.json`", text)
        self.assertIn("禁止忽略整个 `.cgz/`、`docs/`", text)
        self.assertIn("已被跟踪的身份文件", text)
        self.assertIn("不得自动 `git rm`、重写历史", text)

    def test_init_preserves_identity_and_rerun_is_noop(self):
        text = read(f"{INIT}/SKILL.md") + read(f"{INIT}/references/init-spec.md")
        for requirement in ("已有有效身份直接保留", "不写文件、不换 ID", "排他创建", "重新读取并保留", "无 Git", "worktree"):
            self.assertIn(requirement, text)
        self.assertIn("不修改 `git config`", text)

    def test_record_metadata_matches_across_shared_and_standalone_contracts(self):
        expected = {
            "record_id", "author_id", "author_alias", "document_language", "date", "recorded_at",
            "scope", "verification", "branch", "base_commit", "source_ids", "supersedes",
        }
        for path in (
            f"{INIT}/assets/cgz-memory.md.template",
            f"{ARCHIVE}/references/archive-spec.md",
            f"{DAILY}/references/recap-spec.md",
        ):
            with self.subTest(path=path):
                schema = record_schema(path)
                self.assertEqual(set(schema), expected)
                self.assertEqual(schema["source_ids"], [])
                self.assertEqual(schema["supersedes"], [])
                self.assertEqual(schema["verification"], "unverified")
                self.assertIsNone(schema["branch"])
                self.assertIsNone(schema["base_commit"])

    def test_records_are_unique_and_immutable_by_contract(self):
        for path in (
            f"{INIT}/assets/cgz-memory.md.template",
            f"{ARCHIVE}/references/archive-spec.md",
            f"{DAILY}/references/recap-spec.md",
        ):
            with self.subTest(path=path):
                text = read(path)
                for requirement in ("UUID", "YYYY-MM-DD-<record_id>.md", "禁止覆盖", "supersedes"):
                    self.assertIn(requirement, text)
                self.assertRegex(text, r"原始记录不可(?:修改或删除|改写或去重删除)")
        for directory in ("archives", "lessons", "daily"):
            self.assertIn(
                f"docs/{directory}/YYYY-MM-DD-<record_id>.md",
                read(f"{INIT}/assets/cgz-memory.md.template"),
            )

    def test_all_skill_contracts_preserve_scope_pending_and_sources(self):
        paths = (
            f"{INIT}/assets/cgz-memory.md.template",  # init installs this protocol
            f"{ARCHIVE}/references/archive-spec.md",
            f"{DAILY}/references/recap-spec.md",
            "skills/cgz-focused-reading/references/reading-spec.md",
            "skills/cgz-focused-discussion/references/discussion-discipline.md",
        )
        self.assertIn("assets/cgz-memory.md.template", read(f"{INIT}/references/init-spec.md"))
        for path in paths:
            with self.subTest(path=path):
                text = read(path)
                for requirement in ("同义且同范围", "互补", "pending", "来源", "范围", "原始记录"):
                    self.assertIn(requirement, text)

    def test_daily_does_not_recursively_summarize_or_repeat_identical_sources(self):
        text = read(f"{DAILY}/references/recap-spec.md")
        for requirement in (
            "不把 `docs/daily/` 的旧摘要递归当作新来源",
            "先按来源 `record_id` 去重",
            "同一作者、同一目标日期、同一范围、同一来源集合",
            "复用已有摘要路径，不重复创建或计数",
            "来源集合变化或有新会话事实时新建摘要",
        ):
            self.assertIn(requirement, text)

    def test_daily_has_no_mutable_shared_day_instructions(self):
        entry = read(f"{DAILY}/SKILL.md")
        spec = read(f"{DAILY}/references/recap-spec.md")
        self.assertNotIn("每天一份", entry)
        self.assertNotIn("覆盖 / 追加 / 取消", spec)
        self.assertIn("同源复用 / 新建更正 / 取消", spec)

    def test_superseding_requires_adoption_evidence(self):
        for path in (
            f"{INIT}/assets/cgz-memory.md.template",
            f"{ARCHIVE}/references/archive-spec.md",
            f"{DAILY}/references/recap-spec.md",
        ):
            with self.subTest(path=path):
                text = read(path)
                self.assertIn("不代表规则已获采纳", text)
                self.assertIn("采纳证据", text)
                self.assertIn("不证明分支已合入", text)

    def test_no_shared_auto_append_in_active_templates(self):
        protocol = read(f"{INIT}/assets/cgz-memory.md.template")
        self.assertIn("不得自动改写 `AGENTS.md`、`ai-lessons.md`、业务规范或共享索引", protocol)
        self.assertIn("明确批准或团队正常 PR 审阅", protocol)
        for path in (f"{ARCHIVE}/references/archive-spec.md", f"{DAILY}/references/recap-spec.md"):
            self.assertIn("禁止每次记录都追加共享索引", read(path))
        lesson = read(f"{INIT}/assets/ai-lessons.md.template")
        self.assertIn("不得每次自动在本文件顶部插入日志", lesson)
        self.assertIn("Proposed Rule", lesson)

    def test_manual_acceptance_is_explicitly_unrun(self):
        text = read("docs/team-acceptance.md")
        self.assertIn("尚未执行", text)
        self.assertIn("不是运行时验收", text)
        self.assertIn("两个作者", text)
        self.assertIn("同一作者", text)
        self.assertIn("无 Git", text)
        self.assertIn("worktree", text)


if __name__ == "__main__":
    unittest.main()
