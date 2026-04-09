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

## [prefect-managed] · Rule · Block placeholder must be the sole value in its YAML field
> 2026-04-02 · source: pea-pme-pulse
- `{{ prefect.blocks.secret.xxx }}` is only valid when it is the entire string value in a `prefect.yaml` field — no surrounding text
- Mixing it in a multiline `script:` raises: `ValueError: Only a single block placeholder is allowed in a string`
- Fix: pass secret as standalone value in `env:` field of `run_shell_script`, use `$MY_SECRET` shell var in the script body
