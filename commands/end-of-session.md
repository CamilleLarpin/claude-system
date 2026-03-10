# End of Session Checklist

Run the post-milestone checks. Work through each step in order, performing the action (don't just list it).

**1. Update project `.claude/` files**
Review what changed this session. Update `DECISIONS.md`, `LESSONS.md`, `DESIGN.md`, `TODOS.md` in the current project's `.claude/` directory to reflect the work done.

**2. Promotion check — Lessons**
Did any lesson apply beyond this project? If yes: add it to the correct `~/.claude/lessons/LESSONS_*.md` file and output: `PROMOTE: LESSONS_GLOBAL.md — [reason]`

**3. Promotion check — Decisions**
Did any decision apply cross-project? If yes: add it to `~/.claude/DECISIONS_GLOBAL.md` and output: `PROMOTE: DECISIONS_GLOBAL.md — [reason]`

**4. Complexity check**
Did this milestone meaningfully increase complexity? If yes: output `→ REFACTOR: [component] — [reason]`

**5. File threshold check**
Did any `.claude/` file cross its threshold? (LESSONS: 150 lines — DECISIONS: 100 lines) If yes: output `SPLIT` or `ARCHIVE` with file and reason.

**6. Global context update**
Did philosophy, stack, or architecture change? If yes: update `~/.claude/CONTEXT_GLOBAL.md`.

**7. Status and load tier update**
Did project status or load tier change for any file? If yes: update `~/.claude/PROJECT_TRACKER.md` and the relevant file headers.

**8. Done**
Output: "Session closed. Run `/clear` to reset context."
