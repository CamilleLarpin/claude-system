# Lessons — data engineering, dbt, DuckDB

> Scope: data pipelines, dbt models, DuckDB, transaction processing, categorization pipelines.
> Load when: working on finances-ezerpin · data pipeline projects · dbt/DuckDB debugging.
> General architecture lessons → LESSONS_ARCHITECTURE.md · dlt-specific → LESSONS_DLT.md

---

## [data-engineering] · Guideline · Source table naming — system/source first, not owner/entity first
> 2026-03-16 · source: finances-ezerpin
- When raw tables represent data from external systems (banks, APIs, SaaS tools), name them `<system>_<scope>` not `<owner>_<system>` — e.g. `boursorama_joint`, not `joint_boursorama`
- The primary differentiator at the raw layer is the source system (it determines schema, pipeline, freshness) — ownership is an attribute inside the data, not a table name prefix
- In a DB explorer, tables sort alphabetically — system-first groups related sources together (`boursorama_joint`, `boursorama_perso`); owner-first scatters them (`camille_boursorama`, `camille_revolut`, `joint_boursorama`)

## [data-engineering] · Rule · French bank amounts use space as thousands separator
> 2026-03-17 · source: finances-ezerpin
- French bank CSV exports (Boursorama, Crédit Mutuel) use space (or `\u00a0`) as thousands separator: `-1 179.63`, `-1 875,00`
- `float(value.replace(",", "."))` fails with `ValueError` on these — silent until a transaction > 999€ appears
- Fix: `value.strip().replace("\u00a0", "").replace(" ", "").replace(",", ".")` before `float()`
- Always test amount parser on values > 999 when integrating any French bank data source

## [data-engineering] · Guideline · LLM beats sklearn for transaction categorization under ~5k rows/month
> 2026-03-18 · source: finances-ezerpin
- At ~750 transactions/month, Claude Haiku costs ~$0.04/month — sklearn adds training pipeline, model artifacts, and retraining overhead for no cost saving
- sklearn also has a cold-start problem: zero-shot on new categories; LLM handles them immediately
- LLM improves via few-shot examples from stored corrections (no retraining); sklearn requires explicit retraining cycle
- Reassess if volume exceeds ~5k transactions/month (cost becomes non-trivial)

## [data-engineering] · Note · dbt Fusion → dbt Core migration is a binary swap only
> 2026-03-18 · source: finances-ezerpin
- dbt Fusion installs as a standalone binary (not pip) — `pip uninstall dbt-fusion` finds nothing; remove with `rm ~/.local/bin/dbt`
- All SQL models, YAML, tests, seeds, macros are 100% compatible — no file changes needed
- Fusion's `arguments:` syntax for tests is Fusion-specific; Core 1.x uses standard dbt syntax

## [duckdb] · Rule · `UPDATE ... RETURNING *` conflicts with primary key in DuckDB
> 2026-03-19 · source: ai-networking-system
- `UPDATE table SET x=? WHERE id=? RETURNING *` throws `ConstraintException: Duplicate key ... violates primary key constraint` — DuckDB's RETURNING implementation re-evaluates the PK constraint after update
- Fix: split into two statements: `UPDATE ... SET ... WHERE id=?` then `SELECT * ... WHERE id=?`

## [dbt] · Rule · Never join externally-written tables inside a dbt incremental model
> 2026-03-24 · source: finances-ezerpin
- Incremental models write each row once (at insert time) — a LEFT JOIN on an external table (written by a pipeline, not dbt) produces NULL for that row permanently, even after the external table is updated
- Pattern that fails: `stg_transactions` (incremental) joins `raw.category_predictions` (written by Python pipeline after staging runs)
- Fix: move the join to the first non-incremental downstream model (view or table) — it rebuilds fully each run and always sees fresh data
- Rule: if a table is written by an external process on a different schedule, join it in a non-incremental model

## [dbt] · Rule · Surrogate keys on bank transactions need `date_val` + `row_number` tiebreaker
> 2026-03-24 · source: finances-ezerpin
- `generate_surrogate_key(['date_op', 'label', 'amount', 'account'])` produces collisions when: (1) same `date_op` but different `date_val` (SNCF pattern), (2) genuine duplicate transactions same day (LEA GIRAUD -168€ ×2)
- Fix: add `date_val` to the key (resolves case 1) + `row_number() OVER (PARTITION BY date_op, date_val, label, amount, account ORDER BY _loaded_at)` cast as varchar (resolves case 2)
- Key change orphans all downstream predictions — budget for a full re-run of any LLM pipeline that joins on transaction_id; `labeled_corrections` few-shot survives intact
- Add `date_val` + tiebreaker from the start on any bank transaction surrogate key
