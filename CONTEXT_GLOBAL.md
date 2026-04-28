# Global Context — Camille Larpin

> Load when: planning · deciding · starting new work
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
- **Data**: DuckDB (CRM on Hetzner — `crm_data` Docker volume → `/opt/crm/crm.db` inside container · queried via CRM FastAPI) · DuckDB (finances-ezerpin, local) · dbt Core (finances-ezerpin local · pea-pme-pulse GCP) · BigQuery + GCS (pea-pme-pulse team project) · MariaDB (Nextcloud on Hetzner)
- **Logging** (Python pipelines): `loguru` — standard across all `src/` pipeline modules; no `print()` in pipeline code
- **Storage**: file-based (JSON/MD); **Git is the source of truth** including for all project and task management (`~/.claude/projects-tracking/`, project `TODOS.md`)
- **Infra**: Hetzner server `n8n-server` (138.199.205.72), Docker 29.1.5 — independent stacks:
  - `/opt/n8n/`: n8n (SQLite via `n8n_data` volume, no external DB)
  - `/opt/nextcloud/`: Nextcloud + its own MariaDB 10.11 instance (`nextcloud-db`)
  - `/opt/api/`: audio-intelligence-pipeline FastAPI (port 8000)
  - `/opt/ai-networking-system/`: CRM FastAPI (port 8001, docker compose) + DuckDB file (`crm_data` volume → `/opt/crm/crm.db`)
  - **Reverse proxy**: nginx 1.18 on host — TLS via certbot · n8n→5678 · cloud→8080 · crm-api→8001 · audio-api→8000 · mlflow→5000
  - **Hetzner Firewall** (`firewall-server`): inbound open — 22, 80, 443, 5678, 8080, 8000, 5000 · ufw (OS): allow 22/80/443, deny 8000/8001/5000
  - **SSH**: key-only auth (`~/.ssh/id_ed25519`), password auth disabled
  - **IaC**: Terraform + `hetznercloud/hcloud` provider — DR blueprint in progress (`hetzner-infra` project); manages Hetzner layer only (server, SSH key, firewall)
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
- **NanoClaw**: lightweight AI agent framework (Docker per session, Gmail + scheduling native, per-agent-group provider config) — in validation for chief-of-staff-ia; supersedes OpenClaw experiment
- **OneCLI**: self-hosted credential vault for AI agents (Hetzner) — credentials never leave own infra; used by NanoClaw for Gmail + Telegram access
- **MLflow**: experiment tracking — running on `/opt/api/` (port 5000)

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
- Project decisions: archive when superseded → DECISIONS_ARCHIVE.md; never delete LESSONS OR DECISIONS entries
- Archive done project: move entry to `## Archive` in PROJECT_TRACKER.md + folder to `~/projects/archived/<slug>/`
- Temporal plans: `~/.claude/plans/plan-<name>.md` — implementation plans; delete once executed; path referenced in backlog task
