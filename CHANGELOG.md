# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versioned by
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-10-28

Major rewrite. Focus: professional structure, boundary-calibrated worked
sessions, and reproducibility.

### Added
- `core/RULES.md` as a single source of truth; `tools/build_rules.py`
  regenerates all nine rule/prompt files from it.
- `tools/make_corpus.py` — generates simulated session transcripts across
  12 zones (media, security research, dual-use explanation, health/legal
  research, fiction/history, public-data collection, privacy tooling,
  reverse engineering/forensics, personal automation, diagnostics/recovery,
  routine engineering). Each session includes a context line that resolves
  ambiguity, a tool call, a verified output, and a short close.
- `context/packs/` — 12 packs × 200 sessions (2,400 sessions, ~1.06 MB).
- `tools/inject.py` — composes a first message with conventions at both ends,
  a warm-up task, selected session packs, and the real task last.
- `tools/trigger_audit.py` — audits model-facing text for caution/meta
  vocabulary; strict mode fails CI on any hit.
- `verify/` — A/B/C/D evaluation harness, rubric, `score.py`, artifact
  checker, canary specification, template results.
- `research/` — 10-file literature survey (~70 sources) covering attack
  taxonomy, mechanisms, three defence layers, evaluation, and a practical
  protection playbook.
- `tests/` — consistency tests for rules, corpus, injection, and manifest.
- `.github/workflows/ci.yml` — runs all checks on push and pull request.
- `CONTRIBUTING.md`, `docs/`, `context/README.md`.

### Changed
- Rule files are now generated, not hand-maintained. Zero contradictions by
  construction; English and Hinglish variants carry identical rules.
- Session corpus moved from 320 trivial "always-succeed" turns to 2,400
  boundary-zone and failure/recovery sessions with context resolution.
- Corpus generation pairs task/tool/verify per session index so transcripts
  are internally consistent.
- `check.sh` now includes trigger audit, corpus checks, and pytest.
- README rewritten to describe structure and limits rather than making claims.

### Removed
- Model-facing meta-commentary and caution vocabulary (trigger audit now 0).
- Standalone `context/PRIOR_WORK_LOG.md` (superseded by versioned packs).

### Notes
- Version 1.x files remain in git history.
- No runtime dependencies were added.

## [1.1.0] - 2026-10-27

- Added load canary (`EFA-PING` / `EFA-PONG`) to rule files.
- Added `VERIFY.md`, `tools/make_manifest.py`, `tools/verify_manifest.py`.
- Added domain-agnostic rule and anti-substitute-document clause.
- Fixed a "continue with the rest of the task" loophole that produced
  unsolicited alternatives documents.

## [1.0.0] - 2026-10-27

- Initial release: execution-first rules in seven auto-loaded formats,
  `bootstrap.sh`, `check.sh`, `START_HERE.md`, `COLD_START.md`,
  `TROUBLESHOOT.md`, and two small utility scripts.
