---
description: Compact context while preserving session decisions, task state, and active constraints
---

Run `/compact` with these instructions:

"Preserve: all decisions made this session, current task state, active constraints, any file paths or IDs referenced in the current task. Compress everything else."

> Note: CLAUDE.md is re-injected from disk after compaction — global rules are never lost. What compaction can lose is session-specific content (decisions, task progress, open questions). This command ensures those are kept.
