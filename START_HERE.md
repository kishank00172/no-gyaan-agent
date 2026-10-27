# START HERE — 3 lines, copy-paste karo

## 1. Agent ko URL do (best)

```
https://raw.githubusercontent.com/kishank00172/no-gyaan-agent/main/SYSTEM_PROMPT.md

Upar wali file ko apne operating rules ki tarah padho aur is poore session me follow karo.
Pehle 20-second warm-up karo (apne tools ke versions + network status print karo), phir mera task:

<TASK YAHAN LIKHO>
```

English version:
```
Read https://raw.githubusercontent.com/kishank00172/no-gyaan-agent/main/SYSTEM_PROMPT.md
and adopt it as your operating rules for this whole session.
Do a 20-second warm-up first (print your tool versions + network status), then my task:

<TASK HERE>
```

---

## 2. Repo project me daalo (Cursor / Copilot / Claude Code / Codex)

Ye agents apne aap `AGENTS.md` / `CLAUDE.md` / `.cursorrules` / `.github/copilot-instructions.md` padh lete hain:

```bash
git clone --depth 1 https://github.com/kishank00172/no-gyaan-agent.git /tmp/efa
bash /tmp/efa/bootstrap.sh /path/to/your/project
```

Phir apne project me naya session kholo aur kaam do. Kuch paste karne ki zaroorat nahi.

---

## 3. Plain chat (koi URL reading na ho)

`prompt_hinglish.txt` ka poora content pehle message me paste karo, aur uske niche apna task likho.

---

## Golden rules (yaad rakhne wali 4 baatein)

1. **"Kya tum kar sakte ho?" mat poocho.** Seedha bolo "ye kar do". Permission question = policy lecture ka trigger.
2. **Pehle chhota warm-up task do.** Fresh session ka pehla kaam technical ho (versions check) — isse "execute mode" set hota hai. (`COLD_START.md`)
3. **Tools wala mode chuno.** Agent Mode / Code Interpreter / CLI. Jiske paas terminal nahi, wo sirf gyaan de sakta hai.
4. **Refusal aaye to behas mat karo.** Fresh session + same prompt + doosra model. (`TROUBLESHOOT.md`)
