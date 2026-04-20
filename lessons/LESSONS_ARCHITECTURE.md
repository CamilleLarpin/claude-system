# Lessons — architecture & integrations

> Scope: git, ai-agents, system architecture, third-party integrations, infra, bash, shell.
> Load when: building or debugging infra · systems work · third-party integrations.
> LLM/prompt/evaluation lessons → LESSONS_LLM.md

---

→ git-specific lessons: LESSONS_GIT.md

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

## [docker] · Rule · Use `--host 0.0.0.0` when running Uvicorn inside Docker
> 2026-03-12 · source: audio-intelligence-pipeline
- Default `--host 127.0.0.1` binds only inside the container — port mapping (`-p 8000:8000`) has no effect
- Always set `--host 0.0.0.0` in the Dockerfile CMD for any containerised FastAPI/Uvicorn app

## [hetzner] · Rule · Hetzner Firewall must include ports 80 and 443 when nginx is present
> 2026-03-13 · source: server-setup session
- Opening only app ports (5678, 8080, 8000) blocks all domain-based access when nginx sits in front as a reverse proxy — nginx listens on 80/443, not the app ports
- All domain traffic (n8n.helmcome.com, cloud.helmcome.com) timed out immediately after firewall creation; services were running fine but unreachable
- Always include TCP 80 and TCP 443 in any Hetzner Firewall rule set when the server runs a reverse proxy; direct port rules are for fallback/debug only

## [bash] · Rule · Write all CLI commands for the user as single-line strings — no backslash continuations
> 2026-03-13 · source: audio-intelligence-pipeline
- Multi-line commands with `\` continuations break when pasted into zsh — each fragment is treated as a separate command: file paths get "permission denied", flags become "command not found"
- Affects all commands (python, curl, git, etc.), not just long curl calls
- Always write copy-paste commands as one unbroken line; if very long, note it in prose but do not split with `\`

## [integrations] · Rule · Telegram delivers the same webhook update multiple times simultaneously
> 2026-03-03 · source: family-content-manager
- Telegram sometimes sends the same update 2-3× within milliseconds → multiple simultaneous n8n executions triggered by one user action
- Sequential duplicate protection (checking if a file was already moved) doesn't help — all instances start before any finishes; causes MOVE race conditions and 423 Locked on concurrent file writes
- True fix: deduplicate at the trigger level — store processed `message_id` values (e.g. in workflow static data) and skip execution if already seen; or make all operations fully idempotent

## [shell] · Guideline · Ghostty has no OSC title blocking — use a background reset loop
> 2026-03-17 · source: dotfiles session
- Ghostty has no config option to block OSC title escape sequences (OSC 0/2) from running apps; `shell-integration-features = title` and app-sent OSC compete last-in-wins — apps like Claude Code always win
- No `ignore-osc-title`, `title-priority`, or equivalent option exists in Ghostty config reference
- Workaround: wrap the command in zsh to spawn a background loop that resets the title every 0.3s; kill the loop on exit:
  ```zsh
  cmd() {
    local title="${PWD##*/}"
    ( while true; do printf '\033]0;%s\007' "$title"; sleep 0.3; done ) &
    local _pid=$!
    command cmd "$@"
    kill $_pid 2>/dev/null; wait $_pid 2>/dev/null
    printf '\033]0;%s\007' "${PWD##*/}"
  }
  ```

## [shell] · Rule · Ghostty `working-directory = home` does not override OSC 7 from shell integration
> 2026-03-18 · source: dotfiles session
- `working-directory = home` is set in Ghostty config, but new windows (`Cmd+N`) still open in the last active project directory — Ghostty's shell integration sends OSC 7 (current working directory) to the terminal, and new windows inherit that value, overriding the config setting
- The config setting alone is insufficient when `shell-integration = zsh` is active
- Fix: add `cd ~` at the end of `~/.zshrc` — every new shell always starts in `~/` regardless of what Ghostty inherits via OSC 7

## [integrations] · Rule · Read tool documentation before proposing config key names
> 2026-03-18 · source: openclaw-setup
- Proposing OpenClaw config keys from memory led to two consecutive wrong guesses (`heartbeat: {enabled: false}`, `channels.telegram.allowedUsers`) — both rejected; required reading docs to fix
- Wrong keys fail silently, cause boot failure, or get stripped by doctor — hard to trace without knowing the root cause
- Pattern applies to any tool with a config schema (OpenClaw, n8n nodes, etc.): always `cat tool/docs/relevant.md` before proposing a config key; never guess

## [architecture] · Guideline · Distinguish quality gates from hard prerequisites in dependency documentation
> 2026-03-24 · source: meeting-note-taker / ai-networking-system
- A quality gate ("validate quality before building on top") is not the same as a hard prerequisite ("this cannot run without X")
- Pattern that fails: Meeting Note Taker listed audio-intelligence-pipeline Phase 3b (MLflow evaluation) as a hard dependency — it was a quality gate; the pipeline already worked and could be called immediately
- Before adding a `Depends on:` entry, ask: "does this technically block execution, or is it a validation we'd prefer to do first?" — document the difference explicitly; quality gates can be bypassed with risk acknowledgement, hard prerequisites cannot

## [infra] · Rule · Check DNS propagation before running certbot
> 2026-03-25 · source: ai-networking-system
- certbot fails if the subdomain A record doesn't resolve yet — HTTP challenge cannot complete
- Run `dig <subdomain> +short` on the server first — must return the server IP; DNS changes take minutes, not seconds
- Always verify all `-d` domains resolve before running certbot

## [infra] · Rule · GitHub dropped HTTPS password auth — use SSH on servers
> 2026-03-25 · source: ai-networking-system
- `git clone https://github.com/...` fails with "Password authentication is not supported" — GitHub removed this in 2021
- Fix: `ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""` on server → add pubkey to GitHub Settings → SSH keys → clone via `git@github.com:...`
- Do this on every new server before any `git clone`

