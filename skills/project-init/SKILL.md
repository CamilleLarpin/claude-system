---
name: project-init
description: This skill should be used when the user wants to initialize, create, or bootstrap a new project. Use when user says "init project", "new project", "start project [name]", or asks to set up a new codebase. Always use this skill for any new project setup.
---
# Skill: project-init

---

## Pre-flight Checks
Before starting, verify:
1. `~/.claude/templates/` contains all template files
2. `NOTION_API_KEY` + `NOTION_PROJECT_DB_ID` are set in `~/.claude/credentials` (Notion creation will skip gracefully if missing — not a blocker)
3. Git is available: `git --version`
4. Target path `~/projects/<slug>/` does not already exist

If any check fails: stop and tell Camille what is missing before proceeding.

---

## Step 1 — Intake (ask all at once, one message)

Ask Camille for:
- **Project name** (used as folder slug — lowercase, hyphens, no spaces)
- **Stack ideas** *(optional — rough ideas, e.g. "maybe Python + Claude"; leave blank for TBD)*
- **Notion URL** *(optional — leave blank to create a new page)*

Do not proceed until project name is given. Stack and Notion URL are optional.

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

**CLAUDE.md**: fill Stack from intake (or "TBD"), Status=⚫ Scoping, leave Purpose and Current Focus blank
**CONTEXT.md**: fill Current State (= "Project initialized. Nothing built yet."), leave rest for later
**DESIGN.md**: leave all sections as TBD — do not invent pain point or scope
**DECISIONS.md**: leave empty
**LESSONS.md**: leave empty
**TODOS.md**: Now = "Define pain point and scope in DESIGN.md"

---

## Step 4 — Notion + Tracker

**4a — Notion page**
- If Camille provided a Notion URL in intake: use it directly — skip the script.
- If blank: run the script to create a new page:
```bash
bash ~/.claude/skills/project-init/scripts/trigger-notion.sh \
  "<slug>" "<project-name>" "<stack-or-TBD>"
```
Add the Notion URL (provided or generated) to the new project's CLAUDE.md Quick Reference.

**4b — Update PROJECT_TRACKER.md**
Append a new entry to `~/.claude/PROJECT_TRACKER.md` under `## Projects`, using the standard format:
```
### <Project Name>
- **Status**: ⚫ Scoping
- **Stack**: <stack>
- **Repo**: — (not yet created)
- **Notion**: <url from 4a, or — if script skipped>
- **n8n**: —
- **Docs**: ~/projects/<slug>/.claude/
- **Blocker**: none
- **Next**: <first action from TODOS.md > Now>
```
Also update `**Last updated**` date at the top of the file.

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
- ✅ Notion page URL: [url or "skipped — credentials not set"]
- ✅ PROJECT_TRACKER.md updated
- 📋 Suggested first action: [from TODOS.md > Now]

---

## Promotion Check (always run at end of init)
Scan intake answers for anything worth adding to global files.
Flag with `→ PROMOTE: [file] — [reason]` if found.
Camille decides — do not auto-write to global files.
