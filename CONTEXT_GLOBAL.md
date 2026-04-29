# Global Context — Camille Larpin

> Load tier: always · auto-loaded via @ in CLAUDE.md · keep minimal — every line costs every session
> NOT HERE: cross-project decisions with rationale (→ DECISIONS_GLOBAL.md), lessons (→ LESSONS_GLOBAL.md)

---

## Philosophy
- Understand before building: know the system before adding to it; speed is worthless if it compounds confusion
- Know why before how: understand the pain before designing the solution
- Add value first: no building without validated need
- Agility over lock-in: continuously question the stack, stay on top of tools and trends
- Low maintenance: every choice must minimize future maintenance burden — solo developer constraint
- No hidden assumptions: make the implicit explicit; if applying a rule requires inference, the rule is incomplete

## Technical Stack
- **Automation**: self-hosted n8n — https://n8n.helmcome.com
- **AI**: Claude (Sonnet default, Opus for architecture/complex reasoning), Anthropic/OpenAI/Groq APIs where needed
- **Data**: DuckDB (CRM on Hetzner · queried via CRM FastAPI) · DuckDB (finances-ezerpin, local) · dbt Core (finances-ezerpin local · pea-pme-pulse GCP) · BigQuery + GCS (pea-pme-pulse team project) · MariaDB (Nextcloud on Hetzner)
- **Logging** (Python pipelines): `loguru` — standard across all `src/` pipeline modules; no `print()` in pipeline code
- **Storage**: file-based (JSON/MD); **Git is the source of truth** including for all project and task management (`~/.claude/projects-tracking/`, project `TODOS.md`)
- **Infra**: Hetzner `n8n-server` (138.199.205.72) · Docker — 4 independent stacks: n8n · Nextcloud + MariaDB · Audio API · CRM API + DuckDB · reverse proxy: nginx + TLS · SSH: key-only · IaC: Terraform + hcloud → `~/.claude/INFRA.md`
- **Shared infrastructure across projects**:
  - n8n instance: https://n8n.helmcome.com — used by all automation projects · shared error alerting: [Alert] Error Notifier workflow (n8n ID: S3JtzMtNJlNl4SOQ)
  - Nextcloud (cloud.helmcome.com): shared document storage — `family-content-manager` (photo filing) + `gmail-inbox-cleanup` Phase 2 (email document routing)

## Live Services
Cross-project shared capabilities — updated at `/end-of-session` when anything changes.

| Service | URL / endpoint | Status | Used by |
|---|---|---|---|
| n8n | https://n8n.helmcome.com | ✅ live | all automation projects |
| Nextcloud | https://cloud.helmcome.com | ✅ live | family-content-manager · gmail-inbox-cleanup (Ph2) |
| CRM FastAPI | port 8001 (nginx → crm-api) | ✅ live | ai-networking-system |
| Audio Intelligence API | port 8000 (nginx → audio-api) | ✅ live | audio-intelligence-pipeline |
| MLflow | port 5000 (nginx → mlflow) | ✅ live | experimental |
| Error Alerting (n8n) | workflow ID: S3JtzMtNJlNl4SOQ | ✅ live | all n8n workflows |
| nao Talk To My Data | http://35.241.252.5:5005 | ✅ live | pea-pme-pulse · BQ gold · Gemini 2.5 Flash · bonus |
| pea-pme FastAPI | http://35.241.252.5/docs | ✅ live | pea-pme-pulse · BQ gold · X-API-Key auth |

## Experimental Stack
- **NanoClaw**: open-source AI agent framework (Claude Agent SDK) — use before building custom agent infra; native Telegram, Gmail, Slack + scheduling; per-group Docker isolation and config
- **OneCLI**: open-source HTTPS proxy + credential vault — agents never hold raw API keys; real credentials injected at request time; zero code change (HTTPS_PROXY-based); default credential layer for NanoClaw
- **MLflow**: experiment tracking

## Architecture Principles
- **Modularity**: small, composable units over monoliths; each component owns one responsibility
- **DRY**: extract reusable logic to modules (sub-workflows, scripts); never duplicates logic
- **Narrow scope**: agents and tools perform better with well-defined, bounded tasks
- **Design for failure**: define rollback, error and warning handling before building
- **Observability**: cost ceiling defined, effectiveness measurable, trigger defined for when to question the system
- **Reliability over autonomy**: prefer consistent, predictable behavior over powerful-but-fragile
- **Two-zone stack**: Technical Stack — change only when real pain justifies it · experiments — time-boxed, binary verdict: promote to Technical Stack or drop; no tools in limbo

## Project System
- Every project lives in `~/projects/<slug>/`
- Every project has `.claude/`: CONTEXT.md, DECISIONS.md, LESSONS.md, DESIGN.md, TODOS.md
- Every project CLAUDE.md imports `@~/.claude/CLAUDE.md`
- Project registry: `~/.claude/projects-tracking/PROJECT_TRACKER.md`
- Project decisions: archive when superseded → DECISIONS_ARCHIVE.md; never delete LESSONS or DECISIONS entries
- Archive done project: move entry to `## Archive` in PROJECT_TRACKER.md + folder to `~/projects/archived/<slug>/`
- Temporal plans: `~/.claude/plans/plan-<name>.md` — implementation plans; delete once executed; path referenced in backlog task
