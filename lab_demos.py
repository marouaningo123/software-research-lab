"""Small deterministic models of the lab protocols. No external services."""

from collections import Counter, deque
from math import log2
from random import Random

from experiments import cache_cost, replay_effects


def workflow():
    return {"append-only effects": replay_effects(False, False),
            "compacted effects": replay_effects(True, False),
            "fenced effects": replay_effects(True, True)}


def fault_schedules():
    paths = [("enqueue",), ("enqueue", "retry"), ("enqueue", "commit"),
             ("enqueue", "retry", "reconcile")]
    random = Random(7)
    random_paths = [random.choice(paths) for _ in paths]
    guided = sorted(paths, key=len, reverse=True)
    return {"random distinct transitions": len(set(random_paths)),
            "guided distinct transitions": len(set(guided))}


def replay():
    events = [("worker-a", 2), ("worker-b", 3), ("worker-a", -1)]
    def run(trace):
        totals = Counter()
        for worker, amount in trace:
            totals[worker] += amount
        return dict(totals)
    return {"original": run(events), "worker-only replay": run(events[::2]),
            "whole-trace replay": run(events)}


def views():
    grants = {"hot": {"reader"}, "cold": {"editor"}}
    cache = {"hot": grants["hot"].copy()}
    grants["hot"].remove("reader")
    return {"full view entries": len(grants), "cached entries": len(cache),
            "stale authorization": "reader" in cache["hot"],
            "version-checked authorization": "reader" in grants["hot"]}


def api_cache():
    return {"LRU backend ms": cache_cost(12, False),
            "cost-aware backend ms": cache_cost(12, True)}


def storage():
    values = [128, 1024, 4096, 256]
    merges = [4, 2, 3, 1]
    return {"fixed inline bytes": sum((32 + v) * 4 for v in values),
            "adaptive inline bytes": sum((32 + v) * m for v, m in zip(values, merges)),
            "fixed separated bytes": sum(v + 32 * 4 for v in values),
            "adaptive separated bytes": sum(v + 32 * m for v, m in zip(values, merges))}


def workers():
    demand = [1, 3, 4, 1]
    fixed = [2] * len(demand)
    adaptive = [4 - slots for slots in demand]
    def run(worker_slots):
        return {"worker slots used": sum(worker_slots),
                "API slots missed": sum(max(0, api + bg - 4)
                                        for api, bg in zip(demand, worker_slots))}
    return {"fixed": run(fixed), "adaptive": run(adaptive)}


def flags():
    cases = [("pinned", False), ("tenant", False), ("pinned", True)]
    return {"syntactic edits": len(cases),
            "guarded edits": sum(kind == "pinned" and not effect for kind, effect in cases),
            "unsafe cases skipped": sum(kind != "pinned" or effect for kind, effect in cases)}


def tiers():
    trace = ["scan-a", "hot", "scan-b", "hot", "scan-c", "hot", "hot"]
    def run(adaptive):
        counts = Counter()
        resident = None
        writes = hits = 0
        for block in trace:
            counts[block] += 1
            if block == resident:
                hits += 1
            elif not adaptive or (counts[block] >= 2 and writes < 2):
                writes += 1
                resident = block
        return {"hits": hits, "promotions": writes}
    return {"admit all": run(False), "budgeted reuse": run(True)}


def prefetch():
    alone = [2, 1.5]
    before, after = [1.2, 1.45], [1.4, 1.3]
    def measure(shared):
        ratios = [active / isolated for active, isolated in zip(shared, alone)]
        return {"worst slowdown": round(1 / min(ratios), 3),
                "weighted speedup": round(sum(ratios), 3)}
    return {"aggregate policy": measure(before), "fairness guard": measure(after)}


def routing():
    tasks = [("extract", .9, True), ("code", .8, False), ("code", .96, True)]
    def run(thresholds):
        cheap = [confidence >= thresholds[group] for group, confidence, _ in tasks]
        return {"cost units": sum(1 if use else 5 for use in cheap),
                "errors": sum(use and not ok for use, (_, _, ok) in zip(cheap, tasks))}
    return {"global": run({"extract": .75, "code": .75}),
            "group thresholds": run({"extract": .75, "code": .9})}


def compression():
    tokens = ["filler", "policy", "limit", "42", "filler", "filler"]
    naive = tokens[:3]
    protected = [tokens[i] for i in (1, 2, 3)]
    return {"naive": naive, "protected": protected,
            "evidence retained": [("42" in naive), ("42" in protected)]}


def prefix():
    queue = [("unique", 1), ("shared", 4), ("shared", 5)]
    def run(deadline):
        ordered = sorted(queue, key=lambda job: job[1] if deadline else job[0] != "shared")
        cost = 0
        cache = set()
        misses = 0
        for key, due in ordered:
            cost += 1 if key in cache else 2
            cache.add(key)
            misses += cost > due
        return {"prefill units": cost, "deadline misses": misses}
    return {"prefix first": run(False), "earliest deadline": run(True)}


def offload():
    budget, pending = 6, [4, 4, 2]
    chosen = []
    for transfer in pending:
        if sum(chosen) + transfer <= budget:
            chosen.append(transfer)
    return {"unbounded ms": sum(pending), "admitted ms": sum(chosen),
            "budget ms": budget, "jobs deferred": len(pending) - len(chosen)}


def migration():
    rows = {1: {"old": "updated", "new": "updated", "version": 2}}
    snapshot = {"value": "original", "version": 1}
    naive = snapshot["value"]
    guarded = (snapshot["value"] if snapshot["version"] >= rows[1]["version"]
               else rows[1]["new"])
    return {"naive backfill": naive, "version-checked backfill": guarded}


