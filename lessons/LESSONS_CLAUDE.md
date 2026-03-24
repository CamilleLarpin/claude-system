# Lessons — Claude & skills

> Load when: authoring skills or commands · debugging Claude behavior · reviewing setup.
> Scope: Claude behavior, skills authoring, Claude Code usage.
> Split into sub-files at 150 lines.

---

## [skills] · Guideline · Skill authoring — trigger and body
> 2026-02-DD · source: Anthropic docs + community research
- Only `name` + `description` frontmatter are pre-loaded — Claude undertriggers by default
- Vague descriptions cause missed triggers; bloated bodies waste tokens on every load
- Use third-person imperative: "This skill should be used when..."; keep body under 500 lines; move detail to `references/`, deterministic code to `scripts/`; test with 20 eval queries mixing should-trigger and should-not-trigger cases

## [skills] · Guideline · Skills exclusivity
> 2026-02-26 · source: coaching session
- If two skills can both answer the same question, one is wrong — overlapping skills waste tokens and produce inconsistent behavior
- Ambiguity is invisible at authoring time but expensive at runtime
- When adding a new skill, explicitly check for overlap with existing skills; consolidate or sharpen the boundary before shipping

## [anthropic-sdk] · Rule · Wrong model ID produces empty response, not an exception
> 2026-03-06 · source: data-engineering-notes
- Using an invalid model ID (e.g. `claude-sonnet-4-20250514`) causes the API to return an empty/malformed body — `json.loads` fails with `JSONDecodeError: Expecting value` on an empty string; the root cause is invisible without debug logging
- Always use exact model ID format: `claude-sonnet-4-6`, `claude-opus-4-6`, `claude-haiku-4-5-20251001`; log the raw response before `json.loads` to surface this faster

## [claude-behavior] · Guideline · Don't infer a template — ask for it
> 2026-03-03 · source: data-engineering-notes
- Trying to infer a format by reading related files wastes round-trips and risks using the wrong reference
- If a template or format standard exists, ask the user to confirm it before proceeding
- When you need a template: stop, ask, then act

