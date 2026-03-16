# Bootcamp Data Engineering — Project Evaluation
> Artefact Bootcamp · Feb 23 – Mar 27, 2026
> Last updated: 2026-03-16

---

## Certification Criteria

| Code | Requirement | Key deliverables |
|------|------------|-----------------|
| C1 | Automated data collection | Extraction script, multi-source logic, error handling |
| C2 | Data preparation | Cleaning functions (nulls, formats), transformation logic |
| C3 | Aggregation rules | Rules combining/aggregating sources into metrics |
| C4 | Create a database | Schema (MCD/MLD), table creation script, SQL vs NoSQL justification |
| C5 | Expose data via API | Secured endpoints (API key), Swagger/OpenAPI docs, live data proof |

**Deliverables:** Professional written report + Git repo (all code + config) + 10-15 slide presentation (oral)

---

## Scoring Rubric

| Score | Meaning |
|-------|---------|
| ✅ 3 | Fully covered — production-ready or trivial to add |
| 🟡 2 | Partially present — minor work or polish needed |
| 🔶 1 | Concept applies — significant work needed |
| ❌ 0 | Missing entirely — needs to be built |

---

## Active Projects — Evaluation

| Project | C1 | C2 | C3 | C4 | C5 | Total | Verdict |
|---------|----|----|----|----|-----|-------|---------|
| Finances Ezerpin | ✅ 3 | ✅ 3 | ✅ 3 | ✅ 3 | ❌ 0 | **12/15** | Strong — just needs FastAPI |
| Audio Intelligence Pipeline | ✅ 3 | 🟡 2 | 🔶 1 | 🔶 1 | 🔶 1 | **8/15** | Needs DB + aggregation layer |
| Gmail Inbox Cleanup | 🟡 2 | 🟡 2 | 🟡 2 | ❌ 0 | ❌ 0 | **6/15** | C4/C5 missing, weak C1 story |
| claude-one-digest | 🔶 1 | 🟡 2 | 🟡 2 | ❌ 0 | ❌ 0 | **5/15** | Too small/niche for jury |
| Data Engineering Notes | 🔶 1 | 🔶 1 | 🔶 1 | ❌ 0 | ❌ 0 | **3/15** | Not suitable |
| Ghost / Biography / Family CM / AI Networking | — | — | — | — | — | **N/A** | n8n-only, no data engineering foundation |

### Creative fixes for top active project

**Finances Ezerpin (12/15):** Add FastAPI in ~1 day — `GET /expenses`, `GET /summary/monthly`, `GET /categories/breakdown` — API key header auth + auto-generated Swagger at `/docs`. DuckDB is directly queryable from Python.

---

## Backlog Projects — Evaluation

| Project | C1 | C2 | C3 | C4 | C5 | Total | Notes |
|---------|----|----|----|----|-----|-------|-------|
| **Agent Politique** | ✅ 3 | ✅ 3 | ✅ 3 | ✅ 3 | ✅ 3 | **15/15** ⭐ | Official AN API, no scraping risk |
| **Teal (Real Estate)** | ✅ 3 | ✅ 3 | ✅ 3 | ✅ 3 | ✅ 3 | **15/15** ⭐ | Public tool, personal use ~10 months out; DVF dataset, mainly new territory |
| Meeting Note Taker | ✅ 3 | ✅ 3 | ✅ 3 | 🟡 2 | 🟡 2 | **13/15** | Mac hardware recording confirmed; C4 needs DB definition (transcripts + contact metadata); linked to AI Networking System |
| Media Content Manager | ✅ 3 | 🟡 2 | 🟡 2 | 🟡 2 | 🟡 2 | **12/15** | Sources: YouTube/podcasts (Whisper) + Reddit/LinkedIn (text — separate pipeline); C4 gap: needs DB for knowledge base (transcripts, summaries, tags, source URL, date) |
| ~~Automate Finance Investments~~ | ❌ 0 | ✅ 3 | ✅ 3 | ✅ 3 | 🟡 2 | **~~11/15~~** | ❌ **Not suitable** — no bank/broker API; C1 = manual CSV export; fails automated collection criterion; build as personal tool post-bootcamp |
| Observability Layer | ❓ | 🟡 2 | ✅ 3 | 🟡 2 | 🟡 2 | **?** | C1 depends on data source (see open questions) |
| Build Process to Follow News | ✅ 3 | 🟡 2 | ✅ 3 | ❌ 0 | ❌ 0 | **8/15** | C4/C5 missing |
| Context tools (x3) | 🟡 2 | 🟡 2 | 🟡 2 | 🟡 2 | 🔶 1 | **9/15** | Too niche for jury |
| LLM Lessons Repo | 🔶 1 | 🟡 2 | 🟡 2 | 🟡 2 | 🟡 2 | **9/15** | C1 weak without external sources |
| Meal Prep | ❓ | ❓ | ❓ | ❓ | ❓ | **?** | Scope unclear |
| Closet Review | 🔶 1 | 🔶 1 | 🔶 1 | 🔶 1 | 🔶 1 | **5/15** | UX app, not data engineering |

