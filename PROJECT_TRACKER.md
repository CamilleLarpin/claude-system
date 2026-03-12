# Project Tracker — Camille Larpin

> Load when: assessing cross-project relevance or promotion candidates.
> NOT HERE: project-specific implementation details (→ project .claude/).
> Update when: creating a project; changing scope, stack, or status.

**Last updated**: 2026-03-12 (evening)

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
- **Milestone**: FastAPI MVP (needed tomorrow) → Phase 3b MLflow eval → Phase 3c Prefect
- **Blocker**: none
- **Next**: Build FastAPI MVP — POST /summarize, API key auth, wire to analyze_transcript()

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
- **Stack**: Gmail API · n8n or Python (TBD) — rule-based, no LLM
- **Repo**: —
- **n8n**: —
- **Docs**: —
- **Milestone**: —
- **Blocker**: none
- **Next**: Init project → define blitz rules (age, sender patterns, unsubscribe header)

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
- **Milestone**: Phase 0 — Foundation complete
- **Blocker**: need Gsheet categories screenshot from Jo to finalize dim_categories schema
- **Next**: Validate categories (Gsheet screenshot) → export 2024 CSVs → setup DuckDB + dbt-duckdb

### claude-one-digest
- **Status**: 🔵 Building
- **Stack**: Python · Groq (llama-3.1-8b-instant / llama-3.3-70b-versatile)
- **Repo**: https://github.com/CamilleLarpin/claude-one-digest
- **Notion**: https://www.notion.so/Track-Conversations-for-Learning-Insights-320fef9576f1818389e5faf472504c42
- **n8n**: —
- **Docs**: ~/projects/claude-one-digest/.claude/
- **Milestone**: Build digest module — first working output to stdout
- **Blocker**: none
- **Next**: Build digest module — group sessions by project, call Groq API, render Markdown to stdout + data/digests/

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
- **Docs**: ~/projects/archived/project-init-skill/.claude/
- **Completed**: 2026-03-11 — skill fully built, TTY fix confirmed, end-to-end test passed
