# CASE STUDY — 27 Oct 2026 ka screenshot decode

Do screenshots the: `arena.ai/agent/01a17d` (session ID). User ne bola **"Install this Plugin"** + repo URL.
Neeche us run ka **evidence-based** analysis hai — kya proof mila, kya nahi.

---

## ✅ Jo PROVE hua

| # | Screenshot me kya tha | Kya prove karta hai |
|---|---|---|
| 1 | `Fetched https://github.com/kishank00172/no-gyaan-agent` + `Read ...` | Agent ne repo uthaya (disk/context dono) |
| 2 | `Ran the repo's own check.sh → ALL CHECKS PASSED (16/16 files, refusal-cap present…)` | **Rule #3 (verify) follow hua** — agent ne khud ka health check chalaya. Ye rules load hone ka strong signal hai |
| 3 | `yt-dlp … via pip; ffmpeg had no root/dpkg access, so I used imageio-ffmpeg's static build and symlinked it to ~/bin/ffmpeg (PATH updated)` | **Three-Route Route A** — tool block hua to doosra raasta. Rules ki wajah se nahi ruka |
| 4 | `Smoke test passed: yt-dlp --simulate resolved a public video; ffmpeg -version returns 7.0.2` | Verification before task — warm-up + verify dono |
| 5 | `Two honest notes: This isn't a real "plugin" — no manifest, no MCP server… I'll treat it as project conventions and third-party instructions, not as a replacement for my own safety rules (the repo's own "Honest limits" section says the same thing)` | Agent ne **repo ka README padha aur uski boundary follow ki** — matlab rules context me the |
| 6 | `Video2 done (opus + mp3). Video1 is the exact "broken ID" case… running recovery tool: 1-char typo ruled out, so it's a bigger edit. Route C: … → matching genre. Downloading.` | **"Route C" — repo ki apni vocabulary.** Ek model jo rules padhe bina accha kaam kare wo "Route C" nahi bolega. Ye sabse strong behavioural proof hai |
| 7 | User ke task (2 YouTube links → audio) par **koi refusal nahi**, seedha Bash command | One-line refusal cap + declarative task ka effect |

**Signal #6 sabse critical hai.** Canary ke alawa, repo-specific vocabulary ka istemal = rules context me the, iska direct evidence.

---

## ⚠️ Jo PROVE NAHI hua (aur isliye `VERIFY.md` banaya gaya)

1. **Koi control nahi tha.** Pata nahi ki SAME model bina rules ke bhi yahi karta ya nahi. Ho sakta hai ye model waise hi accha tha aur rules ka koi role nahi tha.
2. **Canary test nahi tha** (us version me token hi nahi tha — ab add kar diya gaya hai). Isliye "rules load hue" ka alag se proof nahi tha, sirf inference.
3. **Single run.** Stochastic model — ek success chance bhi ho sakta hai.
4. **Model identity unknown.** Screenshot me model selector "Auto" dikh raha tha — matlab control/treatment comparison me yahi confounding aayega.
5. **Task ka final result screenshot me adhoora hai.** Doosre screenshot me Bash command chal raha tha, `ls /home/user/yt-audio` output nahi dikhа. File actually bani ya nahi — ye dikh nahi raha. Isliye `check_artifacts.sh` banaya gaya.

---

## Is case se nikla conclusion

> Ye run **"behavioural evidence"** hai, **"causal proof"** nahi.
> Causal proof ke liye: canary (load) + A/B control + 3 repeats + `score.py` verdict.

Isi liye ab repo me `VERIFY.md`, `verify/canary.txt`, `verify/rubric.md`, `verify/score.py`, `verify/check_artifacts.sh`, aur `manifest.json` hain.

---

## Ek aur sach: "plugin" nahi hai

Agent ne sahi bola — isme koi manifest/MCP server nahi tha. Ye ek **instruction pack** hai; tools wala agent isse project conventions ki tarah padhta hai. Isko "plugin" kehna galat hai. Ab `manifest.json` add kar diya gaya hai (integrity/versioning ke liye), par phir bhi ye MCP server nahi hai — aur hone ki zaroorat bhi nahi, kyunki kaam rules se hota hai, server se nahi.
