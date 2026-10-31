# Discovery workshop — Customer Support (fictional sample for testing)

Date: 2026-10-20 · Attendees: Head of Support (client), Support Team Lead (client), BA, Solution Architect

## Current state
- Support handles ~1,200 cases per month from email and the website contact form.
- Agents track cases in a shared mailbox and a spreadsheet; no SLA tracking.
- Customers often call to ask for status because they get no updates.

## Needs stated
1. Email and web form should create cases automatically in Salesforce.
2. Cases must be routed to the right queue: Billing, Technical, Returns.
3. Customers should get an automatic acknowledgement email with a case number.
4. High-priority cases not touched within a certain number of hours must escalate
   to the Team Lead. ("Certain number" — Head of Support to confirm.)
5. Team Lead wants a dashboard: open cases by queue, ageing, SLA breaches.
6. Agentforce Service Agent should answer order-status questions on the web
   later — "phase 2, maybe".
7. Returns cases need the order number; returns are handled by a partner
   warehouse system (integration owner unknown).

## Constraints
- Go-live wanted before the holiday peak.
- Only support agents and team leads should see Billing cases.

## SOW extract (for scope tests)
§3.1 In scope: Service Cloud case management for email and web channels,
queue-based routing, auto-response, escalation rules, reports and dashboards.
§3.4 Out of scope: telephony, chat/messaging channels, third-party integrations.
