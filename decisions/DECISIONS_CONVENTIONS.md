# Decisions — Conventions

> Load when: commands · backlog work · project setup · session rituals.
> NOT HERE: build decisions (→ DECISIONS_BUILD.md), infra decisions (→ DECISIONS_INFRA.md).
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

## [conventions] Project vs task distinction
- **Decision**: a **task** completes in one session, has a binary outcome (done/not done), needs no context to resume, and has no repo. A **project** is multi-session, has phases, accumulates decisions, and needs `.claude/` context to pick back up.
- **Rationale**: without a clear rule, the boundary drifts — tasks get over-engineered into projects (wasted setup) or projects get under-documented (lost context). The one-session rule is the clearest practical gate.
- **Date**: 2026-03-18
- **Status**: active

## [conventions] Priority vocabulary — Now / Next / Later / Someday
- **Decision**: all projects and tasks in PROJECT_TRACKER and BACKLOG use a shared 4-level priority vocabulary: Now (active attention), Next (starts when a slot opens), Later (important, not urgent), Someday (nice-to-have, no commitment). Each entry carries an inline priority log (max 2 entries, oldest dropped when a third is added): `  - YYYY-MM-DD [Old] → [New]: [reason]`. /overview shows Now + Next only; Later and Someday hidden by default.
- **Rationale**: time-based vocabulary (This Month/This Quarter) conflates planning with importance; unified vocabulary across both files enables direct comparison between active (TRACKER) and pre-active (BACKLOG) items; priority log provides lightweight history without a separate file; /overview limited to Now + Next keeps daily view actionable
- **Date**: 2026-03-18
- **Status**: active

## [backlog] Done tasks archived to TASKS_DONE.md, not kept in BACKLOG.md
- **Decision**: completed tasks are moved to `~/.claude/projects-tracking/TASKS_DONE.md` and removed from BACKLOG.md entirely — not kept as `[x]` entries
- **Rationale**: done tasks in BACKLOG.md consume tokens on every load for zero value; a separate file is never loaded unless explicitly needed, same principle as project Archive
- **Date**: 2026-03-18
- **Status**: active

## [conventions] `@path` in CLAUDE.md auto-loads — use plain paths for on-demand files
- **Decision**: use plain paths (`` `~/.claude/file.md` ``) in CLAUDE.md and index files (LESSONS_GLOBAL, DECISIONS_GLOBAL) for files that should load on demand. Reserve `@path` only for files that must always be loaded (e.g. project CLAUDE.md → `@~/.claude/CLAUDE.md`).
- **Rationale**: `@path` syntax in Claude Code auto-includes the file immediately — it does not mean "available if needed". Using `@` in index files cascaded into loading all 9 lesson files and 3 decision files on every command, regardless of relevance. Plain paths let Claude read them via Read tool when actually needed.
- **Date**: 2026-03-19
- **Status**: active

## [conventions] /prioritize display format — 4 blocks, projects + tasks differentiated
- **Decision**: `/prioritize` displays in 4 blocks (Now/Next/Later/Someday); within each block: projects bold with the reason they're at that priority; tasks italic at the end with the pain point they solve; blocked projects stay in their priority block with ⚠️ inline — no separate Blocked section
- **Rationale**: separating blocked into its own section hid priority; mixing tasks and projects with equal weight obscured what matters; showing "why" next to each item makes prioritization decisions auditable at a glance
- **Date**: 2026-03-19
- **Status**: active

## [conventions] Agent files — ~/.claude/agents/ global, .claude/agents/ per-project; invoked via paired slash command
- **Decision**: global agents live in `~/.claude/agents/`, project agents in `.claude/agents/`; all new projects scaffold an empty `.claude/agents/` via project-init. Custom agents are NOT registered as subagent_type — invoke via a paired `~/.claude/commands/<name>.md` slash command that spawns a general-purpose agent with the agent's prompt embedded.
- **Rationale**: subagent_type only accepts built-in types (tested 2026-03-19 — "Agent type not found"); slash command pattern is reliable and one-step; agent `.md` file = source of truth for instructions, command file = invocation layer
- **Date**: 2026-03-19
- **Status**: active

