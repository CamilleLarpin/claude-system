# Lessons — n8n ecosystem (continued)

> Scope: n8n, Slack, Notion gotchas.
> Split into sub-files at 150 lines.
> Continued from LESSONS_N8N.md.

---

## [telegram] · Rule · Telegram bots are public by default — always add chat_id allowlist
> 2026-03-11 · source: session
- Any Telegram user who finds your bot can send it messages; n8n workflows will process them without restriction
- Unauthorized users can trigger automation, consume API credits, or exfiltrate workflow outputs
- Add an IF node immediately after the Telegram Trigger: condition `$json.message.chat.id == YOUR_CHAT_ID`; connect the false branch to a No-op or leave it unconnected (unauthorized messages are silently dropped). For multi-user bots, use a Code node with an explicit allowlist array.