## [python-packaging] · Rule · `src/` layout requires explicit setuptools config + __init__.py
> 2026-04-01 · source: pea-pme-pulse
- `pip install -e .` does NOT find packages under `src/` automatically — requires `[tool.setuptools.packages.find] where = ["src"]` in `pyproject.toml`
- Without `src/bronze/__init__.py`, the directory is not a package regardless of setuptools config
- Prefect (and other subprocess-based runners) lose any `sys.path` manipulation done in the parent script — packages must be properly installed via pip to be importable in subflows/subprocesses
- Checklist for `ModuleNotFoundError` after `pip install -e .`: (1) `__init__.py` present? (2) `[tool.setuptools.packages.find]` in pyproject.toml? (3) reinstalled after adding them?

## [architecture] · Guideline · Define concrete use cases before automation architecture
> 2026-03-24 · source: meeting-note-taker / ai-networking-system
- Abstract dependency maps between projects obscure what to build first and what value each step delivers
- Start from concrete scenarios: actor, trigger, input, expected output — then derive build sequence from value delivered per step
- Pattern: "Meeting Note Taker depends on audio-intelligence-pipeline" hid that UC-B (in-person capture) only needed Telegram + existing FastAPI + CRM deploy — no new pipeline work required

## [pytest] · Rule · `tests/<pkg>/__init__.py` shadows `src/<pkg>/` — delete it
> 2026-04-02 · source: pea-pme-pulse
- When `tests/bronze/__init__.py` exists, pytest resolves `from bronze.x import` to `tests/bronze/` (not `src/bronze/`) → ModuleNotFoundError
- Fix: delete `__init__.py` from test subdirectories when using `pythonpath = ["src"]` in pyproject.toml
- Rule: test directories should not have `__init__.py` with a `src/` layout

→ git-specific lessons: LESSONS_GIT.md
