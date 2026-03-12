# Lessons — Notion integration

> Load when: integrating Notion in n8n (API calls, DB IDs, credentials, content limits).

---

## [notion] · Rule · 2000-char limit is per rich_text object, not per page
> 2026-03-01 · source: ghost
- Notion API rejects any single `rich_text` element exceeding 2000 characters — error: `body.children[0].paragraph.rich_text[0].text.content.length should be ≤ 2000`
- AI-generated descriptions easily exceed this
- Workarounds: truncate at 1997 chars (simple), or split into multiple paragraph blocks via HTTP Request node (preserves content); the n8n Notion node cannot handle dynamic block arrays

## [notion] · Rule · Notion DB ID must come from the DB's own URL, not a parent page
> 2026-03-10 · source: project-init-skill
- Copying a DB ID from a parent page or linked view gives the wrong ID → 404 on every API call
- Correct ID is the 32-char hex in the DB's own URL: `notion.so/<workspace>/<id>?v=...`
- Dashes are optional — the API accepts both formats

## [notion] · Rule · Notion integration must be connected directly to each target DB
> 2026-03-10 · source: project-init-skill
- An integration used in n8n for one DB still returns 404 on a different DB in the same workspace
- Notion requires explicit per-DB connection: open DB → `...` → Connections → add integration
- Don't assume workspace-level or parent-page access grants visibility to all DBs
