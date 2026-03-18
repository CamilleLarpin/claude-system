---
description: Daily overview — day of week, active projects by priority, blockers
---

# /overview — Daily Overview

### 1. Establish date

```bash
date "+%A %Y-%m-%d"
```

### 2. Load project tracker

Read `~/.claude/PROJECT_TRACKER.md`.

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
- Group by Priority: Now → Next → Later. Omit a section entirely if empty.
- **Someday projects are hidden** — not shown unless user asks.
- Within each priority group: Blocked (🔴) first, then Building, Testing, Running, Paused, Scoping
- Keep each project to 2–3 lines max — no stack details
- Omit ⚠️ Blocker line if blocker is "none"
- If no blockers exist anywhere, omit all ⚠️ lines
