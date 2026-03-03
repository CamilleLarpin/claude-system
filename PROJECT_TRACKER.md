# Project Tracker — Camille Larpin

> Load when: assessing cross-project relevance or promotion candidates.
> NOT HERE: project-specific implementation details (→ project .claude/).
> Update when: creating a project; changing scope, stack, or status.

**Last updated**: 2026-03-03

---

## Format
```
### [Project Name]
- **Status**: [emoji status]
- **Stack**: [n8n · Claude · etc. or TBD]
- **Repo**: [url or —]
- **n8n**: [workflow IDs or —]
- **Docs**: [~/projects/<slug>/.claude/ or none]
- **Blocker**: [description or none]
- **Next**: [next milestone]
```

---

## Projects

### Audio Intelligence Pipeline
- **Status**: 🔵 Building
- **Stack**: Python 3.13 · OpenAI Whisper · Claude Sonnet · yt-dlp
- **Repo**: https://github.com/CamilleLarpin/audio-intelligence-pipeline
- **n8n**: —
- **Docs**: ~/projects/audio-intelligence-pipeline/.claude/
- **Blocker**: none
- **Next**: Add --summarize flag to CLI (Phase 2)

### Ghost
- **Status**: 🟢 Running
- **Stack**: n8n · Claude Sonnet · OpenAI API · Telegram · Notion
- **Repo**: https://github.com/CamilleLarpin/ghost
- **n8n**: EsMKQrNYifeGbraNshhDc
- **Docs**: ~/projects/ghost/.claude/
- **Blocker**: none
- **Next**: Fix photo resolution bug, review classification quality

### Biography
- **Status**: 🟡 Testing
- **Stack**: n8n · Claude Sonnet · OpenAI API · Telegram · GitHub · Google Docs
- **Repo**: https://github.com/CamilleLarpin/biography
- **n8n**: 4 workflows active
- **Docs**: ~/projects/biography/.claude/
- **Blocker**: none
- **Next**: Google Docs Service Account credential config → end-to-end test with DDA

### Family Content Manager
- **Status**: 🔵 Building
- **Stack**: TBD
- **Repo**: —
- **n8n**: OtWARZS3cBAwql1Z, YOi6nFrvr4RRFub1
- **Docs**: none
- **Blocker**: none
- **Next**: Read workflows → bootstrap .claude/ docs

### AI Assistant Networking
- **Status**: ⚫ Scoping
- **Stack**: TBD
- **Repo**: —
- **n8n**: —
- **Docs**: none
- **Blocker**: scope not defined
- **Next**: Define purpose and scope before building anything

### project-init-skill
- **Status**: 🔵 Building
- **Stack**: Claude Code · bash · n8n · gh CLI · Notion
- **Repo**: — (not yet created)
- **n8n**: — (webhook workflow not yet built)
- **Docs**: ~/projects/project-init-skill/.claude/
- **Blocker**: n8n webhook workflow not built → blocks Notion integration
- **Next**: Decide adapt existing n8n workflow vs. build new one

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
