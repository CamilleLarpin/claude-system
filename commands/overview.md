---
description: Daily overview — day of week, active projects, blockers, what to work on
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

## Active Projects
[For each project with any status — show all]

**[Project Name]** · [status emoji]
→ [Milestone field]
⚠️ Blocker: [Blocker field — omit line if "none"]
```

Rules:
- List projects in this order: 🔴 Blocked first, then 🔵 Building, then 🟡 Testing, then 🟢 Running, then 🟠 Paused, then ⚫ Scoping
- Keep each project to 2–3 lines max — no extra context, no stack details
- If no blockers exist across all projects, omit the ⚠️ lines entirely
