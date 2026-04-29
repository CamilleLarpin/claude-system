# Decisions — Build: AI Agents

> Load when: designing an AI agent · LLM pipeline · classification system · model selection.
> NOT HERE: data pipelines (→ DECISIONS_BUILD_DATA.md), infra (→ DECISIONS_INFRA.md).
> Archive at 100 lines → DECISIONS_BUILD_AGENTS_ARCHIVE.md

---

## [ai-agents] Route evaluation tasks to cheap/fast models, generation to capable models
- **Decision**: use Groq `llama-3.3-70b-versatile` (or equivalent) for structured evaluation tasks (judging, scoring, classification); reserve Claude Sonnet/Opus for generation tasks requiring long context or high output quality
- **Rationale**: evaluation tasks are short, structured, run repeatedly — cost compounds; Llama 3.3 70B on Groq is fast, cheap, and reliable for JSON scoring; generation tasks need Claude's context window and reasoning quality
- **Date**: 2026-03-12 · **Status**: active

## [ai-agents] User label as inclusion rule for archiving pipelines
- **Decision**: when building an AI archiving pipeline, the human decides what's worth archiving (via a label, tag, or explicit action) — the AI only executes the filing logic, never the inclusion judgment
- **Rationale**: "what's worth keeping" is a personal, context-dependent judgment that AI gets wrong at the margins; user labeling is zero-cost (one tap), eliminates false positives entirely, and keeps the pipeline simple and reliable
- **Date**: 2026-03-10 · **Status**: active

## [ai-agents] Human approval gate for all irreversible AI actions
- **Decision**: any AI pipeline that can delete, send, or permanently modify data must have a human approval step before execution — no exceptions regardless of classifier confidence
- **Rationale**: irreversible actions have asymmetric cost — one false negative on an important document, sent message, or deleted record is worse than any inefficiency introduced by a review step; high confidence scores are not a substitute for human sign-off
- **Date**: 2026-03-13 · **Status**: active

## [ai-agents] Category-first classifier: LLM proposes categories, human assigns actions
- **Decision**: for LLM classification pipelines, have LLM output fine-grained categories only; human reviews ~30-50 categories and assigns TRASH/ARCHIVE/REVIEW in a rules file; action is deterministic from that map
- **Rationale**: LLM-assigned actions are hard to audit and override in bulk; reviewing 30-50 categories is far faster than reviewing thousands of individual items; easy to adjust rules without re-running LLM; separates the classification problem (LLM is good at this) from the action problem (human judgment)
- **Date**: 2026-03-18 · **Status**: active

## [ai-agents] External search enrichment at review time, not in automated pipeline
- **Decision**: tools like Perplexity/search APIs should be used as one-time batch enrichment at human review time, not as a step in the automated classification pipeline
- **Rationale**: ~30% of hard classification cases return "unknown" from search anyway; per-item search calls add cost + latency with diminishing returns; the few-shot correction loop is the correct long-term improvement mechanism
- **Date**: 2026-03-23 · **Status**: active

## [ai-agents] ML classifier as primary + LLM fallback for low-confidence / new inputs
- **Decision**: when labeled training data exists, use a local ML classifier (TF-IDF + LR or equivalent) as the primary inference layer; route only low-confidence predictions and unseen input types to an LLM fallback (Groq)
- **Rationale**: LLM inference on every item is expensive when a trained classifier handles the majority at zero marginal cost; labeled data from a prior LLM pass is a ready-made training set; Groq fallback ensures no edge case is silently dropped
- **Date**: 2026-03-26 · **Status**: active

## [ai-agents] Strip markdown fences in code when Claude must return raw JSON
- **Decision**: when a template instructs Claude to output raw JSON, always strip ` ```json ``` ` fences in code before saving or parsing — in addition to tightening the prompt
- **Rationale**: Claude adds fences even when explicitly told not to; `json.loads()` fails on fence-wrapped output; prompt-only enforcement is unreliable; stripping in code is a zero-cost safety net
- **How**: `if s.startswith("```"): s = s.split("\n",1)[1].rsplit("```",1)[0].strip()`
- **Date**: 2026-03-31 · **Status**: active

## [ai-agents] Provider-agnostic architecture — LiteLLM abstraction over framework lock-in
- **Decision**: build AI agent systems with a model abstraction layer (LiteLLM or equivalent); never use the orchestration framework's native model client directly; provider swap must require no code change
- **Rationale**: AI provider pricing changes frequently; frameworks that hardwire model clients create rebuild risk; abstraction decouples orchestration from model; local models (Ollama) available as zero-cost fallback
- **How to apply**: verify the framework supports provider abstraction before building skills; if not, add an abstraction layer first
- **Date**: 2026-04-23 · **Status**: active — first applied in chief-of-staff-ia (D1)

## [ai-agents] No MCP for scheduled / non-interactive sessions
- **Decision**: never use MCPs (Gmail MCP, Calendar MCP, etc.) for tasks that run in cron or non-interactive sessions; use native connectors, purpose-built CLIs, or direct API calls instead
- **Rationale**: MCPs require an interactive Claude Code session — they break silently in cron/daemon contexts; purpose-built CLIs are lightweight, testable, and reliable in any execution context
- **How to apply**: if a scheduled job needs to call an external service, always use the service's API or a native connector — MCPs are UI-layer tools, not automation tools
- **Date**: 2026-04-23 · **Status**: active — first applied in chief-of-staff-ia (D4)

## [privacy] Local LLM (Ollama) evaluation before committing to external API for sensitive data
- **Decision**: before finalising an external LLM API for any pipeline processing sensitive data (financial, medical, personal), run a local model evaluation first (Ollama on Hetzner — Llama 3.1 8B or Qwen 2.5 7B). Use external API only if local quality < 85% accuracy threshold.
- **Rationale**: Anthropic API does not train on API inputs (contractual), but data transits their servers — a trust dependency; local LLM removes that dependency at zero marginal cost; modern 8B models match Haiku quality on classification tasks
- **How to apply**: default to local eval first on sensitive data; document the accuracy comparison before deciding
- **Date**: 2026-04-23 · **Status**: active — first applied in finances-ezerpin (D33)
