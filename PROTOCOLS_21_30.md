# AI research protocols · Studies 21–30

**Marouane Mouhajar · Expert AI Researcher**
[marouane.mouhajar@gmail.com](mailto:marouane.mouhajar@gmail.com)

## Evidence, pilot and replication

These protocols combine published mechanisms into falsifiable experiments. The thresholds are proposed decision criteria. The figures model assumptions and do not report measured AI performance. A targeted source search supports the evidence summaries. Novelty remains to be established through full-text and artifact review.

Freeze model revision, tokenizer, context limit, prompting, split manifests, seed list and stopping rules. Split by underlying source or repository before generating variants. Audit duplicates and benchmark contamination. Use a pilot for variance estimates and a distinct confirmation set. Analyze paired differences at the source or repository level and account for seed variability. Require a confidence interval to clear each proposed effect and guardrail. Report all attempted cases, including refusals, timeouts and out-of-memory runs. For factorial experiments report the main effects, interaction and comparison against the best individual mechanism. Preserve data licenses and record actual compute, wall time, energy where available, and per-task failure reasons. Repeat promising results with a second model family and independent reviewers.

Start with Studies 21–23 on a fixed local document collection, including French and Darija examples where adequate independent labeling is available. Use a small open-weight model for the feasibility run and assess the ability to fit on the intended hardware before selecting model size. Store question IDs, source hashes, gold evidence, outputs, predictions, token counts and blinded review judgments.

## 21. Calibrated abstention for document assistants

