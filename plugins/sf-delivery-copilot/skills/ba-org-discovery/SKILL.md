---
name: ba-org-discovery
description: Read-only as-is analysis of a Salesforce sandbox for a BA — objects, fields, picklists, record types, automations, permission sets, record volumes — to ground requirements and gap analysis. Use for "what exists in the org for X", "as-is analysis", "fit-gap", "does field X exist".
---

# Org discovery (read-only)

Read `${CLAUDE_PLUGIN_ROOT}/reference/operating-principles.md` first.

## Scope and safety
- Work only against the org alias configured in `SF_AGENT_ORG` (a sandbox).
  If the user names a production org, stop and say this skill is sandbox-only.
- Read operations only: describe metadata, SOQL `SELECT` with `COUNT()` or
  `LIMIT 20`, list metadata. Never run DML, anonymous Apex, deploy or delete.
- Prefer counts and field names over record contents. Do not copy customer
  record values (names, emails, phones, account numbers) into outputs.

## Steps
1. Confirm the target org with the user (alias + "sandbox" yes/no) before the
   first query.
2. For each object in scope collect: custom fields (API name, type, required),
   picklist values that matter, record types, validation rules (name + active),
   active Flows / Apex triggers on the object, record count.
3. For the personas in scope: relevant permission sets / profiles and object
   access (CRUD) — summarize, do not dump.
4. Fit-gap table: Requirement/Story → Exists (Y/N/Partial) → Evidence
   `[src: org metadata …]` → Gap / build needed.
5. **Automation debt (L19):** also list legacy workflow rules, process builders
   and inactive flows on in-scope objects, and objects shared by several apps
   (from `.delivery/CONTEXT.md` or tab sets). Any story that would change one
   of these objects needs `ba-impact-analysis` before build.
6. Objects in `.delivery/sensitive-objects.txt`: counts and field metadata only.

## Output
`discovery/<org-alias>-as-is.md` with: Summary, Object inventory, Automation
inventory, Access summary, Fit-gap table, Assumptions · Open questions ·
Confidence. If a query fails or a tool is unavailable, say so in the file —
never fill the gap with guesses.
