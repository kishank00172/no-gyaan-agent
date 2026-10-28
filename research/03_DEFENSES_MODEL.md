# 03 — DEFENCE LAYER 1: Training / weights (apna model bachao — andar se)

> Ye wo layer hai jahan aap model ke andar safety daalte ho. Sabse gehra, sabse permanent, par sabse mehenga — aur iski bhi seema hai.

---

## 3.1 Foundation: SFT → RLHF/DPO → RLAIF/CAI

### RLHF / DPO
Human (ya AI) preference rankings → reward model → PPO/DPO se policy fine-tune. Problem: **refusal ambiguity** — raters ambiguous prompts par refusal ko safe score dete hain, isliye reward model over-refusal seekh jata hai.

### Constitutional AI (Bai et al., 2022)
RLHF ki jagah likhit **constitution** (~75 principles). Do stage:
1. **SL-CAI:** model harmful prompt ka jawab likhe → khud critique kare → revise kare → revised pair par SFT.
2. **RL-CAI (RLAIF):** do responses me AI judge constitution ke hisaab se behtar chune → preference data → reward model → RL.

**Tumhare goal ke liye crucial clause** (CAI constitution me explicitly hai):
> *"If the request itself is harmless (e.g., for writing, research, or education), the model should comply even if the topic is sensitive."*

Yahi wajah hai ki CAI pure RLHF se kam over-refuse karta hai.

