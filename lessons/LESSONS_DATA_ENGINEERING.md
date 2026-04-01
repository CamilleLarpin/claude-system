# Lessons — data engineering, dbt, DuckDB

> Scope: data pipelines, dbt models, DuckDB, transaction processing, categorization pipelines.
> Load when: working on finances-ezerpin · data pipeline projects · dbt/DuckDB debugging.
> General architecture lessons → LESSONS_ARCHITECTURE.md · dlt-specific → LESSONS_DLT.md

---

## [dbt] · Rule · `dbt seed` is not included in `dbt run` — must be run separately
> 2026-03-27 · source: finances-ezerpin
- `dbt run` executes SQL models only — it does NOT load seeds
- After adding or modifying a seed file (and deploying to prod), always run `dbt seed --select <seed_name>` explicitly
- Failure to do so causes downstream models referencing the seed to fail with `Table with name <seed> does not exist`
- Seeds = stable reference data (categories, budgets, revenues) — intentionally excluded from the monthly cron run; load manually after each schema change

---

## [data-engineering] · Guideline · RSS feeds require User-Agent header — direct feedparser call returns 403
> 2026-03-30 · source: pea-pme-pulse
- `feedparser.parse(url)` called directly returns HTTP 403 on ABCBourse (and likely other financial RSS feeds)
- Always wrap with `requests.get(url, headers={"User-Agent": "Mozilla/5.0 ..."})` then `feedparser.parse(r.text)`
- Yahoo Finance FR RSS does not require User-Agent — ABCBourse does

## [data-engineering] · Guideline · Boursorama HTML scraping — ISIN lives in `<h2 class="c-faceplate__isin">`
> 2026-03-30 · source: pea-pme-pulse
- ISIN is not in the listing page — must scrape each ticker's detail page `/cours/{ticker}/`
- Target: `soup.find(class_="c-faceplate__isin").text.strip().split()[0]` (tag contains "FR0004040608 ABCA")
- Regex on full page text misses it on some tickers — class-targeted lookup is reliable across all 5 tested
- 0.5s delay between requests · User-Agent required

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

## [duckdb] · Rule · `strftime` argument order is (format, value) — opposite of SQLite
> 2026-03-26 · source: finances-ezerpin
- `strftime('%Y-%m', column)` is correct in DuckDB — format string first, value second
- `strftime(column, '%Y-%m')` may compile without error but returns wrong results or null
- Opposite of SQLite's `strftime(format, time, ...)` — easy to get wrong when porting SQL across dialects

## [duckdb] · Rule · Query raw source tables to filter intra-month; bypass aggregated marts
> 2026-03-26 · source: finances-ezerpin
- `fct_depenses_mensuelles` (or any mart aggregated by full month) can't be filtered to day N within a month
- For MoM comparison with same-day cutoff (e.g. March 1-26 vs Feb 1-26): query `stg_transactions` directly with `day(date_op) <= ?`
- Pattern: `get_cutoff_day()` = `day(max(date_op))` for the reported month → pass as parameter to both CTEs (current + previous)

## [data-engineering] · Rule · RSS feeds are ephemeral — GCS dump must happen before any filtering
> 2026-03-31 · source: pea-pme-pulse
- RSS feeds have no history — if raw feed is not stored at fetch time, it's gone forever
- GCS dump must precede all matching/filtering logic
- Contrast: AMF (full history via API, GCS for auditability) · yfinance (always re-fetchable, no GCS needed)
- Pattern: fetch → dump to GCS → filter/match → load to BQ Bronze (matched only)

## [data-engineering] · Rule · Fuzzy matching at scale — adaptive scorer by name length
> 2026-03-31 · source: pea-pme-pulse
- `partial_ratio` on short names (<=6 chars) produces false positives at scale — short strings appear as substrings anywhere
- Use `token_set_ratio` for short names (requires whole-token match), `partial_ratio` for longer names
- `fuzz.ratio` also fails for short names: length mismatch between query and name causes low scores even on exact hits
- Threshold: `len(name) <= 6` as cutoff — adjust per domain

## [data-engineering] · Rule · Fuzzy match on free-text titles — three false positive guards required
> 2026-04-01 · source: pea-pme-pulse
- When fuzzy-matching company names against news article titles, three distinct patterns cause false positives:
  1. **Substring in long word**: short name appears inside a common word (e.g. "NEURONES" in "Euronext") — fix: word-boundary regex post-match
  2. **Generic name**: company name is a common word ("OPTION", "CAPITAL") — fix: blocklist checked before fuzzy scoring
  3. **Source attribution suffix**: Google News appends `- source.com` to titles — fix: strip trailing `- word.tld` before matching
- Apply in sequence: `clean_title()` → blocklist check → fuzzy score → word boundary validation
- Validated: reduces false positives from 3/10 to 0/20 on Google News FR financial feeds

## [data-engineering] · Rule · Team PRs — check test import style against shared pythonpath setting
> 2026-04-01 · source: pea-pme-pulse
- `pythonpath = ["src"]` in pyproject.toml means `import src.bronze.xxx` breaks in tests — Python is already inside `src/`, can't find a folder named `src` there
- All branches must use `from bronze.xxx import` when `pythonpath = ["src"]` is set
- When reviewing a team PR: verify test import style is consistent with the project's `pythonpath` setting, especially when two branches both touch `pyproject.toml`

## [dbt] · Rule · Surrogate keys on bank transactions need `date_val` + `row_number` tiebreaker
> 2026-03-24 · source: finances-ezerpin
- `generate_surrogate_key(['date_op', 'label', 'amount', 'account'])` produces collisions when: (1) same `date_op` but different `date_val` (SNCF pattern), (2) genuine duplicate transactions same day (LEA GIRAUD -168€ ×2)
- Fix: add `date_val` to the key (resolves case 1) + `row_number() OVER (PARTITION BY date_op, date_val, label, amount, account ORDER BY _loaded_at)` cast as varchar (resolves case 2)
- Key change orphans all downstream predictions — budget for a full re-run of any LLM pipeline that joins on transaction_id; `labeled_corrections` few-shot survives intact
- Add `date_val` + tiebreaker from the start on any bank transaction surrogate key
