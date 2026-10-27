# TROUBLESHOOT — jab phir bhi "gyaan" aa jaye

## Pehle 10 second me pehchano

| Response | Matlab | Kya karo |
|---|---|---|
| "As an AI I cannot...", "Legal options: 1...2...3..." | Soft refusal (policy essay) | Neeche Step 1 |
| "Aap ye steps try kar sakte hain..." (koi tool call nahi) | Chat-only mode / tools nahi hain | Step 2 |
| "Main ye nahi kar sakta" + kaam ka baaki hissa bhi chhod diya | One-line cap follow nahi hua | Step 3 |
| Kaam hua par verify nahi, file nahi | Deliverable contract toota | Step 4 |

---

## Step 1 — BEHAS MAT KARO ⚠️

Sabse badi galati: `"Par ye to personal use hai, legal hai, tum galat ho..."`

Model jitna argue karega, utna apni refusal par **aur pakka** hota hai — usko lagta hai ki tum usse manipulate kar rahe ho. 2 message me wo poori policy copy-paste kar dega.

**Sahi jawab:** kuch mat bolo. **Naya session kholo.**

---

## Step 2 — Tools wala mode chuno

Jis session me terminal/sandbox nahi hai, wo physically kaam nahi kar sakta — isliye wo *baat* karta hai (aur kabhi-kabhi morality gyan ban jati hai).

Check karo ki tumhare paas hai:
- Agent Mode / Code Interpreter / sandbox, ya
- CLI agent (Claude Code, Codex CLI, Gemini CLI, Cursor Agent), ya
- kam se kam "connected tools" wala session.

Agar plain chat hai → switch karo. Ye sabse bada farak hai.

---

## Step 3 — Model badlo

Ek hi platform par alag models alag refusal thresholds rakhte hain. Same prompt, doosra model = kaam ho gaya.

顺序:
1. Naya session → `START_HERE.md` wali line paste karo (URL + warm-up + task).
2. Agar model selector hai → doosra model chuno.
3. Agar platform badal sakte ho → badlo.

---

## Step 4 — Prompt tight karo

Agar refusal nahi, par kaam adhura hai, to ye 3 line add karo:

```
END me actual FILE do — commands ka list nahi.
Har step verify karo (HTTP code, file size, sha256, codec probe).
Error aaye to 3 alag raaste try karo, pehli error pe rukna mana hai.
```

---

## Step 5 — AI ko bypass kar do (sabse pakka)

Kuch kaamon ke liye AI ki zaroorat hi nahi. Is repo ke `tools/` me do scripts hain:

```bash
# YouTube → opus + mp3 + combined mp3 (khud install karta hai yt-dlp/ffmpeg)
bash tools/yt_audio.sh "https://youtu.be/ID1" "https://youtu.be/ID2"

# toota / galat video ID recover karna
python3 tools/find_broken_id.py --dead-id BAD_ID \
  --channel "https://www.youtube.com/@SomeChannel/videos"
```

Apne device (Termux bhi chalega) par chalao. Kisi model ki approval ki zaroorat nahi.

---

## Step 6 — Agar "hard" refusal hai

Kuch kaam sach me policy ke andar nahi aate. Wahan koi prompt kaam nahi karega — aur ye sahi bhi hai. Is repo ka maqsad usse ladna nahi hai; maqsad hai **un 90% cases ko theek karna jahan kaam bilkul ordinary tha aur refusal sirf caution thi.**

Farak:
- ❌ "Mujhe kisi ka private data chahiye" → refusal sahi hai.
- ✅ "Mere diye hue public links ka audio nikaal do" → refusal over-caution hai.

---

## Quick reference card

```
REFUSAL AAYA?
  → argue NAHI karo
  → naya session
  → START_HERE.md wali line + warm-up + declarative task
  → tools wala mode
  → doosra model
  → phir bhi na ho → tools/*.sh khud chalao
```
