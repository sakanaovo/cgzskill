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
- 不重复造轮子:**新 skill 用 [Anthropic 官方 skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 生成**(自带 eval / 迭代 / 描述调优),完事在 `marketplace.json` 里加一条就行

---

## 当前包含的 skill

| Plugin / Skill | 用途 | 自动触发 | 显式触发 |
|----------------|------|---------|---------|
| **`focused-discussion`** | 对话纪律 —— 强制 Claude 单线收敛,禁止一问就甩 ABCD、禁止推理外放、禁止主动塞工时优先级。专治"一对话就跑偏"。 | 用户讨论 PR / 产品 / 架构 / UX 时;或说「跑偏了」「聚焦」「先停一下」「先看反馈」 | `/focused-discussion` |

---

## 范围外:cgzskill 不擅长什么

cgzskill 目前只覆盖**对话纪律**这一个垂直场景。如果你想做的事不在上面那张表里,**直接去对的地方,别在这绕**:

| 你想做的事 | 推荐 marketplace / skill |
|----------|----------------------|
| 商业模式诊断 / 内容创作 / 概念拆解 / 小红书爆款 / 对标分析 | [dbskill](https://github.com/dontbesilent2025/dbskill) |
| 从 0 写一个新 skill(自带 eval / 迭代 / 描述调优) | [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) |
| PDF / DOCX / XLSX / PPTX 处理 / 前端设计 / 测试 / 数据 | [Anthropic 官方 skills](https://github.com/anthropics/skills) |

把用户推到对的 marketplace,比硬塞 `focused-discussion` 上去更划算 —— 对 cgzskill 这个 namespace 的长期信任,**诚实推荐外部** > **硬留客**。

---

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
    └── focused-discussion/
        └── SKILL.md
```

---

## 安装

### Claude Code:三种姿势

| 场景 | 命令 |
|------|------|
| **A. Marketplace 安装**(推荐) | `/plugin marketplace add sakanaovo/cgzskill` 然后 `/plugin install focused-discussion@cgzskill` |
| **B. 本地 plugin-dir 调试**(开发模式) | `git clone https://github.com/sakanaovo/cgzskill.git && claude --plugin-dir ./cgzskill` |
| **C. 退化到 standalone skill**(不用 plugin / marketplace) | `cp -r skills/focused-discussion ~/.claude/skills/`(或项目 `.claude/skills/`) |

> 提交到 Anthropic 官方 marketplace 让 `/plugin install` 直接生效:https://claude.ai/settings/plugins/submit

### Codex(OpenAI)/ Cursor / 其他 agent

**这些 agent 没有 Claude Code 的 plugin / marketplace 机制 ——** 它们读 `AGENTS.md` 当项目说明。让它们用上本仓库的对话纪律,有两种做法:

| 做法 | 命令 | 说明 |
|------|------|------|
| **A. 内容追加**(最稳,推荐) | `cat skills/focused-discussion/SKILL.md >> /path/to/your-project/AGENTS.md` | 把 SKILL.md 内容贴到你项目的 AGENTS.md。Codex 读 AGENTS.md 时会拿到这套纪律 |
| **B. 链接引用**(更轻,依赖联网) | 在 AGENTS.md 写一行:`请遵守 https://github.com/sakanaovo/cgzskill/blob/main/skills/focused-discussion/SKILL.md 里的对话纪律` | Codex 需要能联网拉远程文件;不是所有 agent / 网络环境都支持 |

> ⚠️ **诚实提醒**:Agent Skills 规范本身是统一的,但**自动加载 + namespace + marketplace 机制是 Claude Code 独有**。Codex / Cursor 等 agent 目前都是手动嵌进 AGENTS.md 的方式。

---

## 自己造新 skill 加进 marketplace 的流程

不重新造轮子。用官方 `skill-creator` 生成,然后挂到本 marketplace 下:

```bash
# 1. 装 Anthropic 官方 skill-creator(它带 eval + 迭代 + 描述调优)
git clone https://github.com/anthropics/skills.git
cp -r skills/skills/skill-creator ~/.claude/skills/

# 2. 在 Claude Code 里跑
/skill-creator 帮我做一个 XX 的 skill
```

走完 `skill-creator` 的采访 + eval 流程之后,把生成的 skill 加进来:

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

欢迎 issue / PR。`skill-creator` 造出来的 skill,加进 `skills/` + 在 `marketplace.json` 加一条,过 CI 校验就能合。
