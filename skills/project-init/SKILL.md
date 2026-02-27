---
name: project-init
description: This skill should be used when the user wants to initialize, create, or bootstrap a new project. Use when user says "init project", "new project", "start project [name]", or asks to set up a new codebase. Always use this skill for any new project setup.
---
# Skill: project-init

---

## Pre-flight Checks
Before starting, verify:
1. `~/.claude/templates/` contains all template files
2. `N8N_WEBHOOK_INIT` env var is set (for Notion/tracker creation)
3. Git is available: `git --version`
4. Target path `~/projects/<slug>/` does not already exist

If any check fails: stop and tell Camille what is missing before proceeding.

---

## Step 1 — Intake (ask all at once, one message)

Ask Camille for:
- **Project name** (used as folder slug — lowercase, hyphens, no spaces)
- **Type**: `n8n-workflow` | `data-pipeline` | `web-app` | `tool` | `research`
- **Stack**: comma-separated tools (be specific — e.g. n8n, Claude Sonnet, BigQuery)
- **Pain point**: 1 sentence — what friction does this solve and for whom
- **Scope**: what is explicitly IN; what is explicitly OUT (prevents scope creep from day 1)

Do not proceed until all 5 are answered.

---

## Step 2 — Structure (run script)

```bash
bash ~/.claude/skills/project-init/scripts/init-structure.sh <project-slug>
```

This creates:
```
~/projects/<slug>/
  .claude/
    CONTEXT.md
    DECISIONS.md
    LESSONS.md
    DESIGN.md
    TODOS.md
  CLAUDE.md
  README.md
  .gitignore
```
And runs `git init` + initial empty commit.

---

## Step 3 — Fill Content (Claude writes, not script)

Using intake answers, populate each file:

**CLAUDE.md**: fill Purpose, Status=planning, Stack, Current Focus from pain point
**CONTEXT.md**: fill Current State (= "Project initialized. Nothing built yet."), leave Architecture for later
**DESIGN.md**: fill Problem Space from pain point, Scope from intake, leave Use Cases to be defined
**DECISIONS.md**: leave empty (no decisions yet — don't invent them)
**LESSONS.md**: leave empty (no lessons yet)
**TODOS.md**: Now = first concrete action to take based on scope

---

## Step 4 — Notion + Tracker (run script)

```bash
bash ~/.claude/skills/project-init/scripts/trigger-notion.sh \
  "<slug>" "<project-name>" "<type>" "<pain-point>"
```

Returns Notion page URL — add it to CLAUDE.md Quick Reference.

---

## Step 5 — Commit

```bash
cd ~/projects/<slug>
git add -A
git commit -m "chore: project init — <project-name>"
```

---

## Step 6 — Verify + Report

Confirm to Camille:
- ✅ Folder structure created
- ✅ All .claude/ files populated (not empty)
- ✅ CLAUDE.md imports @~/.claude/CLAUDE.md
- ✅ Git initialized, first commit done
- ✅ Notion page URL: [url]
- 📋 Suggested first action: [from TODOS.md > Now]

---

## Promotion Check (always run at end of init)
Scan intake answers for anything worth adding to global files.
Flag with `→ PROMOTE: [file] — [reason]` if found.
Camille decides — do not auto-write to global files.
