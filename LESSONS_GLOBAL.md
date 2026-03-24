# Global Lessons Library

> Load when: alongside project LESSONS.md + only relevant category files · when debugging or starting a build.
> This file is the index — load the relevant category file for the actual lessons.
> NOT HERE: cross-project decisions with rationale (→ DECISIONS_GLOBAL.md).

---

## Category files

- `~/.claude/lessons/LESSONS_N8N_RUNTIME.md` — n8n node behavior, expressions, runtime gotchas
- `~/.claude/lessons/LESSONS_N8N_MCP.md` — n8n-mcp tool usage: updateNode, addNode, addConnection
- `~/.claude/lessons/LESSONS_SLACK.md` — Slack integration
- `~/.claude/lessons/LESSONS_TELEGRAM.md` — Telegram integration
- `~/.claude/lessons/LESSONS_NOTION.md` — Notion integration
- `~/.claude/lessons/LESSONS_CLAUDE.md` — skills authoring, Claude behavior, prompting, setup file conventions
- `~/.claude/lessons/LESSONS_CLAUDE_CODE.md` — Claude Code tool: context management, MCPs, agents, commands, /schedule, CLAUDE.md
- `~/.claude/lessons/LESSONS_ARCHITECTURE.md` — git, ai-agents, architecture, integrations, infra, bash, shell, data-engineering
- `~/.claude/lessons/LESSONS_LLM.md` — LLM APIs, prompting, model behavior, evaluation (mlflow, Groq, token limits)
- `~/.claude/lessons/LESSONS_DLT.md` — dlt pipeline behavior, column normalization, schema


---

## Format (for all category files)
```
## [category] · Rule|Guideline|Note · Short title
> YYYY-MM-DD · source: [project or session]
- what happened / what the trap is
- why it matters
- what to do instead
```

## Types
- **Rule**: must follow — violating it breaks things or causes silent failure
- **Guideline**: should follow unless explicitly justified
- **Note**: useful to know — no mandatory action

## Promotion rule
Promote to global only if Rule or Guideline — Notes stay in project files.

## Thresholds
- Each category file splits at 150 lines → split by load context, not by sequence. Name the new file to reflect when it's loaded (e.g. `LESSONS_N8N_CREDENTIALS.md`), never `LESSONS_N8N_2.md`.
- Add new categories as needed — update this index when you do
