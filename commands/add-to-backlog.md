---
description: Add a new project or task to the backlog
---

# /add-to-backlog — Add to Backlog

@~/.claude/decisions/DECISIONS_CONVENTIONS.md

### 2a. If project — ask in sequence:
1. Name
2. **Why** (one-liner motivation — mandatory, no item without this)
3. Priority (Now / Next / Later / Someday)
4. Stack hint (optional)
5. Constraints (optional)
6. Dependencies (optional — what must be done first?)
7. Notes (optional)

Append to `## Projects` in `~/.claude/BACKLOG.md` using the format from the file header. Add a priority log entry: `  - YYYY-MM-DD → [Priority]: [reason given]`

### 2b. If task — ask in sequence:
1. Category (Infrastructure / Tools & Maintenance / Claude Setup / Other)
2. Description
3. **Why** (brief rationale — mandatory; if you can't articulate it, the task probably shouldn't be tracked)
4. Priority (Now / Next / Later / Someday)
5. Dependencies (optional — note inline if this task requires another to be done first)

Append `- [ ] [Description] — [why] · \`[Priority]\`` to the correct category under `## Tasks`. If the category doesn't exist, create it.

### 3. Confirm
Show the added entry. Update `**Last updated**` date in BACKLOG.md.
