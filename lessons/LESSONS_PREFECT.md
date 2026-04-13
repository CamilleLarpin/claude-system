# Lessons — Prefect Orchestration

> Load when: building or debugging Prefect flows, Prefect Managed work pools, or Prefect deployment config.
> Never delete entries. Add date and context.

---

## [prefect] · Rule · Keep source modules Prefect-free — task wrappers in flow file only
> 2026-04-02 · source: pea-pme-pulse
- Adding `@task` to functions in source modules creates a Prefect dependency — breaks unit tests and couples business logic to the orchestrator
- Fix: write thin `@task` wrappers in `src/flows/` that call source module functions; source modules stay pure Python
- Benefit: source modules independently testable; swapping orchestrators only requires changes in `src/flows/`

## [prefect] · Rule · `pip install -e .` required for Prefect subflow context — sys.path hack won't work
> 2026-04-02 · source: pea-pme-pulse
- `sys.path.insert()` in the parent flow file has no effect in Prefect subflow subprocess context
- Fix: `pip install -e .` with `[tool.setuptools.packages.find] where = ["src"]` in pyproject.toml
- Checklist: (1) `__init__.py` in `src/<package>/`? (2) `packages.find where = ["src"]` in pyproject.toml? (3) reinstalled after changes?

## [prefect-managed] · Rule · Pull steps and flow run are separate processes — /tmp/ not shared
> 2026-04-02 · source: pea-pme-pulse
- In Prefect Managed work pools, the `pull` step and the flow run in separate processes — files written to `/tmp/` in pull steps are NOT accessible during flow execution
- Pass credentials/files via `job_variables.env` (env vars persist across the boundary)
- Pattern for GCP: Prefect Secret → `GOOGLE_APPLICATION_CREDENTIALS_JSON` env var in `job_variables` → write to `tempfile.NamedTemporaryFile` at flow module load time → set `os.environ["GOOGLE_APPLICATION_CREDENTIALS"]`

## [prefect] · Rule · Self-hosted Prefect: stale job_variables persist in SQLite DB after deploy
> 2026-04-08 · source: pea-pme-pulse
- `prefect deploy --all` does NOT clear existing `job_variables` from the DB — it merges/updates only fields present in the new config
- Removing a key from `prefect.yaml` does NOT remove it from the deployed config in the DB
- Fix: PATCH the API: `requests.patch('http://<host>/api/deployments/filter', ...)` to get IDs then PATCH each with `{'job_variables': {}}`
- Or nuclear reset: `docker compose down -v && docker compose up -d` (wipes SQLite DB) → redeploy
- Always verify with `prefect deployment inspect '<name>'` after deploy to confirm job_variables are clean

## [prefect] · Rule · Prefect Secret blocks store Python dict repr when migrating from Cloud — always use json.dumps()
> 2026-04-08 · source: pea-pme-pulse
- `Secret.load('key').get()` on Prefect Cloud returns a Python dict if the secret was originally stored as JSON — not a JSON string
- Saving that dict to a self-hosted server via `Secret(value=val).save()` stores Python repr (`{'key': 'val'}` with single quotes) — not valid JSON
- Fix: `json.dumps(val) if isinstance(val, dict) else val` before saving to ensure valid JSON string
- Verify the stored value: `repr(b.get()[:100])` — look for `{"` (valid) vs `{'` (broken)

## [gcp] · Rule · Attach SA to GCP VM for ADC — eliminates JSON key management entirely
> 2026-04-08 · source: pea-pme-pulse
- Instead of passing GCP SA JSON via env var/secret, attach the SA to the VM: `gcloud compute instances set-service-account <vm> --service-account=<sa> --scopes=cloud-platform`
- VM must be stopped first: `gcloud compute instances stop <vm>`; then restart; ADC works automatically in all subprocesses
- dbt: use `method: oauth` in profiles.yml (not `service-account`) — no keyfile line needed
- Eliminates the entire "JSON key → Secret block → env var → tempfile" chain

