# Git Worktrees — Parallel Claude Instances Pattern

## What it is

`git worktree` attaches additional working directories to an existing repo, each on its own branch. No stashing, no branch-switching — multiple checkouts of the same repo coexist simultaneously.

## Why use it with Claude Code

Run parallel Claude Code sessions on separate branches without interference:
- One instance building a feature, one reviewing a PR
- One instance refactoring, one running tests on main
- Experiment on a branch while keeping a stable working copy open

## Commands

```bash
# Add a worktree on a new branch
git worktree add ../repo-feature feature/my-feature

# Add a worktree on an existing branch
git worktree add ../repo-review review-branch

# List all worktrees
git worktree list

# Remove a worktree (after you're done)
git worktree remove ../repo-feature
```

## Typical workflow

```bash
# From main repo
cd ~/projects/my-repo

# Open a worktree for a new feature
git worktree add ../my-repo-feature feature/auth-refactor

# Launch a second Claude Code session in that worktree
# (open a new terminal or Claude Code window pointing to ../my-repo-feature)
claude --cwd ../my-repo-feature
```

## Conventions

- Worktree directories: sibling of the main repo, named `<repo>-<branch-slug>` (e.g. `my-repo-feature`)
- Remove worktrees when done — they persist until explicitly removed
- Shared files (uncommitted `.env`, build artifacts) are NOT shared across worktrees — each worktree has its own working tree

## Constraints

- A branch can only be checked out in one worktree at a time
- `.git/` remains in the original repo; worktrees reference it via a `.git` file
- Hooks, remotes, and config are shared — changes in one worktree affect all
