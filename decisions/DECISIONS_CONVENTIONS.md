# Decisions — Conventions

> Load when: commands, backlog work, project setup, session rituals.
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

## [conventions] DECISIONS_GLOBAL split into index + category files by load context
- **Decision**: DECISIONS_GLOBAL.md is an index only; actual decisions live in category files split by load context: DECISIONS_CONVENTIONS.md (commands, backlog, project setup), DECISIONS_BUILD.md (build, AI agents, data), DECISIONS_INFRA.md (server, credentials, deployment)
- **Rationale**: single file caused full-registry load every time any decision was needed; split by load context (not topic) means each command/task loads only the relevant slice; mirrors the proven LESSONS_GLOBAL pattern; DECISIONS_GLOBAL index stays tiny and cheap to load
- **Date**: 2026-03-18
- **Status**: active

## [conventions] Single post-milestone checklist ordered by signal strength
- **Decision**: one checklist runs after each milestone (not split by session boundary); steps ordered by signal strength — promotions first (highest cognitive value), mechanical checks last
- **Rationale**: splitting into milestone + session checklists created a coordination problem — promotions require live context, which is cleared before end-of-session; collapsing removes deferred state; ordering by signal strength prevents attention decay on high-value steps
- **Date**: 2026-03-04
- **Status**: active

## [conventions] Session ritual commands over CLAUDE.md prose
- **Decision**: user-triggered rituals (`/start`, `/end-of-session`, `/commit-push`) live in `~/.claude/commands/` as dedicated command files, not in CLAUDE.md
- **Rationale**: keeps CLAUDE.md lean (always-loaded context); command files are only loaded on invocation; user owns the trigger — Claude doesn't remind or propose; conventions for authoring commands documented in `~/.claude/commands/CONVENTIONS.md`
- **Date**: 2026-03-09
- **Status**: active

## [conventions] Rule/Guideline/Note type tags on all lesson entries
- **Decision**: every lesson entry is tagged with a type in its header: `## [category] · Rule|Guideline|Note · Title`. Rule = must follow (violating breaks things); Guideline = should follow unless justified; Note = informational. Applies to global files and all project LESSONS.md files.
- **Rationale**: gives Claude a signal to weight lessons correctly — a Rule must be applied unconditionally, a Guideline requires judgment, a Note is context. Promotion gate updated: only Rules and Guidelines are promoted to global; Notes stay in project files.
- **Date**: 2026-03-10
- **Status**: active

## [conventions] Load tier declarations in .claude/ file headers
- **Decision**: every `.claude/` file declares its load tier (hot/warm/cool/cold) in its header block; tier reflects current project phase and is updated when status changes
- **Rationale**: makes context load cost visible at the point of decision; prevents token bloat in frequently-loaded files; applies "no hidden assumptions" principle — tier is self-declared, not inferred
- **Date**: 2026-03-03
- **Status**: active

## [conventions] Global context files always load alongside their project counterparts
- **Decision**: `DECISIONS_GLOBAL.md` loads alongside project `DECISIONS.md`; `LESSONS_GLOBAL.md` index loads alongside project `LESSONS.md` + relevant category files for current task domain. Both triggers preserved: alongside project files AND on their original standalone triggers.
- **Rationale**: DECISIONS_GLOBAL applies to all projects by definition — there is no case where a project DECISIONS.md is loaded without DECISIONS_GLOBAL being relevant. Same logic for LESSONS_GLOBAL.
- **Date**: 2026-03-17
- **Status**: active

## [conventions] Project vs task distinction
- **Decision**: a **task** completes in one session, has a binary outcome (done/not done), needs no context to resume, and has no repo. A **project** is multi-session, has phases, accumulates decisions, and needs `.claude/` context to pick back up.
- **Rationale**: without a clear rule, the boundary drifts — tasks get over-engineered into projects (wasted setup) or projects get under-documented (lost context). The one-session rule is the clearest practical gate.
- **Date**: 2026-03-18
- **Status**: active

## [conventions] BACKLOG.md as unified project pipeline and task registry
- **Decision**: single `~/.claude/BACKLOG.md` holds all pre-active projects and cross-project tasks in two sections; promotes to PROJECT_TRACKER when active development starts
- **Rationale**: TODOS.md and a separate backlog would split related load context with no payoff for a solo developer; one file handles both concerns under one load trigger
- **Date**: 2026-03-13
- **Status**: active

## [conventions] Priority vocabulary — Now / Next / Later / Someday
- **Decision**: all projects and tasks in PROJECT_TRACKER and BACKLOG use a shared 4-level priority vocabulary: Now (active attention), Next (starts when a slot opens), Later (important, not urgent), Someday (nice-to-have, no commitment). Each entry carries an inline priority log (max 2 entries, oldest dropped when a third is added): `  - YYYY-MM-DD [Old] → [New]: [reason]`. /overview shows Now + Next only; Later and Someday hidden by default.
- **Rationale**: time-based vocabulary (This Month/This Quarter) conflates planning with importance; unified vocabulary across both files enables direct comparison between active (TRACKER) and pre-active (BACKLOG) items; priority log provides lightweight history without a separate file; /overview limited to Now + Next keeps daily view actionable
- **Date**: 2026-03-18
- **Status**: active

## [backlog] Done tasks archived to TASKS_DONE.md, not kept in BACKLOG.md
- **Decision**: completed tasks are moved to `~/.claude/TASKS_DONE.md` and removed from BACKLOG.md entirely — not kept as `[x]` entries
- **Rationale**: done tasks in BACKLOG.md consume tokens on every load for zero value; a separate file is never loaded unless explicitly needed, same principle as project Archive
- **Date**: 2026-03-18
- **Status**: active

## [conventions] `@path` in CLAUDE.md auto-loads — use plain paths for on-demand files
- **Decision**: use plain paths (`` `~/.claude/file.md` ``) in CLAUDE.md and index files (LESSONS_GLOBAL, DECISIONS_GLOBAL) for files that should load on demand. Reserve `@path` only for files that must always be loaded (e.g. project CLAUDE.md → `@~/.claude/CLAUDE.md`).
- **Rationale**: `@path` syntax in Claude Code auto-includes the file immediately — it does not mean "available if needed". Using `@` in index files cascaded into loading all 9 lesson files and 3 decision files on every command, regardless of relevance. Plain paths let Claude read them via Read tool when actually needed.
- **Date**: 2026-03-19
- **Status**: active

## [backlog] Backlog management philosophy
- **Decision**: every item must have a documented "why"; Now ≤ 5 active (blocked don't count), Next ≤ 5; Someday is a parking lot swept at each /prioritize; dependencies documented inline on any item that can't start until another is done
- **Rationale**: without "why", prioritization is guesswork and stale items accumulate invisibly; caps prevent overcommitment; Someday without a sweep grows unbounded; undocumented dependencies cause blocked starts with no clear reason
- **Date**: 2026-03-18
- **Status**: active
