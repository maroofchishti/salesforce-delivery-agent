---
name: dm-release-readiness
description: Salesforce release go/no-go assessment — checks scope, UAT sign-off, test coverage, deployment package, data steps, rollback plan, communications and hypercare against evidence, and produces a recommendation with blockers. Use for "release readiness", "go/no-go", "are we ready to deploy", "cutover checklist".
---

# Release readiness (go / no-go)

Read `${CLAUDE_PLUGIN_ROOT}/reference/operating-principles.md`.

The agent recommends; a human decides. The agent never deploys to production.

## Evidence to collect (read-only) — each item: Status ✅ / ⚠️ / ❌ / ❓ + evidence
1. **Scope**: release stories in Jira all Done; nothing in scope still open
   (record JQL). Late-added items flagged.
2. **UAT**: sign-off recorded (who, when, where); open defects by severity —
   any open Sev1/Sev2 = ❌.
3. **Quality**: Apex test run result in the UAT/staging sandbox, org coverage
   ≥ 75%, validation-only deployment (check-only) succeeded — ask for the
   deployment ID / CI link.
4. **Package**: component list matches the stories; destructive changes listed;
   profile/permission set changes reviewed. Deployed from source control, every
   component traceable to a commit by a named author — no shared deploy
   account (L18). Changed existing objects have an impact analysis attached.
4a. **UAT ↔ Prod parity (L17)**: comparison of permission sets, profiles,
   layouts, Lightning pages and active flow versions between UAT and the target
   shows no unexplained drift; every UAT script case has a recorded result.
4b. **Object baseline (L13)**: each new object's Definition of Done checklist
   complete or items waived.
5. **Data**: migration/data-fix scripts tested in a full-copy sandbox, record
   counts reconciled, backup taken before load.
6. **Config steps**: pre/post-deployment manual steps documented with owners —
   the post-deploy checklist (L17) covers users and roles, permission set
   assignments, credential secrets and external credential principal access
   (never carried by a metadata deploy), "run as" users, scheduled jobs
   activated, email deliverability, and a smoke test logged in as each persona.
   For orgs with batch jobs (payroll, accruals, invoicing, syncs), confirm the
   release window avoids their run times.
7. **Rollback**: written rollback plan per component type; decision criteria and
   time limit for rollback.
8. **People & comms**: release window agreed, users notified, training done,
   support/hypercare roster, business owner available.
9. **Integrations**: partner systems ready, credentials/named credentials set in
   target, monitoring in place.
10. **User access & adoption (L10)**: one MFA method standardized with a backup;
    MFA registration done on desktop before go-live; a super user can reset MFA;
    one-page login guide with the org's My Domain URL (mobile app server set to
    it); per-role app, tabs and home page trimmed; in-app guidance planned.
11. **Visibility (L04)**: UAT evidence that each restricted role cannot see the
    hidden fields in pages, list views, reports and files.
12. **Environments (L11)**: no sandbox refresh scheduled during the release or
    hypercare window; target org confirmed.

Missing evidence = ❓, never ✅.

## Recommendation
- **GO**: all ✅.
- **GO with conditions**: only ⚠️ items, each with an owner and deadline before the window.
- **NO-GO**: any ❌, or ❓ on items 2, 3, 4a, 6, 7, 10 or 11.

## Output
`releases/<release>-readiness.md`: recommendation in the first line, checklist
table, blockers, conditions, cutover runbook outline, Assumptions · Open
questions · Confidence. Always run the `delivery-reviewer` agent before
presenting.
