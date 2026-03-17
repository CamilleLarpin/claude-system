# Claude Code Full Course — Setup Analysis
> Source: `~/projects/audio-intelligence-pipeline/data/transcripts/CLAUDE_CODE_FULL_COURSE_4_HOURS_-_Build_Sell_2026.txt`
> Analysed: 2026-03-17 — do NOT re-analyse the transcript (302KB, ~70k tokens)
> Purpose: gap analysis of Camille's Claude setup against course recommendations

---

## Already doing well

- **CLAUDE.md as system brain** — global + per-project hierarchy, exactly what the course prescribes
- **High-density structured rules** — bullets, short headings, compressed language
- **Rules at the top** — critical constraints first (primacy bias)
- **Skills directory** — load-on-demand with front-matter, body loads only on invocation
- **`@include` modular loading** — lessons split by domain, loaded only when relevant
- **Execution gate** — STOP → numbered plan → explicit approval
- **Context load tiers** — hot/warm/cool/cold declared per file
- **`~/.claude/` in private GitHub repo** — portable, versioned
- **Two-zone stack** — core stable, experiments time-boxed with binary verdict
- **Observability / cost ceiling** — defined per project

---

## Gaps / Missing

- **`/init` on inherited/existing repos** — `/init` reads an existing codebase and auto-generates a CLAUDE.md from what's actually there; distinct from project-init skill which creates new projects from scratch
  - **Scope**: narrow — only applies when opening a repo you didn't create (someone else's code, long-dormant repo, inherited codebase); project-init skill already covers new project creation ✅
  - **Pain**: opening an unfamiliar existing repo without `/init` means Claude reads files blind with no generated summary of patterns, structure, and dependencies — slower ramp-up, more assumptions

- **`.claude/agents/` subfolder** — named sub-agent specs (researcher, reviewer, QA) as `.md` files; no equivalent pattern in setup
  - **Pain**: multi-step tasks are handled by one monolithic agent carrying full context; this is slower, more expensive, and more error-prone than delegating to specialized sub-agents with scoped tools and clean context

- **Hooks (`settings.json`)** — auto-fired scripts before/after tool calls (e.g. completion chime, post-commit linting); referenced in CLAUDE.md but no hooks actually configured
  - **Pain**: quality enforcement relies entirely on Claude's behavioral compliance; there's no automated gate — formatting errors, missing steps, and bad outputs slip through without any systematic check

- **`/compact` with custom instructions** — explicit compaction with directives on what to preserve, rather than relying on auto-compaction alone
  - **Pain**: default compaction loses session-specific decisions and task state; on long builds Claude starts "forgetting" earlier choices, revisits resolved decisions, and loses track of where it was — without a directive it has no signal on what matters *(addressed: directive added to CLAUDE.md + /compact command created 2026-03-17)*

- **Status line token monitoring** — ✅ already done: `ctx:37% in:24.3k out:30.1k` configured via `statusLine` in settings.json

- **Sub-agents for parallelisation** — spawning parallel agents to process chunks simultaneously; no documented pattern despite running multi-step pipelines
  - **Pain**: tasks that could run in parallel run sequentially; a pipeline that processes 10 items one by one takes 10x longer than one that spawns 10 agents simultaneously; throughput scales linearly when it could scale flat

- **Test-verify loop in skills** — built-in verification step after task execution (automated test, QA sub-agent); not in skills
  - **Pain**: Claude produces output and stops — errors are only caught when the user reviews manually or runs a test later; the cost of a mistake is a full re-run rather than a fast correction caught at build time

- **MCP → Skill promotion rule** — try MCP first (fast setup), convert to skill (token-efficient) once validated; no decision rule documented
  - **Pain**: MCPs adopted for speed of setup stay in place permanently; no mechanism to retire them once the use case is validated; each MCP adds permanent context cost to every session whether used or not

- **`CLAUDE.local.md`** — gitignored per-workspace override for sensitive or machine-specific config; not in conventions
  - **Pain**: machine-specific or sensitive settings either end up in committed CLAUDE.md (security risk) or aren't captured at all, requiring manual re-setup each time; adds friction and inconsistency across machines

- **Git worktrees for parallel development** — multiple Claude instances on separate branches simultaneously; no documented pattern
  - **Pain**: can only work on one branch/task at a time; switching tasks means losing the current context entirely; no way to have Claude work on a fix in parallel while you review another feature

- **Reviewer sub-agent** — zero-context agent evaluating output with no prior bias; no equivalent quality gate
  - **Pain**: Claude reviews its own output with full context bias — blind spots from building the code persist into the review; it's looking for what it expected to write, not what's actually wrong; a zero-context reviewer catches what the author misses

- **`memory.md` scratch pad** — persistent cross-session notes Claude writes to; no documented use
  - **Pain**: insights, preferences, and conventions discovered in one session aren't automatically available next session unless manually encoded in CLAUDE.md; tribal knowledge is lost at /clear

---

## Could improve

- **Total loaded context cost** — global CLAUDE.md + all `@include` files likely exceeds 200–500 line cap when fully loaded; audit with `/context` and prune or move reference content to skills
- **Skill front-matter hygiene** — verify skill bodies don't load at startup; only the YAML header should be in active context
- **Move rituals from CLAUDE.md to skills** — end-of-session steps, commit conventions partially already skills, but some prose remains in CLAUDE.md
- **Plan mode explicitly, not just behaviorally** — execution gate is a prose rule relying on Claude compliance; course recommends switching to plan mode explicitly for any build >2 steps touching external systems
- **MCP token cost criteria** — a poorly written MCP can consume 20%+ of context before sending a message; no documented evaluation criteria before adopting an MCP
- **Periodic CLAUDE.md pruning** — lessons are never deleted (correct), but CLAUDE.md itself should be actively pruned of stale/redundant rules; treat it like technical debt

---

## Course highlights (key ideas worth referencing)

- **Primacy/recency bias**: most important rules go first AND last in CLAUDE.md — Claude weights these positions more
- **Skills vs rules**: rules stay in CLAUDE.md; repeatable tasks become skills (load only on invocation)
- **MCP token cost**: evaluate token footprint of any MCP before adopting — a single bloated MCP can consume 20%+ of context window at session start
- **Plan mode**: explicitly switch to plan mode for multi-step builds rather than relying on prose instructions alone
- **`/compact` discipline**: use with explicit instructions on what to preserve (e.g. "keep all decisions and current task context") rather than accepting the default summary
- **Sub-agents**: spawn parallel agents per chunk/task to multiply throughput; use scoped tool access to limit blast radius
- **Reviewer pattern**: a fresh zero-context sub-agent as quality gate catches things the main agent misses due to context bias
- **Hooks**: powerful for enforcing post-tool discipline (lint on save, chime on completion, log every tool call)
