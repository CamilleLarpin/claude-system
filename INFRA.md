# Infra — Operational Spec

> Load when: working on server · deploying · configuring ports or services · infra debugging
> NOT HERE: tooling choices and stack coherency (→ CONTEXT_GLOBAL.md)

---

## Server

- **Host**: Hetzner `n8n-server` · IP: 138.199.205.72 · Docker 29.1.5
- **SSH**: key-only auth (`~/.ssh/id_ed25519`), password auth disabled

## Docker Stacks

| Path | Service | Notes |
|---|---|---|
| `/opt/n8n/` | n8n | SQLite via `n8n_data` volume — no external DB |
| `/opt/nextcloud/` | Nextcloud | MariaDB 10.11 (`nextcloud-db`) |
| `/opt/api/` | Audio Intelligence FastAPI | port 8000 |
| `/opt/ai-networking-system/` | CRM FastAPI | port 8001, docker compose · DuckDB: `crm_data` → `/opt/crm/crm.db` |

## Nginx Reverse Proxy

nginx 1.18 on host · TLS via certbot

| Route | Internal port |
|---|---|
| n8n.helmcome.com | 5678 |
| cloud.helmcome.com | 8080 |
| crm-api | 8001 |
| audio-api | 8000 |
| mlflow | 5000 |

## Firewall

- **Hetzner Firewall** (`firewall-server`): inbound open — 22, 80, 443, 5678, 8080, 8000, 5000
- **ufw (OS)**: allow 22/80/443 · deny 8000/8001/5000

## IaC

Terraform + `hetznercloud/hcloud` — manages Hetzner layer only (server, SSH key, firewall)
DR blueprint: `hetzner-infra` project