def api_contract():
    steps = ["create", "update", "read", "delete"]
    item = None
    checks = []
    for step in steps:
        if step == "create":
            item = {"quantity": 1}
        elif step == "update":
            item["quantity"] = 2
        elif step == "read":
            checks.append(item == {"quantity": 2})
        else:
            item = None
    checks.append(item is None)
    return {"fixed lifecycle": steps, "assertions passed": sum(checks)}


def code_review():
    edits = [("move", "return price", "return price"),
             ("move", "return price", "return price * 2")]
    grouped = [kind for kind, before, after in edits if before == after]
    return {"raw edits": len(edits), "verified moves grouped": len(grouped),
            "behavior-changing edits shown": len(edits) - len(grouped)}


def tracing():
    stream = ["popular"] * 7 + ["rare"]
    first = stream[:2]
    reserved = [stream[0], next(service for service in stream if service == "rare")]
    return {"first arrivals": first, "service floor": reserved, "equal budget": 2}


def reconcile():
    left = {"a": 1, "b": 2}
    right = {"a": 1, "b": 3, "c": 4}
    missing = [(key, value) for key, value in right.items() if left.get(key) != value]
    repaired = left | dict(missing)
    return {"full inventory records": len(right), "delta records": len(missing),
            "converged": repaired == right, "fallback needed with budget 1": len(missing) > 1}


def overload():
    def run(budget):
        backlog = 0
        history = []
        for capacity in (1, 1, 5, 5, 5):
            offered = 4 + min(backlog, budget)
            backlog = max(0, offered - capacity)
            history.append(backlog)
        return history
    return {"uncapped backlog": run(100), "budgeted backlog": run(1)}


def abstention():
    samples = [(.9, .9, True), (.9, .2, False), (.5, .9, True), (.3, .4, False)]
    def run(accept):
        answered = [ok for confidence, evidence, ok in samples if accept(confidence, evidence)]
        return {"answered": len(answered), "unsupported": answered.count(False)}
    return {"confidence": run(lambda c, e: c >= .8),
            "evidence-aware": run(lambda c, e: (c + e) / 2 >= .65)}


def citations():
    gold = {"stock": "inventory doc", "shipping": "delivery doc"}
    draft = {"stock": "inventory doc", "shipping": "marketing doc"}
    corrected = {claim: (citation if citation == gold[claim] else gold[claim])
                 for claim, citation in draft.items()}
    return {"draft": draft, "oracle repair": corrected,
            "claims changed": sum(draft[key] != corrected[key] for key in draft)}


def retrieval():
    query = {"rail", "pass"}
    leaves = [("A", {"pass"}), ("B", {"pass", "museum"})]
    contextual = [(key, tokens | ({"rail"} if key == "A" else set())) for key, tokens in leaves]
    def rank(items):
        return [key for key, _ in sorted(items, key=lambda item: (-len(item[1] & query), item[0]))]
    return {"flat ranking": rank(reversed(leaves)), "contextual ranking": rank(contextual),
            "contextual gold score": len(contextual[0][1] & query)}


def sampling():
    answers = ["A", "A", "A", "B", "A", "B"]
    def entropy(sequence):
        return round(-sum((n / len(sequence)) * log2(n / len(sequence))
                          for n in Counter(sequence).values()), 3)
    return {"early entropy bits": entropy(answers[:3]), "full entropy bits": entropy(answers),
            "early samples": 3, "full samples": len(answers)}


def adapters():
    residuals = [9, 4, 2, 1]
    uniform, weighted = [2, 2, 2, 2], [4, 2, 1, 1]
    def proxy(ranks):
        return sum(value / (rank + 1) for value, rank in zip(residuals, ranks))
    return {"rank budget": sum(uniform), "uniform residual proxy": round(proxy(uniform), 3),
            "weighted residual proxy": round(proxy(weighted), 3)}


def preference():
    groups = {"French": (.8, .1), "Darija": (.6, .3)}
    return {group: {"observed preference": observed,
                    "symmetric-flip correction": round((observed - noise) / (1 - 2 * noise), 3)}
            for group, (observed, noise) in groups.items()}


def speculation():
    target = list("abcdef")
    draft = list("abxdef")
    emitted = []
    for expected, proposal in zip(target, draft):
        emitted.append(proposal if expected == proposal else expected)
        if expected != proposal:
            break
    return {"accepted draft prefix": len(emitted) - 1, "verified output": "".join(emitted),
            "greedy parity": emitted == target[:len(emitted)]}


def patch_tests():
    def correct(quantity):
        return max(0, quantity)
    def brittle(quantity):
        return quantity if quantity >= 0 else 1
    def score(patch, cases):
        return sum(patch(value) == expected for value, expected in cases)
    common = [(2, 2)]
    independent = common + [(-1, 0)]
    return {"brittle existing passes": score(brittle, common),
            "brittle independent passes": score(brittle, independent),
            "correct independent passes": score(correct, independent),
            "independent test count": len(independent)}


def triage():
    samples = [("A", .9, .1), ("B", .6, .8), ("C", .2, .5)]
    return {"uncertainty pick": max(samples, key=lambda row: row[1])[0],
            "joint signal pick": max(samples, key=lambda row: row[1] * row[2])[0]}


def continual():
    tasks = deque(["French", "Darija", "English"], maxlen=2)
    return {"old tasks retained": list(tasks), "evicted task": "French",
            "latest-only baseline": ["English"]}


DEMOS = (
    workflow, fault_schedules, replay, views, api_cache, storage, workers, flags, tiers,
    prefetch, routing, compression, prefix, offload, migration, api_contract,
    code_review, tracing, reconcile, overload, abstention, citations, retrieval,
    sampling, adapters, preference, speculation, patch_tests, triage, continual,
)
