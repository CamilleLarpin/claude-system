# Lessons — Git

> Load when: git workflows · rebasing · conflict resolution · PATs · GitHub API.
> Never delete entries. Add date and context.

---

## [git] · Guideline · Rebase before push
> unknown · source: unknown
- Merging without rebase creates noise merge commits when working across machines
- `git pull --rebase` replays your commits on top of remote, keeps history linear
- Set as default: `git config pull.rebase true`

## [git] · Rule · git diff hunks start mid-section — section header may not appear before changed lines
> 2026-03-12 · source: claude-one-digest
- `git diff` hunks start at the nearest context line before the change, not at the section header — if `### Project` is >3 lines above the change, it's outside the hunk and never seen by a line-by-line parser
- Parsing changed lines by scanning for a preceding section header in the diff body silently produces empty results
- Fix: build a line→section map from the full current file first, then use `@@` hunk offsets to resolve which section each change belongs to

## [github] · Rule · Fine-grained PATs require explicit repository + Contents permission
> 2026-03-12 · source: audio-intelligence-pipeline; updated 2026-03-19: ghost
- `github_pat_` tokens return 403/404 unless the token explicitly grants access to the specific repo(s) with the right Contents permission
- **For read** (git clone, GET file): Contents: Read-only — default "Public repositories" causes 404 on private repos
- **For write** (PUT file via API from n8n): Contents: Read and Write — classic `ghp_` PAT with `repo` scope may still return 403 "Restricts updates to workflow files" on private repos; fine-grained PAT is more reliable
- Setup: Settings → token → Edit → Repository access → select repo(s) → Permissions → Contents → Read and Write
- Create one dedicated PAT per project/integration to isolate permissions and avoid breaking shared credentials

## [git] · Rule · Pull `projects-tracking` before pushing — Ghost writes via GitHub API
> 2026-03-24 · source: ghost / ~/.claude setup
- `projects-tracking/` is a separate private git repo; Ghost writes to it via GitHub API (creates commits directly on `main`)
- Claude Code sessions that push to `projects-tracking` without first pulling will silently overwrite Ghost's commits — confirmed lost 2026-03-23
- Fix applied: `/start` now runs `cd ~/.claude/projects-tracking && git pull --rebase` before loading context
- Pattern: any workflow writing to a git repo via API creates a divergence risk — always pull before push in that repo

## [git] · Rule · Same file can conflict multiple times during a rebase — resolve per commit
> 2026-04-07 · source: pea-pme-pulse
- If multiple commits in a branch all touch the same file, `git rebase` will pause for each one — the same file can conflict 3+ times in a single rebase
- Each conflict reflects a different divergence point; the resolution is cumulative — each pass must preserve all prior resolutions plus the new change
- Pattern: resolve → `git add <file>` → `git rebase --continue` → repeat until "Successfully rebased"
- Common trap: resolving early conflicts correctly but dropping a block in a later round — always re-read the full file after each resolution before continuing
