---
description: Flag current session as a rich learning session — adds an entry to the learning log
---

# /digest — Flag Session for Learning Review

Flag the current session as one where Camille learnt a great deal from Claude.

**Steps:**

1. **Detect context** — identify the current project from the working directory (last path component). If ambiguous, ask.

2. **Get today's date** — `YYYY-MM-DD` format.

3. **Write a one-line description** — summarise the main concepts or topics covered in this session (topics Camille asked to have explained, key mental models, analogies used). Be specific — this description is what Camille will see when scanning the learning log later.

4. **Append to learning log** — add one line to `~/projects/claude-one-digest/data/learning_log.md`:
   ```
   YYYY-MM-DD | <project> | <description>
   ```

5. **Confirm** — output: `→ LEARNING LOG: <project> — <description>`
