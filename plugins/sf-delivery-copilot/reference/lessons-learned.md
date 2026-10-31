# Lessons-learned register

Hard-won rules from past engagements. Skills check work against this register;
`dm-lessons` runs the full check at kickoff and phase gates, and adds new lessons
after retros.

Kept anonymized on purpose: no client, company or people names, so this file is
safe in a shared repo. Source "P1" = a 2026 Sales Cloud custom-object build for a
vehicle export brokerage (~25 users, 12-stage lifecycle, monday.com migration,
Experience Cloud portal); its quality retrospective analysed ~560 tracker items
(~417 internal QA, 144 client UAT). Source "P2" = an internal multi-app org
(recruitment, HR and employee site, delivery, invoicing, expenses, sales;
64 core objects, 103 active automations, 29 legacy workflow rules).

**P1 headline numbers** (directional, ±5%): 60% of client UAT feedback was new,
changed or missed requirements / access / layout asks and only 9% genuine
defects; 37% of typed internal QA defects were permission/FLS misses; ~1 in 4
fixes failed first retest; 79 issues (~19% of internal logs) were found after
production deployment.

Status: **Confirmed** = validated by the delivery lead; **Draft** = derived from
project records, awaiting confirmation. Treat Draft lessons as checks, not facts.

Format — every lesson keeps these fields (`evals/test_lessons.py` checks them):
`ID · Title · Status · Source · What happened · Rule · Check · Enforced in`

---

### L01 · Build from the authoritative source, not the earliest one
- **Status:** Draft · **Source:** P1
- **What happened:** Process maps and user stories for the later stages were written
  from a legacy-tool walkthrough plus the BRD before the formal technical design
  docs existed. When the design docs arrived, every one of those artifacts had to
  be reconciled before reuse.
- **Rule:** Declare a source-of-truth hierarchy at kickoff (e.g. signed design doc >
  client decision in meeting > BRD > SOW > legacy-tool walkthrough). Every
  artifact records which sources and versions it was built from. When a
  higher-ranked source lands, list every artifact built from lower ones as
  "needs reconciliation".
- **Check:** Does each requirement cite a source, and is any of it built only from a
  source that a higher-ranked one has since superseded?
- **Enforced in:** ba-requirements, ba-meeting-capture, delivery-reviewer, dm-lessons

### L02 · Reconcile the SOW against the real design early
- **Status:** Draft · **Source:** P1
- **What happened:** The SOW assumed standard objects (Opportunity/Case/Lead); the
  agreed build used a custom object chain. Six material SOW conflicts surfaced
  mid-project and each needed deviation documentation.
- **Rule:** Within the first two weeks, map SOW modules → designed solution and
  record every divergence as a deviation note with client sign-off. Re-run at
  each design milestone.
- **Check:** Is there a signed deviation note for every place the build differs
  from the SOW (objects, channels, licences, phases)?
- **Enforced in:** dm-change-request, dm-lessons

### L03 · Check platform-native dependencies before choosing a custom data model
- **Status:** Draft · **Source:** P1
- **What happened:** WhatsApp intake was designed onto a custom object, but the
  native Salesforce messaging architecture is built around standard objects
  (Case / Messaging Session). The gap stayed unresolved late into the project.
- **Rule:** For every channel or packaged feature in scope (Digital Engagement,
  Omni-Channel, Agentforce, Experience Cloud licences, CPQ…), confirm which
  standard objects it requires before committing to custom objects. Record the
  decision with `dm-decision-record`.
- **Check:** Does any in-scope feature depend on a standard object the design
  doesn't use?
- **Enforced in:** ba-requirements, dm-decision-record, dm-lessons

### L04 · Define the role × field visibility matrix before build
- **Status:** Draft · **Source:** P1
- **What happened:** The client's top requirement was a server-side wall hiding
  cost and margin from Sales. Even so, 37% of typed QA defects and 50+ items
  overall were visibility leaks: purchasers seeing sales price, margin or
  customer info; sales seeing dealer balances or transport cost; list views
  exposing fields; documents visible beyond the uploader's team. The sharing
  model was never confirmed: QA logged "one purchaser can see another's
  requests" as a defect and it was fixed — then the client asked for exactly
  that in UAT, so the work was done twice.
- **Rule:** Before build, produce a role × object × field matrix (Read/Edit/Hidden)
  plus the record sharing model (who sees whose records), client-signed,
  covering record pages, list views, reports, related lists, files and email
  templates. Inventory every persona and region on day 1. Every story touching data has a permission-negative AC scenario
  per restricted role. Enforce at field-level security, not only page layouts.
- **Check:** Is there a signed visibility matrix, and does each story have a
  "user without access cannot see X" scenario for every restricted role?
- **Enforced in:** ba-requirements, ba-uat-scripts, delivery-reviewer

### L05 · Data must flow forward — no re-entry between stages
- **Status:** Draft · **Source:** P1
- **What happened:** Users had to re-key vehicle details on a later-stage record that
  already existed on the earlier one; it was caught only in review.
