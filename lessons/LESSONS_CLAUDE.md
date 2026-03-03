# Lessons — Claude & skills

> Scope: Claude behavior, skills authoring, Claude Code usage.
> NEVER delete entries. Split into sub-files at 150 lines.

---

## [skills] Skill authoring — trigger and body
> 2026-02-DD · source: Anthropic docs + community research
- Only `name` + `description` frontmatter are pre-loaded — Claude undertriggers by default
- Vague descriptions cause missed triggers; bloated bodies waste tokens on every load
- Use third-person imperative: "This skill should be used when..."; keep body under 500 lines; move detail to `references/`, deterministic code to `scripts/`; test with 20 eval queries mixing should-trigger and should-not-trigger cases

## [skills] Skills exclusivity
> 2026-02-26 · source: coaching session
- If two skills can both answer the same question, one is wrong — overlapping skills waste tokens and produce inconsistent behavior
- Ambiguity is invisible at authoring time but expensive at runtime
- When adding a new skill, explicitly check for overlap with existing skills; consolidate or sharpen the boundary before shipping

## [claude-behavior] Don't infer a template — ask for it
> 2026-03-03 · source: data-engineering-notes
- Trying to infer a format by reading related files wastes round-trips and risks using the wrong reference
- If a template or format standard exists, ask the user to confirm it before proceeding
- When you need a template: stop, ask, then act