---

## Open Questions (pending clarification)

| Project | Question | Impact |
|---------|----------|--------|
| Observability Layer | Raw data source: instrumented code logs vs Anthropic billing export vs both? | Determines C1 score |
| ~~Finance Investments~~ | ~~Personal portfolio or general tool? Broker with API?~~ | ✅ Answered: personal tool, no API → **not suitable for bootcamp** |
| Meal Prep | Meal planning tool or course creation tool? | Determines if viable |
| ~~Meeting Note Taker~~ | ~~Local audio files or Zoom/Google Meet API pull?~~ | ✅ Answered: Mac hardware recording + vocal notes post-meeting → C1 = ✅ |
| LLM Lessons Repo | User submissions only or pull from GitHub/HN/SO? | C1 score |
| Agent Politique | Vote theme classification: keyword rules vs Claude API? | C2 complexity |
| Agent Politique | Teacher validation of v1 scope (votes + KPIs only, no manifesto comparison)? | Go/no-go on bootcamp target |

---

## Recommendation: Agent Politique ⭐

### Why over Teal

| Factor | Agent Politique | Teal (DVF) |
|--------|----------------|-----------|
| Jury narrative | Civic data + elections timing — memorable | Good but more common |
| Public sharing | ✅ Publishable — portfolio asset | ❌ Personal tool |
| Personal utility | ✅ Municipales in 1 month, présidentielles in 1 year | ✅ But 6-12 months out |
| Build risk | Low — official AN API, stable | Low with DVF, more setup |
| Originality | Very high | Moderate |

**Teal is not lost** — build it as a personal tool when property search starts (6-12 months). DVF + a lightweight scraper layer is a 2-week project.

### Data flow overview

```
Data In
  ├── Deputies profiles     → assemblee-nationale.fr API (JSON)
  ├── Vote records          → assemblee-nationale.fr API (XML scrutins)
  └── Scheduled refresh     → cron (daily or weekly)

C2 — Prepare
  ├── Parse XML vote records
  ├── Normalize deputy IDs/names
  ├── Handle vote types (pour / contre / abstention / absent / proxy)
  └── Classify vote theme → keyword rules (v1) or Claude API (v2)

C3 — Aggregate
  ├── Loyalty score per deputy (% aligned with party group vote)
  ├── Participation rate per deputy
  ├── Vote breakdown by theme (economy / social / environment / justice)
  └── Trend over time (per month of legislature)

C4 — PostgreSQL
  Tables: deputies, parties, scrutins, votes, themes, scores

C5 — FastAPI
  GET /deputies                    → list with KPI scores
  GET /deputies/{id}               → full vote record + aggregated KPIs
  GET /parties/{id}/comparison     → loyalty + thematic breakdown
  GET /votes/by-theme              → cross-party breakdown by topic
  Auth: API key header
  Docs: Swagger at /docs
```

### v1 scope (bootcamp delivery)

In scope:
- Deputies + votes for current legislature (17th, 2022–present)
- Keyword-based theme classification
- Loyalty score + participation rate per deputy
- PostgreSQL + FastAPI + Swagger

Out of scope (v2, post-bootcamp):
- Promise vs vote comparison (requires manifesto PDF parsing — separate project)
- Historical legislature comparison
- Claude-based theme classification
- Public-facing UI

### Data quality assessment

| Concern | Reality |
|---------|---------|
| data.gouv.fr quality is poor | True for aggregated/municipal datasets — NOT for AN data |
| AN vote data specifically | High quality — primary source, official legal record, structured XML |
| Main challenge | Theme classification — votes have titles but no predefined taxonomy |
| Mitigation | Build a taxonomy (10-15 themes) and classify by keyword first; upgrade to Claude API in v2 |

---

## Current Top 5 Ranking (updated 2026-03-16)

| Rank | Project | Score | Key risk |
|---|---|---|---|
| 1 | **Agent Politique** | 15/15 ⭐ | Domain ramp-up + teacher validation pending |
| 2 | **Teal** | 15/15 ⭐ | New territory (DVF), time |
| 3 | **Meeting Note Taker** | ~13/15 | C4 DB definition needed |
| 4 | **Finances Ezerpin** | 12/15 | FastAPI only remaining — lowest risk |
| 5 | **Media Content Manager** | ~12/15 | C4 DB gap + Reddit/LinkedIn scope adds complexity |

**Dropped:** Automate Finance Investments — no bank/broker API, C1 fails certification criterion.
**Time available:** 2+ weeks as of 2026-03-16.

---

## Next Steps

1. Confirm scope with teacher — validate that v1 (no manifesto comparison) meets C1-C5
2. Decide theme classification approach: keyword rules vs Claude API
3. Explore data.assemblee-nationale.fr API — check rate limits, data format, current legislature availability
4. Initialize project repo and `.claude/` structure
5. Build C1 first — get deputies + votes flowing into PostgreSQL before anything else
