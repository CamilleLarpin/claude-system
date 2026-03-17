---
description: Show the correct /compact command with preservation instructions — does NOT compact itself
---

**This skill does NOT compact context.** Type this directly in the CLI input bar:

```
/compact Keep: all decisions made this session, current task state, active constraints, active file paths. Compress everything else.
```

`/compact` is a Claude Code built-in slash command — it must be typed in the input bar, not sent as a message.

If context is too loaded to compact usefully: `/end-of-session` → `/commit-push` → `/clear`
