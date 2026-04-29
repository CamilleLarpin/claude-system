# Decisions — Build: Data Pipelines

> Load when: building a data pipeline · dbt model · Prefect orchestration · financial data ingestion.
> NOT HERE: AI agents (→ DECISIONS_BUILD_AGENTS.md), infra (→ DECISIONS_INFRA.md).
> Archive at 100 lines → DECISIONS_BUILD_DATA_ARCHIVE.md

---

## [data] ISIN as universal pivot key for French financial data pipelines
- **Decision**: use ISIN as the central join key across all French market data sources (AMF, yfinance, scraping) — build a master referential that maps ISIN → all other identifiers (ticker_bourso, nom, ticker_yahoo)
- **Rationale**: ISIN is the only identifier natively present in AMF and accepted directly by `yf.Ticker(isin)`; Boursorama tickers are internal and non-standard; RSS feeds have no identifier — fuzzy match on company name is the only option, with ISIN resolved via the master referential
- **Date**: 2026-03-30 · **Status**: active

## [data] Semantic layer YAML written for LLMs — four-file structure, single definition rule
- **Decision**: in any project combining dbt + NL interface, treat YAML as AI documentation. Four-file ownership: `definitions.md` (concepts via `{{ doc('term') }}`) · `sources.yml` (external table declarations + column docs) · layer `schema.yml` (model docs + business context incl. when-to-use/when-not-to-use) · agent context file (routing keywords + example questions + query patterns only). 100% column coverage required. No concept defined in two places.
- **Rationale**: NL interfaces consume the semantic layer at query time — ambiguity causes silent misinterpretation; `sources.yml` vs `schema.yml` split follows dbt convention; agent context file adds only what schema.yml structurally can't express. Validated in pea-pme-pulse 2026-04-07.
- **Date**: 2026-04-07 (refined from 2026-03-17) · **Status**: active

## [data-pipeline] Extract shared matching/scoring logic into a single module when multiple sources use the same pattern
- **Decision**: when ≥2 pipeline sources share the same matching or scoring logic, extract it into a dedicated module (e.g. `fuzzy_match.py`) rather than duplicating per-source
- **Rationale**: logic diverges silently across sources when duplicated — one source gets a guard fix, others don't; tests need to be written once not per-source; new sources just import the module
- **Date**: 2026-04-01 · **Status**: active

## [data-pipeline] Three-guard pattern for fuzzy matching on free-text titles
- **Decision**: apply three guards in sequence: (1) `clean_title()` — strip source attribution suffix, (2) blocklist — skip generic names, (3) `valid_match()` — post-match word-boundary regex validation
- **Rationale**: fuzzy scoring alone allows three distinct false positive patterns — substring in longer word, generic name coincidence, URL domain suffix; each guard targets one pattern. Validated: 0 false positives on 20 live Google News entries.
- **Date**: 2026-04-01 · **Status**: active

## [data-pipeline] dbt orchestration — CLI + Prefect, no dbt Cloud for team projects
- **Decision**: open-source dbt CLI for local dev · Prefect triggers `dbt run` in prod after upstream flows succeed · no dbt Cloud
- **Rationale**: dbt Cloud free tier = 1 seat, incompatible with team use; Prefect already live; conditioning Silver on Bronze success (not a blind cron) is only possible via Prefect; dev local = SQL runs in BQ directly from laptop
- **Date**: 2026-04-02 · **Status**: active

## [data-pipeline] dbt incremental merge on surrogate key for append-only sources
- **Decision**: for RSS/event sources that append rows, use `materialized='incremental'` + `unique_key='row_id'` + `incremental_strategy='merge'` + `fetched_at` watermark filter; surrogate key = `md5(lower(natural_key_1) || '|' || natural_key_2)`
- **Rationale**: full rebuild scans all source data each run — cost grows linearly with Bronze table size; incremental processes only new rows; surrogate key is stable across sources and preserves dedup semantics
- **Test**: run `dbt run` with no new data → must produce `MERGE (0.0 rows)` to confirm watermark works
- **Date**: 2026-04-02 · **Status**: active

## [data-pipeline] Prefect: one orchestrator per domain, direct subflow calls — never run_deployment for same-pool chaining
- **Decision**: each data domain has one Prefect deployment with a schedule; all downstream steps are called as direct subflows or tasks — never via `run_deployment()` on the same work pool
- **Rationale**: `run_deployment(timeout=0)` = fire-and-forget; parent appears "Completed" even if downstream crashes silently; direct subflow call = parent fails red immediately if any step fails
- **Date**: 2026-04-10 · **Status**: active

## [data-pipeline] dbt Silver/Gold layer separation — clean vs enrich
- **Decision**: Bronze→Silver = cleaning only (dedup, type cast, timestamp parse, union) · Silver→Gold = all enrichment and scoring (aggregations, LLM outputs, normalized scores) · no business logic in Silver
- **Rationale**: Silver models containing scoring logic become hard to reuse and test independently; the separation makes each layer's responsibility unambiguous
- **Date**: 2026-04-02 · **Status**: active
