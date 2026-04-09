# Lessons — data engineering, DuckDB

> Scope: data pipelines, DuckDB, transaction processing, fuzzy matching, RSS, bank data.
> Load when: working on finances-ezerpin · pea-pme-pulse · any data pipeline project.
> dbt-specific → LESSONS_DBT.md · dlt-specific → LESSONS_DLT.md · architecture → LESSONS_ARCHITECTURE.md

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
- In a DB explorer, tables sort alphabetically — system-first groups related sources together (`boursorama_joint`, `boursorama_perso`); owner-first scatters them

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

## [duckdb] · Rule · `UPDATE ... RETURNING *` conflicts with primary key in DuckDB
> 2026-03-19 · source: ai-networking-system
- `UPDATE table SET x=? WHERE id=? RETURNING *` throws `ConstraintException: Duplicate key ... violates primary key constraint` — DuckDB's RETURNING implementation re-evaluates the PK constraint after update
- Fix: split into two statements: `UPDATE ... SET ... WHERE id=?` then `SELECT * ... WHERE id=?`

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

## [git] · Rule · Conflict markers committed to a data file cause silent production KeyError
> 2026-04-03 · source: pea-pme-pulse
- Merging a PR with unresolved conflict markers in a CSV file breaks all downstream consumers silently — pandas reads `<<<<<<< HEAD` as the header row, so expected columns don't exist → `KeyError` on every run
- GitHub does not block merging a branch with conflict markers in binary/text data files — it only warns on code files in some contexts
- Detection: `git show origin/main:<file> | head -3` to check for markers in prod · `grep -n "^<<<<" <file>` locally
- Fix: hotfix branch → clean file → fast PR → merge; trigger manual flow run to confirm
- Prevention: CI pre-commit hook grepping `^<<<<<<<` in CSV/JSON files in the repo

## [bigquery] · Rule · Verify BQ column type per-table before applying a type-cast fix
> 2026-04-08 · source: pea-pme-pulse
- Applied the same `match_score.astype(str)` fix to two Bronze tables — correct for `yahoo_rss` (STRING column) but caused `ArrowInvalid` on `google_news_rss` (FLOAT column)
- Tables in the same dataset and pipeline can have divergent schemas — never assume same column type across tables
- Diagnosis command: `bq show --schema <project>:<dataset>.<table>` · filter with `jq` or python
- Fix: cast to whatever type the BQ column actually declares, not a uniform type across tables

## [bigquery] · Rule · BQ external table backed by GCS auto-refreshes on object overwrite
> 2026-04-09 · source: pea-pme-pulse
- A BQ external table pointing to a GCS path reads the file at query time — overwriting the GCS object immediately makes the new data available; no DDL or cache invalidation needed
- The ingestion flow only needs to write to GCS (`blob.upload_from_string()`); no BQ write step required
- Limitation: no partition filter support, no BQ table history — if history matters, write to a native BQ table instead and reserve external tables for reference data that changes infrequently

## [git] · Rule · Rebase team PR branches before merging — resolves conflicts one commit at a time
> 2026-04-02 · source: pea-pme-pulse
- When multiple branches diverge from main, each branch accumulates conflicts with main as other PRs merge
- Fix: `git fetch origin main && git rebase origin/main` — replays each commit individually, surfaces conflicts per-commit, produces clean linear history
- In rebase conflict: `--ours` = main (the branch rebasing onto), `--theirs` = the commit being replayed
- After rebase: `git push --force-with-lease` (safer than `--force` — fails if remote was updated since your last fetch)

## [data-engineering] · Rule · SQL and Python dual implementations diverge on division-by-zero edge cases
> 2026-04-09 · source: pea-pme-pulse
- SQL `nullif(BB_upper - BB_lower, 0)` returns NULL when band width = 0 → falls through to `else 1.0` (neutral)
- Python `pct_b = (Close - BB_lower) / band_width` with `band_width = 0` → pandas float division returns `inf` (not NaN) → downstream comparisons (`inf > 0.8`) produce wrong signal (bearish instead of neutral)
- Pattern: whenever you maintain a dual SQL + Python implementation of the same scoring/transformation logic, explicitly test the `NULL` / `NaN` / zero-denominator path in both — the languages handle silent errors differently
- Fix for Python: `band_width = band_width.replace(0, float("nan"))` before dividing; NaN propagates cleanly through comparisons like SQL NULL

## [docker] · Rule · Validate Docker image end-to-end locally before declaring a PR ready
> 2026-04-02 · source: pea-pme-pulse
- `docker build` passing proves the image builds — it does NOT prove the application runs inside it
- Full validation: `docker run --env-file .env -v /path/to/gcp_creds.json:/tmp/gcp_adc.json:ro <image> python src/flows/<flow>.py`
- Common failure mode: credentials masked by `prefect config view` (outputs `'********'`) — read API key directly from `~/.prefect/profiles.toml`
- `.env` must be gitignored; `GOOGLE_CLOUD_PROJECT` must be set explicitly or GCP SDK emits a warning and some APIs fail silently
