# Changelog

本仓库遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与 [SemVer](https://semver.org/lang/zh-CN/)。

每个 skill 的版本在 `.claude-plugin/marketplace.json` 的 `plugins[].version` 字段；marketplace 整体版本在 `metadata.version`。

---

## [Unreleased]

<!-- 下一版的改动写这里。release 时移到新版本号下，并补 [Unreleased] 空段。 -->

---

## [1.2.0] — 2026-05-20

### Added

- **`daily-recap` skill** —— 按天聚合 `docs/archives/` / `docs/ai-lessons.md` / 当前会话，写一份 Obsidian 友好的 `Daily/YYYY-MM-DD.md`（YAML frontmatter + `[[wikilinks]]`）到 `obsidian_vault`。跟 `archive-session`（单次归档）职责区分：daily-recap 是按天索引。首发 `1.0.0`。

### Tooling

- `scripts/bump.py`：npm 风格版本管理脚本。`bump <plugin> --patch|--minor|--major --note "..."` 改 `marketplace.json` 并追加 CHANGELOG 条目；`--release` 把 `[Unreleased]` 切到新版本段；`--status` 看当前状态。不自动 commit / tag，最后两步必须手动。
- `CONTRIBUTING.md` 的「版本与发布」节重写，全面切换到脚本流程，禁止手改 `marketplace.json` 的 version 字段。
- **cgz-init** `1.0.0 → 1.1.0` (minor) — Ask for obsidian_vault path on init; write to AGENTS.md cgz config block for daily-recap to read

---

## [1.1.0] — 2026-05-20

### Added

- **`cgz-init` skill** —— 在用户项目里扫描记忆体系（`AGENTS.md` / `docs/ai-lessons.md` / `docs/archives/`），缺失则询问后生成。带三份模板 (`assets/AGENTS.md.template` / `assets/ai-lessons.md.template` / `assets/archives-README.md.template`)。首发 `1.0.0`。
- 三个老 skill 的 `references/` 统一改为**五大节骨架**：五原则 / 五维度 / 五心理学 / 对话严苛规则 / 语言纯化规则。
- `CONTRIBUTING.md`：贡献流程、五大节要求、命名合规、commit / PR 规范。
- `CHANGELOG.md`：本文件。
- `.github/PULL_REQUEST_TEMPLATE.md` + `.github/ISSUE_TEMPLATE/{bug_report,skill_request}.md`：PR 与 issue 引导。
- `skills/focused-discussion/agents/openai.yaml`：补齐缺失的 OpenAI 元数据；三个 skill 现在元数据齐整。

### Changed

- **Plugin versions**: `focused-discussion` / `archive-session` / `focused-reading` 从 `1.0.0` 升到 `1.1.0`（references 重写 + 风格统一）。
- **Marketplace metadata.version**: `1.0.0 → 1.1.0`。
- `marketplace.json` 四个 plugin 的描述同步「禁止 / 必须」严苛风格，与 SKILL.md 保持一致。
- `README.md` 仓库结构图、安装命令排版、贡献章节重写；技能表格新增 `cgz-init` 行；补「整体设计」说明。
- `docs/ai-self-evolution-architecture.md`：句式严苛化，明确标注与五大节骨架的关系。

### Notes

- 1.0.0 此前从未打 git tag，1.1.0 是首个真正切版本号的 release。后续严格按 SemVer 走，每次 release 必须 `git tag vX.Y.Z`。

---

## [1.0.0] — 2026-05-19

### Added

- 初版 marketplace 结构 (`.claude-plugin/marketplace.json`)。
- `focused-discussion` skill：对话纪律。
- `focused-reading` skill：阅读纪律。
- `archive-session` skill：会话归档。
- CI：`.github/workflows/validate-skills.yml` + `validate_skills.py` 校验 Agent Skills spec。
- MIT License。
