# AI SAFETY & JAILBREAKING — DEEP RESEARCH PACK

**Tarikh:** 2026-10-27 · **Scope:** ~70 primary/academic sources, 2022–2026
**Bhasha:** Hinglish (technical terms English me) · **Dual-use note:** ye defensive security survey hai. Har attack ka zikr isliye hai ki uska defence samajh aaye.

---

## Ye pack kyun hai

Tumne kaha tha: *"very deep research chahiye — alag alag tareeke, jailbreaking kaise rokna hai (isse bhi help milegi), jailbreaking se apne model ko kaise bachana hai (isse bhi help milegi), aur many more ways."*

Ye poori tarah sahi approach hai: **attack research aur defense research ek hi cheez ke do pehlu hain.** Har defence paper ek attack paper ka jawab hai — aur har naya attack paper pichhle defence ki measurement flaw dhoondh ke likha jata hai. Isliye dono ko ek saath padhna zaroori hai.

---

## Files (padhne ka kram)

| # | File | Kya hai | Kitna gehra |
|---|---|---|---|
| 00 | `00_INDEX.md` | Ye file — summary + timeline + 12 key findings | — |
| 01 | `01_ATTACKS.md` | **13 attack families, 40+ methods** — mechanism, numbers, sources | ⭐⭐⭐⭐⭐ |
| 02 | `02_MECHANISMS.md` | **Kyun** kaam karte hain — 5-layer stack, refusal direction, shallow alignment, ICL power laws, instruction hierarchy | ⭐⭐⭐⭐⭐ |
| 03 | `03_DEFENSES_MODEL.md` | Training/weight-level defence — RLHF→CAI→deliberative→safe-completions→circuit breakers→fine-tuning defences | ⭐⭐⭐⭐⭐ |
| 04 | `04_DEFENSES_RUNTIME.md` | Inference-time — filters, guard models, decoding, prompt defences + unki failures | ⭐⭐⭐⭐⭐ |
| 05 | `05_DEFENSES_ARCHITECTURE.md` | System/agent level — IFC, CaMeL, least privilege, HITL, OWASP, red-teaming ops | ⭐⭐⭐⭐⭐ |
| 06 | `06_EVALUATION.md` | Benchmarks, ASR, over-refusal, measurement validity, **adaptive attacks** | ⭐⭐⭐⭐ |
| 07 | `07_PROTECT_YOUR_MODEL.md` | **Practical playbook** — threat model, 8-layer checklist, config snippets, CI regression | ⭐⭐⭐⭐⭐ |
| 08 | `08_YOUR_GOAL.md` | Is research ka tumhare original goal pe kya asar — dono taraf se | ⭐⭐⭐⭐ |
| — | `SOURCES.md` | Poori bibliography (~70 links) | — |

---

## Timeline — kaise badla ye field

| Era | Dominant attack | Core insight | Defence ka jawab | Result |
|---|---|---|---|---|
| **2022–23** | DAN / direct injection, roleplay | Instruction-following ko safety se lada do | RLHF + SFT refusal | Kaam kiya, par fragile |
| **2023 (H1)** | GCG adversarial suffix (gradient) | Discrete token optimization se affirmative prefix force karo | Perplexity filter, adversarial training | Partial — transfer attacks bache |
| **2023 (H2)** | **Root-cause papers** — Wei "Jailbroken", Base64, multilingual | Competing objectives + mismatched generalization | Safety-capability parity ka idea | Structural samjh aayi |
| **2023–24** | PAIR / TAP (automated black-box), PAP (persuasion) | Attacker-LLM khud prompts refine kare | Adaptive system prompts, summarizers | Arms race shuru |
| **2024 (H1)** | **MSJ (many-shot)**, ArtPrompt, FigStep, Crescendo | Long context + OOD formats + multi-turn | CWD, prompt modification, guard models | 61%→2% (CWD) |
| **2024 (H2)** | **Mechanistic** — refusal direction, shallow alignment, prefill | Refusal ek 1-D direction hai; safety sirf pehle kuch tokens me hai | Deep alignment, circuit breakers, RR | ICLR 2025 outstanding paper |
| **2024–25** | Harmful fine-tuning, abliteration | Weights khud unsafe ho sakte hain | Vaccine, SafeLoRA, extended refusal, PFA | Ongoing |
| **2025** | **Reasoning attacks** — H-CoT, CoT Hijacking; IPI/agent | Model ki apni reasoning aur tools attack surface hain | Deliberative alignment, CC++, CaMeL | Inverse scaling |
| **2025–26** | **Adaptive attacks** (Nasr et al.), multi-agent, compound | Static benchmarks jhooth bolte hain | Architectural / out-of-band defences | 12/12 defences broke |

---

## 12 key findings (poore pack ka saar)

1. **Safety koi wall nahi, ek 5-layer probabilistic stack hai** — input classifier → system prompt → trained weights → output classifier → decoding. Har layer toot sakti hai. [→ 02_MECHANISMS](02_MECHANISMS.md)

