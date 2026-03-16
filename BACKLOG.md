# Backlog — Camille Larpin

> Load when: selecting or prioritizing projects; stack decisions with cross-project implications.
> Active projects → PROJECT_TRACKER.md
> Promote to PROJECT_TRACKER when starting active development.

**Last updated**: 2026-03-16

---

## Format
```
### Project Name
- **Priority**: This Month | Next Month | This Quarter | Next Quarter | Unprioritized
- **Status**: idea | scoping | ready-to-start
- **Why**: one-liner motivation
- **Stack hint**: TBD or known tools
- **Constraints**: free-form
- **Notes**: optional
```

---

## Projects

### Media Content Manager
- **Priority**: This Month
- **Status**: scoping
- **Why**: Digest video/podcast content by passing a link — transcribe + clean summary; build a hand-picked knowledge base over time
- **Stack hint**: Python · Whisper · Claude · yt-dlp — extends audio-intelligence-pipeline
- **Constraints**: depends on audio-intelligence-pipeline engine being stable
- **Notes**: Sources confirmed: YouTube + podcasts (Whisper pipeline) + Reddit/LinkedIn posts (text — separate pipeline, not audio). C4 gap: needs DB for knowledge base (transcripts, summaries, tags, source URL, date) — without it C4 = 🟡. Shares transcription engine with Meeting Note Taker; consider building together. Bootcamp score: ~12/15.

### Meeting Note Taker
- **Priority**: This Month
- **Status**: scoping
- **Why**: Transcribe meetings (Mac hardware recording) + capture vocal notes after face-to-face meetings → structured notes; several meetings/week = real recurring use case
- **Stack hint**: Python · Whisper · Claude — extends audio-intelligence-pipeline
- **Constraints**: —
- **Notes**: C1 confirmed: Mac hardware recording (audio/video file input). Linked to AI Networking System — vocal note per person met → structured summary → feed into networking CRM. Shares transcription engine with Media Content Manager. Bootcamp score: ~13/15.

### Lightweight Observability Layer for Context Performance
- **Priority**: This Month
- **Status**: idea
- **Why**: Measure and optimize Claude context cost and performance over time
- **Stack hint**: Claude
- **Constraints**: —
- **Notes**: related to context engineering cluster below

### Automate Finance Investments
- **Priority**: Next Month
- **Status**: scoping
- **Why**: Personal investment tracking (consolidated picture across accounts) + recommendation layer — like Finary but tailored; phase 1: track; phase 2: recommend where to invest
- **Stack hint**: TBD — broker/bank API TBD
- **Constraints**: No bank/broker API available → C1 (automated collection) fails bootcamp criterion; manual CSV export only. **Not suitable as a bootcamp project.** Build post-bootcamp as a personal tool; benchmark against Finary before investing build time (might just pay for Finary).
- **Notes**: —

### Build Process to Follow News
- **Priority**: Next Month
- **Status**: idea
- **Why**: Automated news monitoring and digest pipeline
- **Stack hint**: Claude · n8n
- **Constraints**: —
- **Notes**: —

### Automate Online Course with Weekly Meal Prep
- **Priority**: This Quarter
- **Status**: idea
- **Why**: —
- **Stack hint**: Claude · n8n
- **Constraints**: —
- **Notes**: —

### Review Entire Closet for Workplace
- **Priority**: This Quarter
- **Status**: idea
- **Why**: AI-assisted wardrobe audit for workplace fit
- **Stack hint**: Claude
- **Constraints**: —
- **Notes**: —

### Teal — AI for Real Estate Search
- **Priority**: Next Quarter
- **Status**: idea
- **Why**: Leverage AI/software to optimize property search process
- **Stack hint**: TBD
- **Constraints**: —
- **Notes**: —

### Community-Driven LLM Coding Lessons Repository
- **Priority**: Next Quarter
- **Status**: idea
- **Why**: —
- **Stack hint**: TBD
- **Constraints**: —
- **Notes**: —

### Agent IA d'Analyse Politique et Aide à la Décision Électorale
- **Priority**: Next Quarter
- **Status**: idea
- **Why**: AI agent to analyze political positions and support electoral decision-making
- **Stack hint**: TBD
- **Constraints**: —
- **Notes**: —

### Context Version Tracker
- **Priority**: Unprioritized
- **Status**: idea
- **Why**: Version Claude setup/context; compare versions for cost and performance over time
- **Stack hint**: Claude
- **Constraints**: —
- **Notes**: part of context engineering cluster; related to Lightweight Observability Layer

### Conversation Pattern Analyzer
- **Priority**: Unprioritized
- **Status**: idea
- **Why**: Identify patterns in Claude conversations to optimize context setup for cost and efficiency
- **Stack hint**: Claude
- **Constraints**: —
- **Notes**: part of context engineering cluster; related to claude-one-digest

### Context Ambiguity Detector
- **Priority**: Unprioritized
- **Status**: idea
- **Why**: Detect ambiguity in Claude context — check what Claude is inferring, flag inconsistencies
- **Stack hint**: Claude
- **Constraints**: —
- **Notes**: part of context engineering cluster

---

## Tasks

### Infrastructure
- [ ] **Rotate GitHub PAT "server"** by 2027-03-13 — fine-grained, all Hetzner repos; stored in `.git/config` on server (plaintext). Update in: `/opt/finances-ezerpin/.git/config`, `/opt/api/.git/config`
- [ ] Install UFW as second firewall layer on n8n-server
- [ ] Install fail2ban for SSH brute-force protection — low priority, password auth already disabled

### Tools & Maintenance
- [ ] Enhance Project-Init Skill Bootstrap
- [ ] Test and Validate Open.claw Functionality
- [ ] Build Automated Error Correction Flow in n8n
- [ ] Version Control and Visualize n8n Workflow Code
- [ ] Clean Python and Tool Library Management Structure
- [ ] Launch automation to sync Notion and md files
- [ ] Enable Remote Development Management Through Telegram Integration
