# Decisions — Conventions

> Load when: commands · backlog work · project setup · session rituals
> NOT HERE: build decisions (→ DECISIONS_BUILD.md), infra decisions (→ DECISIONS_INFRA.md)
> Archive at 100 lines → DECISIONS_CONVENTIONS_ARCHIVE.md

---

## Format
```
## [category] Decision title
- **Decision**: what was chosen
- **Rationale**: why — include alternatives considered
- **Date**: YYYY-MM-DD
- **Status**: active | superseded by [title] | archived
```

---

## [conventions] `@path` in CLAUDE.md auto-loads — use plain paths for on-demand files
- **Decision**: use plain paths (`` `~/.claude/file.md` ``) in CLAUDE.md and index files (LESSONS_GLOBAL, DECISIONS_GLOBAL) for files that should load on demand. Reserve `@path` only for files that must always be loaded (e.g. project CLAUDE.md → `@~/.claude/CLAUDE.md`).
- **Rationale**: `@path` syntax in Claude Code auto-includes the file immediately — it does not mean "available if needed". Using `@` in index files cascaded into loading all 9 lesson files and 3 decision files on every command, regardless of relevance. Plain paths let Claude read them via Read tool when actually needed.
- **Date**: 2026-03-19
- **Status**: active

## [conventions] Cross-project relationship types — blocking dependency vs shared infrastructure
- **Decision**: two distinct relationship types, documented in different places:
  - **Blocking dependency** (`⚠️ Blocked by: [project] — [what]` / `⚡ Unblocks: [project] — [what]`): lives in TODOS.md of *both* projects (blocked: which phase is waiting; blocking: which task unblocks another project) + PROJECT_TRACKER.md on both projects (`Blocker:` on the blocked project's entry, `⚡ Unblocks:` note on the blocking project's entry — prioritization signal).
  - **Shared infrastructure/tool**: lives in `CONTEXT_GLOBAL.md` only — not in PROJECT_TRACKER, not in individual project CONTEXT.md. Shared infra is an architectural fact about the stack, not a project coordination concern.
- **Rationale**: blocking dependencies affect whether a project can proceed and how to prioritize it — relevant on both sides. Shared infrastructure doesn't affect project execution or priority — it belongs in the global stack description, not duplicated across project files.
- **Date**: 2026-03-19
- **Status**: active

## [conventions] Writing convention — punctuation as semantic operators in setup files
- **Decision**: every `.claude/` setup file follows a fixed punctuation convention: `—` (em-dash) = structural separator (label → content); `·` = inline list items; `→` = sequence or pointer; `;` = two independent conditions in one bullet; `-` = compound words only. No trailing period on bullets. Capital first word per bullet; lowercase after `—` or `·`.
- **Rationale**: inconsistent punctuation forces re-parsing on every read; semantic chars carry logic without token cost; consistent format is faster to parse and reduces ambiguity; full reference in `skills/review-setup/SKILL.md`
- **Date**: 2026-03-20
- **Status**: active

## [conventions] CONTEXT_GLOBAL load trigger — planning/deciding, not every session
- **Decision**: CONTEXT_GLOBAL.md loads when: planning · deciding · starting new work. Not on every session start. "Starting new work" = no approved plan to execute yet.
- **Rationale**: "starting a session" = auto-load, violates on-demand principle; real failure mode (decisions without stack knowledge) is covered by "planning · deciding"; executing an approved plan does not need CONTEXT_GLOBAL
- **Date**: 2026-03-20
- **Status**: superseded by [conventions] CONTEXT_GLOBAL always-loaded via @

## [conventions] CONTEXT_GLOBAL always-loaded via @
- **Decision**: CONTEXT_GLOBAL.md is auto-loaded every session via `@~/.claude/CONTEXT_GLOBAL.md` in CLAUDE.md — same tier as CLAUDE.md itself. Must be kept minimal — every line costs every session.
- **Rationale**: any build or architecture decision risks cross-project incoherence without global stack visibility — not just planning sessions but any session involving a significant decision. The "load when planning" trigger was too narrow. File must stay tight: no operational detail (→ INFRA.md), no project-specific state (→ project CONTEXT.md).
- **Date**: 2026-04-28
- **Status**: active

