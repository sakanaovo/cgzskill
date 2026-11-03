# Changelog

本仓库遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与 [SemVer](https://semver.org/lang/zh-CN/)。

每个 skill 的版本在 `.claude-plugin/marketplace.json` 的 `plugins[].version` 字段；marketplace 整体版本在 `metadata.version`。

---

## [Unreleased]

<!-- 下一版的改动写这里。release 时移到新版本号下，并补 [Unreleased] 空段。 -->

---

## [2.1.0] — 2026-11-03

### Added

- 本地 `document_language` 保存中文、英文或其他明确语言选择；新文档支持本次请求、保存偏好、项目约定、首次询问的优先级。
- 共享 `project_document_language` 与个人偏好隔离；旧身份只补语言字段，不重生成 UUID，不翻译不可变历史。
- 新记录保存实际 `document_language`；日报复用要求输出语言相同，不同语言另建摘要并保留相同来源。

### Changed

- 英文 README 成为首页，完整中文说明迁到 `README.zh-CN.md`，`README.en.md` 保留兼容入口。
- 五个 skill 与初始化模板按选定语言输出正文，保留 schema、路径、ID 与来源引用；不宣称任意语言已实测。
- 更新通用 Agent Skills 定位、安装提示词和语言迁移说明；补充语言配置与文档链接契约检查。

### Versions

- **cgz-focused-discussion** `2.0.0 → 2.1.0` (minor) — 支持保存文档语言偏好，区分个人新记录与团队共享语言，保留来源及历史
- **cgz-archive-session** `2.0.0 → 2.1.0` (minor) — 支持保存文档语言偏好，区分个人新记录与团队共享语言，保留来源及历史
- **cgz-focused-reading** `2.0.0 → 2.1.0` (minor) — 支持保存文档语言偏好，区分个人新记录与团队共享语言，保留来源及历史
- **cgz-init** `2.0.0 → 2.1.0` (minor) — 支持保存文档语言偏好，区分个人新记录与团队共享语言，保留来源及历史
- **cgz-daily-recap** `2.0.0 → 2.1.0` (minor) — 支持保存文档语言偏好，区分个人新记录与团队共享语言，保留来源及历史
- **cgz-all** `2.0.0 → 2.1.0` (minor) — 支持保存文档语言偏好，区分个人新记录与团队共享语言，保留来源及历史

---

## [2.0.0] — 2026-11-03

### Changed

- 初始化一次确认作者别名，建立精确忽略的本地身份和共享记忆协议；无 Git 也能使用，旧身份和记录保留。
- 归档、候选教训、复盘改为随机 UUID 独立记录，不再自动追加共享索引或规则；汇总保留来源、同范围矛盾待确认，重复来源不重复计数。
- 团队协议为说明型 skill 执行约束，不声称提供后台监听、同步或自动合并。
- 四个未加前缀的 skill 重命名为 `cgz-*`：`cgz-focused-discussion` / `cgz-archive-session` / `cgz-focused-reading` / `cgz-daily-recap`；同步更新 marketplace plugin name、skill 路径、文档示例和内部引用。
- 五个 `SKILL.md` frontmatter `description` 改为中文触发描述，并同步 `agents/openai.yaml` 展示名与提示语。
- 新增 `cgz-all` bundle plugin，一次安装 5 个 cgz skill，单独安装入口保留。
- 重写中英文 README：功能定位、AI 安装提示词、安装与初始化、团队记录示例、1.x 升级和验证边界。

### Fixed

- 移除核心流程对 Obsidian 的集成要求：初始化不问 vault，日复盘写项目 `docs/daily/YYYY-MM-DD-<record_id>.md`，使用普通 Markdown。
- 旧项目配置保留但不再使用；保留写入确认和不覆盖规则，明确 Obsidian 接入尚未实测。
- 日复盘统一按目标日期筛选和命名，修正补昨天时仍被要求只读今天归档的冲突；沿用项目明确的归档目录、索引或单文件，避免遗漏合法归档。
- 校验脚本只把独立一行的 `---` 识别为 frontmatter 边界，避免误切描述里的连字符。
- 版本脚本先验证并生成变更日志，再写入版本清单，避免缺失 `[Unreleased]` 标题时只更新版本。
- 移除只拼接 `SKILL.md` 到 `AGENTS.md` 的不完整安装示例，要求保留规范和模板引用。
- 为上述边界条件补充回归测试，并接入 CI。

### Versions

- **cgz-focused-discussion** `1.1.0 → 2.0.0` (major) — 采用带范围和来源的团队讨论规则，兼容迁移 cgz-* 命名
- **cgz-archive-session** `1.1.0 → 2.0.0` (major) — 改用不可变随机 ID 归档，取消共享日志与索引自动追加
- **cgz-focused-reading** `1.1.0 → 2.0.0` (major) — 按来源和范围读取团队记录，矛盾待确认，兼容迁移 cgz-* 命名
- **cgz-init** `1.1.0 → 2.0.0` (major) — 初始化本地作者身份与团队协议，移除 Obsidian 配置前置
- **cgz-daily-recap** `1.0.0 → 2.0.0` (major) — 项目内独立复盘替代外部 vault 输出，按目标日期与来源去重
- **cgz-all** `1.0.0 → 2.0.0` (major) — 统一打包 2.0 团队记忆协议与五个更新后的技能

---

## [1.2.0] — 2026-05-20

### Added

- **`cgz-daily-recap` skill** —— 按天聚合 `docs/archives/` / `docs/ai-lessons.md` / 当前会话，写一份 Obsidian 友好的 `Daily/YYYY-MM-DD.md`（YAML frontmatter + `[[wikilinks]]`）到 `obsidian_vault`。跟 `cgz-archive-session`（单次归档）职责区分：cgz-daily-recap 是按天索引。首发 `1.0.0`。

### Tooling

- `scripts/bump.py`：npm 风格版本管理脚本。`bump <plugin> --patch|--minor|--major --note "..."` 改 `marketplace.json` 并追加 CHANGELOG 条目；`--release` 把 `[Unreleased]` 切到新版本段；`--status` 看当前状态。不自动 commit / tag，最后两步必须手动。
- `CONTRIBUTING.md` 的「版本与发布」节重写，全面切换到脚本流程，禁止手改 `marketplace.json` 的 version 字段。
- **cgz-init** `1.0.0 → 1.1.0` (minor) — Ask for obsidian_vault path on init; write to AGENTS.md cgz config block for cgz-daily-recap to read

---

## [1.1.0] — 2026-05-20

### Added

- **`cgz-init` skill** —— 在用户项目里扫描记忆体系（`AGENTS.md` / `docs/ai-lessons.md` / `docs/archives/`），缺失则询问后生成。带三份模板 (`assets/AGENTS.md.template` / `assets/ai-lessons.md.template` / `assets/archives-README.md.template`)。首发 `1.0.0`。
- 三个老 skill 的 `references/` 统一改为**五大节骨架**：五原则 / 五维度 / 五心理学 / 对话严苛规则 / 语言纯化规则。
- `CONTRIBUTING.md`：贡献流程、五大节要求、命名合规、commit / PR 规范。
- `CHANGELOG.md`：本文件。
- `.github/PULL_REQUEST_TEMPLATE.md` + `.github/ISSUE_TEMPLATE/{bug_report,skill_request}.md`：PR 与 issue 引导。
- `skills/cgz-focused-discussion/agents/openai.yaml`：补齐缺失的 OpenAI 元数据；三个 skill 现在元数据齐整。

### Changed

- **Plugin versions**: `cgz-focused-discussion` / `cgz-archive-session` / `cgz-focused-reading` 从 `1.0.0` 升到 `1.1.0`（references 重写 + 风格统一）。
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
- `cgz-focused-discussion` skill：对话纪律。
- `cgz-focused-reading` skill：阅读纪律。
- `cgz-archive-session` skill：会话归档。
- CI：`.github/workflows/validate-skills.yml` + `validate_skills.py` 校验 Agent Skills spec。
- MIT License。
