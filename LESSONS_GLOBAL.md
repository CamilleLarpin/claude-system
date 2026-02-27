# Global Lessons Library

> Load when: debugging or starting a build.
> NOT HERE: cross-project decisions with rationale (→ DECISIONS_GLOBAL.md).
> Prune at 150 lines — split by category if file exceeds 500 lines.

---

## Format
```
## [category] Short title
> YYYY-MM-DD · source: [project or session]
- what happened / what the trap is
- why it matters
- what to do instead
```

---

## [n8n] Expression syntax — Code nodes vs expression fields
> unknown · source: unknown
- `$now.toFormat()` works only in expression fields `{{ }}`; `={{ }}` is wrong in n8n
- Code nodes run JavaScript — n8n expression helpers are not available there
- Inside Code nodes use `new Date().toISOString().slice(0,10)` instead

## [n8n] Node parameter defaults are unreliable
> unknown · source: unknown
- Default values are not guaranteed — workflows that pass validation can still crash at runtime due to missing params
- Silent failures are hard to trace back to a missing default
- Set ALL parameters explicitly; always run `validate_node({mode: 'full', profile: 'runtime'})` before deploying

## [n8n] Merge node defaults to Append, not Combine
> unknown · source: unknown
- Merge node default mode is Append — not Combine
- Wrong mode silently drops or duplicates data across branches
- For voice/text path merge: Mode=Combine, CombineBy=Position, IncludeUnpaired=true; use Position (not Matching Fields) when paths share no common fields

## [n8n] Execute Workflow input configuration
> unknown · source: unknown
- "Add option" in the caller node appears disabled by design when no trigger inputs are defined
- Sub-workflow inputs must be defined in the Execute Workflow Trigger first — the caller auto-discovers them after

## [n8n] GitHub onError returns empty object, not null
> unknown · source: unknown
- GitHub node returns `{}` on missing file — no content field, no error thrown
- Absence of error does not mean the file exists
- Always check `if (item.json.content)` before decoding base64

## [n8n] $getWorkflowStaticData for cross-execution persistence
> unknown · source: unknown
- `$getWorkflowStaticData` is available in Code nodes only; persists key-value at workflow level in n8n DB
- Always key by user_id; read at start of execution, write after computing
```javascript
const state = $getWorkflowStaticData('global');
const saved = state[userId] || null;  // read
state[userId] = newValue;             // write
```

## [n8n] Set node field propagation
> unknown · source: unknown
- Set nodes only output explicitly configured fields — nothing passes through automatically
- Assuming implicit pass-through causes silent data loss downstream
- Map the full data flow before configuring; list every field needed downstream explicitly

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
