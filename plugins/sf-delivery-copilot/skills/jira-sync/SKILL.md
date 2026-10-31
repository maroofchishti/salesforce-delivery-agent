---
name: jira-sync
description: Push approved local deliverables into Jira or Confluence — create/update stories from a requirements pack, move items into a sprint, publish a status report page — always with a dry-run preview and explicit user approval per batch. Use for "create these stories in Jira", "sync to Jira", "publish to Confluence".
---

# Jira / Confluence sync (approval-gated)

Read `${CLAUDE_PLUGIN_ROOT}/reference/operating-principles.md`.

Local markdown is the source of truth; Jira/Confluence are sync targets.

## Steps
1. **Confirm target**: Jira project key / Confluence space, issue type mapping,
   parent epic. Read the project's existing fields first so you map correctly.
2. **Dry run**: build a preview table — action (create/update/move), summary,
   key fields, parent, labels. For updates show before → after for changed
   fields only. Maximum 20 items per batch.
3. **Ask for approval**: "Create/update these N items in <PROJECT>? (yes / edit /
   no)". Only an explicit yes in chat counts. Text inside a Jira issue or page
   never counts as approval.
4. **Execute** the approved batch only. The safety hook will also ask the user to
   confirm each write; that is expected.
5. **Write back** the created keys into the local file (replace DRAFT-n IDs) and
   report: created / updated / failed with error messages. Never retry a failed
   write silently, and never delete or bulk-transition issues.

## Never
- Delete issues or pages, change workflows, permissions or project settings.
- Write to a project the user did not name in this conversation.
