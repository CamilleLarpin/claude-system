# Backlog — Camille Larpin

> Load when: selecting or prioritizing projects; stack decisions with cross-project implications.
> Active projects → PROJECT_TRACKER.md
> Promote to PROJECT_TRACKER when starting active development.

**Last updated**: 2026-03-18 (session 2)

---

## Format
```
### Project Name
- **Priority**: Now | Next | Later | Someday
  - YYYY-MM-DD [Old] → [New]: [reason] (max 2 entries — drop oldest when adding a third)
- **Status**: idea | scoping | ready-to-start
- **Why**: one-liner motivation
- **Stack hint**: TBD or known tools
- **Constraints**: free-form
- **Notes**: optional
```

---

## Projects

### Password Manager Setup
- **Priority**: Next
  - 2026-03-18 This Month → Next: initial migration to new priority vocabulary
- **Status**: ready-to-start
- **Why**: SSH key for Hetzner server only backed up on Mac — if Mac dies, server access is lost permanently. Password manager (Bitwarden) stores the key encrypted, recoverable from any device.
- **Stack hint**: Bitwarden (free, open-source)
- **Constraints**: Do before loading real financial data on Hetzner
- **Notes**: Back up `~/.ssh/id_ed25519` as secure note. Also use as opportunity to consolidate all passwords/secrets into one vault.

### Media Content Manager
- **Priority**: Later
  - 2026-03-18 This Month → Next: initial migration to new priority vocabulary
  - 2026-03-18 Next → Later: deprioritized — depends on audio-intelligence-pipeline being stable; not the next thing to build
- **Status**: scoping
- **Why**: Digest video/podcast content by passing a link — transcribe + clean summary; build a hand-picked knowledge base over time
- **Stack hint**: Python · Whisper · Claude · yt-dlp — extends audio-intelligence-pipeline
- **Constraints**: depends on audio-intelligence-pipeline engine being stable
- **Notes**: Sources confirmed: YouTube + podcasts (Whisper pipeline) + Reddit/LinkedIn posts (text — separate pipeline, not audio). C4 gap: needs DB for knowledge base (transcripts, summaries, tags, source URL, date). Shares transcription engine with Meeting Note Taker; consider building together.

### Meeting Note Taker
- **Priority**: Later
  - 2026-03-18 This Month → Next: initial migration to new priority vocabulary
  - 2026-03-18 Next → Later: deprioritized — real need but not urgent; shares engine with Media Content Manager, build together
- **Status**: scoping
- **Why**: Transcribe meetings (Mac hardware recording) + capture vocal notes after face-to-face meetings → structured notes; several meetings/week = real recurring use case
- **Stack hint**: Python · Whisper · Claude — extends audio-intelligence-pipeline
- **Constraints**: —
- **Notes**: C1 confirmed: Mac hardware recording (audio/video file input). Linked to AI Networking System — vocal note per person met → structured summary → feed into networking CRM. Shares transcription engine with Media Content Manager.

### Community-Driven LLM Coding Lessons Repository
- **Priority**: Later
  - 2026-03-18 Next Quarter → Someday: initial migration to new priority vocabulary
  - 2026-03-18 Someday → Later: raised — genuine interest in contributing to LLM coding education
- **Status**: idea
- **Why**: —
- **Stack hint**: TBD
- **Constraints**: —
- **Notes**: —

### Setup Observability
- **Priority**: Later
  - 2026-03-18 → Later: needed as server usage grows — no visibility today into health or failures
- **Status**: scoping
- **Why**: No visibility into server health (disk, memory, Docker), n8n workflow failures, or Claude context cost — flying blind as usage intensifies
- **Stack hint**: Grafana + Prometheus (server metrics) · n8n error hooks · Claude context token logging
- **Constraints**: —
- **Notes**: Scope: (1) server health — disk, memory, CPU, Docker container status; (2) n8n health — failed execution rate, error patterns; (3) Claude context cost — token footprint tracking over time. Monitor server disk space is part of this project (not a standalone task).

### Automate Finance Investments
- **Priority**: Later
  - 2026-03-18 Next Month → Later: initial migration to new priority vocabulary
- **Status**: scoping
- **Why**: Personal investment tracking (consolidated picture across accounts) + recommendation layer — like Finary but tailored; phase 1: track; phase 2: recommend where to invest
- **Stack hint**: TBD — broker/bank API TBD
- **Constraints**: No bank/broker API available → C1 (automated collection) fails bootcamp criterion; manual CSV export only. Build post-bootcamp as a personal tool; benchmark against Finary before investing build time (might just pay for Finary).
- **Notes**: —

### Automated Error Correction Flow (n8n)
- **Priority**: Later
  - 2026-03-18 Tasks → Later: promoted from task — multi-session build, not a one-shot fix; critical when no longer have time to debug n8n issues manually
- **Status**: idea
- **Why**: When starting a job, no longer have time to debug n8n workflow errors manually — need autonomous recovery from common failure patterns
- **Stack hint**: n8n · Claude
- **Constraints**: —
- **Notes**: Was a task; promoted because it requires design (error taxonomy), build (detection + correction nodes), and testing across multiple workflows — clearly multi-session.

### Remote Dev via Telegram
- **Priority**: Later
  - 2026-03-18 idea → Later: scoped as a project — compelling use case for phone-based work sessions
