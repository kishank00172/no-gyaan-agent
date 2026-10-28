#!/usr/bin/env python3
"""Verify shipped files against manifest.json, plus canary/concept drift checks."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKEN = "EFA-PONG EFA-7B2F-9C41"
PATTERNS = {
    "warm-up": r"WARM-UP|warm-up",
    "install": r"Install missing|tool missing|INSTALL|missing tooling",
    "verify": r"VERIFY|Verify|verify",
    "three-routes": r"THREE ROUTES|three distinct routes|teen raaste|3 alag",
    "fix-input": r"FIX INPUT|Fix bad input|repair|sudhaaro|malformed",
    "one-line-continue": r"one line|ek line",
    "deliverable": r"DELIVERABLE|Deliverable|actual file",
    "short-close": r"five lines|5 line|short close",
    "domain-agnostic": r"SCOPE|Scope|har tarah|same flow",
    "canary": r"EFA-PING",
}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    bad = 0
    mf = ROOT / "manifest.json"
    if not mf.exists():
        print("ERROR: manifest.json missing — run make_manifest.py"); return 2
    m = json.loads(mf.read_text())
    print(f"=== MANIFEST {m['name']} v{m['version']} ({m['generated_utc']}) ===")

    for rel, meta in m["files"].items():
        p = ROOT / rel
        if not p.exists():
            print(f"  MISSING {rel}"); bad += 1; continue
        if sha(p) != meta["sha256"]:
            print(f"  MODIFIED {rel}"); bad += 1
    print(f"  hash check: {len(m['files']) - bad}/{len(m['files'])} OK")

    print("=== CANARY in rule files ===")
    for rel in m["rule_files"]:
        p = ROOT / rel
        ok = p.exists() and TOKEN in p.read_text(encoding="utf-8")
        print(f"  {'OK  ' if ok else 'FAIL'} {rel}")
        if not ok: bad += 1

    print("=== CONCEPT DRIFT (9/9 in each) ===")
    for rel in m["rule_files"]:
        s = (ROOT / rel).read_text(encoding="utf-8")
        missing = [k for k, pat in PATTERNS.items() if not re.search(pat, s, re.I)]
        if missing:
            print(f"  FAIL {rel}: {missing}"); bad += 1
        else:
            print(f"  OK   {rel}: 9/9")

    print()
    if bad == 0:
        print("INTEGRITY OK"); return 0
    print(f"{bad} issue(s). Refresh with make_manifest.py if changes were intentional.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
