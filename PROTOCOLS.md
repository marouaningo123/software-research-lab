# Ten research protocols in computer science and software engineering
## Companion portfolio | 9 November 2026

This portfolio targets software reliability, operating cost and maintainability. The lead prototype uses a stack familiar to PHP teams: Symfony Messenger, PostgreSQL and RabbitMQ. The other protocols cover storage, operating systems and computer architecture. The literature screen draws on specialized conference papers and implementation records. Some papers are well known within their fields. Media visibility and citation rarity were not measured.

These are experimental protocols. The numerical examples are dimensional or statistical checks with explicit assumptions. No prototype benchmarks, simulations or independent reviews were conducted for this edition.

## Wave 1 — From published result to testable question

Each protocol combines mechanisms demonstrated separately, or transfers a mechanism to a specific workload with constraints that the source evaluation did not establish. Existing implementations count as prior art. An engineering contribution can be a reproducible comparison or a measured boundary at which an existing approach stops paying off. The closest known overlap is identified where the search found one. Search coverage was targeted. Before a publication claim, extend it to full-text papers, proceedings, theses, references and competing artifacts, and document inclusion and exclusion decisions.

## Wave 2 — Common experimental design

- Freeze hypotheses, primary metrics, exclusions, failure semantics, dataset provenance, build revisions and a baseline tuning budget. Separate development from confirmation by service, repository, workload family or trace period as specified. Compare at equal resource, durability and correctness budgets.
- Use isolated networks, licensed public datasets or generated data and synthetic secrets. Pin container and compiler versions, hardware topology, storage firmware, settings and seeds. Store manifests, scripts, fault schedules, raw outputs, elapsed time and commands for regenerating every table.
- Report the actual experimental unit. Requests inside one process run are correlated. Replay identical inputs across arms and randomize run order across clean-state blocks. Report paired effects across independent blocks with confidence intervals. Size confirmatory runs from a pilot and retain pilot runs separately. Report per-workload results alongside aggregate estimates. Keep timeouts and failures in the denominator.
- For factorial tests, estimate the interaction as Y11 − Y10 − Y01 + Y00 on a prespecified scale. Directly compare the combination to both components. Require the prespecified confidence bound to clear the performance gate and its guardrails. Treat failure to clear a bound as inconclusive unless evidence supports a material negative effect. Apply a multiplicity procedure when asserting several superiority findings from the same experiment.
- Run open-loop arrivals when measuring a service under overload, timestamp at the offered arrival or report generator lateness separately, and count failed requests. Record CPU time, wall time, peak memory, writes and restarts where applicable. Lock machine and workload budgets before viewing holdout results. Publish negative results and identify all untested environments.

## 01. Crash-safe Symfony Messenger workflows with bounded deduplication state

