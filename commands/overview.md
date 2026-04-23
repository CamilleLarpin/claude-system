---
description: Daily overview — day of week, active projects by priority, blockers
---

# /overview — Daily Overview

### 1. Establish date

```bash
date "+%A %Y-%m-%d"
```

### 2. Pull latest tracking state

```bash
cd ~/.claude/projects-tracking && git pull --rebase
```

### 3. Load files

Read `~/.claude/projects-tracking/PROJECT_TRACKER.md` and `~/.claude/projects-tracking/BACKLOG.md`.

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
- Within each priority group: all projects first (TRACKER then BACKLOG, Blocked 🔴 first within each), then tasks under a `**Tasks**` sub-header — blank line between projects and tasks block.
- All projects use the same format regardless of source:
  `**[Project Name]** · [status emoji if TRACKER | status label if BACKLOG]`
  `→ [Milestone if TRACKER | Why field if BACKLOG]`
  `⚠️ Blocker: [Blocker field]` (omit if none)
- BACKLOG projects with no status emoji: use their status label (idea · scoping · ready-to-start)
- Tasks: listed under `**Tasks**` as `· [description]` — only `- [ ]` tasks; skip `- [x]` (done)
- Keep each project to 2–3 lines max — no stack details
- If no blockers exist anywhere, omit all ⚠️ lines
