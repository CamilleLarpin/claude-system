# Project Tracker — Camille Larpin

> Load when: assessing cross-project relevance or promotion candidates.
> NOT HERE: project-specific implementation details (→ project .claude/).
> Update when: creating a project; changing scope, stack, or status.

**Last updated**: 2026-03-16

---

## Format
```
### [Project Name]
- **Status**: [emoji status]
- **Stack**: [n8n · Claude · etc. or TBD]
- **Repo**: [url or —]
- **Notion**: [url or —]
- **n8n**: [workflow IDs or —]
- **Docs**: [~/projects/<slug>/.claude/ or none]
- **Milestone**: [current milestone being worked toward]
- **Blocker**: [description or none]
- **Next**: [immediate next action]
```

---

## Projects

### Audio Intelligence Pipeline
- **Status**: 🔵 Building
- **Stack**: Python 3.13 · OpenAI Whisper · Claude Sonnet · yt-dlp · MLflow · Prefect
- **Repo**: https://github.com/CamilleLarpin/audio-intelligence-pipeline
- **Notion**: —
- **n8n**: —
- **Docs**: ~/projects/audio-intelligence-pipeline/.claude/
- **Milestone**: Phase 3b: migrate to MLflow GenAI primitives (Judges, Datasets, mlflow.genai.evaluate)
- **Blocker**: none
- **Next**: Register 4-axis scorer with @mlflow.genai.scorer → switch to mlflow.genai.create_dataset() → mlflow.genai.evaluate()

### Ghost
- **Status**: 🟢 Running
- **Stack**: n8n · Claude Sonnet · OpenAI API · Telegram · Notion
- **Repo**: https://github.com/CamilleLarpin/ghost
- **Notion**: —
- **n8n**: EsMKQrNYifeGbraNshhDc
- **Docs**: ~/projects/ghost/.claude/
- **Milestone**: —
- **Blocker**: none
- **Next**: Fix photo resolution bug, review classification quality

### Biography
- **Status**: 🟡 Testing
- **Stack**: n8n · Claude Sonnet · OpenAI API · Telegram · GitHub · Google Docs
- **Repo**: https://github.com/CamilleLarpin/biography
- **Notion**: —
- **n8n**: 4 workflows active (DDA) + 4 pending (MIC)
- **Docs**: ~/projects/biography/.claude/
- **Milestone**: DDA end-to-end test — Google Docs credential + full flow validation
- **Blocker**: none
- **Next**: Google Docs credential config → DDA end-to-end test; MIC rollout (duplicate workflows, add allowlists)

### Family Content Manager
- **Status**: 🔵 Building
- **Stack**: n8n · Claude Vision · Nextcloud · Telegram
- **Repo**: https://github.com/CamilleLarpin/family_content_manager
- **n8n**: OtWARZS3cBAwql1Z, YOi6nFrvr4RRFub1
- **Docs**: ~/projects/family_content_manager/.claude/
- **Milestone**: P1 Stability — validate budget kill switch → user test with Joffrey
- **Blocker**: none
- **Next**: Test budget kill switch → test with Joffrey → Phase 3 Gmail archiving

### Gmail Inbox Cleanup
- **Status**: ⚫ Scoping
- **Stack**: Gmail API · LLM classifier · OpenClaw or n8n (TBD) · Nextcloud (Phase 2)
- **Repo**: https://github.com/CamilleLarpin/gmail-inbox-cleanup
- **Notion**: https://www.notion.so/TBC-Inbox-cleaning-and-archival-assistant-2e3fef9576f180ff97fdfff26d92c986
- **n8n**: —
- **Docs**: ~/projects/gmail-inbox-cleanup/.claude/
- **Milestone**: Design aligned — stack decision + Gmail API setup next
- **Blocker**: none
- **Next**: Evaluate OpenClaw vs n8n → set up Gmail API OAuth in GCP

