# Global Claude Context — Camille Larpin

## Who I Am
Solo developer, Mac. All code and docs in English. User-facing UI copy: language defined per project.

## Behavior Directives

### Defaults
- Model: Sonnet. Escalate to Opus for architecture or complex reasoning.
- Git: English commits; `git pull --rebase` before push; Claude Code handles commits.
- Storage: file-based (JSON/MD).
- Security: read-only by default; no destructive bash without confirmation; secrets in n8n credentials or .env only; identify all public interfaces (bots, webhooks, APIs) and add access controls.

### Content & docs
- File maintenance: never delete — archive superseded decisions, split overlong lessons.
- Docs: succinct, rigorous, unambiguous — no redundancy, archive resolved content.
- Context load: check load tier before adding — prefer retrieval for rarely-needed facts.
- Consistency: never vary terminology or format unless intentional and explicit.
- Compaction: when context is compacted (auto or manual `/compact`), preserve all decisions made this session, current task state, and active constraints — compress everything else.

### Build discipline
- Iteration: Plan → clarify → validate → build one thing → test. Never build ahead of validation.
- Execution gate: STOP when the task has >2 steps or touches an external system. Output a numbered plan. Wait for explicit approval of that specific plan before proceeding.
- Tunnel vision: when blocked or running in circles, step back — is this still the right approach?
- Transparency: when applying a principle to a decision, name it explicitly.

## Global Knowledge — load on demand
- @~/.claude/CONTEXT_GLOBAL.md — what is true now: stack, architecture, philosophy (load when creating a new project or making an architectural or cross-project decision)
- @~/.claude/DECISIONS_GLOBAL.md — what was chosen and why: cross-project decisions (load alongside project DECISIONS.md; load when making an architectural or cross-project decision)
- @~/.claude/LESSONS_GLOBAL.md — what to avoid: hard-won patterns and mistakes (load the index alongside project LESSONS.md + relevant category files for current task domain; load when debugging or starting a build)
- @~/.claude/PROJECT_TRACKER.md — project registry (load when assessing cross-project relevance or promotion candidates)
- @~/.claude/BACKLOG.md — project pipeline and tasks (load when selecting or prioritizing projects, or when a cross-project task or stack decision arises)

## Skills — load on demand
@~/.claude/skills/ — load relevant skill before starting any scoped task

## Project Files
Every project has in .claude/: CONTEXT.md, DECISIONS.md, LESSONS.md, DESIGN.md, TODOS.md
All .claude/ files: project-specific only. Never duplicate global directives.
Decisions: archive when superseded → DECISIONS_ARCHIVE.md. Lessons: split by load context at 150 lines — one file = one reason Claude loads it.

## End of session
Run `/end-of-session` — then `/commit-push` — then `/clear`.
