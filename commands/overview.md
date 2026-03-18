---
description: Daily overview — day of week, active projects by priority, blockers
---

# /overview — Daily Overview

### 1. Establish date

```bash
date "+%A %Y-%m-%d"
```

### 2. Load files

Read `~/.claude/PROJECT_TRACKER.md` and `~/.claude/BACKLOG.md`.

### 3. Output

```
📅 [Day], [Date]

## Now
**[Project Name]** · [status emoji]
→ [Milestone field]
⚠️ Blocker: [Blocker field]

## Next
...

## Later
...
```

Rules:
- Group by Priority: Now → Next. Later, Someday hidden — not shown unless user asks.
- Omit a section entirely if empty.
- Within each priority group: projects first (Blocked 🔴 first, then Building/Testing/Running/Paused/Scoping), then tasks
- Tasks shown as: `· [description]`
- Keep each project to 2–3 lines max — no stack details
- Omit ⚠️ Blocker line if blocker is "none"
- If no blockers exist anywhere, omit all ⚠️ lines
