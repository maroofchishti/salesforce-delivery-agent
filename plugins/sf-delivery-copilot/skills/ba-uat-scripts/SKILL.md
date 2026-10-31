---
name: ba-uat-scripts
description: Generate UAT test scripts from Salesforce user stories and Gherkin acceptance criteria — step-by-step cases per persona with test data needs, expected results, and a sign-off sheet. Use for "UAT script", "test cases", "UAT plan", "sign-off template".
---

# UAT scripts

Read `${CLAUDE_PLUGIN_ROOT}/reference/operating-principles.md` and
`${CLAUDE_PLUGIN_ROOT}/reference/salesforce-conventions.md`.

## Inputs
Stories with acceptance criteria (a requirements pack, Jira issues via the
Atlassian tools, or pasted text). If AC are missing for a story, list it under
"Not testable yet" instead of inventing criteria.

## Rules
- One test case per Gherkin scenario at minimum; IDs `UAT-<story>-<n>`.
- Every case: ID, story ref, persona + required permission set, preconditions,
  test data (describe — e.g. "Account with 2 open Cases" — never real customer
  data), numbered steps written for a business user (Lightning UI clicks, no API
  names in steps), expected result per step, Pass/Fail/Blocked, tester, date,
  defect ID.
- Always include: a permission-negative case (user without access cannot see /
  edit), a validation-rule case, and a bulk/volume note where the story
  mentions volume.
- **Visibility sweep (L04):** from `requirements/visibility-matrix.md`, add one
  case per restricted role checking hidden fields on the record page, list
  views, reports, related files and email templates — not just the page layout.
- **No re-entry (L05):** for each stage handoff, a case confirming carried-forward
  fields are prefilled and not re-typed.
- **Notifications (L12):** one case per notification-matrix row checking who
  receives it (and who must not), the channel and the wording.
- **Alternate flows (L14):** one case per alternate/exception scenario
  (cancel, reverse, partial, re-assign) — not only the happy path.
- **Defect logging (L15):** the defect columns are Severity (S1–S4), Type
  (defect / change / clarification / training), Root cause (requirement gap,
  design gap, FLS/sharing, automation logic, config baseline, data,
  deployment, environment) and Retest count; only QA sets Closed. Items typed
  "change" go to `dm-change-request` (L16).
- **Regression:** include the regression cases listed by `ba-impact-analysis`
  for every changed existing object.
- Log in as each persona (or use "Log in as") — never test visibility as admin.
- Order cases into an end-to-end business flow where possible.
- **Exit criteria (L17):** every case has a recorded result; no open S1/S2.

## Output
`uat/<release-or-epic>-uat.md` containing: Scope & entry/exit criteria, Test data
setup list, Test cases table, Not testable yet, Sign-off block (role, name TBD,
date, decision). Offer an .xlsx version only if the user asks for a spreadsheet.
Update the traceability matrix UAT column if a requirements pack exists.
