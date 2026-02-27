# ~/.claude/ — System Overview
This file is your orientation guide to the ~/.claude/ system.
Read it when returning after a break, onboarding to a new machine, or when the system feels unclear.
Claude maintains this file but never loads it.

## Structure
~/.claude/
├── CLAUDE.md
├── CONTEXT_GLOBAL.md
├── DECISIONS_GLOBAL.md
├── DECISIONS_GLOBAL_ARCHIVE.md
├── LESSONS_GLOBAL.md
├── README.md
├── templates/
└── skills/

## Reader Map
| File | Read by | When |
|------|---------|------|
| CLAUDE.md | Claude | Every session |
| CONTEXT_GLOBAL.md | Claude | On demand — new projects, architectural or cross-project decisions |
| DECISIONS_GLOBAL.md | Claude | On demand — architectural or cross-project decisions |
| LESSONS_GLOBAL.md | Claude | On demand — debugging, starting a build |
| _PROJECT_TRACKER.md | Claude | On demand — cross-project relevance check |
| skills/ | Claude | On demand — before any scoped task |
| README.md | Human | Never auto-loaded |

## Maintenance Triggers
| File | Update when |
|------|-------------|
| CLAUDE.md | Behavior directives, process, or instructions change |
| CONTEXT_GLOBAL.md | Philosophy, stack, architecture principles, or project system conventions change |
| DECISIONS_GLOBAL.md | New cross-project decision made; prune at 200 lines → DECISIONS_GLOBAL_ARCHIVE.md |
| LESSONS_GLOBAL.md | New lesson promoted; prune at 150 lines |
| templates/ | Any structural change to .claude/ file conventions |
| skills/ | Domain added, removed, or boundary shifted |
| README.md | High-level structure or system principles change |

## Promotion Rules
Project → Global when a lesson or decision is:
- Applicable to 2+ projects, or likely to recur
- Represents a corrected mistake worth preventing globally

Claude flags: `→ PROMOTE: [file] — [reason]`. Camille decides.
Claude runs promotion check at end of every session — no exceptions.

## Skills Contract
Each skill owns one exclusive domain.
If two skills can answer the same question, one is wrong.
When adding a skill: check for overlap first — consolidate or sharpen boundary before creating.

## System Principles

### Context Engineering
- **Three-tier hierarchy**: always-on (CLAUDE.md) → on-demand (skills, globals) → never (archives). Keep always-on tiny.
- **Specificity beats volume**: one precise constraint beats three vague ones. Vague instructions dilute each other.
- **Recency bias**: Claude weights tokens near end of context more heavily. Put critical constraints last.
- **Negative space**: "what I don't want" sections are often more effective than positive instructions.
- **Prune ruthlessly, archive don't delete**: stale content dilutes active content. Archived → never loaded.
- **Structure for skipping**: headers and tags save attention, not tokens.
- **Test your context**: periodically ask Claude to reflect back what it understands — gaps reveal what's missing or buried.

### System Maintenance
- Hard Rules exist to force behaviors that directives alone don't enforce. Use sparingly.
- When a rule feels important enough to repeat, escalate it to CLAUDE.md.
- Templates diverge from usage silently — update templates immediately when conventions change.
- Be consistent: never vary terminology or format unless the difference is intentional and explicit.
