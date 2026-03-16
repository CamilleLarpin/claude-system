---
description: Run post-milestone checks — update docs, promote lessons, flag complexity
---

# /end-of-session — End of Session Checklist

Work through each step in order. Perform the action, don't just list it.

**1. Update project `.claude/` files** — reflect work done this session in `DECISIONS.md`, `LESSONS.md`, `DESIGN.md`, `TODOS.md`.

**2. Promote lessons** — if any lesson applies beyond this project, add it to the correct `~/.claude/lessons/LESSONS_*.md` and output: `PROMOTE: LESSONS_GLOBAL.md — [reason]`

**3. Promote decisions** — if any decision applies cross-project, add it to `~/.claude/DECISIONS_GLOBAL.md` and output: `PROMOTE: DECISIONS_GLOBAL.md — [reason]`

**4. Complexity check** — if this milestone meaningfully increased complexity, output: `→ REFACTOR: [component] — [reason]`

**5. Threshold check** — if any `.claude/` file crossed its threshold (LESSONS: 150 lines, DECISIONS: 100 lines), output: `SPLIT` or `ARCHIVE — [file] — [reason]`

**6. Global context** — if philosophy, stack, or architecture changed, update `~/.claude/CONTEXT_GLOBAL.md`.

**7. PROJECT_TRACKER.md** — for the project(s) worked on this session, update Status, Milestone, Next, Blocker if changed; update Load tier on any `.claude/` file header if changed.

**9. Output** — one-line summary of what was updated. Then: "Run `/commit-push` → `/clear`."
