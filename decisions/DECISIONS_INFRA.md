# Decisions — Infrastructure

> Load when: touching server, credentials, deployment.
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

## [infra] One GitHub PAT per Hetzner server, not per project
- **Decision**: use a single fine-grained GitHub PAT scoped to all Hetzner repos; stored in `.git/config` on server; rotate annually
- **Rationale**: per-project PATs create maintenance overhead; blast radius difference is negligible on a single-tenant server — a server compromise already exposes all repos; one token = one rotation reminder
- **Date**: 2026-03-13
- **Status**: active
