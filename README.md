# cgzskill

> `sakanaovo` 的个人 Claude Code 插件 + skill 命名空间。
>
> 一行命令安装,自动 namespace 隔离,不和别人的 skill 撞名。

---

## 这是什么

一个符合 [Agent Skills 规范](https://agentskills.io/specification) 的 Claude Code **plugin**(同时也是 skill 集合),包含我自己反复打磨的工作流 skill。

**为什么有这个仓库:**

- 整理我反复用的 skill,共享出来给同样工作流场景的人用
- 用 plugin 形式分发,**用户一行命令装,不用 `git clone` + `cp -r`**
- 不重复造轮子:**新 skill 用 [Anthropic 官方 skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 生成**(自带 eval / 迭代 / 描述调优),完事归到 `cgzskill` namespace 即可

---

## 当前包含的 skill

| Skill | 用途 | 自动触发 | 显式触发 |
|-------|------|---------|---------|
| **`focused-discussion`** | 对话纪律 —— 强制 Claude 单线收敛,禁止一问就甩 ABCD、禁止推理外放、禁止主动塞工时优先级。专治"一对话就跑偏"。 | 用户讨论 PR / 产品 / 架构 / UX 时;或说「跑偏了」「聚焦」「先停一下」「先看反馈」 | `/cgzskill:focused-discussion` |

> 注:Claude Code plugin 加载后,所有 skill 自动加 `cgzskill:` 前缀(plugin namespace)。

---

## 仓库结构

```
cgzskill/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
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

| 场景 | 命令 | 调用方式 |
|------|------|---------|
| **本地 plugin 调试**(你 clone 到本地用) | `git clone https://github.com/sakanaovo/cgzskill.git && claude --plugin-dir ./cgzskill` | `/cgzskill:focused-discussion` |
| **远程 zip plugin**(打成 zip 挂到任意 URL) | `claude --plugin-url https://example.com/cgzskill.zip` | `/cgzskill:focused-discussion` |
| **走 marketplace**(提交到官方后) | `/plugin install cgzskill` | `/cgzskill:focused-discussion` |
| **退化到 standalone skill**(不用 plugin) | `cp -r skills/focused-discussion ~/.claude/skills/`(或项目 `.claude/skills/`) | `/focused-discussion`(无 namespace) |

> 提交到官方 marketplace:https://claude.ai/settings/plugins/submit

### Codex(OpenAI)/ Cursor / 其他 agent

**这些 agent 没有 Claude Code 的 plugin 机制 ——** 它们读 `AGENTS.md` 当项目说明。让它们用上本仓库的对话纪律,有两种做法:

| 做法 | 命令 | 说明 |
|------|------|------|
| **A. 内容追加**(最稳,推荐) | `cat skills/focused-discussion/SKILL.md >> /path/to/your-project/AGENTS.md` | 把 SKILL.md 内容贴到你项目的 AGENTS.md。Codex 读 AGENTS.md 时会拿到这套纪律 |
| **B. 链接引用**(更轻,依赖联网) | 在 AGENTS.md 写一行:`请遵守 https://github.com/sakanaovo/cgzskill/blob/main/skills/focused-discussion/SKILL.md 里的对话纪律` | Codex 需要能联网拉远程文件;不是所有 agent / 网络环境都支持 |

> ⚠️ **诚实提醒**:Agent Skills 规范本身是统一的,但**自动加载 + namespace 机制是 Claude Code 独有**。Codex / Cursor 等 agent 目前都是手动嵌进 AGENTS.md 的方式。

---

## 自己造新 skill 加进来的推荐流程

不重新造轮子。用官方 `skill-creator` 生成,然后归入 `cgzskill` namespace:

```bash
# 1. 装 Anthropic 官方 skill-creator(它带 eval + 迭代 + 描述调优)
git clone https://github.com/anthropics/skills.git
cp -r skills/skills/skill-creator ~/.claude/skills/

# 2. 在 Claude Code 里用
/skill-creator 帮我做一个 XX 的 skill
```

走完 `skill-creator` 的采访 + eval 流程之后,把生成的 skill:

1. 父目录改成不带前缀的名字(plugin namespace 会自动加前缀,前缀重复就丑了)
2. `name` 字段同步父目录名(spec 硬性要求)
3. 提 PR 到本仓库 `skills/` 下
4. CI 自动跑校验,绿了能合

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

欢迎 issue / PR。`skill-creator` 造出来的 skill,改父目录名 + name 字段后,过 CI 校验就能合。
