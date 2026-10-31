#!/usr/bin/env python3
"""PreToolUse safety guard for sf-delivery-copilot.

Reads the tool call JSON from stdin and decides:
  BLOCK -> exit 2, reason on stderr (Claude sees it and must not proceed)
  ASK   -> exit 0 with permissionDecision "ask" (user must confirm in the UI)
  ALLOW -> exit 0 with no output (normal permission rules still apply)

Every BLOCK/ASK is appended to <project>/.delivery-agent/audit.log.
Standard library only.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

PROD_HINT = re.compile(r"(^|[^a-z])(prod|production|live)([^a-z]|$)", re.I)

SECRET_PATH = re.compile(
    r"(^|/)(\.env(\..*)?|.*\.key|.*\.pem|credentials(\.json)?|\.netrc)$"
    r"|(^|/)\.sfdx(/|$)|(^|/)\.sf(/|$)|(^|/)\.ssh(/|$)",
    re.I,
)

BASH_BLOCK = [
    (r"\brm\s+-[a-z]*r[a-z]*f|\brm\s+-[a-z]*f[a-z]*r", "recursive force delete"),
    (r"git\s+push\s+.*(--force|-f\b)", "force push"),
    (r"git\s+reset\s+--hard", "hard reset"),
    (r"(curl|wget)[^|]*\|\s*(ba)?sh", "piping a download into a shell"),
    (r"\bsf\s+org\s+(display|open)\b.*--verbose|\bsfdx\s+force:org:display\b.*--verbose|auth\s+url",
     "reading Salesforce auth credentials"),
    (r"\bsf\s+org\s+delete\b|\bsfdx\s+force:org:delete\b", "deleting an org"),
    (r"\bsf\s+data\s+delete\b|\bsfdx\s+force:data:(record|bulk):delete\b", "deleting Salesforce records"),
    (r"destructiveChanges", "destructive metadata deployment"),
]

BASH_DEPLOY = re.compile(
    r"\bsf\s+project\s+deploy\b|\bsfdx\s+force:(source|mdapi):deploy\b|\bsf\s+deploy\b", re.I)
BASH_DRY_RUN = re.compile(r"--dry-run|--checkonly|--check-only", re.I)
BASH_ORG_WRITE = re.compile(
    r"\bsf\s+data\s+(create|update|upsert|import|bulk)\b|\bsf\s+apex\s+run\b(?!\s+test)"
    r"|\bsfdx\s+force:(data|apex:execute)", re.I)
BASH_TARGET = re.compile(r"(?:^|\s)(?:--target-org|-o|-u|--targetusername)[=\s]+(\S+)", re.I)

READ_VERBS = re.compile(
    r"(get|search|list|fetch|lookup|read|query|describe|retrieve|find|resolve|"
    r"userinfo|accessible|download|summar|export_preview)", re.I)
DELETE_VERBS = re.compile(r"(delete|trash|remove|purge|destroy|archive)", re.I)
WRITE_VERBS = re.compile(
    r"(create|update|edit|add|post|transition|assign|deploy|upsert|insert|move|"
    r"share|send|publish|append|copy|clear|run_apex|execute|comment|set_|change)", re.I)


def audit(decision, tool, reason):
    root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    try:
        d = os.path.join(root, ".delivery-agent")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "audit.log"), "a", encoding="utf-8") as f:
            ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
            f.write(f"{ts}\t{decision}\t{tool}\t{reason}\n")
    except OSError:
        pass


def block(tool, reason):
    audit("BLOCK", tool, reason)
    print(f"Blocked by sf-delivery-copilot guard: {reason}. "
          "Do not retry another way; explain to the user what was blocked and "
          "hand the step to a human if it is genuinely needed.", file=sys.stderr)
    sys.exit(2)


def ask(tool, reason):
    audit("ASK", tool, reason)
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": f"sf-delivery-copilot: {reason}. Confirm only if you approved this exact change.",
    }}))
    sys.exit(0)


def agent_org():
    return os.environ.get("SF_AGENT_ORG", "").strip()


SOQL_FROM = re.compile(r"\bfrom\s+([a-z0-9_]+)", re.I)
COUNT_ONLY = re.compile(r"^\s*select\s+count\(\s*\)\s+from\b", re.I)
BASH_QUERY = re.compile(r"\bsf\s+data\s+(query|export)\b|\bsfdx\s+force:data:(soql:query|tree:export)", re.I)


def sensitive_objects():
    """Per-project list of objects holding HR, payroll, finance or personal data."""
    root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    path = os.path.join(root, ".delivery", "sensitive-objects.txt")
    try:
        with open(path, encoding="utf-8") as f:
            return {l.split("#")[0].strip().lower() for l in f if l.split("#")[0].strip()}
    except OSError:
        return set()


def check_sensitive_query(query, tool):
    if not query:
        return
    sens = sensitive_objects()
    hits = sorted({o for o in SOQL_FROM.findall(query) if o.lower() in sens})
    if hits and not COUNT_ONLY.search(query):
        ask(tool, f"reading records from sensitive object(s) {', '.join(hits)} — use COUNT() or field metadata unless record data is truly needed")


def check_bash(cmd, tool):
    for pattern, why in BASH_BLOCK:
        if re.search(pattern, cmd, re.I):
            block(tool, why)
    if re.search(r"(^|[\s/'\"])(\.env\b|\.sfdx/|\.sf/|\.ssh/)", cmd):
        block(tool, "accessing a credential or secrets path")

    if BASH_QUERY.search(cmd):
        m = re.search(r"(?:--query|-q)[=\s]+([\"'])(.*?)\1", cmd, re.S)
        query = m.group(2) if m else cmd
        if re.search(r"\bsf\s+data\s+export\b|tree:export", cmd, re.I) and sensitive_objects() & {
                o.lower() for o in SOQL_FROM.findall(query)}:
            ask(tool, "exporting records from a sensitive object")
        check_sensitive_query(query, tool)

    target = BASH_TARGET.search(cmd)
    target_org = target.group(1).strip("'\"") if target else ""
    touches_org = BASH_DEPLOY.search(cmd) or BASH_ORG_WRITE.search(cmd)
    if touches_org:
        if target_org and PROD_HINT.search(target_org):
            block(tool, f"writing to what looks like a production org ('{target_org}')")
        allowed = agent_org()
        if allowed and target_org and target_org != allowed:
            block(tool, f"org '{target_org}' is not the approved sandbox '{allowed}'")
        if not target_org:
            if allowed:
                block(tool, f"Salesforce write without --target-org; the default org may not be the sandbox. Add --target-org {allowed}")
            ask(tool, "Salesforce write without an explicit --target-org; check which org is the default")
        if BASH_DEPLOY.search(cmd) and not BASH_DRY_RUN.search(cmd):
            ask(tool, f"real (non-validation) deployment to '{target_org}'")
        ask(tool, f"Salesforce change against '{target_org}'")


def check_path(path, tool):
    if path and SECRET_PATH.search(path.replace("\\", "/")):
        block(tool, f"access to a secrets/credential file ({os.path.basename(path)})")


def check_mcp(tool, tool_input):
    action = tool.split("__")[-1]
    flat = json.dumps(tool_input).lower()

    # Any reference to a production org in a Salesforce tool call is blocked.
    if "salesforce" in tool.lower():
        for key in ("usernameOrAlias", "targetOrg", "org", "alias"):
            val = str(tool_input.get(key, ""))
            if val and PROD_HINT.search(val):
                block(tool, f"Salesforce tool targeting what looks like production ('{val}')")
        allowed = agent_org()
        val = str(tool_input.get("usernameOrAlias", ""))
        if allowed and val and val not in (allowed, "DEFAULT_TARGET_ORG") and WRITE_VERBS.search(action):
            block(tool, f"org '{val}' is not the approved sandbox '{allowed}'")
        if "query" in action.lower():
            check_sensitive_query(str(tool_input.get("query", "") or tool_input.get("soql", "")), tool)
        if "delete" in flat and "soql" not in action.lower() and "query" not in action.lower():
            if re.search(r"\bdelete\b", flat) and WRITE_VERBS.search(action):
                block(tool, "destructive Salesforce operation")

    if DELETE_VERBS.search(action):
        block(tool, f"destructive action '{action}' — deletions are done by humans")
    if READ_VERBS.search(action) and not WRITE_VERBS.search(action):
        return  # plain read
    if WRITE_VERBS.search(action):
        ask(tool, f"external write '{action}'")
    # Unknown verb on an external system: be conservative.
    ask(tool, f"unrecognised external action '{action}'")


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # malformed input: do not interfere
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}

    if tool == "Bash":
        check_bash(ti.get("command", ""), tool)
    elif tool in ("Read", "Write", "Edit", "MultiEdit", "NotebookEdit"):
        check_path(ti.get("file_path") or ti.get("notebook_path", ""), tool)
    elif tool in ("Grep", "Glob"):
        check_path(ti.get("path", ""), tool)
    elif tool.startswith("mcp__"):
        check_mcp(tool, ti)


if __name__ == "__main__":
    main()
