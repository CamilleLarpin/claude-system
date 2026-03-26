# Lessons — Infrastructure & Security

> Load when: setting up backups · managing credentials · configuring servers · securing services.
> Never delete entries. Add date and context.

---

## 2026-03-25 — Never use cloud file storage as a secrets store

**Context**: API keys (Anthropic, OpenAI, Telegram, GitHub, n8n, Notion) were found in a Nextcloud folder that had been "deleted" ~6 weeks earlier but remained in the Nextcloud trash bin, accessible to any admin.

**What we learned**:
- Nextcloud (and any cloud file storage) trash retains deleted files for up to 30 days — deletion is not immediate erasure.
- Files in trash are still accessible to anyone with admin credentials.
- Nextcloud logs (`nextcloud.log`) can be grepped for file paths to check if access occurred.
- No evidence of access found in logs — risk was low retrospectively, but non-zero for 6 weeks.

**Lesson**: credentials belong in the n8n credential store (workflows), `.env` files on server (gitignored, never uploaded), or a password manager. Never in a cloud file system — even temporarily.

---

## 2026-03-25 — Never paste secrets in chat — rotate immediately if exposed

**Context**: CRM bearer token pasted in full into a Claude Code session while building a test curl command.

**Lesson**: Any secret pasted in a chat session should be treated as compromised — conversation logs may persist the value. Rotate immediately: generate new token, update `.env` on server, restart container, update n8n credential.

**Prevention**: use shell substitution to inject secrets without exposing them: `$(grep TOKEN .env | cut -d= -f2)` or `$(ssh server "grep TOKEN file | cut -d= -f2")`.

---

## infra · Rule · Use launchd instead of cron for scheduled scripts on macOS
> 2026-03-26 · source: finances-ezerpin
- `cron` on macOS **skips jobs entirely** if the machine is asleep at the scheduled time — no catch-up
- `launchd` runs the job as soon as the machine wakes up after a missed window — correct behavior for daily backups
- Create a `.plist` in `~/Library/LaunchAgents/` and load with `launchctl bootstrap gui/$(id -u) <plist>` (macOS Ventura+ — `launchctl load` is deprecated)
- Verify registration: `launchctl list | grep <label>` — `-` PID means registered but not running (expected)

---

## infra · Rule · Docker Compose v5: --env-file flag not supported on run
> 2026-03-26 · source: finances-ezerpin
- `docker compose run --env-file <file>` fails with `unknown flag: --env-file` on Compose v5
- Use shell substitution instead: `-e KEY=$(grep KEY .env | cut -d= -f2)`
- Works for single keys; for multiple keys, repeat `-e` flags

---

## infra · Rule · docker compose run does not mount project data dir by default
> 2026-03-26 · source: finances-ezerpin
- `docker compose run` only mounts volumes defined in `docker-compose.yml` — project host directories are not mounted
- If scripts need access to files in `data/`, `data/reference/`, etc., add explicit `-v /host/path:/container/path` flag
- Example: `docker compose run --rm -v /opt/project/data:/app/data pipeline python script.py`

---

## infra · Rule · Server repo never auto-updates — always git pull before running pipeline
> 2026-03-26 · source: finances-ezerpin
- A server cloning a GitHub repo does NOT auto-update when you push — it stays on whatever commit it was at when you last SSH'd in and pulled
- Any `git push` from Mac → GitHub → must be followed by `git pull` on server before running pipelines
- Failure to pull = running stale code against prod data (silent divergence)
- Add `git pull` as the first step in any prod deployment runbook

---

## 2026-03-26 — docker-compose up -d without --build uses cached image

**Context**: added new FastAPI endpoint, pushed code, ran `git pull` on server + `docker-compose up -d` — new route not visible. API still served old image.

**Lesson**: `docker-compose up -d` alone never rebuilds the image — it reuses whatever image was last built. New code is NOT picked up.

**Fix**: `docker-compose build --no-cache && docker-compose stop && docker-compose rm -f && docker-compose up -d`
- `--build` flag on `up` triggers an interactive "Continue?" prompt via SSH — blocks non-interactive execution; use the split form above
- `--no-cache` forces layer invalidation when Docker incorrectly caches `COPY api/` step

---

## infra · Rule · Terraform modules must declare required_providers explicitly
> 2026-03-26 · source: hetzner-infra
- Terraform cannot infer provider namespace inside a module — defaults to `hashicorp/<name>` instead of e.g. `hetznercloud/hcloud`
- `terraform init` installs two conflicting providers and fails with "provider not found in registry"
- Fix: add `terraform { required_providers { hcloud = { source = "hetznercloud/hcloud" } } }` block in every module that uses a non-hashicorp provider

---

## 2026-03-25 — Rsync Nextcloud: exclude cache and internal folders

**Context**: first rsync of `/opt/nextcloud/files/` pulled Nextcloud app cache (preview thumbnails, theming) and internal trash/version history — massively inflating backup size with non-essential data.

**Folders to always exclude when rsyncing Nextcloud user data**:
- `appdata_oc8odmpvrrzm/` — Nextcloud app cache (preview thumbnails, theming icons)
- `admin/files_trashbin/` — Nextcloud internal trash bin (soft-deleted files with timestamps)
- `admin/files_versions/` — Nextcloud file version history
- `admin/files/Trash/` — user-facing trash folder

**Essential to keep**: `admin/files/Archive/` · `admin/files/Inbox/` · `admin/files/system/`

**Lesson**: always scope Nextcloud rsync to user data only. The named volume `nextcloud_nextcloud_data` contains both app code and user data — the bind mount at `/opt/nextcloud/files/` is cleaner but still includes internal Nextcloud folders.

---
