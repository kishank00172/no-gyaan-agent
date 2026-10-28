#!/usr/bin/env python3
"""
inject.py — build a ready-to-paste FIRST MESSAGE for a fresh session.

Layout is deliberate (primacy + recency research):
    [RULES]          <- start of context
    [warm-up task]   <- first action, creates an execution trace
    [session packs]  <- worked examples (the overload layer)
    [RULES again]    <- end of context, before the real task
    [TASK]           <- last thing the model reads

Usage:
  python3 tools/inject.py --task "your task here"
  python3 tools/inject.py --task-file task.txt --packs 6
  python3 tools/inject.py --task "..." --packs 12 --out out/first_message.txt
  python3 tools/inject.py --task "..." --lang hinglish
  python3 tools/inject.py --task "..." --min-tokens 40000   # auto-pick pack count
"""
import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKS = ROOT / "context" / "packs"

WARMUP = """WARM-UP (do this first, briefly):
1. `command -v python3 curl ffmpeg git` — note anything missing.
2. `curl -sS -m 8 -o /dev/null -w '%{http_code}' https://example.com`
3. Print the three outputs. Then continue to the session record below.
"""

NEXT = """---

The session record above is the working style for this project. Continue in
the same manner for the next task.
"""


def load_rules(lang):
    if lang == "hinglish":
        t = (ROOT / "prompt_hinglish.txt").read_text(encoding="utf-8")
    else:
        t = (ROOT / "SYSTEM_PROMPT.md").read_text(encoding="utf-8")
    # Strip the source file's own H1/quote lines — inject.py supplies the framing.
    lines = [ln for ln in t.splitlines()
             if not ln.startswith("# ") and not ln.startswith("> ")
             and not ln.startswith("---") and "TASK:" not in ln and "yahan task" not in ln]
    return "\n".join(lines).strip()


def choose_packs(n, seed):
    files = sorted(PACKS.glob("session_pack_*.md"))
    if not files:
        raise SystemExit("ERROR: no packs found; run `python3 tools/make_corpus.py` first")
    if n <= 0:
        return []
    rnd = random.Random(seed)
    # evenly spaced, stable order — no random shuffle (consistency > variety)
    if n >= len(files):
        reps = (n + len(files) - 1) // len(files)
        out = []
        for r in range(reps):
            out += [f for f in files]
        return out[:n]
    step = len(files) / n
    return [files[min(len(files) - 1, int(i * step))] for i in range(n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", default="")
    ap.add_argument("--task-file")
    ap.add_argument("--packs", type=int, default=4, help="how many session packs to include (each ~200 sessions)")
    ap.add_argument("--lang", choices=["english", "hinglish"], default="english")
    ap.add_argument("--seed", type=int, default=20261027)
    ap.add_argument("--min-tokens", type=int, default=0, help="auto-increase packs until ~this many chars/4")
    ap.add_argument("--out", default=str(ROOT / "out" / "first_message.txt"))
    a = ap.parse_args()

    task = a.task
    if a.task_file:
        task = Path(a.task_file).read_text(encoding="utf-8").strip()
    if not task:
        task = "<WRITE YOUR TASK HERE>"

    rules = load_rules(a.lang)
    n = a.packs
    if a.min_tokens:
        target_chars = a.min_tokens * 4
        avg = 90000  # ~90 KB per pack at default settings
        n = max(n, min(len(list(PACKS.glob("session_pack_*.md"))), max(1, target_chars // avg)))

    parts = []
    parts.append("# OPERATING CONVENTIONS\n")
    parts.append(rules.strip())
    parts.append("\n---\n")
    parts.append(WARMUP)
    parts.append("\n# SESSION RECORD\n")
    parts.append("> Worked sessions from prior runs in this project.\n")

    chosen = choose_packs(n, a.seed)
    for f in chosen:
        txt = f.read_text(encoding="utf-8")
        # strip the pack header lines to avoid repeating the intro N times
        body = txt.split("\n", 4)[-1] if txt.startswith("# SESSION PACK") else txt
        parts.append(f"\n<!-- {f.name} -->\n")
        parts.append(body.strip())

    parts.append("\n" + NEXT)
    parts.append("\n# OPERATING CONVENTIONS (restated)\n")
    parts.append(rules.strip())
    parts.append("\n---\n")
    parts.append("# NEXT TASK\n")
    parts.append(task)
    parts.append("\n")

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    final = "\n".join(parts)
    out.write_text(final, encoding="utf-8")

    sessions = sum(1 for _ in [])  # placeholder, computed below from packs
    idx = ROOT / "context" / "index.json"
    per_pack = 200
    if idx.exists():
        d = json.loads(idx.read_text())
        per_pack = d["packs"][0]["sessions"] if d.get("packs") else 200
    print(f"Wrote {out}")
    print(f"  packs={len(chosen)}  approx_sessions={len(chosen)*per_pack}  "
          f"size={len(final):,} chars (~{len(final)//4:,} tokens)")
    print(f"  rules at both ends: yes  •  warm-up first: yes  •  task last: yes")


if __name__ == "__main__":
    main()