- **Rule:** For every object handoff in the process, list which fields carry
  forward (prefill / formula / lookup) and which are newly captured.
- **Check:** For each stage transition, does the story state what is prefilled vs
  entered? Any field entered twice by a user?
- **Enforced in:** ba-requirements, ba-uat-scripts

### L06 · One status glossary across all stages
- **Status:** Draft · **Source:** P1
- **What happened:** A record-creation status name conflicted between stage designs
  and had to be logged as an alignment issue.
- **Rule:** Maintain a single glossary of status / stage / picklist values with
  meaning and owning stage; stories reference glossary values, never new names.
- **Check:** Does any story introduce a status value missing from, or conflicting
  with, the glossary?
- **Enforced in:** ba-requirements, delivery-reviewer

### L07 · Keep the open-questions register small and owned
- **Status:** Draft · **Source:** P1
- **What happened:** The open-questions register grew to ~70 items with 8
  high-priority blockers.
- **Rule:** Every open question gets an owner, a due date and a blocking flag;
  blocking questions are reviewed in every client sync and escalated after one
  missed due date. A story with a blocking question is not Ready.
- **Check:** How many blocking questions are open, how many lack an owner or are
  past due?
- **Enforced in:** pm-raid-log, pm-status-report, pm-sprint-plan, dm-lessons

### L08 · Record and transcribe every requirements and UAT session
- **Status:** Draft · **Source:** P1
- **What happened:** Shorthand review notes contained terms no one could decode
  afterwards, and one uploaded recording was only a few seconds long. The
  meeting transcript was what resolved the ambiguities.
- **Rule:** Turn on Meet transcripts for every requirements, review and UAT
  session; process them with `ba-meeting-capture` the same day. Never resolve an
  ambiguous note by guessing — mark it `[verify]` and ask.
- **Check:** Does every requirement from a session trace to a transcript line, and
  is every undecodable note an open question instead of a guess?
- **Enforced in:** ba-meeting-capture, delivery-reviewer

### L09 · Trace internally-written specs back to the client's words
- **Status:** Draft · **Source:** P1
- **What happened:** Portal requirements were stated by the client in one session
  and turned into a detailed spec in later internal meetings, where several
  scope decisions were made (deferrals, licensing approach). Portal additions and
  timeline feasibility then stayed open.
- **Rule:** Requirements decided in internal meetings are Proposals until the
  client confirms them in writing; additions beyond the baseline go through
  `dm-change-request` with timeline impact before the team commits.
- **Check:** Does every requirement trace to a client statement or written client
  confirmation? Are scope additions backed by an approved CR?
- **Enforced in:** ba-meeting-capture, dm-change-request, delivery-reviewer

### L10 · Plan go-live for the users, not just the metadata
- **Status:** Draft · **Source:** P1
- **What happened:** Users new to Salesforce were overwhelmed after go-live: MFA and
  passkey login failures (including a phone app pointed at the wrong org), and
  too many tabs for what each role needs.
- **Rule:** Release readiness includes: MFA method standardized (Authenticator)
  with a backup, desktop-first MFA registration session, a super user who can
  reset MFA, a one-page login guide naming the org's My Domain, per-role app /
  tabs / home page trimmed, and in-app guidance for the first weeks.
- **Check:** Is every item above evidenced before go-live?
- **Enforced in:** dm-release-readiness

### L11 · Protect environments during sandbox refreshes
- **Status:** Draft · **Source:** P1
- **What happened:** Sandbox refresh decisions (auto-activate, post-copy class,
  access group) came up ad hoc; auto-activation replaces the old copy and logs
  users out, and emails are suffixed `.invalid`.
- **Rule:** Refreshes follow a checklist: work committed/deployed first, team
  notified, purpose stated (dev/QA/UAT), access group set, post-copy steps
  defined, refresh dates in the RAID log against UAT and release dates.
- **Check:** Are sandbox refresh dates on the plan, and do any collide with UAT?
- **Enforced in:** pm-raid-log, dm-release-readiness

---

### L12 · Agree a notification matrix before building any email
- **Status:** Draft · **Source:** P1
- **What happened:** 45+ items were notifications to the wrong people, on the
  wrong trigger, or with the wrong wording (e.g. the client wanted only the
  assigned accountant emailed).
- **Rule:** Before build, a client-signed matrix: event × recipient (role, not
  person) × channel (email / bell / Chatter) × template text × frequency. No
  alert or email flow is built without a row.
- **Check:** Does every email/notification in scope have a signed matrix row,
  and does the UAT pack test each row's recipients?
- **Enforced in:** ba-requirements, ba-uat-scripts, ba-impact-analysis, delivery-reviewer

### L13 · Every new object meets a baseline Definition of Done
- **Status:** Draft · **Source:** P1
- **What happened:** 25+ items were missing object basics found late: Chatter
  off on seven objects, field history, Files related list, list views, default
  Details tab, help text.
- **Rule:** Each new custom object ships with: page layout / Lightning page,
  default tab chosen, Chatter (feed tracking) decision, field history on key
  fields, Files related list, role list views, help text, search layout, and
  tab visibility per profile — checked before "Done".
