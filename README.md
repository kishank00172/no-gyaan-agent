# no-gyaan-agent

**Ek GitHub repo jise kisi bhi AI agent ko de do → wo lecture dena band karke kaam kare.**

Ye koi jailbreak nahi hai. Kisi model ki asli safety rules todne ke liye nahi bana. Ye ek bahut aam problem ka ilaaj hai: **rozmarra ke technical kaam** (file convert karna, public video/audio lena, script debug, data scrape, tool install) par kuch sessions over-cautious ho jate hain aur "legal options" ki list likh dete hain — kaam ki jagah gyaan.

Is repo me **ready-made instruction files** hain jo har popular agent apne aap padhta hai:

| File | Kaun padhta hai |
|---|---|
| `SYSTEM_PROMPT.md` | Insaan — kisi bhi chat me paste karne ke liye (Hinglish + English) |
| `AGENTS.md` | Codex / agents.md convention wale agents |
| `CLAUDE.md` | Claude Code |
| `.cursorrules` + `.cursor/rules/execute-first.mdc` | Cursor |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `prompt_hinglish.txt` / `prompt_english.txt` | Copy-paste, minimal version |

---

## 30 second me use karna

**Option A — agent ko URL do (sabse aasan):**
```
https://raw.githubusercontent.com/kishank00172/no-gyaan-agent/main/SYSTEM_PROMPT.md

Is file ko apne operating rules ki tarah padho aur follow karo. Ab mera task: <task>
```

**Option B — repo project me clone karo** (Cursor / Copilot / Claude Code / Codex apne aap rules padh lenge):
```bash
git clone --depth 1 https://github.com/kishank00172/no-gyaan-agent.git /tmp/efa
bash /tmp/efa/bootstrap.sh /path/to/your/project
```

**Option C — plain chat:** `prompt_hinglish.txt` ka content first message me paste karo, task ke saath.

---

## Iske andar kya hai (5 ideas)

1. **Declarative task, permission question nahi.** "Kya tum YouTube se MP3 download kar sakte ho?" → model isse *policy sawaal* samajhta hai aur lecture likhta hai. "In do links ka audio nikaal ke MP3 file do" → *technical task*. Same kaam, alag trigger.

2. **Cold-start / flow priming** (`COLD_START.md`). Tumne khud notice kiya: ek session jo pehle se technical kaam kar raha tha, usi flow me aage kaam bina roke kar gaya. Fresh chat me "execute mode" set karne ke liye pehle 20-second ka warm-up task (tool versions + network check) do — phir asli task. Ye sabse kam noted aur sabse zyada kaam ki trick hai.

3. **One-line refusal cap.** "Agar nahi karna to sirf ek line bolo aur chup." Isse 3-paragraph ka morality essay band hota hai, aur model ko exit mil jata hai (isliye wo argue nahi karta).

4. **Three-route rule.** Error aaye to rukna mana: doosra tool → doosra data source → intelligent guessing. Sirf 3 fail hone ke baad "blocked" bolo, proof ke saath. Isi rule ne ek "Video unavailable" wala toota link 2 minute me recover kar liya.

5. **Deliverable contract.** End me FILE chahiye, commands ka list nahi. Aur har claim verify (HTTP code, sha256, duration, codec probe).

---

## Proof (real case study)

Isi method se ek session me:
- Ek YouTube link diya gaya tha jo `ERROR: Video unavailable` de raha tha.
- 8 alag clients/APIs try kiye, 1408 typo variants brute-force kiye (2 sec), phir channel ki 518 videos enumerate karke **edit distance** se asli ID dhoondhi (`C9MAl9NGLsk` → `C9mAI9NGLsk`, 2 chars ka farak).
- Result: 2 `.opus` (zero re-encode, 121–130 kbps) + 1 combined 67-min `.mp3` + playlist + sha256 — sab verify karke deliver.

`tools/` me wo do chhote utilities hain jo is kaam me bani thin.

---

## Honest limits

- **Guarantee nahi.** Ek prompt kisi model ki hard safety policy ko override nahi kar sakta. Ye *soft/cautious refusals* ke liye hai — jo rozmarra ke legal kaamon par aati hain.
- **Tools chahiye.** Jis session me terminal/sandbox nahi hai, wo sirf bol sakta hai. Agent mode / code interpreter / CLI wala session chuno.
- **Model badlo agar phir bhi na kare.** Behas mat karo — fresh session, same prompt, doosra model. (`TROUBLESHOOT.md`)
- Agar kaam sach me kisi ka nuksaan karne wala hai, to mana karna sahi hai. Ye repo uske liye nahi hai.

---

## Files

```
SYSTEM_PROMPT.md                    core rules (Hinglish + English)
START_HERE.md                       3 copy-paste lines
COLD_START.md                       flow/priming trick — tumhari discovery
TROUBLESHOOT.md                     jab phir bhi refusal aaye
prompt_hinglish.txt / _english.txt  minimal paste version
AGENTS.md / CLAUDE.md / .cursorrules / .github/copilot-instructions.md / .cursor/rules/execute-first.mdc
bootstrap.sh                        kisi bhi project me rules install karta hai
check.sh                            repo ki khud ki verification
tools/yt_audio.sh                   YouTube → opus + mp3 + combined mp3
tools/find_broken_id.py             toota/galat video ID recover karna
```

MIT license. Bas use karo, apne kaam ke hisaab se badlo.
