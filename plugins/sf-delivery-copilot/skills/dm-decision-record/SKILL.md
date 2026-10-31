---
name: dm-decision-record
description: Record a costly or hard-to-reverse delivery or design decision (Flow vs Apex, integration pattern, data model, scope trade-off, release approach) as a short decision record with context, options, rationale and consequences. Use for "log this decision", "ADR", "decision record", "why did we choose X".
---

# Decision record

Read `${CLAUDE_PLUGIN_ROOT}/reference/operating-principles.md`.

## Rules
- Record what the humans decided. If no decision has been made yet, write the
  record with Status: Proposed and list the options neutrally — do not decide
  for the team.
- Decider and date come from the user or the source; otherwise `TBD`.
- **Platform dependencies (L03):** for data-model or channel decisions, each
  option lists the standard objects, licences and native features it relies on
  or gives up (e.g. messaging channels that expect Case / Messaging Session).

## Template — `decisions/DR-<nnn>-<slug>.md`
```
# DR-<nnn>: <decision title>
Status: Proposed | Accepted | Superseded by DR-<x>
Date: <yyyy-mm-dd>   Decider(s): <names/roles>   Source: [src: …]
## Context        (problem, constraints, requirement IDs)
## Options        (2–4, each with pros / cons / Salesforce limits involved)
## Decision       (chosen option, one paragraph)
## Rationale
## Consequences   (what gets easier/harder, follow-up stories, risks → RAID)
## Revisit when   (trigger that would reopen this)
```
Number sequentially by checking existing files in `decisions/`. Keep it to one page.
