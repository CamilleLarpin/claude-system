# Global Lessons Library

> Load when: debugging or starting a build.
> This file is the index — load the relevant category file for the actual lessons.
> NOT HERE: cross-project decisions with rationale (→ DECISIONS_GLOBAL.md).

---

## Category files

- @~/.claude/lessons/LESSONS_N8N.md — n8n, Slack, Notion gotchas
- @~/.claude/lessons/LESSONS_CLAUDE.md — skills authoring, Claude behavior
- @~/.claude/lessons/LESSONS_ARCHITECTURE.md — git, ai-agents, architecture, integrations

---

## Format (for all category files)
```
## [category] Short title
> YYYY-MM-DD · source: [project or session]
- what happened / what the trap is
- why it matters
- what to do instead
```

## Thresholds
- Each category file splits at 150 lines → create a sub-file, e.g. `LESSONS_N8N_2.md`
- Add new categories as needed — update this index when you do
