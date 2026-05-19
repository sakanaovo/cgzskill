# 贡献指南

本仓库是符合 [Agent Skills 规范](https://agentskills.io/specification) 的 Claude Code marketplace。每个 skill 是一个独立可装的 plugin。

新 skill 必须来自真实使用场景 —— 你反复遇到的同一类问题，沉淀成一套简洁规则，而不是凭空设计。

---

## 加新 skill 的流程

### 1. 目录结构

```
skills/<skill-name>/
├── SKILL.md                   # 入口：触发、形状、收束句式
├── agents/openai.yaml         # Codex 等 OpenAI 兼容 host 的元数据
└── references/<spec-name>.md  # 判定依据：五大节骨架
```

`<skill-name>` 必须是 kebab-case，且**等于父目录名**（spec 硬性要求）。

### 2. SKILL.md frontmatter

```yaml
---
name: <skill-name>
description: "1-1024 字符。描述「做什么 + 何时用」，必须含触发关键词。"
---
```

- `name` ≤ 64 字符，只能是小写字母 / 数字 / 连字符，不能以连字符开头或结尾，不能有连续连字符。
- `description` 必须有触发关键词，让 host 能自动匹配。
- `SKILL.md` 正文 ≤ 500 行；超出必须拆 `references/`。

### 3. references/ 必须走五大节骨架

每个 skill 的 references 文件统一分五节：

1. **五原则** —— 必须遵守的核心约束
2. **五维度** —— 发送 / 写入前的硬性自检
3. **五心理学** —— 失败模式背后的认知机制
4. **对话严苛规则** —— 允许 / 禁止句式，禁止铺垫与客套
5. **语言纯化规则** —— 中文段落不夹裸英文，英文模板保留纯英文

参考实现：

- [`skills/cgz-focused-discussion/references/discussion-discipline.md`](skills/cgz-focused-discussion/references/discussion-discipline.md)
- [`skills/cgz-focused-reading/references/reading-spec.md`](skills/cgz-focused-reading/references/reading-spec.md)
- [`skills/cgz-archive-session/references/archive-spec.md`](skills/cgz-archive-session/references/archive-spec.md)

### 4. agents/openai.yaml 必填

```yaml
interface:
  display_name: "Skill Title"
  short_description: "一句中文短描述，不加句号"
  default_prompt: "host 调用 skill 时使用的一句中文指令"
```

每个 skill 都必须有这份文件，字段完整。

### 5. 注册到 marketplace

在 `.claude-plugin/marketplace.json` 的 `plugins` 数组里加一条：

```json
{
  "name": "<skill-name>",
  "description": "对中文用户友好的简短描述,语气与 SKILL.md 保持一致(禁止/必须/立刻)。",
  "source": "./",
  "strict": false,
  "version": "1.0.0",
  "category": "<category>",
  "keywords": ["..."],
  "skills": ["./skills/<skill-name>"]
}
```

- `description` 必须和 SKILL.md 内的风格一致：用「禁止 / 必须 / 立刻」，禁止「优先 / 尽量 / 建议」。
- `version` 走 [SemVer](https://semver.org/)：bug 修 patch、加规则 minor、破坏性改动 major。

### 6. 更新 CHANGELOG.md

在 `Unreleased` 段加一条改动记录，合并前由维护者归到对应版本。

---

## 提交规范

### Commit message

参考 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>: <短句，禁止句号结尾>

<可选正文，解释 why，不是 what>
```

允许的 `<type>`：

- `feat` —— 新 skill 或新功能
- `fix` —— 修 bug
- `docs` —— 仅文档改动
- `refactor` —— 不改行为的重构
- `ci` —— CI / 校验脚本
- `chore` —— 杂项

近期参考：`e774b82 feat: add cgz-archive-session + cgz-focused-reading skills, restructure`

### PR 流程

1. Fork → 新分支 → 改动 → push。
2. 提 PR，按 `.github/PULL_REQUEST_TEMPLATE.md` 填 checklist。
3. CI 必须绿（`.github/scripts/validate_skills.py`）。
4. 维护者 review 后合并。

---

## 版本与发布（Releasing）

本仓库走 [SemVer](https://semver.org/)，工作流类似 npm workspaces：每个 plugin 在 `marketplace.json` 有自己的 `version`，`metadata.version` 是整个 marketplace 的当前版本。

**所有 bump 与 release 操作必须用 `scripts/bump.py`**，不要手改 `marketplace.json` 的 `version` 字段。

### 改动性质 → bump 幅度

| 改动 | Bump |
| --- | --- |
| 修文档错别字 / 重写不改行为 | 不 bump（直接合 main） |
| 修 bug | `--patch`（`1.1.0 → 1.1.1`） |
| 加 skill / 加规则 / 兼容性改动 | `--minor`（`1.1.0 → 1.2.0`） |
| 删 skill / 改 SKILL.md 触发关键词 / 破坏既有行为 | `--major`（`1.1.0 → 2.0.0`） |

### 一次 release 的完整流程

```bash
# 1. 看当前状态
python scripts/bump.py --status

# 2. 改完代码后,每个动过的 plugin bump 一次
python scripts/bump.py cgz-focused-discussion --minor --note "Added X feature"
python scripts/bump.py cgz-init --patch --note "Fix scan order"

# 3. 把 [Unreleased] 切成新版本段
python scripts/bump.py --release

# 4. 按脚本输出的命令提交 + 打 tag
git add CHANGELOG.md .claude-plugin/marketplace.json
git commit -m "release: vX.Y.Z"
git tag vX.Y.Z
git push origin main --tags
```

### 脚本会做的事

- 改 `marketplace.json` 里指定 plugin 的 `version`。
- 同步 `metadata.version`（取该 release 周期内最大 bump 幅度，从上一个 released 版本算起）。
- 在 `CHANGELOG.md` 的 `[Unreleased]` 段追加固定格式的 bullet：`- **<plugin>** \`<old> → <new>\` (<kind>) — <note>`。
- `--release` 把 `[Unreleased]` 内容切到 `[X.Y.Z] — YYYY-MM-DD` 段，顶部留新的空 `[Unreleased]`。
- **不会自动 commit、不会自动打 tag**，最后两步必须手动。

### 不要做的事

- **禁止手改 `marketplace.json` 的 version 字段** —— 走脚本。
- **禁止跳版本号**（`1.0.0 → 1.2.0` 没有 `1.1.0`）。
- **禁止重用 tag**（不删旧 tag 重打）。
- **禁止只改 marketplace.json 不改 CHANGELOG**，反向亦然 —— 脚本保证两边同步,人手改容易漏。
- **禁止打 tag 不切 release**（先跑 `--release` 再 `git tag`）。

---

## CI 校验

每次 push / PR 都会跑 `.github/scripts/validate_skills.py`：

- `SKILL.md` 存在
- YAML frontmatter 合法
- `name` = 父目录名，kebab-case，≤ 64 字符
- `description` ≤ 1024 字符
- `SKILL.md` 正文 ≤ 500 行

校验失败的 PR 不会被合。

---

## 不要做的事

- **禁止往 SKILL.md 里塞项目私货** —— 本仓库开源。Skill 里不得出现内部产品名、内部 docs 路径、特定团队术语。
- **禁止直接编辑别人贡献的 skill** —— 改前必须看 `git blame`，确认上下文。
- **默认单文件 skill** —— 先尝试单文件；只有当主文件因模板 / 规范变厚、或正文逼近 500 行 spec 上限时，才拆 `references/`。但 references 一旦拆出，必须沿用五大节骨架。
- **禁止只改 SKILL.md 不改 marketplace.json**（或反向）—— 描述风格必须双向一致。

---

## Spec 与工具

- 官方规范：<https://agentskills.io/specification>
- 校验工具：`skills-ref validate ./skills/<name>`（来自 [agentskills/agentskills](https://github.com/agentskills/agentskills)）
- 本仓库 CI：`python3 .github/scripts/validate_skills.py`