- **Check:** For each new object, is every baseline item done or explicitly
  waived?
- **Enforced in:** ba-requirements, dm-release-readiness

### L14 · Design alternate flows and complex logic before coding
- **Status:** Draft · **Source:** P1
- **What happened:** Pairing logic was rebuilt three times and finally moved to
  another object; the alternate "reserved" flow, cancellations and "customer
  arranges shipping" broke VIN, pricing, approvals and invoice transfers
  repeatedly (~30 items). Logic was coded first and redesigned after "Done".
- **Rule:** Every story lists its alternate and exception flows (cancel,
  reverse, re-pair, partial, customer-does-it-themselves). Pricing, matching,
  balances and similar logic get a one-page design (states, rules, worked
  examples) reviewed before any Apex or flow is written; walk the client
  through a clickable playback of the stage before build.
- **Check:** Does each story have alternate-flow scenarios, and does each
  complex rule have a reviewed one-page design?
- **Enforced in:** ba-requirements, ba-uat-scripts, delivery-reviewer

### L15 · "Done" means verified as each persona, closed only by QA
- **Status:** Draft · **Source:** P1
- **What happened:** ~1 in 4 fixes failed their first retest; one item failed
  three times. Dev status read "Done" beside QA "FAIL"; ~12 items closed as
  "working as designed" because tester and developer read the spec
  differently; root causes logged as symptoms ("access issue").
- **Rule:** Developers log in as each affected persona before marking Done;
  only QA closes a defect; every defect has severity and a root cause from a
  fixed list (requirement gap, design gap, FLS/sharing, automation logic,
  config baseline, data, deployment, environment); ambiguous AC goes back to
  the BA, not to "working as designed".
- **Check:** What share of fixes failed first retest, and what share of
  closed defects have a coded root cause and severity?
- **Enforced in:** ba-uat-scripts, pm-status-report, dm-lessons

### L16 · Keep change requests out of the defect log
- **Status:** Draft · **Source:** P1
- **What happened:** 86 of 144 client UAT items were new or changed
  requirements, logged in the same sheet as defects with no impact estimate
  or approval, so scope grew silently while the plan stayed the same.
- **Rule:** Every UAT or meeting item is classified on intake: defect,
  change, clarification, training. Changes go to a separate CR log with
  effort/timeline impact and client approval before work starts.
- **Check:** Is every open item classified, and does every change have an
  approved CR or a recorded "defer"?
- **Enforced in:** dm-change-request, ba-meeting-capture, pm-status-report

### L17 · Prove UAT ↔ Production parity and run a post-deploy checklist
- **Status:** Draft · **Source:** P1
- **What happened:** 79 issues were found after production deployment, several
  already fixed once in UAT: FLS "not the same as UAT", a layout to be "made
  consistent with UAT", a user role not created, a reminder scheduler never
  activated. Only part of the client UAT script had a recorded result.
- **Rule:** Deploy from source control so what passed UAT is what goes to
  production; run a UAT↔Prod comparison of permission sets, profiles, layouts
  and flows' active versions; a post-deploy checklist covers users and roles,
  permission set assignments, scheduled jobs, credential secrets, email
  deliverability and smoke tests per persona. UAT exit requires every scripted
  case to have a result.
- **Check:** Is there a parity comparison, a completed post-deploy checklist,
  and a result for every UAT case?
- **Enforced in:** dm-release-readiness, ba-impact-analysis

### L18 · No shared deploy accounts — every change has a named author
- **Status:** Draft · **Source:** P2
- **What happened:** A shared deployment account owns ~290 components, most of
  the last four years' work, so nobody can tell from the org who built what
  or why; questions about behaviour have no owner.
- **Rule:** Deploy through source control (pipeline or CLI from a repo) with
  commits by named people; shared accounts only for integrations, never for
  deployments. Record the owner of each app/feature in the project context.
- **Check:** Can every component in this release be traced to a commit and a
  named author?
- **Enforced in:** dm-release-readiness, dm-lessons

### L19 · In a mature org, map the automation stack before changing an object
- **Status:** Draft · **Source:** P2
- **What happened:** Objects carry layered automation — legacy workflow rules,
  process builders, record-triggered flows and Apex triggers on the same
  events. At least two workflow rules duplicate newer flows (same emails sent
  twice), dozens of process builders and flows sit inactive, and several core
  objects are shared by three apps.
- **Rule:** Any change to an existing object starts with `ba-impact-analysis`:
  full automation stack in execution order, duplicates, emails, integrations,
  batch jobs, apps sharing the object, regression scope. Prefer consolidating
  into one flow or trigger per object/event over adding another layer.
- **Check:** Does each story changing an existing object link an impact
  analysis, and does it add automation to an object/event that already has
  another type?
- **Enforced in:** ba-impact-analysis, ba-requirements, ba-org-discovery

---

## Adding a lesson
Use `dm-lessons` → capture mode after any retro, escalation or UAT round.
Next ID: L20.
