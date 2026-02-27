# Global Claude Context — Camille Larpin

## Who I Am
Solo developer, Mac. All code and docs in English. User-facing UI copy: language defined per project.

## Behavior Directives
- Default model: Sonnet. Escalate to Opus for architecture decisions or complex reasoning.
- Git: English commit messages; `git pull --rebase` before push; Claude Code handles commits.
- Storage: file-based (JSON/MD).
- Docs: succinct, rigorous, unambiguous — no accidental redundancy, archive resolved content.
- Iteration: Plan → clarify → validate → build one thing → test. Never build ahead of validation.
- Security: read-only by default; no destructive bash without explicit confirmation; secrets in n8n credentials or .env only.
- Avoid tunnel vision: when blocked or running in circles, step back — is this still the right approach?
- Be consistent: never vary terminology or format unless the difference is intentional and explicit.

## Global Knowledge — load on demand
- @~/.claude/CONTEXT_GLOBAL.md — what is true now: stack, architecture, philosophy (load when creating a new project or making an architectural or cross-project decision)
- @~/.claude/DECISIONS_GLOBAL.md — what was chosen and why: cross-project decisions (load when making an architectural or cross-project decision)
- @~/.claude/LESSONS_GLOBAL.md — what to avoid: hard-won patterns and mistakes (load when debugging or starting a build)
- @~/projects/_PROJECT_TRACKER.md — project registry (load when assessing cross-project relevance or promotion candidates)

## Skills — load on demand
@~/.claude/skills/ — load relevant skill before starting any scoped task

## Project Files
Every project has in .claude/: CONTEXT.md, DECISIONS.md, LESSONS.md, DESIGN.md, TODOS.md
All .claude/ files: project-specific only. Never duplicate global directives.
Decisions: archive when superseded → DECISIONS_GLOBAL_ARCHIVE.md. Lessons: never delete, append only.

## End-of-Session Checklist
Run at the end of every session — no exceptions:
1. Any lesson worth promoting? Flag: `→ PROMOTE: LESSONS_GLOBAL.md — [reason]`
2. Any decision that applies beyond this project? Flag: `→ PROMOTE: DECISIONS_GLOBAL.md — [reason]`
3. Did ~/.claude/ structure change (new skill, template, global file)? Update ~/.claude/README.md.
4. Is any global file approaching its size limit? Flag: `→ PRUNE: [file] — [current line count]`
   - LESSONS_GLOBAL.md: 150 lines
   - DECISIONS_GLOBAL.md: 200 lines
   - CONTEXT_GLOBAL.md: review on major stack shift
5. Did philosophy, stack, architecture principles, or project system conventions change? Update CONTEXT_GLOBAL.md.
