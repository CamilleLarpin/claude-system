# Lessons — dlt (data load tool)

> Load when: building or debugging dlt pipelines — ingestion, normalization, schema behavior.

---

## [data-ingestion] · Rule · Bank export filename ≠ date range — always verify actual span
> 2026-03-23 · source: finances-ezerpin
- A Boursorama export named for the date it was pulled (`export-operations-16-03-2026`) contained data from Dec 2023 → Jan 2026 — 722 rows from 2024 + 580 from 2025
- Banks export the full history available at export time regardless of any date intent; the filename reflects the export date, not the data range
- Always audit the actual date range after loading: `SELECT MIN(date_op), MAX(date_op), COUNT(*) FROM raw.table`
- Applies to any bank/financial CSV — never assume the file covers only the expected period

## [dlt] · Rule · dlt caches pipeline destination by pipeline_name — clear before first prod run
> 2026-03-31 · source: finances-ezerpin
- dlt stores pipeline state (including the destination DB path) in `~/.dlt/pipelines/<pipeline_name>/`
- If a pipeline was run locally with `--db data/dev.duckdb`, the cached destination persists and will be reused on the server even if you pass `--db /data/finances.duckdb`
- Always verify the line `The duckdb destination used duckdb://...` in dlt output — it shows the actual destination, not the argument
- Fix: `rm -rf ~/.dlt/pipelines/<pipeline_name>/` on the server before the first prod run, or use a distinct `pipeline_name` per environment

---

## [dlt] · Rule · dlt normalizes column names camelCase → snake_case
> 2026-03-17 · source: finances-ezerpin
- dlt automatically normalizes column names on load: `dateOp` → `date_op`, `supplierFound` → `supplier_found`, `categoryParent` → `category_parent`
- Exception: already-lowercase names like `accountbalance` stay as-is (no underscore inserted)
- dbt models written against dlt-loaded tables must use normalized names, not original CSV names — mismatch causes "column not found" errors at compile time
- After any new dlt pipeline: inspect actual column names in DB before writing dbt models
