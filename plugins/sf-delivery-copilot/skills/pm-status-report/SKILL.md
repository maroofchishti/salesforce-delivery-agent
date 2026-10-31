---
name: pm-status-report
description: Weekly project status report for a Salesforce engagement built from Jira sprint data, the RAID log and the user's notes — RAG status with evidence, progress, milestones, risks, decisions needed. Use for "status report", "weekly update", "steering committee update", "client update".
---

# Status report

Read `${CLAUDE_PLUGIN_ROOT}/reference/operating-principles.md`.

## Gather (read-only)
1. Ask for or confirm: project, reporting period, audience (internal / client /
   steerco), Jira project key + sprint, path to RAID log.
2. From Jira (Atlassian tools): issues done / in progress / blocked in the
   period, scope added mid-sprint, overdue items. Record the JQL you used.
3. From the RAID log: open High risks/issues, decisions pending, and the
   open-questions health line (L07): blocking count, unowned, past due. Any
   past-due blocking question appears under "Decisions needed" with its owner.
4. From the user: milestone dates and budget figures — never estimate these.
5. **Quality KPIs** (internal audience, from the defect tracker; only what the
   data supports, else "not measurable yet" and why):
   | KPI | P1 baseline | Target |
   |---|---|---|
   | Defects found after production deploy | ~19% | < 5% |
   | Fixes failing first retest (L15) | ~25% | < 10% |
   | Permission/FLS share of QA defects (L04) | 37% | < 10% |
   | UAT items that are changes, not defects (L16) | 60% | < 25%, all via CR |
   | Defects with a coded root cause (L15) | < 30% | 100% |
   Also report open change requests and their approval state (L16).

## RAG rules (show the evidence for the rating)
- **Green**: milestones on track, no High open issue older than 5 working days.
- **Amber**: a milestone at risk OR a High issue without an owner/plan.
- **Red**: a committed milestone will be missed OR a blocker with no path.
If data is missing to judge, rate "Unknown" and say what is missing.

## Output (≤ 1 page)
```
# <Project> — Status <period>   Overall: <RAG> (prev: <RAG>)
Headline: <one sentence>
Progress: done / in progress / blocked counts + 3–5 highlights [src: JQL …]
Milestones: table (milestone, baseline, forecast, RAG)
Top risks & issues: max 5, owner + next action + due
Decisions needed: who, by when
Change requests: open / approved / deferred (internal and steerco only)
Quality KPIs: table (internal audience only)
Next period: 3–5 bullets
Assumptions · Open questions · Confidence
```
Save to `status/<yyyy-mm-dd>-status.md`. For client or steerco audiences run the
`delivery-reviewer` agent first. Sending or posting the report is a separate
step that needs the user's explicit approval.
