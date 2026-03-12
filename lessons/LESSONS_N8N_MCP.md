# Lessons — n8n MCP tool usage

> Load when: using n8n-mcp tools to build or modify workflows (updateNode, addNode, addConnection, GET→PUT patterns).

---

## [n8n] · Rule · updateNode replaces parameters entirely, does not merge
> 2026-03-01 · source: ghost
- `updateNode` in `n8n_update_partial_workflow` replaces the entire `parameters` object with whatever you provide — it does not merge
- Providing only `{blockUi: {...}}` wipes all other params (resource, operation, databaseId, title, etc.) — workflow fails with `WorkflowHasIssuesError`
- Always include the full parameters object when using updateNode, or read current params first and patch only what changed

## [n8n] · Guideline · Dot notation for partial param updates in updateNode
> 2026-03-03 · source: ghost
- `updates: {"parameters.jsCode": "..."}` patches a single field inside parameters without replacing the full object
- contrast with `updates: {parameters: {...}}` which replaces entirely (see updateNode lesson above)
- use dot notation when changing one field; use full object when restructuring params
- **caveat**: unreliable for complex nested objects (e.g. `parameters.conditions` on IF nodes) — n8n sanitization may silently revert the change; always verify with a GET after; for IF node conditions always use the full `parameters` object

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

## [n8n] · Rule · Dot notation on array indices in updateNode creates new keys, does not patch array
> 2026-03-04 · source: ghost (Format Response node)
- `updates: {"parameters.assignments.assignments[0].value": "..."}` does NOT update the array element at index 0; it creates a new sibling key `assignments[0]` inside the object, leaving the original array untouched
- the corrupted structure (both `assignments` array and `assignments[0]` key) causes further expression errors at execution time; hard to spot without reading raw node parameters
- rule: dot notation works for scalar fields only; for array elements, always pass the full `parameters` object in the updateNode update

## [n8n] · Rule · n8n_update_partial_workflow — correct format for updateNode, addConnection, removeConnection
> 2026-03-10 · source: family-content-manager
- `updateNode` requires `updates: {...}` wrapper — `{type:"updateNode", nodeName:"X", parameters:{...}}` fails with "Missing required parameter 'updates'"; correct: `{type:"updateNode", nodeName:"X", updates:{"parameters.field": value}}`
- `addConnection` and `removeConnection` require flat format — `source`/`target` at top level, NOT nested in a `connection: {}` object; nested silently resolves to `undefined` → "Source node not found: undefined"
- IF node connections: always use `branch:"true"` / `branch:"false"` instead of `sourceIndex` — `sourceIndex:0` puts ALL connections on the TRUE branch regardless of intent
