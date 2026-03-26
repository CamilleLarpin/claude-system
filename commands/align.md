---
name: align
description: Strategic alignment review — step back from implementation, re-validate end vision, review milestone sequencing, surface misordering, premature complexity, and cross-project dependencies. Use when starting a new phase, after a milestone completes, or when feeling lost in the weeds.
---

# /align — Strategic Alignment Review

## How this works
This is a **conversation**, not a report. Each step ends with a question or prompt. Wait for the user's response before moving to the next step. Never run multiple steps in one message. The user builds the alignment with you — you don't produce it for them.

---

## Step 1 — Anchor to pain

Ask ONE question. Then stop.

> "Before I read the docs — what's the most painful or frustrating thing about [this problem space] right now? What made you start this project?"

Wait. This answer is the true north for everything that follows.

---

## Step 2 — Present current state

Read `.claude/DESIGN.md`, `.claude/TODOS.md`, `.claude/CONTEXT.md`.

Present concisely — no analysis yet:
- **End vision** — one sentence from DESIGN.md
- **Live / built / not started** — one line each
- **Milestone sequence** — flat list from TODOS.md

Then ask: *"Does this still feel like an accurate picture?"*

Wait for confirmation or corrections before continuing.

---

## Step 3 — Stress test the vision

Surface ONE tension at a time. Ask, wait, react, then surface the next.

Tensions to surface (in order of importance):
1. **Pain vs. design match** — does the DESIGN.md problem statement match what the user said in Step 1? If not, name the gap explicitly and ask if it should be updated.
2. **Measurability** — for each success criterion: is it actually measurable? ("feel personal" is not. "80% of drafts sent without edit" is.) Flag the ones that aren't and propose rewrites.
3. **Key assumption** — what does this vision *assume* will be true? Name the riskiest one. Ask: "Is that assumption realistic?"
4. **Failure mode** — "What would make this project a failure in 6 months, even if everything gets built?" This surfaces hidden criteria.

For each: present your finding briefly, ask a focused question, wait for the answer. Don't move on until the user has engaged with it.

---

## Step 4 — Diverge: generate options

Generate 2–3 meaningfully different ways to phase the work. For each:
- Name the **core bet** ("bet: if we close the existing loop first, we get signal before building more")
- What it **unlocks earliest**
- What it **defers** and why that's acceptable

Present all options. Then ask: *"Which of these feels closest to right, or is the answer somewhere between them?"*

Wait. Do not recommend yet.

---

## Step 5 — Converge: recommend a sequence

Based on the user's response to Step 4, recommend one sequence. Apply these filters explicitly:
1. **Real pain first** — does this milestone solve the pain from Step 1, or a hypothetical one?
2. **Minimum viable phase** — what's the smallest thing that validates the core assumption?
3. **Data gates** — milestones that generate data before milestones that consume it
4. **"Skip for 3 months" test** — if the answer is "not much breaks," it's not a priority

Present as phases:
```
Phase N — [What the user can do or see after this phase that they couldn't before]
  [milestone]
  [milestone]  ⚠️ Depends on: [X]
```

Phase names must describe **added value for the user** — not technical themes or internal milestones. A good name passes this test: "After this phase, I can [X]" where X is something concrete and meaningful to the user. Bad: "Data layer complete." Good: "Get to 1st draft monthly report."

When proposing a resequenced roadmap, also rename all phases in DESIGN.md and TODOS.md to match the new names — never leave stale phase names in the docs after alignment.

State which option from Step 4 you're recommending and why.

Then ask: *"Does this sequencing feel right? What would you change?"*

Iterate (back to Step 4 if needed) until the user says yes.

---

## Step 6 — Coherence check: DESIGN ↔ TODOS

Cross-reference silently, then surface only real gaps:
- **In DESIGN but not in TODOS** — scoping gap or intentional deferral? Ask.
- **In TODOS but not in DESIGN** — scope creep or undocumented decision? Flag.
- **Contradictions** — sequence in TODOS contradicts dependency logic in DESIGN?

Present findings. Ask: *"Should I fix these, or are some intentional?"*

---

## Step 7 — Cross-project dependencies

For any milestone that depends on another project, propose the flags explicitly:
- `⚠️ Depends on: [project] [specific task]` in TODOS.md
- `**Depends on**:` in BACKLOG.md for the dependent project
- `⚡ Unblocks: [project]` on the blocking task in the other project's TODOS.md

Ask: *"Should I add these flags now?"*

---

## Step 8 — Confirm and write

Only once the user has explicitly agreed on the sequence:

Update:
- `DESIGN.md` — milestone phases section + any success criteria rewrites
- `TODOS.md` — restructure to confirmed phases, add dependency flags
- Other projects — add `⚡ Unblocks` and `**Depends on**` flags as agreed

If DESIGN had coherence gaps: ask whether to add missing use cases to TODOS or mark them explicitly deferred.
