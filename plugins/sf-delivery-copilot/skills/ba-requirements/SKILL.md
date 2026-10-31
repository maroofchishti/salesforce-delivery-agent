---
name: ba-requirements
description: Turn Salesforce discovery notes, workshop transcripts or a client brief into a requirements pack — business requirements, INVEST user stories with Gherkin acceptance criteria, Salesforce impact, traceability, assumptions and open questions. Use for "write user stories", "BRD", "requirements from these notes", "groom the backlog".
---

# BA requirements pack

Before starting, read:
- `${CLAUDE_PLUGIN_ROOT}/reference/operating-principles.md`
- `${CLAUDE_PLUGIN_ROOT}/reference/salesforce-conventions.md`

## Inputs
Discovery notes, transcript, SOW extract, existing Confluence page or Jira epic.
If no input is given, ask for it. Do not write requirements from imagination.

## Steps
1. **Extract.** List every stated need, pain point, rule, volume, persona and
   system mentioned, each with a `[src: …]` tag. Keep the client's wording.
2. **Classify.** Business requirement (why), functional requirement (what),
   NFR, constraint, out of scope. Flag conflicts between sources explicitly.
3. **Gap check.** For each requirement ask: who does it, which object/record,
   what triggers it, what happens on error, who must NOT see it, what volume.
   Every unanswered item becomes an Open Question with the role to ask.
4. **Write stories** in the format from `salesforce-conventions.md`. Each story
   needs at least three Gherkin scenarios: happy, negative/validation, permission.
   Split anything failing INVEST.
5. **Org check (optional).** If the Salesforce MCP tools are available and the
   user agrees, run the `ba-org-discovery` skill to confirm objects/fields exist
   and mark each story New build vs Configure existing.
6. **Traceability matrix**: BR-ID → Story IDs → AC scenarios → UAT case IDs (TBD).
6a. **Lessons checks** (`reference/lessons-learned.md`):
   - L01 — header lists sources used with their rank/version; flag any story
     built only from a source that a higher-ranked one has superseded.
   - L03 — for each channel/packaged feature, note the standard objects it needs
     and flag conflicts with a custom data model.
   - L04 — produce or update the role × object × field visibility matrix
     (`requirements/visibility-matrix.md`): record pages, list views, reports,
     files, email templates; one permission-negative AC per restricted role.
   - L05 — for each stage/object handoff, list fields prefilled vs entered; flag
     any field a user enters twice.
   - L06 — use values from `requirements/status-glossary.md` (create it if
     missing); flag new or conflicting status names.
   - L12 — every email/alert/bell notification gets a row in
     `requirements/notification-matrix.md` (event × recipient role × channel ×
     template × frequency); no notification story without a row.
   - L13 — each new custom object gets the baseline Definition of Done checklist
     (layout, default tab, Chatter, history, Files, list views, help text).
   - L14 — each story lists alternate and exception flows (cancel, reverse,
     partial, re-assign) as Gherkin scenarios; complex rules (pricing,
     matching, balances, allocation) get a one-page logic design to review
     before build.
   - L19 — a story changing an existing object links its `ba-impact-analysis`
     output; flag stories that add a new automation type to an object/event
     that already has one.
7. **Review.** Run the `delivery-reviewer` agent on the pack. Fix every BLOCKER;
   list remaining MAJOR items for the user.

## Output
Write `requirements/<epic-slug>-requirements.md` in the working folder:
1. Summary (3–5 lines: scope, personas, clouds, #stories, top risks)
2. Business requirements table (ID, requirement, priority, source)
3. User stories (full format)
4. Traceability matrix
5. Out of scope
6. Lessons checked (IDs + any failed checks)
7. Assumptions · Open questions (owner, due, blocking Y/N — L07) · Confidence
Plus `requirements/visibility-matrix.md` (with the sharing model),
`requirements/notification-matrix.md` and `requirements/status-glossary.md`.

## Update mode (after a client meeting)
When given a meeting capture from `ba-meeting-capture` and an existing pack:
1. Add **New** items as new requirements/stories; carry the meeting citation.
2. For **Changed** / **Conflicts** items, do not overwrite silently: show the
   before → after for each affected story and ask the user to confirm.
3. Keep **Tentative** items in a "Tentative / to confirm" section, not in the
   committed backlog.
4. Append a change log row: date, meeting, IDs added/changed, approved by.

Offer `jira-sync` afterwards. Never create Jira issues from this skill directly.
