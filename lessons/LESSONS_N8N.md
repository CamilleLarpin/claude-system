# Lessons — n8n ecosystem

> Scope: n8n, Slack, Notion gotchas.
> NEVER delete entries. Split into sub-files at 150 lines.

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

## [n8n] · Rule · updateNode replaces parameters entirely, does not merge
> 2026-03-01 · source: ghost
- `updateNode` in `n8n_update_partial_workflow` replaces the entire `parameters` object with whatever you provide — it does not merge
- Providing only `{blockUi: {...}}` wipes all other params (resource, operation, databaseId, title, etc.) — workflow fails with `WorkflowHasIssuesError`
- Always include the full parameters object when using updateNode, or read current params first and patch only what changed

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

## [slack] · Rule · Events API requires bot user in channel — user token not enough
> 2026-03-02 · source: ai-networking-system
- Slack Events API `message.channels` requires the app's bot user to be a member of the channel — user token scopes alone are insufficient
- If the app has no bot user configured (only user token scopes), the bot can't join channels and the Events API won't fire
- For once-a-week or infrequent events: polling via `conversations.history` + cron is simpler; user token with `channels:history` scope can read public channel history without joining

## [n8n] · Guideline · Dot notation for partial param updates in updateNode
> 2026-03-03 · source: ghost
- `updates: {"parameters.jsCode": "..."}` patches a single field inside parameters without replacing the full object
- contrast with `updates: {parameters: {...}}` which replaces entirely (see updateNode lesson above)
- use dot notation when changing one field; use full object when restructuring params
- **caveat**: unreliable for complex nested objects (e.g. `parameters.conditions` on IF nodes) — n8n sanitization may silently revert the change; always verify with a GET after; for IF node conditions always use the full `parameters` object

## [n8n] · Rule · IF node isNotEmpty unreliable — use notEquals instead
> 2026-03-03 · source: ghost (confirmed 2026-03-03)
- `isNotEmpty` on an IF node can evaluate FALSE even when the value is a clearly non-empty string — confirmed with `project_hint: "Claude excellence"` routing to the false branch
- `String()` coercion around the expression does NOT fix this; the bug persists at typeVersion ≤ 2.2
- Fix: use operator `notEquals` with `rightValue: ""` instead of `isNotEmpty`; also upgrade typeVersion to 2.3
- `={{ String($json.field ?? '') }}` + `notEquals ""` is the reliable pattern for non-empty string checks

## [n8n] · Rule · updateNode uses nodeId/nodeName, not id/name
> 2026-03-03 · source: ghost
- `n8n_update_partial_workflow` updateNode operations require `nodeId` (not `id`) or `nodeName` (not `name`) to reference the target node
- passing `{type: "updateNode", id: "..."}` silently uses an empty name and fails with "Node not found for updateNode: ''"
- always use `nodeId: "..."` or `nodeName: "..."` in updateNode operations

## [n8n] · Rule · n8n_update_partial_workflow adds internal settings fields that PUT API rejects
> 2026-03-03 · source: family-content-manager
- After adding/updating nodes via `n8n_update_partial_workflow`, the workflow's `settings` object gains internal fields (`callerPolicy`, `availableInMCP`, `timeSavedMode`, `binaryMode`) that n8n stores internally but the public API rejects on PUT → "request/body/settings must NOT have additional properties"
- Any workflow that does GET → modify → PUT silently breaks after a partial update touches settings
- In the Code node that prepares the PUT body, allowlist settings: `const ALLOWED = ['executionOrder','saveDataErrorExecution','saveDataSuccessExecution','saveManualExecutions','saveExecutionProgress','executionTimeout','timezone','errorWorkflow']; const cleanSettings = Object.fromEntries(Object.entries(full.settings ?? {}).filter(([k]) => ALLOWED.includes(k)));`

## [n8n] · Guideline · MCP-created nodes get wrong credential when multiple exist
> 2026-03-03 · source: family-content-manager
- Nodes added via `n8n_update_partial_workflow` (addNode) are assigned the first available credential of the matching type — not necessarily the correct one
- Fails silently with "Unknown error" at runtime; difficult to trace without checking credentials explicitly
- After adding any node via MCP that requires a credential, open the canvas and verify the credential before testing

## [n8n] · Rule · `\n` in Set node expression strings causes "invalid syntax" — use String.fromCharCode(10)
> 2026-03-04 · source: ghost (Format Response node)
- `'\n'` inside a Set node expression (e.g. `'\n→ '`) is stored as a literal newline in the workflow JSON; n8n's expression evaluator sees an unterminated string literal and throws "invalid syntax"
- the error is indistinguishable from a JS syntax error — no hint that it's an encoding issue; persists even after other expression fixes since those don't affect the `\n`
- fix: use `String.fromCharCode(10)` in place of `'\n'` in n8n expressions — produces an actual newline without escape parsing

## [n8n] · Rule · Dot notation on array indices in updateNode creates new keys, does not patch array
> 2026-03-04 · source: ghost (Format Response node)
- `updates: {"parameters.assignments.assignments[0].value": "..."}` does NOT update the array element at index 0; it creates a new sibling key `assignments[0]` inside the object, leaving the original array untouched
- the corrupted structure (both `assignments` array and `assignments[0]` key) causes further expression errors at execution time; hard to spot without reading raw node parameters
- rule: dot notation works for scalar fields only; for array elements, always pass the full `parameters` object in the updateNode update

## [telegram] · Rule · Markdown mode strips underscores from stored message text — breaks data extraction from replies
> 2026-03-09 · source: family-content-manager
- Filename `2025-08-22_ConventionAuPair_MinistereInterieur_Schwebe-12mois.pdf` sent in a Telegram notification came back as `2025-08-22ConventionAuPairMinistereInterieurSchwebe-12mois.pdf` in `reply_to_message.text` — underscores gone. Correction path built the wrong WebDAV URL → 404.
- Telegram Markdown mode interprets `_word_word_` as italic markers and removes underscores from the stored text. Any workflow that extracts data from `reply_to_message.text` will receive corrupted values if the sending node used Markdown parse_mode (or n8n defaulted to it).
- Fix: set `parse_mode: HTML` on ALL Telegram send nodes — not just those in the correction flow. Confirmation and error messages also include filenames; an incomplete fix leaves silent corruption paths open.

## [notion] · Rule · 2000-char limit is per rich_text object, not per page
> 2026-03-01 · source: ghost
- Notion API rejects any single `rich_text` element exceeding 2000 characters — error: `body.children[0].paragraph.rich_text[0].text.content.length should be ≤ 2000`
- AI-generated descriptions easily exceed this
- Workarounds: truncate at 1997 chars (simple), or split into multiple paragraph blocks via HTTP Request node (preserves content); the n8n Notion node cannot handle dynamic block arrays
