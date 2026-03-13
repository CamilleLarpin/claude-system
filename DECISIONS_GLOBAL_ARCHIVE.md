# Global Decisions Archive — Camille Larpin

> ARCHIVE ONLY — decisions that are superseded or archived.
> NOT HERE: active decisions (→ DECISIONS_GLOBAL.md).
> Format: same as DECISIONS_GLOBAL.md — add archived date and superseded-by reference.

---

<!-- Archived decisions below — oldest at top, newest at bottom -->

## [stack] File-based storage as default
- **Decision**: JSON/MD files as default storage — no exceptions without explicit re-evaluation
- **Rationale**: zero infra overhead, git-versionable, natively readable by LLMs without connectors or query layers; unconditional default removes a recurring decision that has no current justification to revisit
- **Date**: 2024-01-DD
- **Archived**: 2026-03-13 — too stable to need active recall; re-add if ever revisited

## [conventions] Git commit language
- **Decision**: English commit messages only
- **Rationale**: universal readability, consistent with code language
- **Date**: 2024-01-DD
- **Archived**: 2026-03-13 — reflexive convention, no value in keeping hot

## [conventions] Claude Code handles commits
- **Decision**: Claude Code stages and commits — not manual git commands
- **Rationale**: keeps commit messages consistent and tied to task context
- **Date**: 2024-01-DD
- **Archived**: 2026-03-13 — reflexive convention, no value in keeping hot

## [git] Default branch name
- **Decision**: `main` as default branch for all repositories
- **Rationale**: industry standard, avoids Git 3.0 warning, consistent across all projects
- **Date**: 2026-02
- **Archived**: 2026-03-13 — reflexive convention, no value in keeping hot
