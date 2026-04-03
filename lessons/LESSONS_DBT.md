# Lessons — dbt

> Scope: dbt models, materialization strategies, BigQuery adapter, schema config, surrogate keys.
> Load when: working on any dbt model · dbt debugging · adding a new dbt layer.
> Data engineering (non-dbt) → LESSONS_DATA_ENGINEERING.md

---

## [dbt] · Rule · `dbt seed` is not included in `dbt run` — must be run separately
> 2026-03-27 · source: finances-ezerpin
- `dbt run` executes SQL models only — it does NOT load seeds
- After adding or modifying a seed file (and deploying to prod), always run `dbt seed --select <seed_name>` explicitly
- Failure to do so causes downstream models referencing the seed to fail with `Table with name <seed> does not exist`
- Seeds = stable reference data (categories, budgets, revenues) — intentionally excluded from the monthly cron run; load manually after each schema change

## [dbt] · Rule · Never join externally-written tables inside a dbt incremental model
> 2026-03-24 · source: finances-ezerpin
- Incremental models write each row once (at insert time) — a LEFT JOIN on an external table (written by a pipeline, not dbt) produces NULL for that row permanently, even after the external table is updated
- Pattern that fails: `stg_transactions` (incremental) joins `raw.category_predictions` (written by Python pipeline after staging runs)
- Fix: move the join to the first non-incremental downstream model (view or table) — it rebuilds fully each run and always sees fresh data
- Rule: if a table is written by an external process on a different schedule, join it in a non-incremental model

## [dbt] · Note · dbt Fusion → dbt Core migration is a binary swap only
> 2026-03-18 · source: finances-ezerpin
- dbt Fusion installs as a standalone binary (not pip) — `pip uninstall dbt-fusion` finds nothing; remove with `rm ~/.local/bin/dbt`
- All SQL models, YAML, tests, seeds, macros are 100% compatible — no file changes needed
- Fusion's `arguments:` syntax for tests is Fusion-specific; Core 1.x uses standard dbt syntax

## [dbt] · Rule · BigQuery PARSE_TIMESTAMP — use %Z for timezone names, %z for numeric offsets
> 2026-04-02 · source: pea-pme-pulse
- RFC 2822 strings from RSS feeds end in `GMT` (timezone name), not `+0000` (numeric offset)
- `%z` silently returns NULL on `GMT` — no error, just missing data
- Fix: `SAFE.PARSE_TIMESTAMP('%a, %d %b %Y %H:%M:%S %Z', col)` — `%Z` handles `GMT`, `UTC`, named zones
- `SAFE.` prefix is always correct here: returns NULL on parse failure instead of crashing the query

## [dbt] · Rule · dbt default schema generates double-prefix — override with generate_schema_name macro
> 2026-04-02 · source: pea-pme-pulse
- `+schema: silver` in `dbt_project.yml` + `dataset: silver` in `profiles.yml` → BQ creates `silver_silver`
- Fix: `macros/generate_schema_name.sql` returning `custom_schema_name` directly when set
- Standard pattern for projects with explicit dataset names (not environment-prefixed)
- Macro: `{%- if custom_schema_name is none -%}{{ target.schema }}{%- else -%}{{ custom_schema_name | trim }}{%- endif -%}`

## [dbt] · Rule · Surrogate keys on bank transactions need `date_val` + `row_number` tiebreaker
> 2026-03-24 · source: finances-ezerpin
- `generate_surrogate_key(['date_op', 'label', 'amount', 'account'])` produces collisions when: (1) same `date_op` but different `date_val` (SNCF pattern), (2) genuine duplicate transactions same day (LEA GIRAUD -168€ ×2)
- Fix: add `date_val` to the key (resolves case 1) + `row_number() OVER (PARTITION BY date_op, date_val, label, amount, account ORDER BY _loaded_at)` cast as varchar (resolves case 2)
- Key change orphans all downstream predictions — budget for a full re-run of any LLM pipeline that joins on transaction_id; `labeled_corrections` few-shot survives intact
- Add `date_val` + tiebreaker from the start on any bank transaction surrogate key

## [dbt] · Rule · dbt incremental — fetched_at watermark + intra-batch QUALIFY dedup
> 2026-04-02 · source: pea-pme-pulse
- Watermark filter: `fetched_at > (select max(fetched_at) from {{ this }})` — both sources share the same Silver max; safe when all Bronze flows finish before dbt runs once
- Still need `QUALIFY row_number() OVER (PARTITION BY row_id ORDER BY fetched_at DESC) = 1` — deduplicates within the incoming batch (same article from two sources in the same run)
- Surrogate key: `to_hex(md5(concat(lower(title), '|', isin)))` — stable across sources, matches prior dedup semantics
- Test the NO-OP path: run `dbt run` with no new Bronze data → expect `MERGE (0.0 rows)` in output

## [dbt] · Rule · on_schema_change='fail' blocks runs when a new column is added to an incremental model
> 2026-04-03 · source: pea-pme-pulse
- Adding a column to an incremental model SQL while the BQ table was created before that column → dbt raises `Compilation Error: source and target schemas out of sync`
- `on_schema_change='fail'` is the dbt default — always override with `'append_new_columns'` on incremental models
- If the new column is the `unique_key` (e.g. `row_id`): NULL values on old rows break merge dedup → run `dbt run --full-refresh --select <model>` once to rebuild cleanly
- Local full-refresh works with oauth dev profile: `cd dbt && dbt run --full-refresh --select <model>`

## [dbt] · Rule · Generate dbt service-account profile at runtime — never commit keyfile path
> 2026-04-02 · source: pea-pme-pulse
- On managed infra (Prefect, CI), no `gcloud auth` — build `profiles.yml` at task runtime using `GOOGLE_APPLICATION_CREDENTIALS` (tempfile path of SA key JSON)
- Pattern: `with tempfile.TemporaryDirectory() as d: write profiles.yml → dbt run --profiles-dir d --project-dir <dbt/>`
- Local dev fallback: if `GOOGLE_APPLICATION_CREDENTIALS` not set → omit `--profiles-dir` → dbt uses `~/.dbt/profiles.yml` (oauth)
- Never commit a `profiles.yml` with `method: service-account` — keyfile path is process-local and ephemeral
