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

## [infra] One GitHub PAT per Hetzner server, not per project
- **Decision**: use a single fine-grained GitHub PAT scoped to all Hetzner repos; stored in `.git/config` on server; rotate annually
- **Rationale**: per-project PATs create maintenance overhead; blast radius difference is negligible on a single-tenant server — a server compromise already exposes all repos; one token = one rotation reminder
- **Date**: 2026-03-13
- **Status**: active
