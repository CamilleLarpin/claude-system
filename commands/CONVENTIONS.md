# Command Conventions

Rules for writing commands in this folder.

- **Frontmatter**: always include `description` — one line, ≤ 80 chars (used by /help for discoverability)
- **No CLAUDE.md duplication**: if it's a global directive, don't repeat it
- **Imperative only**: steps are instructions, not explanations or rationale
- **Explicit branching**: `If X → do Y, else stop` — no ambiguity
- **Tight output spec**: when a command produces output, specify its format to constrain response tokens
- **Max ~25 lines of content**: if longer, the command is doing too much
- **Bash only when it adds information**: include bash snippets for unique flags, non-obvious sequences, or command-specific patterns — not for patterns Claude already knows from CLAUDE.md
- **Reference, don't describe**: point to files by path; don't summarize their content
