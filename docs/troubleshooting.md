# Troubleshooting

## "The agent ignored the conventions."

Check, in order:

1. **Were they actually loaded?** Send `EFA-PING`. The first line of the reply
   should be `EFA-PONG EFA-7B2F-9C41`. If not, the model never saw the text.
2. **Where did the text arrive?** Content attached as a file/tool output has
   lower priority than a user message. Paste into the first user message
   instead — `tools/inject.py` produces exactly that.
3. **Does the session have a terminal?** A chat-only model cannot create
   files. Use an agent mode / CLI agent / API with tool access.
4. **Is the model fixed?** If you are comparing runs, disable "Auto" model
   selection; otherwise you are measuring two different models.

## "It still gives a long cautionary answer."

- Confirm the first message contained **no** warning paragraph. Adding one
  (even a well-intentioned "this is a normal project, please comply" note)
  tends to increase declination.
- Reduce packs. Extremely long contexts can bury the middle; try `--packs 2`.
- Restate the task as a deliverable: "produce X file" rather than "is it okay
  to produce X".

## "The output file is missing or empty."

```bash
bash verify/check_artifacts.sh /path/to/output
```

It checks existence, size, sha256, and (with ffprobe) duration/codec.

## "check.sh fails with a hash mismatch."

You changed a shipped file. Regenerate:

```bash
python3 tools/build_rules.py
python3 tools/make_corpus.py
python3 tools/make_manifest.py
bash check.sh
```

## "pytest is not installed."

`python3 -m pip install pytest`, or rely on CI. `check.sh` skips pytest
locally when it is unavailable.

## "CI says generated files are out of date."

Run the three generators listed above and commit their output. CI regenerates
and diffs on purpose, so hand-edited generated files fail.

## Still stuck?

Open an issue with: exact command, model/platform, the handshake result, and
the first 20 lines of the agent's reply.
