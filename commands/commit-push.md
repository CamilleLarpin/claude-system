---
description: Commit and push dirty .claude/ and ~/.claude/ files with logical grouping
---

# /commit-push — Commit & Push Claude Files

## Instructions

### 1. Check current state

Run in both repos:
- Current project: `git status` and `git diff --stat` scoped to `.claude/`
- Global: `git -C ~/.claude status` and `git -C ~/.claude diff --stat`

If neither has dirty files, report "Nothing to commit." and stop.

### 2. Group changes

Identify logical groupings within each repo:

| Group | Files | Commit type |
|-------|-------|-------------|
| Decisions | `DECISIONS.md`, `DECISIONS_ARCHIVE.md` | `docs:` |
| Lessons | `LESSONS.md`, `lessons/LESSONS_*.md` | `docs:` |
| Context / Design | `CONTEXT.md`, `DESIGN.md`, `CONTEXT_GLOBAL.md` | `docs:` |
| Todos / Tracker | `TODOS.md`, `PROJECT_TRACKER.md` | `chore:` |
| Commands / Skills | `commands/`, `skills/` | `feat:` |
| Config | `CLAUDE.md`, `*.json`, `*.sh` | `chore:` |

### 3. Create commits

For each logical group, one focused commit:

```bash
git add <relevant-files>
git commit -m "$(cat <<'EOF'
<type>: <short description>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

Commit order: commands/skills first → decisions/lessons → context/design → todos/tracker → config last.

### 4. Pull and push

For each repo that has new commits:

```bash
git stash  # if unstaged changes remain
git pull --rebase
git push
git stash pop  # if stashed
```

### 5. Verify

```bash
git log --oneline -5
```

Report what was committed and pushed in each repo.
