# cgzskill

> `sakanaovo` 的个人 Claude 兼容 skill 命名空间。
>
> 所有 skill 统一用 `cgz-` 前缀,方便在团队 / 多仓库混用 skill 时一眼识别来源。

---

## 这是什么

一个开源的 [Agent Skills 规范](https://agentskills.io/specification) 兼容 skill 集合。

**为什么有这个仓库:**

- 整理我自己反复用的 skill,共享出来给同样的工作流场景用
- 用统一 `cgz-` 前缀,避免和官方 / 其他人的 skill 重名(比如自带的 `focused-discussion` 不止一个版本在流传,加前缀更清楚)
- 不重复造轮子:**新 skill 用 [Anthropic 官方 skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 生成**(它带 eval / 迭代 / 描述调优,比我自己写的强),完事后改 `name` 字段加 `cgz-` 前缀就行

---

## 当前包含的 skill

| Skill | 用途 | 自动触发 | 显式触发 |
|-------|------|---------|---------|
| **`cgz-focused-discussion`** | 对话纪律 —— 强制 Claude 单线收敛,禁止一问就甩 ABCD、禁止推理外放、禁止主动塞工时优先级。专治"一对话就跑偏"。 | 用户讨论 PR / 产品 / 架构 / UX 问题时;或说「跑偏了」「聚焦」「先停一下」「先看反馈」 | `/cgz-focused-discussion` |

> 后续 skill 会加进 `skills/` 下,统一 `cgz-` 前缀。

---

## 仓库结构

```
cgzskill/
├── README.md
├── LICENSE
├── .gitignore
├── .github/
│   ├── workflows/validate-skills.yml   # CI:推送时校验 spec 合规
│   └── scripts/validate_skills.py
└── skills/
    └── cgz-focused-discussion/
        └── SKILL.md
```

---

## 安装

### Claude Code

Claude Code 启动时会自动扫描 `.claude/skills/`(项目级)和 `~/.claude/skills/`(用户级)目录,**复制 skill 文件夹进去就能用,不需要重启**。

```bash
# Clone 本仓库
git clone https://github.com/sakanaovo/cgzskill.git
cd cgzskill

# 选项 A:装到「单个项目」(只在该项目下可用)
cp -r skills/cgz-focused-discussion /path/to/your-project/.claude/skills/

# 选项 B:装到「全局用户级」(所有项目都能用)
mkdir -p ~/.claude/skills
cp -r skills/cgz-focused-discussion ~/.claude/skills/
```

验证安装成功:在 Claude Code 里输入 `/cgz-focused-discussion`,如果有响应就装好了。

### Codex / 其他 AI 编程 agent

Codex(OpenAI)目前没有 Claude Code 那套 `.claude/skills/` 自动加载机制。Codex 读 **`AGENTS.md`** 当项目说明。让 Codex 也用上本 skill,有两种做法:

**做法 A:把 SKILL.md 内容贴进 AGENTS.md**(最简单,推荐)

```bash
# 在你的项目根目录
cat skills/cgz-focused-discussion/SKILL.md >> AGENTS.md
```

(把 cgzskill 仓库的 SKILL.md 内容追加到你项目的 AGENTS.md。Codex 读 AGENTS.md 时就会拿到这套对话纪律。)

**做法 B:在 AGENTS.md 里引用,让 Codex 读时去拉**

```markdown
# AGENTS.md

## 对话纪律
请遵守 https://github.com/sakanaovo/cgzskill/blob/main/skills/cgz-focused-discussion/SKILL.md 里的对话纪律。
```

(更轻,但依赖 agent 能联网取内容。)

> ⚠️ **诚实提醒**:Agent Skills spec 本身是统一的,但**自动加载机制是 Claude Code 独有**。Codex / Cursor / 其他 agent 用本仓库的 skill,目前都是手动"贴进 AGENTS.md"的方式。

---

## 自己创建新 skill 的推荐流程

**不用我重新造轮子。用 Anthropic 官方的 `skill-creator`,完事改个前缀就行:**

```bash
# 1. clone 官方 skills 仓库(里面有 skill-creator)
git clone https://github.com/anthropics/skills.git

# 2. 把 skill-creator 装到你的项目
cp -r skills/skills/skill-creator /path/to/your-project/.claude/skills/

# 3. 在 Claude Code 里跑
/skill-creator 帮我做一个 XX 的 skill
```

走完 skill-creator 的采访 + eval 流程之后,把生成的 skill:

1. 改 `name` 字段:`my-skill` → `cgz-my-skill`
2. 同步改父目录名 `my-skill/` → `cgz-my-skill/`(spec 硬性要求 name = 父目录名)
3. 提 PR 到本仓库 `skills/` 下

---

## CI

每次 push / PR 自动跑 `.github/scripts/validate_skills.py`,校验:

- SKILL.md 存在
- YAML frontmatter 合法
- `name` 字段 = 父目录名,kebab-case,≤ 64 字符
- `description` ≤ 1024 字符
- SKILL.md 正文 ≤ 500 行(超出建议拆 `references/`)

红 → 合并被拦。

---

## License

MIT

---

## Contributing

欢迎 issue / PR。如果你用 `skill-creator` 造出了好 skill,改个 `cgz-` 前缀提过来 —— 通过 CI 校验就能合。
