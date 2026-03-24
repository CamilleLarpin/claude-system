# ~/.claude/ — Claude Code Setup

Personal Claude Code configuration for a solo developer building automation with n8n, AI, and self-hosted infrastructure.

---

## What this is

A structured `~/.claude/` system that gives Claude persistent context, behavioral directives, reusable skills, and session commands — without bloating the always-on context window.

The core idea: **context engineering over prompt engineering**. Instead of repeating instructions every session, the system loads the right knowledge at the right time.

---

## Philosophy

- Understand before building — know the system before adding to it
- Know why before how — validate the pain before designing the solution
- Low maintenance — every choice must minimize future burden (solo developer constraint)
- Specificity beats volume — one precise constraint beats three vague ones
- Prune ruthlessly, archive don't delete — stale content dilutes active content

---

## Directory Structure

```
~/.claude/
├── CLAUDE.md                    # Always-on: behavior directives, defaults, conventions
├── CONTEXT_GLOBAL.md            # On-demand: stack, architecture, philosophy
├── DECISIONS_GLOBAL.md          # On-demand: cross-project decisions index
├── DECISIONS_GLOBAL_ARCHIVE.md  # Archive: superseded decisions (never deleted)
├── LESSONS_GLOBAL.md            # On-demand: lessons index → points to lessons/
├── lessons/                     # Category files (split at 150 lines each)
│   ├── LESSONS_N8N_RUNTIME.md
│   ├── LESSONS_N8N_MCP.md
│   ├── LESSONS_SLACK.md
│   ├── LESSONS_TELEGRAM.md
│   ├── LESSONS_NOTION.md
│   ├── LESSONS_CLAUDE.md
│   └── LESSONS_ARCHITECTURE.md
├── projects-tracking/
│   ├── PROJECT_TRACKER.md       # Active project registry
│   └── BACKLOG.md               # Project pipeline
├── agents/                      # Global sub-agents
├── commands/                    # Slash command definitions
├── skills/                      # On-demand domain knowledge
├── templates/                   # Project file templates
└── README.md                    # This file — human only, never auto-loaded
```

---

## How It Works

### Three-tier context hierarchy

| Tier | Files | When loaded |
|------|-------|-------------|
| Always-on | `CLAUDE.md` | Every session — kept minimal |
| On-demand | `CONTEXT_GLOBAL.md`, `DECISIONS_GLOBAL.md`, `LESSONS_GLOBAL.md`, `skills/` | Read when trigger applies |
| Never | Archives | Not loaded — kept for human reference |

### Skills

Loaded on demand before any scoped task. Each skill owns one exclusive domain — no overlap.

```
skills/
├── n8n-node-configuration/    # Operation-aware node config guidance
├── n8n-code-javascript/       # JS in n8n Code nodes ($input, $json, $helpers)
├── n8n-code-python/           # Python in n8n Code nodes
├── n8n-expression-syntax/     # n8n {{ }} expression syntax and common mistakes
├── n8n-workflow-patterns/     # Proven architectural patterns for n8n workflows
├── n8n-validation-expert/     # Interpreting validation errors and fixing them
├── n8n-mcp-tools-expert/      # Using n8n-mcp MCP tools effectively
├── project-init/              # Bootstrapping new projects
└── review-setup/              # Auditing ~/.claude/ for staleness and redundancy
```

### Agents

Sub-Claude instances with isolated context — intentionally bias-free. Live in `~/.claude/agents/` (global) or `.claude/agents/` (per-project). Invoked via paired slash command.

| Agent | Command | Role |
|-------|---------|------|
| `reviewer.md` | `/review` | Zero-context code review — correctness, security, over-engineering |

### Commands

Slash commands that invoke skills or agents. Defined in `commands/`.

| Command | Purpose |
|---------|---------|
| `/start` | Load project context, give focused briefing |
| `/overview` | Day of week, active projects by priority, blockers |
| `/commit-push` | Commit and push dirty `.claude/` files with logical grouping |
| `/end-of-session` | Post-milestone checks — update docs, promote lessons, flag complexity |
| `/align` | Strategic review — re-validate end vision, surface misordering |
| `/review` | Zero-context code review via reviewer agent |
| `/prioritize` | Review and prioritize all projects and tasks |
| `/add-to-backlog` | Add a new project or task to the backlog |
| `/compact` | Show correct `/compact` command with preservation instructions |
| `/digest` | Flag session as rich learning session — add to learning log |

---

## Project System

Every project lives in `~/projects/<slug>/` with a `.claude/` folder containing:

```
.claude/
├── CONTEXT.md     # What is true now for this project
├── DECISIONS.md   # Project-specific decisions (never deleted — archive when superseded)
├── LESSONS.md     # Project-specific lessons
├── DESIGN.md      # Architecture and design notes
└── TODOS.md       # Tasks and backlog
```

Project CLAUDE.md imports `@~/.claude/CLAUDE.md` — never duplicates global directives.

Templates for all project files live in `templates/`.

---

## Key Behaviors

- **Execution gate**: tasks with >2 steps or touching an external system require a numbered plan and explicit approval before proceeding
- **Build discipline**: Plan → clarify → validate → build one thing → test — never build ahead of validation
- **Lessons promotion**: project lessons applicable to 2+ projects get promoted to `LESSONS_GLOBAL.md`
- **Archive, never delete**: superseded decisions → `DECISIONS_ARCHIVE.md`; stale content dilutes active content

---

## Stack

- **Automation**: self-hosted n8n
- **AI**: Claude (Sonnet default, Opus for architecture), Anthropic/OpenAI/Groq APIs
- **Data**: DuckDB · dbt · MariaDB
- **Infra**: Hetzner server, Docker, nginx reverse proxy
- **Version control**: Git — source of truth for all project and task management
