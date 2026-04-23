# Decisions — Infrastructure

> Load when: touching server · credentials · deployment.
> NOT HERE: conventions (→ DECISIONS_CONVENTIONS.md), build (→ DECISIONS_BUILD.md).
> Archive at 100 lines → DECISIONS_INFRA_ARCHIVE.md

---

## Format
```
## [category] Decision title
- **Decision**: what was chosen
- **Rationale**: why — include alternatives considered
- **Date**: YYYY-MM-DD
- **Status**: active | superseded by [title] | archived
```

---

## [security] Server security model — n8n-server
- **Decision**: ports 80/443 open to all IPs; SSH key-only auth; app-level login as the real access gate
- **Rationale**: 80/443 must be open for any browser to reach the services — IP restriction is impractical for a personal server accessed from multiple locations; security relies on HTTPS encryption (nginx + Let's Encrypt) + app login screens, not firewall IP filtering; SSH locked to key-only since password brute-force is automated and constant on any public VPS
- **Date**: 2026-03-13
- **Status**: active

## [infra] One API key per project for cost tracking
- **Decision**: each project gets its own Anthropic (and Groq) API key so costs are trackable per project in the provider dashboard
- **Rationale**: shared keys make it impossible to attribute spend; per-project keys give a direct cost signal per project with zero extra tooling; negligible overhead (key creation is free and instant)
- **Date**: 2026-03-18
- **Status**: active

## [infra] ~/.claude/ split into public + private git repos
- **Decision**: `~/.claude/` is a public git repo (Claude setup: CLAUDE.md, skills, lessons, decisions, commands). Project tracking files live in `~/.claude/projects-tracking/` which is a separate private git repo (PROJECT_TRACKER.md, BACKLOG.md, TASKS_DONE.md).
- **Rationale**: Claude setup is reusable and shareable; project tracking contains personal project names, priorities, and task details that should stay private. Nested git repos work cleanly — git stops at `.git` boundaries, so the public repo cannot see inside `projects-tracking/`. No gitignore hacks needed.
- **Implementation**: `~/.claude/projects-tracking/` → `github.com/CamilleLarpin/projects-tracking` (private). All path references updated from `~/.claude/X.md` → `~/.claude/projects-tracking/X.md`.
- **Date**: 2026-03-19
- **Status**: active

## [infra] Services called by n8n from another container — Docker Compose + nginx required
- **Decision**: any service that n8n calls over HTTP must be deployed via Docker Compose (named volume for data persistence + nginx server block for HTTPS). Port bound to 127.0.0.1 only — nginx is the sole external entry point. TDD (pytest) before implementation to lock the API contract before n8n depends on it.
- **Rationale**: n8n runs in its own Docker container — HTTP is the only interface. nginx 1.18 runs on the Hetzner host (not in Docker) and handles TLS for all services — adding a server block is zero-overhead. Raw port exposure is fragile and insecure. Named volume prevents data loss. TDD ensures stable contract before wiring.
- **Note**: Traefik was incorrectly stated as "already running" in the original version of this decision — it is not. nginx is the actual reverse proxy on this server. Always verify with `docker ps` + `systemctl status nginx` before writing infra facts to decisions.
- **Date**: 2026-03-19 (corrected 2026-03-19)
- **Status**: active

## [backup] Hetzner backup strategy — Mac relay to WD NAS
- **Decision**: daily rsync from Hetzner → Mac (`~/backups/hetzner/`) → WD My Cloud Home (SMB). Script at `~/scripts/backup_hetzner.sh`. Mac cron at 02:00. WD NAS sync skipped gracefully if not mounted.
- **Rationale**: WD NAS is behind home NAT — Hetzner can't push to it directly. Mac is reliably on at home. Zero extra cost. Cloud storage alternatives (Hetzner Object Storage, Backblaze, R2) rejected — correlated failure risk or unnecessary cost at this scale.
- **Scope**: covers all Hetzner projects — currently finances-ezerpin (DuckDB) + family-content-manager (Nextcloud files). Add new projects to the script as needed.
- **Nextcloud exclusions**: `appdata_oc8odmpvrrzm/` · `admin/files_trashbin/` · `admin/files_versions/` · `admin/files/Trash/`
- **Date**: 2026-03-25
- **Status**: active

## [security] No disk encryption on Hetzner Docker volumes — risk accepted
- **Decision**: no LUKS or volume encryption on Hetzner Docker volumes. Risk documented and accepted.
- **Rationale**: LUKS requires OS reinstall — too disruptive. Realistic threat (unauthorized Hetzner staff access) is low probability. SSH key-only auth is the main protection. Encryption at rest does not protect against the primary threat vector (SSH compromise). Personal/family data — sensitive but not critical.
- **Date**: 2026-03-25
- **Status**: active

## [iac] Terraform for Hetzner infra — hcloud provider, DR blueprint first
- **Decision**: use Terraform (`hetznercloud/hcloud` provider) to codify Hetzner infra; adopt as DR blueprint before managing live state; import firewall only as Phase 2; provision new servers via Terraform from day 1 (no import needed)
- **Rationale**: single server doesn't justify full IaC overhead, but restore value + firewall-as-code justifies it; DR blueprint approach removes import risk on live server; `prevent_destroy = true` on all server resources as hard guard against accidental destroy; local state sufficient for solo dev
- **Scope**: Hetzner layer only (server, SSH key, firewall, volumes) — docker/nginx/certbot stay out of scope
- **Date**: 2026-03-26
- **Status**: active

## [infra] One GitHub PAT per Hetzner server, not per project
- **Decision**: use a single fine-grained GitHub PAT scoped to all Hetzner repos; stored in `.git/config` on server; rotate annually
- **Rationale**: per-project PATs create maintenance overhead; blast radius difference is negligible on a single-tenant server — a server compromise already exposes all repos; one token = one rotation reminder
- **Date**: 2026-03-13
- **Status**: active

## [infra] n8n Variables not available on Community plan — use Docker env vars
- **Decision**: inject secrets into n8n workflows via Docker Compose environment block (`/opt/n8n/docker-compose.yml`); access in workflows via `$env.VAR_NAME`
- **Rationale**: n8n Variables (`$vars.VAR_NAME`) requires a paid license — throws "Plan lacks license for this feature" on Community plan. Docker env vars are free, already supported by n8n, and live in the same compose file as the n8n service.
- **Date**: 2026-04-03
- **Status**: active

## [infra] Separate Docker Compose file per independent service on shared VM
- **Decision**: each logically independent service gets its own `docker-compose.<service>.yml` on a shared VM; only shared services (nginx, DB) go in the main `docker-compose.yml`
- **Rationale**: single compose file creates tight lifecycle coupling — restarting one service requires `down/up` of all others, risking disruption to production services; separate files allow independent `up/down/build` per service with zero blast radius on neighbors
- **Pattern**: `~/prefect/docker-compose.yml` (Prefect + nginx) · `~/nao/docker-compose.nao.yml` (nao only) — each in its own directory with its own config files
- **Date**: 2026-04-09
- **Status**: active — validated on pea-pme-pulse (nao + Prefect on same GCP VM)

## [orchestration] Self-hosted Prefect Server on GCP VM for team projects with >5 flows
- **Decision**: Prefect 3 self-hosted · Docker Compose (prefect-server + prefect-worker + nginx) · Process work pool · GCP VM with SA attached for ADC · nginx basic auth on port 80
- **Rationale**: Prefect Cloud free tier = 5 deployment hard limit; team projects exceed this quickly. Self-hosted removes limit, same CLI/API/prefect.yaml. GCP VM chosen for shared team projects (easy shutdown); personal projects → Hetzner (same docker-compose, swap IP).
- **GCP auth pattern**: attach SA to VM → ADC handles auth in all subprocesses; no JSON key, no secret block, no env var chain. dbt uses `method: oauth` profile.
- **Static IP**: always reserve a static IP before assigning to VM — ephemeral IPs change on restart
- **Date**: 2026-04-08
- **Status**: active — ✅ validated on pea-pme-pulse

## [security] Self-host credential vaults when handling personal communication data
- **Decision**: never use a cloud-hosted credential vault for services that handle personal email, messaging, or communication content; self-host the vault on own infra (e.g. OneCLI on Hetzner)
- **Rationale**: cloud vaults proxy requests — personal email body, subjects, and contacts transit third-party infrastructure; even with AES-256 at rest, data is decrypted at request time on a server you don't control; self-hosted vault = same security model with zero third-party exposure; OneCLI is MIT open-source and runs cleanly on Docker
- **Applies to**: any agent or automation that reads Gmail, WhatsApp, Telegram, or similar personal comms via a credential vault layer
- **Date**: 2026-04-23 · **Status**: active — first applied in chief-of-staff-ia (D3)

## [bank-ingestion] GoCardless (PSD2) over Playwright scraper for bank transaction ingestion
- **Decision**: use GoCardless open banking API (PSD2-regulated) via n8n workflow instead of Playwright scraper for automatic bank transaction ingestion
- **Rationale**: Playwright = brittle (session expiry, 2FA, bank UI changes); GoCardless = stable regulated API, read-only access, covers most European banks. The manual CSV export pattern breaks adoption — people forget to export, pipeline runs stale. GoCardless removes that friction permanently.
- **Fallback**: CSV manual export for banks not supported by GoCardless (cooperative banks like Crédit Mutuel — validate before committing)
- **Security**: GoCardless is PSD2-regulated (FCA/ACPR) — deliberate trust decision; credentials in `.env`, never in code
- **Date**: 2026-04-23 · **Status**: active — first validated in finances-ezerpin (M8)
