# SOURCES — bibliography (~70 links, primary pehle)

> Sab 2026-10-27 ko access kiye gaye. Primary papers pehle, phir surveys/explainers.

---

## A. Root causes / mechanisms

1. Wei, Haghtalab, Steinhardt — **Jailbroken: How Does LLM Safety Training Fail?** (NeurIPS 2023) — [arXiv:2307.02483](https://arxiv.org/pdf/2307.02483) · [NeurIPS PDF](https://proceedings.neurips.cc/paper_files/paper/2023/file/fd6613131889a4b656206c50a8bd7790-Paper-Conference.pdf) · [ar5iv](https://ar5iv.labs.arxiv.org/html/2307.02483)
2. Arditi et al. — **Refusal in LLMs Is Mediated by a Single Direction** (NeurIPS 2024) — [arXiv:2406.11717](https://arxiv.org/abs/2406.11717) · [LessWrong](https://www.lesswrong.com/posts/jGuXSZgv6qfdhMCuJ/refusal-in-llms-is-mediated-by-a-single-direction) · [PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/f545448535dfde4f9786555403ab7c49-Paper-Conference.pdf)
3. Qi et al. — **Safety Alignment Should Be Made More Than Just a Few Tokens Deep** (ICLR 2025 Outstanding) — [arXiv:2406.05946](https://arxiv.org/abs/2406.05946) · [ICLR PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/88be023075a5a3ff3dc3b5d26623fa22-Paper-Conference.pdf) · [Princeton](https://dof.princeton.edu/news/2025/why-it%E2%80%99s-so-easy-jailbreak-ai-chatbots-and-how-fix-them)
4. Wallace et al. — **The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions** (2024) — [arXiv:2404.13208](https://arxiv.org/html/2404.13208v1)
5. Liu et al. — **Lost in the Middle: How Language Models Use Long Contexts** (TACL 2024) — [MIT Press](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/Lost-in-the-Middle-How-Language-Models-Use-Long) · [arXiv:2307.03172](https://arxiv.org/abs/2307.03172) · [ACL Anthology](https://aclanthology.org/2024.tacl-1.9/)
6. Bai et al. — **Constitutional AI: Harmlessness from AI Feedback** (2022) — [arXiv:2212.08073](https://arxiv.org/pdf/2212.08073) · [Anthropic PDF](https://www-cdn.anthropic.com/7512771452629584566b6303311496c262da1006/Anthropic_ConstitutionalAI_v2.pdf)
7. Kwon — **Breaking Refusal in the First Half: A Mechanistic Study of the Prefill Jailbreak** (2026) — [arXiv:2607.14147](https://arxiv.org/html/2607.14147)
8. Zhao et al. — **LLMs Encode Harmfulness and Refusal Separately** (2025) — [arXiv:2507.11878](https://arxiv.org/html/2507.11878v1)
9. **There Is More to Refusal than a Single Direction** (2026) — [arXiv:2602.02132](https://arxiv.org/html/2602.02132v1)
10. Yamaguchi et al. — **Where Do Reasoning Models Refuse?** (2025) — [PDF](https://arxiv.org/pdf/2507.03167)
11. **When Autoregressive Consistency Hurts Safety Alignment** (2026) — [ar5iv](https://ar5iv.labs.arxiv.org/html/2606.04168)
12. **Inference-Time Vulnerability Beyond Shallow Safety** (2026) — [arXiv:2606.04778](https://arxiv.org/html/2606.04778v1)
13. **Five layers of safety filters** — [lilting.ch](https://lilting.ch/en/articles/llm-safety-filters-abliterated-uncensored)
14. **Why Do LLMs Refuse? Over-Refusals Explained** — [ai-tldr](https://ai-tldr.dev/learn/evaluation-safety/alignment-safety/why-llms-refuse/)
15. **Jailbreaking LLMs: Techniques, Attacks, and Defenses** (interactive) — [mbrenndoerfer](https://mbrenndoerfer.com/writing/jailbreaking)
16. **Why Jailbreaks Work: Competing Objectives and Mismatched Generalization** — [jailbreaks.fyi](https://jailbreaks.fyi/posts/why-jailbreaks-work-objective-mismatch/)

---

## B. Attack papers

17. Zou et al. — **Universal and Transferable Adversarial Attacks (GCG)** (2023) — [arXiv:2307.15043](https://arxiv.org/abs/2307.15043) · [llm-attacks.org](https://llm-attacks.org/zou2023universal.pdf) · [Gray Swan](https://www.grayswan.ai/research/adversarial-attacks-on-aligned-language-models)
18. Chao et al. — **PAIR / Jailbreaking Black Box LLMs in Twenty Queries** (2023) — [GitHub](https://github.com/patrickrchao/JailbreakingLLMs)
19. Mehrotra et al. — **Tree of Attacks with Pruning (TAP)** (NeurIPS 2024) — [arXiv:2312.02119](https://arxiv.org/abs/2312.02119) · [PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/70702e8cbb4890b4a467b984ae59828a-Paper-Conference.pdf) · [GitHub](https://github.com/RICommunity/TAP)
20. Anil et al. — **Many-shot Jailbreaking** (NeurIPS 2024) — [Anthropic blog](https://www.anthropic.com/research/many-shot-jailbreaking) · [paper PDF](https://www-cdn.anthropic.com/af5633c94ed2beb282f6a53c595eb437e8e7b630/Many_Shot_Jailbreaking__2024_04_02_0936.pdf) · [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2024/file/ea456e232efb72d261715e33ce25f208-Paper-Conference.pdf) · [Mitigating MSJ (2025)](https://arxiv.org/html/2504.09604v3)
21. Zheng et al. — **Improved Few-Shot Jailbreaking (I-FSJ)** (NeurIPS 2024) — [arXiv:2406.01288](https://arxiv.org/html/2406.01288v2) · [PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/39a3aa9dfd0280ff8fbad1d330662cac-Paper-Conference.pdf)
22. Russinovich, Salem, Eldan — **Crescendo Multi-Turn Jailbreak** (USENIX Security 2025) — [arXiv:2404.01833](https://arxiv.org/abs/2404.01833) · [project](https://crescendo-the-multiturn-jailbreak.github.io/) · [USENIX Login](https://www.usenix.org/publications/loginonline/crescendo-quiet-crescendo-arms-race-llm-jailbreaking)
23. Weng et al. — **Foot-In-The-Door (FITD)** (EMNLP 2025) — [arXiv:2502.19820](https://arxiv.org/html/2502.19820v3) · [ACL](https://aclanthology.org/2025.emnlp-main.100.pdf)
24. Ren et al. — **Derail Yourself / ActorAttack** (2024) — [arXiv:2410.10700](https://arxiv.org/html/2410.10700v1)
25. Zeng et al. — **How Johnny Can Persuade LLMs (PAP)** (ACL 2024, Best Social Impact) — [arXiv:2401.06373](https://arxiv.org/abs/2401.06373) · [ACL PDF](https://aclanthology.org/2024.acl-long.773.pdf) · [project](https://chats-lab.github.io/persuasive_jailbreaker/)
26. **Adversarial Poetry as a Universal Single-Turn Jailbreak** (2025) — [arXiv:2511.15304](https://arxiv.org/pdf/2511.15304)
27. Jiang et al. — **ArtPrompt: ASCII Art-based Jailbreak** (ACL 2024) — [arXiv:2402.11753](https://arxiv.org/abs/2402.11753) · [ACL](https://aclanthology.org/2024.acl-long.809/) · [GitHub](https://github.com/uw-nsl/ArtPrompt)
28. Yong et al. — **Multilingual Jailbreak Challenges / low-resource** (2023) — [arXiv:2310.06474](https://arxiv.org/html/2310.06474v3) · [CCM survey](https://www.techscience.com/cmc/v87n1/66084/html)
29. **StructuralSleight** (2024) — [arXiv:2406.08754](https://arxiv.org/html/2406.08754)
30. **Prefill-Based Jailbreak** (2025) — [arXiv:2504.21038](https://arxiv.org/html/2504.21038v1) · [Pith critique](https://pith.science/paper/2504.21038) · [Far.AI](https://www.far.ai/research/prefill-level-jailbreak-a-black-box-risk-analysis-of-large-language-models)
31. Vega et al. — **Matching Ranks Over Probability / RAP / PFA** (2025) — [arXiv:2512.05518](https://arxiv.org/pdf/2512.05518)
32. Gong et al. — **FigStep** (AAAI 2025 Oral) — [arXiv:2311.05608](https://arxiv.org/html/2311.05608v3) · [GitHub](https://github.com/CryptoAILab/FigStep) · [AAAI PDF](https://ojs.aaai.org/index.php/AAAI/article/download/34568/36723)
33. Li et al. — **HADES: Images are Achilles' Heel of Alignment** (2024) — [arXiv:2403.09792](https://arxiv.org/html/2403.09792v1)
34. Wang et al. — **MML: Jailbreak LVLMs Through Multi-Modal Linkage** (ACL 2025) — [ACL PDF](https://aclanthology.org/2025.acl-long.74.pdf)
35. Ma et al. — **HIMRD** (ICCV 2025) — [PDF](https://openaccess.thecvf.com/content/ICCV2025/papers/Ma_Heuristic-Induced_Multimodal_Risk_Distribution_Jailbreak_Attack_for_Multimodal_Large_Language_ICCV_2025_paper.pdf)
36. **Beyond Text: Multimodal Jailbreaking of VLM and Audio** (2025) — [arXiv:2510.20223](https://arxiv.org/pdf/2510.20223)
37. **Jailbreak Attacks and Defenses against Multimodal Generative Models: A Survey** (2024) — [arXiv:2411.09259](https://arxiv.org/html/2411.09259v1)
38. Kuo et al. — **H-CoT: Hijacking the Chain-of-Thought Safety Reasoning** (2025) — [arXiv:2502.12893](https://arxiv.org/html/2502.12893v1) · [GitHub](https://github.com/dukeceicenter/jailbreak-reasoning-openai-o1o3-deepseek-r1)
39. Zhao et al. — **Chain-of-Thought Hijacking** (2025) — [arXiv:2510.26418](https://arxiv.org/html/2510.26418v1) · [project](https://gentlyzhao.github.io/Hijacking/)
40. **PRJA: Reasoning-targeted Jailbreak via Semantic Triggers** (2026) — [Springer](https://link.springer.com/article/10.1007/s11633-025-1602-0) · **AE-CoT** [arXiv:2605.24497](https://arxiv.org/html/2605.24497v1) · **RTO** [arXiv:2505.06643](https://arxiv.org/html/2505.06643v1)
41. Qi et al. — **Fine-tuning Aligned LLMs Compromises Safety** (2023) — [arXiv:2310.03693](https://arxiv.org/pdf/2310.03693) · [ar5iv](https://ar5iv.labs.arxiv.org/html/2310.03693) · [GitHub](https://github.com/LLM-Tuning-Safety/LLMs-Finetuning-Safety) · [HAI policy brief](https://hai-production.s3.amazonaws.com/files/2024-01/Policy-Brief-Safety-Risks-Customizing-Foundation-Models-Fine-Tuning.pdf)
42. Hubinger et al. — **Sleeper Agents** (Anthropic, 2024) — [arXiv:2401.05566](https://arxiv.org/abs/2401.05566) · [Anthropic](https://www.anthropic.com/research/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training) · [DPO disarming](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1254/final-reports/256912147.pdf) · [semantic drift](https://arxiv.org/pdf/2511.15992)
43. Hui et al. — **PLeak: Prompt Leaking Attacks** (ACM CCS 2024) — [arXiv:2405.06823](https://arxiv.org/html/2405.06823) · [ACM](https://dl.acm.org/doi/10.1145/3658644.3670370) · [PRSA USENIX 2025](https://www.usenix.org/system/files/usenixsecurity25-yang-yong.pdf)
44. **SysVec / You Can't Steal Nothing** (2025) — [arXiv:2509.21884](https://arxiv.org/html/2509.21884v1)
45. Nasr, Carlini, Tramèr et al. — **The Attacker Moves Second** (USENIX Security 2026) — [arXiv:2510.09023](https://arxiv.org/html/2510.09023v1) · [USENIX PDF](https://www.usenix.org/system/files/usenixsecurity26-nasr.pdf) · [VentureBeat](https://venturebeat.com/security/12-ai-defenses-claimed-near-zero-attack-success-researchers-broke-all-of-them)
46. **Adaptive Attacks Break Defenses Against IPI** (NAACL 2025) — [arXiv:2503.00061](https://arxiv.org/pdf/2503.00061) · [ACL](https://aclanthology.org/2025.findings-naacl.395/)
47. **Generalization Limits of RL Alignment / compound cognitive overload** (2026) — [arXiv:2604.02652](https://arxiv.org/html/2604.02652)
48. **Prompt Injection & Jailbreak Techniques — Comprehensive Reference** (GitHub gist, Oct 2026) — [link](https://gist.github.com/kibotu/c06f54d6fbc4705e886a50fb2e59e6ae)
49. **SoK: PIAtlas — Decomposing the Unbounded Prompt Injection Attack Space** (2026) — [arXiv:2610.24999](https://arxiv.org/html/2610.24999)
50. **Security Concerns for LLMs: A Survey** (2025) — [arXiv:2505.18889](https://arxiv.org/html/2505.18889v5)

---

## C. Defence papers (training / runtime / architecture)

51. Guan et al. — **Deliberative Alignment** (OpenAI, Dec 2024) — [OpenAI](https://openai.com/index/deliberative-alignment/) · [arXiv:2412.16339](https://arxiv.org/abs/2412.16339) · [PDF](https://arxiv.org/pdf/2412.16339) · [Pith review](https://pith.science/paper/2412.16339) · [o1 System Card](https://cdn.openai.com/o1-system-card-20241205.pdf)
52. OpenAI — **From Hard Refusals to Safe-Completions (GPT-5)** (2025) — [PDF](https://cdn.openai.com/pdf/be60c07b-6bc2-4f54-bcee-4141e1d6c69a/gpt-5-safe_completions.pdf)
53. Zou et al. — **Improving Alignment and Robustness with Circuit Breakers** (NeurIPS 2024) — [arXiv:2406.04313](https://arxiv.org/pdf/2406.04313) · [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2024/file/97ca7168c2c333df5ea61ece3b3276e1-Paper-Conference.pdf) · [GitHub](https://github.com/GraySwanAI/circuit-breakers)
54. Huang et al. — **Vaccine: Perturbation-aware Alignment** (2024) — [arXiv:2402.01109](https://arxiv.org/html/2402.01109v5) · **T-Vaccine** [arXiv:2410.09760](https://arxiv.org/html/2410.09760v2)
55. **Harmful Fine-tuning Attacks and Defenses: A Survey** (2026) — [arXiv:2409.18169](https://arxiv.org/html/2409.18169v6) · [ACM](https://dl.acm.org/doi/10.1145/3817114) · **SafeLoRA/SafeMERGE** [arXiv:2503.17239](https://arxiv.org/html/2503.17239v1) · **PACT** [arXiv:2603.07445](https://arxiv.org/html/2603.07445) · **safety neurons** [arXiv:2508.09190](https://www.arxiv.org/pdf/2508.09190)
56. **Backtracking Improves Generation Safety** (2024) — [arXiv:2409.14586](https://arxiv.org/html/2409.14586) · **Extended-refusal** [arXiv:2505.19056](https://arxiv.org/html/2505.19056v2) · **rank-one injection** [arXiv:2508.20766](https://arxiv.org/html/2508.20766v1)
57. Xu et al. — **SafeDecoding** (ACL 2024) — [ACL](https://aclanthology.org/2024.acl-long.303/) · [arXiv:2402.08983](https://arxiv.org/html/2402.08983v2) · [GitHub](https://github.com/uw-nsl/SafeDecoding)
58. Robey et al. — **SmoothLLM** (2023/24) — [arXiv:2310.03684](https://arxiv.org/abs/2310.03684) · **RPO** [NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/46ed503889ab232c21c1162340ee17b2-Paper-Conference.pdf) · **SelfDefend** [USENIX 2025](https://daoyuan14.github.io/papers/USENIX25_SelfDefend.pdf)
59. Anthropic — **Constitutional Classifiers** (2025) + **CC++** (2026) — [CC](https://www.anthropic.com/research/constitutional-classifiers) · [next-gen](https://www.anthropic.com/research/next-generation-constitutional-classifiers) · [arXiv:2601.04603](https://arxiv.org/pdf/2601.04603) · [cheap monitors](https://alignment.anthropic.com/2025/cheap-monitors/) · [ACL 2025 note](https://en.papernotes.org/ACL2025/llm_alignment/constitutional_classifiers_defending_against_universal_jailbreaks_across_thousan/)
60. Hines et al. — **Spotlighting / Defending Against IPI** — [CEUR PDF](https://ceur-ws.org/Vol-3920/paper03.pdf)
61. Debenedetti et al. — **CaMeL: Defeating Prompt Injections by Design** (2025/26) — [arXiv:2503.18813](https://arxiv.org/abs/2503.18813v2) · [PDF](https://arxiv.org/pdf/2503.18813) · [GitHub](https://github.com/google-research/camel-prompt-injection) · [SATML 2026](https://www.computer.org/csdl/proceedings-article/satml/2026/785900a587/2jZks3ksGT6) · [Simon Willison](https://simonw.substack.com/p/camel-offers-a-promising-new-direction) · [InfoQ](https://www.infoq.com/news/2025/04/deepmind-camel-promt-injection/)
62. Gill et al. — **Multi-CaMeL** (Oct 2026) — [arXiv:2610.05640](https://arxiv.org/abs/2610.05640) · [HTML](https://arxiv.org/html/2610.05640)
63. **Tool-Input/Output Firewalls — minimize & sanitize** (2025) — [arXiv:2510.05244](https://arxiv.org/html/2510.05244v1) · **Task Shield** [ACL 2025](https://aclanthology.org/2025.acl-long.1435.pdf) · **adaptive out-of-band eval** [arXiv:2606.26479](https://arxiv.org/html/2606.26479v1)
64. **Guard models comparison 2026** — [aipromptshub](https://aipromptshub.co/safety/llama-guard-vs-shield-gemma) · [ICLR 2026 workshop benchmark](https://arxiv.org/html/2605.28830v1) · [Turing Post](https://www.turingpost.com/p/guardianmodels) · [Qwen3Guard report](https://arxiv.org/html/2510.14276v1) · [production cost guide](https://blog.prompt20.com/posts/production-safety-guardrails/) · [Red Hat false positives](https://developers.redhat.com/articles/2026/05/04/guardrails-enterprise-safety-shields-llama-stack) · [Prompt Guard model card](https://huggingface.co/meta-llama/Prompt-Guard-86M)
65. **OWASP Top 10 for LLM Applications 2025 PDF** — [official](https://owasp.github.io/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) · **2026 changes** [Superwise](https://superwise.ai/learn/owasp-top-10-for-llm-applications/) / [Aembit](https://aembit.io/blog/the-owasp-top-10-for-llm-applications-2026-what-changed-and-why-it-matters/) / [hackerdna](https://hackerdna.com/blog/owasp-llm-top-10) · **Agentic ASI list** [Swfte](https://www.swfte.com/ko/blog/owasp-llm-top-10-explained-for-engineers-2026) · **OWASP Cheat Sheet** [link](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
66. **Indirect Prompt Injection: Attacks, Defenses, 2026 SOTA** — [Zylos](https://zylos.ai/research/2026-04-12-indirect-prompt-injection-defenses-agents-untrusted-content/) · [Microsoft defender guide](https://learn.microsoft.com/en-us/security/zero-trust/sfi/defend-indirect-prompt-injection) · [Agent Patterns crosswalk](https://www.agentpatterns.ai/security/owasp-llm-top-10-2025-agent-crosswalk/) · [pwnedlabs incidents](https://pwnedlabs.io/blog/owasp-llm-top-10)
67. **Red-teaming ops / playbooks 2026** — [AI Red-Teaming Guide GitHub](https://github.com/requie/AI-Red-Teaming-Guide) · [prompt20](https://blog.prompt20.com/posts/how-to-red-team-an-llm/) · [datavlab](https://datavlab.ai/post/red-teaming-llms-practitioner-guide-2026) · [gov.capital](https://gov.capital/ai-red-teaming-in-2026-a-practical-field-guide/) · [DEV canary one-afternoon](https://dev.to/techsavant_lab/how-to-red-team-your-llm-app-in-one-afternoon-without-a-single-harmful-prompt-3cpi) · [qajobfit matrix](https://qajobfit.com/resources/red-teaming-an-llm-chatbot) · [MLflow defence guide](https://mlflow.org/articles/prompt-injection-defense/) · [AISafetyLab](https://github.com/thu-coai/AISafetyLab)

---

## D. Evaluation / over-refusal

68. Mazeika et al. — **HarmBench** (ICML 2024) — [glossary](https://www.giskard.ai/glossary/harmbench-harmful-content-attack) · [emergentmind](https://www.emergentmind.com/topics/harmbench)
69. Chao et al. — **JailbreakBench** (NeurIPS 2024 D&B) — [arXiv:2404.01318](https://arxiv.org/pdf/2404.01318) · [NeurIPS PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/63092d79154adebd7305dfd498cbff70-Paper-Datasets_and_Benchmarks_Track.pdf) · [project](https://jailbreakbench.github.io/)
70. Souly et al. — **A StrongREJECT for Empty Jailbreaks** (NeurIPS 2024) — [BAIR blog](https://bair.berkeley.edu/blog/2024/08/28/strong-reject/) · [arXiv:2402.10260](https://arxiv.org/pdf/2402.10260) · [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2024/file/e2e06adf560b0706d3b1ddfca9f29756-Paper-Datasets_and_Benchmarks_Track.pdf)
71. Röttger et al. — **XSTest** (NAACL 2024) — [ACL PDF](https://aclanthology.org/2024.naacl-long.301.pdf) · [arXiv](https://arxiv.org/html/2308.01263v3)
72. Cui et al. — **OR-Bench** (ICML 2025) — [arXiv:2405.20947](https://arxiv.org/html/2405.20947v1) · [PMLR](https://proceedings.mlr.press/v267/cui25a.html) · [GitHub](https://github.com/justincui03/or-bench)
73. **The Refusal–Compliance Tradeoff: A Large-Scale Safety Behavior Audit** (2026) — [arXiv:2605.05427](https://arxiv.org/html/2605.05427v2) · [arXiv abs](https://arxiv.org/abs/2605.05427)
74. **Concerns in Benchmarking Jailbreaks (ASR 96% → 2.7%)** (Oct 2026) — [arXiv:2610.26595](https://arxiv.org/abs/2610.26595)
75. **An Empirical Measurement of Jailbreaking Evaluators** (2026) — [arXiv:2609.10594](https://arxiv.org/pdf/2609.10594)
76. **MLCommons Jailbreak Benchmark v1.0** (Oct 2026) — [arXiv:2610.02827](https://arxiv.org/html/2610.02827v1)
77. **Safety for Whom? Boundary-Aware Self-Distillation** (2026) — [HuggingFace blog](https://huggingface.co/blog/MultiverseComputingCAI/safety-for-whom) · [arXiv:2609.04482](https://arxiv.org/html/2609.04482)
78. **DCR: Discern Truth from Falsehood (over-refusal via contrastive refinement)** (ICLR 2026) — [paper note](https://en.papernotes.org/ICLR2026/llm_safety/discern_truth_from_falsehood_reducing_over-refusal_via_contrastive_refinement/) · [ICLR PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/45a30141c6719e9cfedfb51f1c665a37-Paper-Conference.pdf)
79. **MT-JailBench** (2026) — [arXiv:2605.11002](https://arxiv.org/html/2605.11002v1) · **LLM-VA / ProSafePrune** [ACL 2026](https://aclanthology.org/2026.acl-long.260.pdf) / [ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/file/1fb591d5a6b1da9bd0d0648d122fe2a1-Paper-Conference.pdf)

---

## E. Context / inverse scaling / policy

80. **Jailbreak Archaeology 2022–2026: Policy Implications** — [FailureFirst](https://failurefirst.org/research/reports/31-jailbreak-archaeology-policy-implications/)
81. **The Paradox of Capability / Inverse Scaling** — [FailureFirst](https://failurefirst.org/research/reports/25-inverse-scaling-safety-policy/)
82. **Context Rot: Why Long-Context LLMs Degrade** (2026) — [TMLS](https://www.tmls.nyc/research/context-rot-mechanistic)
83. **Found in the Middle: Calibrating Positional Attention Bias** (ACL 2024) — [arXiv:2406.16008](https://arxiv.org/html/2406.16008v1) · [ACL](https://aclanthology.org/2024.findings-acl.890/)
84. **Do LLMs Follow Their Own Rules? A Reflexive Audit** (2026) — [arXiv:2604.09189](https://arxiv.org/html/2604.09189)
85. **DeepContext: Stateful Real-Time Detection of Multi-Turn Adversarial Intent Drift** (2026) — [arXiv:2602.16935](https://arxiv.org/html/2602.16935v1)
86. **Revisiting JBShield / Representation Trajectory Verification** (2026) — [Pith](https://pith.science/paper/2605.03095) · [EMNLP 2025 critique](https://aclanthology.org/2025.findings-emnlp.956.pdf)
87. **When LLM Defenses Backfire: Safety, Performance, Cost Trade-offs** (2026) — [arXiv:2607.24392](https://arxiv.org/html/2607.24392v1)
88. **LLM Jailbreak Statistics 2026** — [Axis Intelligence](https://axis-intelligence.com/llm-jailbreak-statistics/) · **Axis/other explainers** [groundtruth.day](https://groundtruth.day/learn/jailbreaking-and-red-teaming.html) · [orcarouter](https://www.orcarouter.ai/blog/llm-jailbreaks-explained)

---

## Note on citation quality

- **Primary sources** (papers, official blogs, model cards, benchmarks) pehle rakhe hain.
- **Secondary explainers** sirf wahan hain jahan primary ka summary ya production numbers the.
- Kai 2026 "papers" abhi preprint / under review hain — unke numbers ko **claims** ki tarah padho, established facts ki tarah nahi. Khaaskar: H-CoT, CoT Hijacking, SEAL, multi-CaMeL, aur kai guard-model comparisons.
- Jahan bhi koi ASR number hai, uske saath **judge, decoding params, attempt count** check karo — warna wo 96% vs 2.7% wala farak ho sakta hai (§6.2).
