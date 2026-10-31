---
name: ba-impact-analysis
description: Before changing an existing Salesforce org, map everything a change touches — the automation stack on each object (flows, triggers, validation rules, workflow rules, process builders, approvals), dependent Apex/LWC, emails, integrations, Experience sites, other apps sharing the object, sensitive data — and produce a risk rating, regression scope and manual post-deploy steps. Use for "impact analysis", "what will this change break", "change to existing object", "regression scope", "is it safe to modify X".
---

# Impact analysis (existing org, read-only)

Read `${CLAUDE_PLUGIN_ROOT}/reference/operating-principles.md`, and the
project's `.delivery/CONTEXT.md` if it exists (apps, shared objects, sensitive
objects, integrations, known risks).

Mature orgs fail at the seams: a new field or rule on an object that already
has a workflow rule, a process builder, a flow and a trigger can double-send
emails or change the order things happen. This skill finds those seams before
build. Lesson L19 applies throughout.

## Inputs
The change (story, CR or meeting capture) and the objects/fields it touches.
Missing object list → derive it from the change and confirm with the user.

## Safety
- Sandbox in `SF_AGENT_ORG` only; metadata and `COUNT()` queries only. Never
  read HR, payroll, finance or candidate record contents — objects listed in
  `.delivery/sensitive-objects.txt` need the user's approval for anything but
  counts (the guard will ask).
- No deploys, no data changes, no anonymous Apex.

## Steps
1. **Automation stack per object** (Tooling API / metadata, read-only):
   Apex triggers on the object; record-triggered flows (before/after save,
   delete), scheduled and autolaunched flows that reference it; active
   validation rules; legacy workflow rules (field updates, email alerts);
   active process builders; approval processes; duplicate rules. If a query
   fails, say which, and fall back to retrieving that metadata into the
   project and scanning it locally — never guess.
2. **Dependents**: Apex classes, LWC/Aura, flows, reports and Experience site
   pages that reference the touched objects/fields (metadata dependency
   query, then a text search of retrieved source to confirm; dependency APIs
   can miss dynamic references).
3. **Seams to flag**:
   - Same object/event handled by more than one automation type → order of
     execution risk; list them in execution order.
   - A legacy workflow rule or process builder doing the same job as a flow
     (same email or field update) → duplicate-email / double-update risk;
     propose retire-or-merge.
   - Emails sent (alerts, templates, recipients) → check against the
     notification matrix (L12).
   - Integrations (e.g. accounting, email/identity provisioning, external
     APIs) and batch/scheduled jobs that read the fields.
   - Object shared by several apps → every app is in regression scope.
   - Experience/employee site exposure → guest/portal access and sharing (L04).
   - Inactive automations on the object that someone may reactivate.
4. **Risk rating**
   - **High**: sensitive object, integration or batch touched, object shared
     across apps, or 3+ automation types on the object/event.
   - **Medium**: 2 automation types, or emails change, or site-exposed.
   - **Low**: isolated config with no automation or dependents.
5. **Regression scope**: existing UAT/regression cases to rerun (by persona and
   app), plus new cases for each seam found.
6. **Deployment notes** (L17): component list in dependency order (objects →
   fields → Apex → flows → permission sets → layouts/actions); manual steps a
   metadata deploy does not carry — credential secrets, permission set
   assignments, external credential principal access, "run as" users,
   scheduled job activation, email deliverability, data.

## Output
`impact/<story-or-cr>-impact.md`:
1. Verdict line: risk High/Medium/Low + one-sentence reason
2. Automation stack table per object (type, name, event, active, what it does)
3. Seams flagged (each with evidence path or query)
4. Dependents · Emails affected · Apps & personas affected
5. Regression scope · Deployment notes · Post-deploy manual steps
6. Lessons checked · Assumptions · Open questions · Confidence

Offer: add High risks to the RAID log (`pm-raid-log`); feed regression cases
to `ba-uat-scripts`; record a retire-or-merge decision with `dm-decision-record`.