## [conventions] File split/rename discipline — update callers, no index-of-indexes
- **Decision**: before renaming or splitting any file: grep for its name across `~/.claude/`; update all `@`-references and plain-path references in commands and skills. When splitting a file: update callers to point to the new files directly — never leave a thin index at the old path as a redirect.
- **Rationale**: `@`-references break silently on rename (no error, missing context at runtime); an index-of-indexes adds an indirection layer with no load-tier benefit and makes the dependency harder to trace
- **Date**: 2026-03-20
- **Status**: active

## [conventions] Git workflow — always branch before changes; pull before start and before push
- **Decision**: before making any changes in a git repo: (1) `git pull --rebase`; (2) create a feature branch — never commit directly to main. `git pull --rebase` again before pushing. Claude Code handles commits and push.
- **Rationale**: parallel Claude sessions (multiple terminals) can conflict on the same branch; branching isolates each session's working tree. Pull before starting ensures the branch forks from up-to-date main. Rule is unconditional — Claude cannot detect parallel sessions, so "always branch" is the only reliable form.
- **Date**: 2026-03-25
- **Status**: active

## [conventions] loguru as standard logging library for Python pipeline modules
- **Decision**: use `loguru` in all Python pipeline modules (`src/`) — no `print()` in pipeline code
- **Rationale**: `print()` produces plain text with no timestamp or level — unusable for observability in production (Prefect, cron, GCP). `loguru` gives structured logs (INFO/WARNING/ERROR + timestamp) with zero configuration. Consistent across all Bronze/Silver/Gold modules.
- **Date**: 2026-04-01
- **Status**: active

## [conventions] CONTEXT.md = reality snapshot — fixed section structure
- **Decision**: every project's CONTEXT.md answers one question: "what does this system look like right now?" Fixed sections: Purpose (1 sentence) · Architecture (components + deploy status: ✅/🔵/⚫) · Functionalities (what works end-to-end ✅ / partial 🔵 / not built ⚫) · Entry Points (commands, URLs, webhooks, cron) · Data (what exists, where — omit if not data-heavy) · Known Gaps (2–3 bullets delta vs DESIGN.md). Goals → DESIGN.md · Decisions → DECISIONS.md · Next actions → TODOS.md. Updated at every `/end-of-session`. Template: `~/.claude/templates/CONTEXT.template.md`
- **Rationale**: CONTEXT.md had become a catch-all mixing goals, design, stack decisions, and state — making it unreliable for answering "what's live right now." Strict section contract forces separation of concerns; Architecture (structural) and Functionalities (behavioral) are distinct axes that together answer the "what's built" question without ambiguity.
- **Date**: 2026-04-01
- **Status**: active

## [conventions] ~/.claude/plans/ — temporal implementation plans
- **Decision**: implementation plans too detailed for a backlog task but not permanent enough to be a skill or decision live in `~/.claude/plans/plan-<name>.md`; delete the file once the plan is executed; path referenced inline in the backlog task
- **Rationale**: draft files (`report/draft-*.md`) are for deferred config/prompts; decisions files are permanent; plans are temporary working docs that should be discoverable until executed then discarded; a dedicated folder with clear naming keeps them findable without polluting permanent files
- **Date**: 2026-04-28
- **Status**: active

## [conventions] references/ folder — on-demand lookup for tools, concepts, and patterns
- **Decision**: `~/.claude/references/` stores deep reference docs on specific tools, concepts, and patterns — one file per subject, retrieved by name when needed. Generic name retained intentionally: accommodates both tools (NanoClaw, OneCLI) and concepts/patterns (git worktrees). Registered in CLAUDE.md Global Knowledge with load condition: `load when: working with or evaluating a specific tool — retrieve the relevant file by name`.
- **Rationale**: CONTEXT_GLOBAL.md carries summary-level stack info; references/ provides depth without polluting always-loaded context. Not a catch-all — each file must be a distinct, retrievable subject. Reports (analysis outputs, research) live in reports/ instead.
- **Date**: 2026-04-28
- **Status**: active
