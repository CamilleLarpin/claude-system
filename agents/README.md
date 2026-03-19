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

## Invocation — how custom agents are actually called

Custom agents in `.claude/agents/` are **not** registered as `subagent_type` values in the Agent tool. Built-in types only: `general-purpose`, `Explore`, `Plan`, etc.

Two working invocation patterns:
1. **Slash command** (preferred): create a paired `~/.claude/commands/<name>.md` that spawns a `general-purpose` agent with the agent's prompt embedded. This gives reliable one-step invocation via `/<name>`.
2. **Auto-selection**: Claude Code may auto-select an agent based on description match when the task context fits — but this is implicit and not reliable for explicit quality gates.

Agent `.md` files in this folder serve as the **source of truth** for the agent's role and instructions. The paired command file is the invocation layer.

---

## Global agents

| Agent file | Slash command | Role |
|---|---|---|
| `reviewer.md` | `/review` | Zero-context code review — correctness, security, over-engineering |
