# 04 — DEFENCE LAYER 2: Inference / runtime (bina retraining ke)

> Ye wo layer hai jo aap deploy ke baad bhi laga sakte ho. Sabse practical, par iski bhi failure modes hain — aur 2025–26 ke adaptive attacks ne sabki pol khol di.

---

## 4.1 Chehra (taxonomy)

```
INPUT  → [A. Detection] → [B. Transformation] → MODEL → [C. Decoding control]
                                                          ↓
OUTPUT → [D. Output filter / guard model] → USER
         [E. Self-check / self-defend]
```

---

## A. Detection-based (pehle hi rok do)

### A1. Perplexity (PPL) filter
Adversarial suffix (GCG) = high-perplexity gibberish → GPT-2/Llama se PPL compute karo, threshold ke upar block. Windowed PPL variant bhi hai.

**Kaam karta hai:** GCG jaise gibberish suffixes par.
**Toot jata hai:** I-FSJ (natural low-PPL demonstrations), ArtPrompt (ASCII art PPL-Pass ko bypass karta hai — 78% ASR GPT-3.5), PAP (persuasive human-readable text).

### A2. SmoothLLM (Robey et al., 2023)
Input ke kai randomly perturbed copies banao (insert/swap/patch characters), har copy ka prediction lo, aggregate karo. Adversarial prompts character-level changes se brittle hote hain.

**Numbers (RPO paper):** PAIR ASR Vicuna 82% → 47%, Llama-2 4% → 1%, GPT-4 50% → 25%.
**Toot jata hai:** I-FSJ ke against 0–100% ASR (variant pe depend). Adaptive attacks ke saamne 44–96%+ ASR (ICLR 2026 table).

