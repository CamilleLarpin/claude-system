---
name: review-setup
description: Periodic ~/.claude/ setup review — audit directives for staleness, redundancy, precision, convention violations, and load-tier consistency. Use when: "review setup", "audit config", "review ~/.claude", or after major changes.
---
# Skill: review-setup

## Purpose
Audit Claude setup files so every directive earns its place. Collaborative — propose, validate, apply. One file per session.

## Mindset
Every line must justify itself. For each directive ask:
- Still true? Still followed in practice?
- Every word doing work — or is one word doing another's job?
- Could it be misread or is a term undefined?
- Redundant with another directive?
- Follows the writing convention?

When reviewing a change: challenge the author's intent — "Why didn't you like the old wording?" Surface the reasoning, not just the delta.

## Scope
Ask which file(s) to review. Default order: CLAUDE.md → CONTEXT_GLOBAL.md → DECISIONS_GLOBAL.md → LESSONS_GLOBAL.md → file headers.

## Process

### Step 1 — Load + announce
Read the target file. State: `Loaded: [filename]` before proceeding.

### Step 2 — Scan
For each section/bullet, check:
- **Staleness**: still true? reflects current practice?
- **Redundancy**: duplicated elsewhere?
- **Precision**: every word earning its place? undefined terms?
- **Convention**: punctuation and capitalization per convention below?
- **Load tier**: any file referenced → does it have a load condition declared?
- **Sync**: trigger in CLAUDE.md → does the file header match exactly?

### Step 3 — Challenge and fix
Two modes:
- **Mechanical fixes** (punctuation, trailing artifacts, convention violations): batch and apply in one pass — no need to ask.
- **Content/intent decisions** (changed meaning, dropped concept, new term, wording that changes behavior): one at a time — state what you noticed, ask why ("Why did you write X?" / "Why did you drop Y?"), propose alternative, wait for response before moving on.

### Step 4 — Apply immediately
After each validation, apply the change before moving on.

### Step 5 — Check propagation
After completing a file:
- CLAUDE.md trigger changed → update corresponding file header
- File header changed → verify CLAUDE.md reference matches
- Concept added or removed → check if referenced elsewhere

### Step 6 — Suggest next
`Review complete for [file]. Next: [next logical file]?`

---

## Writing Convention

| Character | Meaning | Rule |
|---|---|---|
| `—` | label → content | structural separator; lowercase after |
| `·` | inline list items | lowercase after |
| `→` | sequence or pointer | `Plan → build → test`; `→ filename.md` |
| `;` | two independent conditions in one bullet | |
| `-` | compound words only | never as structural separator |
| no trailing `.` | bullets are directives, not prose | |
| Capital first word | per bullet | lowercase thereafter unless proper noun/code |

---

## Load Tier Reference

| Tier | Location | Loaded |
|---|---|---|
| Always | CLAUDE.md | every session |
| On-demand | Global Knowledge files | when trigger matches |
| Deep retrieval | Category files (`decisions/`, `lessons/`) | when index points to them |
| Invoked | Skills (`skills/<name>/SKILL.md`) | via Skill tool |
| Invoked | Agents (`agents/<name>.md`) | via slash command |