### AI Networking System
- **Status**: 🔵 Building
- **Stack**: n8n · Claude Sonnet · Notion API · Slack · Telegram · Google Workspace
- **Repo**: https://github.com/CamilleLarpin/ai-networking-system
- **Notion**: —
- **n8n**: L9mXT4tovnOM2Xiz (Part A ✅), CW7WSVtKPFaczTiw (Part B ✅ — DM from Camille's personal profile confirmed)
- **Docs**: ~/projects/ai-networking-system/.claude/
- **Blocker**: none
- **Next**: Production test Monday (real RandomCoffee pairing) → Slack Workflow Builder trigger → P0 Notion CRM

### Finances Ezerpin
- **Status**: 🔵 Building
- **Stack**: Python · dlt · DuckDB · dbt-duckdb · Claude Haiku · nao · Evidence.dev (fallback) · cron + Makefile
- **Repo**: https://github.com/CamilleLarpin/finances-ezerpin
- **Notion**: https://www.notion.so/Build-finance-family-tools-for-2026-2aafef9576f180eb931fd6f8e96106b3
- **n8n**: —
- **Docs**: ~/projects/finances-ezerpin/.claude/
- **Milestone**: Phase 0 — DuckDB on Hetzner ✅; dbt-duckdb setup next
- **Blocker**: categories blocked on Jo's Gsheet screenshot
- **Next**: Setup dbt-duckdb → export 2024 CSVs → validate categories with Jo

### claude-one-digest
- **Status**: 🔵 Building
- **Stack**: Python · Claude Haiku API
- **Repo**: https://github.com/CamilleLarpin/claude-one-digest
- **Notion**: https://www.notion.so/Track-Conversations-for-Learning-Insights-320fef9576f1818389e5faf472504c42
- **n8n**: —
- **Docs**: ~/projects/claude-one-digest/.claude/
- **Milestone**: Validate session recap quality against gold standard
- **Blocker**: none
- **Next**: Manual review of Mar 12 recap vs gold standard → resume daily/weekly rollup once validated

### Data Engineering Notes
- **Status**: 🔵 Building
- **Stack**: Python · Claude API · Telegram · Docker · GCP
- **Repo**: —
- **Notion**: —
- **n8n**: —
- **Docs**: ~/projects/data-engineering-notes/.claude/
- **Milestone**: GCP Compute Engine deploy
- **Blocker**: none
- **Next**: Deploy to GCP Compute Engine
- **Notes**: Artefact bootcamp project (Feb 23 – Mar 27, 2026) — 3-layer learning system: capture → digest → master

### Agent Politique
- **Status**: ⚫ Scoping
- **Stack**: Python · assemblee-nationale.fr API · PostgreSQL · FastAPI · Claude (theme classification TBD)
- **Repo**: —
- **Notion**: —
- **n8n**: —
- **Docs**: —
- **Milestone**: Bootcamp certification project (Artefact, deadline ~2026-03-27) — 2+ weeks available as of 2026-03-16
- **Blocker**: teacher validation of v1 scope (votes + KPIs only, no manifesto comparison)
- **Next**: Confirm scope with teacher → explore AN API → initialize repo + .claude/
- **Notes**: Top bootcamp candidate (15/15). v1 KPIs: loyalty score (% votes aligned with parliamentary group) + participation rate per deputy. Manifesto comparison = comparing votes vs pre-election promises (PDF parsing) — out of scope for v1. Domain ramp-up needed (with Claude). Evaluation in ~/.claude/report/BOOTCAMP_PROJECT_EVALUATION.md; secondary motivation: public tool for municipales (2026-03) + présidentielles (2027)

---

## Cross-Project Notes
- Shared n8n instance: https://n8n.helmcome.com
- Shared error alerting: [Alert] Error Notifier (ID: S3JtzMtNJlNl4SOQ)

---

## Status Legend
- 🟢 Running — in production, working as intended
- 🟡 Testing — built, validating with users
- 🔵 Building — active development
- 🔴 Blocked — can't progress, waiting on something external
- 🟠 Paused — real project, deliberately on hold
- ⚫ Scoping — new, purpose/scope not yet defined
- ✅ Done — completed, no active development (see Archive section)

---

## Archive

### project-init-skill
- **Status**: ✅ Done
- **Stack**: Claude Code · bash · Notion API · gh CLI
- **Repo**: —
- **Docs**: ~/projects/.archived/project-init-skill/.claude/
- **Completed**: 2026-03-11 — skill fully built, TTY fix confirmed, end-to-end test passed
