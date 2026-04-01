# Global Claude Context — Camille Larpin

> Load tier: hot — auto-loaded every session · add only what is needed in every session · everything else belongs in a warm/cold file

## Who I Am
Solo developer, Mac. All code and docs in English. User-facing UI copy: language defined per project.

## Behavior Directives

### Defaults
- Model: Sonnet. Escalate to Opus for architecture or complex reasoning.
- Git: English commits; `git pull --rebase` before starting work and before push; create a feature branch before making changes — never commit directly to main; Claude Code handles commits-push.
- Storage: file-based (JSON/MD).
- Security: read-only by default; no destructive bash without confirmation; secrets in n8n credentials or .env only; identify all public interfaces (bots, webhooks, APIs) and add access controls.

### Content & docs
- File maintenance: never delete — archive superseded or resolved content; split overlong content; before renaming or splitting a file: `grep -r "<filename>" ~/.claude/` — update all callers before proceeding.
- Docs: succinct, rigorous, unambiguous — no redundancy.
- Context load: check load tier before adding — prefer retrieval for rarely-needed facts.
- Consistency: never vary terminology or format unless intentional and explicit.
- Writing convention: `—` separator · `·` list items · `→` sequence · `;` two clauses · no trailing `.` on bullets · full ref: `skills/review-setup/SKILL.md`
- Compaction: when context is compacted (auto or manual `/compact`), preserve all decisions made this session, current task state, and active constraints — compress everything else.

### Build discipline
- Iteration: Plan → clarify → validate → build one thing → test. Never build ahead of validation. Never silently skip the test step — name it.
- Execution gate: STOP when the task has >2 steps or touches an external system. Output a numbered plan. Wait for explicit approval of that specific plan before proceeding.
- Tunnel vision: Estimate execution time before starting; at 2× estimate, step back and decompose — smallest testable next step?
- Transparency: when applying a principle to a decision, name it explicitly.

## Global Knowledge — load on demand (read file when trigger applies, do not auto-load)
- `@~/.claude/CONTEXT_GLOBAL.md` — what is true now: stack, live services, architecture, philosophy · load when: planning · deciding · starting new work
- `~/.claude/DECISIONS_GLOBAL.md` — cross-project decisions index · load when: starting a build · touching server/infra · backlog or project-setup work · architectural decision
- `~/.claude/LESSONS_GLOBAL.md` — lessons index · load alongside project LESSONS.md + only relevant category files · load when: debugging or starting a build 
- `~/.claude/projects-tracking/PROJECT_TRACKER.md` (alias: **project-tracker**) — project registry · load when: active project status · cross-project dependency
- `~/.claude/projects-tracking/BACKLOG.md` (alias: **backlog**) — project pipeline and tasks · load when: new project idea · next project selection · cross-project dependency

## Skills — load on demand
`~/.claude/skills/` — load relevant skill before starting any scoped task

## Agents
`~/.claude/agents/` — global sub-agents (bias-free quality gates, parallel tasks) or per-project: `.claude/agents/`. 
Invoke via paired slash command (e.g. `/review`), not by subagent_type name.

## Commands
`/command` → Skill tool → `skills/<name>/SKILL.md` or `agents/<name>.md`

## Project Files
Every project: `.claude/` with CONTEXT.md, DECISIONS.md, LESSONS.md, DESIGN.md, TODOS.md
Project-specific only — never duplicate global directives.

## End of session
Suggest `/end-of-session` after milestones, significant decisions, or long sessions.
