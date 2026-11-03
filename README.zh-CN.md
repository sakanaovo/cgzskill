# cgzskill：面向 AI 助手与编程工具的项目记忆技能

[English](README.md) · [更新记录](CHANGELOG.md) · [贡献指南](CONTRIBUTING.md) · [团队验收清单](docs/team-acceptance.md)

**让 AI 阅读和讨论更聚焦，让会话归档、团队交接和每日复盘有据可查。**

cgzskill 是一套支持选择文档语言、面向支持 [Agent Skills](https://agentskills.io/specification) 的 AI 助手与编程工具的项目记忆技能。包含 5 个独立技能；Claude Code marketplace 另提供全套安装包 `cgz-all`。下方以 Claude Code 和 Codex 演示安装，不限定适用宿主；其他工具须按其技能规范适配，未逐一实测。

**本次更新准备 2.1.0。** 初始化时可选择简体中文（`zh-CN`）、英文（`en`）或明确指定的其他语言，并保存为后续文档偏好。技能说明与参考规范仍主要使用中文，生成的文档正文遵循下方语言规则，不由技能说明的语言决定；这不表示所有语言或宿主都已实测。

项目记忆保存在可审查的 Markdown 文件中。团队成员各自写独立记录，再按来源汇总，减少多人争写同一个日志或索引的机会。它不是模型自动学习、账号系统或自动 Git 合并服务。

## 五个 skill 分别做什么

| Skill | 解决的问题 | 你可以这样说 | 输出或行为 |
| --- | --- | --- | --- |
| [`cgz-focused-reading`](skills/cgz-focused-reading/SKILL.md) | 读文档、代码、PR 或日志时容易扩题 | “读这个 PR，只说风险” | 只回答当前问题，区分事实、推断和未验证点 |
| [`cgz-focused-discussion`](skills/cgz-focused-discussion/SKILL.md) | 讨论发散，没问就给多套方案 | “先聚焦这个问题” | 闭合当前议题，不擅自扩展方案、工时和优先级 |
| [`cgz-archive-session`](skills/cgz-archive-session/SKILL.md) | 长会话或交接丢上下文，多人追加同一日志 | “把这轮归档，给下一位接手” | 带作者、范围、验证状态和来源的独立会话记录 |
| [`cgz-init`](skills/cgz-init/SKILL.md) | 每个项目都要手动搭记忆目录 | “初始化 cgz，作者别名用 alice，以后文档用英文” | 一次补齐本地身份、文档语言偏好与共享协议，保留已有文件 |
| [`cgz-daily-recap`](skills/cgz-daily-recap/SKILL.md) | 一天多份归档难以回看，重复内容混在一起 | “复盘今天”或“补昨天的复盘” | 按目标日期聚合事实，按来源去重，冲突保留为待确认 |

阅读和讨论可直接单独使用。归档、复盘也包含独立使用的最小协议；团队项目用 `cgz-init` 建立统一入口更方便。主动建议写入仍须确认，用户明确要求初始化或归档时按对应 skill 的授权范围执行。

## 让 AI 帮你安装

把下面这段发给有本地项目访问能力的 AI 编程助手。安装来源是仓库当前 `main`；语言功能需要包含本次 2.1.0 更新的版本：

```text
请帮我安装 https://github.com/sakanaovo/cgzskill 当前 main 的技能。先核对检出的版本和实际功能，再判断是否已有新的语言配置支持。阅读 README，识别我正在使用的 AI 助手或编程工具，核对其是否支持 Agent Skills，并确认项目级或用户级等宿主支持的安装范围；Claude Code 和 Codex 可参考文中示例，其他宿主按其官方规范处理，不猜路径或命令。按宿主说明安装完整目录（含 references 和 assets），已有同名技能先核对，不覆盖或重复安装。安装后用宿主实际显示的入口引导 cgz-init，按需确认作者别名，并询问以后生成文档使用简体中文（zh-CN）、英文（en）还是我明确指定的其他语言。把偏好保存到 .cgz/local.json 的 document_language，保留已有作者别名和 UUID。项目共享文件的语言单独遵循已有约定，没有约定时在初始化中确认一次。保留原项目文件和已有身份。分别核验“宿主已加载技能”和“初始化已完成”，不要把复制成功当作加载成功；没有本地访问权限就给我操作步骤。不要关闭安全限制、运行未经审查的代码或提交凭据。
```

也可按下面的命令自行安装。

## 安装示例一：Claude Code

在 **Claude Code 会话里**输入，不是在系统 shell 中执行：

```text
/plugin marketplace add sakanaovo/cgzskill
/plugin install cgz-all@cgzskill
```

在需要记忆的项目中调用：

```text
/cgz-all:cgz-init
```

首次确认作者别名和文档语言；也可以直接说明“作者别名用 alice，以后文档用英文”。语言可选 `zh-CN`、`en` 或明确指定的其他语言。项目共享文件没有既定语言时，初始化会单独确认一次。Git 显示名仅作候选，不取邮箱。初始化会展示已有与缺失项，只补齐授权骨架，不覆盖旧身份或项目规则。

随后按需使用：

```text
/cgz-all:cgz-focused-reading
/cgz-all:cgz-focused-discussion
/cgz-all:cgz-archive-session
/cgz-all:cgz-daily-recap
```

只装一个技能时，例如：

```text
/plugin install cgz-archive-session@cgzskill
/cgz-archive-session:cgz-archive-session
```

Claude Code 插件命令使用 `/插件名:技能名`，详见[官方插件说明](https://code.claude.com/docs/en/plugins)。不要同时安装全套包和重复的单项包，避免出现重复技能入口。实际可用命令以宿主的技能列表为准。

## 安装示例二：Codex 与其他方式

### Codex：复制完整目录

在终端执行下面的首次安装示例。已有同名目录时先检查本地改动，不盲目覆盖：

```bash
git clone https://github.com/sakanaovo/cgzskill.git
cd cgzskill
mkdir -p ~/.agents/skills
cp -Rn skills/cgz-* ~/.agents/skills/
```

在目标项目里通过 `/skills` 选择技能，或输入 `$cgz-init`。团队也可将选定的完整目录放到项目 `.agents/skills/`，但不要重复安装同名技能。目录与调用方式见 [Codex 官方技能说明](https://developers.openai.com/codex/skills/)。

### Claude Code：本地开发或独立 skill

```bash
# 在包含该仓库的父目录启动本地插件开发模式
claude --plugin-dir ./cgzskill
```

不走 marketplace 时，将所需完整 skill 目录复制到 `~/.claude/skills/` 或目标项目 `.claude/skills/`。这种安装方式的命令没有插件命名空间；以宿主显示的名称为准。

其他宿主需要**保留完整 skill 目录**，包括 `SKILL.md`、`references/` 和已有 `assets/`，再按其说明适配入口。只拼接 `SKILL.md` 到项目说明会丢失引用。其他宿主的目录、调用入口和能力以其官方说明为准；本仓库未逐一验证，不能由遵循技能规范推定已兼容。

## 初始化后，项目里有什么

```text
项目根/
├── .cgz/local.json        # 本工作副本身份与 document_language，精确忽略 /.cgz/local.json
├── .gitignore            # 仅补所需的身份忽略项
├── AGENTS.md             # 共享入口，已有规则保留
└── docs/
    ├── cgz-memory.md     # 团队记录协议
    ├── ai-lessons.md     # 已采纳规则与稳定入口
    ├── archives/         # 独立会话归档
    ├── lessons/          # 独立候选教训
    └── daily/            # 独立日复盘
```

每份记录的路径为：

- `docs/archives/YYYY-MM-DD-<record_id>.md`
- `docs/lessons/YYYY-MM-DD-<record_id>.md`
- `docs/daily/YYYY-MM-DD-<record_id>.md`

`author_id` 是工作副本本地生成的随机 UUID，用于追溯来源，不证明现实身份。每份新记录另有随机 `record_id`；同人多会话也不用作者名或日期充当唯一标识。无 Git 仍可使用，分支和基线 commit 无法获取时不编造。

以下是记录元数据的示意，ID 不能直接复制用于新记录：

```yaml
record_id: "<每份记录新生成的 UUID>"
author_id: "<本地随机作者 UUID>"
author_alias: "alice"
document_language: "zh-CN"
date: "2026-11-03"
recorded_at: "2026-11-03T10:00:00+08:00"
scope: "src/auth/"
verification: "unverified"
branch: null
base_commit: null
source_ids: []
supersedes: []
```

## 选择文档语言

初始化把用户明确选择的语言保存为 `.cgz/local.json` 中的 `document_language`：简体中文用 `zh-CN`，英文用 `en`，其他语言填写明确的名称或标签，例如 `日本語` 或 `ja`。“其他”只是继续询问具体语言的选项，不能直接存作语言值。

新生成的个人记录（会话归档、候选教训、日复盘等）按以下顺序决定正文语言：

1. 本次请求明确指定的语言。
2. `.cgz/local.json` 中已保存的 `document_language`。
3. 项目已有的文档语言约定。
4. 都没有时，在首次生成文档前询问。

不根据系统区域设置、账号、位置、Git 身份或单条消息的语言猜测偏好。“这次复盘用英文”只作用于本次；“以后文档都用英文”才更新保存的偏好。表达不明确时，先确认是临时选择还是长期偏好，不擅自修改配置。

**共享文件遵循项目语言，不跟随个人偏好切换。** `AGENTS.md`、`docs/cgz-memory.md`、`docs/ai-lessons.md` 保持项目已有的语言约定；没有约定时，在初始化中单独确认一次，并记录到共享协议。个人语言设置不能静默改变团队约定。

为旧安装补语言字段时，保留已有 `author_alias` 和 `author_id`，不生成新身份。偏好只影响未来生成的正文，不自动翻译或改写历史记录、已采纳规则或来源引文。路径、文件名、命令、元数据字段名、UUID、来源 ID，以及 `pending`、`unverified` 等协议值保持不变。修改已有共享规则仍需通常的明确批准或团队审阅。

## 两个人同时使用时怎么处理

- **写入分开**：独立文件、独占创建，不自动追加共享索引、`AGENTS.md` 或 `docs/ai-lessons.md`。已有身份被 Git 跟踪时先警告，不自动删除或改历史。
- **原始记录保留**：更正写新记录并引用旧 ID，不改写或去重删除原文件。
- **汇总有规则**：同义且同范围合并来源；互补差异保留；不同范围分别标注；同范围矛盾标 `pending`，等待确认。
- **规则需采纳**：新的 lesson 是候选。经明确批准或团队 PR 审阅后才更新稳定规则，不能按最后写入时间决定谁正确。
- **复盘不递归**：只聚合归档、教训和可核实的会话事实，不把旧日报当新来源。同一作者、日期、范围、来源集合及实际输出语言没有变化且无新事实时复用已有摘要；语言不同则新建独立摘要，保留旧记录。

完整说明见[项目记忆架构](docs/ai-self-evolution-architecture.md)。这些规则减少共享文件冲突的来源，不保证 agent 永不犯错，也不替代 Git review。

## 从 2.0 升级到 2.1

更新完整 skill 目录后运行 `cgz-init`，确认并补上缺失的 `document_language`，保留原作者别名与 UUID。已有有效语言偏好保持不变，除非用户明确要求修改；缺失的共享文件语言约定与个人偏好分开确认。原文件保留，不自动翻译或迁移历史。

仓库首页现为英文，完整中文说明在 [README.zh-CN.md](README.zh-CN.md)，旧 [README.en.md](README.en.md) 地址保留兼容入口。本次更新时，已发布版本为 [v2.0.0](https://github.com/sakanaovo/cgzskill/releases/tag/v2.0.0)，不包含这次新增的语言功能。本次改动准备 2.1.0，尚未创建 `v2.1.0` tag 或 Release。安装提示使用当前 `main`，需要核实它已包含本次更新，才能使用新行为。

## 从 1.x 升级到 2.0

这是包含不兼容变化的主版本升级：

1. 四个旧名称统一加 `cgz-` 前缀：`focused-discussion`、`archive-session`、`focused-reading`、`daily-recap`。`cgz-init` 保持原名。检查旧安装入口，按上方新名称安装，避免新旧副本同时加载。
2. 更新完整 skill 目录，保留本地修改再迁移；不要只换 `SKILL.md`。marketplace 安装在 `/plugin` 中检查更新。
3. 在项目中运行新版 init，补齐本地身份和团队协议。已有规则与新协议冲突时先确认，不自动替换；再次运行不更换有效身份或重复追加说明。
4. 历史日志、单文件归档和旧索引保留并兼容读取，不自动搬移或删除。新记录改用随机 ID 独立文件，候选教训不再自动写到共享日志顶部。
5. **Obsidian 集成要求已移除**。旧 vault 配置保留但不读取、不使用。复盘写项目内 `docs/daily/`，不写外部 vault，不要求安装 Obsidian。

版本详情见 [2.0.0 变更记录](CHANGELOG.md)。版本文件与日志不等同于 Git tag 或 GitHub Release，是否发布以仓库实际状态为准。

## 验证范围与限制

- Python 校验器检查 5 个 skill 的基础规范；工具与契约测试覆盖工具回归、元数据模板与文本契约。
- 文本契约通过不代表实际宿主一定正确执行。**真实双人、多会话、不同 worktree 及多语言的宿主端到端验收尚未执行**，不表示所有语言都已验证，见[人工验收清单](docs/team-acceptance.md)。
- 本仓库主要提供说明型技能，由宿主 agent 按需执行。没有后台文件监听、自动同步、账号认证或自动 Git 合并，也不会自动训练模型。
- Obsidian 接入未实测且不作为当前支持功能。使用任何宿主时仍受其权限与确认机制约束。

本地检查：

```bash
python3 -m pip install pyyaml
python3 .github/scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```

## 目录与贡献

- `skills/`：五个入口、各自规范和初始化模板。
- `.claude-plugin/marketplace.json`：五个独立 plugin 与 `cgz-all`。
- `.github/`、`tests/`：校验脚本、回归与契约测试、CI。
- `scripts/bump.py`：版本与 CHANGELOG 同步工具。
- [CONTRIBUTING.md](CONTRIBUTING.md)：贡献要求与发布流程。

每个 skill 的规范遵循五原则、五维度、五心理学、对话严苛规则、语言纯化规则。欢迎报告可复现的工作流问题或提交有真实使用场景的改进。

## License

[MIT](LICENSE)
