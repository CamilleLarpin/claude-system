# Lessons — architecture & integrations

> Scope: git, ai-agents, system architecture, third-party integrations.
> NEVER delete entries. Split into sub-files at 150 lines.

---

## [git] Rebase before push
> unknown · source: unknown
- Merging without rebase creates noise merge commits when working across machines
- `git pull --rebase` replays your commits on top of remote, keeps history linear
- Set as default: `git config pull.rebase true`

## [ai-agents] Conversation memory corruption from empty messages
> unknown · source: ghost
- Empty messages corrupt entire conversation history in agent memory
- Corrupted history produces unpredictable agent behavior with no clear error signal
- Validate non-empty BEFORE saving to Conversation Memory; recovery: change session key (e.g. append `_v2`) to start fresh

## [ai-agents] Loop-back for chicken-and-egg context problems
> unknown · source: ghost
- Need data before agent runs, but only know which data is needed after agent responds
- Solution: run agent → detect context change → load data → run second agent → discard first output
- Use a different session key for the second agent to avoid memory contamination

## [integrations] Google Docs auth on self-hosted n8n
> unknown · source: biography
- OAuth2 requires a verified redirect URI — unavailable on self-hosted n8n instances
- Service Account bypasses this constraint entirely
- Use `googleApi` (Service Account) credential; grant the service account email Editor permission on the target Doc

## [architecture] Batch vs immediate write
> unknown · source: unknown
- Choosing write strategy ad-hoc leads to inconsistent behavior across workflows
- Apply this decision tree: API charges per call? → batch. Data irreplaceable? → immediate. Latency user-facing? → batch. Rate limits tight? → batch.

## [integrations] `load_dotenv()` does not override existing env vars — direnv takes precedence
> 2026-03-06 · source: data-engineering-notes
- If direnv is active and sets a var (e.g. `ANTHROPIC_API_KEY`) via `.envrc`, `load_dotenv()` silently skips it — shell env wins; `.env` looks correct but the wrong value is used at runtime
- To let `.env` win: use `load_dotenv(override=True)`; to debug: `echo $VAR_NAME` before running the script

## [integrations] Telegram delivers the same webhook update multiple times simultaneously
> 2026-03-03 · source: family-content-manager
- Telegram sometimes sends the same update 2-3× within milliseconds → multiple simultaneous n8n executions triggered by one user action
- Sequential duplicate protection (checking if a file was already moved) doesn't help — all instances start before any finishes; causes MOVE race conditions and 423 Locked on concurrent file writes
- True fix: deduplicate at the trigger level — store processed `message_id` values (e.g. in workflow static data) and skip execution if already seen; or make all operations fully idempotent
