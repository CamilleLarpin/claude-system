# Plan — Branch Guard (block direct commits to main)

> Status: pending · Delete once executed

## Goal
Prevent direct commits to `main` across all repos — by Claude and by Camille.

## Two-layer approach

**Layer 1 — Global git pre-commit hook** (hard stop, all actors)
- Script at `~/.git-template/hooks/pre-commit`
- Blocks any `git commit` when `HEAD = main`
- Applies to all new repos via `git config --global init.templateDir`
- Must be copied manually to existing repos

**Layer 2 — Claude Code PreToolUse hook** (early warning, Claude only)
- Script at `~/.claude/hooks/check-branch.sh`
- Registered in `settings.json` as PreToolUse on Bash
- Intercepts my `git commit` calls before they run
- Prints branch reminder + exits non-zero if on main

## Implementation steps

```
1. Create ~/.git-template/hooks/pre-commit
   #!/bin/sh
   branch=$(git symbolic-ref --short HEAD 2>/dev/null)
   if [ "$branch" = "main" ]; then
     echo "ERROR: direct commit to main blocked — create a feature branch first"
     exit 1
   fi

2. git config --global init.templateDir ~/.git-template
   chmod +x ~/.git-template/hooks/pre-commit

3. Copy hook to existing repos:
   - ~/.claude/
   - ~/.claude/projects-tracking/
   - ~/projects/chief-of-staff-ia/
   - ~/projects/ai-networking-system/
   - ~/projects/finances-ezerpin/
   - ~/projects/audio-intelligence-pipeline/
   - ~/projects/biography/
   - ~/projects/family_content_manager/
   - ~/projects/ghost/
   - ~/projects/hetzner-infra/
   - ~/projects/openclaw-setup/
   - ~/projects/gmail-inbox-cleanup/
   - ~/projects/pea-pme-pulse/

4. Create ~/.claude/hooks/check-branch.sh
   #!/bin/bash
   if echo "$CLAUDE_TOOL_INPUT" | grep -q "git commit"; then
     branch=$(git symbolic-ref --short HEAD 2>/dev/null)
     if [ "$branch" = "main" ]; then
       echo "BLOCKED: on branch 'main' — create a feature branch before committing"
       exit 1
     fi
   fi

5. Register in settings.json under hooks.PreToolUse:
   { "matcher": "Bash", "hooks": [{ "type": "command", "command": "bash ~/.claude/hooks/check-branch.sh" }] }
```

## Validation
- Try `git commit` on main in any repo → both layers should block
- Create a branch, commit → should succeed
- New repo via `git init` → hook should be present automatically
