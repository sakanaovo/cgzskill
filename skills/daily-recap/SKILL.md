---
name: daily-recap
description: "Generate an Obsidian-friendly daily recap (Markdown with YAML frontmatter and [[wikilinks]]) from today's archives, lesson log, and current session. Use when the user says today recap, 今天复盘, 收尾今天, daily recap, 日报, or when a new day begins with unreviewed archives from yesterday. Writes to the obsidian_vault path configured in AGENTS.md."
---

# 每日复盘

按天聚合当日上下文，写一份 Obsidian 友好的 `Daily/YYYY-MM-DD.md`。

跟 `archive-session` 的区别：archive 是**单次**会话归档（每发生一次写一份），daily-recap 是**按天**聚合（每天一份，串当天所有归档）。

## 入口与依据

判定依据全部写在 [复盘规范](references/recap-spec.md)。该文件分五大节：

1. **五原则** —— 只写当天事实、不重新分析、不补方案、跨会话只读落地文件、用户未确认不写。
2. **五维度** —— 写入前自检：触发 / 数据源 / 输出位置 / 链接合法 / 语言。
3. **五心理学** —— 失败模式：重复分析 / 完整性焦虑 / 过度拼凑 / 链接编造 / 时间错乱。
4. **对话严苛规则** —— 句式、单一询问句、12 行收尾。
5. **语言纯化规则** —— 中文段落不夹裸英文，YAML 字段 / wikilink / 英文 section 名保留原文。

写复盘前必须读取该规范。

## 触发

显式触发：

- `/daily-recap`
- 用户说：「今天复盘」「收尾今天」「today recap」「daily recap」「日报」

自检触发（agent 主动建议，仍需用户确认）：

- 当天首次启动，检测到 `docs/archives/` 里有昨天的归档但 vault 里没有对应日期的 Daily note。
- 当前会话已经写过多份归档，但还没有按天聚合。

主动建议句式：

```text
今天已经有 N 份归档落地，还没写日复盘。要现在生成 Daily/YYYY-MM-DD.md 吗？
```

## 前置条件

`AGENTS.md` 里必须有 cgz 配置段，含 `obsidian_vault` 路径：

```text
## cgz 配置

- Obsidian vault: `~/Obsidian/cgz`（daily-recap 写到此目录下的 `Daily/YYYY-MM-DD.md`）
```

未配置时不写文件，直接提示：

```text
AGENTS.md 缺 cgz 配置段（obsidian_vault）。先跑 /cgz-init 补上，再回来跑 daily-recap。
```

## 数据源（只读落地文件，禁止凭记忆）

按顺序读：

1. `docs/archives/` 里日期匹配今天的文件
2. `docs/ai-lessons.md` 当天追加的条目
3. 当前会话上下文（仅用于补充未落盘的当下决策）

跨会话信息**只能**从前两项读，禁止假设 agent 记得早些会话里说过的话。

## 输出格式

写入 `${obsidian_vault}/Daily/YYYY-MM-DD.md`：

```markdown
---
date: YYYY-MM-DD
tags: [daily, recap, cgz]
related:
  - "[[YYYY-MM-DD-yesterday]]"
---

# YYYY-MM-DD

## 主要决策

- ……（来自 archives 的 Decisions / 用户已确认的结论）

## 改过的文件

- [[path/to/file]]
- ……

## 新增 lessons

- ……（docs/ai-lessons.md 当天追加的条目摘要，禁止改写规则原文）

## 未决问题

- ……（archives 里 Open questions / Risks）

## 明天先看

- [[next-archive]]
- ……
```

字段约束：

- `date` 必须是绝对日期 `YYYY-MM-DD`。
- `related` 的 wikilink 只能指向 vault 里**已存在**的 daily note，禁止编未来文件。
- 「改过的文件」列项目相对路径，用 wikilink 包裹（Obsidian 自动解析）。
- 「新增 lessons」只摘要、不重写；详细规则原文留在 `docs/ai-lessons.md`。

## 收尾回复

写完后回复 ≤ 12 行：

```text
日复盘已写。

文件：
- ${obsidian_vault}/Daily/YYYY-MM-DD.md

收录：
- 归档 N 份
- 新 lessons M 条
- 未决问题 K 条

下一步：
- 在 Obsidian 里打开核对，必要时手改
```

禁止在收尾里展开新分析、补建议、给明天的方案。

## 禁止

- 禁止在 vault 外写文件。
- 禁止覆盖已存在的 Daily note（已存在时询问：覆盖 / 追加 / 取消）。
- 禁止从记忆里编归档内容，所有事实必须来自落地文件。
- 禁止编 wikilink 指向不存在的文件。
- 禁止把当天没发生的事写进复盘。
- 禁止把 `archive-session` 已经写过的细节重抄一遍，复盘是索引不是重复。
