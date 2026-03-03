# Global Context — Camille Larpin

> Load when: creating a new project or making an architectural or cross-project decision.
> NOT HERE: cross-project decisions with rationale (→ DECISIONS_GLOBAL.md), lessons (→ LESSONS_GLOBAL.md).

---

## Philosophy
- Prioritize comprehension over velocity.
- Know why before how: understand the pain before designing the solution.
- Add value first: no building without validated need.
- Agility over lock-in: continuously question the stack, stay on top of tools and trends.
- Low maintenance: every choice must minimize future maintenance burden — solo developer constraint.
- No hidden assumptions: make the implicit explicit. If applying a rule requires inference, the rule is incomplete.

## Technical Stack
- **Automation**: self-hosted n8n — https://n8n.helmcome.com
- **AI**: Claude (Sonnet default, Opus for architecture/complex reasoning), OpenAI API where needed
- **Data**: BigQuery, dbt, GCP
- **Storage**: file-based (JSON/MD)
- **Infra**: Hetzner server, Docker containers (n8n, Nextcloud, MariaDB)
- **Version control**: Git

## Architecture Principles
- **Modularity**: small, composable units over monoliths. Each component owns one responsibility.
- **DRY**: reusable logic in sub-workflows/modules; orchestrator coordinates, never duplicates.
- **Narrow scope**: agents and tools perform better with well-defined, bounded tasks.
- **Design for failure**: define rollback, error and warning handling before building.
- **Observability**: cost ceiling defined, effectiveness measurable, trigger defined for when to question the system.
- **Reliability over autonomy**: prefer consistent, predictable behavior over powerful-but-fragile.
- **Two-zone stack**: core is stable — change only when real pain justifies it; experiments are time-boxed and end in a binary verdict: promote to core or drop. No tools in limbo. Drivers: real pain solved, maintenance surface reduced.

## Project System
- Every project lives in `~/projects/<slug>/`
- Every project has `.claude/`: CONTEXT.md, DECISIONS.md, LESSONS.md, DESIGN.md, TODOS.md
- Every project CLAUDE.md imports `@~/.claude/CLAUDE.md`
- Project registry: `~/.claude/PROJECT_TRACKER.md`
- Project decisions: archive when superseded → DECISIONS_ARCHIVE.md. Never delete LESSONS entries.