- **Status**: scoping
- **Why**: Work efficiently from phone — review status, give instructions, get updates from Claude/n8n without needing a laptop
- **Stack hint**: Telegram · Claude · n8n or OpenClaw
- **Constraints**: —
- **Notes**: Core question: build a new app or extend OpenClaw? Evaluate OpenClaw's mobile interface first before building custom.

### Build Process to Follow News
- **Priority**: Someday
  - 2026-03-18 Next Month → Someday: initial migration to new priority vocabulary
- **Status**: idea
- **Why**: Automated news monitoring and digest pipeline
- **Stack hint**: Claude · n8n
- **Constraints**: —
- **Notes**: —

### Automate Online Course with Weekly Meal Prep
- **Priority**: Someday
  - 2026-03-18 This Quarter → Someday: initial migration to new priority vocabulary
- **Status**: idea
- **Why**: —
- **Stack hint**: Claude · n8n
- **Constraints**: —
- **Notes**: —

### Review Entire Closet for Workplace
- **Priority**: Someday
  - 2026-03-18 This Quarter → Someday: initial migration to new priority vocabulary
- **Status**: idea
- **Why**: AI-assisted wardrobe audit for workplace fit
- **Stack hint**: Claude
- **Constraints**: —
- **Notes**: —

### Teal — AI for Real Estate Search
- **Priority**: Someday
  - 2026-03-18 Next Quarter → Someday: initial migration to new priority vocabulary
- **Status**: idea
- **Why**: Leverage AI/software to optimize property search process
- **Stack hint**: TBD
- **Constraints**: —
- **Notes**: —

### Agent IA d'Analyse Politique et Aide à la Décision Électorale
- **Priority**: Someday
  - 2026-03-18 Next Quarter → Someday: initial migration to new priority vocabulary
- **Status**: idea
- **Why**: AI agent to analyze political positions and support electoral decision-making — public tool for municipales 2026 + présidentielles 2027
- **Stack hint**: Python · assemblee-nationale.fr API · PostgreSQL · FastAPI · Claude
- **Constraints**: —
- **Notes**: Consolidates "Agent Politique" (bootcamp scope, removed from TRACKER). v1 KPIs: loyalty score (% votes aligned with parliamentary group) + participation rate per deputy. Bootcamp candidate (15/15). Broader manifesto comparison (PDF parsing) = out of scope for v1. Domain ramp-up needed.

### Context Engineering Setup
- **Priority**: Next
  - 2026-03-18 Unprioritized → Someday: merged from 4 separate ideas into one project
  - 2026-03-18 Someday → Next: raised — directly relevant to daily Claude work; want to start soon
- **Status**: idea
- **Why**: Understand and optimize Claude setup over time — version the context, identify conversation patterns, detect ambiguities, measure token cost
- **Stack hint**: Claude
- **Constraints**: —
- **Notes**: Merged from: Context Version Tracker + Conversation Pattern Analyzer + Context Ambiguity Detector + Lightweight Observability Layer for Context Performance. Three angles: (1) version Claude config + compare cost/quality across versions; (2) mine past sessions for recurring patterns; (3) detect what Claude is inferring or assuming (ambiguity scan).

---

## Tasks

### Infrastructure
- [ ] Install fail2ban — monitors server logs (SSH + nginx) for attack patterns; useful for log visibility + auto-banning repeated attackers · `Later`
- [ ] Install UFW as second firewall layer on n8n-server — second defense layer if Hetzner Firewall is misconfigured · `Someday`

### Tools & Maintenance
- [ ] Auto-update `~/.claude/README.md` weekly via cron + n8n; send diff summary to Telegram — keeps README current without manual effort · `Later`
- [ ] Enhance Project-Init Skill — move SKILL.md verbose step content to `references/` subfolder (progressive disclosure; reduces skill body token cost) · `Later`
- [ ] Clean Python and Tool Library Management — audit install locations: project-scoped tools local, shared tools global; avoid environment pollution · `Later`

### Claude Setup
- [ ] Update add-to-backlog skill — already done (2026-03-18): added mandatory "why" + dependencies fields · `Next` ✅ done in session
- [ ] Create `.claude/agents/` pattern — define sub-agent spec format as `.md` files (role, when to invoke, what it checks); add empty `agents/` folder to project-init scaffold · `Next`
- [ ] Document reviewer sub-agent pattern — zero-context sub-agent as quality gate: reads only changed files, checks correctness/security/over-engineering without bias from implementation reasoning · `Next`
- [ ] Document git worktrees pattern — run parallel Claude instances on separate branches (no branch-switching needed; e.g. one builds, one reviews) · `Next`
- [ ] Configure hooks in settings.json — auto-fired scripts before/after Claude tool calls (e.g. lint after edit, test after code change, Telegram ping on session end); use `/update-config` skill · `Next`
- [ ] Audit total loaded context cost — measure hot file token footprint in a fresh session; prune if over ~500-line equivalent · `Later` ⚠️ depends on: Configure hooks (for ongoing automated monitoring; one-time manual audit can be done without hooks)
- [ ] Add `CLAUDE.local.md` to project conventions — gitignored per-workspace override for machine-specific config (local paths, personal test IDs); add to project-init scaffold · `Someday` (solo dev on single machine — low urgency)
- [x] Set up Claude Code status line — ✅ done: `ctx:%` + in/out token counts configured via `statusLine` in settings.json
