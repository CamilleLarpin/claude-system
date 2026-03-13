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
