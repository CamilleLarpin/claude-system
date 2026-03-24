# Lessons — Claude Code tool usage

> Load when: configuring Claude Code · managing context · working with MCPs, agents, commands, or sessions.
> Scope: Claude Code-specific behavior — context, MCPs, agents, commands, /schedule, CLAUDE.md.
> Split into sub-files at 150 lines.

---

## [claude-code] · Rule · MCP token cost — evaluate footprint before adopting
> 2026-03-17 · source: CLAUDE_CODE_COURSE_ANALYSIS.md
- A single poorly written MCP can consume 20%+ of the context window before you send the first message — this compounds across all sessions that load it
- Easy to miss: the MCP appears to "work" while silently degrading every subsequent call
- Before adopting any MCP in a Claude Code session: check its token footprint; prefer skills (load on demand) over MCPs (always loaded) for anything not used every session

## [claude-code] · Guideline · Primacy/recency bias — front-load and back-load critical rules in CLAUDE.md
> 2026-03-17 · source: CLAUDE_CODE_COURSE_ANALYSIS.md
- Claude weights the first and last sections of any prompt more than the middle
- Critical must-never-do rules and security constraints buried mid-file get less weight at runtime
- Put the most important rules at the top of CLAUDE.md and repeat or summarise the hardest constraints at the bottom

## [claude-code] · Rule · Previous session context lives in ~/.claude/projects/<slug>/*.jsonl
> 2026-03-18 · source: gmail-inbox-cleanup session
- Each Claude Code conversation is stored as a JSONL file in `~/.claude/projects/<slug>/` — one file per session, named by UUID
- When the user says "we discussed this yesterday" or "look at the previous conversation", do NOT say the context is unavailable — check `~/.claude/projects/<slug>/` sorted by modification time, read the most recent relevant file, extract text blocks from assistant/user messages
- The slug matches the project path with `/` replaced by `-`, e.g. `/Users/camillelarpin/projects/gmail-inbox-cleanup` → `-Users-camillelarpin-projects-gmail-inbox-cleanup`

## [claude-code] · Guideline · /compact with explicit preservation instructions
> 2026-03-17 · source: CLAUDE_CODE_COURSE_ANALYSIS.md
- Default `/compact` produces a generic summary — it may lose decisions, current task state, or key constraints
- Losing context mid-build causes Claude to revisit resolved decisions or miss active constraints
- Use `/compact` with explicit instructions: e.g. "keep all decisions made this session, current task state, and active constraints; compress everything else"

## [claude-code] · Guideline · CLAUDE.md pruning — treat as technical debt, not append-only
> 2026-03-17 · source: CLAUDE_CODE_COURSE_ANALYSIS.md
- CLAUDE.md accumulates stale, redundant, or over-precise rules over time — each one adds token cost on every load
- Distinction: LESSONS files are append-only (never delete hard-won patterns); CLAUDE.md is the live ruleset and should be pruned when rules no longer apply
- Periodically review CLAUDE.md for stale rules; archive superseded ones; do not let it grow unbounded

## [claude-code] · Guideline · Rules in CLAUDE.md, repeatable tasks as skills
> 2026-03-17 · source: CLAUDE_CODE_COURSE_ANALYSIS.md
- Putting task procedures (e.g. end-of-session ritual, commit flow) in CLAUDE.md loads them on every session even when unused
- Skills load only when invoked — zero token cost otherwise
- Move any repeatable, triggered procedure out of CLAUDE.md into a skill file; keep CLAUDE.md for always-applicable rules and constraints only

## [claude-code] · Rule · /compact skill generates a prompt — it does NOT compact context
> 2026-03-17 · source: finances-ezerpin session
- A skill named `compact` in `~/.claude/commands/` only outputs preservation instructions as text — it does not trigger Claude Code's built-in context compaction
- User runs the prompt as a message → nothing compacts; context stays full; session continues degraded
- Correct usage: type `/compact [preservation instructions]` directly in the CLI input bar — this triggers the actual built-in compaction
- If context is too loaded to compact usefully: `/end-of-session` → `/commit-push` → `/clear` is the clean alternative
- The `compact` skill should be deleted or replaced with a note pointing to the correct built-in command

## [claude-code] · Guideline · MCP→Skill promotion rule — try MCP first, convert once validated
> 2026-03-18 · source: prioritization session
- MCPs are fast to set up but always-loaded (token cost on every session); skills load only on invocation (zero cost otherwise)
- Pattern: adopt as MCP first to validate the tool is worth using; once confirmed useful and stable, convert to a skill for long-term token efficiency
- Do NOT start with a skill if you're unsure whether you'll use the tool — MCP lets you evaluate with minimal investment

## [claude-code] · Rule · Custom agents in .claude/agents/ are not subagent_type values
> 2026-03-19 · source: reviewer agent test
- Claude Code's Agent tool only accepts built-in subagent_type values: general-purpose, Explore, Plan, statusline-setup, claude-code-guide. Custom `.md` files in `.claude/agents/` are NOT registered there — calling subagent_type "reviewer" fails with "Agent type not found"
- Correct pattern: create a paired `~/.claude/commands/<name>.md` that spawns a general-purpose agent with the agent's system prompt embedded; invoke via `/<name>`
- Agent `.md` files = source of truth for instructions; command file = invocation layer

## [claude-code] · Guideline · Agents vs commands — choose by bias and context isolation
> 2026-03-19 · source: claude-setup session (agents pattern)
- Commands run inside the current conversation — they see full history and are biased by prior reasoning; good for interactive workflows, multi-turn tasks, things that need conversation state
- Agents run as isolated sub-processes with blank context — no history, no bias; good for quality gates (e.g. code reviewer must not see implementation reasoning), parallel tasks, checks that should be objective
- Invoke via paired slash command (e.g. `/review`) — not by asking Claude to "use the reviewer agent" (that tries subagent_type which fails for custom agents)

## [claude-code] · Rule · /schedule creates remote agents — incompatible with interactive skills
> 2026-03-24 · source: ~/.claude/ setup session
- Remote triggers (CCR) spawn fully isolated cloud sessions — no user present, no back-and-forth possible; attempting to run an interactive skill produces a headless monologue with no value
- Pattern for periodic interactive skills: remote agent does headless prep (reads files, writes findings report, commits to repo) → user runs the interactive skill with findings as pre-loaded context
- Match the execution model to the skill type before scheduling: autonomous jobs for headless tasks, scheduled reminders for interactive ones
