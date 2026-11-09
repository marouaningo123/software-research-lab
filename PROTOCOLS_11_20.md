# Software Research Lab · Studies 11–20

**Marouane Mouhajar · Expert AI Researcher**
[marouane.mouhajar@gmail.com](mailto:marouane.mouhajar@gmail.com)

## Experimental design

This second wave covers local AI inference, software delivery and distributed services. The papers establish the source mechanisms. The combinations and thresholds below are research proposals. The curves are analytical scenarios. There are no measured prototype results in this wave.

1. Reproduce a strong published or production-like baseline and log all dependencies, versions, hardware, workloads and seeds.
2. Pilot to estimate variability, then freeze the primary metric, threshold, guardrails and analysis. Split by workload family or project. Randomize run order and compare paired independent runs under the same resource and tuning budgets.
3. Report confidence intervals on paired effects. Include timed-out, cancelled and failed work in the denominator. Treat an interval crossing a gate as inconclusive. For factorial designs, separately estimate the interaction and compare the combination to the best single component.
4. Run the specified failure cases and ask a second team to rerun promising results. Record close prior art and publish negative results. A systematic novelty review is pending.

## 11. Risk-calibrated LLM routing

**Evidence and hypothesis.** [RouteLLM](https://arxiv.org/abs/2406.18665) learns model preferences for routing. [FrugalGPT](https://arxiv.org/abs/2305.05176) explores cascades. Combine confidence gating with a separate error budget for code edits, factual answers and extraction. Cascades and routers are established. The test is whether group-specific risk constraints survive workload drift.

**Experiment.** Replay time-ordered, labeled tasks through strong-only, cheap-only, global threshold and per-task threshold arms. Include retry and verification costs. Hold out whole repositories and prompt families, blind reviewers and report worst-group correctness with confidence bounds.

**Decision and critique.** Advance if cost per correct task falls ≥20% against strong-only while ruling out a >2-point correctness drop per supported group. A router trained on easy examples can look cheap by routing rare hard tasks badly.

**Model curve.** Assumes $12 and $2 per thousand strong and cheap requests. Fifteen percent of cheap requests escalate. [SVG](wave2-results/11-routing.svg) · [CSV](wave2-results/11-routing.csv)

## 12. Evidence-preserving prompt compression

**Evidence and hypothesis.** [LLMLingua](https://arxiv.org/abs/2310.05736) compresses prompts. [Lost in the Middle](https://arxiv.org/abs/2307.03172) reports sensitivity to evidence placement. Test preserving attributed evidence spans and moving them to favorable positions while compressing the rest.

**Experiment.** Use a compression × ordering factorial with fixed model, token budget and retrieval pool. Randomize evidence position, test single- and multi-document questions and adversarial distractors, and score answer and citation correctness independently.

**Decision and critique.** Advance at ≥25% fewer input tokens versus uncompressed retrieval with a ≤2-point citation accuracy loss. Require the combination to outperform a budget-matched ordering-only control on grounded answers. Oracle spans would overstate real performance.

**Model curve.** The 8,000-token context contains 1,000 evidence tokens and 7,000 background tokens. Background is compressed to 40%. [SVG](wave2-results/12-compression.svg) · [CSV](wave2-results/12-compression.csv)

## 13. Deadline-aware prefix reuse for local LLMs

**Evidence and hypothesis.** [SGLang](https://arxiv.org/abs/2312.07104) reuses prefix states. [Orca](https://www.usenix.org/conference/osdi22/presentation/yu) schedules generation at iteration granularity. Test a bounded scheduling preference for shared prefixes under mixed interactive and batch traffic.

**Experiment.** Compare arrival order, shortest estimated work, prefix-first and deadline-bounded prefix reuse. Replay identical open-loop arrivals and vary shared prefix lengths, workload mix, cancellations and KV-cache pressure. Measure per-class p99 time to first token and deadline goodput.

**Decision and critique.** Advance at ≥15% interactive deadline goodput improvement versus the strongest baseline under equal memory, with a fixed batch completion floor. Reuse can starve unique prompts and cache lifetime must respect tenant boundaries.

**Model curve.** A 2,000-token prompt has a reusable 1,500-token prefix. The figure omits cache management and queueing. [SVG](wave2-results/13-prefix.svg) · [CSV](wave2-results/13-prefix.csv)

## 14. Latency-budgeted local model offload

**Evidence and hypothesis.** [FlexGen](https://proceedings.mlr.press/v202/sheng23a/sheng23a.pdf) evaluates offload for throughput. [Orca](https://www.usenix.org/conference/osdi22/presentation/yu) evaluates iteration-level serving. Test whether admitting batches by transfer cost prevents interactive stalls on one modest GPU.

**Experiment.** Use one GPU with fixed VRAM and identical model precision across static offload, throughput-oriented batching and budgeted batching. Vary prompt and output lengths, pinned memory availability and contention. Measure transfer bytes, peak host/device memory and p95 inter-token latency.

**Decision and critique.** Advance at ≥15% more batch tokens per hour than fixed interactive reservations while meeting a preregistered interactive latency ceiling. PCIe transfer overlap must be measured separately.

**Model curve.** Uses decimal units and models transfer-only time with no overlap or fixed overhead. [SVG](wave2-results/14-offload.svg) · [CSV](wave2-results/14-offload.csv)

## 15. Fault-tested rolling schema changes

**Evidence and hypothesis.** [F1 online schema change](https://research.google/pubs/online-asynchronous-schema-change-in-f1/) supplies a staged schema protocol. [Sieve](https://www.usenix.org/conference/osdi22/presentation/sun) perturbs controller observations. Test perturbing migration checkpoints while application versions overlap.

**Experiment.** In disposable PostgreSQL environments run expand, dual-write, resumable backfill, validation, switch and contract. Compare normal deploy tests, random process kills and checkpoint-targeted faults. Inject stale reads, duplicates and crashes between data writes and watermark commits. Compare against a version-aware reference model.

**Decision and critique.** Advance if targeted faults find ≥25% more distinct reproducible defects per runner-hour than random faults. The test oracle must distinguish legal transitional reads from lost updates.

**Model curve.** Constant-rate floor with no lock contention, retries or maintenance windows. [SVG](wave2-results/15-migration.svg) · [CSV](wave2-results/15-migration.csv)

## 16. Change-directed stateful API fuzzing

**Evidence and hypothesis.** [RESTler](https://www.microsoft.com/en-us/research/publication/restler-stateful-rest-api-fuzzing/) infers producer-consumer dependencies. [AFLGo](https://research.monash.edu/en/publications/directed-greybox-fuzzing/) prioritizes target code. Test change proximity as a seed scheduler for schema-valid API sequences.

**Experiment.** Build a local API Platform fixture with disposable databases and an OpenAPI spec. Compare breadth-first sequences, unguided dependency-aware fuzzing and changed-handler guidance at matched request and CPU budgets. Include known historical fixes and hold out releases. Detect invariant failures beyond HTTP 500.

**Decision and critique.** Advance with ≥25% more distinct confirmed regressions per hour. Track unchanged-endpoint coverage and test whether shared service changes make handler proximity misleading.

**Model curve.** Illustrative branching at exact depth. Dependencies, invalid states and equivalent sequences change actual search cost. [SVG](wave2-results/16-api-fuzz.svg) · [CSV](wave2-results/16-api-fuzz.csv)

## 17. Refactor-aware code review for PHP

**Evidence and hypothesis.** [GumTree](https://www.labri.fr/perso/xblanc/data/papers/ASE14.pdf) produces syntax-tree edits. [RefactoringMiner](https://users.encs.concordia.ca/~nikolaos/publications/TSE_2020.pdf) evaluates refactoring detection. Test a view that groups verified moves and renames while retaining access to the original diff.

**Experiment.** Build a labeled corpus of licensed PHP commits with mixed refactors and behavioral changes. Compare line diffs, syntax edits and grouped views in a counterbalanced review task. Hold out projects and include Doctrine metadata changes, dynamic method calls and moves with embedded behavior changes.

**Decision and critique.** Advance if median review time drops ≥20% and the lower confidence bound rules out a >5-point drop in defect detection. Never hide a change on a grouping heuristic alone.

**Model curve.** Linear illustrative time allocation for a fixed edit workload. Human review time requires a study. [SVG](wave2-results/17-diff.svg) · [CSV](wave2-results/17-diff.csv)

## 18. Rare incident capture under a fixed telemetry budget

**Evidence and hypothesis.** [Canopy](https://www.microsoft.com/en-us/research/publication/canopy-an-end-to-end-performance-tracing-and-analysis-system/) supports end-to-end tracing and analysis. [Sifter](https://www.microsoft.com/en-us/research/publication/sifter-scalable-sampling-for-distributed-traces-without-feature-engineering/) and [STEAM](https://www.microsoft.com/en-us/research/publication/steam-observability-preserving-trace-sampling/) already address informative sampling. Test adding per-service budget floors for newly deployed and low-volume services.

**Experiment.** Replay synthetic and licensed traces with labeled rare faults. Compare uniform, error/latency tail sampling, dissimilarity sampling and dissimilarity plus service floors at equal stored bytes. Track incomplete traces, collector memory, classification delay and rare incident recall.

**Decision and critique.** Advance if rare incident recall rises ≥15 points without a >5-point drop on frequent incidents. A burst of novel but harmless traffic can consume the budget.

**Model curve.** Independent uniform sampling model. Correlated decisions and tail policies need replay. [SVG](wave2-results/18-traces.svg) · [CSV](wave2-results/18-traces.csv)

## 19. Sketch-first reconciliation for offline replicas

**Evidence and hypothesis.** [Invertible Bloom lookup tables](https://arxiv.org/abs/1101.2245) support probabilistic recovery of sparse differences. [DottedDB](https://ieeexplore.ieee.org/document/8069082/) demonstrates an alternative anti-entropy design with causal metadata. Test a sketch fast path and a deterministic repair fallback for small disconnected replicas.

**Experiment.** Compare full inventory, deterministic range comparison and sketch-first repair using identical versioned records. Verify convergence with a canonical digest and force fallback on decode failure. Include collisions, deletes, simultaneous updates and prolonged disconnection. Digests must cover versions and deletions, not just live keys.

**Decision and critique.** Advance if median repair bytes fall ≥30% against deterministic range comparison without incorrect convergence. Report worst-case wire overhead and repair latency with failed sketches.

**Model curve.** Two 32-byte cells and a 16-byte identifier per difference are planning assumptions. Excludes record bodies and fallback. [SVG](wave2-results/19-reconcile.svg) · [CSV](wave2-results/19-reconcile.csv)

## 20. Retry budgets for metastable overload

**Evidence and hypothesis.** [Metastable Failures in the Wild](https://www.usenix.org/publications/loginonline/metastable-failures-wild) documents self-sustaining overload. [Sieve](https://www.usenix.org/conference/osdi22/presentation/sun) targets timing and observation perturbations in controllers. Transfer targeted perturbation to retry feedback loops in an API and its worker queue.

**Experiment.** Compare fixed retries, capped exponential backoff with jitter, fixed retry budgets and adaptive budgets. Apply matched offered traffic and timed dependency slowdowns, stale backlog readings and recovery-phase bursts. Measure time until sustained baseline goodput returns and count suppressed requests.

**Decision and critique.** Advance if recovery time drops ≥30% versus the best fixed baseline with a preregistered floor for completion of retryable work. A low retry count can conceal dropped useful work.

**Model curve.** Independent timeout scenario with at most two retries. The capped line is an offered-load bound, with no completion or recovery claim. [SVG](wave2-results/20-overload.svg) · [CSV](wave2-results/20-overload.csv)
