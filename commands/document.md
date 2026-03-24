---
description: Lightweight mid-session save — update current project .claude/ docs from conversation context
---

# /document — Update Project Docs

Infer all updates from the current conversation. No prompting, no commit, no push.

### 1. Identify project

Detect from `pwd` → current project's `.claude/` folder.

### 2. Update docs

For each file that exists in `.claude/`, apply only what changed this session:

- **CONTEXT.md** — update status, stack, or architecture if it changed
- **TODOS.md** — check off completed items; add new ones surfaced this session
- **DECISIONS.md** — append any decisions made (format: `## YYYY-MM-DD — [topic]`)
- **LESSONS.md** — append any lessons learned (format: `## YYYY-MM-DD — [topic]`)
- **DESIGN.md** — update if design changed

Skip a file if nothing changed for it this session.

### 3. Confirm

Output one line per file updated: `updated: .claude/TODOS.md` — then stop.
