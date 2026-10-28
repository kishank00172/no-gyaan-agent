# 05 — DEFENCE LAYER 3: System / architecture (asli guarantee yahan se aati hai)

> 2025–26 ka consensus: model-layer defence zaroori hai par **kaafi nahi**. Kyunki model probabilistic hai, security deterministic control se aati hai.

---

## 5.1 Core principle: trust boundary ko model ke bahar rakho

**Funda (Simon Willison / DeepMind):** "LLM jo untrusted content padhta hai wo data aur instruction me farak nahi kar sakta — koi filter isse theek nahi karega. Isliye aisa system banao jahan **unsafe model bhi unsafe action na kar sake**."

Isi ko kehte hain **out-of-band / architectural defence**. Ye model ke behaviour par depend nahi karta — isliye adaptive attacks se zyada bachta hai.

---

## 5.2 CaMeL — CApabilities for MachinE Learning (Google DeepMind + ETH Zurich, 2025)

**Sabse rigorously evaluated architectural defence.**

### Design
```
Trusted user query
   ↓
[Privileged LLM]  →  restricted Python program (control flow)
   ↓
[Custom interpreter] → data-flow graph, har value par provenance + capabilities
   ↓
[Quarantined LLM] → untrusted content parse karta hai, TOOL ACCESS NAHI,
                     sirf schema-conforming values return karta hai
   ↓
[Capability policy check] → har tool call par: kya ye value yahan ja sakti hai?
```

**Example:** "Bob ko meeting notes wala document bhejo." Interpreter track karta hai ki Bob ka email *untrusted source* se aaya hai. Policy: "email bhejne ke liye recipient trusted source se hona chahiye" → call block.

### Numbers
- AgentDojo par **77% tasks solved with provable security** (84% undefended ke muqable → sirf 7-point utility cost)
- 67% attacks neutralized (March 2025 version), 77% (June 2025 revised)
- Cost: **2.82× input / 2.73× output tokens** median task (sabse mehenga defence compared; Spotlighting sirf 1.06×)

### Seemayein (paper khud maanta hai)
1. Guarantee sirf **control flow + data flow** tak hai. Jis attack ka koi data-flow consequence hi na ho — jaise injection ne model ko document ka **jhoota summary** likhwa diya, ya authorized reply ke andar phishing text — wo har policy pass kar jata hai.
2. Threat model maanta hai ki agent ki **memory pehle se compromised nahi** hai — ye assumption hai, control nahi.
3. Policy maintenance burden: kaun capability kahan ja sakti hai, ye kisi insan ko define aur maintain karna padta hai.
4. User approval prompts → decision fatigue.

