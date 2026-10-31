---
name: pm-sprint-plan
description: Draft a sprint plan from the Jira backlog — check Definition of Ready, fit work to the team's stated capacity, surface dependencies and risks, and propose a sprint goal. Use for "plan the next sprint", "sprint planning prep", "what fits in sprint N", "backlog readiness".
---

# Sprint plan (draft for the team to confirm)

Read `${CLAUDE_PLUGIN_ROOT}/reference/operating-principles.md` and
`${CLAUDE_PLUGIN_ROOT}/reference/salesforce-conventions.md`.

## Inputs to confirm with the user
Jira project/board, sprint dates, team capacity (people × days, leave,
holidays — ask, never assume), historical velocity if available, priorities
from the PO.

## Steps
1. Pull candidate backlog items in rank order (record the JQL).
2. **Readiness check** each against Definition of Ready; list Not Ready items
   with the exact missing piece (no AC, open blocking question, no estimate,
   unmet dependency). A story with any open blocking question is Not Ready, and
   its question goes on the list to chase with its owner before planning (L07).
3. **Fit**: take Ready items in rank order until capacity (use velocity if known,
   otherwise ask the team to estimate — do not invent story points). Keep 10–15%
   buffer for defects/support.
4. **Dependencies & risks**: integration partners, data loads, sandbox refreshes,
   environment availability, single-person knowledge.
5. Propose a one-sentence sprint goal tied to the top-ranked outcome.

## Output
`sprints/sprint-<n>-plan.md`: goal, capacity calc, committed list, stretch list,
not-ready list with fixes, risks/dependencies, Assumptions · Open questions ·
Confidence. Moving issues into the sprint in Jira is done only via `jira-sync`
after the team agrees.
