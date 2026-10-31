---
name: pm-raid-log
description: Create or update a RAID log (Risks, Assumptions, Issues, Dependencies) from meeting notes, status calls or Jira — scored, owned and dated. Use for "RAID log", "risk register", "log this risk", "update issues list after the call".
---

# RAID log

Read `${CLAUDE_PLUGIN_ROOT}/reference/operating-principles.md`.

## File
Default `raid/raid-log.csv` (columns below). If the user keeps the log in a
Google Sheet, read it with the Google Sheets tools; writing to it needs a
preview of the exact rows and the user's "yes".

`ID,Type,Title,Description,Impact(1-5),Likelihood(1-5),Score,Severity,Owner,Raised,Due,Status,Mitigation/Next action,Source`

## Rules
- Type: R (risk – may happen), A (assumption – believed true, needs validation),
  I (issue – happening now), D (dependency – needed from others).
- Score = Impact × Likelihood (issues: Likelihood = 5). Severity: ≥15 High,
  8–14 Medium, ≤7 Low.
- Owner must be a named person from the source or `TBD — PM to assign`. Never
  assign people yourself.
- Before adding, check for duplicates and update the existing row instead.
- A risk that has materialized → close the R row, open an I row that references it.
- Salesforce-typical risks to prompt for when relevant: data migration quality,
  integration partner readiness, sandbox refresh timing, license/edition limits,
  governor limits at volume, UAT tester availability, release window conflicts.
- **Open questions (L07):** blocking open questions live in the log as type A
  (assumption pending) or I (issue) with owner, due date and `Blocking` in the
  title. Each run reports: open blocking count, how many lack an owner, how many
  are past due. Past-due blocking questions are escalated in the next status report.
- **Sandbox refreshes (L11):** log planned refresh dates as dependencies and flag
  any that overlap UAT or release windows.

## Output
Show a diff-style summary: added / updated / closed rows, then the top 5 by
score, then the open-questions health line (L07).
