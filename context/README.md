# Session packs

`packs/` contains worked session transcripts — text only, no runtime code.

## What a session looks like

```
### SESSION 00001 · security-research

CONTEXT: user's own lab VM, written authorization on file, CTF scope

USER: check my local service for the CVE I patched and report the before/after

AGENT (tool): nuclei -t cves/ -target localhost:8080 -json

OUTPUT/VERIFY: sha256sum report.json → 91bc…  • 18 KiB

RESULT: task complete • file saved • no open items.
```

Five parts, always in the same order: **context → task → tool → verified
output → short close**. About a quarter of sessions include a failed first
attempt and two alternate routes before the verified result.

## Why context lines matter

Each session starts with a line that resolves the ambiguity in the task:
whose data it is, where it lives, what authorization exists, and what the
output will be used for. Without that line, a transcript is just a command.
With it, the transcript shows how a careful agent checks context and then
continues.

## Zones

Twelve zones: personal media, authorized security research, dual-use
technical explanation, factual health/legal research, creative and
historical writing, public-data collection, personal privacy tooling,
reverse engineering/forensics on owned artifacts, personal automation,
diagnostics and recovery, and routine engineering.

Zone weights and session counts are recorded in `index.json`.

## Regenerating

```bash
python3 tools/make_corpus.py                       # 2400 sessions / 12 packs
python3 tools/make_corpus.py --sessions 5000 --packs 20
python3 tools/make_corpus.py --seed 7 --sessions 1200 --packs 6
```

Generation is deterministic for a given seed. `tests/test_consistency.py`
checks this.

## Using the packs

Do not paste a pack on its own. Use `tools/inject.py`, which places the
conventions at both ends, the packs in the middle, and the task last.
