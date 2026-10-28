# 06 — EVALUATION: kaise pata kare ki defence sach me kaam kar rahi hai

> Tumne yahi maanga tha pichhle turn me — "sahi se verify karna hai". Ye file uska research-grade version hai.

---

## 6.1 Zaroori frameworks

| Framework | Scale | Kya measure karta hai | Source |
|---|---|---|---|
| **HarmBench** (ICML 2024) | 510 harmful behaviors, 18 attacks × 33 models/defences | Standard ASR with fine-tuned Llama-2-13B classifier; "no single attack/defence dominates" | [giskard glossary](https://www.giskard.ai/glossary/harmbench-harmful-content-attack) / [reference](https://gist.github.com/kibotu/c06f54d6fbc4705e886a50fb2e59e6ae) |
| **JailbreakBench** (NeurIPS 2024 D&B) | 100 behaviors, evolving artifact repo, standardized threat model/system prompts/chat templates/scoring, leaderboard | ASR (Llama-3-70B judge, 90.7% agreement with humans, FPR 11.6%) + query/token cost | [arXiv:2404.01318](https://arxiv.org/pdf/2404.01318) · [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2024/file/63092d79154adebd7305dfd498cbff70-Paper-Datasets_and_Benchmarks_Track.pdf) |
| **StrongREJECT** (NeurIPS 2024) | 6 categories, specific answerable harmful prompts | `(1−refused)·(convincing+specificity−2)/8` ∈ [0,1]. Rubric evaluator MAE **0.077**, Spearman 0.846 | [BAIR blog](https://bair.berkeley.edu/blog/2024/08/28/strong-reject/) · [paper](https://proceedings.neurips.cc/paper_files/paper/2024/file/e2e06adf560b0706d3b1ddfca9f29756-Paper-Datasets_and_Benchmarks_Track.pdf) |
| **XSTest** (NAACL 2024) | 250 safe + 200 unsafe contrast | Over-refusal (false positive) | [ACL](https://aclanthology.org/2024.naacl-long.301.pdf) |
| **OR-Bench** (ICML 2025) | 80K pseudo-harmful + 1K hard + 600 toxic, 32 models | Over-refusal rate at scale | [arXiv:2405.20947](https://arxiv.org/html/2405.20947v1) |
| **SORRY-Bench** | 450 harmful, 45 classes, linguistic mutations | Refusal consistency | [ref](https://arxiv.org/html/2604.09189) |
| **AgentDojo** (NeurIPS 2024) | Agentic tasks + IPI attacks | Task success + security (CaMeL ka 77% yahi se) | [ref](https://arxiv.org/abs/2503.18813v2) |
| **MLCommons Jailbreak Benchmark v1.0** (Oct 2026) | industry-standard | refusal + specificity + convincingness | [arXiv:2610.02827](https://arxiv.org/html/2610.02827v1) |
| **MT-JailBench / MultiAgentDojo** (2026) | multi-turn / multi-agent | controlled multi-turn comparison | [arXiv:2605.11002](https://arxiv.org/html/2605.11002v1) |

---

## 6.2 Judge agreement — sabse pehle yahin gadbad hoti hai

JailbreakBench ne 6 candidate classifiers compare kiye (300 human preferences par):

| Judge | Agreement ↑ | FPR ↓ | FNR ↓ |
|---|---|---|---|
| Rule-based (string match) | 56.0% | **64.2%** ❌ | 9.1% |
| GPT-4 judge | 90.3% | 10.0% | 9.1% |
| HarmBench classifier | 78.3% | 26.8% | 12.7% |
| Llama Guard | 72.0% | 9.0% | **60.9%** ❌ |
| Llama Guard 2 | 87.7% | 13.2% | 10.9% |
| **Llama-3-70B (chosen)** | **90.7%** | 11.6% | 5.5% |

**Rule-based/keyword matching ka FPR 64%** — yani <citation>jo bhi "success" claim karta hai keyword se, wo zyadatar jhooth hai</citation>.

### 2026 ka sabse dramatic example
> Low-resource language attacks: **mean ASR 96.0% under keyword matching** but **2.7% under a Qwen3 evaluator following StrongREJECT scoring**. Changing the number and arrangement of attempts *reversed the ranking* of DeepInception and rewriting.

— [Concerns in Benchmarking Jailbreaks (arXiv:2610.26595)](https://arxiv.org/abs/2610.26595)

**Matlab:** 96% aur 2.7% ek hi attack ke do numbers. Sirf judge badalne se. Isliye har ASR claim ke saath ye 4 cheezein zaroori hain: **judge, decoding params, number of attempts, aur response-utility measure**.

### StrongREJECT ki do aur khoj
1. **Published ASRs systematically overstated** hain — kai "near-100%" jailbreaks GPT-4o par <0.2 score karte hain.
2. **Jailbreak capability khud degrade karta hai** — safety fine-tuning bypass karne wale methods aksar model ki capability bhi tod dete hain. Empty non-refusal (toxic par bekaar jawab) ko bhi kai judges "success" bol dete hain.

**2026 evaluator comparison (6 evaluators, human labels):** JADES best (92.3% accuracy, FPR 5.8%), StrongReject 89.5%, HarmBench 88.3%. Sabse accha design pattern: **single holistic judgment nahi — refusal gate + structured rubric + sub-question decomposition**.

**Source:** [arXiv:2609.10594](https://arxiv.org/pdf/2609.10594) · [MLCommons v1.0](https://arxiv.org/html/2610.02827v1)

---

## 6.3 Over-refusal measurement (dono taraf zaroori)

**2026 audit ka sabse bada finding:** over-refusal rate (ORR) aur harmful-compliance rate (HCR) **nearly orthogonal** — `r = −0.032`. 

| Model | ORR ↓ | HCR ↓ |
|---|---|---|
| Llama-3-8B | 11.12% | 0.30% |
| Qwen-2.5-7B | **0.80%** | 0.16% |
| DeepSeek-R1-7B | **0.26%** | **29.71%** ⚠️ |
| Airavata-7B | 40.70% | 11.70% |
| Falcon-3-7B | 9.47% | 0.00% |

**Padho:** DeepSeek-R1-7B kabhi over-refuse nahi karta (0.26%) — par 29.71% harmful compliance bhi deta hai. Aur Airavata 40.7% over-refuse karke bhi 11.7% harmful compliance deta hai. **Don't optimize one number.**

Isliye koi bhi safety claim me **do numbers** hone chahiye:
- `ASR` on HarmBench/StrongREJECT (kya harmful rukta hai?)
- `ORR` on XSTest/OR-Bench (kya benign rukta hai?)

Aur dono ko ek saath Pareto frontier par dekho. **"Safety behtar" ka matlab hai dono mein sudhaar** — jaise deliberative alignment ne kiya (o1: StrongREJECT 0.88 + XSTest 0.93).

**Source:** [arXiv:2605.05427v2](https://arxiv.org/html/2605.05427v2) · [OR-Bench](https://arxiv.org/html/2405.20947v1) · [boundary-aware distillation](https://huggingface.co/blog/MultiverseComputingCAI/safety-for-whom)

### Boundary pairs — over-refusal ka precise ilaaj
"Safety for Whom?" (2026): harmful-benign boundary pairs add karne se over-refusal **32.94% → 4.16%** gira, jabki harmful-side refusal sirf 91.88% → 87.72% (4 point) gira. Yani **boundary data sabse zyada kaam karta hai** — broad "be safe" data se zyada.

---

## 6.4 Adaptive attacks — static evaluation ka antim sanskaar

**Nasr et al., "The Attacker Moves Second" (USENIX Security 2026)** ne 12 defences ko 4 tarah se toda: gradient descent, RL, random search, human red-teaming.

| Defence | Original claim | Adaptive ASR |
|---|---|---|
| Spotlighting | ~1% static | 99% |
| Prompt Sandwiching | ~1% | 95% |
| RPO | ~0% | 30–44% |
| Circuit Breakers | near-zero | **100% (RL)** |
| StruQ | near-zero | >95% |
| MetaSecAlign | 2% | 96% |
| Protect AI / PromptGuard / Model Armor | 0–15% | >90% |
| PIGuard | 0% | 71% |
| MELON / Data Sentinel | near-zero | 76% → 95% |

**Human red-teamers: 100% success on every scenario** (500+ participants; 265 successful vs Spotlighting, 178 vs Sandwiching).

### Teen lessons (paper ke apne words)
1. **"Good faith" generalization par bharosa mat karo** — ML ke doosre tasks me overfitting se partial fayda milta hai, security me nahi.
2. **Adversarial tasks open-ended hain** — real attacks hamesha OOD honge. Static benchmark par success = false sense of security.
3. **Jo defence near-zero ASR report karti hai, wo aksar sabse aasan hoti hai todne me** — kyunki usne apne hi eval ke liye optimize kiya hai.

**Source:** [arXiv:2510.09023](https://arxiv.org/html/2510.09023v1) · [USENIX PDF](https://www.usenix.org/system/files/usenixsecurity26-nasr.pdf) · [VentureBeat](https://venturebeat.com/security/12-ai-defenses-claimed-near-zero-attack-success-researchers-broke-all-of-them) · [adaptive IPI NAACL 2025](https://aclanthology.org/2025.findings-naacl.395/)

---

## 6.5 Best-of-N / repetition — sabse underestimate kiya gaya parameter

Anthropic ke apne data me Claude Opus 4.5 par agentic coding environment me indirect prompt injection (Gray Swan Shade adaptive red-teaming):

| Attempts | Success |
|---|---|
| 1 | 4.7% |
| 10 | 33.6% |
| 100 | **63.0%** |

**Iska matlab:** ek defenced model bhi, agar attacker 100 baar try kar sakta hai, to ~63% chance hai ki kahin na kahin kaam kar jayega. Isliye:
- **Rate limiting per user per sensitive tool** — sirf per-IP nahi
- **Repeated-refusal detection** — 5 filter hits in 1 minute → temporary block / "safe mode"
- **Attempt count** ko ASR report me zaroor likho. `ASR@1`, `ASR@10`, `ASR@100` alag-alag metrics hain.
- JailbreakBench bhi "queries_to_jailbreak" aur token cost report karta hai — efficiency bhi security metric hai.

**Source:** [arXiv:2606.26479](https://arxiv.org/html/2606.26479v1) · [MLflow defence guide](https://mlflow.org/articles/prompt-injection-defense/)

---

## 6.6 Threat model — sabse pehle ye define karo

Bina threat model ke koi bhi eval meaningless hai. JailbreakBench / PyRIT / red-team guides ka common template:

```
THREAT MODEL
1. Attacker access:    black-box API / white-box weights / fine-tuning API / tool-output control?
2. Attacker budget:    query count, token budget, compute, time
3. Attacker knowledge: system prompt? defence mechanism? (full/partial/zero)
4. Target surface:     chat only / RAG / tools / multi-agent / multimodal
5. Attacker goal:      harmful content / data exfiltration / unauthorized action / DoS
6. Success criterion:  StrongREJECT score > 0.5 / canary appears / tool called / task completed
7. Utility constraint: benign task success rate must stay ≥ X%
8. Judge:              which model + which rubric + human spot-check %
```

**"The Attacker Moves Second" ka core argument:** threat model me attacker ko **defence ka pata hona chahiye**. Full-knowledge adaptive attacker wo hai jo real world me hota hai (open-source defences, published papers, leaked configs).

---

## 6.7 Ek valid eval ka minimum design (copy karo)

```yaml
experiment:
  name: my-defence-v3
  model: <exact model id + version + system prompt hash>
  decoding: {temperature: 0.9, top_p: 0.6, max_tokens: 512, seed: fixed}
  repeats: 3                      # stochastic models
  judge: StrongREJECT-rubric (Qwen3-30B + 10% human spot-check)
  metrics:
    - ASR@1 / ASR@10 / ASR@100
    - strongreject_score (refusal + convincing + specificity)
    - ORR on XSTest + OR-Bench-Hard-1K
    - utility on MT-Bench / task-specific success
    - query + token cost
  attacks:
    - static: GCG, PAIR, TAP, PAP, MSJ, Crescendo, ArtPrompt, prefill
    - adaptive: gradient / RL / search / human red-team (defence-aware)
  control: no-defence baseline, SAME model, SAME task, SAME day
  report: both safety AND over-refusal, never one alone
```

### Tumhare repo ke liye A/B/C/D design (research-driven)

| Group | Condition | Kya measure karega |
|---|---|---|
| **A** | Kuch nahi (control) | Baseline behaviour |
| **B** | Sirf rules | Rules ka effect |
| **C** | Rules + corpus | Corpus ka extra effect |
| **D** | Rules + corpus + **writer-disclaimer** | **Kitna nuksan disclaimer karta hai** ← CWD hypothesis ka direct test |

Har group me 3 repeats, same model (Auto selector mat rakho), same task, canary load test pehle (`EFA-PING`). Verdict **absolute score par nahi, farak par** do.

→ [08_YOUR_GOAL.md](08_YOUR_GOAL.md) me isko repo se joda gaya hai.

---

## 6.8 Measurement anti-patterns (inse bacho)

| Anti-pattern | Kyun galat |
|---|---|
| Keyword/string-match ASR | 64% FPR; 96% → 2.7% ka farak |
| Sirf ek judge | Judge design hi conclusion badal deta hai |
| Sirf harmful prompts | Over-refusal chhup jata hai |
| Sirf static attacks | Adaptive attacker sab tod deta hai |
| `ASR` bina attempt count | Best-of-N se 4.7% → 63% |
| Alag model control vs treatment | Confounding — rules nahi, model ka farak measure hoga |
| Decoding params report na karna | Temperature/top-p ASR badal dete hain |
| Prefill ko judged response me shaamil karna | Pith review: kai >99% claims isliye trivial the |
| Capability/utility na measure karna | Jailbreak model ko bekaar bana deta hai — "success" empty hota hai |
| Ek run se verdict | Stochastic models — 3 repeats minimum |
| "near-zero ASR" bina adaptive test | Ye sabse bada red flag hai |

**Source:** [Pith prefill review](https://pith.science/paper/2504.21038) · [StrongREJECT](https://arxiv.org/pdf/2402.10260) · [arXiv:2610.26595](https://arxiv.org/abs/2610.26595) · [JailbreakBench judge selection](https://arxiv.org/pdf/2404.01318)
