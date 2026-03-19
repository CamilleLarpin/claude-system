# Claude Agents — Format & Conventions

Agents are sub-Claude instances with isolated context and a fixed system prompt.
They live in `.claude/agents/` (per-project) or `~/.claude/agents/` (global).

---

## File format

```markdown
---
name: agent-name          # kebab-case, matches filename
description: One sentence — when to invoke this agent and what it does.
model: sonnet             # sonnet | opus | haiku
---

System prompt body — role, behavior rules, output format.
```

## Naming conventions

- One file per agent, named by role: `reviewer.md`, `sql-reviewer.md`, `test-writer.md`
- Global agents (`~/.claude/agents/`): project-agnostic quality gates and utilities
- Project agents (`.claude/agents/`): domain-specific checks (e.g. `schema-validator.md`)

## Key properties

- **Isolated context**: agents do not see the parent conversation history — intentional for bias-free checks
- **Parallel**: can run alongside the main session without blocking it
- **Invocable by name**: Claude Code can invoke by agent name; you can also reference them in instructions

## When to use an agent vs a command

| | Agent | Command |
|---|---|---|
| Needs conversation history | ✗ | ✓ |
| Should be bias-free | ✓ | ✗ |
| Runs in parallel | ✓ | ✗ |
| Multi-turn interaction | ✗ | ✓ |

---

## Global agents

| File | Role |
|---|---|
| `reviewer.md` | Zero-context code review — correctness, security, over-engineering |
