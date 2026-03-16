# Lessons — Slack integration

> Load when: integrating Slack in n8n (credentials, Events API, sending messages).

---

## [slack] · Rule · Events API requires bot user in channel — user token not enough
> 2026-03-02 · source: ai-networking-system
- Slack Events API `message.channels` requires the app's bot user to be a member of the channel — user token scopes alone are insufficient
- If the app has no bot user configured (only user token scopes), the bot can't join channels and the Events API won't fire
- For once-a-week or infrequent events: polling via `conversations.history` + cron is simpler; user token with `channels:history` scope can read public channel history without joining

## [slack] · Rule · Slack Header Auth credential — Name must be `Authorization`, not the credential label
> 2026-03-11 · source: ai-networking-system
- Credential created with Name: `Slack_NW` (the display label) → Slack API returned `not_authed` — the wrong HTTP header was sent
- Header Auth `Name` field IS the literal HTTP header name; any value other than `Authorization` is silently wrong
- Correct: Name: `Authorization`, Value: `Bearer xoxp-TOKEN` (include `Bearer ` prefix)

## [slack] · Rule · Slack Workflow Builder has no outgoing webhook step — use polling instead
> 2026-03-16 · source: ai-networking-system
- Slack Workflow Builder has no native "send webhook" / "HTTP POST" action — adding one requires building a custom Slack app with SDK + hosted run handler
- Any n8n workflow waiting for a Slack-triggered webhook call will never fire without this custom app
- For infrequent channel events (weekly, daily): poll `conversations.history` via cron instead — use existing xoxp- token with `channels:history` scope + `$getWorkflowStaticData` for deduplication (write-first: mark processed before returning the message)

## [slack] · Rule · Bot Token Scopes presence determines sender identity — not the token type
> 2026-03-12 · source: ai-networking-system (confirmed end-to-end)
- **App with any Bot Token Scopes** + xoxp- token → message appears as the bot profile in Slack UI
- **App with zero Bot Token Scopes** + xoxp- token → message appears as the personal user profile ✅
- `as_user: true` is irrelevant — do not use it
- API response always shows `bot_id` — ignore it; what matters is the UI display
- `conversations.open` to get DM channel ID → `chat.postMessage` with `channel` + `text` is the correct pattern
- Setup: create Slack app → add ONLY User Token Scopes (`chat:write`, `users:read`) → add ZERO Bot Token Scopes → install → use xoxp- token
