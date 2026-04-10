# Lessons — Infrastructure & Operations

> Load when: setting up backups · configuring servers · Docker · Terraform · orchestration · SSH.
> Never delete entries. Add date and context.
> Security/credentials lessons → LESSONS_SECURITY.md

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

## [infra] · Rule · ngrok v3 config format: `version: "3"` + `agent.authtoken`
> 2026-04-09 · source: pea-pme-pulse
- ngrok v3 (3.4+) uses `version: "3"` with authtoken nested under `agent:` — top-level `authtoken` causes `field authtoken not found in type config.v3yamlConfig`
- Old v2 config (`version: '2'` + top-level `authtoken`) causes TLS cert errors on v3 binary: `failed to send authentication request: x509: certificate signed by unknown authority`
- Correct format: `version: "3"\nagent:\n  authtoken: <token>`
- Verify config: `ngrok config check` · diagnose connectivity: `ngrok diagnose`

## [shell] · Rule · `source .env` does not export variables to child processes — use `set -a`
> 2026-04-07 · source: pea-pme-pulse
- `source .env` sets variables in the current shell but does NOT export them — child processes (Python, subprocess, etc.) don't inherit them
- `echo $VAR` prints the value (same shell process) but `python -c "import os; print(os.environ['VAR'])"` raises KeyError
- Fix: `set -a && source .env && set +a` — `set -a` auto-exports every variable until `set +a`
- Alternative: `export $(grep -v '^#' .env | xargs)` — breaks on values containing spaces

## [infra] · Rule · Nextcloud behind nginx: config.php overwrite settings required for mobile OAuth
> 2026-04-07 · source: family-content-manager
- Nextcloud mobile app login hung indefinitely at the OAuth grant screen — no error shown
- Nextcloud was running in Docker on HTTP:8080 with nginx terminating HTTPS; without `overwriteprotocol`, Nextcloud generates `http://` redirect URLs — the mobile app rejects or loops on them
- Fix: three entries in `config.php`: `'overwrite.cli.url' => 'https://your-domain.com'` (was `http://localhost`) · `'overwriteprotocol' => 'https'` · `'overwritehost' => 'your-domain.com'`
- nginx proxy headers (`X-Forwarded-Proto`, `X-Real-IP`, `X-Forwarded-For`) are necessary but not sufficient on their own

## [prefect-managed] · Rule · sys.path.insert must precede all project imports in Prefect managed env
> 2026-04-07 · source: pea-pme-pulse
- Prefect loads flow scripts via `load_script_as_module` — runs the file top-to-bottom in a fresh Python process; pip editable-install .pth files are NOT retroactively loaded
- `sys.path.insert` placed after project imports → `ModuleNotFoundError` even though `pip install -e .` ran successfully in the pull step
- Fix: move `sys.path.insert(0, src_path)` to the very top of any flow file that imports from sibling packages
- Also: `prefect deploy --all` YAML parse errors silently fall back to interactive mode (no hard failure) — validate YAML separately with `python -c "import yaml; yaml.safe_load(open('prefect.yaml'))"` if deploy behaves unexpectedly

## [prefect-cloud] · Rule · Prefect Cloud free tier: 5 deployment hard limit per workspace
> 2026-04-07 · source: pea-pme-pulse
- Exceeding 5 deployments → HTTP 403 `ObjectLimitReached` — no warning before the limit is hit
- For team projects with multiple contributors: 5 slots fill quickly; plan ahead
- Self-hosting Prefect Server (Docker Compose on any VM) removes the limit entirely — same CLI/API, same prefect.yaml, just a different `PREFECT_API_URL`

## [nginx] · Rule · `alias` + `try_files` causes internal redirect loop for static file serving
> 2026-04-09 · source: pea-pme-pulse
- `alias /path/` combined with `try_files $uri $uri/ /prefix/index.html` → nginx enters an infinite internal redirect loop (500)
- Fix: use `alias /path/;` + `index index.html;` only — no `try_files` needed for static single-page apps served at a sub-path
- Host-side files are invisible to the nginx container — must be volume-mounted into the container via `docker-compose.yml`

## [cron] · Rule · Gmail after: filters by date not time — ID dedup required for cron scripts
> 2026-03-31 · source: gmail-inbox-cleanup phase 1
- Gmail API `q="after:{unix_seconds}"` treats the timestamp as a date boundary — all emails from the current calendar date are returned regardless of exact time
- A cron script using only checkpoint timestamp will re-fetch and re-process all same-day emails on every run → duplicates, double-trashing
- Fix: maintain a set of processed message IDs (from an audit/decisions log) and filter fetched emails against it before processing; use the timestamp only to prune the API query, not as the sole dedup mechanism

## [deployment] · Rule · Streamlit Cloud ignores pyproject.toml — needs root requirements.txt
> 2026-04-10 · source: pea-pme-pulse
- Streamlit Cloud does not parse `pyproject.toml` — only `requirements.txt` at repo root (or `streamlit/requirements.txt`)
- Keep it minimal: only what the dashboard file imports; don't copy the full project deps
- `pandas .style.background_gradient()` requires `matplotlib` at runtime even without a direct import — omitting it causes a runtime crash in any styled dataframe rendering

---
