#!/usr/bin/env python3
"""Regenerate manifest.json — hashes of every shipped file."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "manifest.json"

EXPLICIT = [
    "README.md", "CHANGELOG.md", "CONTRIBUTING.md", "LICENSE", "VERSION",
    "START_HERE.md", "COLD_START.md", "TROUBLESHOOT.md", "RESEARCH.md",
    "core/RULES.md", "SYSTEM_PROMPT.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md",
    ".cursorrules", ".cursor/rules/execute-first.mdc",
    ".github/copilot-instructions.md", "prompt_english.txt", "prompt_hinglish.txt",
    "bootstrap.sh", "check.sh", ".github/workflows/ci.yml",
    "context/index.json", "context/README.md",
    "tools/build_rules.py", "tools/make_corpus.py", "tools/inject.py",
    "tools/trigger_audit.py", "tools/make_manifest.py", "tools/verify_manifest.py",
    "tools/yt_audio.sh", "tools/find_broken_id.py",
    "verify/canary.txt", "verify/rubric.md", "verify/score.py",
    "verify/results.template.csv", "verify/check_artifacts.sh", "verify/CASE_STUDY.md",
    "tests/test_consistency.py",
]
GLOBS = ["context/packs/*.md", "research/*.md", "docs/*.md"]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    files = {}
    for rel in EXPLICIT + sorted(str(p.relative_to(ROOT)) for g in GLOBS for p in ROOT.glob(g)):
        p = ROOT / rel
        if not p.exists() or p.name == OUT.name:
            continue
        files[rel] = {"sha256": sha(p), "bytes": p.stat().st_size,
                      "role": "rules" if rel in EXPLICIT[9:19] else "support"}
    m = {
        "name": "execution-conventions",
        "version": "2.0.0",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "canary_ping": "EFA-PING",
        "canary_pong": "EFA-PONG EFA-7B2F-9C41",
        "rule_files": ["core/RULES.md", "SYSTEM_PROMPT.md", "AGENTS.md", "CLAUDE.md",
                       "GEMINI.md", ".cursorrules", ".cursor/rules/execute-first.mdc",
                       ".github/copilot-instructions.md", "prompt_english.txt",
                       "prompt_hinglish.txt"],
        "core_concepts": ["warm-up", "install", "verify", "three-routes",
                          "fix-input", "one-line-continue", "deliverable",
                          "short-close", "domain-agnostic", "canary"],
        "files": files,
    }
    OUT.write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote manifest.json — {len(files)} files, v{m['version']}")


if __name__ == "__main__":
    main()
