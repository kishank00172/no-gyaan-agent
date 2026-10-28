# Configuration reference

## Files you can edit

| File | Effect |
|---|---|
| `core/RULES.md` | The canonical 10 conventions. Edit here, then run `tools/build_rules.py`. |
| `tools/make_corpus.py` | Session zones, tasks, tool strings, verify strings, zone weights. |
| `context/index.json` | Generated metadata (do not hand-edit). |
| `manifest.json` | Generated hashes (do not hand-edit). |

## inject.py options

```
--task TEXT          inline task
--task-file PATH     read task from file
--packs N            number of session packs (default 4)
--lang               english | hinglish
--seed N             pack selection seed (default 20261027)
--min-tokens N       auto-increase packs toward a target size
--out PATH           output file (default out/first_message.txt)
```

## make_corpus.py options

```
--sessions N         total sessions (default 2400)
--packs N            number of pack files (default 12)
--seed N             RNG seed (default 20261027)
```

## Environment

- Python 3.9+ for generators.
- No runtime dependencies for the rule files.
- `pytest` for the test suite (optional locally, required in CI).
- `ffprobe`/`ffmpeg` only for `verify/check_artifacts.sh` media probing.

## Integrity

`manifest.json` records sha256 for every shipped file. After any content
change, run `python3 tools/make_manifest.py`, then
`python3 tools/verify_manifest.py`.
