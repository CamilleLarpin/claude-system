---
description: Compact context while preserving session decisions, task state, and active constraints
---

**This skill does NOT compact context** — it only generates preservation instructions.

To actually compact, type this directly in the CLI input bar (replacing `[...]` with what to preserve):

```
/compact Keep: all decisions made this session, current task state, active constraints, active file paths. Compress everything else.
```

> Note: `/compact` is a Claude Code built-in command. Skills in `~/.claude/commands/` cannot trigger it. The instructions above must be typed as a slash command directly — not sent as a message to Claude.
