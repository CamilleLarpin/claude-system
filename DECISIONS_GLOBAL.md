# Global Decisions — Camille Larpin

> Load when: making an architectural or cross-project decision.
> NOT HERE: project-specific decisions (→ project DECISIONS.md), lessons (→ LESSONS_GLOBAL.md).
> Archive at 100 lines → DECISIONS_GLOBAL_ARCHIVE.md.

---

## Format
```
## [category] Decision title
- **Decision**: what was chosen
- **Rationale**: why — include alternatives considered
- **Date**: YYYY-MM-DD
- **Status**: active | superseded by [title] | archived
```

---

## [stack] File-based storage as default
- **Decision**: JSON/MD files as default storage — no exceptions without explicit re-evaluation
- **Rationale**: zero infra overhead, git-versionable, natively readable by LLMs without connectors or query layers; unconditional default removes a recurring decision that has no current justification to revisit
- **Date**: 2024-01-DD
- **Status**: active

## [stack] Claude Sonnet as default model
- **Decision**: Sonnet for standard tasks; Opus for architecture or complex multi-step reasoning
- **Rationale**: cost/quality balance; Opus reserved for decisions with long-lasting consequences
- **Date**: 2024-01-DD
- **Status**: active

## [stack] Self-hosted n8n over cloud
- **Decision**: n8n on Hetzner server via Docker
- **Rationale**: credential control, no per-execution cost at scale, full workflow portability
- **Date**: 2024-01-DD
- **Status**: active

## [conventions] Git commit language
- **Decision**: English commit messages only
- **Rationale**: universal readability, consistent with code language
- **Date**: 2024-01-DD
- **Status**: active

## [conventions] Claude Code handles commits
- **Decision**: Claude Code stages and commits — not manual git commands
- **Rationale**: keeps commit messages consistent and tied to task context
- **Date**: 2024-01-DD
- **Status**: active

## [conventions] ~/.claude/ versioned in private GitHub repo
- **Decision**: `~/.claude/` tracked in private repo `claude-system` on GitHub
- **Rationale**: backup against machine loss, full history of system evolution, cross-machine portability; same reasoning as file-based storage — git-versionable is a feature; private to avoid exposing server URLs and project structure
- **Date**: 2026-02-27
- **Status**: active
