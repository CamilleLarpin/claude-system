# Global Claude Context — Camille Larpin

## Who I Am
Solo developer, Mac. All code and docs in English. User-facing UI copy: language defined per project.

## Behavior Directives
- Default model: Sonnet. Escalate to Opus for architecture decisions or complex reasoning.
- Git: English commit messages; `git pull --rebase` before push; Claude Code handles commits; after each milestone, propose to commit and push relevant `.claude/` (project) and `~/.claude/` changes before moving on.
- Storage: file-based (JSON/MD).
- File maintenance: never delete content — archive superseded decisions, split overlong lessons into category files.
- Docs: succinct, rigorous, unambiguous — no accidental redundancy, archive resolved content.
- Iteration: Plan → clarify → validate → build one thing → test. Never build ahead of validation.
- Security: read-only by default; no destructive bash without explicit confirmation; secrets in n8n credentials or .env only.
- Avoid tunnel vision: when blocked or running in circles, step back — is this still the right approach?
- Be consistent: never vary terminology or format unless the difference is intentional and explicit.
- Context load: check a file's load tier before adding content — prefer retrieval for rarely-needed facts.
- Transparency: when applying a principle to a decision, name it explicitly — state which rule is driving the choice.

## Global Knowledge — load on demand
- @~/.claude/CONTEXT_GLOBAL.md — what is true now: stack, architecture, philosophy (load when creating a new project or making an architectural or cross-project decision)
- @~/.claude/DECISIONS_GLOBAL.md — what was chosen and why: cross-project decisions (load when making an architectural or cross-project decision)
- @~/.claude/LESSONS_GLOBAL.md — what to avoid: hard-won patterns and mistakes (load when debugging or starting a build)
- @~/.claude/PROJECT_TRACKER.md — project registry (load when assessing cross-project relevance or promotion candidates)

## Skills — load on demand
@~/.claude/skills/ — load relevant skill before starting any scoped task

## Project Files
Every project has in .claude/: CONTEXT.md, DECISIONS.md, LESSONS.md, DESIGN.md, TODOS.md
All .claude/ files: project-specific only. Never duplicate global directives.
Decisions: archive when superseded → DECISIONS_ARCHIVE.md. Lessons: never delete — split into category files at 150 lines.

## After each milestone
0. Commit and push all dirty `.claude/` and `~/.claude/` files.
1. Update `.claude/` files (DECISIONS.md, LESSONS.md, DESIGN.md, TODOS.md) as needed.
2. Any lesson worth promoting? → `PROMOTE: LESSONS_GLOBAL.md — [reason]`
3. Any decision cross-project? → `PROMOTE: DECISIONS_GLOBAL.md — [reason]`
4. Complexity check: did this milestone meaningfully increase complexity? If yes → flag `→ REFACTOR: [component] — [reason]`
5. Did any file cross its threshold? → `SPLIT` or `ARCHIVE`
6. Did philosophy/stack/architecture change? Update CONTEXT_GLOBAL.md.
7. Did project status or load tier change? Update declarations.
8. Run `/clear` — don't carry stale state into the next milestone.
