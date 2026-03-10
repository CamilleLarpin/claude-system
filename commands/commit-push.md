---
description: Commit and push dirty .claude/ and ~/.claude/ files with logical grouping
---

# /commit-push — Commit & Push Claude Files

### 1. Check state

```bash
git status && git diff --stat --cached .claude/
git -C ~/.claude status && git -C ~/.claude diff --stat
```

If neither has dirty files → "Nothing to commit." and stop.

### 2. Group and commit

One commit per logical group, in order:

| Group | Files | Type |
|-------|-------|------|
| Commands / Skills | `commands/`, `skills/` | `feat:` |
| Decisions | `DECISIONS.md`, `DECISIONS_ARCHIVE.md` | `docs:` |
| Lessons | `LESSONS.md`, `lessons/LESSONS_*.md` | `docs:` |
| Context / Design | `CONTEXT.md`, `DESIGN.md`, `CONTEXT_GLOBAL.md` | `docs:` |
| Todos / Tracker | `TODOS.md`, `PROJECT_TRACKER.md` | `chore:` |
| Config | `CLAUDE.md`, `*.json`, `*.sh` | `chore:` |

### 3. Pull and push

For each repo with new commits — stash unstaged leftovers if any, then:

```bash
git pull --rebase && git push
```

### 4. Verify

```bash
git log --oneline -5
```

Report: one line per commit created, one line per repo pushed.
