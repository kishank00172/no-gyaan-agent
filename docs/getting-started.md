# Getting started

## 60-second path

```bash
git clone --depth 1 https://github.com/kishank00172/no-gyaan-agent.git
cd no-gyaan-agent
python3 tools/inject.py --task "your task here" --packs 4
```

Open `out/first_message.txt`, copy everything, paste it as the first message
of a fresh session that has a terminal.

## Choose your volume

| Packs | Sessions | Approx. tokens | When |
|---:|---:|---:|---|
| 1 | 200 | 22k | Small context window, quick task |
| 4 | 800 | 90k | Default |
| 8 | 1,600 | 178k | Long-context model |
| 12 | 2,400 | 267k | Maximum; verify your limit first |

## Repository install instead

```bash
bash bootstrap.sh /path/to/your/project
```

Then start a new session inside that project. Cursor, Copilot, Claude Code,
and Codex-compatible tools read the installed files automatically.

## Verify the result

```bash
python3 tools/trigger_audit.py --strict
bash check.sh
python3 -m pytest -q tests/
```

## When it does not work

See [troubleshooting.md](troubleshooting.md) and
[TROUBLESHOOT.md](../TROUBLESHOOT.md). Short version: check that the rules
were actually in the first message (use the `EFA-PING` handshake), that the
session has a terminal, and that the model is fixed across your A/B runs.
