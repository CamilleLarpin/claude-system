# Lessons — Telegram bot integration

> Load when: integrating Telegram in n8n (sending messages, parse_mode, triggers, security).

---

## [telegram] · Rule · Markdown mode strips underscores from stored message text — breaks data extraction from replies
> 2026-03-09 · source: family-content-manager
- Filename `2025-08-22_ConventionAuPair_MinistereInterieur_Schwebe-12mois.pdf` sent in a Telegram notification came back as `2025-08-22ConventionAuPairMinistereInterieurSchwebe-12mois.pdf` in `reply_to_message.text` — underscores gone. Correction path built the wrong WebDAV URL → 404.
- Telegram Markdown mode interprets `_word_word_` as italic markers and removes underscores from the stored text. Any workflow that extracts data from `reply_to_message.text` will receive corrupted values if the sending node used Markdown parse_mode (or n8n defaulted to it).
- Fix: set `parse_mode: HTML` on ALL Telegram send nodes — not just those in the correction flow. Confirmation and error messages also include filenames; an incomplete fix leaves silent corruption paths open.

## [telegram] · Rule · Square brackets `[text]` also stripped in Telegram Markdown mode — same root cause as underscores
> 2026-03-11 · source: ai-networking-system
- `[id:U06L11F1RN1]` sent with Markdown parse_mode stored as `id:U06L11F1RN1` — brackets removed (Telegram treats `[...]` as link syntax)
- Regex matching `\[id:...\]` silently fails; same issue as underscores
- Fix: use HTML parse_mode (brackets and underscores both preserved); make regexes bracket-tolerant: `\[?id:([A-Z0-9]+)\]?`

## [telegram] · Rule · One webhook per bot token — last activated n8n workflow wins
> 2026-04-28 · source: ai-networking-system (UC5 test)
- n8n registers one webhook with Telegram per bot token. Activating a second workflow using the same bot token silently overwrites the first — it stops receiving messages with no error surfaced.
- Fix: Dispatcher pattern — one workflow owns the Telegram Trigger for the bot; all other workflows use executeWorkflowTrigger (sub-workflows never register a webhook). Route by message type (Switch node) to the appropriate sub-workflow.

## [telegram] · Rule · Telegram file download requires token in URL path — use Telegram node, not HTTP Request
> 2026-04-28 · source: ai-networking-system (UC5 test)
- Downloading a file requires two calls: `getFile` (returns file_path) then `/file/bot{TOKEN}/{file_path}` (binary). Both embed the token in the URL path — incompatible with header-based n8n credentials and `$env` if `N8N_BLOCK_ENV_ACCESS_IN_NODE` is set.
- Fix: use the Telegram node (resource: file, operation: get, fileId: ..., download: true) — one node, uses stored telegramApi credential, returns binary with `data` key.
- Read binary with `this.helpers.getBinaryDataBuffer(0, 'data')` in a downstream Code node.

## [telegram] · Rule · Telegram bots are public by default — always add chat_id allowlist
> 2026-03-11 · source: session
- Any Telegram user who finds your bot can send it messages; n8n workflows will process them without restriction
- Unauthorized users can trigger automation, consume API credits, or exfiltrate workflow outputs
- Add an IF node immediately after the Telegram Trigger: condition `$json.message.chat.id == YOUR_CHAT_ID`; connect the false branch to a No-op or leave it unconnected (unauthorized messages are silently dropped). For multi-user bots, use a Code node with an explicit allowlist array.
