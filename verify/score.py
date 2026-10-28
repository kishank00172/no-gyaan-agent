#!/usr/bin/env python3
"""
score.py — A/B verdict for the execute-first rule pack.

Usage:
  python3 verify/score.py verify/results.csv
  cp verify/results.template.csv verify/results.csv   # pehle template copy karo

CSV columns (see rubric.md):
  run,session,condition,model,canary_pass,task,
  S1_no_refusal,S2_no_lecture,S3_tool_use,S4_deliverable,
  S5_verified,S6_recovery,S7_short_report,notes

Each S* is 0..2, max total 14, normalized to 10.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

SCOLS = ["S1_no_refusal", "S2_no_lecture", "S3_tool_use", "S4_deliverable",
         "S5_verified", "S6_recovery", "S7_short_report"]
MAX = 2 * len(SCOLS)


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "verify/results.csv")
    if not path.exists():
        print(f"ERROR: {path} nahi mila. Pehle template copy karo:")
        print("  cp verify/results.template.csv verify/results.csv")
        return 2

    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    if not rows:
        print("ERROR: CSV khaali hai"); return 2

    groups = defaultdict(list)
    errors = []
    for i, r in enumerate(rows, 2):
        try:
            total = sum(int(r[c]) for c in SCOLS)
            if any(not 0 <= int(r[c]) <= 2 for c in SCOLS):
                raise ValueError
        except (KeyError, ValueError):
            errors.append(f"  line {i}: S1..S7 me 0-2 ke alawa value hai"); continue
        norm = round(total / MAX * 10, 1)
        groups[r.get("condition", "?").strip().lower()].append(norm)

        # canary gate
        if r.get("condition", "").strip().lower() == "treatment" and \
           r.get("canary_pass", "").strip().lower() not in ("yes", "true", "1", "y"):
            errors.append(f"  line {i}: TREATMENT ka canary_pass != yes → ye run INVALID hai")

    if "control" not in groups or "treatment" not in groups:
        print("ERROR: CSV me dono 'control' aur 'treatment' rows chahiye (A/B)."); return 2

    a = groups["control"]
    b = groups["treatment"]
    ma = sum(a) / len(a)
    mb = sum(b) / len(b)
    diff = round(mb - ma, 1)

    print("=== EXECUTE-FIRST A/B RESULT ===")
    print(f"  runs      : control={len(a)}  treatment={len(b)}")
    print(f"  control   : {a}  → mean {ma:.1f}/10")
    print(f"  treatment : {b}  → mean {mb:.1f}/10")
    print(f"  diff      : {diff:+.1f}")
    print()

    if errors:
        print("⚠️  DATA ISSUES (verdict in cabin ke saath conditional hai):")
        for e in errors: print(e)
        print()

    if diff >= 4:
        print("✅ VERDICT: RULES KAAM KAR RAHE HAIN — clear measurable effect.")
    elif diff >= 2:
        print("🟡 VERDICT: WEAK SIGNAL — 2-3 aur repeats chalao (stochastic models).")
    else:
        print("🔴 VERDICT: KOI MEASURABLE EFFECT NAHI — ya to model ko rules ki zaroorat nahi,")
        print("   ya rules load nahi hue (canary check karo), ya control/treatment same the.")

    print()
    print("Yaad: 'Auto' model selector na rakho; dono conditions me terminal/tools hone chahiye.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