**Evidence and hypothesis.** [Conformal Risk Control](https://research.google/pubs/conformal-risk-control/) controls expected monotone losses under its assumptions. [Semantic entropy](https://www.nature.com/articles/s41586-024-07421-0) estimates uncertainty across meanings. Test whether semantic entropy plus evidence agreement increases safe answer coverage over either score alone.

**Design and failure test.** Define loss as unsupported answers per offered question for conformal calibration. Separately report error among answered questions, which is a different denominator. Freeze model, clustering and calibration thresholds before testing. Split by source and time, compare single-score baselines, and test document drift. Advance if coverage improves 10 points at a fixed unsupported-answer budget and the answered-only error guardrail holds. Shared systematic errors can survive both scores.

**Calculation.** [Curve](ai-results/21-ai.svg) · [CSV](ai-results/21-ai.csv). The model assumptions are encoded in [the generator](ai_experiments.py).

## 22. Claim-level repair of AI citations

**Evidence and hypothesis.** [ALCE](https://aclanthology.org/2023.emnlp-main.398/) evaluates citation quality. [RARR](https://arxiv.org/abs/2210.08726) retrieves evidence and revises generations. Test selective repair of unsupported claims with an explicit revision budget and an abstention option.

**Design and failure test.** Compare answer-only retrieval, full revision and claim-selective repair at equal retrieval and token budgets. Have blinded raters check entailment, completeness and whether revisions introduce new errors. Hold out topics and source families. Advance if unsupported claim rate falls 20% relative to full revision without losing >5 points of answer completeness. Test repairs against contradictory sources and check whether claim splitting games the metric.

**Calculation.** [Curve](ai-results/22-ai.svg) · [CSV](ai-results/22-ai.csv). The model assumptions are encoded in [the generator](ai_experiments.py).

## 23. Hierarchical retrieval with contextual leaf embeddings

**Evidence and hypothesis.** [RAPTOR](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html) retrieves across a summary tree. [Late Chunking](https://arxiv.org/abs/2409.04701) derives contextual embeddings from larger text windows. Test whether context-aware leaves improve evidence recovery after hierarchical routing.

**Design and failure test.** Use hierarchy × contextual embedding factorial. Equalize retrieved tokens, reranker and generation settings. Label gold spans, include cross-section queries and report retrieval recall separately from answer quality. Require +5 points of span recall over both single mechanisms and cap index build cost at 1.5× the strongest baseline. Explicitly test routing errors and mismatched summary/leaf evidence.

**Calculation.** [Curve](ai-results/23-ai.svg) · [CSV](ai-results/23-ai.csv). The model assumptions are encoded in [the generator](ai_experiments.py).

## 24. Sampling until uncertainty stabilizes

**Evidence and hypothesis.** [SelfCheckGPT](https://arxiv.org/abs/2303.08896) compares sampled answers. [Semantic entropy](https://www.nature.com/articles/s41586-024-07421-0) clusters paraphrases by meaning. Test early stopping for easy cases while preserving detection of unsupported factual answers.

**Design and failure test.** Compare fixed K, budget-matched random allocation and sequential sampling on locked questions and generation settings. Learn stopping thresholds on calibration only. Evaluate AUPRC, missed unsupported answers at matched coverage and inference tokens. Advance at ≥25% fewer tokens with ≤2 points of recall loss at the operating threshold. Agreement can reflect a repeated falsehood. Include cases where early samples agree incorrectly.

**Calculation.** [Curve](ai-results/24-ai.svg) · [CSV](ai-results/24-ai.csv). The model assumptions are encoded in [the generator](ai_experiments.py).

## 25. Quantization-aware adapters under a fixed VRAM budget

**Evidence and hypothesis.** [QLoRA](https://arxiv.org/abs/2305.14314) trains adapters over quantized weights. [LoftQ](https://proceedings.iclr.cc/paper_files/paper/2024/hash/39ec972afab01e0d8ddc6834a9d12ac1-Abstract-Conference.html) initializes adapters alongside quantization. Test whether reallocating rank toward layers with larger residuals improves French and Darija task performance at matched parameter count.

**Design and failure test.** Compare uniform random, uniform LoftQ, residual-weighted random and residual-weighted LoftQ. Match the sum of r*(in+out), train tokens and stopping rules. Use source-disjoint held-out tasks and multiple seeds. Require +3 points on held-out task success over the best single mechanism with ≤2 points of general-domain degradation. Log peak VRAM and check that residual magnitude predicts downstream benefit.

**Calculation.** [Curve](ai-results/25-ai.svg) · [CSV](ai-results/25-ai.csv). The model assumptions are encoded in [the generator](ai_experiments.py).

## 26. Noise-aware preference training for multilingual assistants

**Evidence and hypothesis.** [DPO](https://arxiv.org/abs/2305.18290) directly optimizes pairwise preferences. [Robust DPO](https://arxiv.org/abs/2403.00409) addresses noisy labels under a model of label flips. Test calibrating label noise separately for French, English and Darija.

**Design and failure test.** Cross global versus group-specific noise estimates with vanilla DPO and robust DPO controls. Collect independent reannotations, hold out raters and source tasks, and simulate symmetric and systematic flips separately. Require +5 points in worst-group blinded win rate at matched tokens and ≥95% of baseline task correctness. Rater disagreement may reflect legitimate preferences rather than labeling error.

**Calculation.** [Curve](ai-results/26-ai.svg) · [CSV](ai-results/26-ai.csv). The model assumptions are encoded in [the generator](ai_experiments.py).

## 27. Adaptive draft length for exact speculative decoding

**Evidence and hypothesis.** [Speculative decoding](https://proceedings.mlr.press/v202/leviathan23a) verifies draft proposals while preserving the target distribution with its exact correction rule. [Medusa](https://arxiv.org/abs/2401.10774) explores multiple decoding heads. Test whether acceptance-aware scheduling across draft lengths improves latency for heterogeneous local workloads.

**Design and failure test.** Compare no speculation, best fixed lookahead and adaptive lookahead at identical sampling parameters. Verify toy target distributions and greedy parity. Use the exact acceptance and correction algorithm in every speculative arm. Measure p95 inter-token latency, throughput and energy under open-loop mixed arrivals. Advance at 15% p95 improvement with no throughput loss. High acceptance can still lose to draft overhead.

**Calculation.** [Curve](ai-results/27-ai.svg) · [CSV](ai-results/27-ai.csv). The model assumptions are encoded in [the generator](ai_experiments.py).

## 28. Independent tests for AI-generated bug fixes

**Evidence and hypothesis.** [SWE-bench](https://arxiv.org/abs/2310.06770) evaluates fixes on real issues. [Agentless](https://arxiv.org/abs/2407.01489) separates localization, repair and patch validation. Test independent test generation for functional Symfony and Python regressions.

**Design and failure test.** Compare existing tests, tests written by the patch generator and tests from a separate model that sees only the issue and original code. Use isolated execution with no network and maintainer-authored hidden tests as ground truth. Hold out repositories. Require a ≥20% reduction in false accepted patches at ≤10% loss in correct-patch acceptance. Evaluate the risk that both models reproduce the same misunderstanding.

**Calculation.** [Curve](ai-results/28-ai.svg) · [CSV](ai-results/28-ai.csv). The model assumptions are encoded in [the generator](ai_experiments.py).

## 29. Data triage using training dynamics and influence

**Evidence and hypothesis.** [Dataset Cartography](https://arxiv.org/abs/2009.10795) identifies example groups from training dynamics. [TracIn](https://arxiv.org/abs/2002.08484) approximates training-example influence. Test allocating a limited label-audit budget by combining both signals.

**Design and failure test.** Compare random audit, uncertainty-only, influence-only and combined selection on a labeled multilingual classification corpus. Blind annotators and keep an independent audit target separate from final evaluation. Match review budget and retraining tokens. Require +3 points of macro-F1 at equal audit budget. Track discarded hard examples and rare-label recall to catch feedback loops.

**Calculation.** [Curve](ai-results/29-ai.svg) · [CSV](ai-results/29-ai.csv). The model assumptions are encoded in [the generator](ai_experiments.py).

## 30. Small replay buffers for continual AI learning

**Evidence and hypothesis.** [Gradient Episodic Memory](https://ai.meta.com/research/publications/gradient-episodic-memory-for-continual-learning/) uses episodic examples to mitigate forgetting. [Learning without Forgetting](https://arxiv.org/abs/1606.09282) distills prior outputs. Test replay plus distillation for sequential local adapter updates.

**Design and failure test.** Compare sequential fine-tuning, replay, distillation and both with fixed training steps, plus a joint-training reference. Rotate task orders and separately report new-task gain, old-task accuracy and backward transfer. Advance if mean old-task loss falls ≥30% relative to the best single arm without >2 points of new-task degradation. Include storage and teacher-forward compute in the budget.

**Calculation.** [Curve](ai-results/30-ai.svg) · [CSV](ai-results/30-ai.csv). The model assumptions are encoded in [the generator](ai_experiments.py).