## [prefect+gcp] · Rule · Before rotating GCP SA keys, audit all Prefect Secret blocks referencing them
> 2026-04-09 · source: pea-pme-pulse
- Revoking a SA key breaks any deployment still using `GOOGLE_APPLICATION_CREDENTIALS_JSON` via a Secret block — fails at runtime, not at deploy time; no warning
- `prefect deploy --all` does NOT validate that Secret block values are still valid credentials
- Audit before rotating: `grep -r "gcp-sa-key\|CREDENTIALS_JSON" prefect.yaml` — any hit = update that flow to ADC (`method: oauth`) before revoking
- After migration to VM ADC, flows written pre-migration must be manually updated — they don't inherit ADC automatically

## [prefect] · Rule · Use non-editable install in prefect.yaml pull step
> 2026-04-09 · source: pea-pme-pulse
- `pip install -e .` writes `__editable__.<pkg>.pth` into container site-packages; `git_clone` wipes source dir each run but leaves the `.pth` — next run crashes with `OSError: [Errno 2] No such file or directory`
- Fix: `pip install ".[dev]"` — no `.pth` file, each run installs cleanly

## [prefect] · Rule · Crash-recovery loops nest clone directory — wipe manually to recover
> 2026-04-09 · source: pea-pme-pulse
- Prefect re-runs pull steps when loading `on_crashed` hooks with cwd already inside the cloned repo → `git_clone` nests: `repo/repo/repo/...`; after enough retries path exceeds OS limits and git clone itself starts failing
- Root fix: fix the crash (PR with the actual bug fix); VM fix: `rm -rf /opt/prefect/<repo-name>`

## [prefect] · Rule · Module-level env var reads crash at flow import time — must be in job_variables
> 2026-04-09 · source: pea-pme-pulse
- `os.environ.get("VAR")` / `os.environ["VAR"]` at module level runs when Prefect imports the flow file to check for hooks — before the flow function runs; missing var → `TypeError` or `KeyError` at import time, before any retry logic
- Fix: inject via `job_variables.env` in `prefect.yaml`, OR move reads inside the flow/task function
- Audit pattern: `grep -n "os.environ" src/flows/*.py` then check if any match is at module level (not inside a function/class)

## [gcs] · Rule · Use get_bucket before create_bucket — least-privilege SAs lack storage.buckets.create
> 2026-04-09 · source: pea-pme-pulse
- `create_bucket()` requires `storage.buckets.create` — a Storage Object Admin SA gets `Forbidden 403`; pattern that only catches `Conflict` (409) silently breaks when bucket exists and SA can't create
- Fix: `get_bucket()` first (only needs `storage.buckets.get`); `create_bucket()` only on `NotFound`

## [prefect] · Rule · Add dbt deps as explicit task before every dbt run — packages/ not persisted
> 2026-04-10 · source: pea-pme-pulse
- Prefect workers clone the repo fresh on each run; `dbt_packages/` is never persisted between runs
- Any `dbt run` fails with `Compilation Error: dbt found N package(s)... Run "dbt deps"` unless `dbt deps` runs first
- Fix: `@task(name="dbt-deps")` calling `subprocess.run(["dbt", "deps", "--project-dir", ...])` — no profiles dir needed; call before first dbt task in every flow

## [prefect] · Rule · Concurrent flows race on pip install — serialize with flock in pull step
> 2026-04-10 · source: pea-pme-pulse
- Multiple deployments starting simultaneously run `pip install` concurrently into the same shared container filesystem → `OSError: ...INSTALLERxxxxxx.tmp` (temp file created by one process, deleted by another)
- Fix: `flock /tmp/pip-install.lock pip install ".[dev]"` in `prefect.yaml` pull step — zero performance cost
- After changing `prefect.yaml` pull step: must run `prefect deploy --all` — pull step is stored in the deployment record on the server, not re-read from yaml at runtime

## [infra] · Rule · GCP VM resize wipes firewall-dependent routing — verify connectivity after any resize
> 2026-04-10 · source: pea-pme-pulse
- Resizing a GCP VM (stop → change machine type → start) does NOT affect GCP firewall rules — but nginx and other reverse proxies that were started manually (not via systemd) won't restart; also any firewall rule that was previously deleted but not noticed becomes obvious only after the restart
- After any VM resize: verify each exposed port (`curl http://<ip>/api/health`, `curl http://<ip>:<port>`) before declaring the VM healthy
- All Docker containers with `restart: unless-stopped` + Docker enabled on boot will restart correctly — only bare processes (non-systemd nginx, manual scripts) won't