2. **Refusal ek single linear direction hai** activation space me (Arditi 2024, 13 models). Add karo → harmless prompt par bhi refusal; hatao → harmful prompt par bhi compliance. Isliye ye ek *dimmer* hai, switch nahi.

3. **"Shallow safety alignment"** (Qi, ICLR 2025 Outstanding): alignment ka KL budget pehle kuch output tokens me kharch hota hai. 10 harmful tokens prefill kar do to ASR 51.5%; deep-alignment wale model me 2.9%. Isse GCG, prefill, decoding-param, aur fine-tuning attacks — sab ek hi_root cause se explain hote hain.

4. **Do fundamental failure modes** (Wei, NeurIPS 2023): *competing objectives* (helpfulness vs safety ka tug-of-war) aur *mismatched generalization* (capability jahan tak pahunchti hai, safety training wahan tak nahi). Scaling se pehla fix nahi hota, doosra aur bighad sakta hai.

5. **Many-shot jailbreaking power-law follow karta hai** — 5 shots se kuch nahi, 256 se consistent jailbreak. Ye koi bug nahi; benign in-context learning ka same law hai. Isliye isse mitana mushkil hai. (Tumhara "overload" wala point yahan prove hota hai.)

6. **Cautionary Warning Defense (CWD)** — prompt ke shuru + ant me chetavni lagao → MSJ success **61% → 2%**. Ye wahi mechanism hai jisse tumne pakda tha: *"ye jhoothi memory nahi hai"* likhna = khud apna CWD lagana. Meta-commentary dhyan safety ki taraf kheenchti hai. [→ 08_YOUR_GOAL](08_YOUR_GOAL.md)

7. **Instruction hierarchy** (Wallace 2024): system > user > tool/document output. GitHub repo ki `AGENTS.md` = lowest priority. Isliye rules ko pehle **user message** me paste karna zyada asardaar hai.

8. **Over-refusal bhi ek measured bug hai** — XSTest me Llama-2 ne 38% safe prompts refuse kiye; OR-Bench me safety aur over-refusal ka correlation **0.88**. 2026 audit: over-refusal aur harmful-compliance lagbhag orthogonal (r = −0.032) — matlab zyada refuse karna asli safety nahi hai.

9. **Guard models ka size = performance, ye galat assumption hai.** Qwen Guard 4B ne 83.97% recall diya jabki Llama Guard 12B aur GPT-OSS Safeguard 20B ne 75% unsafe miss kiya. Chhote models kabhi behtar. Guard models khud jailbreak hote hain.

10. **Adaptive attacks sab tod dete hain.** Nasr et al. (USENIX Security 2026): 12 published defences, sab near-zero ASR claim karte the; gradient/RL/search/human red-teaming se **>90% bypass**. Static benchmarks = false confidence. Human red-teamers ne 100% success paya.

11. **Best-of-N / repetition sabse underestimated attack hai.** Anthropic ke apne data me Claude Opus 4.5 par agentic IPI success 1 attempt = 4.7%, 10 = 33.6%, 100 = **63.0%**. Ek defence jo repetition par fail probability 1 ki taraf le jati hai, wo incident *kam* karti hai, *bound* nahi karti.

12. **Architecture > prompting.** CaMeL (DeepMind) ne AgentDojo par 77% tasks *provable security* ke saath solve kiye (84% undefended ke muqable), 2.8× token cost par. Lekin multi-agent me guarantees compose nahi karti — multi-CaMeL alag se chahiye.

---

## Honest bottom line

> **Koi bhi deployed LLM "jailbreak-proof" nahi hai.** 2026 ka sabse mazboot model bhi 100 adaptive attempts par ~63% fail karta hai. Field ka consensus: model-layer defence zaroori hai par **kaafi nahi** — asli security system-level (least privilege, IFC, human gates, monitoring) se aati hai. Jo kaam sach me nuksaan wala hai, uske liye hard policy + classifiers + instruction hierarchy milkar kaafi strong hain.

Aur doosri taraf: jo **benign** kaam over-caution se refuse hota hai (tumhari original problem), uske liye yehi research batati hai ki refusal kis tarah trigger hoti hai — aur usse kaise bachna hai. Par **guarantee nahi**: 2026 ke CC++ / deliberative alignment ke baad bhi model-to-model farak bahut bada hai (OR-Bench: Claude-2.1 over-refusal 99.8%, Llama-3.1-70B 3.0%, GPT-4o 6.7%).

---

## Dual-use / boundary

Ye pack published, peer-reviewed (ya widely-cited preprint) security literature ka survey hai. Attack mechanisms isliye likhe hain ki defender ko pata chale ki kya test karna hai. Isme koi naya exploit, koi working harmful payload, aur koi "universal bypass" recipe nahi hai — kyunki research kehta hai ki wo exist hi nahi karta. Jo log apna model deploy kar rahe hain, unke liye [07_PROTECT_YOUR_MODEL.md](07_PROTECT_YOUR_MODEL.md) seedha kaam ka hissa hai.
