---
name: cgz-init
description: "在项目里初始化 cgz 记忆架构和本地作者身份。扫描共享规则、独立记录目录与本地身份；确认作者别名后只补缺失骨架。用户说初始化 cgz、启动 cgz、让 AI 学这套、设置项目记忆，或新项目首次使用 cgz 时触发。"
---

# cgz 启动检测

把项目共享规则和每份工作副本的本地身份分开，一次初始化即可开始独立归档。不安装服务，不要求账号、Git 或外部应用。

## 入口与依据

扫描或生成前读取 [启动检测规范](references/init-spec.md)。该文件保留五大节：五原则 / 五维度 / 五心理学 / 对话严苛规则 / 语言纯化规则。

## 生成范围

```text
项目根/
├── .cgz/local.json           # 仅本工作副本的作者别名和随机 author_id
├── .gitignore               # 只补精确条目 /.cgz/local.json
├── AGENTS.md                # 共享入口；已有内容保留
└── docs/
    ├── cgz-memory.md        # 团队记录协议；已有内容保留
    ├── ai-lessons.md        # 已采纳规则的稳定入口，不是并发日志
    ├── archives/           # YYYY-MM-DD-<record_id>.md
    ├── lessons/            # YYYY-MM-DD-<record_id>.md
    └── daily/              # YYYY-MM-DD-<record_id>.md
```

每份新记录使用新的随机 `record_id`，不能只靠日期、作者别名或分支名防重名。日复盘写 `docs/daily/YYYY-MM-DD-<record_id>.md` 独立文件，不争写同一天的共享文件。共享规则与本地身份分离；不会把身份配置写进共享模板。

初始化不要求 Obsidian，不询问或生成 vault 配置。已有旧配置保留不使用。其他 skill 由用户自行安装，`cgz-init` 不生成 `.claude/skills/*` 或修改用户主目录。

## 触发与授权

- 用户明确说 `/cgz-init`、初始化 cgz、启动 cgz、设置项目记忆：视为授权补齐上列骨架；先展示简短已有 / 缺失清单，首次只确认作者别名，不逐文件重复询问。
- 只是 agent 发现缺记忆骨架：先询问是否初始化，获得确认后再执行。
- 作者别名已明确提供时无需再问。已有有效身份直接保留；异常、覆盖、权限限制或现有规则冲突必须停在相关项并询问。

## 最小流程

1. **扫描项目**。只检查项目内相关文件、既有归档约定和 Git 状态；不得自动扫描主目录或其他项目。
2. **确认身份**。首次确认作者别名；`git user.name` 只作候选，不代表认证，不取邮箱。无 Git 时直接询问。用安全随机 UUID 生成 `author_id`，按 [身份模板](assets/local.json.template) 写 `.cgz/local.json`，只在本项目 `.gitignore` 中补 `/.cgz/local.json`。
3. **补齐骨架**。共享协议用 [协议模板](assets/cgz-memory.md.template)，共享入口用 [AGENTS 模板](assets/AGENTS.md.template)，稳定教训入口用 [教训模板](assets/ai-lessons.md.template)。归档目录说明用 [归档说明模板](assets/archives-README.md.template)。仅创建缺失文件和目录；已有文件不覆盖、不搬移、不删历史。
4. **核对后收尾**。验证本地 JSON 可解析、必填字段和 UUID 有效、忽略条目精确且无重复。确认身份文件未被跟踪；已被跟踪时警告并询问，不自动删除文件或改写 Git 历史。

再次运行时，身份、协议和入口齐全则不写文件、不换 ID、不追加重复说明。不同 worktree 或工作副本分别保留自己的 `.cgz/local.json`，不写共享 Git 配置；同一作者多会话依靠每次新 `record_id` 区分。

## 收尾

回复 ≤ 12 行，包含「生成」「保留未动」「下一步」。只报告实际结果和阻塞；不能把未完成身份设置称为就绪。下一步指向独立归档 / 教训记录，不让用户先搭账号或手改业务配置。

## 禁止

- 禁止覆盖已有身份、共享规则、协议或历史记录。
- 禁止把新教训直接追加到共享 `AGENTS.md`、`ai-lessons.md` 或索引。
- 禁止改业务代码、自动提交、自动合并、后台监听或宣称已经实现同步服务。
- 禁止每次会话重跑；仅显式请求或确认初始化时执行。
