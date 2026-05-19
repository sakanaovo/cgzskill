# cgzskill

> `sakanaovo` 的个人 Claude Code skill **marketplace**。
>
> 一条命令加 marketplace,然后挑想要的 skill 单独装。

---

## 这是什么

一个符合 [Agent Skills 规范](https://agentskills.io/specification) 的 Claude Code **marketplace** —— 我自己反复打磨的工作流 skill 集合,每个 skill 作为一个独立可安装的 plugin 列在 marketplace 下。

**为什么有这个仓库:**

- 整理我反复用的 skill,共享出来给同样工作流场景的人用
- 用 marketplace 形式分发,**用户挑自己要的装,不用整包 clone**
- 每个 skill 都来自自己的真实使用需求,先解决我自己反复遇到的问题,再整理成可复用的开源版本

---

## 当前包含的 skill

| Plugin / Skill | 用途 | 自动触发 | 显式触发 |
|----------------|------|---------|---------|
| **`focused-discussion`** | 对话纪律 —— 强制 Claude 单线收敛,禁止一问就甩 ABCD、禁止推理外放、禁止主动塞工时优先级。专治"一对话就跑偏"。 | 用户讨论 PR / 产品 / 架构 / UX 时;或说「跑偏了」「聚焦」「先停一下」「先看反馈」 | `/focused-discussion` |
| **`archive-session`** | 会话归档 —— 对话变长、主题变多、工作完成或准备交接时,把上下文写进项目 docs,禁止新增分析。 | 用户说「归档」「收尾」「先到这」「交接」;或 agent 自检发现上下文过长 / 分支过多时主动建议归档 | `/archive-session` |
| **`focused-reading`** | 专注阅读 —— 看文档、源码、PR、日志、网页、图文和长上下文时只回答当前问题,禁止扩题。 | 用户说「读一下」「看看文档」「理解上下文」「看这个 PR / 日志 / 图文」 | `/focused-reading` |
| **`cgz-init`** | 启动检测 —— 在新项目里扫描 `AGENTS.md` / `docs/ai-lessons.md` / `docs/archives/` 是否就位,缺失则询问后生成;同时询问并写入 `obsidian_vault` 配置供 daily-recap 使用。一次性操作。 | 用户说「初始化 cgz」「启动 cgz」「让 AI 学这套」;或在新项目首次调用其他 cgz skill 但缺记忆架构时主动建议 | `/cgz-init` |
| **`daily-recap`** | 每日复盘 —— 按天聚合当日 `docs/archives/` / `docs/ai-lessons.md` / 会话上下文,写一份 Obsidian 友好的 `Daily/YYYY-MM-DD.md`(YAML frontmatter + `[[wikilinks]]`)到 `obsidian_vault`。 | 用户说「今天复盘」「收尾今天」「daily recap」「日报」;或当天首次启动检测到昨天有未复盘归档时主动建议 | `/daily-recap` |

> 五个 skill 共用同一份骨架(写在各自 `references/`):**五原则 / 五维度 / 五心理学 / 对话严苛规则 / 语言纯化规则**。SKILL.md 是入口,references 是判定依据。
>
> **整体设计**:`cgz-init` 在项目里铺好「记忆架构」(AGENTS.md / docs/ai-lessons.md / docs/archives/) + 配置 `obsidian_vault`;`focused-reading` / `focused-discussion` / `archive-session` 在每次会话里读写这套记忆;`daily-recap` 按天把当日上下文聚合成 Obsidian Daily note。AI 不能自动学习,但下次启动读到这些文件就「像学会了」。

## 仓库结构

```
cgzskill/
├── .claude-plugin/
│   └── marketplace.json              # Marketplace manifest(列出所有可装 plugin)
├── .github/
│   ├── workflows/validate-skills.yml # CI:每次 push / PR 校验 skill spec
│   ├── scripts/validate_skills.py
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/{bug_report,skill_request}.md
├── scripts/
│   └── bump.py                       # npm 风格版本管理:bump + CHANGELOG + release
├── docs/
│   └── ai-self-evolution-architecture.md  # 四个 skill 的闭环说明
├── skills/
│   ├── focused-discussion/
│   │   ├── SKILL.md                  # 入口:触发、形状、收束句式
│   │   ├── agents/openai.yaml        # Codex 等 OpenAI 兼容 host 的元数据
│   │   └── references/discussion-discipline.md  # 判定依据:五大节骨架
│   ├── archive-session/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   └── references/archive-spec.md
│   ├── focused-reading/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   └── references/reading-spec.md
│   ├── cgz-init/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   ├── references/init-spec.md
│   │   └── assets/                   # 生成到用户项目的模板
│   │       ├── AGENTS.md.template
│   │       ├── ai-lessons.md.template
│   │       └── archives-README.md.template
│   └── daily-recap/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/recap-spec.md
├── CONTRIBUTING.md                   # 加新 skill 的流程与硬性要求
├── CHANGELOG.md                      # 版本变更记录
├── LICENSE                           # MIT
├── README.md
└── .gitignore
```

每个 skill 的 `references/` 都遵循同一份**五大节骨架**:五原则 / 五维度 / 五心理学 / 对话严苛规则 / 语言纯化规则。新 skill 的 references 必须沿用,见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

---

## 安装

### Claude Code:三种姿势

**A. Marketplace 安装(推荐)**

```bash
/plugin marketplace add sakanaovo/cgzskill
/plugin install focused-discussion@cgzskill
```

**B. 本地 plugin-dir 调试(开发模式)**

```bash
git clone https://github.com/sakanaovo/cgzskill.git
claude --plugin-dir ./cgzskill
```

**C. 退化到 standalone skill(不用 plugin / marketplace)**

```bash
cp -r skills/<skill-name> ~/.claude/skills/   # 或项目内的 .claude/skills/
```

> 提交到 Anthropic 官方 marketplace 让 `/plugin install` 直接生效:https://claude.ai/settings/plugins/submit

### Codex(OpenAI)/ Cursor / 其他 agent

Codex 可以把 skill 目录复制到用户级 skill 目录使用:

```bash
cp -r skills/focused-discussion ~/.codex/skills/
cp -r skills/archive-session ~/.codex/skills/
cp -r skills/focused-reading ~/.codex/skills/
```

如果目标 agent 不支持 skill 自动加载,再退化成项目说明方式:

```bash
cat skills/focused-discussion/SKILL.md >> /path/to/your-project/AGENTS.md
```

> 不同 agent 对 Agent Skills 的加载方式不完全一致。Claude Code 优先走 plugin / marketplace;Codex 优先走本地 skills 目录;其他 agent 可把规则放进项目说明文件。

---

## 贡献

欢迎 issue / PR。完整流程、五大节骨架要求、命名合规与提交规范见 [`CONTRIBUTING.md`](CONTRIBUTING.md);版本变更记录见 [`CHANGELOG.md`](CHANGELOG.md)。

每次 push / PR 都会自动跑 `.github/scripts/validate_skills.py`,校验 SKILL.md 是否符合 Agent Skills spec。

---

## License

MIT
