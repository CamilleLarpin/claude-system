# Lessons — LLM APIs, prompting & evaluation

> Load when: writing prompts, integrating LLM APIs, evaluating models, debugging LLM output quality.

---

## [llm] · Rule · Groq free tier limits are per-model and separate — 70b exhausts fast
> 2026-03-12 · source: claude-one-digest
- `llama-3.3-70b-versatile`: 6000 TPM + 100k TPD — exhausted in one heavy dev session
- `llama-3.1-8b-instant`: 6000 TPM + separate (larger) daily quota
- Use 8b-instant as daily driver for any repeated task; reserve 70b for occasional spot-checks only

## [llm] · Guideline · Chunk by character count, not word count, when targeting token limits
> 2026-03-12 · source: claude-one-digest
- Word count underestimates tokens by 1.3–1.5x; a 6000-word chunk easily exceeds a 6000-token limit
- Prompt template overhead (~300 tokens) must also be budgeted
- Use char-based chunking: `CHUNK_CHAR_LIMIT = 10_000` chars ≈ 2500 tokens — leaves headroom for prompt

## [llm] · Rule · Small models need `max_tokens` cap to prevent hallucination loops on list generation
> 2026-03-13 · source: claude-one-digest
- `llama-3.1-8b-instant` generating a flat concept list entered a repetition loop with no token cap — produces garbage output and can exhaust rate limits
- Open-ended list tasks have no natural stopping signal for small models
- Always set `max_tokens` on API calls for list generation tasks; 400 is sufficient for short concept extraction

## [llm] · Guideline · LLM DROP/exclusion rules unreliable for small models — use Python post-filter
> 2026-03-13 · source: claude-one-digest
- `llama-3.1-8b-instant` ignored DROP rules in prompt instructions — single-word tokens, path strings, and questions survived after deduplication
- Small models follow inclusion rules better than exclusion rules; negative filtering logic in prompts adds complexity they can't reliably execute
- Move deterministic filtering to code (short entries, known noisy tokens, pattern matches); keep LLM prompt focused on the positive task

## [prompt] · Rule · Missing `{content}` placeholder in prompt template causes silent empty-context failure
> 2026-03-13 · source: claude-one-digest
- Both EXTRACT_PROMPT and MERGE_PROMPT lost `{content}` after a manual edit — the LLM received no session data and responded as if nothing was provided; no error was raised
- The pipeline runs successfully and produces output; the failure is invisible without reading the LLM response critically
- Always verify `{content}` (or equivalent) is present in the template body AND in the `.format()` call; add an assertion if the prompt is edited often

## [prompt] · Rule · Format examples with placeholder names cause the model to output them literally
> 2026-03-13 · source: claude-one-digest
- `Format:\n- ConceptName` caused the model to output `- ConceptName` as the first line of its response — it treats example text as a template to follow verbatim
- Use real-looking example values in format instructions (e.g. `- Docker layer caching`), never abstract placeholder labels

## [llm-pipeline] · Rule · Insert few-shot corrections before the full classification run, not after
> 2026-03-19 · source: finances-ezerpin
- `labeled_corrections` is injected into every prompt at run time — waiting until after the full run means the run itself misses the signal
- Safe corrections (specific label, unambiguous merchant) should go in as soon as they're identified during sample review
- Unsafe: multi-purpose platform examples (e.g. Yoojo used for both childcare and home services) — adding one service type as an example biases ALL future transactions from that platform

## [llm-pipeline] · Rule · DELETE + re-run pattern: never re-classify already-correct predictions
> 2026-03-19 · source: finances-ezerpin
- `load_unclassified()` should LEFT JOIN on the predictions table and skip rows already classified — only deleted rows get re-processed
- Corrections = DELETE wrong predictions + re-run; pay only for the corrections, not the full dataset
- Running a large --sample before the full run means paying twice (sample calls + full run calls) — skip to full run once the prompt is stable

## [llm-pipeline] · Pattern · Use external enrichment (Perplexity/search) at review time, not in automated pipeline
> 2026-03-23 · source: finances-ezerpin
- Perplexity descriptions helped identify unknown merchants during a human review batch (~70% useful, ~30% "je ne sais pas")
- Adding a search call per transaction to the automated pipeline adds cost + latency with diminishing returns — the hard cases are precisely the ones search can't resolve
- Correct flow: one-time batch enrichment at review time → human decisions → corrections → few-shot examples → improved future runs
- The few-shot correction loop is the right long-term mechanism; search is a bootstrap aid

## [llm-pipeline] · Pattern · Pre-fill corrections in review files — human validates, doesn't create from scratch
> 2026-03-23 · source: finances-ezerpin
- Exporting a review CSV with `corrected_category` + `corrected_sub_category` pre-filled (AI best guess) + free-text comment column is significantly faster than a blank review file
- Human reviews agreement/disagreement rather than producing corrections from zero — much faster for 1000+ row batches
- A reconciliation script reads comments and updated columns → generates final corrections file
- Include any enrichment (Perplexity descriptions, confidence scores) in the review file to reduce decision time on unknown items

## [mlflow] · Rule · mlflow.evaluate() + make_metric is the old ML API — use mlflow.genai for LLM evaluation
> 2026-03-13 · source: audio-intelligence-pipeline
- `mlflow.evaluate()` + `make_metric` logs scores as flat metrics in regular runs — they do NOT appear in the GenAI Evaluation view, Judges tab, or linked to datasets
- `@mlflow.genai.scorer` + `mlflow.genai.evaluate()` is the correct GenAI-native API in MLflow 3.x — scores appear in Evaluation runs, linked to datasets and prompt versions
- The two APIs look similar but produce fundamentally different UI; using the wrong one means building the right logic in the wrong place