**Published inputs.** Beldi attaches durable execution and transaction mechanisms to serverless functions. Boki implements stateful serverless abstractions using a shared log. Neither result alone establishes an external side-effect guarantee for a conventional broker and SQL application. Research question: can combining SQL-recorded workflow steps with log-style checkpointing make retries cheaper than an append-only durable ledger while preserving the same invariants? [Beldi, OSDI 2020](https://www.usenix.org/conference/osdi20/presentation/zhang-haoran) · [Boki, SOSP 2021](https://pdos.csail.mit.edu/6.5840/papers/jia21sosp-boki.pdf)

**Implementation.** Build an order reservation workflow on a test database with stable workflow and step IDs. Commit the local domain update, step ledger and outbox in one SQL transaction. A separate relay publishes the outbox and retries ambiguous sends. A consumer deduplicates by stable event ID, with the deduplication record committed atomically with its local mutation. A synthetic external service supports explicit idempotency keys and durable lookup. Include a deliberately non-idempotent service to expose the boundary at which an ambiguous timeout requires reconciliation. Terminal workflow tombstones or an equivalent durable epoch/fencing scheme must prevent stale replays after compaction. Define maximum accepted message age across normal retries, dead letters and manual replays before deleting any deduplication state. Assert that messages beyond the supported horizon are quarantined.

**Sizing.** An illustrative 1,000 completed step IDs/min × 60 × 24 × 7 gives 10.08 million IDs per week. At 160 B per record that is 1.61 GB of logical payload before indexes, page overhead, WAL or replicas. A deployment decision requires observed disk use and reclaim behavior after steady-state retention. For zero failures in 3,000 independent scenarios the exact one-sided 95% upper binomial bound is about 0.10% for the sampled scenario distribution. Similar schedules from one fault family do not represent independent coverage of production failures.

**Controlled test.** Compare ordinary retry handling as a diagnostic control, durable inbox/outbox with an append-only ledger as the correctness baseline, and the checkpointed variant. Run paired schedules for relay crashes before/after broker confirmation, consumer crashes before/after database commit, duplicate and reordered delivery, ambiguous external acknowledgments, database failover and late replays after compaction. Include concurrent updates to one aggregate and an outage long enough to fill the backlog. Verify conservation of inventory, at most one committed reservation per command, no lost accepted commands under the declared recovery model, and equivalent final state against a reference state machine. Record offered and completed throughput, 99th-percentile end-to-end latency, backlog drain time and bytes per completed workflow. Start with 30 fault schedules in each family to debug the harness. Use frozen independent scenario generators for confirmation. Add bounded exhaustive exploration of the smallest two-worker model as a distinct check.

**Advance if** all correctness oracles pass, storage per completed workflow falls by at least 30% over steady state versus the durable baseline, and p99 latency grows by no more than 10% at the same offered load. Publish minimized failing histories. Replicate with two PostgreSQL deployments and a second workload. Payment, email and third-party APIs each require their own side-effect contract.

## 02. Coverage-guided fault injection for message-driven services

**Published inputs.** FoundationDB describes deterministic simulation in a distributed transactional store. Mallory uses feedback to guide distributed fault injection. Combine deterministic event capture with feedback on domain-state transitions. Mallory already guides faults adaptively. The proposed contribution is an evaluation of business-level feedback in a brokered application with realistic retry behavior. [FoundationDB, SIGMOD 2021](https://www.foundationdb.org/files/fdb-paper.pdf) · [Mallory paper](https://arxiv.org/abs/2305.02601)

**Mechanism and calculation.** Instrument a controllable clock, delivery order and service responses. A useful feedback signal might be a newly observed transition through timeout, recovery or reconciliation rather than a new source line. A schedule with 12 eligible sites and 3 distinct fault types has 36 possible single faults and 594 unordered pairs at distinct sites before timing and ordering are varied. Exhaustive testing grows quickly even in this small model.

**Protocol.** Compare uniform random injection, fixed fault suites, trace-event feedback and domain-state feedback with matched CPU budgets. Use held-out real bug histories where reproducible and a separately curated mutation set. Keep designers of feedback blind to held-out defects. Randomize seeds in paired runs, cap wall time, score only oracle-confirmed distinct root causes, and report time to first bug with censoring. Replay discoveries in real broker containers to audit simulator fidelity.

**Advance if** domain feedback finds ≥25% more unique confirmed defects per CPU-hour than the best comparator with at least 90% reproducible counterexamples. Count duplicates and synthetic mutants separately. Reject feedback that only rewards more instrumented paths or exploits the simulator.

## 03. Record-and-replay escalation for rare integration-test failures

**Published inputs.** rr demonstrates deployable user-space record/replay. PANDA supports recording and deeper inspection at whole-system scope. Evaluate a CI policy that allocates heavier capture to tests with demonstrated kernel or dependency interactions. Re-running an unrecorded failure can miss its original schedule. [rr, USENIX ATC 2017](https://www.usenix.org/conference/atc17/technical-sessions/presentation/ocallahan) · [PANDA research](https://www.ll.mit.edu/r-d/publications/repeatable-reverse-engineering-greater-good-panda)

**Calculation.** With illustrative total per-test cost 1.2× native under light recording and 3× native under whole-system recording, applying the latter to 10% of equally costly tests gives 0.9×1.2 + 0.1×3 = 1.38× native cost before triage. If the expensive tests dominate runtime, count by native CPU time and resource occupancy.

**Protocol.** Compare ordinary logs with targeted reruns, always-light recording, always-whole-system recording and a tiered policy chosen before the test runs. Use the same VM/container topology for matched comparisons where tools permit. Include thread ordering, filesystem timing, client/server interaction and timeouts. Report captured original failures per CPU-hour, replay fidelity, bytes per run and recording-induced changes in observed failure rate. Assess diagnosis time with blinded reviewers on randomized bugs if feasible. Preflight CPU/tool support, and record only synthetic credentials and data.

**Advance if** at least 90% of failures replayable under always-heavy capture are reproducible from the tiered run, with ≥30% less compute than always-heavy recording. Check whether instrumentation changes scheduling enough to suppress the failures it is meant to preserve.

## 04. Incremental access and entitlement views with bounded memory

**Published inputs.** Differential dataflow supports incremental iterative computation. Noria evaluates partially stateful views for web workloads. Test demand-driven materialization of frequently read tenant subgraphs combined with incremental maintenance of nested entitlement relations. Add correctness conditions for access revocation during partitions. [Differential dataflow, CIDR 2013](https://www.microsoft.com/en-us/research/publication/differential-dataflow/) · [Noria, OSDI 2018](https://www.usenix.org/conference/osdi18/presentation/gjengset)

**Calculation.** Ten million materialized relation tuples at an illustrative 48 bytes each need 480 MB of payload before indexes and allocator overhead. A single update affecting 50,000 derived tuples at 10 µs per tuple requires 0.5 CPU-seconds even with zero scheduling overhead. Skew and revocation fan-out should appear explicitly in the workload.

**Protocol.** Compare indexed recursive SQL, fully maintained materialization, demand-only caching and a hybrid. Use generated hierarchies with cycles, dense group membership, multi-tenant traffic and permission revocation. Cross-check answers at the same committed version against a reference recursive evaluator. Version the authorization state, require strong verification or fail closed when freshness cannot be established, and report rejected requests. Measure p99 latency, update backlog, stale-answer rate and peak memory at equal CPU budget. Include cold-cache reads and cache churn.

**Advance if** peak memory falls ≥25% versus full materialization and p99 falls ≥20% versus indexed SQL on the intended read-heavy mix, with zero incorrect authorizations and a preregistered availability floor under fault injection. Publish the fan-out region where the hybrid loses.

## 05. Regeneration-cost-aware API caching

**Published inputs.** TinyLFU uses frequency estimates to govern admission. S3-FIFO evaluates queue-based eviction on a broad trace corpus. CacheSack optimizes flash-cache admission by traffic categories. TinyUFO already combines TinyLFU admission and S3-FIFO eviction. The proposed study isolates the incremental value of bounded regeneration-cost awareness in multitenant API workloads. [TinyLFU](https://cris.bgu.ac.il/en/publications/tinylfu-a-highly-efficient-cache-admission-policy/) · [S3-FIFO, SOSP 2023](https://pdl.cmu.edu/PDL-FTP/Storage/FIFOqueues-SOSP23_abs.shtml) · [CacheSack, USENIX ATC 2022](https://www.usenix.org/conference/atc22/presentation/yang-tzu-wei) · [TinyUFO prior implementation](https://docs.rs/TinyUFO/latest/tinyufo/)

**Mechanism.** Prioritize entries by bounded estimated reuse × avoidable backend CPU / resident bytes, with explicit tenant limits. Example: 100 expected reuses × 5 ms for 10 KiB implies 50 ms/KiB of expected avoided CPU. Ten expected reuses × 60 ms for 100 KiB gives 6 ms/KiB. The score is a heuristic. Actual value depends on TTL, invalidations and contention. Derive estimates only from observations available at decision time.

**Protocol.** Compare LRU, frequency-only admission, S3-FIFO, the existing admission/eviction combination and cost-aware admission at the same memory budget including metadata. Start with trace replay, then run a real API harness with heterogeneous SQL costs, burst scans, tenant shifts and cold starts. Use chronological holdout and hold out tenants. Keep TTLs, correctness and tenant isolation fixed. Track backend CPU per offered request, p99, per-tenant penalties and prediction overhead.

**Advance if** backend CPU drops ≥15% at the same memory budget versus the strongest baseline and no qualifying tenant has >5% worse p99. Report performance when costs drift rapidly or an adversarial tenant repeatedly requests expensive one-off keys.

## 06. Compaction and value separation for event-state storage

**Published inputs.** WiscKey separates keys from values to reduce I/O amplification. Dostoevsky studies adaptive removal of unnecessary LSM merges. Evaluate their interaction on update-heavy application-state data. Compare against integrated blob storage when present in the selected baseline version. [WiscKey, FAST 2016](https://www.usenix.org/conference/fast16/technical-sessions/presentation/lu) · [Dostoevsky, SIGMOD 2018](https://stratos.seas.harvard.edu/publications/dostoevsky-better-space-time-trade-offs-lsm-tree-based-key-value-stores)

**Calculation.** For an illustrative 1 KiB value and 32 B key-plus-pointer, four rewrites of all 1,056 B imply 4,224 B rewritten per logical update. Four 32 B pointer rewrites plus one 1,024 B value append imply 1,152 B before garbage collection. Any background rewriting or overhead difference must be counted before interpreting savings.

**Protocol.** Use one engine with four configurations: fixed/adaptive compaction × inline/separated values, plus its best supported production-like tuned configuration. Sweep object size, update skew, range scan share and TTL. Match durability, snapshots, compression and RAM. Run long enough for several reclamation cycles and report host and device writes separately where counters permit. Inject crashes during garbage collection and verify surviving state against durable acknowledged operations.

**Advance if** host bytes per accepted logical byte fall ≥20% versus the best single component, p99 scans increase by ≤10% and space amplification remains within a fixed budget. A test finishing before reclamation can falsely show reduced writes.

## 07. Interference-aware throttling for API and worker co-location

**Published inputs.** Shenango evaluates rapid core allocation for latency-sensitive services. Caladan detects and mitigates shared-resource interference on much finer timescales than a typical application controller. Their techniques overlap. The transfer question concerns how much of the isolation benefit is achievable with a slower, deployable controller using worker concurrency and CPU limits. [Shenango, NSDI 2019](https://www.usenix.org/system/files/nsdi19-ousterhout.pdf) · [Caladan, OSDI 2020](https://www.usenix.org/system/files/osdi20-fried.pdf)

**Calculation.** If a background job consumes 0.08 CPU-seconds, four core-equivalents have a CPU-only upper bound of 50 jobs/s. Reserving one core-equivalent reduces it to 37.5 jobs/s under that simplification. CPU quota, memory bandwidth and database contention can lower achievable throughput further.

**Protocol.** On a Linux host run an API and CPU-heavy or memory-heavy background workers. Compare fixed reservations, a queue-depth controller, a latency-only controller and a controller that also measures pressure or bandwidth indicators. Match offered API traffic and background backlog. Randomize burst onset, tune only on training bursts and test sustained load, sensor delay and resource saturation. Report API deadline misses, background jobs/hour and maximum starvation time. Include a safe fixed-cap fallback.

**Advance if** background goodput improves ≥15% versus fixed isolation without increasing API deadline misses by more than a prespecified absolute margin. Require bounded starvation. Inspect oscillations and report the burst durations at which a user-space controller reacts too late.

## 08. Reviewable stale-flag removal in PHP

**Published inputs.** Piranha automates stale feature flag cleanup. Coccinelle evaluates declarative semantic patches on cross-cutting C API changes. Transfer semantic preconditions and match explanations to PHP cleanup across typed wrappers, configuration and dependency injection. PolyglotPiranha already generalizes across languages. PHP-specific semantic safety and measured maintainer effort are the research questions. [Piranha research and artifacts](https://github.com/uber/piranha) · [Coccinelle evaluation, EuroSys 2008](https://coccinelle.gitlabpages.inria.fr/website/papers/eurosys08.pdf)

**Calculation.** At 100 cleanup candidates, 3 minutes per review and 5 minutes for each of 8 rejected changes, candidate review costs 340 minutes before rule authoring. Automated throughput without review cost says little about team savings.

**Protocol.** Compare manual edits, syntax-only transformations and guarded rules. Build a labeled benchmark from licensed historical PHP revisions and synthetic edge cases. Hold out repositories and flag wrapper styles. Freeze the intended terminal state and use baseline execution with flags pinned as the comparison oracle. Test side effects of flag evaluation, dynamic dispatch, tenant-specific flags, serialized config, aliases and unreachable branches. Have two maintainers independently assess changed behavior. Report coverage, false edit rates, abstentions and review minutes including rule authoring amortization.

**Advance if** no high-severity behavior changes are observed, median maintainer time falls ≥30% and coverage reaches ≥60% of independently labeled removable flags. A syntactically plausible patch must remain reviewable even when tests pass.

## 09. Adaptive fast-tier storage with an explicit write budget

**Published inputs.** Sibyl applies online reinforcement learning to hybrid-storage placement. CacheSack evaluates traffic-class admission under practical flash-cache costs. Test whether a hard promotion budget with simple class-aware feedback captures enough benefit to justify deployment on constrained edge servers. [Sibyl, ISCA 2022](https://arxiv.org/abs/2205.07394) · [CacheSack, USENIX ATC 2022](https://www.usenix.org/conference/atc22/presentation/yang-tzu-wei)

**Calculation.** A 20 GB/day logical promotion budget allows about 4.88 million 4 KiB promotions per day, roughly 56.5/s averaged over 24 h. This budget covers logical admissions. Physical flash writes also depend on internal write amplification and normal writes. Require separate device counters or explicitly report the measurement gap.

**Protocol.** Use a read-through cache with the authoritative backing store retained. Compare LRU, static class-aware admission, adaptive unbudgeted placement and adaptive budgeted placement. Add a hard-budget variant of the strongest simple policy. Run identical capacity and write budgets where the comparison is intended to isolate policy. Test scans, phase shifts, mixed sequential/random I/O and restarts. Separate trace simulation from physical NVMe/slow-tier measurements. Report p99 read latency, device writes and upstream I/O.

**Advance if** p99 is ≥15% better than the best equal-budget comparator and measured physical writes stay within the device budget. Report sensitivity to budget size and delayed adaptation. Include cache loss and stale-version checks.

## 10. Fairness-aware hardware prefetching

**Published inputs.** Pythia trains online prefetch decisions using memory-bandwidth-aware feedback. MISE estimates slowdown from shared-memory interference. Test whether a slowdown-based guardrail can protect co-running workloads even when aggregate bandwidth looks acceptable. Simulator results and estimates require validation against isolated execution. [Pythia, MICRO 2021](https://arxiv.org/abs/2109.12021) · [MISE, HPCA 2013](https://www.istc-cc.cmu.edu/publications/papers/2013/mise-hpca13.pdf)

**Calculation.** If a workload runs at 2.0 instructions/cycle alone and 1.2 when co-scheduled, its equal-work slowdown is about 1.67×, assuming comparable clocks and progress. If a controller raises shared IPC to 1.4, slowdown becomes about 1.43×. Compare estimated and measured slowdowns, and account for asymmetric harm across cores.

**Protocol.** Reproduce each source mechanism in a simulator that models multi-core memory arbitration and exposes priority sampling. Compare no prefetch, a standard fixed prefetcher, Pythia, MISE-style bandwidth arbitration without learned prefetch and a combined controller. Match storage overhead and prefetch degree limits, including bookkeeping and estimation intervals. Use workload mixes stratified by memory sensitivity and hold out benchmark families. Measure weighted speedup, worst-core slowdown, wasted traffic and estimator error over multiple intervals and mixes. Confirm results in a second configuration with different DRAM channel counts.

**Advance if** the combined controller lowers worst-core slowdown ≥10% versus the best competitive performance baseline with ≤3% weighted-speedup loss and bounded storage and traffic overhead. A biased slowdown estimate may protect the wrong core. Run an oracle controller with isolated-rate knowledge to separate estimator limits from policy limits.

## Wave 3 — Critique and order of execution

| Priority | Candidate | Earliest decisive check |
|---|---|---|
| First | 01 Messenger durability | Can a late replay after compaction duplicate a committed effect? |
| First | 05 API caching | Does cost-aware admission beat existing policy on held-out backend CPU? |
| Next | 02 Fault testing | Do discovered failures reproduce on the real broker? |
| Next | 08 PHP refactoring | Can a flag getter have a side effect the rewrite erases? |
| Next | 04 Access views | Do deletions and revocations maintain the same authorization result? |
| Later | 03 CI replay | Does recording suppress the failure it should capture? |
| Later | 06 Compaction | Does the write reduction survive reclamation? |
| Later | 07 Co-location | Does controller delay erase the latency benefit during bursts? |
| Later | 09 Storage tiers | Does the physical write budget survive phase changes? |
| Later | 10 Prefetch | Does measured slowdown agree with estimated slowdown? |

**Prototype order for Study 01.** First write the reference state machine and a failing test for the commit-before-ack window. Implement the durable baseline and use crash injection to validate its semantics. Then add checkpointing and the late-message fence, measure storage and recovery against the baseline, and repeat with a different workload. Package the failure traces, commit IDs, run scripts and raw measurements for independent reproduction.

**Before submission.** Obtain full source methods and reproducibility artifacts, finish a documented prior-art search per protocol, verify artifact and dataset licenses, freeze the analysis and obtain external statistical and engineering review. The portfolio supports deciding what to build and what evidence would change that decision.