## [conventions] Cross-project relationship types — blocking dependency vs shared infrastructure
- **Decision**: two distinct relationship types, documented in different places:
  - **Blocking dependency** (`⚠️ Blocked by: [project] — [what]` / `⚡ Unblocks: [project] — [what]`): lives in TODOS.md of *both* projects (blocked: which phase is waiting; blocking: which task unblocks another project) + PROJECT_TRACKER.md on both projects (`Blocker:` on the blocked project's entry, `⚡ Unblocks:` note on the blocking project's entry — prioritization signal).
  - **Shared infrastructure/tool**: lives in `CONTEXT_GLOBAL.md` only — not in PROJECT_TRACKER, not in individual project CONTEXT.md. Shared infra is an architectural fact about the stack, not a project coordination concern.
- **Rationale**: blocking dependencies affect whether a project can proceed and how to prioritize it — relevant on both sides. Shared infrastructure doesn't affect project execution or priority — it belongs in the global stack description, not duplicated across project files.
- **Date**: 2026-03-19
- **Status**: active

## [conventions] Experimental Stack section in CONTEXT_GLOBAL — separate from Technical Stack
- **Decision**: CONTEXT_GLOBAL.md has two stack sections: `## Technical Stack` (stable, changes only when real pain justifies it) and `## Experimental Stack` (tools under time-boxed evaluation — binary verdict: promote to Technical Stack or drop)
- **Rationale**: mixing stable and experimental tools in one list obscured which tools were committed vs. under evaluation; separation makes the two-zone stack principle concrete and visible; current experimental: OpenClaw, MLflow
- **Date**: 2026-03-20
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
- **Status**: active

## [conventions] PROJECT_TRACKER vs BACKLOG — distinct load triggers
- **Decision**: PROJECT_TRACKER loads when: active project status · cross-project dependency. BACKLOG loads when: new project idea · next project selection · cross-project dependency. Both load for cross-project dependency.
- **Rationale**: both had identical triggers ("assessing cross-project relevance") — unclear when to load one vs the other; TRACKER = active projects, BACKLOG = future/candidate projects; distinct contexts
- **Date**: 2026-03-20
- **Status**: active

## [conventions] Commands section in CLAUDE.md — slash command → skill/agent mapping
- **Decision**: CLAUDE.md has a Commands section documenting the pattern: `/command` → Skill tool → `skills/<name>/SKILL.md` or `agents/<name>.md`
- **Rationale**: three "on demand" mechanisms (context reading, skill invocation, agent invocation) were conflated; Commands section makes the distinction explicit and answers "what is a command vs a skill vs a file to load"
- **Date**: 2026-03-20
- **Status**: active

## [conventions] File split/rename discipline — update callers, no index-of-indexes
- **Decision**: before renaming or splitting any file: grep for its name across `~/.claude/`; update all `@`-references and plain-path references in commands and skills. When splitting a file: update callers to point to the new files directly — never leave a thin index at the old path as a redirect.
- **Rationale**: `@`-references break silently on rename (no error, missing context at runtime); an index-of-indexes adds an indirection layer with no load-tier benefit and makes the dependency harder to trace
- **Date**: 2026-03-20
- **Status**: active

## [backlog] Backlog management philosophy
- **Decision**: every item must have a documented "why"; Now ≤ 5 active (blocked don't count), Next ≤ 5; Someday is a parking lot swept at each /prioritize; dependencies documented inline on any item that can't start until another is done
- **Rationale**: without "why", prioritization is guesswork and stale items accumulate invisibly; caps prevent overcommitment; Someday without a sweep grows unbounded; undocumented dependencies cause blocked starts with no clear reason
- **Date**: 2026-03-18
- **Status**: active
