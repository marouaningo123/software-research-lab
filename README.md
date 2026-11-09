# Software Research Lab

**Marouane Mouhajar · Expert AI Researcher**
**Contact:** [marouane.mouhajar@gmail.com](mailto:marouane.mouhajar@gmail.com)

Ten computer-science protocols for investigating software reliability, performance and maintainability. Each protocol links the published work it draws on and specifies an experiment, comparison baselines, a failure test and a decision criterion.

## Research index

| Study | Research question | Reproducible example |
|---|---|---|
| 01 · Durable workflows | Can a Symfony Messenger retry ledger be compacted safely? | Logical ledger growth and a late-replay counterexample |
| 02 · Fault injection | Does domain-state feedback help find reproducible bugs? | Growth in single- and two-fault schedule counts |
| 03 · CI replay | Can selective recording preserve useful failures at lower cost? | Capture cost as the heavy-recording share changes |
| 04 · Access views | Can partial materialization lower memory while preserving access semantics? | Relation payload versus materialized share |
| 05 · API caching | Does admission based on rebuild cost save backend CPU? | Seeded equal-capacity cache replay with a workload shift |
| 06 · Event storage | Can value separation and adaptive compaction reduce writes? | Write estimates under garbage collection sensitivity |
| 07 · Worker isolation | Can background jobs coexist with latency-sensitive APIs? | CPU-only throughput ceiling as reservation increases |
| 08 · PHP refactoring | Do guarded transformations reduce maintainer effort? | Review cost as the rejection count rises |
| 09 · SSD placement | Can adaptive promotion meet a physical write budget? | Effective promotion limit under write amplification |
| 10 · Prefetch fairness | Can slowdown feedback protect co-running workloads? | Slowdown sensitivity to shared IPC |

[Read the protocols and sources](PROTOCOLS.md) · [Open the graph gallery](results/README.md) · [Read the launch copy](OUTREACH.md)

## Reproduce the examples

Run from the repository root with Python 3.10 or newer. The examples use the standard library.

```sh
python experiments.py
python -m unittest -v
```

The script regenerates CSV data and SVG figures in **results/**. Each example includes its assumptions in the source. The curves are analytical scenarios or seeded toy simulations. The test suite checks reference values and the intended failure in the workflow model. The full protocols specify the service, hardware or maintainer studies needed to evaluate effectiveness.

## Evidence status

| Layer | Status |
|---|---|
| Published input studies and prior art | Linked in each protocol |
| Analytical scenarios and toy models | Executable and checked against reference cases |
| Real service, storage and hardware benchmarks | Proposed |
| Independent review and replication | Pending |

The first prototype target is Study 01. A durable baseline and a compacted ledger would receive the same crash and replay schedules. A duplicate business effect fails the experiment even if disk usage improves.
