# Decisions — Build

> Load when: starting a build · AI agent design · data modeling.
> NOT HERE: conventions (→ DECISIONS_CONVENTIONS.md), infra (→ DECISIONS_INFRA.md).
> Archive at 100 lines → DECISIONS_BUILD_ARCHIVE.md

---

## Format
```
## [category] Decision title
- **Decision**: what was chosen
- **Rationale**: why — include alternatives considered
- **Date**: YYYY-MM-DD
- **Status**: active | superseded by [title] | archived
```

---

## [ai-agents] Route evaluation tasks to cheap/fast models, generation to capable models
- **Decision**: use Groq `llama-3.3-70b-versatile` (or equivalent) for structured evaluation tasks (judging, scoring, classification); reserve Claude Sonnet/Opus for generation tasks requiring long context or high output quality
- **Rationale**: evaluation tasks are short, structured, run repeatedly — cost compounds; Llama 3.3 70B on Groq is fast, cheap, and reliable for JSON scoring; generation tasks need Claude's context window and reasoning quality
- **Date**: 2026-03-12
- **Status**: active

## [ai-agents] User label as inclusion rule for archiving pipelines
- **Decision**: when building an AI archiving pipeline, the human decides what's worth archiving (via a label, tag, or explicit action) — the AI only executes the filing logic, never the inclusion judgment
- **Rationale**: "what's worth keeping" is a personal, context-dependent judgment that AI gets wrong at the margins; user labeling is zero-cost (one tap), eliminates false positives entirely, and keeps the pipeline simple and reliable
- **Date**: 2026-03-10
- **Status**: active

## [ai-agents] Human approval gate for all irreversible AI actions
- **Decision**: any AI pipeline that can delete, send, or permanently modify data must have a human approval step before execution — no exceptions regardless of classifier confidence
- **Rationale**: irreversible actions have asymmetric cost — one false negative on an important document, sent message, or deleted record is worse than any inefficiency introduced by a review step; high confidence scores are not a substitute for human sign-off
- **Date**: 2026-03-13
- **Status**: active

## [ai-agents] Category-first classifier: LLM proposes categories, human assigns actions
- **Decision**: for LLM classification pipelines, have LLM output fine-grained categories only; human reviews ~30-50 categories and assigns TRASH/ARCHIVE/REVIEW in a rules file; action is deterministic from that map
- **Rationale**: LLM-assigned actions are hard to audit and override in bulk; reviewing 30-50 categories is far faster than reviewing thousands of individual items; easy to adjust rules without re-running LLM; separates the classification problem (LLM is good at this) from the action problem (human judgment)
- **Date**: 2026-03-18
- **Status**: active

## [ai-agents] External search enrichment at review time, not in automated pipeline
- **Decision**: tools like Perplexity/search APIs should be used as one-time batch enrichment at human review time, not as a step in the automated classification pipeline
- **Rationale**: ~30% of hard classification cases (the ones that matter most) return "unknown" from search anyway; adding per-item search calls to the pipeline adds cost + latency with diminishing returns; the few-shot correction loop is the correct long-term improvement mechanism
- **Date**: 2026-03-23
- **Status**: active

## [ai-agents] ML classifier as primary + LLM fallback for low-confidence / new inputs
- **Decision**: when labeled training data exists, use a local ML classifier (TF-IDF + LR or equivalent) as the primary inference layer; route only low-confidence predictions and unseen input types to an LLM fallback (Groq)
- **Rationale**: LLM inference on every item is expensive and slow when a trained classifier can handle the majority of cases at zero marginal cost; labeled data from a prior LLM pass is a ready-made training set — no new labeling effort required; ML model is personalized to the domain; Groq fallback ensures no edge case is silently dropped; high confidence threshold keeps auto-action conservative
- **Date**: 2026-03-26
- **Status**: active

## [data] ISIN as universal pivot key for French financial data pipelines
- **Decision**: use ISIN as the central join key across all French market data sources (AMF, yfinance, scraping) — build a master referential that maps ISIN → all other identifiers (ticker_bourso, nom, ticker_yahoo)
- **Rationale**: ISIN is the only identifier natively present in AMF and accepted directly by `yf.Ticker(isin)`. Boursorama tickers are internal and non-standard. RSS feeds have no identifier at all — fuzzy match on company name is the only option, with ISIN resolved via the master referential.
- **Date**: 2026-03-30
- **Status**: active

## [ai-agents] Strip markdown fences in code when Claude must return raw JSON
- **Decision**: when a template instructs Claude to output raw JSON, always strip ` ```json ``` ` fences in code before saving or parsing — in addition to tightening the prompt
- **Rationale**: Claude adds fences even when explicitly told not to, especially when the content looks like code; `json.loads()` fails on fence-wrapped output; prompt-only enforcement is unreliable; stripping in code is a zero-cost safety net that makes downstream consumers robust
- **How**: `if s.startswith("```"): s = s.split("\n",1)[1].rsplit("```",1)[0].strip()`
- **Date**: 2026-03-31
- **Status**: active

## [data] Semantic layer YAML written for LLMs, not humans
- **Decision**: in any project combining dbt + NL interface, treat schema.yml column descriptions as AI documentation — precise, unambiguous, one definition per concept; enforced via a central `definitions.md` glossary; 100% column coverage required before connecting NL layer
- **Rationale**: NL interfaces consume the semantic layer at query time — vague descriptions cause the LLM to misinterpret queries silently; one concept = one name = one definition eliminates this
- **Date**: 2026-03-17
- **Status**: active

## [data-pipeline] Extract shared matching/scoring logic into a single module when multiple sources use the same pattern
- **Decision**: when ≥2 pipeline sources share the same matching or scoring logic, extract it into a dedicated module (e.g. `fuzzy_match.py`) rather than duplicating per-source; each source imports and calls the shared function
- **Rationale**: logic diverges silently across sources when duplicated — one source gets a guard fix, others don't; tests need to be written once not per-source; new sources just import the module
- **Date**: 2026-04-01
- **Status**: active

## [data-pipeline] Three-guard pattern for fuzzy matching on free-text titles
- **Decision**: when fuzzy-matching entity names against free-text, apply three guards in sequence: (1) `clean_title()` — strip source attribution suffix (`- source.tld`), (2) blocklist — skip generic names that are common words, (3) `valid_match()` — post-match word-boundary regex validation
- **Rationale**: fuzzy scoring alone allows three distinct false positive patterns — substring in longer word, generic name coincidence, URL domain suffix. Each guard targets one pattern. Validated: 0 false positives on 20 live Google News entries.
- **Date**: 2026-04-01
- **Status**: active

## [data-pipeline] dbt orchestration — CLI + Prefect, no dbt Cloud for team projects
- **Decision**: open-source dbt CLI for local dev · Prefect triggers `dbt run` in prod after upstream flows succeed · no dbt Cloud
- **Rationale**: dbt Cloud free tier = 1 seat, incompatible with team use. Prefect already live; conditioning Silver on Bronze success (not a blind cron) is only possible via Prefect. Dev local = SQL runs in BQ directly from laptop, no server needed.
- **Date**: 2026-04-02
- **Status**: active

## [data-pipeline] dbt Silver/Gold layer separation — clean vs enrich
- **Decision**: Bronze→Silver = cleaning only (dedup, type cast, timestamp parse, union) · Silver→Gold = all enrichment and scoring (aggregations, LLM outputs, normalized scores) · no business logic in Silver
- **Rationale**: Silver models that contain scoring logic become hard to reuse and test independently; the separation makes each layer's responsibility unambiguous for team members building their own models.
- **Date**: 2026-04-02
- **Status**: active
