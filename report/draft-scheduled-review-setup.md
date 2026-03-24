# Draft — Scheduled Review-Setup Agent

> Status: draft — not yet created. Resume with: load this file + run /schedule

---

## What this does
Monthly remote agent that audits Claude setup files and writes findings to repo.
User then pulls, reads findings, and runs /review-setup interactively with context prepared.

---

## Schedule
- Frequency: every month
- Proposed: 1st of each month, 9am Paris time = `0 8 1 * *` (UTC) — shifts 1h in summer (CEST)
- UNRESOLVED: day/time not confirmed by user

---

## Repo
`https://github.com/CamilleLarpin/claude-system` confirmed

## Report folder
Proposed: `report/review-setup/review-setup-YYYY-MM-DD.md`
UNRESOLVED: folder naming not confirmed by user

---

## Agent prompt (final draft)

You are running a scheduled monthly audit of Camille Larpin's Claude Code setup files.

**1. Read and audit these files** for staleness, redundancy, imprecision, load-tier gaps, and effectiveness (directives/skills that appear unused or theoretical):
- `CLAUDE.md`
- `CONTEXT_GLOBAL.md`
- `LESSONS_GLOBAL.md`
- `DECISIONS_GLOBAL.md`
- All files under `skills/`

**Criteria per file:**
- Staleness — still true and practiced?
- Redundancy — duplicated elsewhere?
- Precision — every word earning its place? undefined terms?
- Load tier — referenced files have declared load conditions?
- Effectiveness — any directive or skill that looks unused or theoretical?

**2. Write findings** to `report/review-setup/review-setup-YYYY-MM-DD.md` (use today's date).
Format each finding: **File** · **Issue type** · **Observation** · **Why it matters**
End with: `Recommended focus for /review-setup: [top files]`

**3. Add a task** to `projects-tracking/BACKLOG.md` under `## Tasks > ### Claude Setup`:
`- [ ] Run /review-setup — findings at report/review-setup/review-setup-YYYY-MM-DD.md · Now`

**4. Commit** both changes: `chore: monthly review-setup findings YYYY-MM-DD`

---

## Also pending: update /review-setup skill
Add Step 2.5 — Effectiveness check after current Step 2 (Scan) in `skills/review-setup/SKILL.md`:

> For each skill and directive: has this been used or applied since the last review?
> Flag anything that exists but hasn't fired in practice — candidate for removal or simplification.
> Ask: "Is anything here adding complexity that isn't earning its place?"
