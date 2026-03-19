---
description: Review and prioritize all projects and tasks across PROJECT_TRACKER and BACKLOG
---

# /prioritize — Prioritize Work

@~/.claude/decisions/DECISIONS_CONVENTIONS.md

### 1. Load files
Read `~/.claude/projects-tracking/PROJECT_TRACKER.md` and `~/.claude/projects-tracking/BACKLOG.md`.

### 2. Display current state
Show all projects and tasks in 4 blocks: Now, Next, Later, Someday.

Within each block:
- Projects first, **bold**, with the reason they're at this priority (from the latest priority log entry, or the project's current milestone/why)
- Blocked projects stay in Now with ⚠️ inline — do NOT move them to a separate section
- Tasks at the end of the block, *italic*, with a short pain point (why the task matters)

Format:
```
## Now

**[Project Name]** — [why it's here / what's driving it]
**[Project Name]** ⚠️ — [why it's here], blocked on [what]

*[Task name] — [pain point it solves]*

## Next

**[Project Name]** — [why it's here]

*[Task name] — [pain point it solves]*

## Later

...

## Someday

...
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
Update `~/.claude/projects-tracking/PROJECT_TRACKER.md` and `~/.claude/projects-tracking/BACKLOG.md`. Update `**Last updated**` date in both.
