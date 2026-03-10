---
description: Start a work session - load project context and give a focused briefing
---

# /start — Start Session

## Instructions

### 1. Establish date

Run `date +%Y-%m-%d` to get today's date.

### 2. Identify project

Detect from the current working directory (`pwd`). If not inside a `~/projects/<slug>/` directory, ask: "Which project are we working on today?"

### 3. Load context

Read in order:
- `~/.claude/PROJECT_TRACKER.md` — status, stack, blockers, next milestone
- `.claude/CONTEXT.md` — current state and architecture
- `.claude/TODOS.md` — active milestones, next actions, blocked items

### 4. Present briefing

Give a concise briefing:
- **Project**: name, status, stack
- **Next milestone**: what we're working toward
- **Open todos**: immediate next actions
- **Blockers**: anything blocking progress
- **Ask**: "What do you want to work on today?"

Keep it tight — one short paragraph or a few bullet points. Offer to load DECISIONS.md or LESSONS.md on request.

### 5. Load relevant global context on demand

Only load if the session touches these areas:
- Architectural or cross-project decision → `~/.claude/DECISIONS_GLOBAL.md`
- Debugging or starting a build → `~/.claude/lessons/LESSONS_*.md` (correct category)
- New project or stack change → `~/.claude/CONTEXT_GLOBAL.md`
