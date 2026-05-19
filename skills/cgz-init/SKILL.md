---
name: cgz-init
description: "在项目里初始化 cgz 记忆架构。扫描 AGENTS.md、docs/ai-lessons.md、docs/archives/ 是否就位；缺失时先询问用户再生成骨架。用户说初始化 cgz、启动 cgz、让 AI 学这套、设置项目记忆，或新项目首次使用 cgz 时触发。"
---

# cgz 启动检测

把 cgz 这套「项目记忆」架构在新项目里落地。一次性操作：扫描 → 询问 → 生成。

## 入口与依据

判定依据全部写在 [启动检测规范](references/init-spec.md)。该文件分五大节：

1. **五原则** —— 先扫后生成、先问后写、已存在不覆盖、只生成骨架、一次性操作。
2. **五维度** —— 写入前自检：触发 / 扫描 / 询问 / 安全 / 收尾。
3. **五心理学** —— 失败模式：全包冲动 / 默认偏好 / 自动化幻觉 / 完整性焦虑 / 越界冲动。
4. **对话严苛规则** —— 句式、单一询问句、12 行收尾。
5. **语言纯化规则** —— 中文不夹裸英文，英文模板保持纯英文，路径保留原文。

扫描或生成前必须读取该规范。

## 这套记忆体系包含什么

```
项目根/
├── AGENTS.md                 # 长期规则:cgz section + 6 步教训循环 + cgz 配置
├── CLAUDE.md                 # (可选) Claude Code 项目的 bridge
├── docs/
│   ├── ai-lessons.md         # 教训日志:错误 → 纠正 → 规则
│   └── archives/             # cgz-archive-session 归档目录
```

**AGENTS.md 里必须有 `## cgz 配置` 段**，记录 `obsidian_vault` 路径（`cgz-daily-recap` skill 读取）。空值表示禁用每日复盘。

`cgz-focused-discussion` / `cgz-focused-reading` / `cgz-archive-session` / `cgz-daily-recap` 等 skill 由用户通过 `/plugin install` 单独装到 `.claude/skills/`，**不在 cgz-init 的生成范围内**。

## 触发

显式触发：

- `/cgz-init`
- 用户说：「初始化 cgz」「启动 cgz」「set up cgz memory」「让 AI 学这套」「bootstrap memory」

自检触发（agent 主动建议，仍需用户确认）：

- 项目根没有 `AGENTS.md` 也没有 `docs/ai-lessons.md`，但用户已经在用三个 cgz skill 之一。
- 用户首次让 cgz skill 做归档，但项目里没有 `docs/archives/`。

主动建议句式：

```text
这个项目还没建 cgz 记忆体系（缺 AGENTS.md / docs/ai-lessons.md / docs/archives/）。要现在初始化吗？
```

## 最小流程

1. **扫描**。列出已存在 / 缺失项，展示给用户：

   ```text
   已存在：
   - AGENTS.md（缺 cgz section）

   缺失：
   - docs/ai-lessons.md
   - docs/archives/

   配置：
   - obsidian_vault: 未设置
   ```

2. **询问**。两个单一问句，顺序问：

   - 「缺失的 N 项要全部生成，还是挑选？」
   - 「Obsidian vault 路径填什么？（留空 = 禁用 cgz-daily-recap）」

3. **生成**。已存在项一律不覆盖：

   - `AGENTS.md` 缺失 → 从 `assets/AGENTS.md.template` 生成，把用户给的 vault 路径写入 `## cgz 配置` 段。
   - `AGENTS.md` 已存在但没有 cgz section → 追加 cgz section（含配置段）到末尾，禁止重写。
   - `AGENTS.md` 已存在且有 cgz section 但缺 `obsidian_vault` 配置 → 询问后只追加配置段。
   - `docs/ai-lessons.md` 缺失 → 从 `assets/ai-lessons.md.template` 生成。
   - `docs/archives/` 缺失 → `mkdir -p docs/archives/` 并放一个最小 `README.md`。

4. **收尾**。回复 ≤ 12 行，固定结构：

   ```text
   cgz 记忆体系已就位。

   生成：
   - ……

   保留未动：
   - ……

   下一步：
   - 在 AGENTS.md 里把「项目专属规则」段补上
   - 出错 / 被纠正时按 6 步循环记录到 docs/ai-lessons.md
   ```

## 禁止

- 禁止擅自写文件，必须先问。
- 禁止覆盖已存在文件，只补缺失项或追加 cgz section。
- 禁止生成 `.claude/skills/*`，那是 `/plugin install` 的职责。
- 禁止动业务代码。
- 禁止每次会话重跑，只在显式触发或自检条件全部满足时跑。
- 禁止把模板里的「示例规则」当成项目规则强加。
