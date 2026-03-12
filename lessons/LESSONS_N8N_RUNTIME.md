# Lessons — n8n node behavior & runtime

> Load when: building or debugging n8n workflows — node configuration, expressions, runtime gotchas.

---

## [n8n] · Rule · Expression syntax — Code nodes vs expression fields
> unknown · source: unknown
- `$now.toFormat()` works only in expression fields `{{ }}`; `={{ }}` is wrong in n8n
- Code nodes run JavaScript — n8n expression helpers are not available there
- Inside Code nodes use `new Date().toISOString().slice(0,10)` instead

## [n8n] · Rule · Node parameter defaults are unreliable
> unknown · source: unknown
- Default values are not guaranteed — workflows that pass validation can still crash at runtime due to missing params
- Silent failures are hard to trace back to a missing default
- Set ALL parameters explicitly; always run `validate_node({mode: 'full', profile: 'runtime'})` before deploying

## [n8n] · Rule · Merge node defaults to Append, not Combine
> unknown · source: unknown; corrected 2026-03-05 · source: ghost
- Merge node default mode is Append — not Combine
- Wrong mode silently drops or duplicates data across branches
- **Converging Switch pattern** (only one path fires per execution): Append is correct — it passes through whichever input arrives. Do NOT change to Combine; Combine waits for all connected inputs simultaneously and will hang the workflow when only one path fires.
- **Concurrent paths pattern** (multiple paths fire in the same execution): Mode=Combine, CombineBy=Position, IncludeUnpaired=true; use Position (not Matching Fields) when paths share no common fields

## [n8n] · Note · Execute Workflow input configuration
> unknown · source: unknown
- "Add option" in the caller node appears disabled by design when no trigger inputs are defined
- Sub-workflow inputs must be defined in the Execute Workflow Trigger first — the caller auto-discovers them after

## [n8n] · Rule · GitHub onError returns empty object, not null
> unknown · source: unknown
- GitHub node returns `{}` on missing file — no content field, no error thrown
- Absence of error does not mean the file exists
- Always check `if (item.json.content)` before decoding base64

## [n8n] · Guideline · $getWorkflowStaticData for cross-execution persistence
> unknown · source: unknown
- `$getWorkflowStaticData` is available in Code nodes only; persists key-value at workflow level in n8n DB
- Always key by user_id; read at start of execution, write after computing
```javascript
const state = $getWorkflowStaticData('global');
const saved = state[userId] || null;  // read
state[userId] = newValue;             // write
```

## [n8n] · Rule · Set node field propagation
> unknown · source: unknown
- Set nodes only output explicitly configured fields — nothing passes through automatically
- Assuming implicit pass-through causes silent data loss downstream
- Map the full data flow before configuring; list every field needed downstream explicitly

## [n8n] · Guideline · Avoid `}}` in Code node jsCode — triggers false expression error
> 2026-03-02 · source: ghost
- n8n expression validator scans jsCode field for `{{`/`}}` pairs — `}}` from nested object literals (e.g. `return{json:{...}}`) triggers "Unmatched expression brackets" error
- Workflow saves fine but shows as invalid; confusing because the JS is correct
- Assign to an intermediate variable first, then `return {json: out};` — eliminates `}}` at the return site

## [n8n] · Rule · continueOnFail does not suppress downstream nodes — silent false positives
> 2026-03-02 · source: family-content-manager
- Workflow sent a ✅ success notification even though the preceding MOVE failed (412). `continueOnFail: true` keeps the flow running — downstream nodes have no automatic awareness of the upstream failure
- Users act on a success notification that was never true
- After any critical action with `continueOnFail`, check `$json.error` before sending a success notification. Either branch with an IF node, or use a ternary: `={{ $json.error ? '⚠️ Failed' : '✅ Done' }}`

## [n8n] · Rule · IF node isNotEmpty unreliable — use notEquals instead
> 2026-03-03 · source: ghost (confirmed 2026-03-03)
- `isNotEmpty` on an IF node can evaluate FALSE even when the value is a clearly non-empty string — confirmed with `project_hint: "Claude excellence"` routing to the false branch
- `String()` coercion around the expression does NOT fix this; the bug persists at typeVersion ≤ 2.2
- Fix: use operator `notEquals` with `rightValue: ""` instead of `isNotEmpty`; also upgrade typeVersion to 2.3
- `={{ String($json.field ?? '') }}` + `notEquals ""` is the reliable pattern for non-empty string checks

## [n8n] · Rule · `\n` in Set node expression strings causes "invalid syntax" — use String.fromCharCode(10)
> 2026-03-04 · source: ghost (Format Response node)
- `'\n'` inside a Set node expression (e.g. `'\n→ '`) is stored as a literal newline in the workflow JSON; n8n's expression evaluator sees an unterminated string literal and throws "invalid syntax"
- the error is indistinguishable from a JS syntax error — no hint that it's an encoding issue; persists even after other expression fixes since those don't affect the `\n`
- fix: use `String.fromCharCode(10)` in place of `'\n'` in n8n expressions — produces an actual newline without escape parsing
