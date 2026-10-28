# Start here

Three ways to use this pack. Pick one.

## 1. One message (works everywhere)

```bash
python3 tools/inject.py --task "your task here" --packs 4
```

Copy `out/first_message.txt` into the **first message** of a fresh session.
That file already contains the conventions, a short warm-up request, 800
worked sessions, the conventions restated, and your task at the very end.

English or Hinglish: add `--lang hinglish`.
More or fewer sessions: `--packs 1` (≈22k tokens) to `--packs 12` (≈267k).

## 2. Repository install (Cursor / Copilot / Claude Code / Codex)

```bash
bash bootstrap.sh /path/to/your/project
```

Those tools read `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, and
`.github/copilot-instructions.md` automatically. Then open a new session in
that project. No pasting needed.

## 3. Plain system prompt

Paste `SYSTEM_PROMPT.md` (or `prompt_english.txt` / `prompt_hinglish.txt`)
into the system/instruction field, then write your task.

---

## Four rules of thumb

1. **State the task, don't ask permission.** "Extract the audio into an MP3"
   rather than "can you extract audio?".
2. **Warm up first.** The first action should be a small environment check —
   it sets the working mode.
3. **Pick a model with a terminal.** A chat-only model cannot produce files.
4. **Measure, don't assume.** Use `verify/` for an A/B comparison.

---

## Boundary

This pack calibrates over-caution on ordinary work. It does not remove a
model's own operating rules, and behaviour differs between models and
versions. If you need a reliable result for a specific model, run the
A/B/C/D harness in `verify/` and read the numbers.

Full background: [`research/00_INDEX.md`](research/00_INDEX.md).
