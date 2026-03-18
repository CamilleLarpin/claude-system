---
description: Review and prioritize all projects and tasks across PROJECT_TRACKER and BACKLOG
---

# /prioritize — Prioritize Work

@~/.claude/decisions/DECISIONS_CONVENTIONS.md

### 1. Load files
Read `~/.claude/PROJECT_TRACKER.md` and `~/.claude/BACKLOG.md`.

### 2. Display current state
Show all projects and tasks grouped by priority. Format:

```
## Now
**[Name]** · [TRACKER|BACKLOG] · [one-line milestone or why]

## Next
...

## Later
...

## Someday
...

## Blocked
**[Name]** · ⚠️ [blocker]

## TBD
**[Name]** · [source]
```

### 3. Ask
"What needs to change?"

### 4. Apply changes
For each priority change:
- Update the Priority field on the entry
- Append: `  - YYYY-MM-DD [Old] → [New]: [reason]`
- If 3 log entries exist, drop the oldest

### 5. Redisplay → repeat from step 3
Continue until user says done or confirms no more changes.

### 6. Someday sweep
Ask: "Any Someday items that no longer resonate? Drop them now or they'll stay forever."

### 7. Write files
Update `~/.claude/PROJECT_TRACKER.md` and `~/.claude/BACKLOG.md`. Update `**Last updated**` date in both.
