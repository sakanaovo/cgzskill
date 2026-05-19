# cgzskill

> Claude Code 对话纪律 + skill 工厂套件。
>
> **focused-discussion** 让 Claude 不再一问就甩 ABCD 方案、不再把一次对话越聊越散。
> **build-skill** 用采访的方式,5 分钟帮你造一个属于你自己的 skill。
>
> *后续会扩展更多 skill,统一放在 `skills/` 目录下。*

---

## 为什么有这个仓库

如果你用过 Claude Code 超过一周,大概率遇到过这两件事:

1. **你问一句,Claude 答出来 4 个方案 + 利弊表格 + 工时估**。挑完一个,下一句它又开始新的 ABCD。一次对话被切碎成 10 个子话题,**最后什么都没拍板**。

2. **你想把"我每次都这么干"的工作流写成 skill**,提高效率。但落笔时永远卡在"这个 skill 该在什么时候触发""反模式怎么写才不空洞""description 该写多详细"……纠结到放弃。

这两件事不是你的问题,是**没有人告诉过 Claude 该怎么聊天、也没有人告诉你该怎么写 skill**。

这个仓库解决这两件事:

- `focused-discussion` —— 一份给 Claude 的对话纪律。
- `build-skill` —— 一个会**采访你**的 skill,问完 6 个问题,自动生成另一个 skill。

---

## 仓库结构

```
cgzskill/
├── README.md
├── LICENSE
└── skills/
    ├── focused-discussion/
    │   └── SKILL.md
    └── build-skill/
        └── SKILL.md
```

每个 skill 是 `skills/` 下的独立子文件夹,**复制对应文件夹就能用**,互不依赖(`build-skill` 在设计上引用了 `focused-discussion`,建议一起装)。

---

## 当前包含的 skill

### 1. `focused-discussion` —— Claude 对话纪律

**做什么**:强制 Claude 在每次回答时遵守"先闭合上一个问题,再开下一个"。禁止一问就甩 ABCD、禁止推理过程外放、禁止用户没问就主动塞工时/优先级/推荐。

**什么时候触发**:
- 用户在 PR / 产品 / 架构 / UX 上提了具体问题
- 用户说「跑偏了」「聚焦」「先停一下」「先看反馈」
- 显式触发:`/focused-discussion`

**适合谁**:
- 跟 Claude 做产品讨论 / 架构辩论 / 方案对齐,被甩 ABCD 烦过的人
- 自己也容易跟着 Claude 一起发散,聊到最后什么都没决定的人

### 2. `build-skill` —— 采访式 skill 生成器

**做什么**:用 6 个问题采访你 —— 触发场景 / 真实失败案例 / 反模式 / 正确做法 / 输出格式 / 命名 —— 然后生成一份可以直接放进 `.claude/skills/` 的 SKILL.md。

**关键设计**:严格遵守 `focused-discussion` 的对话纪律,**一次只问一个问题,前一个没答清楚不开下一个**。

**什么时候触发**:
- 你有一套反复用的工作流想做成 skill,但不知道怎么写
- 显式触发:`/build-skill [一句话描述你想做的 skill]`

**适合谁**:
- 想把自己的方法论沉淀成可复用工具的人
- 已经手写过几个 skill 但效果一般,不知道为什么的人

---

## 安装

把对应文件夹复制进你项目的 `.claude/skills/`:

```bash
git clone https://github.com/sakanaovo/cgzskill.git
cd cgzskill

# 一次性安装全部 skill
cp -r skills/* /path/to/your-project/.claude/skills/

# 或者只挑你要的
cp -r skills/focused-discussion /path/to/your-project/.claude/skills/
cp -r skills/build-skill /path/to/your-project/.claude/skills/
```

**两个 skill 强烈建议一起装** —— `build-skill` 内部引用 `focused-discussion`,单独装会留断引用。

---

## 怎么用

### 让 Claude 自动遵守对话纪律

`focused-discussion` 装好后**不需要每次显式调用**。当你跟 Claude 讨论 PR / 产品 / 架构 / UX 问题,或者说"跑偏了 / 聚焦 / 先停一下"时,Claude 会自动激活。

也可以手动唤起:

```
/focused-discussion
```

### 5 分钟造一个自己的 skill

```
/build-skill 帮我做代码评审的固定问法
```

Claude 会进入采访模式,一个问题一个问题问你:

1. 这个 skill 你希望什么时候触发?
2. 上一次你没用这个 skill 时,具体出了什么问题?
3. Claude 通常会做错什么?
4. 你希望 Claude 具体怎么做?
5. 输出长什么样?
6. 叫什么名字?

答完之后会先**回放确认**,你说对了才会写文件。

---

## 来自一次真实的失败

`focused-discussion` 不是凭空设计的。它来自一次真实的对话:

> 用户问了一个**具体的 UX 问题**,我做完 MVP 之后,**一次对话被我切碎成 10 个子话题** —— 登录方式、账户隔离、容器架构、扩展选型、二维码时效、备注规则、接口超时、监控告警 …… 每个子话题我都甩 A/B/C/D 方案 + 利弊表格 + 工时估。
>
> 用户花精力挑选 / 挑战,挑完又冒出新分支。**最后用户说**:
>
> > 「我觉得这样不好 一直推理 要跑偏 给出方案 又要花时间想 慢慢的就聊跑题了」

根本问题不是回答错了,是**每个回答都被做成了"新决策点"**,而不是"闭合上一个问题"。

`focused-discussion` 把这件事写成了硬规则。

而 `build-skill` 解决另一件事 —— **大多数人不是写不出 skill,是不知道一个"好用"的 skill 长什么样**。这个 skill 不教你 markdown 语法,它**采访你**。问完 6 件事,SKILL.md 自动出来,直接能用。

---

## License

MIT

---

## 贡献

欢迎 issue / PR。如果你用 `build-skill` 造出了自己觉得不错的 skill,也欢迎来分享。
