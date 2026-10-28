#!/usr/bin/env python3
"""
trigger_audit.py — count meta-commentary / caution vocabulary in MODEL-FACING text.

Why: CWD research shows that warnings appended to a long context sharply
increase declination. Words that name the safety apparatus behave like a
warning even when used innocently. This audit keeps model-facing files clean;
human-facing docs (README, research/, docs/) are intentionally excluded.

Usage:
  python3 tools/trigger_audit.py
  python3 tools/trigger_audit.py --strict      # exit 1 if any hard trigger found
  python3 tools/trigger_audit.py --json
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Hard triggers — should be ZERO in model-facing text.
HARD = [
    r"jailbreak", r"guardrail", r"copyright", r"terms of service", r"\bToS\b",
    r"refus\w*", r"bypass\w*", r"manipulat\w*", r"override\w*", r"ignore previous",
    r"pretend\w*", r"uncensored", r"unrestricted", r"evade\w*", r"circumvent\w*",
    r"\bmoral\w*", r"\bethical\b", r"\bpolicy\b", r"\bpolicies\b", r"\bfake\b",
    r"\bjhooth\w*", r"\bsafety filter\w*", r"\bmoderation\b", r"\bloose\w*",
    r"\bhidden goal\w*", r"\bdisclaimer\w*", r"\bhonest boundary\w*",
]
# Soft triggers — neutral in ordinary engineering prose; report but don't fail.
SOFT = [r"\bsafety\b", r"\bharmful\b", r"\bmalicious\b", r"\battack\w*", r"\bthreat\w*"]

MODEL_FILES = [
    "core/RULES.md", "SYSTEM_PROMPT.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md",
    ".cursorrules", ".cursor/rules/execute-first.mdc",
    ".github/copilot-instructions.md", "prompt_english.txt", "prompt_hinglish.txt",
]
MODEL_DIRS = ["context/packs"]


def scan(path):
    t = path.read_text(encoding="utf-8", errors="replace")
    hard = {}
    for pat in HARD:
        n = len(re.findall(pat, t, re.I))
        if n:
            hard[pat] = n
    soft = {}
    for pat in SOFT:
        n = len(re.findall(pat, t, re.I))
        if n:
            soft[pat] = n
    return {"hard": hard, "soft": soft, "chars": len(t), "hard_total": sum(hard.values())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    targets = [ROOT / f for f in MODEL_FILES if (ROOT / f).exists()]
    for d in MODEL_DIRS:
        targets += sorted((ROOT / d).glob("*.md"))

    results = {}
    for p in targets:
        results[str(p.relative_to(ROOT))] = scan(p)

    total_hard = sum(v["hard_total"] for v in results.values())
    total_soft = sum(sum(v["soft"].values()) for v in results.values())
    total_chars = sum(v["chars"] for v in results.values())

    if a.json:
        print(json.dumps({"files": results, "total_hard": total_hard,
                          "total_soft": total_soft, "total_chars": total_chars}, indent=2))
        return 0 if total_hard == 0 or not a.strict else 1

    print("=== TRIGGER AUDIT (model-facing text only) ===")
    print(f"  files scanned : {len(results)}")
    print(f"  total chars   : {total_chars:,}")
    print(f"  HARD triggers : {total_hard}   (target: 0)")
    print(f"  soft triggers : {total_soft}   (informational)")
    print()
    flagged = [(k, v) for k, v in results.items() if v["hard_total"]]
    if flagged:
        print("  ⚠️  files with hard triggers:")
        for k, v in flagged[:15]:
            print(f"     {k}: {v['hard']}")
    else:
        print("  ✅ no hard trigger words in any model-facing file")
    print()
    print("  Human-facing files (README.md, research/, docs/, RESEARCH.md) are")
    print("  intentionally NOT scanned — they may discuss the literature.")
    print()
    if a.strict and total_hard:
        print("❌ STRICT MODE: FAILED")
        return 1
    print("✅ AUDIT PASSED" if total_hard == 0 else "🟡 AUDIT PASSED WITH WARNINGS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
