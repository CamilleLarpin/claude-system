# Decisions — Conventions Archive

> Archived from DECISIONS_CONVENTIONS.md — established decisions no longer needing active reference
> NOT HERE: active decisions (→ DECISIONS_CONVENTIONS.md)

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

## [backlog] Backlog management philosophy
- **Decision**: every item must have a documented "why"; Now ≤ 5 active (blocked don't count), Next ≤ 5; Someday is a parking lot swept at each /prioritize; dependencies documented inline on any item that can't start until another is done
- **Rationale**: without "why", prioritization is guesswork and stale items accumulate invisibly; caps prevent overcommitment; Someday without a sweep grows unbounded; undocumented dependencies cause blocked starts with no clear reason
- **Date**: 2026-03-18
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

## [conventions] Experimental Stack section in CONTEXT_GLOBAL — separate from Technical Stack
- **Decision**: CONTEXT_GLOBAL.md has two stack sections: `## Technical Stack` (stable, changes only when real pain justifies it) and `## Experimental Stack` (tools under time-boxed evaluation — binary verdict: promote to Technical Stack or drop)
- **Rationale**: mixing stable and experimental tools in one list obscured which tools were committed vs. under evaluation; separation makes the two-zone stack principle concrete and visible
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

## [conventions] /document command — lightweight mid-session project doc save
- **Decision**: `/document` updates only the current project's `.claude/` files (CONTEXT, TODOS, DECISIONS, LESSONS, DESIGN if exists); infers all changes from the conversation; no commit, no push, no global scope. Distinct from `/end-of-session` (no promotion, no threshold checks, no tracker update).
- **Rationale**: end-of-session is too heavy when dropping a session quickly; a lightweight save prevents context loss without the full ritual; inferring from conversation avoids interrupting the user
- **Date**: 2026-03-24
- **Status**: active

## [conventions] Draft files for deferred work — `report/draft-*.md`
- **Decision**: deferred work with configuration details (pending trigger config, agent prompts, etc.) is saved as `~/.claude/report/draft-<name>.md`; the backlog task description includes the path inline
- **Rationale**: decisions made mid-session about how to build something shouldn't be lost when execution is deferred; draft is the context handoff to future self; path in task ensures discoverability at pickup
- **Date**: 2026-03-24
- **Status**: active

## [conventions] /prioritize scoring model — Impact + Effort + Alignment, max 9
- **Decision**: `/prioritize` scores every Now/Next/Later item on 3 dimensions (1–3 each): Impact (value + what it unblocks), Effort (inverse: 3=hours, 1=weeks), Alignment (fit with current phase/goals). Score = sum, max 9. Output as a single table sorted by score descending with a Signal column (`✅` aligned · `↑ promote` score ≥ 7 in Later · `↓ demote` score ≤ 4 in Now/Next) — no separate mismatch section. Someday excluded from scoring.
- **Rationale**: vibe-based prioritization drifts; scores make trade-offs auditable; consolidating score + mismatch into one Signal column is faster to scan than a ranked table + separate flags section
- **Date**: 2026-03-24
- **Status**: active

## [conventions] When two backlog items describe the same build, consolidate into one
- **Decision**: if a backlog project and a use case in an active project describe the same build (same trigger flow, same output, same team), they are one entry — tracked in BACKLOG.md with a clear `IS [UC-X] in [Project]` note; the active project TODOS.md references the backlog item as its dependency
- **Rationale**: tracking the same build in two places (Meeting Note Taker in BACKLOG + UC5 in AI Networking System TODOS) creates drift — dependency chains reference different names for the same work, priority signals diverge, and it's unclear where the authoritative spec lives
- **Date**: 2026-03-24
- **Status**: active
