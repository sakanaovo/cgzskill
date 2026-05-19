# PR Checklist

## 类型

- [ ] 新 skill
- [ ] 修改已有 skill
- [ ] 文档 / CI / 其他

## 改动说明

<!-- 一句话：改了什么、为什么。why 比 what 重要。 -->

## 新 skill 必须勾全（仅新 skill 适用）

- [ ] 目录在 `skills/<skill-name>/`，`<skill-name>` 是 kebab-case
- [ ] `SKILL.md` 的 `name` 字段 = 父目录名
- [ ] `description` 含触发关键词，≤ 1024 字符
- [ ] `SKILL.md` 正文 ≤ 500 行
- [ ] `references/<spec>.md` 走五大节骨架（五原则 / 五维度 / 五心理学 / 对话严苛规则 / 语言纯化规则）
- [ ] `agents/openai.yaml` 存在，三个字段完整（`display_name` / `short_description` / `default_prompt`）
- [ ] `.claude-plugin/marketplace.json` 已加一条 plugin entry
- [ ] marketplace plugin description 与 SKILL.md 风格一致（禁止 / 必须 / 立刻；不用「优先 / 尽量」）
- [ ] `CHANGELOG.md` 的 `Unreleased` 段已加条目

## 修改已有 skill 必须勾全（仅修改适用）

- [ ] `SKILL.md` 与 `references/*.md` 行为约束没有互相矛盾
- [ ] 描述风格（marketplace / SKILL.md / references）三处一致
- [ ] `marketplace.json` 中对应 plugin 的 `version` 已按 SemVer bump
- [ ] `CHANGELOG.md` 的 `Unreleased` 段已加条目

## 通用

- [ ] CI 绿（`.github/workflows/validate-skills.yml`）
- [ ] 改了 `AGENTS.md`（如果用了）的同时也改了 `CLAUDE.md` —— 两份必须同步
- [ ] 没有提交内部产品名、内部 docs 路径、个人配置

## 关联 issue

<!-- Closes #X 或 Refs #X -->
