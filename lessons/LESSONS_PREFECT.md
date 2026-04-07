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

## [prefect-managed] · Rule · Block placeholder must be the sole value in its YAML field
> 2026-04-02 · source: pea-pme-pulse
- `{{ prefect.blocks.secret.xxx }}` is only valid when it is the entire string value in a `prefect.yaml` field — no surrounding text
- Mixing it in a multiline `script:` raises: `ValueError: Only a single block placeholder is allowed in a string`
- Fix: pass secret as standalone value in `env:` field of `run_shell_script`, use `$MY_SECRET` shell var in the script body