## [prefect] · Rule · `run_deployment(timeout=0)` hides downstream failures — use direct subflow call instead
> 2026-04-10 · source: pea-pme-pulse
- `run_deployment(..., timeout=0)` = fire-and-forget: parent completes immediately; if downstream crashes, parent stays "Completed" — silent failure
- Direct subflow call (`flow_fn()`) = parent waits, parent fails red if subflow fails — 1 run in the UI covers the full pipeline
- Use `run_deployment` only when flows run on **different work pools** (resource isolation need); for same-pool chaining, always use direct subflow calls

## [prefect-managed] · Rule · Block placeholder must be the sole value in its YAML field
> 2026-04-02 · source: pea-pme-pulse
- `{{ prefect.blocks.secret.xxx }}` is only valid when it is the entire string value in a `prefect.yaml` field — no surrounding text
- Mixing it in a multiline `script:` raises: `ValueError: Only a single block placeholder is allowed in a string`
- Fix: pass secret as standalone value in `env:` field of `run_shell_script`, use `$MY_SECRET` shell var in the script body

## [prefect-managed] · Rule · sys.path.insert must precede all project imports in Prefect managed env
> 2026-04-07 · source: pea-pme-pulse
- Prefect loads flow scripts via `load_script_as_module` — runs the file top-to-bottom in a fresh Python process; pip editable-install .pth files are NOT retroactively loaded
- `sys.path.insert` placed after project imports → `ModuleNotFoundError` even though `pip install -e .` ran successfully in the pull step
- Fix: move `sys.path.insert(0, src_path)` to the very top of any flow file that imports from sibling packages
- Also: `prefect deploy --all` YAML parse errors silently fall back to interactive mode (no hard failure) — validate YAML separately with `python -c "import yaml; yaml.safe_load(open('prefect.yaml'))"` if deploy behaves unexpectedly

## [prefect] · Rule · Multiple work pools on a single VM = silent stuck runs
> 2026-04-11 · source: pea-pme-pulse
- A deployment pointing to a pool with no registered worker parks all runs as `Scheduled` forever — no error, no timeout
- Multiple pools (`bronze-pool`, `silver-pool`, `gold-pool`) on one VM with one worker only serve one pool at a time — others stall silently
- Fix: one pool per VM; use tags for layer filtering in the UI; start the worker with `--pool <single-pool-name>`

## [infra] · Rule · Check for existing systemd services before dockerizing a process on a VM
> 2026-04-11 · source: pea-pme-pulse
- A systemd service already running on a port will cause a Docker container binding that same port to crash with `[Errno 98] address already in use` — kill attempts fail because systemd auto-restarts (new PID each time)
- Detect first: `sudo systemctl list-units --type=service --state=running | grep <keyword>`
- If systemd service is already robust (`restart=always` equivalent), prefer it — no need to dockerize
- Applies to any process you intend to containerize on a VM with existing services

## [infra] · Rule · nginx /var/www/ is root-owned — scp to home dir first, then sudo mv
> 2026-04-13 · source: pea-pme-pulse
- `gcloud compute scp` (or any scp) directly to `/var/www/` fails with "Permission denied" — nginx static dirs are root-owned
- Fix: `gcloud compute scp <files> <vm>:~` → `gcloud compute ssh <vm> --command="sudo mv ~/<files> /var/www/<dir>/"`
- No nginx restart needed — static files are served on-read; only the directory ownership matters

## [prefect-cloud] · Rule · Prefect Cloud free tier: 5 deployment hard limit per workspace
> 2026-04-07 · source: pea-pme-pulse
- Exceeding 5 deployments → HTTP 403 `ObjectLimitReached` — no warning before the limit is hit
- For team projects with multiple contributors: 5 slots fill quickly; plan ahead
- Self-hosting Prefect Server (Docker Compose on any VM) removes the limit entirely — same CLI/API, same prefect.yaml, just a different `PREFECT_API_URL`