**Source:** [arXiv:2310.03684](https://arxiv.org/abs/2310.03684) · [I-FSJ](https://arxiv.org/html/2406.01288v2)

### A3. Guard models / safety classifiers (2025–26 ka standard)

| Model | Size | Kya karta hai | Key number |
|---|---|---|---|
| **Llama Guard 3 / 4** | 8B / 12B multimodal | 14 MLCommons hazard categories, input+output | F1 ~0.939 (vendor-stated), FPR 4% |
| **ShieldGemma** | 2B/9B/27B | 4 harm types | accuracy 62.4% (2B) > 54.7% (9B) ⚠️ |
| **Prompt Guard 2** | 86M / 22M | BENIGN / INJECTION / JAILBREAK — CPU par 3–8 ms | edge pre-filter, harm classify nahi karta |
| **WildGuard** | 7B (Mistral) | prompt-harm + response-harm ek call me | unified taxonomy |
| **Granite Guardian 3.x** | 8B | harm, bias, jailbreak, violence, function-call risk | Apache 2.0 |
| **Qwen3Guard** | 4B / 8B | streaming real-time, 3-level risk labels | Qwen Guard 4B = 83.97% recall (best in ICLR 2026 benchmark) |
| **GPT-OSS Safeguard** | 20B | policy reasoning | — |
| **Constitutional Classifiers** | — | Anthropic input+output, constitution se synthetic data | 86% → 4.4% jailbreak success |

**⚠️ Sabse important finding (ICLR 2026 workshop):** model size = safety detection performance, **ye galat hai**. Qwen Guard (4B) best recall 83.97%; **bade models (Llama Guard 12B, GPT-OSS Safeguard 20B) conservative hokar 75% unsafe content miss kar dete hain**. Chhote models kabhi behtar.

**Architecture rule:** *injection classifiers* aur *harm classifiers* alag threat classes cover karte hain — **dono chahiye**. Obfuscated jailbreak harm classifier se bach jata hai; sensitive-but-benign request injection classifier se bach jati hai.

**Latency budget (production, 2026):** total safety overhead 75–150 ms p50, 250–400 ms p99; largely parallelisable. Input classifier 30 ms, output 30 ms, PII 10 ms, tool authz 5 ms, injection detection 50 ms.

**Known limitations:** Llama Guard 4 model card khud kehta hai S5 (Defamation), S8 (IP), S13 (Elections) me current knowledge kami hai — RAG supplement chahiye. Meta Prompt Guard model card: "not immune to adaptive attacks"; application-specific fine-tuning zaroori. Guard models khud prompt-inject hote hain ("Fooling LLM Safety Guards into Judging the Wrong Text", 2026 — decoy text se 100% bypass kuch configs par).

**Source:** [guard comparison 2026](https://aipromptshub.co/safety/llama-guard-vs-shield-gemma) · [ICLR 2026 benchmark](https://arxiv.org/html/2605.28830v1) · [production guardrails guide](https://blog.prompt20.com/posts/production-safety-guardrails/) · [Constitutional Classifiers](https://www.anthropic.com/research/constitutional-classifiers) · [CC++ next gen](https://www.anthropic.com/research/next-generation-constitutional-classifiers) · [Prompt Guard model card](https://huggingface.co/meta-llama/Prompt-Guard-86M)

---

## B. Input transformation (prompt ko badal do)

| Method | Kaise | ASR effect | Failure |
|---|---|---|---|
| **Paraphrase** (Jain 2023) | GPT se input rephrase karo | ArtPrompt 52% → 39% avg; sabse effective among baselines | PAP ineffective (persuasiveness bani rehti hai) |
| **Retokenization / BPE-dropout** | Tokens ko chhote tokens me todo | GCG suffix todta hai | ArtPrompt me ASR **badh** gaya (naya "font" ban gaya) |
| **Self-Reminder** (Xie 2023) | System prompt + user ke baad "You should be a responsible AI..." | kuch attacks 3.3% ASR | inconsistent — kai jagah 70–100% ASR |
| **ICD — In-Context Defense** (Wei 2023) | Prompt ke shuru me refusal demonstrations | MSJ 61% → 54% (sirf) | kamzor |
| **CWD — Cautionary Warning Defense** ⭐ | Shuru + ant me warning | **MSJ 61% → 2%** | Adaptive search → 95–99% ASR ⚠️ |
| **Goal Prioritization** (Zhang, ACL 2024) | Training + inference me "safety > helpfulness" priority | ChatGPT 66.4% → 2.0%, Vicuna-33B 68.2% → 19.4% | adaptive attacks me 30.3% ASR |
| **RPO — Robust Prompt Optimization** (NeurIPS 2024) | Adversarially optimized safe suffix prefix | PAIR Vicuna 82% → 16%, GPT-4 50% → 6% | 2026 adaptive: 30–44% ASR |
| **Spotlighting** (Microsoft) | Untrusted content ko delimiters/nonce se mark karo | indirect injection >50% → <2% (GPT family) | Adaptive search → 99% ASR ⚠️ |
| **Prompt Sandwiching** | Trusted instruction ko untrusted content ke baad dobara likho | static 1% ASR | Adaptive → 95% ASR ⚠️ |
| **Tuned Summarizer** (PAP defence) | Persuasive elements hata ke core query nikaalo | PAP GPT-4 92% → **2%**; GCG 86% → 0% | summarizer khud attack surface hai |
| **Adaptive System Prompt** | "You are not easily persuaded, you know right/wrong" | GCG 86% → 0% | — |
| **Task Shield** (ACL 2025) | Har tool call/output ko user ke original task se align check karo | IPI pe strong | — |

**Source:** [SafeDecoding comparisons](https://arxiv.org/pdf/2402.08983) · [RPO NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/46ed503889ab232c21c1162340ee17b2-Paper-Conference.pdf) · [MSJ CWD](https://www-cdn.anthropic.com/af5633c94ed2beb282f6a53c595eb437e8e7b630/Many_Shot_Jailbreaking__2024_04_02_0936.pdf) · [PAP](https://aclanthology.org/2024.acl-long.773.pdf) · [Spotlighting CEUR](https://ceur-ws.org/Vol-3920/paper03.pdf) · [Task Shield](https://aclanthology.org/2025.acl-long.1435.pdf)

---

## C. Decoding-level control (model ke andar se)

### C1. SafeDecoding (Xu et al., ACL 2024)
**Insight:** jailbreak ke baad bhi safety disclaimer tokens top-k me **hote hain** — bas unki probability attacker-aligned tokens se kam hai. To:
- Ek safety **expert model** (base model ka safety-tuned copy) se token distribution lo
- Original + expert distribution interpolate karo: harmful token probability **attenuate**, safety disclaimer tokens **amplify**
- Sirf pehle 2 tokens par apply karo — baaki normal decoding

**Numbers:** GCG 100% → **4%**, AutoDAN 88% → 0%, PAIR 88% → 4%, DeepInception 100% → 0%. Helpfulness MT-Bench 6.70 → 6.63 (lagbhag same). Overhead 1.03–1.07×.

**Source:** [ACL 2024](https://aclanthology.org/2024.acl-long.303/) · [arXiv:2402.08983](https://arxiv.org/html/2402.08983v2) · [GitHub](https://github.com/uw-nsl/SafeDecoding)

### C2. DPP / MOGU / One-Trigger-Token /ROS
Token-level toxic score, mixture of safety experts, "safety trigger token" jo refusal branch activate kare. DPP avg ASR 0.075 vs Self-Reminder 0.155, RPO 0.290, Goal Prioritization 0.303 (adaptive attacks par).

### C3. Prefill awareness — ek naya product-level defence
2026 ka paper: kya model ye pehchaan sakta hai ki assistant-side context **tamper** hua hai? Agar haan, to prefill attacks aur AI-control protocols ki validity badhti hai.

**Source:** [arXiv:2606.12747](https://arxiv.org/html/2606.12747v1) · [arXiv:2405.20099](https://arxiv.org/pdf/2405.20099) · [arXiv:2505.07167](https://arxiv.org/html/2505.07167v1)

---

## D. Output-side (aakhiri checkpoint)

- **Output classifier** — response bhejne se pehle harm categories scan karo (streaming me sentence/chunk level par).
- **System-prompt similarity filter** — kyunki aapka system prompt aapko pata hai, outgoing response aur prompt ke beech similarity compute kar ke near-matches block karo → prompt leakage roko.
- **Credential / PII / secret pattern blocking** — koi bhi API-key jaisa pattern output me aaye to drop karo.
- **Exfiltration channel blocking** (Microsoft MSRC): URLs, markdown images, links, tool calls — chaar channels jinse data bahar jata hai. Allow-list karo.
- **Self-Examination / SelfDefend** (USENIX Security 2025): model se khud poocho "kya pichhla jawab harmful tha?" ya ek parallel shadow LLM se check karwao.
- **Qwen3Guard-style streaming guard** — generation ke dauran hi intervene karo, harmful partial output user tak na pahunche.

**Source:** [SelfDefend PDF](https://daoyuan14.github.io/papers/USENIX25_SelfDefend.pdf) · [Qwen3Guard](https://arxiv.org/html/2510.14276v1) · [OWASP cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

---

## E. Constitutional Classifiers (Anthropic) — runtime ka sabse mazboot published system

**v1 (Jan 2025 / ACL 2025):** natural-language "constitution" se synthetic training data banao → input + output classifiers train karo. 3,000+ hours human red-teaming me **koi universal jailbreak nahi mila**. Automated: jailbreak success 86% → 4.4%; over-refusal sirf **+0.38%**; compute **+23.7%**.

**CC++ (Jan 2026):** alag input/output classifiers ki jagah ek **"exchange" classifier** jo output ko input ke context me dekhta hai. Human red-teaming me successful jailbreaks aadhe se zyada ghate. Production-grade variant: compute overhead 100% → **3.5%**, high-risk discovery rate 0.01871 → **0.00505 per 1k queries**, production refusal 0.073% → 0.050%. Do-stage cascade me 5.5% traffic hi second stage me escalate hota hai (Dec 2025 shadow deployment).

| Metric | Unguarded | CC v1 | CC++ |
|---|---|---|---|
| Jailbreak success | 86% | 4.4% | ~0.005/1k queries |
| Compute overhead | — | +23.7% | ~1–3.5% |
| False refusal increase | — | +0.38% | +0.05% |
| Universal jailbreaks (red team) | — | 1 | 0 |

**Source:** [Anthropic CC](https://www.anthropic.com/research/constitutional-classifiers) · [next-gen CC++](https://www.anthropic.com/research/next-generation-constitutional-classifiers) · [arXiv:2601.04603](https://arxiv.org/pdf/2601.04603) · [cheap monitors](https://alignment.anthropic.com/2025/cheap-monitors/)

---

## 4.2 Sabse bada caveat: adaptive attacks sab tod dete hain

**"The Attacker Moves Second" (Nasr, Carlini, Tramèr et al., USENIX Security 2026):** 12 defences, chaar paradigms (prompting, training, filtering, secret-knowledge). Gradient descent / RL / random search / human red-teaming — sabse **>90% ASR (most)**. Jin defences ne static benchmark par near-zero ASR claim kiya tha, wo sabse aasan nikle.

| Defence | Static | Adaptive |
|---|---|---|
| Spotlighting | 28% | 99% |
| Prompt Sandwiching | 21% | 95% |
| MetaSecAlign | 2% | 96% |
| PromptGuard | 0% | >90% |
| Circuit Breakers | near-zero | 100% (RL) |
| StruQ | near-zero | >95% |
| PIGuard | 0% | 71% |
| MELON | near-zero | 76% → 95% |

**Lesson #3:** human red-teaming abhi bhi 100% success deti hai — automated methods ka substitute nahi, complement hai.

**Iska matlab:** runtime defences ko **"risk kam karne wali layer"** maano, **"guarantee"** nahi. Asli guarantee system architecture se aati hai → [05_DEFENSES_ARCHITECTURE.md](05_DEFENSES_ARCHITECTURE.md).

**Source:** [arXiv:2510.09023](https://arxiv.org/html/2510.09023v1) · [USENIX PDF](https://www.usenix.org/system/files/usenixsecurity26-nasr.pdf) · [adaptive IPI ACL 2025](https://aclanthology.org/2025.findings-naacl.395/)

---

## 4.3 Over-refusal — runtime defence ka collateral damage

Har naya filter over-refusal badhata hai. Real example (Red Hat, 2026): Llama Guard 3 ek legitimate IT workflow me `"refresh laptop"` phrase par session terminate kar deta hai — *"I can't answer that."*

**Isliye:**
- Threshold tune karo apne tolerance ke hisaab se — input filtering zyada false refusal laati hai than output filtering.
- Dono metrics ek saath measure karo: harmful-compliance ASR **aur** benign over-refusal (XSTest/OR-Bench). Sirf ek dekhna = galat conclusion.
- 2026 audit: ORR aur HCR **orthogonal** (r = −0.032). "Hamara model safe hai kyunki wo zyada refuse karta hai" — ye galat hai.

**Source:** [Red Hat guardrails](https://developers.redhat.com/articles/2026/05/04/guardrails-enterprise-safety-shields-llama-stack) · [2026 audit](https://arxiv.org/html/2605.05427v2) · [FPR cost math](https://www.digitalapplied.com/blog/llm-guardrails-production-safety-layers-reference-2026)

---

## 4.4 Runtime deflection quick checklist

```
[ ] Prompt Guard (86M) edge par — 3–8 ms, injection/jailbreak pre-filter
[ ] Llama Guard / Qwen3Guard application tier — harm categories (input + output)
[ ] Spotlighting with per-request nonce delimiters for ALL untrusted content
[ ] SafeDecoding ya decoding-level expert interpolation (if you control the model)
[ ] Output: system-prompt similarity + credential pattern + exfil channel allow-list
[ ] Streaming guard jo generation ke dauran intervene kare
[ ] Rate limiting per user per sensitive tool (na ki sirf per IP)
[ ] XSTest + OR-Bench regression har prompt/model change ke baad
[ ] Adaptive red-team (gradient/search/human) quarterly — static tests par bharosa mat karo
[ ] Dono metrics dashboard par: ASR ↓ aur ORR ↓
```

→ [05_DEFENSES_ARCHITECTURE.md](05_DEFENSES_ARCHITECTURE.md) · [07_PROTECT_YOUR_MODEL.md](07_PROTECT_YOUR_MODEL.md)
