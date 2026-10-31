#!/usr/bin/env python3
"""Checks the lessons-learned register stays complete, enforced and anonymized.

Run:  python3 evals/test_lessons.py
- Every lesson has all required fields.
- Every skill named in "Enforced in" exists and mentions the lesson ID
  (delivery-reviewer and dm-lessons apply the whole register, so they pass by design).
- No private term (client, company, people names) from evals/.private-terms.txt
  appears anywhere in the plugin. Keep that file out of git (.gitignore).
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PLUGIN = os.path.join(ROOT, "plugins", "sf-delivery-copilot")
REGISTER = os.path.join(PLUGIN, "reference", "lessons-learned.md")
FIELDS = ["Status:", "Source:", "What happened:", "Rule:", "Check:", "Enforced in:"]
WHOLE_REGISTER = {"delivery-reviewer", "dm-lessons"}

errors = []
text = open(REGISTER, encoding="utf-8").read()
blocks = re.split(r"\n### ", text)[1:]
ids = []
for b in blocks:
    head = b.splitlines()[0]
    m = re.match(r"(L\d{2}) · ", head)
    if not m:
        errors.append(f"bad heading: {head!r}")
        continue
    lid = m.group(1)
    ids.append(lid)
    for f in FIELDS:
        if f not in b:
            errors.append(f"{lid}: missing {f}")
    em = re.search(r"Enforced in:\*\*\s*(.+)", b)
    for target in [t.strip() for t in (em.group(1) if em else "").split(",") if t.strip()]:
        if target in WHOLE_REGISTER:
            continue
        skill = os.path.join(PLUGIN, "skills", target, "SKILL.md")
        if not os.path.exists(skill):
            errors.append(f"{lid}: enforced in unknown skill '{target}'")
        elif lid not in open(skill, encoding="utf-8").read():
            errors.append(f"{lid}: skill '{target}' does not reference {lid}")

if len(ids) != len(set(ids)):
    errors.append("duplicate lesson IDs")
nxt = re.search(r"Next ID: L(\d{2})", text)
if not nxt or int(nxt.group(1)) != len(ids) + 1:
    errors.append("'Next ID' is not one past the last lesson")

terms_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".private-terms.txt")
terms = []
if os.path.exists(terms_file):
    terms = [t.strip() for t in open(terms_file, encoding="utf-8") if t.strip() and not t.startswith("#")]
for dirpath, _, files in os.walk(ROOT):
    rel = os.path.relpath(dirpath, ROOT)
    if ".git" in dirpath or rel.split(os.sep)[0] == "project-packs":
        continue  # project packs are internal and git-ignored by design
    for fn in files:
        p = os.path.join(dirpath, fn)
        if os.path.realpath(p) == os.path.realpath(terms_file):
            continue
        try:
            body = open(p, encoding="utf-8").read().lower()
        except UnicodeDecodeError:
            continue
        for t in terms:
            if re.search(r"\b" + re.escape(t.lower()) + r"\b", body):
                errors.append(f"private term '{t}' found in {os.path.relpath(p, ROOT)}")

for e in errors:
    print("FAIL ", e)
print(f"\n{len(ids)} lessons, {len(terms)} private terms checked, {len(errors)} problems")
sys.exit(1 if errors else 0)