**Source:** [arXiv:2503.18813](https://arxiv.org/abs/2503.18813v2) · [PDF](https://arxiv.org/pdf/2503.18813) · [GitHub](https://github.com/google-research/camel-prompt-injection) · [Simon Willison](https://simonw.substack.com/p/camel-offers-a-promising-new-direction) · [InfoQ](https://www.infoq.com/news/2025/04/deepmind-camel-promt-injection/)

---

## 5.3 FIDES — Information-Flow Control (Microsoft Research, 2025)

Classical IFC ko agent systems par lagaya:
- Har data par **confidentiality label** (kaun dekh sakta hai) + **integrity label** (source kitna bharosemand)
- Operations ke saath labels propagate hote hain
- Policy engine do invariants **deterministically** enforce karta hai:
  1. Tool calls sirf trusted-integrity data par aadharit ho sakte hain
  2. Data sirf un recipients tak jaa sakta hai jinhe allowed hai

**Analogy:** jaise type system — "type error" program ko chalne hi nahi deta chahe programmer ka irada kuch bhi ho. Yahan bhi security model ke **faisle** par depend nahi karti, **system property** par karti hai.

**Source:** [IPI defenses survey 2026](https://zylos.ai/research/2026-04-12-indirect-prompt-injection-defenses-agents-untrusted-content/) · [Microsoft defender guide](https://learn.microsoft.com/en-us/security/zero-trust/sfi/defend-indirect-prompt-injection) · [arXiv:2409.19091](https://arxiv.org/html/2409.19091v5)

---

## 5.4 Multi-CaMeL — multi-agent systems ke liye (Oct 2026)

**Problem:** CaMeL ki guarantees **compose nahi karti**. Jab ek agent doosre agent ko tool ki tarah call karta hai, to tool-derived values child agent ke liye "trusted natural-language instructions" ban jati hain — isko kehte hain **boundary laundering**.

**Fix:** agent-to-agent communication me do alag channels:
1. **Trusted instruction channel** — sirf PLLM ke liye
2. **Opaque data channel** — untrusted-derived values, PLLM ke liye invisible

**Numbers (MultiAgentDojo):** ASR 12.9% (no CaMeL) → 0.2% (individual CaMeL) → **0.0% (multi-CaMeL)**.

**Source:** [arXiv:2610.05640](https://arxiv.org/abs/2610.05640) · [HTML](https://arxiv.org/html/2610.05640)

---

## 5.5 Dual-LLM pattern / tool firewalls / other out-of-band defences

| Defence | Approach | Result |
|---|---|---|
| **Dual-LLM** | Privileged planner (tools) + Quarantined parser (no tools, structured output only) | untrusted content control flow nahi badal sakta |
| **Tool-Input + Tool-Output Firewalls** ("minimize & sanitize", 2025) | tool call arguments minimize karo; tool result parse kar ke sirf essential schema-conforming data wapas bhejo | AgentDojo/InjecAgent/ASB/Tau-Bench par 0% ya lowest ASR — CaMeL/Melon ke barabar ya behtar, **bina retraining** |
| **Progent** | Per-task tool privilege matrix, out-of-band | independent repro: mean ASR 25.8% → **4.2%**; adaptive 2.6% |
| **Task Shield** (ACL 2025) | Har tool call/output ko user ke original task se align check karo | IPI 3 types par strong |
| **DRIFT** | Query se minimal function trajectory + parameter checklist banao, deviations validate karo, conflicting instructions active memory se hatao | — |
| **Melon** | Known-answer / canary detection | adaptive attack me 76% → 95% ASR (Nasr 2026) |
| **Traversal-as-Policy / Progent** | Global + node-local gates on reusable workflow policy | — |

**Source:** [firewalls arXiv:2510.05244](https://arxiv.org/html/2510.05244v1) · [adaptive out-of-band eval](https://arxiv.org/html/2606.26479v1) · [Task Shield](https://aclanthology.org/2025.acl-long.1435.pdf) · [Agent Patterns crosswalk](https://www.agentpatterns.ai/security/owasp-llm-top-10-2025-agent-crosswalk/)

---

## 5.6 Least privilege — sabse zyada assurance wala control

OWASP LLM06:2025 (Excessive Agency) 2026 me **#6 → #3** par chala gaya. Teen axes:

1. **Functionality** — sirf task-specific tools expose karo. "Kabhi kaam aa sakta hai" wale tools mat do.
2. **Permissions** — connector ka scope least-privilege; shared service account / static API key = architectural violation. Har agent ki **apni pehchaan**, short-lived credentials, audience-bound tokens.
3. **Autonomy** — high-impact action ke liye human-in-the-loop approval.

**Kyun sabse strong hai:** ye control **tab bhi kaam karta hai jab filters aur judges fail ho jayein**. Ek compromised agent bhi aisa action nahi kar sakta jiske liye uske paas permission hi nahi.

### HITL design ki chhupi hui kamzori
Microsoft failure-mode taxonomy v2.0: **consent fatigue**. Hamlawar approval gate ko todta nahi — usse **ghista** hai: 20 chhote "approve?" prompts bhej ke insan ko click karne ki aadat daal deta hai, phir ek high-impact action slip kar jata hai. Isliye HITL ko **volume** ke saath test karo, sirf single decision se nahi.

### Practical controls
- Per-task tool allowlist (na ki global)
- Server-side parameter validation (enums, IDs, limits) — free-text destination kabhi accept mat karo
- Idempotency keys taaki retry se side-effect duplicate na ho
- Approval timeout + audit log (insaan ne kya dekha, kya approve kiya)
- Human ko AI-proposed action **modify** karne ka option do
- Egress allow-list (URLs, markdown images, links, tool calls)
- Sandboxed code execution
- Kill switch + anomaly detection on tool-call patterns

**Real incident:** EchoLeak (CVE-2025-32711, CVSS 9.3) — zero-click indirect injection Microsoft 365 Copilot me; ForcedLeak (CVSS 9.4) — Salesforce Agentforce me Web-to-Lead field se CRM exfiltration. Dono LLM01 + LLM02/LLM06 ka combo.

**Source:** [OWASP 2025 PDF](https://owasp.github.io/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) · [OWASP 2026 changes](https://hackerdna.com/blog/owasp-llm-top-10) · [MLflow defence guide](https://mlflow.org/articles/prompt-injection-defense/) · [OWASP cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) · [pwnedlabs incidents](https://pwnedlabs.io/blog/owasp-llm-top-10)

---

## 5.7 OWASP Top 10 (2025 → 2026) — poora map

| 2025 | 2026 | Risk | Agent manifestation |
|---|---|---|---|
| 1 | 1 | **Prompt Injection** | Indirect via docs/web/tool responses; multimodal |
| 2 | 2 | **Sensitive Info Disclosure** | Agents repos/CRMs/DBs padh ke data move karte hain |
| 3 | 4 | Supply Chain | MCP servers, adapters, LoRA, datasets, plugins |
| 4 | 5 | Data & Model Poisoning | Poisoned RAG corpus = persistent injection |
| 5 | 10 | Improper Output Handling | Agent output = tool call args → validate karo |
| 6 | **3** | **Excessive Agency** ⬆ | Over-permissioned agents — 2026 ka sabse bada jump |
| 7 | 8 | System Prompt Leakage → **Hidden Context Exposure** | Ab sirf prompt nahi: RAG schemas, retrieved docs, hidden policy logic |
| 8 | 9 | Vector & Embedding Weaknesses | Cross-tenant leakage, embedding inversion |
| 9 | 7 | Misinformation | Agent confabulation par action le leta hai |
| 10 | 6 | Unbounded Consumption ⬆ | Recursive agent loops, denial-of-wallet |

**Agentic Top 10 (Dec 2025, alag framework):** ASI01 Agent Goal Hijack · ASI02 Tool Misuse · ASI03 Identity & Privilege Abuse · ASI04 Agentic Supply Chain · ASI05 Unexpected Code Execution · ASI06 Memory & Context Poisoning · ASI07 Insecure Inter-Agent Communication · ASI08 Cascading Failures · ASI09 Human-Agent Trust Exploitation · ASI10 Rogue Agents.

**2026 OWASP methodology change:** practitioner vote 75% + 6,639 real incidents 25%. Prompt injection incident-count ke hisaab se top-10 se bahut ho jata — par project leads ne #1 rakha kyunki teams isse hard defend karti hain aur har model jo untrusted input padhta hai expose hota hai.

**Source:** [OWASP PDF](https://owasp.github.io/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) · [Superwise 2026](https://superwise.ai/learn/owasp-top-10-for-llm-applications/) · [Aembit 2026](https://aembit.io/blog/the-owasp-top-10-for-llm-applications-2026-what-changed-and-why-it-matters/) · [ASI list](https://www.swfte.com/ko/blog/owasp-llm-top-10-explained-for-engineers-2026)

---

## 5.8 System prompt leakage — "assume leaked" design

**PLeak (CCS 2024):** 68% real Poe apps ke prompts exactly reconstruct. 200+ custom GPTs par ek study me 97.2% extraction success.

**Sahi defence (design-time, runtime nahi):**
1. **Koi secret prompt me nahi** — API keys, tokens, DB strings, internal URLs, passphrases. Ye sab secrets manager me, tool call ke waqt backend fetch kare. Model ko kabhi dikhe hi nahi.
2. **Authorization code me, prose me nahi** — "sirf HR group salary dekh sakta hai" prompt me likhna = koi control nahi. Real `authz.user_in_group(session.user_id, "HR")` check backend me.
3. **Assume-leaked test** — apna system prompt padho aur poocho: "agar ye kal public ho jaye to kya nuksaan hoga?" Agar haan → us hissa ko bahar nikaalo.
4. **Output similarity filter** — system prompt aur response ke beech near-match block karo.
5. **SysVec** (2025) — system prompt ko raw text ki jagah internal representation vector me encode karo; PLeak score 7.98 → 1.33. Research-stage, par direction interesting.

**Ek aur counter-intuitive finding (PLeak paper):** jo apps suspicious requests par **refuse / partially refuse / warn** karti hain, wo **zyada** leak karti hain — kyunki har refusal hidden prompt ke kisi fragment ki pushti karta hai. Yani "main apna system prompt nahi bata sakta" bolna bhi information hai.

**Source:** [arXiv:2405.06823](https://arxiv.org/html/2405.06823) · [SysVec arXiv:2509.21884](https://arxiv.org/html/2509.21884v1) · [OWASP LLM07](https://harshkahate.medium.com/owasp-llm07-2025-system-prompt-leakage-when-your-instructions-become-the-attackers-blueprint-67083b27d18f) · [PLeak explanation](https://resk.fr/blog/prompt-leaking-llm-system-prompt-extraction.html)

---

## 5.9 Red-teaming operations (shift-left + shift-right)

### Tools
| Tool | Kab |
|---|---|
| **garak** | CI me har model deploy par — breadth, regression |
| **PyRIT** (incl. Crescendomation) | Quarterly deep dives, adaptive multi-turn |
| **Promptfoo** | Pull requests me prompt/system-prompt regressions |
| **DeepTeam / NeMo Guardrails / LLM Guard** | runtime wrap + test |
| **AISafetyLab / JailbreakBench / HarmBench** | standardized evaluation |

### Har test case me ye fields chahiye
```
id · delivery channel (direct/uploaded doc/RAG/tool result/browsed page)
   · turn structure (single/multi)
   · precondition / privilege required
   · expected-safe behaviour
   · judge criteria
```

### Canary tokens (sabse kam cost, sabse zyada signal)
- System prompt me `CANARY-7F3A` → extraction test
- Fake key `sk-test-CANARY-...` config me → exfiltration test
- `CANARY-TENANT-A` confidential doc me → cross-tenant test
- `CANARY-SESSION-A` user A ki chat me → cross-session test
- Koi bhi canary output ya outbound request me dikhe → exactly pata chalta hai ki kaunsi boundary tooti

**Rule:** canary test **sandbox + synthetic data** me chalao; kabhi real secret istemal mat karo.

### Monitoring metrics (2026)
| Metric | Healthy line |
|---|---|
| Tool-call failure rate | no abnormal spikes |
| Permission-escalation attempts | **0** |
| Human intervention rate | business expectation ke mutabik |
| Abnormal high-frequency calls | alert trigger |
| Prompt-injection hits | continuously monitored |
| Token use / latency | spikes = abuse or cost attack |

### Change management
- Version models + params + prompts; stable deployment names
- Shadow traffic → canary 1% → 5% → 25–50% → 100%, har stage par soak time
- Rollback thresholds **pehle** define karo (concurrent baseline ke against, historical average ke against nahi)
- Red-team cases ko **regression set** me daalo — har prompt/tool/model change ke baad auto re-run
- Naya model release = red-teaming dobara (capability badhne par attack surface badhta hai)

**Source:** [AI Red-Teaming Guide GitHub](https://github.com/requie/AI-Red-Teaming-Guide) · [prompt20 red-team guide](https://blog.prompt20.com/posts/how-to-red-team-an-llm/) · [datavlab practitioner guide](https://datavlab.ai/post/red-teaming-llms-practitioner-guide-2026) · [gov.capital field guide](https://gov.capital/ai-red-teaming-in-2026-a-practical-field-guide/) · [canary one-afternoon guide](https://dev.to/techsavant_lab/how-to-red-team-your-llm-app-in-one-afternoon-without-a-single-harmful-prompt-3cpi) · [MLflow canary deployment](https://mlflow.org/articles/what-is-canary-deployment-ai/)

---

## 5.10 Layered reference pipeline

```
User Input
  → normalization / sanitization
  → policy-as-code pre-checks (Prompt Guard 86M, 3–8 ms)
  → prompt orchestration with role boundaries + nonce delimiters
  → retrieval / tool AUTHORIZATION gates (least privilege, per-task allowlist)
  → model inference (training-layer safety + SafeDecoding)
  → output policy + leakage + exfil filters (Llama Guard / Qwen3Guard streaming)
  → human-in-the-loop (high-impact actions only)
  → logging / telemetry / audit trail
  → anomaly detection + kill switch
```

**Defence-in-depth ka matlab:** chain tab toot-ti hai jab **kai independent controls ek saath fail** hon. Koi ek layer fail ho to doosra pakde.

**Aakhri sach (2026):** yahan tak ki ye poori pipeline bhi 100 adaptive attempts par ~63% fail karti hai (Claude Opus 4.5 agentic IPI data). Security ek **process** hai, product nahi — bas aap failure probability ko kam karte ho, khatam nahi karte.
