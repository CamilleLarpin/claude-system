---
description: Start a work session — load project context and give a focused briefing
---

# /start — Start Session

### 1. Establish date

```bash
date +%Y-%m-%d
```

### 2. Identify project

Detect from `pwd`. If not inside `~/projects/<slug>/`, ask: "Which project are we working on today?"

### 3. Load context

- `~/.claude/PROJECT_TRACKER.md`
- `.claude/CONTEXT.md`
- `.claude/TODOS.md`

### 4. Briefing

Output in this format:
- **Project**: name · status · stack
- **Next milestone**: one line
- **Next actions**: bullet list from TODOS.md
- **Blockers**: if any
- "What do you want to work on today?"

Offer to load `DECISIONS.md` or `LESSONS.md` on request.
