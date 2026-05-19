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
| **`archive-session`** | 会话归档 —— 对话变长、主题变多、工作完成或准备交接时,把上下文写进项目 docs,不新增分析。 | 用户说「归档」「收尾」「先到这」「handoff」;或 agent 自检发现上下文过长/分支过多时先建议归档 | `/archive-session` |
| **`focused-reading`** | 专注阅读 —— 看文档、源码、PR、日志、网页、图文和长上下文时,只回答当前问题。 | 用户说「读一下」「看看文档」「理解上下文」「看这个 PR/日志/图文」 | `/focused-reading` |

## 仓库结构

```
cgzskill/
├── .claude-plugin/
│   └── marketplace.json         # Marketplace manifest(列出所有可装 plugin)
├── README.md
├── LICENSE
├── .gitignore
├── .github/
│   ├── workflows/validate-skills.yml
│   └── scripts/validate_skills.py
└── skills/
    ├── focused-discussion/
    │   ├── SKILL.md
    │   └── references/discussion-discipline.md
    ├── archive-session/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/archive-spec.md
    └── focused-reading/
        ├── SKILL.md
        ├── agents/openai.yaml
        └── references/reading-spec.md
```

---

## 安装

### Claude Code:三种姿势

| 场景 | 命令 |
|------|------|
| **A. Marketplace 安装**(推荐) | `/plugin marketplace add sakanaovo/cgzskill` 然后 `/plugin install focused-discussion@cgzskill` |
| **B. 本地 plugin-dir 调试**(开发模式) | `git clone https://github.com/sakanaovo/cgzskill.git && claude --plugin-dir ./cgzskill` |
| **C. 退化到 standalone skill**(不用 plugin / marketplace) | `cp -r skills/<skill-name> ~/.claude/skills/`(或项目 `.claude/skills/`) |

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

## 新 skill 加进 marketplace 的流程

每个新 skill 先从自己的真实使用场景出发,把反复出现的问题沉淀成一套简洁规则,再按 Agent Skills 规范整理成目录:

1. 把 skill 目录放到 `skills/<skill-name>/SKILL.md`
2. `name` 字段同步父目录名(spec 硬性要求)
3. 在 `.claude-plugin/marketplace.json` 的 `plugins` 数组里加一条:
   ```json
   {
     "name": "<skill-name>",
     "description": "...",
     "source": "./",
     "strict": false,
     "version": "1.0.0",
     "category": "...",
     "keywords": ["..."],
     "skills": ["./skills/<skill-name>"]
   }
   ```
4. 提 PR → CI 校验通过 → 合并

---

## CI

每次 push / PR 自动跑 `.github/scripts/validate_skills.py`,校验:

- SKILL.md 存在
- YAML frontmatter 合法
- `name` 字段 = 父目录名,kebab-case,≤ 64 字符
- `description` ≤ 1024 字符
- SKILL.md 正文 ≤ 500 行(超出建议拆 `references/`)

---

## License

MIT

---

## Contributing

欢迎 issue / PR。新 skill 需要来自真实使用场景,加进 `skills/` + 在 `marketplace.json` 加一条,过 CI 校验就能合。
