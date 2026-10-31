---
name: dm-change-request
description: Assess a new client ask against the signed SOW / baseline scope — in scope, clarification, or change request — and draft the change request with impact on effort, timeline, cost and risk. Use for "is this in scope", "scope creep", "change request", "CR impact".
---

# Scope check and change request

Read `${CLAUDE_PLUGIN_ROOT}/reference/operating-principles.md`.

## Inputs
The new ask (email, call notes, Jira comment) and the baseline: SOW scope
section, signed requirements pack, or approved backlog. Without a baseline,
stop and ask for it — scope cannot be judged from memory.

## Steps
1. Restate the ask in one sentence, with its source.
2. Search the baseline for matching or related scope; quote the clause IDs /
   section numbers (short references, not long extracts).
3. Classify:
   - **In scope** — cite the clause.
   - **Clarification** — baseline is ambiguous; propose the interpretation and
     who must agree.
   - **Change** — not covered, or exceeds what was agreed (more objects, new
     integration, new persona, more volume, new environment).
4. For a Change, draft impact: affected components (Salesforce impact checklist),
   effort range from the team's estimate (ask; never invent hours or cost),
   timeline/milestone impact, new risks, options (do now / defer to phase 2 /
   swap with lower-priority scope).
5. **Deviation, not just change (L02):** if the ask is already being built
   differently from the SOW (e.g. custom objects instead of the SOW's standard
   objects, a different channel architecture), classify it as **Deviation** and
   draft a deviation note for client sign-off, even if effort is unchanged.
6. **Platform dependency (L03):** if the ask involves a channel or packaged
   feature, state which standard objects/licences it requires and whether the
   current design supports them.
7. **Internal decisions (L09):** if the ask was shaped in an internal meeting,
   cite the original client statement; without one, mark it Proposal.
8. **Separate log (L16):** record every change in `change-requests/cr-log.csv`
   (ID, request, source, classification, effort range, timeline impact,
   status: Proposed / Approved / Deferred / Rejected, approver, date) — never
   in the defect tracker. Work starts only on Approved rows. For a batch of
   UAT items, classify each (defect / change / clarification / training) and
   raise one CR per change.
9. **Existing objects:** if the change touches an existing object, attach a
   `ba-impact-analysis` result so the effort reflects regression and
   automation risk.

## Output
`change-requests/CR-<n>-<slug>.md`: Classification line, Request, Baseline
reference, Impact table, Options with recommendation, Approval block (client
sponsor, delivery lead — names TBD), Assumptions · Open questions · Confidence.
Add a RAID entry suggestion. Commercial numbers are filled by a human.