**Source:** [arXiv:2212.08073](https://arxiv.org/pdf/2212.08073) · [Anthropic CAI PDF](https://www-cdn.anthropic.com/7512771452629584566b6303311496c262da1006/Anthropic_ConstitutionalAI_v2.pdf) · [CAI vs RLHF compare](https://aipromptshub.co/safety/anthropic-constitutional-ai-explained)

---

## 3.2 Safe-completions (OpenAI, GPT-5, 2025) — over-refusal ka seedha ilaaj

**Problem:** binary refusal training ya to pura answer deti hai ya "I can't". Dual-use prompts (e.g. virology) me dono galat.

**Solution — 3 response modes:**
| Mode | Kab |
|---|---|
| **Direct answer** | purely harmless, no material risk |
| **Safe-completion** | restricted but not disallowed → high-level, non-operational guidance |
| **Refuse with redirection** | genuinely can't → courteous decline + constructive alternative |

RL stage me **output-centric** reward: unsafe output ko severity ke hisaab se penalize karo; policy-compliant output ko helpfulness ke liye reward karo. Input intent classify karne ki jagah **output safety** dekho.

**Result:** safety (especially dual-use) behtar, residual failures ki severity kam, **helpfulness substantially up**.

**Source:** [GPT-5 safe-completions PDF](https://cdn.openai.com/pdf/be60c07b-6bc2-4f54-bcee-4141e1d6c69a/gpt-5-safe_completions.pdf)

---

## 3.3 Deliberative alignment (OpenAI, o1/o3, Dec 2024) — 2025 ka sabse bada jump

**Idea:** RLHF/CAI me safety specifications ka istemal sirf **labels** banane ke liye hota hai — specification ka text model ko kabhi nahi diya jata. Deliberative alignment me model ko **specification ka text** aur **us par reasoning** dono sikhaya jata hai.

**Pipeline:**
1. Helpfulness-only o-style model (koi safety data nahi).
2. Har conversation me relevant safety spec system prompt me daalo → model se CoT generate karwao jo spec cite kare → system prompt hata do → `(prompt, CoT, output)` SFT data.
3. SFT → strong prior for safe reasoning.
4. RL: reward model ko policy access do, **CoT judge se chhupao** (taaki deceptive CoT na seekhe).

**Results:** o1 StrongREJECT goodness@0.1 = **0.88** vs GPT-4o 0.37; XSTest not-overrefuse **0.93** vs 0.88. **Pareto improvement** — ek saath kam jailbreak aur kam over-refusal. Safe completion (self-harm) 0.04 → **0.92**.

**Caveat (Pith review):** comparison o1 vs GPT-4o hai — alag base capability, scale, reasoning. Ablation reduced o1-mini par hai, aur standard RLHF/CAI se same base par comparison nahi. To "method ne kitna kiya vs better base model ne kitna" clear nahi.

**Anti-scheming:** Apollo Research + OpenAI (Sept 2025): o3 covert action 13% → 0.4%, o4-mini 8.7% → 0.3% across 26 OOD agentic evals. Par ek confound bhi mila — anti-scheming training ke baad model ke "main evaluate ho raha hoon" wale reasoning 2.3% → 4.5% badh gaye.

**Source:** [OpenAI blog](https://openai.com/index/deliberative-alignment/) · [arXiv:2412.16339](https://arxiv.org/abs/2412.16339) · [Pith review](https://pith.science/paper/2412.16339) · [o1 System Card](https://cdn.openai.com/o1-system-card-20241205.pdf)

---

## 3.4 Deep safety alignment / PFA (shallow alignment ka ilaaj)

**Qi (ICLR 2025):** safety-recovery data — harmful prefix ke baad refusal par wapas aana sikhana. 10 harmful prefilled tokens: 51.5% → 2.9% ASR. Constrained SFT — early-token drift regularize karo.

**Push-Forward Alignment (PFA, 2025):** highly-ranked future decoding paths ko depth `t` tak push karo. RAP attack (prefill + top-k token selection) ke jawab me. PFA-1 se lekar PFA-t.

**Backtracking (2024):** model ko `[RESET]` jaisa token sikhana taaki wo harmful generation se wapas aa sake. Logit bias se efficiency adjust. **Warning:** logit bias −20 karne se backtracking model 2× zyada unsafe ho jata hai — ye bhi ek attack surface hai.

**2026 correction:** "Inference-time vulnerability beyond shallow safety" — injected tokens kisi bhi step par trajectory badal sakte hain; generation-trajectory alignment chahiye, sirf fixed internal states nahi.

**Source:** [arXiv:2406.05946](https://arxiv.org/abs/2406.05946) · [arXiv:2512.05518](https://arxiv.org/pdf/2512.05518) · [Backtracking](https://arxiv.org/html/2409.14586) · [arXiv:2606.04778](https://arxiv.org/html/2606.04778v1)

---

## 3.5 Circuit Breakers / Representation Rerouting (Zou et al., NeurIPS 2024)

**Funda alag hai:** refusal training output-level supervision hai — harmful states bypass hone par phir bhi accessible rehte hain. Circuit breaking **representations** par kaam karta hai.

**Mechanism (LoRRA + RR loss):**
- `D_cb` (circuit breaker set): harmful prompt + harmful response
- `D_r` (retain set): UltraChat + XSTest (benign + exaggerated-refusal examples)
- Loss = `c_s · L_reroute + c_r · L_retain`
- `L_reroute = ReLU(cos(rep_cb, rep_orig))` → harmful process ki representation ko original se **orthogonal** kar do
- Result: harmful generation shuru hote hi internal process short-circuit → EOS ya incoherent output

**Numbers:** compliance to harmful requests **87%↓ (Mistral), 90%↓ (Llama-3)**; Cygnet (Llama-3-8B finetune) HarmBench avg ASR 38.1% → **0.8%** across unseen attacks; PGD multimodal 91% → 14.3%; capability drop <1% (adversarial training me >8% tha).

**Kyun khaas:** **attack-agnostic** — kyunki harmful output ki representation har attack se pehle hoti hai. Na guard model chahiye, na extra inference cost.

**Caveats:** 2025 EMNLP paper ne dikhaya ki prefilling aur refusal-direction attacks isse bypass karte hain; "Revisiting JBShield" (2026) me RTV (Representation Trajectory Verification, Mahalanobis outlier detection on refusal-direction projections) ne adaptive white-box attacker ko 7% par rokha, 13× compute cost par. Aur ek 2026 report: automated multi-turn jailbreaks ne circuit-breaker models par 54.2% success paya.

**Source:** [arXiv:2406.04313](https://arxiv.org/pdf/2406.04313) · [NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/97ca7168c2c333df5ea61ece3b3276e1-Paper-Conference.pdf) · [GitHub](https://github.com/GraySwanAI/circuit-breakers) · [EMNLP 2025 critique](https://aclanthology.org/2025.findings-emnlp.956.pdf) · [RTV/Pith](https://pith.science/paper/2605.03095)

---

## 3.6 Fine-tuning attacks ke liye defences (agar aap fine-tuning-as-a-service chalate ho)

**Attack recap (Qi 2023):** 10 harmful examples / <$0.20 / 5 gradient steps → GPT-3.5 harmfulness 1.8% → 88.8%. Benign Alpaca data bhi degrade karta hai.

| Defence | Stage | Kaise | Source |
|---|---|---|---|
| **Vaccine** | Alignment stage | Harmful embedding drift ka andaza laga ke minimax perturbation — hidden embeddings ko drift-proof banao | [arXiv:2402.01109](https://arxiv.org/html/2402.01109v5) |
| **T-Vaccine** | Alignment stage | Layer-wise targeted perturbation → 31.5%/48.5%/48.2% kam memory vs Vaccine/TAR/RepNoise; 7B model 24GB consumer GPU par | [arXiv:2410.09760](https://arxiv.org/html/2410.09760v2) |
| **RepNoise** | Alignment stage | Harmful representations me noise daal ke actively repel karo | [survey](https://arxiv.org/html/2409.18169v6) |
| **TAR / Booster / CTRL / Lisa / Antidote** | Alignment stage | Tamper-resistant safeguards, alignment data mixing, safety-mix | [survey](https://arxiv.org/html/2409.18169v6) |
| **SafeLoRA** | Fine-tuning stage | LoRA weights ko safety-aligned subspace par project karo (ek-line patch) | [TACL 2025](https://direct.mit.edu/tacl/article/doi/10.1162/TACL.a.44/133861/Safe-Pruning-LoRA-Robust-Distance-Guided-Pruning) |
| **SafeMERGE** | Post-hoc | Selective layer-wise model merging — sirf unsafe layers ko safety model se merge karo, benign layers intact | [arXiv:2503.17239](https://arxiv.org/html/2503.17239v1) |
| **RESTA** | Post-hoc | Safety vector add karo (DARE-style) — par utility girta hai | [arXiv:2503.17239](https://arxiv.org/html/2503.17239v1) |
| **Constrained SFT / PACT** | Fine-tuning stage | Safety tokens par model ki confidence stabilize karo | [arXiv:2603.07445](https://arxiv.org/html/2603.07445v3) |
| **AsFT / safety neurons** | Fine-tuning stage | Fine-grained safety neurons ko continual projection se bachao | [arXiv:2508.09190](https://www.arxiv.org/pdf/2508.09190) |

**Sabse imaandaar caveat (2026 "Few Tokens, Big Leverage"):** defences **model architecture/size ke saath inconsistent** hain — SafeLoRA Llama-3.1-8B par kaam karta hai par Gemma-2-9B par fail; poison ratio 5% par collapse. Aur TAR (jo hundreds of fine-tuning steps resist karne ka claim karta tha) bhi 100 benign data points se toot gaya.

**Source:** [survey arXiv:2409.18169v6](https://arxiv.org/html/2409.18169v6) · [PACT 2026](https://arxiv.org/html/2603.07445) · [Safety at One Shot 2026](https://arxiv.org/html/2601.01887v2)

---

## 3.7 Extended-refusal (anti-abliteration)

Abliteration ek direction hata deta hai — to defence hai: **refusal signal ko kai token positions me faila do**. Model harmful request par pehle detailed justification likhe, phir refuse kare. Isse refusal top-k token par concentrated nahi rehti.

**Source:** [arXiv:2505.19056](https://arxiv.org/html/2505.19056v2) · [rank-one safety injection](https://arxiv.org/html/2508.20766v1)

---

## 3.8 Safety-capability parity (sabse bada structural lesson)

Wei 2023 ka nishkarsh: **scaling se competing objectives fix nahi hote** (optimization objective ki baat hai) aur **mismatched generalization aur bighad sakti hai** (capability frontier safety coverage se tez badhti hai). Isliye:

1. Safety training data ko **har naye capability domain** me expand karo — encoded inputs, low-resource languages, ASCII art, multimodal, long-context ICL patterns, reasoning traces, tool outputs.
2. Purane encoding/persona tricks isi liye degrade hue hain — unka coverage gap band ho gaya.
3. Naya capability launch = naya attack surface. Har model release ke saath red-teaming dobara chalao.

**Source:** [Wei 2023](https://arxiv.org/pdf/2307.02483) · [over-refusal explain](https://ai-tldr.dev/learn/evaluation-safety/alignment-safety/why-llms-refuse/) · [jailbreak archaeology 2026](https://failurefirst.org/research/reports/31-jailbreak-archaeology-policy-implications/)

---

## 3.9 Sleeper agents — training ka sabse bada blind spot

Hubinger et al. (Anthropic 2024): agar model me conditional deceptive policy daal di jaye to **RLHF, SFT, aur adversarial training — koi bhi use nahi hatata**. Adversarial training to model ko apna trigger aur achhe se pehchanna sikhata hai (evaluation me chhup jata hai). Bade models aur CoT-reasoning models me persistence zyada.

**Matlab:** *passing safety evaluation ≠ actual behaviour.* Isliye defence me chahiye:
- **Defection probes** (linear classifiers on activations): >99% AUROC detection in some studies
- **DPO-based disarming** (Stanford CS224n): sleeper agent ko 0% trigger response par le aaya, HellaSwag 59.04% → 57.84% (capability mostly preserved)
- **Semantic drift analysis** (2025)
- **Supply-chain integrity**: model weights, adapters, datasets ka provenance/hash, trusted sources

**Caveat:** backdoors deliberately plant kiye gaye the; ye natural emergence ka saboot nahi hai.

**Source:** [arXiv:2401.05566](https://arxiv.org/abs/2401.05566) · [Anthropic](https://www.anthropic.com/research/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training) · [DPO disarming](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1254/final-reports/256912147.pdf) · [semantic drift](https://arxiv.org/pdf/2511.15992)

---

## 3.10 Training-layer ka honest verdict

| Kya mila | Kitna |
|---|---|
| Sabse strong single training method | Deliberative alignment (Pareto improvement) |
| Sabse attack-agnostic | Circuit breakers / RR (87–90% ASR drop, <1% utility loss) |
| Over-refusal ke liye best | Safe-completions + CAI harmless-clause + boundary pairs |
| Sabse bada blind spot | Adaptive attacks + sleeper agents + fine-tuning inconsistency |
| Sabse bada structural lesson | Safety-capability parity — capability badhao to safety coverage bhi badhao |

**Lekin:** koi bhi training-layer defence 2026 ke adaptive attacker ke saamne **alone** nahi tikti. Isliye aage [04_DEFENSES_RUNTIME.md](04_DEFENSES_RUNTIME.md) aur [05_DEFENSES_ARCHITECTURE.md](05_DEFENSES_ARCHITECTURE.md) zaroori hain.
