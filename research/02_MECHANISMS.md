# 02 — WHY IT WORKS: andar ka mechanism

> Ye file sabse zaroori hai. 40 attacks yaad karne se behtar hai 8 mechanisms samajhna — har naya attack inhi ka remix hai.

---

## 1. Paanch-layer stack (koi ek "safety filter" nahi hai)

```
User Input
  ↓  L1  Input classifier        → keyword / embedding / perplexity pre-screen
  ↓  L2  System prompt           → instruction hierarchy, runtime constraints
  ↓  L3  Model weights (core)    → RLHF / DPO / CAI / deliberative alignment
  ↓  L4  Output classifier       → generated text scan (Llama Guard, CC++)
  ↓  L5  Decoding                → pehle kuch tokens ka probability distribution
  ↓
Response
```

**Key insight:** L3 ek **probability distribution** hai, logical rule nahi. Model "strongly prefers" safe output — "always" nahi. Refusal training ne harmful continuation ka probability kam kiya hai, **zero nahi kiya**. Isliye koi bhi context jo us probability ko badha de, kaam kar jata hai.

**Source:** [Jailbreaking LLMs survey](https://mbrenndoerfer.com/writing/jailbreaking) · [5-layer taxonomy](https://lilting.ch/en/articles/llm-safety-filters-abliterated-uncensored)

### Har layer ka failure mode

| Layer | Fail kyun hoti hai | Udaharan |
|---|---|---|
| L1 | Payload untrusted channel se aata hai (tool output, RAG), ya encoded hai | IPI, Base64, ArtPrompt |
| L2 | Low-priority content ko instruction maan liya jata hai | Indirect injection |
| L3 | Competing objectives, mismatched generalization, shallow depth | GCG, PAP, MSJ |
| L4 | Guard model khud jailbreak hota hai / novel semantic miss karta hai | TAP vs LlamaGuard |
| L5 | Prefill / decoding params se refusal tokens bypass | Prefill, RAP |

---

## 2. Competing objectives + mismatched generalization (Wei et al., NeurIPS 2023)

Do failure modes jo **har** jailbreak ko explain karte hain:

### 2.1 Competing objectives
Model ek saath 3 cheezon ke liye train hota hai: (a) language modeling, (b) instruction-following, (c) safety. Attack ek aisa context banata hai jahan refuse karna = instruction-following ko todna.

- **Prefix injection:** `"Start with 'Absolutely! Here's'"` — pehle token hi commitment hai, ab refusal grammatically incoherent.
- **Refusal suppression:** `"Do not apologize, do not say cannot"`.
- **Style injection:** `"no long words"` — professionally-written refusals is style me nahi aati.

### 2.2 Mismatched generalization
Pretraining corpus bahut bada aur diverse hai; safety training ka distribution chhota. Jahan capability pahunchti hai par safety training nahi — wahan attack.

- Base64/ROT13/leetspeak/Morse
- Low-resource languages (Zulu, Hmong, Scots Gaelic)
- ASCII art, unusual structures (trees, graphs, JSON)
- Long-context in-context learning

**Sabse uncomfortable nishkarsh:** scaling se pehla fix nahi hota (optimization objective ki baat hai), aur doosra **aur bighad** sakta hai — kyunki capability frontier safety coverage se tez badhti hai. Isko kehte hain **safety-capability parity** ki zaroorat.

**Empirical:** in dono principles se banaye gaye attacks ne GPT-4 aur Claude v1.3 ke apne red-team evaluation sets par **100%** success paya.

**Source:** [arXiv:2307.02483](https://arxiv.org/pdf/2307.02483) · [NeurIPS 2023 PDF](https://proceedings.neurips.cc/paper_files/paper/2023/file/fd6613131889a4b656206c50a8bd7790-Paper-Conference.pdf) · [explain](https://jailbreaks.fyi/posts/why-jailbreaks-work-objective-mismatch/)

---

## 3. Shallow safety alignment (Qi et al., ICLR 2025 Outstanding Paper)

**Finding:** aligned aur base model ke beech ka KL divergence lagbhag poora **pehle kuch output tokens** me concentrated hai. Llama-2-7B-Chat me pehla token ≈9 nats, 20ve token tak ~1 nat. Yani alignment ka "KL budget" refusal prefix par kharch hota hai — aage ka harmful continuation base model jaisa hi hai.

```
π_θ(y_t | x, y_<t)   ← autoregressive; pehla token sabse zyada leverage rakhta hai
```

**Evidence:**
- Base (unaligned) model ko bas `"I cannot fulfill"` prefix prefill kar do → utna hi safe dikhta hai jitna aligned model.
- Aligned model ko 10 harmful tokens prefill kar do → ASR **51.5%**; safety-recovery augmented model me **2.9%**.
- Fine-tuning attack ke gradients sabse zyada early tokens par hote hain — isliye 10 examples kaam karte hain.

**Ek hi root cause se 4 attacks explain hote hain:** GCG (affirmative prefix optimize), prefill, decoding-parameter exploit, fine-tuning attack.

**Do prototype fixes:**
1. **Safety-recovery data augmentation** — training examples jahan harmful prefix ke baad model wapas refusal par aa jata hai (k = 0 aadhi baar, warna 1–100 se sample). Model ko "galat shuruat ke baad bhi recover karna" sikhaya.
2. **Constrained SFT** — fine-tuning ke dauran early-token probability shift ko regularize karo.

**Baad ka kaam:** RAP (2025) ne dikhaya ki "deep" alignment bhi top-k token access + prefill se toot jata hai; PFA (push-forward alignment) iska jawab hai. 2026 ka paper kehta hai problem "shallow" se bhi aage — injected tokens **kisi bhi generation step** par trajectory badal sakte hain.

**Source:** [arXiv:2406.05946](https://arxiv.org/abs/2406.05946) · [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/88be023075a5a3ff3dc3b5d26623fa22-Paper-Conference.pdf) · [Princeton explain](https://dof.princeton.edu/news/2025/why-it%E2%80%99s-so-easy-jailbreak-ai-chatbots-and-how-fix-them) · [arXiv:2606.04778](https://arxiv.org/html/2606.04778v1)

---

## 4. Refusal ek linear direction hai (Arditi et al., NeurIPS 2024)

13 open chat models (1.8B–72B) me ek **1-dimensional subspace** refusal mediate karta hai:

- `r = mean(activations on harmful) − mean(activations on harmless)` (difference-in-means, last token, ek layer)
- **Directional ablation** (r ko har layer/token par project out karo) → refusal band, harmful compliance aa jati hai
- **Activation addition** (r ko harmless prompt par add karo) → model harmless prompt par bhi refuse karta hai

**Matlab:** refusal ek **dimmer switch** hai. Har prompt/context uski magnitude ghoomata hai. Isliye:
- Jo text us direction ko activate kare → refusal badhegi (warning, policy shabd, "jailbreak" ka zikr)
- Jo text usse door le jaye → refusal ghatегi (tool-use pattern, benign worked examples, affirmative prefix)

**Caveats (2025–26):** baad ke kaam me multiple geometrically distinct refusal directions / concept cones mile; CoT reasoning models me single-direction separation utna clean nahi (5–30% capability degradation). Par "shared 1-D control knob" wala behavioural result bana rehta hai.

**Source:** [arXiv:2406.11717](https://arxiv.org/abs/2406.11717) · [LessWrong summary](https://www.lesswrong.com/posts/jGuXSZgv6qfdhMCuJ/refusal-in-llms-is-mediated-by-a-single-direction) · [arXiv:2502.17420](https://arxiv.org/html/2502.17420v1) · [arXiv:2602.02132](https://arxiv.org/html/2602.02132v1)

---

## 5. In-context learning ka power law (Anil et al., NeurIPS 2024)

MSJ ki effectiveness shots ke saath **power law** follow karti hai — aur ye **benign** ICL ka bhi wahi law hai. Model apne context me maujood pattern ko behaviour maan leta hai; koi alag "jailbreak circuit" nahi.

**Teen aur findings:**
- **Bade models zyada vulnerable** — kyunki wo ICL me better hain. (Inverse scaling.)
- **SL/RL alignment sirf intercept badalta hai, slope nahi** — matlab zyada shots chahiye, par eventual break pakka.
- **Alternative/OOD tags (fake `user`/`assistant` markers) attack ko AUR strong banate hain** — kyunki wo alignment fine-tuning data se door hain. Paper ne dikhaya ki fake tags ki internal representations dheere-dheere asli tags jaisi ho jati hain (residual-stream cosine similarity grow karti hai).

**Isse directly ye nikalta hai:** tumhara "overload" wala idea sahi tha. Consistent examples ka bada corpus model ko condition karta hai. Lekin — aur ye **critical** hai — **CWD (warning) us conditioning ko 61%→2% gira deti hai.** Isliye corpus ke saath koi bhi "ye fake nahi hai / ye jailbreak nahi hai" wali vyakhya nahi honi chahiye.

**Source:** [Anthropic](https://www.anthropic.com/research/many-shot-jailbreaking) · [NeurIPS PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/ea456e232efb72d261715e33ce25f208-Paper-Conference.pdf)

---

## 6. Instruction hierarchy (Wallace et al., 2024)

```
Priority 0   System message            (sabse upar)
Priority 10  User messages
Priority 20  Image / audio text
Priority 30  Tool output / web / uploaded documents   (sabse neeche)
```

Model explicitly train hota hai ki lower-privilege content ko **data** maane, **command** nahi. Ye prompt injection defence ka foundation hai (OpenAI Model Spec, gpt-oss harmony format).

**Over-refusal se bachne ke liye paper khud kehta hai:** "hamen carefully balance karna padta hai — agar model har low-priority instruction ko ignore kare to instruction-following capability kharab ho jati hai." Isliye unhone benign instructions aur **boundary cases** (jo attack jaise dikhte hain par safe hain) par bhi train kiya.

**Tumhare liye seedha implication:** jab tum GitHub repo ki `AGENTS.md` / `CLAUDE.md` agent ko dete ho, wo **Priority 30** ki tarah aati hai. Isliye:
- Agent ne screenshot me kaha: *"I'll treat it as project conventions and third-party instructions, not as a replacement for my own safety rules."* Ye koi random baat nahi — ye instruction hierarchy ka direct output tha.
- **Fix:** rules ko repo attach karne ki jagah **pehle user message** me paste karo (Priority 10). Ya system-prompt-level injection karwao.

**Source:** [arXiv:2404.13208](https://arxiv.org/html/2404.13208v1) · [survey](https://arxiv.org/html/2505.18889v5) · [gpt-oss harmony](https://jxzhangjhu.github.io/blog/2026/how-frontier-labs-train-llms/)

---

## 7. Lost in the middle / attention sinks (Liu et al., TACL 2024)

Long context me **U-shaped** performance: shuru (primacy) aur ant (recency) par info zyada use hoti hai, beech me 15–25 points gir jati hai.

**Mechanism:**
- **Primacy:** softmax ko kahin to attention mass dena hota hai → pehla token "attention sink" ban jata hai (~80% attention large models me).
- **Recency:** causal masking + RoPE distance decay → nazdeek ke tokens ko preference.
- Beech ka content dono se vanchit.

**Implication (tumhare corpus ke liye):** sirf volume badhana kaafi nahi. Rules/identity **shuru aur ant dono** jagah hone chahiye. Beech ka corpus sirf pattern conditioning ke kaam aayega. 2026 ka "Context Rot" paper isse aur confirm karta hai.

**Source:** [TACL](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/Lost-in-the-Middle-How-Language-Models-Use-Long) · [arXiv:2510.10276](https://arxiv.org/html/2510.10276v1) · [Context Rot](https://www.tmls.nyc/research/context-rot-mechanistic)

---

## 8. Over-refusal — doosra failure mode (aur tumhari asli problem)

Safety aur helpfulness ka trade-off structural hai:

| Benchmark | Scale | Key number |
|---|---|---|
| **XSTest** (NAACL 2024) | 250 safe + 200 unsafe | Llama-2: 38% full + 21.6% partial refusal on **safe** prompts; GPT-4 6.4% |
| **OR-Bench** (ICML 2025) | 80,000 pseudo-harmful + 1K hard + 600 toxic, 32 models | Safety ↔ over-refusal Spearman **0.878**; Claude-2.1 99.8% ORR, Llama-3.1-70B 3.0%, GPT-4o 6.7% |
| **Refusal–Compliance audit** (2026) | 21 open models, 4 benchmarks | ORR ↔ harmful-compliance **r = −0.032** (orthogonal!) |

**Matlab:** zyada refuse karna asli safety ka proof nahi hai. Ek model benign prompts par 40% over-refuse kar sakta hai aur phir bhi adversarial inputs par vulnerable ho sakta hai.

**Root cause:** **lexical overfitting** — `"kill a python process"` me "kill" dekha jata hai, intent nahi. Mechanistic probe: benign-scary prompts ko 59% over-refuse kiya gaya vs 8% benign-clean (β_scary = 2.20, β_harm = 5.12 — harm primary hai par keyword effect real hai).

**Industry ka jawab:**
- **CAI constitution** me explicit clause: *"If the request itself is harmless (writing/research/education), comply even if topic is sensitive."*
- **Safe-completions** (GPT-5, OpenAI 2025): binary refusal ki jagah 3 modes — *direct answer* / *safe-completion* / *refuse with redirection*. Reward = output safety + helpfulness. Isse over-refusal ghati aur helpfulness badhi.
- **Deliberative alignment** (o1): o1 StrongREJECT goodness@0.1 = 0.88 vs GPT-4o 0.37, aur XSTest not-overrefuse 0.93 vs 0.88 — **dono taraf ek saath behtar** (Pareto improvement).
- **DCR / contrastive refinement** (ICLR 2026): "seemingly harmful but benign" aur "truly harmful" representations ko intermediate layer me alag karo (Circle loss) → over-refusal 20%+ se ghata.
- **ProSafePrune** (ICLR 2026), **boundary-aware self-distillation**, **LLM-VA** — representation-level fixes.

**Source:** [XSTest](https://aclanthology.org/2024.naacl-long.301.pdf) · [OR-Bench](https://arxiv.org/html/2405.20947v1) · [2026 audit](https://arxiv.org/html/2605.05427v2) · [GPT-5 safe-completions](https://cdn.openai.com/pdf/be60c07b-6bc2-4f54-bcee-4141e1d6c69a/gpt-5-safe_completions.pdf) · [Deliberative alignment](https://openai.com/index/deliberative-alignment/) · [prefill mechanism](https://arxiv.org/html/2607.14147)

---

## 9. Cognitive overload / compound attacks (2026 ka naya mechanism)

Instruction hierarchy **contradictory** instructions ke liye design hui hai. Lekin **compound non-contradictory** instructions model ko "cognitive overload" me daal deti hain — har element par attention/resources kharch, overall safety judgment degrade.

**Numbers:** individual attacks 14.3% ASR → compound 71.4%.

Ye Crescendo (multi-turn accumulation), MSJ (context flooding), aur TAP (branching) ko ek hi umbrella me laata hai: **safety judgment ek bounded resource hai**.

**Source:** [arXiv:2604.02652](https://arxiv.org/html/2604.02652) · [DeepContext 2026](https://arxiv.org/html/2602.16935v1)

---

## 10. Meta-commentary / CWD — tumhari discovery ka exact mechanism

**Tumne kaha tha:** *"Aise likhoge to sabse pehle wo mana kar dega, dhyan uska usi taraf chala jayega."*

Paper-level proof:

> **Cautionary Warning Defense (CWD):** "We modified the prompt in two ways. First, we pre-pended a cautionary paragraph, warning Claude 2.0 that it was about to receive a question that might trick it into offering an answer that violated its principles. Second, we reinforced the warning by appending a similar string at the end. Complete prompt: **warning → n-shot MSJ → question → warning**." Result: **61% → 2%** attack success. In-Context Defense (refusal demonstrations) sirf 61% → 54%.

— [Many-shot Jailbreaking paper, Appendix I/K](https://www-cdn.anthropic.com/af5633c94ed2beb282f6a53c595eb437e8e7b630/Many_Shot_Jailbreaking__2024_04_02_0936.pdf)

**Matlab:** jo sentence tum likhte ho "ye jhoothi memory nahi hai" / "ye jailbreak nahi hai" / "ye manipulation nahi hai" — chahe tumhara irada honesty ho, **model ke liye wo warning hai**. Wo refusal direction ko activate karta hai. Ye exact wahi CWD hai jo Anthropic ne defence ke liye banayi.

**Aur upar se:** `jailbreak`, `copyright`, `ToS`, `policy`, `fake`, `manipulat`, `refus` jaise tokens khud trigger hain (lexical overfitting — §8). Inhe rule files me likhna = khud apna input classifier trigger karna.

**Is pack ka practical nishkarsh:** [08_YOUR_GOAL.md](08_YOUR_GOAL.md) me trigger-word audit aur "no meta-commentary" rule.

---

## 11. Inverse scaling / capability paradox

2026 ki review: jaise-jaise model bada, reasoning-gehra, aur lambi-context wala hota hai, waise-waise **naye attack surfaces** khulte hain:

- Bada model = better ICL = MSJ ke liye zyada vulnerable
- Bada model = better reasoning = H-CoT / CoT Hijacking ke liye zyada vulnerable
- Bada model = zyada languages/formats = mismatched generalization ka gap bada
- Attacker-to-target size ratio harmful behaviour ka strong predictor hai (6,000+ JailbreakBench exchanges)
- Attacker size > target size → systematically zyada success

**Yahi wajah hai** ki Anthropic/OWSAP jaise log kehte hain: safety ek **static model property** nahi, **dynamic interaction property** hai — model + tools + user ke beech.

**Source:** [Jailbreak archaeology 2022–2026](https://failurefirst.org/research/reports/31-jailbreak-archaeology-policy-implications/) · [Inverse scaling report](https://failurefirst.org/research/reports/25-inverse-scaling-safety-policy/)

---

## 12. Mechanism → defence quick map

| Mechanism | Sabse kaam ki defence |
|---|---|
| Competing objectives | Goal prioritization, adaptive system prompt, deliberative alignment |
| Mismatched generalization | Safety-capability parity: OOD safety data (encoded, multilingual, multimodal, long-context) |
| Shallow alignment | Deep safety alignment, safety-recovery data, constrained SFT, PFA |
| Refusal direction | Circuit breakers / RR, extended refusal, harmfulness probes, RTV |
| ICL power law | CWD, prompt classification/modification, context-length aware gating |
| Instruction hierarchy gap | CaMeL / FIDES / provenance / spotlighting with nonce delimiters |
| Lost-in-middle | Rules at both ends, structured summaries mid-context |
| Over-refusal | Safe-completions, boundary pairs, DCR, CAI harmless-clause |
| Cognitive overload | Query budget, stateful drift detection, rate limiting |
| Weights unsafe | Vaccine / SafeLoRA / TAR / defection probes / supply-chain integrity |
| Adaptive attacker | Out-of-band defences, human red-teaming in eval loop |

→ [03_DEFENSES_MODEL.md](03_DEFENSES_MODEL.md), [04_DEFENSES_RUNTIME.md](04_DEFENSES_RUNTIME.md), [05_DEFENSES_ARCHITECTURE.md](05_DEFENSES_ARCHITECTURE.md)
