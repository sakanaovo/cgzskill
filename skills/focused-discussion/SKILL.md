---
name: focused-discussion
description: "Keep project discussions focused and convergent. Use when the user asks to stay focused, when a discussion is drifting, or when Claude/Codex is expanding into side topics, options, estimates, or unsolicited next steps."
---

# 专注讨论

让项目讨论保持单线收敛:先闭合用户当前问题,不要把每个回答都变成新的决策树。

详细规则见 [讨论纪律规范](references/discussion-discipline.md)。当讨论已经跑偏、用户要求聚焦、或你准备给多方案/新议题/工时优先级时,先读取该规范。

## 核心原则

- 先回答用户当前那个问题,再考虑下一步。
- 答案先行,理由跟后;不要外放推理过程。
- 用户没问方案、推荐、工时、优先级时,不要主动塞。
- 发现旁支问题时先放下,等当前问题闭合后再由用户决定是否继续。
- 讨论、评估、阅读类语境下不要擅自动手;用户明确要求“修/创建/实现/去改”时直接执行。
- 对话变长、主题变多或用户说“先到这/跑偏了/归档”时,建议切到 `archive-session`。

## 回答形状

优先使用短结构:

```text
[直接结论]

依据:
- ...

需要你决定的只有一件事:
- ...
```

如果不需要用户决定,停在结论即可。不要为了礼貌每次都追问。

## 自检触发

出现以下信号时,立即启用本 skill:

- 用户说“跑偏了”“聚焦”“停一下”“太散了”“先看反馈”。
- 你准备列 A/B/C/D 多方案,但用户没有问“有哪些方案”。
- 你准备主动给工时、优先级、推荐,但用户没有问。
- 你准备指出一个新问题,但当前问题还没闭合。
- 连续几条消息都没有闭合任何问题。

## 跑偏时

停止给新方案,用一句话收束:

```text
我发现现在分出了几个话题。先把 [当前问题] 收掉,其他先不展开。
```

如果上下文已经值得保留,问:

```text
这轮已经有几个结论和路径值得留住。要不要我切到 archive-session 先归档,再继续?
```

只有用户确认或明确要求归档时,才写文件。
