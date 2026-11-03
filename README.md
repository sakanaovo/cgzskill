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
| **`cgz-focused-discussion`** | 对话纪律 —— 强制 Claude 单线收敛,禁止一问就甩 ABCD、禁止推理外放、禁止主动塞工时优先级。专治"一对话就跑偏"。 | 用户讨论 PR / 产品 / 架构 / UX 时;或说「跑偏了」「聚焦」「先停一下」「先看反馈」 | `/cgz-focused-discussion` |
| **`cgz-archive-session`** | 会话归档 —— 对话变长、主题变多、工作完成或准备交接时,把上下文写进项目 docs,禁止新增分析。 | 用户说「归档」「收尾」「先到这」「交接」;或 agent 自检发现上下文过长 / 分支过多时主动建议归档 | `/cgz-archive-session` |
| **`cgz-focused-reading`** | 专注阅读 —— 看文档、源码、PR、日志、网页、图文和长上下文时只回答当前问题,禁止扩题。 | 用户说「读一下」「看看文档」「理解上下文」「看这个 PR / 日志 / 图文」 | `/cgz-focused-reading` |
| **`cgz-init`** | 启动检测 —— 在新项目里扫描 `AGENTS.md` / `docs/ai-lessons.md` / `docs/archives/` 是否就位,缺失则经一次身份确认后生成，不要求外部应用配置。一次性操作。 | 用户说「初始化 cgz」「启动 cgz」「让 AI 学这套」;或在新项目首次调用其他 cgz skill 但缺记忆架构时主动建议 | `/cgz-init` |
| **`cgz-daily-recap`** | 每日复盘 —— 按天聚合当日 `docs/archives/` / `docs/ai-lessons.md` / 会话上下文,写一份项目内 `docs/daily/YYYY-MM-DD-<record_id>.md`，使用普通 Markdown。 | 用户说「今天复盘」「收尾今天」「daily recap」「日报」;或当天首次启动检测到昨天有未复盘归档时主动建议 | `/cgz-daily-recap` |

> 五个 skill 共用同一份骨架(写在各自 `references/`):**五原则 / 五维度 / 五心理学 / 对话严苛规则 / 语言纯化规则**。SKILL.md 是入口,references 是判定依据。
>
> **整体设计**:`cgz-init` 在项目里铺好「记忆架构」(AGENTS.md / docs/ai-lessons.md / docs/archives/);`cgz-focused-reading` / `cgz-focused-discussion` / `cgz-archive-session` 在每次会话里读写这套记忆;`cgz-daily-recap` 按天把当日上下文聚合成项目内日复盘，不要求先初始化。AI 不能自动学习,但下次启动读到这些文件就「像学会了」。

> **Obsidian 集成已从核心流程移除**：初始化不问 vault，复盘不读旧 vault 配置，也不向外部目录写入。已有项目配置原样保留。只移除集成要求，保留复盘能力；Obsidian 接入尚未实测，不宣称已支持。

## 团队开箱使用

1. 安装所需 skill，在项目里运行 `/cgz-init`，首次确认作者别名。Git 用户名只是候选，不用 email 识别人；没有 Git 也能使用。
2. 初始化创建本地 `.cgz/local.json`（随机 `author_id`），仅用 `/.cgz/local.json` 精确忽略；团队协议在 `docs/cgz-memory.md`。已有文件和身份不覆盖，旧记录不搬移。每个工作副本独立身份，不写全局 Git 配置。
3. 归档写 `docs/archives/YYYY-MM-DD-<record_id>.md`，候选教训写 `docs/lessons/YYYY-MM-DD-<record_id>.md`，复盘写 `docs/daily/YYYY-MM-DD-<record_id>.md`。每次新记录用随机 UUID；作者、日期、分支不是唯一性保证。
4. 原始记录不可改写或去重删除；修正用新记录引用旧 ID。不会每次追加共享索引、`AGENTS.md` 或 `docs/ai-lessons.md`。后者是稳定规则入口，采纳候选规则须明确确认或团队 PR 审核。
5. 汇总同义且同范围合并并保留全部来源；互补差异保留，不同范围标范围，同范围矛盾标 `pending`。不采用最后写入覆盖；同来源集合重复复盘不重复计数，也不把日报递归当新来源。

这是 agent 执行的文件协议，不是账号系统、后台监听或自动 Git 合并服务；`author_id` 不是身份认证。初始化授权只涵盖列出的项目骨架和精确忽略项，不读取主目录、不改业务代码、不存密钥。单独安装阅读/讨论无需初始化；归档/复盘各自含最小身份与记录协议。

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
│   └── ai-self-evolution-architecture.md  # 五个 skill 的闭环说明
├── skills/
│   ├── cgz-focused-discussion/
│   │   ├── SKILL.md                  # 入口:触发、形状、收束句式
│   │   ├── agents/openai.yaml        # Codex 等 OpenAI 兼容 host 的元数据
│   │   └── references/discussion-discipline.md  # 判定依据:五大节骨架
│   ├── cgz-archive-session/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   └── references/archive-spec.md
│   ├── cgz-focused-reading/
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
│   │       ├── archives-README.md.template
│   │       ├── local.json.template
│   │       └── cgz-memory.md.template
│   └── cgz-daily-recap/
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
/plugin install cgz-all@cgzskill
```

只想装单个 skill 时，把 `cgz-all` 换成对应 plugin 名，例如:

```bash
/plugin install cgz-focused-discussion@cgzskill
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
cp -r skills/cgz-focused-discussion ~/.codex/skills/
cp -r skills/cgz-archive-session ~/.codex/skills/
cp -r skills/cgz-focused-reading ~/.codex/skills/
cp -r skills/cgz-init ~/.codex/skills/
cp -r skills/cgz-daily-recap ~/.codex/skills/
```

如果目标 agent 不支持 skill 自动加载，需要保留完整 skill 目录（包括 `SKILL.md`、`references/` 和已有 `assets/`），并按目标 agent 的说明手动适配入口和引用路径。禁止只把 `SKILL.md` 拼接到 `AGENTS.md`：入口依赖的规范和模板不会随文本自动复制。

> 不同 agent 对 Agent Skills 的加载方式不完全一致。Claude Code 优先走 plugin / marketplace；Codex 优先复制完整 skill 目录；其他 agent 的手动适配不等于已验证支持。

---

## 贡献

欢迎 issue / PR。完整流程、五大节骨架要求、命名合规与提交规范见 [`CONTRIBUTING.md`](CONTRIBUTING.md);版本变更记录见 [`CHANGELOG.md`](CHANGELOG.md)。

每次 push / PR 都会自动跑 `.github/scripts/validate_skills.py`,校验 SKILL.md 是否符合 Agent Skills spec。

---

## License

MIT
