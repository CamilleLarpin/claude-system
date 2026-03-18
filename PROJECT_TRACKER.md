# Project Tracker — Camille Larpin

> Load when: assessing cross-project relevance or promotion candidates.
> NOT HERE: project-specific implementation details (→ project .claude/).
> Update when: creating a project; changing scope, stack, or status.

**Last updated**: 2026-03-18 (session 2)

---

## Format
```
### [Project Name]
- **Status**: [emoji status]
- **Priority**: Now | Next | Later | Someday
  - YYYY-MM-DD [Old] → [New]: [reason] (max 2 entries — drop oldest when adding a third)
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

### OpenClaw Setup
- **Status**: 🔵 Building
- **Priority**: Next
  - 2026-03-18 TBD → Next: under active evaluation; next experiment slot
- **Stack**: OpenClaw · Claude Sonnet 4.6 · Telegram (@Crab_140_bot)
- **Repo**: https://github.com/CamilleLarpin/openclaw-setup
- **Notion**: https://www.notion.so/Test-and-Validate-Open-claw-Functionality-317fef9576f18162b96fd6131e8c4aa9
- **n8n**: —
- **Docs**: ~/projects/openclaw-setup/.claude/
- **Milestone**: P1 Stability — restart gateway, enable exec write, set up daily habit tracker
- **Blocker**: none
- **Next**: `openclaw gateway --help` → find restart command → restart to apply exec config

### Audio Intelligence Pipeline
- **Status**: 🔵 Building
- **Priority**: Now
  - 2026-03-18 TBD → Now: active build — MLflow GenAI migration in progress
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
- **Priority**: Now
  - 2026-03-18 TBD → Now: active — extending with task management from Telegram
- **Stack**: n8n · Claude Sonnet · OpenAI API · Telegram · Notion
- **Repo**: https://github.com/CamilleLarpin/ghost
- **Notion**: —
- **n8n**: EsMKQrNYifeGbraNshhDc
- **Docs**: ~/projects/ghost/.claude/
- **Milestone**: Phase 1 — extend Ghost with task management from Telegram (view, mark done, reprioritize)
- **Blocker**: none
- **Next**: Add Telegram bot access control (allowlist by chat_id) → start task management Phase 1

### Biography
- **Status**: 🔴 Blocked
- **Priority**: Now
  - 2026-03-18 TBD → Now: active testing phase; blocked on external feedback
- **Stack**: n8n · Claude Sonnet · OpenAI API · Telegram · GitHub · Google Docs
- **Repo**: https://github.com/CamilleLarpin/biography
- **Notion**: —
- **n8n**: 4 workflows active (DDA) + 4 pending (MIC)
- **Docs**: ~/projects/biography/.claude/
- **Milestone**: DDA end-to-end test — Google Docs credential + full flow validation
- **Blocker**: pending father's and MIC user feedback
- **Next**: Google Docs credential config → DDA end-to-end test; MIC rollout (duplicate workflows, add allowlists)

### Family Content Manager
- **Status**: 🔴 Blocked
- **Priority**: Now
  - 2026-03-18 TBD → Now: active; blocked on user feedback from Joffrey
- **Stack**: n8n · Claude Vision · Nextcloud · Telegram
- **Repo**: https://github.com/CamilleLarpin/family_content_manager
- **n8n**: OtWARZS3cBAwql1Z, YOi6nFrvr4RRFub1
- **Docs**: ~/projects/family_content_manager/.claude/
- **Milestone**: P1 Stability — validate budget kill switch → user test with Joffrey
- **Blocker**: pending Joffrey's user feedback
- **Next**: Test budget kill switch → test with Joffrey → Phase 3 Gmail archiving

### Gmail Inbox Cleanup
- **Status**: 🔵 Building
- **Priority**: Now
  - 2026-03-18 TBD → Now: active rule-based blitz in progress
- **Stack**: Gmail API · Python (Phase 0) · n8n Hetzner · Claude API Sonnet (Phase 2 drafting only)
- **Repo**: https://github.com/CamilleLarpin/gmail-inbox-cleanup
- **Notion**: https://www.notion.so/TBC-Inbox-cleaning-and-archival-assistant-2e3fef9576f180ff97fdfff26d92c986
- **n8n**: —
- **Docs**: ~/projects/gmail-inbox-cleanup/.claude/
- **Milestone**: Phase 0 Wave 2 — LLM classifier pipeline built; 1000-email sample categorised (43 categories); enriched report generated
- **Blocker**: none
- **Next**: Review category_report.txt → assign TRASH/ARCHIVE/REVIEW per category → move hard rules to config.json → run full 35k classify → apply

### AI Networking System
- **Status**: 🔵 Building
- **Priority**: Now
  - 2026-03-18 TBD → Now: active — DuckDB CRM setup pending
- **Stack**: n8n · Claude Sonnet · DuckDB · FastAPI · Slack · Telegram · Google Workspace
- **Repo**: https://github.com/CamilleLarpin/ai-networking-system
- **Notion**: —
- **n8n**: L9mXT4tovnOM2Xiz (Part A ✅ polling), CW7WSVtKPFaczTiw (Part B ✅)
- **Docs**: ~/projects/ai-networking-system/.claude/
- **Milestone**: P0 — DuckDB CRM setup (schema + FastAPI wrapper + backup + first contacts)
- **Blocker**: none
- **Next**: Set up DuckDB on Hetzner → FastAPI CRM wrapper → nightly backup cron → enter first 10 contacts

### Finances Ezerpin
- **Status**: 🔵 Building
- **Priority**: Now
  - 2026-03-18 TBD → Now: active — first result milestone in progress
- **Stack**: Python · dlt · DuckDB · dbt Core 1.11.7 · Claude Haiku · nao · Evidence.dev (fallback) · cron + Makefile
- **Repo**: https://github.com/CamilleLarpin/finances-ezerpin
- **Notion**: https://www.notion.so/Build-finance-family-tools-for-2026-2aafef9576f180eb931fd6f8e96106b3
- **n8n**: —
- **Docs**: ~/projects/finances-ezerpin/.claude/
- **Milestone**: M2 — Clean categorization (Claude Haiku + few-shot from corrections → confidence threshold → Telegram review)
- **Blocker**: none
- **Next**: Build `pipelines/categorize.py` — Claude Haiku categorization + `pipelines/validate_2024.py` — calibrate confidence threshold

### claude-one-digest
- **Status**: 🟢 Running
- **Priority**: Someday
  - 2026-03-18 TBD → Someday: running autonomously; no active development planned
- **Stack**: Python · Claude Haiku API
- **Repo**: https://github.com/CamilleLarpin/claude-one-digest
- **Notion**: https://www.notion.so/Track-Conversations-for-Learning-Insights-320fef9576f1818389e5faf472504c42
- **n8n**: —
- **Docs**: ~/projects/claude-one-digest/.claude/
- **Milestone**: Pipeline running with auto-digest for key projects
- **Blocker**: none
- **Next**: Retroactive tagging — flag past sessions not tagged at the time

### Data Engineering Notes
- **Status**: 🟠 Paused
- **Priority**: Someday
  - 2026-03-18 TBD → Someday: bootcamp artefact; deprioritized post-bootcamp
- **Stack**: Python · Claude API · Telegram · Docker · GCP
- **Repo**: —
- **Notion**: —
- **n8n**: —
- **Docs**: ~/projects/data-engineering-notes/.claude/
- **Milestone**: GCP Compute Engine deploy
- **Blocker**: none
- **Next**: Deploy to GCP Compute Engine
- **Notes**: Artefact bootcamp project (Feb 23 – Mar 27, 2026) — 3-layer learning system: capture → digest → master

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

## Priority Legend
- **Now** — getting active attention
- **Next** — high priority, starts when a slot opens
- **Later** — important but not urgent
- **Someday** — nice-to-have, no commitment

---

## Archive

### project-init-skill
- **Status**: ✅ Done
- **Stack**: Claude Code · bash · Notion API · gh CLI
- **Repo**: —
- **Docs**: ~/projects/.archived/project-init-skill/.claude/
- **Completed**: 2026-03-11 — skill fully built, TTY fix confirmed, end-to-end test passed