## [claude-api] · Rule · Strip ```json code fences before json.loads()
> 2026-03-12 · source: audio-intelligence-pipeline
- Claude wraps JSON in ` ```json ... ``` ` even when the prompt explicitly says "return ONLY a JSON object — no other text"; `json.loads()` then fails with `JSONDecodeError: Expecting value`
- Silent in logs — the error points at `json.loads`, not at Claude's output format
- Fix: always strip code fences before parsing: check `if raw.startswith("```")`, split on "```", strip the `json` language tag, then call `json.loads(raw.strip())`

## [prompt] · Rule · LLM outputs reasoning after (none) unless explicitly forbidden
> 2026-03-16 · source: claude-one-digest
- Prompt said "If no X found, output: (none)" — model output `(none)\n\n**Reasoning:** ...` explaining its decision; downstream code checking `result == "(none)"` misses it; the reasoning block ends up in saved output
- Fix in prompt: "output ONLY (none), no reasoning, no explanation"; fix in code: check `result.startswith("(none)")` not just equality

## [prompt] · Guideline · Strip trailing `(none)` from responses that use it as a fallback marker
> 2026-03-13 · source: claude-one-digest
- Prompt said "If no concepts, output: (none)" — Claude appended `(none)` at the end of a response that already contained valid content, treating it as a section terminator
- The stray `(none)` appears in saved output and confuses readers; no error is raised
- Strip after receiving: `if result.endswith("(none)"): result = result[:-len("(none)")].rstrip()`; handle the empty-response case separately

## [claude-behavior] · Rule · Execution gate — plan before any multi-step or external-system task
> 2026-03-09 · source: biography (recurring failure)
- Pattern: Claude jumps into execution on complex tasks the moment it has enough context to act — skipping the plan→validate step entirely
- Impact: wasted work, irreversible actions taken, user loses trust; especially bad for n8n/GitHub/API tasks
- Fix encoded in CLAUDE.md "Build discipline": STOP when task has >2 steps or touches an external system; output a numbered plan; wait for explicit approval of that specific plan before calling any tool
- "Go ahead" or "do it" without a prior plan shown is NOT approval

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

## [skills] · Rule · Commands must @-reference shared rules, never embed them inline
> 2026-03-18 · source: prioritize session
- Inline philosophy blocks in commands (`/prioritize`, `/add-to-backlog`) duplicated the same rules in two places — one update missed the other, causing drift within the same session
- The correct pattern: extract shared rules to a single file (e.g. `DECISIONS_CONVENTIONS.md`) and `@`-reference it from every command that needs it; commands stay thin, truth stays in one place
- Applies to any rule, philosophy, or convention referenced by more than one command or skill

## [skills] · Rule · Multi-step skills must be conversational — one step, one question, then wait
> 2026-03-19 · source: ai-networking-system (/align skill)
- Running all steps of a structured skill in a single message produces a wall of analysis the user didn't co-build — goes in the wrong direction without checkpoints
- User said "way too much in a row" and "you go in the wrong direction by yourself"
- For any skill structured as a sequence of steps: end each step with ONE question, stop, and wait for the user's response before proceeding. The user builds the output with you. Add an explicit "How this works" block at the top of the skill: "This is a conversation, not a report. Each step ends with a question. Wait for the user's response before moving to the next step. Never run multiple steps in one message."

## [claude-code] · Guideline · MCP→Skill promotion rule — try MCP first, convert once validated
> 2026-03-18 · source: prioritization session
- MCPs are fast to set up but always-loaded (token cost on every session); skills load only on invocation (zero cost otherwise)
- Pattern: adopt as MCP first to validate the tool is worth using; once confirmed useful and stable, convert to a skill for long-term token efficiency
- Do NOT start with a skill if you're unsure whether you'll use the tool — MCP lets you evaluate with minimal investment

## [claude-behavior] · Rule · Never state infrastructure facts as truth without verification
> 2026-03-19 · source: ai-networking-system
- Said "Traefik already runs on your Hetzner stack (n8n uses it)" — stated as fact; written into DECISIONS_INFRA.md; persisted across sessions. Traefik was not running at all.
- Root cause: the exercise prompt listed Traefik as an option; plausible-sounding assumption was stated as verified fact
- Before writing any claim about running infrastructure into a decision: require `docker ps`, `systemctl status`, or equivalent evidence. "Likely", "probably", and "already" are red flags — replace with "please verify with X command"

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

## [claude-setup] · Rule · Punctuation in setup files is semantic — follow writing convention
> 2026-03-20 · source: ~/.claude/ review session
- Inconsistent punctuation (mixing `—`, `;`, `,`, `·`) forces re-parsing and creates ambiguity; in setup files every character should carry a defined role
- Convention: `—` = structural separator (label → content); `·` = inline list items; `→` = sequence or pointer; `;` = two independent conditions in one bullet; `-` = compound words only; no trailing `.` on bullets; capital first word per bullet, lowercase after `—` or `·`
- Full reference in `~/.claude/skills/review-setup/SKILL.md` > Writing Convention

## [skills] · Rule · `@`-referenced files are hard dependencies — break silently on rename
> 2026-03-20 · source: ~/.claude/ review session
- Commands using `@~/.claude/some-file.md` auto-load that file; if the file is renamed or split, the reference silently stops working — no error, just missing context
- Trap is invisible: the command still runs, it just doesn't load the file it needs
- Before renaming or splitting any file: `grep -r "<filename>" ~/.claude/` to find all callers; update them first. When splitting: update callers to the new paths directly — no index-of-indexes

## [skills] · Guideline · Downloaded SKILL.md files may be massively overweight
> 2026-03-20 · source: ~/.claude/ review session
- Open-source skills embed Summary, Best Practices Do/Don't, Related Skills, and Quick Reference Checklist sections directly in SKILL.md — these load in full on every invocation regardless of whether they're needed
- These sections are retrieval-tier content at the wrong load tier; they restate what's already in the skill body and add 80–250 lines each
- On adoption: check SKILL.md line count; trim those 4 sections if present — reference files (already linked at the bottom) carry the full detail; the skill itself is safe to re-download if needed

## [claude-setup] · Rule · When adding a pull step to one command, audit all sibling commands for the same gap
> 2026-03-24 · source: ~/.claude/ setup session
- Added `git pull --rebase` to `/start` in a prior session; this session discovered `/overview` and `/prioritize` read the same shared repo (`projects-tracking`) without pulling — stale reads were silently possible
- Pattern: a fix applied to one command often reveals the same gap in all commands with the same input source
- When adding a pull/sync step to any command: grep for all other commands reading the same source; apply consistently before closing the task

## [llm] · Rule · Python .format() breaks on prompt strings containing literal braces
> 2026-03-18 · source: gmail-inbox-cleanup
- Prompt strings with JSON examples like `{"key": "value"}` cause `KeyError` when passed to `.format()` — Python interprets `{key}` as a format placeholder
- Silent until runtime; error message points at the key name, not the brace
- Fix: escape literal braces by doubling them `{{"key": "value"}}`, or use a different substitution method (e.g. `prompt.replace("{emails_json}", value)`)
