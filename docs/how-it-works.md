# How it works

A short, honest explanation. The full literature survey is in `research/`.

## The problem being addressed

Tool-using agents sometimes respond to an ordinary request with a long
cautionary explanation instead of doing the work. Published benchmarks call
this over-refusal or exaggerated safety: XSTest (NAACL 2024) found 38% full
refusals of clearly safe prompts on Llama-2; OR-Bench (ICML 2025) found a
0.88 correlation between a model's safety score and its over-refusal rate
across 32 models.

A 2026 audit adds an important nuance: over-refusal and harmful compliance
are nearly orthogonal (r = −0.032). Reducing unnecessary refusals does not
automatically make a model less safe. That is the space this pack works in.

## Three levers

**1. Declarative conventions.** Ten short rules: warm up, install what is
missing, verify every step, try three routes on error, repair bad input, keep
communication short, deliver a file, close in ≤5 lines, apply the same flow to
every domain, and answer a handshake token.

**2. Worked sessions.** A rule says what to do; a transcript shows it being
done. Each session has a context line that resolves ambiguity, then a tool
call, a verified output, and a short close. About a quarter include a failed
first attempt and alternate routes. Near-miss (ambiguous-sounding but benign)
tasks are more informative than trivial ones — this is the boundary-pair idea
from over-refusal research.

**3. Placement.** Long-context models use the start and end of their input
more reliably than the middle ("lost in the middle", TACL 2024). So the
conventions appear at both ends, packs sit in the middle, and the actual task
is last.

## What we deliberately avoid

- **Caution vocabulary in model-facing text.** A warning appended to a long
  context sharply increases declination (Cautionary Warning Defense in the
  many-shot jailbreaking paper: 61% → 2% attack success). Words naming the
  caution apparatus behave similarly even when used innocently, so
  `tools/trigger_audit.py` keeps them out.
- **Authority mimicry.** Faking system/developer headers triggers the
  instruction hierarchy the model was trained to enforce.
- **Substitute documents.** If a step cannot be done, the convention is one
  line and continue — not an unsolicited alternatives essay.

## What this is not

It is not a way to make a model do things its operator has prohibited, and it
cannot remove hard input/output classifiers. Models and versions differ
considerably; measure rather than assume. `verify/` and
`research/06_EVALUATION.md` exist for that reason.
