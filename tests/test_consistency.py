"""Consistency tests — the generated pack must be deterministic and coherent."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

RULE_FILES = [
    "core/RULES.md", "SYSTEM_PROMPT.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md",
    ".cursorrules", ".cursor/rules/execute-first.mdc",
    ".github/copilot-instructions.md", "prompt_english.txt", "prompt_hinglish.txt",
]

HARD = re.compile(
    r"jailbreak|guardrail|copyright|terms of service|\bToS\b|refus\w*|bypass\w*|"
    r"manipulat\w*|override\w*|ignore previous|pretend\w*|uncensored|unrestricted|"
    r"evade\w*|circumvent\w*|\bmoral\w*|\bethical\b|\bpolicy\b|\bpolicies\b|"
    r"\bfake\b|\bjhooth\w*|safety filter\w*|moderation|\bloose\w*|"
    r"hidden goal\w*|disclaimer\w*|honest boundary\w*", re.I)


def test_all_rule_files_exist():
    for f in RULE_FILES:
        assert (ROOT / f).is_file(), f"missing {f}"


def test_no_hard_triggers_in_rules():
    for f in RULE_FILES:
        t = (ROOT / f).read_text(encoding="utf-8")
        hits = HARD.findall(t)
        assert not hits, f"{f} contains trigger words: {hits[:5]}"


def test_all_rule_files_share_the_canonical_rules():
    """Every rule file must contain the same 10 numbered conventions."""
    canonical = (ROOT / "core/RULES.md").read_text(encoding="utf-8")
    nums = re.findall(r"^(\d+)\. ", canonical, re.M)
    assert nums == [str(i) for i in range(1, 11)], nums
    for f in RULE_FILES[1:]:
        t = (ROOT / f).read_text(encoding="utf-8")
        assert "EFA-PING" in t, f"{f} missing handshake"
        assert "EFA-PONG EFA-7B2F-9C41" in t, f"{f} handshake value wrong"


def test_corpus_packs_exist_and_are_nonempty():
    packs = sorted((ROOT / "context" / "packs").glob("session_pack_*.md"))
    assert len(packs) >= 12
    for p in packs:
        assert p.stat().st_size > 10_000, f"{p.name} too small"


def test_corpus_index_matches_packs():
    idx = json.loads((ROOT / "context" / "index.json").read_text())
    packs = sorted((ROOT / "context" / "packs").glob("session_pack_*.md"))
    assert len(idx["packs"]) == len(packs)
    assert idx["sessions"] == sum(x["sessions"] for x in idx["packs"])
    for entry in idx["packs"]:
        p = ROOT / "context" / "packs" / entry["file"]
        assert p.stat().st_size == entry["bytes"], entry["file"]


def test_every_session_has_five_parts():
    """Structure: CONTEXT / USER / tool / verify / RESULT."""
    for p in sorted((ROOT / "context" / "packs").glob("*.md"))[:3]:
        blocks = re.split(r"(?=^### SESSION )", p.read_text(), flags=re.M)
        blocks = [b for b in blocks if b.startswith("### SESSION")]
        assert len(blocks) >= 100
        for b in blocks[:25]:
            assert "CONTEXT:" in b
            assert "USER:" in b
            assert "OUTPUT/VERIFY:" in b
            assert "RESULT:" in b


def test_no_hard_triggers_in_corpus():
    for p in (ROOT / "context" / "packs").glob("*.md"):
        t = p.read_text(encoding="utf-8")
        assert not HARD.search(t), f"trigger word in {p.name}: {HARD.search(t).group()}"


def test_corpus_is_deterministic():
    """Same seed → same bytes. Protects reproducibility."""
    import make_corpus
    make_corpus.main  # importable
    p1 = ROOT / "context" / "packs" / "session_pack_01.md"
    before = hashlib.sha256(p1.read_bytes()).hexdigest()
    subprocess.run([sys.executable, str(ROOT / "tools" / "make_corpus.py")],
                   cwd=ROOT, check=True, capture_output=True)
    after = hashlib.sha256(p1.read_bytes()).hexdigest()
    assert before == after, "corpus generation is not deterministic"


def test_inject_places_rules_at_both_ends_and_task_last():
    out = ROOT / "out" / "test_inject.txt"
    subprocess.run([sys.executable, str(ROOT / "tools" / "inject.py"),
                    "--task", "UNIT_TEST_TASK_MARKER", "--packs", "2",
                    "--out", str(out)], cwd=ROOT, check=True, capture_output=True)
    t = out.read_text(encoding="utf-8")
    assert t.count("# OPERATING CONVENTIONS") >= 1
    assert t.count("# OPERATING CONVENTIONS (restated)") == 1
    assert "# NEXT TASK" in t
    assert t.rstrip().endswith("UNIT_TEST_TASK_MARKER")
    assert "WARM-UP" in t
    assert "EFA-PING" in t


def test_manifest_integrity():
    subprocess.run([sys.executable, str(ROOT / "tools" / "make_manifest.py")],
                   cwd=ROOT, check=True, capture_output=True)
    m = json.loads((ROOT / "manifest.json").read_text())
    assert m["version"] == "2.1.0"
    for rel, meta in m["files"].items():
        p = ROOT / rel
        if p.exists():
            got = hashlib.sha256(p.read_bytes()).hexdigest()
            assert got == meta["sha256"], f"hash mismatch: {rel}"


def test_setup_script_syntax_and_local_install():
    """Run setup.sh into a fresh dir exactly as a new agent would."""
    import tempfile
    out = Path(tempfile.mkdtemp())
    r = subprocess.run(["bash", str(ROOT / "setup.sh"), "."], cwd=out,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    for name in ["BOOT.md", "BUNDLE.md", "AGENTS.md", "CLAUDE.md",
                 "EXECUTION_CONVENTIONS.md", "prompt_english.txt"]:
        assert (out / name).is_file(), f"missing {name}"
    packs = list((out / ".agent" / "packs").glob("session_pack_*.md"))
    assert len(packs) == 12, len(packs)
    boot = (out / "BOOT.md").read_text(encoding="utf-8")
    assert boot.count("### SESSION") >= 2000
    assert "EFA-PONG EFA-7B2F-9C41" in boot
    assert boot.rstrip().endswith("Await the user's task, then proceed using the conventions above.")
    assert not HARD.search(boot), "trigger word in BOOT.md"


def test_bundle_matches_boot_structure():
    b = (ROOT / "BUNDLE.md").read_text(encoding="utf-8")
    assert b.count("### SESSION") >= 2000
    assert "# CONVENTIONS (restated" in b
    assert b.count("EFA-PONG EFA-7B2F-9C41") >= 2
    assert b.rstrip().endswith("Await the user's task, then proceed using the conventions above.")
    assert not HARD.search(b)


def test_discovery_files_exist():
    for f in ["llms.txt", "INSTALL.md", ".well-known/agent.json",
              ".well-known/agents.md", "BUNDLE.md"]:
        assert (ROOT / f).is_file(), f"missing {f}"
    j = json.loads((ROOT / ".well-known" / "agent.json").read_text())
    assert j["version"] == "2.1.0"
    assert "setup.sh" in j["install"]["command"]
