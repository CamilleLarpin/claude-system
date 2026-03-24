# Lessons — Claude & skills

> Load when: authoring skills or commands · debugging Claude behavior · reviewing setup.
> Scope: Claude behavior, skills authoring, prompting, setup file conventions.
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

## [claude-behavior] · Rule · Never state infrastructure facts as truth without verification
> 2026-03-19 · source: ai-networking-system
- Said "Traefik already runs on your Hetzner stack (n8n uses it)" — stated as fact; written into DECISIONS_INFRA.md; persisted across sessions. Traefik was not running at all.
- Root cause: the exercise prompt listed Traefik as an option; plausible-sounding assumption was stated as verified fact
- Before writing any claim about running infrastructure into a decision: require `docker ps`, `systemctl status`, or equivalent evidence. "Likely", "probably", and "already" are red flags — replace with "please verify with X command"

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
