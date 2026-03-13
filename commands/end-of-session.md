---
description: Run post-milestone checks — update docs, promote lessons, flag complexity
---

# /end-of-session — End of Session Checklist

Work through each step in order. Perform the action, don't just list it.

**1. Update project `.claude/` files** — reflect work done this session in `DECISIONS.md`, `LESSONS.md`, `DESIGN.md`, `TODOS.md`.

**2. Promote lessons** — if any lesson applies beyond this project, add it to the correct `~/.claude/lessons/LESSONS_*.md` and output: `PROMOTE: LESSONS_GLOBAL.md — [reason]`

**3. Digest flag** — if this session contained significant concepts worth keeping in the knowledge library (deep explanation, new mental model, multi-concept teaching moment), output `→ DIGEST: [project] — [one-line description]` and append one line to `~/projects/claude-one-digest/data/queue.md`:
`YYYY-MM-DD | <project> | <description>`
If not, skip silently.

**4. Promote decisions** — if any decision applies cross-project, add it to `~/.claude/DECISIONS_GLOBAL.md` and output: `PROMOTE: DECISIONS_GLOBAL.md — [reason]`

**5. Complexity check** — if this milestone meaningfully increased complexity, output: `→ REFACTOR: [component] — [reason]`

**6. Threshold check** — if any `.claude/` file crossed its threshold (LESSONS: 150 lines, DECISIONS: 100 lines), output: `SPLIT` or `ARCHIVE — [file] — [reason]`

**7. Global context** — if philosophy, stack, or architecture changed, update `~/.claude/CONTEXT_GLOBAL.md`.

**8. PROJECT_TRACKER.md** — for the project(s) worked on this session, update Status, Milestone, Next, Blocker if changed; update Load tier on any `.claude/` file header if changed.

**9. Output** — one-line summary of what was updated. Then: "Run `/commit-push` → `/clear`."
