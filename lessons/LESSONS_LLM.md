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

## [llm-pipeline] · Rule · Confidence gate downgrade must go to REVIEW queue, not KEEP
> 2026-03-25 · source: gmail-inbox-cleanup
- Initial confidence gate downgraded low-confidence TRASH → KEEP; this silently buried borderline trash in the inbox with no recovery path
- KEEP means "I want this" — it must never be used as a fallback for uncertain destructive actions; that defeats the purpose of having a review queue
- Correct pattern: low-confidence TRASH → TRASH_REVIEW (or equivalent review bucket); KEEP is only assigned when the category action is genuinely KEEP

## [llm-pipeline] · Rule · Protect self-sent / system emails via hard rule before LLM sees them
> 2026-03-25 · source: gmail-inbox-cleanup
- Self-sent emails (voice memos, self-notes, forwarded docs) have no consistent signal — the LLM classifies them based on subject/snippet and routinely misassigns them to wrong categories (e.g. "Real Estate - Alerts") → marked TRASH
- Hard rule pre-classification (exact sender match before LLM) is the only reliable protection; LLM context cannot be trusted for this
- Always add the user's own address(es) and known system senders to a hard-rule allowlist that runs before LLM classification

## [llm-pipeline] · Rule · Never add senders to always_trash from a sample — inspect full metadata first
> 2026-03-23 · source: gmail-inbox-cleanup
- A 1000-email sample is unrepresentative: personal contacts, financial senders (Boursorama, Revolut), and health senders appeared in a "Subscriptions" category due to misclassification — adding them to always_trash would have permanently deleted critical emails
- always_trash is a hard override that bypasses all LLM classification — wrong entries cause irreversible data loss
- Before adding any sender to always_trash: search the full metadata (not just the sample) for that sender's subjects; when in doubt, leave unset and let category logic decide

## [llm-pipeline] · Rule · Multi-address senders need per-address review before trashing
> 2026-03-23 · source: gmail-inbox-cleanup
- MiiMOSA (crowdfunding/investment platform) uses investisseurs@ and noreply@ for financial statements and reimbursements, and communication@ / bonjour@ for newsletters — blanket-trashing all MiiMOSA would have deleted tax documents and monthly reimbursement records
- Platforms mixing transactional and promotional mail use separate sender addresses — always check all sub-addresses before adding any to a trash list
- Pattern: search full metadata by domain first; only add specific addresses confirmed to be purely promotional

## [llm-pipeline] · Guideline · Domain-only filters too blunt for mixed senders — use content classification
> 2026-03-26 · source: gmail-inbox-cleanup
- First instinct for email filtering: extract trash sender domains → apply domain-level rules; fails because the same domain sends both TRASH (marketing) and KEEP (booking confirmation) e.g. Ryanair, Amazon, any bank
- Domain-only rules are safe only for senders where 100% of historical emails are trash (pure-trash domains); for anything mixed, subject+snippet classification is required
- Architecture: ML classifier (subject+snippet → category) as primary; LLM fallback for low confidence / new senders; domain rules alone are insufficient for real-world filtering

## [llm-pipeline] · Guideline · Bottom-up taxonomy outperforms hardcoded taxonomy for action-homogeneity
> 2026-03-23 · source: gmail-inbox-cleanup
- Hardcoded 43-category taxonomy (Claude-designed without seeing the data) produced categories mixing emails with different ideal actions — action assignment was hard and produced ambiguous categories
- Bottom-up (LLM proposes from actual sample, max count constraint, action-homogeneity requirement in prompt) produced 29 categories mapping cleanly to TRASH/KEEP/REVIEW
- For any inbox/triage classification pipeline: sample → LLM proposes taxonomy (max 20-30, action-homogeneous) → human assigns actions → LLM classifies full corpus

## [llm-pipeline] · Pattern · 2-round agent for credit/debit matching — identify credits first, find debits second
> 2026-03-24 · source: finances-ezerpin
- When matching paired transactions (credit + debit), expose only the credit leg to the LLM in Round 1 — isolating the signal prevents confusion with unrelated debits
- Round 2 takes the confirmed credits and searches for matching debits (same amount, ±N days) — deterministic, no LLM needed
- Applies to: reimbursement detection, inter-account transfer matching, refund pairing
- Anti-pattern: asking the LLM to identify both legs simultaneously — it will apply the category to unrelated transactions that happen to look similar

## [prompt] · Rule · LLM returns full "Parent > Sub" path in structured output when taxonomy uses that format
> 2026-03-24 · source: finances-ezerpin
- When the taxonomy is displayed as `"Kids > Gardes"` and the expected JSON has `{"category": "...", "sub_category": "..."}`, the LLM may return the full path in `category` (e.g. `"Kids > Gardes"`) instead of just the parent (`"Kids"`)
- Two fixes required: (1) explicit prompt instruction: `"category" must be the parent name only (e.g. "Kids"), never the full path`; (2) defensive post-processing: if `" > "` in `pred["category"]`, split and keep first part
- DB fix for already-stored dirty rows: `UPDATE table SET category = string_split(category, ' > ')[1] WHERE category LIKE '% > %'`

## [classification] · Rule · For systematic category renames, change the taxonomy — don't rely on few-shot examples
> 2026-03-23 · source: finances-ezerpin
- With N corrections in `labeled_corrections` and only 10 few-shot examples injected per prompt, the probability of hitting the right example for a given batch is low
- Systematic patterns (mass rename of a sub-category) do not propagate reliably via few-shot; LLM reverts to its trained priors
- For systematic renames: remove the old sub-category from the taxonomy entirely — the LLM cannot predict a category that isn't an option
- Few-shot examples are effective for isolated merchant-specific corrections, not mass category migrations
- Even for merchant-specific corrections, few-shot fails if: (1) selection window doesn't include that example (10 from 170 batch = arbitrary), AND (2) the model has a strong prior (e.g. "Lovys" → Kids, "AREA NFC" → Restaurants)
- For merchants with counter-intuitive categories, the only robust fix is an explicit merchant rule in the system prompt — few-shot cannot override a strong LLM prior reliably

---

## [mlflow] · Rule · mlflow.evaluate() + make_metric is the old ML API — use mlflow.genai for LLM evaluation
> 2026-03-13 · source: audio-intelligence-pipeline
- `mlflow.evaluate()` + `make_metric` logs scores as flat metrics in regular runs — they do NOT appear in the GenAI Evaluation view, Judges tab, or linked to datasets
- `@mlflow.genai.scorer` + `mlflow.genai.evaluate()` is the correct GenAI-native API in MLflow 3.x — scores appear in Evaluation runs, linked to datasets and prompt versions
- The two APIs look similar but produce fundamentally different UI; using the wrong one means building the right logic in the wrong place
