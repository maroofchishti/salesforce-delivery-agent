# <Project / org name> · project context

Copy this folder into the root of your project as `.delivery/` and fill it in.
Every skill reads it first. Keep real packs private: they name systems and people.

Sources: <where this came from and when, e.g. "metadata pull, 2026-10-27">

## Environments
| Stage | Org / alias | Notes |
|---|---|---|
| Dev | <alias> | Agent's only org (`SF_AGENT_ORG`) |
| QA | <alias> | Promotions by humans through the pipeline |
| UAT | <alias> | |
| Production | <org> | Out of bounds for the agent |

Pipeline: <DevOps Center / CI tool / change sets>, promotion order:
objects/fields → Apex → flows → permission sets → layouts/actions.

**Never carried by a deploy — redo by hand in each org:** credential secrets,
external credential principal access, connected app secrets and "run as"
users, permission set assignments, users, data.

## Apps and core objects
| App | Core objects | Notes |
|---|---|---|
| <app> | <objects> | <sites, batches, integrations> |

## Shared objects (regression across apps)
<objects used by more than one app, and which apps>

## Integrations and batch jobs
- <integration — direction — owner>
- <batch / scheduled job — what it touches — when it runs>

## Known risks
- <duplicate automations, legacy workflow rules, inactive flows, gaps>

## Who to ask
| Area | Owner |
|---|---|
| <area> | <name / role> |

## Delivery notes
- <audience, release windows, comms, data sensitivity>
