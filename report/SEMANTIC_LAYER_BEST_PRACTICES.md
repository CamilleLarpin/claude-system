# Semantic Layer & Documentation Best Practices
> Source: "How AI is changing the standard for BI" — Juliette Duizabo, Head of Data @ Photoroom
> Extracted: 2026-03-17

---

## Context
3-person data team, 100+ employees. Stack: Airbyte → Snowflake → dbt → Omni (BI + NL assistant).
Goal: every employee gets an answer to any data question in under 1 minute, from anywhere.

---

## Principles

### 1. Semantic layer = single source of truth
Split across two layers:
- **dbt**: data transformation + column definitions (dimensions)
- **BI/NL tool**: topics (query routing), views (dimensions + measures), calculated metrics
Both must be consistent — dbt definitions flow into the BI tool automatically.

### 2. YAML files are AI documentation — write for LLMs, not humans
The semantic layer is consumed by LLMs to answer NL queries. This means:
- Descriptions must be **unambiguous** — an LLM cannot ask for clarification
- No synonyms for the same concept — pick one word and use it everywhere
- No vague descriptions like "transaction amount" — say "transaction amount in euros, negative = debit, positive = credit"
- Treat every column description as a contract, not a comment

### 3. 100% documentation coverage — enforced, not aspirational
- Cannot merge a PR without documentation on every column
- Non-negotiable: undocumented columns = LLM guesses = wrong answers

### 4. Single definition principle — one concept, one definition
- Central `definitions.md` (or equivalent) lists every business concept with one canonical definition
- Tool: `dbt-datadict` package — raises an error if the same column name has two different descriptions across models
- If you need a second meaning for a concept, use a **different name** — not a second definition of the same name

### 5. Topics = AI query routing context
A "topic" is a short text file that tells the LLM:
- Which table/view to use
- When to use it (keywords, question types)
- What it contains
Without this routing context, the LLM picks the wrong table. In dbt terms: the model `description` field + a dedicated context block serve the same role.

### 6. 1 dbt model = 1 semantic view = 1 topic (start simple)
Photoroom's rule: simplistic 1:1 mapping to ship fast.
Do not design complex many-to-many semantic structures before you understand usage patterns.
Start small (7 dashboards/topics), add as users ask.

### 7. Measures defined centrally, not per chart
Calculated metrics (e.g. "monthly spend", "couple balance") belong in the semantic layer — not in ad-hoc queries.
Without this: two people calculate the same metric differently → discrepancies → loss of trust.

### 8. Visual consistency = semantic alignment
Color coding in reports is part of the semantic layer — same color always means the same dimension.
Applied: consistent naming and formatting conventions carry the same weight as code conventions.

---

## Applied to dbt + nao projects
- `schema.yml` column descriptions = the semantic layer nao reads
- `dbt/definitions.md` = central glossary for all business terms
- Model `description` fields should include: what the table is, when to use it, what it does NOT contain
- Every mart model should have a topic-style context block in its description
- `dbt-datadict` or equivalent to enforce single-definition rule
