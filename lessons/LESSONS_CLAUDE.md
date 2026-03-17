# Lessons — Claude & skills

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
