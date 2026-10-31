# Salesforce delivery conventions

Customize this file with your company / client standards. Skills read it.

## User story format
```
ID:        <PROJ>-<n> (assigned by Jira; use DRAFT-<n> before sync)
Title:     <Persona> can <capability>   (≤ 10 words, verb-first capability)
Story:     As a <persona>, I want <capability>, so that <business outcome>.
Cloud:     Sales | Service | Experience | Marketing | FSC | Platform | Agentforce
Type:      Config | Flow | Apex | LWC | Integration | Data | Security | Report
Priority:  MoSCoW (Must / Should / Could / Won't)
Source:    [src: ...]
Acceptance criteria (Gherkin):
  Scenario: <happy path>
    Given <context>
    When <action>
    Then <observable outcome>
  Scenario: <negative / validation path>
  Scenario: <permission path — user WITHOUT access>
Salesforce impact checklist: objects, fields, record types, page layouts /
  Lightning pages, profiles / permission sets, sharing, validation rules,
  automation (Flow vs Apex), reports, integrations, data migration.
NFRs: volume, performance, governor limits, audit / field history, accessibility.
Dependencies:
Open questions:
```

## INVEST check
Independent, Negotiable, Valuable, Estimable, Small (fits a sprint), Testable.
Split stories that touch more than one persona or more than one automation.

## Definition of Ready
- Story + Gherkin AC with at least happy, negative and permission scenarios
- Salesforce impact checklist filled
- Dependencies and data needs identified
- No open question marked BLOCKING (L07)
- Fields touched are in the role visibility matrix (L04)
- Prefilled vs entered fields stated for any stage handoff (L05)
- Status values come from the status glossary (L06)
- Traces to a client statement or written confirmation, not only an internal meeting (L09)
- Every notification it sends has a notification-matrix row (L12)
- Alternate/exception flows written as scenarios; complex logic has a reviewed one-page design (L14)
- Changes an existing object? Impact analysis linked (L19)

## Definition of Done
- Built in dev sandbox, peer reviewed (Apex and flows)
- Developer logged in as each affected persona and checked access before "Done" (L15)
- New objects meet the baseline: layout/Lightning page, default tab, Chatter
  decision, field history, Files, list views, help text, search layout, tab
  visibility (L13)
- Defects closed only by QA, with severity and coded root cause (L15)
- Apex: tests pass, org coverage ≥ 75% (target ≥ 85% for new classes)
- Deployed to QA/UAT sandbox via the agreed pipeline
- UAT script executed and signed off
- Release notes + rollback steps written
- Documentation updated in Confluence

## Environment path
Dev sandbox → QA → UAT (Full/Partial copy) → Production.
The agent operates only against the sandbox in `SF_AGENT_ORG`.

## Automation preference (for the BA to flag, architect decides)
Declarative first (Flow) → Apex when volume, complexity or transaction control
requires it. Flag but do not decide; record the decision with `dm-decision-record`.
