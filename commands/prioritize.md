---
description: Review and prioritize all projects and tasks across PROJECT_TRACKER and BACKLOG
---

# /prioritize — Prioritize Work

@~/.claude/decisions/DECISIONS_CONVENTIONS.md

### 1. Pull latest tracking state

```bash
cd ~/.claude/projects-tracking && git pull --rebase
```

### 2. Load files
Read `~/.claude/projects-tracking/PROJECT_TRACKER.md` and `~/.claude/projects-tracking/BACKLOG.md`.

### 3. Display current state
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

### 3.5. Score and rank (Now + Next + Later only)

Score every project and task from those three tiers on 3 dimensions (1–3 each):

| Dimension | 1 | 2 | 3 |
|---|---|---|---|
| **Impact** | Low value; unblocks nothing | Moderate value or unblocks one thing | High value or unblocks multiple projects |
| **Effort** | Weeks of work | Days of work | Hours / one session |
| **Alignment** | Tangential to current phase/goals | Supports current phase | Core to current phase |

**Score = Impact + Effort + Alignment** (max 9)

Output as a single table, sorted by score descending. Include a **Signal** column that fuses score and tier into one verdict — no separate mismatch section needed:

```
| Item | Tier | I | E | A | Score | Signal |
|------|------|---|---|---|-------|--------|
| ...  | Now  | 3 | 2 | 3 | 8     | ✅     |
| ...  | Next | 3 | 3 | 2 | 8     | ✅     |
| ...  | Later| 3 | 2 | 2 | 7     | ↑ promote |
| ...  | Now  | 1 | 2 | 1 | 4     | ↓ demote  |
```

Signal rules:
- `✅` — score and tier are aligned (no action needed)
- `↑ promote` — score ≥ 7 but in Later → candidate to move up
- `↓ demote` — score ≤ 4 but in Now/Next → candidate to move down or drop

### 4. Ask
"What needs to change?"

### 5. Apply changes
For each priority change:
- Update the Priority field on the entry
- Append: `  - YYYY-MM-DD [Old] → [New]: [reason]`
- If 3 log entries exist, drop the oldest

### 6. Redisplay → repeat from step 4
Continue until user says done or confirms no more changes.

### 7. Someday sweep
Ask: "Any Someday items that no longer resonate? Drop them now or they'll stay forever."

### 8. Write files
Update `~/.claude/projects-tracking/PROJECT_TRACKER.md` and `~/.claude/projects-tracking/BACKLOG.md`. Update `**Last updated**` date in both.
