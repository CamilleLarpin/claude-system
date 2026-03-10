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
- **Decision**: n8n on Hetzner server via Docker, scoped to HTTP/webhook/integration automation (connecting services, reacting to events, chaining API calls). Python-native pipeline orchestration is a separate category, not yet decided.
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

## [git] Default branch name
- **Decision**: `main` as default branch for all repositories
- **Rationale**: industry standard, avoids Git 3.0 warning, consistent across all projects
- **Date**: 2026-02
- **Status**: active

## [conventions] Single post-milestone checklist ordered by signal strength
- **Decision**: one checklist runs after each milestone (not split by session boundary); steps ordered by signal strength — promotions first (highest cognitive value), mechanical checks last
- **Rationale**: splitting into milestone + session checklists created a coordination problem — promotions require live context, which is cleared before end-of-session; collapsing removes deferred state; ordering by signal strength prevents attention decay on high-value steps; alternatives considered: mandatory vs conditional split (adds complexity with no payoff for solo developer), separate end-of-session checklist (broken by /clear)
- **Date**: 2026-03-04
- **Status**: active

## [conventions] Session ritual commands over CLAUDE.md prose
- **Decision**: user-triggered rituals (`/start`, `/end-of-session`, `/commit-push`) live in `~/.claude/commands/` as dedicated command files, not in CLAUDE.md
- **Rationale**: keeps CLAUDE.md lean (always-loaded context); command files are only loaded on invocation; user owns the trigger — Claude doesn't remind or propose; conventions for authoring commands documented in `~/.claude/commands/CONVENTIONS.md`
- **Date**: 2026-03-09
- **Status**: active

## [conventions] Load tier declarations in .claude/ file headers
- **Decision**: every `.claude/` file declares its load tier (hot/warm/cool/cold) in its header block; tier reflects current project phase and is updated when status changes
- **Rationale**: makes context load cost visible at the point of decision; prevents token bloat in frequently-loaded files; applies "no hidden assumptions" principle — tier is self-declared, not inferred; alternatives considered: global rule only (requires inference at read time), budgets by line count (no principled basis for numbers)
- **Date**: 2026-03-03
- **Status**: active
