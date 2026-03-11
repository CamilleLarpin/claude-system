# Lessons — n8n ecosystem (continued)

> Scope: n8n, Slack, Notion gotchas.
> Split into sub-files at 150 lines.
> Continued from LESSONS_N8N.md.

---

## [slack] · Rule · Slack Header Auth credential — Name must be `Authorization`, not the credential label
> 2026-03-11 · source: ai-networking-system
- Credential created with Name: `Slack_NW` (the display label) → Slack API returned `not_authed` — the wrong HTTP header was sent
- Header Auth `Name` field IS the literal HTTP header name; any value other than `Authorization` is silently wrong
- Correct: Name: `Authorization`, Value: `Bearer xoxp-TOKEN` (include `Bearer ` prefix)

## [slack] · Rule · `chat.postMessage` with xoxp- token + bot-enabled Slack app sends as bot, not as user
> 2026-03-11 · source: ai-networking-system
- `as_user: true` is deprecated and ignored when the Slack app has a bot user — message is sent from the bot profile, lands in the app DM thread, not as a user-to-user DM
- Debug: `curl https://slack.com/api/auth.test -H "Authorization: Bearer TOKEN"` — if `bot_id` is present, the token is bot-linked regardless of `xoxp-` prefix
- Fix: use a legacy Slack app without a bot user configured; OR accept bot sender; `as_user: true` alone is insufficient

## [telegram] · Rule · Square brackets `[text]` also stripped in Telegram Markdown mode — same root cause as underscores
> 2026-03-11 · source: ai-networking-system
- `[id:U06L11F1RN1]` sent with Markdown parse_mode stored as `id:U06L11F1RN1` — brackets removed (Telegram treats `[...]` as link syntax)
- Regex matching `\[id:...\]` silently fails; same issue as underscores (see LESSONS_N8N.md)
- Fix: use HTML parse_mode (brackets and underscores both preserved); make regexes bracket-tolerant: `\[?id:([A-Z0-9]+)\]?`

## [telegram] · Rule · Telegram bots are public by default — always add chat_id allowlist
> 2026-03-11 · source: session
- Any Telegram user who finds your bot can send it messages; n8n workflows will process them without restriction
- Unauthorized users can trigger automation, consume API credits, or exfiltrate workflow outputs
- Add an IF node immediately after the Telegram Trigger: condition `$json.message.chat.id == YOUR_CHAT_ID`; connect the false branch to a No-op or leave it unconnected (unauthorized messages are silently dropped). For multi-user bots, use a Code node with an explicit allowlist array.
