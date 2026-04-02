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

## infra · Rule · After `terraform import`, review every "to add" in plan before any apply
> 2026-03-26 · source: hetzner-infra Phase 2
- `terraform import` adds one resource to state — all other resources in `.tf` code but not in state still appear as "to add" in the next plan
- After a partial import, plan will show N resources to add — this is expected but NOT safe to apply blindly
- Inspect every "to add" entry: new resource (safe) vs existing resource not yet imported (would create a duplicate on the provider)

---

## infra · Rule · Terraform modules must declare required_providers explicitly
> 2026-03-26 · source: hetzner-infra
- Terraform cannot infer provider namespace inside a module — defaults to `hashicorp/<name>` instead of e.g. `hetznercloud/hcloud`
- `terraform init` installs two conflicting providers and fails with "provider not found in registry"
- Fix: add `terraform { required_providers { hcloud = { source = "hetznercloud/hcloud" } } }` block in every module that uses a non-hashicorp provider

---

## infra · Rule · `crontab -e` fails with ghostty terminal over SSH — use pipe instead
> 2026-03-27 · source: finances-ezerpin
- `crontab -e` over SSH from a ghostty terminal fails with `Error opening terminal: xterm-ghostty` — the editor can't open because the remote server doesn't have the ghostty terminfo entry
- Fix: pipe the cron line directly without opening an editor:
  `echo '<cron line>' | ssh server 'crontab -'`
  or locally: `echo '<cron line>' | ssh server 'EDITOR=true crontab -'`
- Verify with: `ssh server 'crontab -l'`
- General pattern: any `crontab -e` (or other TUI editor) over SSH from an unusual terminal emulator will fail if the server lacks the terminfo entry

---

## infra · Rule · Run multi-command server scripts via scp + ssh, not interactive paste
> 2026-03-31 · source: finances-ezerpin
- Pasting multi-line commands into an SSH terminal is unreliable: line breaks are interpreted as command separators, leading lines are stripped, and heredocs fail if indented
- Reliable pattern: write the script locally, scp it, execute remotely
  `scp /tmp/script.sh server:/tmp/script.sh && ssh server bash /tmp/script.sh`
- Or pipe directly without creating a file on the server: `ssh server 'bash -s' < local_script.sh`
- Always add `cd /path/to/project` as first line of any server script — `ssh server bash script.sh` runs from `$HOME`, not the project dir

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

## [github] · Rule · Fine-grained PAT scoped to specific repos → 404 on unlisted private repos
> 2026-04-01 · source: Ghost n8n debug session
- GitHub returns 404 (not 403) for private repos not in the PAT's allowed list — designed to avoid leaking repo existence
- A PAT configured for "selected repos" silently excludes any new repos you create later
- If a service (e.g. n8n workflow) needs to read/write across multiple private repos: scope the PAT to "All repositories" or explicitly add each new repo when created
- Diagnosis: 404 from `GET /repos/{owner}/{repo}/contents/...` with a valid PAT = repo not in PAT scope (or doesn't exist)

---

## [cron] · Rule · Gmail after: filters by date not time — ID dedup required for cron scripts
> 2026-03-31 · source: gmail-inbox-cleanup phase 1
- Gmail API `q="after:{unix_seconds}"` treats the timestamp as a date boundary — all emails from the current calendar date are returned regardless of exact time
- A cron script using only checkpoint timestamp will re-fetch and re-process all same-day emails on every run → duplicates, double-trashing
- Fix: maintain a set of processed message IDs (from an audit/decisions log) and filter fetched emails against it before processing; use the timestamp only to prune the API query, not as the sole dedup mechanism

---
