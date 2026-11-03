# cgzskill: Project memory for AI assistants and coding tools

English · [简体中文](README.zh-CN.md) · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [Team acceptance checklist](docs/team-acceptance.md)

> **Important update: 2.0 → 2.1** changes how document language is selected and saved, and makes English the repository homepage. Existing users should update the complete skills and run init to check missing language settings. **Your identity, historical records, and team language remain intact.** Read the [upgrade impact and checklist](#upgrading-from-20-to-21) before upgrading; the published v2.0.0 release does not include these changes.

**Focused reading, focused discussion, and file-based project memory for AI assistants and coding tools that support Agent Skills.**

cgzskill packages five reusable AI workflows: initialize project memory, keep a conversation on topic, read only what answers the question, archive a session for handoff, and produce a daily recap. Claude Code and Codex are installation examples, not the only intended hosts. The Claude Code marketplace offers the full `cgz-all` bundle or individual skills; other hosts require adaptation to their own skill specifications and have not all been tested.

The current `main` contains **2.1.0**, adding a saved document-language preference: choose Simplified Chinese (`zh-CN`), English (`en`), or another explicitly named language during initialization. Skills follow the [Agent Skills specification](https://agentskills.io/specification). Their instructions and reference documents remain primarily in Chinese; generated document prose follows the language rules below, rather than the language of those instructions. This is configurable output, not a claim that every language or host has been tested.

## Ask your AI to install it

Copy this prompt into an agent with access to your development environment. It installs the current `main`; the language feature requires a revision containing the 2.1.0 changes.

```text
Install cgzskill from the current main branch of https://github.com/sakanaovo/cgzskill. Verify the checked-out revision and its available features before claiming the new language configuration is supported. Read its README, identify my AI assistant or coding tool, check whether it supports Agent Skills, and confirm the supported installation scope, such as project-level or user-level, with me. Use the documented examples for Claude Code or Codex; for other hosts, follow their official specifications without guessing paths or commands. Use the supported installation method and preserve complete skill directories, including references and assets; do not overwrite existing files or install duplicate skills. Invoke cgz-init through the host's actual skill entry, confirm my author alias if needed, and ask which language I want for future documents: Simplified Chinese (zh-CN), English (en), or another language I name explicitly. Save that preference as document_language in .cgz/local.json while preserving any existing author alias and UUID. Keep the project's shared-file language separate; if there is no established convention, confirm it once during initialization. Preserve existing project files and identity. Verify separately that the host loaded the skills and that initialization succeeded. If you lack local access, give me the steps instead of claiming completion. Do not bypass safety controls, run unreviewed code, or request credentials.
```

## What it helps with

- **Keep context between sessions:** save confirmed decisions, relevant files, unresolved questions, and the next place to start in project Markdown.
- **Make reading and discussion more focused:** answer the current question without turning a code review, log inspection, or product discussion into an unsolicited implementation plan.
- **Prepare a team handoff:** preserve authors, sources, scope, and verification status so another person or agent can pick up the work.
- **Close the day:** summarize that day's archives and lessons without repeating the analysis or requiring an external notes app.

Project memory comes from an agent reading these files in a later session. The skills do not train the model or provide automatic self-learning.

## The five skills

The commands below assume the `cgz-all` bundle is installed in Claude Code.

| Skill | Use it when | Bundle command |
| --- | --- | --- |
| `cgz-init` | Set up missing project memory files, a local author identity, and a document-language preference without overwriting existing content. | `/cgz-all:cgz-init` |
| `cgz-focused-reading` | Read documentation, source code, pull requests, logs, screenshots, or long context to answer one question. | `/cgz-all:cgz-focused-reading` |
| `cgz-focused-discussion` | Keep a discussion on its current decision and avoid unsolicited options or new topics. | `/cgz-all:cgz-focused-discussion` |
| `cgz-archive-session` | Save one session's facts, decisions, and open questions for the next session or a team handoff. | `/cgz-all:cgz-archive-session` |
| `cgz-daily-recap` | Aggregate one day's saved records and verifiable current-session context into a project-local recap. | `/cgz-all:cgz-daily-recap` |

Reading and discussion work without initialization. Archive and recap also include a minimal identity and record protocol when the project has not been initialized.

## Install

### Example: Claude Code marketplace

Run these commands inside Claude Code, then follow the installation prompts:

```text
/plugin marketplace add sakanaovo/cgzskill
/plugin install cgz-all@cgzskill
```

To install just one skill instead:

```text
/plugin install cgz-focused-reading@cgzskill
```

Plugin commands use `/<plugin>:<skill>`. The individual reading plugin therefore exposes `/cgz-focused-reading:cgz-focused-reading`; the individual init plugin exposes `/cgz-init:cgz-init`. Type `/` to check the commands available in your session. See the official [Claude Code installation guide](https://code.claude.com/docs/en/discover-plugins).

Choose the bundle or the individual plugins you need; installing both creates redundant copies of the same skills.

### Example: Codex and standalone skills

Clone this repository, then copy **complete skill directories**, including `SKILL.md`, `references/`, `agents/`, and any `assets/`:

```bash
git clone https://github.com/sakanaovo/cgzskill.git
cd cgzskill
mkdir -p ~/.agents/skills
cp -Rn skills/cgz-* ~/.agents/skills/
```

This is a fresh-install example. `-n` preserves existing files; it does not upgrade an existing installation. Review and back up an installed directory before deliberately replacing it with a new version.

Codex supports user-level `~/.agents/skills/` and project-level `.agents/skills/`. Use `/skills` to find a skill or mention it explicitly, for example `$cgz-init`. See the official [Codex skills guide](https://developers.openai.com/codex/skills/).

For standalone Claude Code skills, use `~/.claude/skills/` or the project's `.claude/skills/` instead. Other Agent Skills hosts may need their own loading configuration. Do not paste only `SKILL.md` into `AGENTS.md`: that omits the referenced rules and templates. Follow each host's official directory and invocation rules. Supporting the skill format does not by itself establish compatibility; host-specific behavior still needs validation in the environment you use.

## First project: initialize, work, archive, recap

1. Open your project in the host and invoke `cgz-init`. On first use, confirm an author alias and a document language: `zh-CN`, `en`, or another language you explicitly name. A Git username is only a suggested alias; Git and an email address are not required. If shared project files have no established language, confirm their language separately during initialization.
2. Use focused reading or discussion for the work in front of you. For example: “Read this PR and explain the cause of the failing test. Stay within that question.”
3. Invoke `cgz-archive-session` when you finish a useful unit of work: “Archive this session for the next person, keeping confirmed decisions and unresolved questions.”
4. Invoke `cgz-daily-recap` at the end of the day: “Create today's recap from the project's saved records.”

An explicit archive or recap request authorizes that record. If the agent merely notices that an archive or recap would help, it must ask before writing one.

Initialization fills in missing parts of this structure and preserves existing files:

```text
your-project/
├── .cgz/local.json       # Local author identity and document_language; Git-ignored
├── AGENTS.md            # Shared entry point for project instructions
└── docs/
    ├── cgz-memory.md    # Shared record protocol
    ├── ai-lessons.md    # Stable, accepted rules
    ├── archives/       # Session records
    ├── lessons/        # Candidate lessons, pending review
    └── daily/          # Daily recaps
```

The only added ignore pattern is `/.cgz/local.json`. Initialization stays within the listed project files; it does not scan your home directory, edit application code, change global Git settings, or store secrets.

## Choose your document language

Initialization records your explicit choice in `.cgz/local.json` as `document_language`. Use `zh-CN` for Simplified Chinese, `en` for English, or a clear language name or tag for another language, such as `日本語` or `ja`. “Other” is a prompt to name a language, not a language value to save.

For new personal records, such as session archives, candidate lessons, and daily recaps, resolve the language in this order:

1. An explicit language instruction in the current request.
2. Your saved `document_language` in `.cgz/local.json`.
3. An established project document-language convention.
4. If none exists, ask before creating the first document.

Do not infer a preference from your operating system locale, account, location, Git identity, or the language of a single message. “Write this recap in English” applies to that recap only. “Use English for my documents from now on” updates the saved preference. If the request does not make the scope clear, ask whether it is a one-time choice or a lasting preference before changing the setting.

**Shared files follow the project, not an individual preference.** `AGENTS.md`, `docs/cgz-memory.md`, and `docs/ai-lessons.md` retain the project's established language. If none exists, initialization confirms the shared-file language once and records that convention in the shared protocol. A personal preference does not silently change it.

Adding a language preference to an existing installation keeps the existing `author_alias` and `author_id`; it must not create a new identity. The preference applies to future prose only. Do not translate or rewrite historical records, accepted rules, or source quotations. Keep paths, filenames, commands, metadata field names, UUIDs, source IDs, and schema values such as `pending` and `unverified` unchanged. Existing shared rules still require their usual explicit approval or team review to change.

## How team records work

- **Local identity:** each working copy has its own random `author_id` and author alias. These label sources; they do not authenticate a person or grant permissions.
- **Independent records:** archives, candidate lessons, and recaps use `docs/archives/YYYY-MM-DD-<record_id>.md`, `docs/lessons/YYYY-MM-DD-<record_id>.md`, and `docs/daily/YYYY-MM-DD-<record_id>.md`, with a new random UUID for each new record. Dates, author names, and branches are not uniqueness guarantees.
- **Traceable facts:** records retain authors, source IDs, dates and time zones, scope, verification status, and branch or baseline commit when available.
- **Preserved history:** original records are not rewritten or deleted to deduplicate them. A correction is a new record that refers to the old ID.
- **Stable shared rules:** routine writes do not append to a shared index, `AGENTS.md`, or `docs/ai-lessons.md`. Promoting a candidate lesson into an accepted rule requires explicit confirmation or team review through a PR.
- **Careful summaries:** equivalent facts in the same scope can be combined with all sources retained. Complementary facts stay distinct; conflicts in the same scope remain `pending`. Repeated sources are not counted twice, and daily recaps are not recursively treated as new evidence. Reuse also requires the same actual output language, saved as `document_language` in each new record; changing language creates an independent summary and preserves the old one.

These are file-handling instructions executed by the agent. They do not provide an account system, background service, synchronization service, or automatic Git merging. Independent filenames reduce shared-file contention; they do not guarantee conflict-free collaboration.

## Upgrading from 2.0 to 2.1

### What changes

- **Personal output language:** `.cgz/local.json` gains `document_language`. New personal documents use the current request first, then your saved preference, then the project convention; ask if none exists. A one-time request does not change the saved default.
- **Separate team language:** `docs/cgz-memory.md` records `project_document_language`. Shared instructions and accepted rules keep the project language; a personal preference cannot override it.
- **Traceable new records:** each new record stores its actual output `document_language`. Recap reuse requires the same language as well as the same sources, author, date, and scope, with no new facts. A different language creates a separate summary without changing the old one or counting it as new evidence.
- **English homepage:** this does not require shared project documents to become English or change your Chinese or other personal output choice. The complete Chinese guide is now [README.zh-CN.md](README.zh-CN.md); [README.en.md](README.en.md) remains a compatibility entry.

### What existing users should do

1. Review and preserve local customizations, then update **complete skill directories**, including references and assets, through your host's supported update method. Copying only `SKILL.md`, or using the fresh-install `cp -Rn` example, does not upgrade an existing installation.
2. Verify that the host loaded the updated skills, then invoke init through its actual entry: `/cgz-all:cgz-init` for the Claude Code bundle, `/cgz-init:cgz-init` for the individual plugin, or `$cgz-init` / the skill picker in Codex. For other hosts, follow their own invocation rules.
3. Let init check for missing language settings. An old `.cgz/local.json` without the language field is still a valid identity: add the missing field after confirmation, retaining the author alias, UUID, and other fields. Correct existing settings are preserved without asking again. Confirm a shared language only if the project has no established convention. If existing language or team rules conflict, resolve that conflict explicitly rather than silently replacing them.
4. Check the local preference and shared protocol separately. Existing records are **not translated, moved, or migrated**; old records are not backfilled with guessed language metadata. Paths, schema fields, IDs, source quotations, and accepted rules remain intact. Changed preferences affect future documents only.

**Version and verification status at this documentation update (2026-11-03):** `main` version files are **2.1.0**. Check [Releases](https://github.com/sakanaovo/cgzskill/releases) for the latest published stable version; version files alone do not establish a tag or release. The published [v2.0.0 release](https://github.com/sakanaovo/cgzskill/releases/tag/v2.0.0) does not include this language feature; no `v2.1.0` tag or GitHub Release has been created as of this check. Installing the existing release therefore differs from installing current `main`; the old release is not replaced. All 33 tooling/configuration/template contract tests and the five-skill validator pass, but these checks are **not multilingual or multi-host end-to-end tests**. See the [manual acceptance checklist](docs/team-acceptance.md).

The naming changes, independent UUID records, and removal of the Obsidian dependency below happened in **1.x → 2.0**, not in this 2.0 → 2.1 update.

## Upgrading from 1.x to 2.0

- Four skill and plugin names now have the `cgz-` prefix: `focused-discussion`, `focused-reading`, `archive-session`, and `daily-recap`. Update old installation entries and command references to their names shown above. `cgz-init` keeps its name.
- `cgz-all` installs all five skills together. Review old installed plugins before choosing the bundle so both versions are not loaded at once.
- Daily recaps now write ordinary Markdown to the project's `docs/daily/`. Core workflows no longer ask for an Obsidian vault or write into one. Existing vault configuration is preserved but not used; Obsidian integration has not been validated.
- Existing identities, rules, and historical records remain in place. There is no automatic migration or cleanup. New records use the independent UUID format; an old shared-file archive convention needs confirmation before switching new writes to an independent directory.

See [CHANGELOG.md](CHANGELOG.md) for release details.

## Repository and validation

Each skill has a `SKILL.md` entry point and a `references/` document with its detailed rules. `cgz-init/assets/` contains the project templates, and `agents/openai.yaml` supplies host metadata. The marketplace manifest is [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).

Run the repository checks with Python and PyYAML installed:

```bash
python .github/scripts/validate_skills.py
python -m unittest discover -s tests -v
```

The tooling and contract tests check repository content and helper behavior; they do not execute the skills inside Claude Code or Codex. Real-host multi-user and multilingual scenarios have not been run, so the test suite is not evidence of end-to-end team compatibility or support for every language.

For the workflow design, see [the architecture notes](docs/ai-self-evolution-architecture.md). Contributions and issue reports are welcome; read [CONTRIBUTING.md](CONTRIBUTING.md) for naming, structure, and release conventions.

## License

[MIT](LICENSE)
