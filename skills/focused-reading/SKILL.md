---
name: focused-reading
description: "Read documents, code, PRs, issues, logs, webpages, screenshots, exported chats, or long context while staying on the user's stated question. Use when the user asks to read, review, understand, summarize, inspect, compare, or extract from materials without drifting into broad tutorials, unrelated findings, implementation plans, or unsolicited recommendations."
---

# 专注阅读

读取材料时保持单线收敛:只读和用户问题相关的内容,只输出能推进当前问题的结论。

详细规范见 [阅读输出规范](references/reading-spec.md)。处理长文档、PR、日志、网页、图文材料或需要固定输出结构时,先读取该规范。

## 核心原则

- 先锚定用户问题,再决定读什么。
- 不把“读一下”变成完整教程、全量重写、架构评审或实现计划。
- 不主动扩大阅读范围。需要额外文件时,说明为什么需要,再读。
- 区分原文事实、推断、不确定点。
- 旁支发现最多列 1-3 条,放在最后,不展开。
- 用户问判断题时先给 Yes/No;问位置时先给路径/行号;问摘要时先给 3-5 条核心点。

## 最小流程

内部先确认:

```text
用户要我读什么?
用户真正问的问题是什么?
这次输出需要:结论 / 摘要 / 风险 / 对比 / 提取 / 定位?
哪些材料是必须读的?哪些只是可能相关?
```

如果材料或问题不明确,只问一个澄清问题。

## 范围控制

| 用户请求 | 读取范围 |
| --- | --- |
| “看这个文档讲了什么” | 只读该文档,输出核心结论 |
| “这段 PR 有没有问题” | 读 diff + 相关测试/调用点,不扫全仓库 |
| “帮我理解上下文” | 读用户指定上下文 + 最近相关 docs,不扩到全项目 |
| “从图文/网页里提取信息” | 提取可见事实,需要细则时读 reference |
| “找某个答案/字段” | 优先 grep/search,直接返回位置和答案 |

长材料先扫目录、标题、索引、首尾段、代码入口;只有命中相关问题时再深入。

## 默认输出

```markdown
**结论**
[直接回答用户问题]

**依据**
- `path:line`: [关键事实]

**不确定**
- [缺失材料或待验证点]

**附带发现**
- [最多 1-3 条,没有就省略]
```

## 什么时候建议归档

阅读本身只负责回答当前问题。出现以下情况时,停止继续扩展阅读,建议切换到 `archive-session`:

- 用户说“归档 / 收尾 / 给下次看 / 保存上下文 / handoff”。
- 本轮读了多个文档、网页、PR、日志或长聊天记录。
- 输出里已经包含多个路径、结论、未决问题或后续入口。
- 图文/网页素材后续可能复用。
- 用户的问题已经回答完,但阅读结果明显会影响后续工作。
- 对话开始从“读材料”变成“讨论方案/做决策/安排下一步”。

只有用户确认,或用户已经明确要求归档时,才写文件。
