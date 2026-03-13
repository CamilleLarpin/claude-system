# Lessons — architecture & integrations

> Scope: git, ai-agents, system architecture, third-party integrations.
> Split into sub-files at 150 lines.

---

## [git] · Guideline · Rebase before push
> unknown · source: unknown
- Merging without rebase creates noise merge commits when working across machines
- `git pull --rebase` replays your commits on top of remote, keeps history linear
- Set as default: `git config pull.rebase true`

## [ai-agents] · Rule · Conversation memory corruption from empty messages
> unknown · source: ghost
- Empty messages corrupt entire conversation history in agent memory
- Corrupted history produces unpredictable agent behavior with no clear error signal
- Validate non-empty BEFORE saving to Conversation Memory; recovery: change session key (e.g. append `_v2`) to start fresh

## [ai-agents] · Note · Loop-back for chicken-and-egg context problems
> unknown · source: ghost
- Need data before agent runs, but only know which data is needed after agent responds
- Solution: run agent → detect context change → load data → run second agent → discard first output
- Use a different session key for the second agent to avoid memory contamination

## [integrations] · Rule · Google Docs auth on self-hosted n8n
> unknown · source: biography
- OAuth2 requires a verified redirect URI — unavailable on self-hosted n8n instances
- Service Account bypasses this constraint entirely
- Use `googleApi` (Service Account) credential; grant the service account email Editor permission on the target Doc

## [architecture] · Guideline · Batch vs immediate write
> unknown · source: unknown
- Choosing write strategy ad-hoc leads to inconsistent behavior across workflows
- Apply this decision tree: API charges per call? → batch. Data irreplaceable? → immediate. Latency user-facing? → batch. Rate limits tight? → batch.

## [integrations] · Rule · `load_dotenv()` does not override existing env vars — direnv takes precedence
> 2026-03-06 · source: data-engineering-notes
- If direnv is active and sets a var (e.g. `ANTHROPIC_API_KEY`) via `.envrc`, `load_dotenv()` silently skips it — shell env wins; `.env` looks correct but the wrong value is used at runtime
- To let `.env` win: use `load_dotenv(override=True)`; to debug: `echo $VAR_NAME` before running the script

## [bash] · Rule · Scripts called from Claude Code or CI must not use interactive `read` prompts
> 2026-03-11 · source: project-init-skill
- `read -p "..."` fails with exit code 1 when stdin has no TTY (Claude Code tool calls, CI pipelines, `bash script.sh` piped) — `set -e` then aborts the script silently
- Anything after the `read` never runs; failures are hard to diagnose without knowing the TTY constraint
- Accept all inputs as positional CLI arguments (`$1`, `$2`, etc.) with sensible defaults; reserve `read` for scripts explicitly documented as interactive-only

## [llm] · Rule · Groq free tier limits are per-model and separate — 70b exhausts fast
> 2026-03-12 · source: claude-one-digest
- `llama-3.3-70b-versatile`: 6000 TPM + 100k TPD — exhausted in one heavy dev session
- `llama-3.1-8b-instant`: 6000 TPM + separate (larger) daily quota
- Use 8b-instant as daily driver for any repeated task; reserve 70b for occasional spot-checks only

## [git] · Rule · git diff hunks start mid-section — section header may not appear before changed lines
> 2026-03-12 · source: claude-one-digest
- `git diff` hunks start at the nearest context line before the change, not at the section header — if `### Project` is >3 lines above the change, it's outside the hunk and never seen by a line-by-line parser
- Parsing changed lines by scanning for a preceding section header in the diff body silently produces empty results
- Fix: build a line→section map from the full current file first, then use `@@` hunk offsets to resolve which section each change belongs to

## [llm] · Guideline · Chunk by character count, not word count, when targeting token limits
> 2026-03-12 · source: claude-one-digest
- Word count underestimates tokens by 1.3–1.5x; a 6000-word chunk easily exceeds a 6000-token limit
- Prompt template overhead (~300 tokens) must also be budgeted
- Use char-based chunking: `CHUNK_CHAR_LIMIT = 10_000` chars ≈ 2500 tokens — leaves headroom for prompt

## [github] · Rule · Fine-grained PATs require explicit repository + Contents permission
> 2026-03-12 · source: audio-intelligence-pipeline
- `github_pat_` tokens return 403 on `git clone` unless the token explicitly grants access to that specific repo with Contents: Read-only
- Classic `ghp_` tokens with `repo` scope work without per-repo config
- After creating a fine-grained PAT: Settings → token → Edit → Repository access → select repo → Permissions → Contents: Read-only

## [docker] · Rule · Use `--host 0.0.0.0` when running Uvicorn inside Docker
> 2026-03-12 · source: audio-intelligence-pipeline
- Default `--host 127.0.0.1` binds only inside the container — port mapping (`-p 8000:8000`) has no effect
- Always set `--host 0.0.0.0` in the Dockerfile CMD for any containerised FastAPI/Uvicorn app

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

## [hetzner] · Rule · Hetzner Firewall must include ports 80 and 443 when nginx is present
> 2026-03-13 · source: server-setup session
- Opening only app ports (5678, 8080, 8000) blocks all domain-based access when nginx sits in front as a reverse proxy — nginx listens on 80/443, not the app ports
- All domain traffic (n8n.helmcome.com, cloud.helmcome.com) timed out immediately after firewall creation; services were running fine but unreachable
- Always include TCP 80 and TCP 443 in any Hetzner Firewall rule set when the server runs a reverse proxy; direct port rules are for fallback/debug only

## [integrations] · Rule · Telegram delivers the same webhook update multiple times simultaneously
> 2026-03-03 · source: family-content-manager
- Telegram sometimes sends the same update 2-3× within milliseconds → multiple simultaneous n8n executions triggered by one user action
- Sequential duplicate protection (checking if a file was already moved) doesn't help — all instances start before any finishes; causes MOVE race conditions and 423 Locked on concurrent file writes
- True fix: deduplicate at the trigger level — store processed `message_id` values (e.g. in workflow static data) and skip execution if already seen; or make all operations fully idempotent
