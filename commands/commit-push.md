# Commit and Push Claude Files

Commit and push all dirty `.claude/` and `~/.claude/` files.

**Steps:**

1. In the current project directory: run `git status` scoped to `.claude/`, stage any modified files, commit with a descriptive English message, push.

2. In `~/.claude/` (tracked in the `claude-system` repo): run `git status`, stage any modified files, commit with a descriptive English message, push.

Skip a repo if it has no dirty files. Report what was committed and pushed, or confirm nothing to commit.
