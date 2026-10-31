---
name: dm-lessons
description: Check a Salesforce project against the lessons-learned register so past mistakes aren't repeated (at kickoff, design sign-off, before UAT and before go-live), and capture new lessons after retros, escalations or UAT rounds. Use for "lessons learned check", "are we repeating mistakes", "phase gate review", "add this to lessons learned", "retro".
---

# Lessons learned — check and capture

Read `${CLAUDE_PLUGIN_ROOT}/reference/operating-principles.md` and
`${CLAUDE_PLUGIN_ROOT}/reference/lessons-learned.md`.

## Mode A — Check (phase gate)
1. Ask which gate: **Kickoff**, **Design sign-off**, **Pre-UAT**, **Pre-go-live**
   (or "all"). Gate → lessons to check:
   - Kickoff: L01, L02, L03, L07, L08, L11, L16, L18, L19
   - Design sign-off: L01–L06, L09, L12, L14, L19
   - Pre-UAT: L04, L05, L06, L07, L11, L12, L13, L14, L15
   - Pre-go-live: L04, L07, L10, L11, L13, L15, L16, L17, L18
   - Plus any lesson added later whose "Enforced in" includes `dm-lessons`.
2. For each lesson, answer its **Check** question using evidence from the project
   folder (requirements/, meetings/, raid/, decisions/, change-requests/,
   releases/), Jira/Confluence (read-only) or the user. Record the evidence path.
3. Rate each: ✅ handled (evidence) · ⚠️ partly (what's missing) · ❌ repeating
   the mistake · ❓ no evidence. No evidence is ❓, never ✅.
4. For every ⚠️ / ❌, propose one concrete action with an owner role, and offer to
   add it to the RAID log via `pm-raid-log`.

**Output** `lessons/<yyyy-mm-dd>-<gate>-check.md`: one-line verdict (e.g.
"3 lessons at risk"), table (lesson, rating, evidence, action), Assumptions ·
Open questions · Confidence.

## Mode B — Capture (after a retro, escalation or UAT round)
1. Gather what happened from the user, retro notes or a meeting capture.
2. Check for an existing lesson on the same theme; if found, extend its "What
   happened" and sharpen its Rule instead of adding a duplicate.
3. Draft the new lesson in the register format (`ID · Title · Status · Source ·
   What happened · Rule · Check · Enforced in`), Status **Draft**, next free ID.
4. **Anonymize**: no client, company, people or product-instance names, no
   record data. Refer to the project as `P<n>` with a one-line neutral description.
5. Rules must be testable: the Check must be a question someone can answer yes/no
   with evidence.
6. Show the draft and ask for approval before editing `lessons-learned.md`. Only
   the user can change a lesson to **Confirmed**.
7. If the lesson should be enforced by a specific skill, propose the one-line
   addition to that skill's SKILL.md and apply it only after approval.
