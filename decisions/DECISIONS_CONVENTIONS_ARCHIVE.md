# Decisions — Conventions Archive

> Archived from DECISIONS_CONVENTIONS.md when file crossed 100-line threshold.
> Status: all entries below are **active** unless noted — archived for space, not superseded.

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
- **Decision**: every `.claude/` file declares its load tier in its header block (`> Load when:`) · tier reflects when the file should be read; updated when scope changes
- **Rationale**: makes context load cost visible at the point of decision; prevents token bloat in frequently-loaded files; applies "no hidden assumptions" principle — tier is self-declared, not inferred
- **Date**: 2026-03-03
- **Status**: active

## [conventions] BACKLOG.md as unified project pipeline and task registry
- **Decision**: single `~/.claude/BACKLOG.md` holds all pre-active projects and cross-project tasks in two sections; promotes to PROJECT_TRACKER when active development starts
- **Rationale**: TODOS.md and a separate backlog would split related load context with no payoff for a solo developer; one file handles both concerns under one load trigger
- **Date**: 2026-03-13
- **Status**: active

## [conventions] Global context files always load alongside their project counterparts
- **Decision**: `DECISIONS_GLOBAL.md` loads alongside project `DECISIONS.md`; `LESSONS_GLOBAL.md` index loads alongside project `LESSONS.md` + relevant category files for current task domain. Both triggers preserved: alongside project files AND on their original standalone triggers.
- **Rationale**: DECISIONS_GLOBAL applies to all projects by definition — there is no case where a project DECISIONS.md is loaded without DECISIONS_GLOBAL being relevant. Same logic for LESSONS_GLOBAL.
- **Date**: 2026-03-17
- **Status**: active
