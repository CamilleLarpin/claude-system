# Decisions — Build

> Load when: starting a build, AI agent design, data modeling.
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

## [data] Semantic layer YAML written for LLMs, not humans
- **Decision**: in any project combining dbt + NL interface, treat schema.yml column descriptions as AI documentation — precise, unambiguous, one definition per concept; enforced via a central `definitions.md` glossary; 100% column coverage required before connecting NL layer
- **Rationale**: NL interfaces consume the semantic layer at query time — vague descriptions cause the LLM to misinterpret queries silently; one concept = one name = one definition eliminates this
- **Date**: 2026-03-17
- **Status**: active
