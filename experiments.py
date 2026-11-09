"""Generate analytical scenarios and a seeded toy workload for all ten studies."""

import csv
from collections import OrderedDict
from html import escape
from pathlib import Path
from random import Random


def replay_effects(compact, fence):
    """Model one commit, a lost acknowledgment, and a replay after retention."""
    seen = {"reservation-1"}
    effects = 1
    if compact:
        seen.clear()
    if not fence and "reservation-1" not in seen:
        effects += 1
    return effects


def cache_cost(capacity, cost_aware):
    """Compare LRU with a bounded cost-aware admission heuristic."""
    random = Random(2026)
    cache = OrderedDict()
    scores = {}
    backend_ms = 0
    for request in range(3000):
        offset = 0 if request < 1500 else 50
        key = offset + int(random.random() ** 2 * 50)
        cost = 25 if key % 7 == 0 else 2
        if request % 100 == 0:
            scores = {item: count * 0.5 for item, count in scores.items()}
        scores[key] = scores.get(key, 0) + 1
        if key in cache:
            cache.move_to_end(key)
            continue
        backend_ms += cost
        if len(cache) == capacity:
            victim = next(iter(cache))
            victim_cost = 25 if victim % 7 == 0 else 2
            if cost_aware and scores[key] * cost < scores[victim] * victim_cost:
                continue
            cache.popitem(last=False)
        cache[key] = None
    return backend_ms


def scenarios():
    return [
        ("01-ledger", "Retention (days)", "Logical payload (GB)",
         [(d, 1000 * 1440 * d * 160 / 1e9, 1000 * 1440 * min(d, 2) * 160 / 1e9)
          for d in range(1, 15)], ("Append-only window", "Two-day detail cap, fences excluded")),
        ("02-faults", "Eligible sites", "Distinct schedules",
         [(n, 3 * n, 9 * n * (n - 1) / 2) for n in range(2, 17)],
         ("Single fault", "Two distinct sites")),
        ("03-replay", "Heavy capture share (%)", "Native compute multiplier",
         [(p, 1.2 * (1 - p / 100) + 3 * p / 100, 3) for p in range(0, 101, 10)],
         ("Tiered capture", "Always heavy")),
        ("04-views", "Materialized share (%)", "Tuple payload (MB)",
         [(p, 10_000_000 * 48 * p / 100 / 1e6, 480) for p in range(0, 101, 10)],
         ("Partial", "Full")),
        ("05-cache", "Capacity (entries)", "Backend regeneration (ms)",
         [(n, cache_cost(n, False), cache_cost(n, True)) for n in range(2, 32, 2)],
         ("LRU", "Cost-aware admission")),
        ("06-compaction", "Value GC rewrites per update", "Estimated bytes per update",
         [(i / 4, 4224, 1152 + 1024 * i / 4) for i in range(17)],
         ("Inline", "Separated")),
        ("07-workers", "Reserved core equivalents", "CPU ceiling (jobs/s)",
         [(i / 4, (4 - i / 4) / 0.08, 50) for i in range(17)],
         ("With reservation", "Without reservation")),
        ("08-php", "Rejected changes (of 100)", "Review time (min)",
         [(n, 300 + 5 * n, 300) for n in range(0, 31, 2)],
         ("Review and rework", "Review only")),
        ("09-ssd", "Physical write amplification", "Promotion ceiling (blocks/s)",
         [(i / 4, 20e9 / (4096 * 86400 * i / 4), 20e9 / (4096 * 86400))
          for i in range(4, 21)], ("Physical budget", "Logical budget only")),
        ("10-prefetch", "Shared IPC", "Equal-work slowdown (x)",
         [(i / 10, 2 / (i / 10), 1) for i in range(5, 21)],
         ("Shared execution", "Isolated reference")),
    ]


def chart(name, x_label, y_label, rows, labels):
    """Render two line series with labeled ticks and a fixed zero origin on Y."""
    left, right, top, bottom = 88, 680, 60, 320
    low_x, high_x = rows[0][0], rows[-1][0]
    high_y = max(max(row[1:]) for row in rows) * 1.08
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="720" height="420" '
        'viewBox="0 0 720 420" role="img">',
        f"<title>{escape(name)}: illustrative scenario</title>",
        '<rect width="720" height="420" fill="white"/>',
        '<g font-family="sans-serif" fill="#17233b" font-size="13">',
        f'<text x="88" y="28" font-size="19">{escape(y_label)}</text>',
    ]
    for tick in range(6):
        ratio = tick / 5
        x = left + ratio * (right - left)
        y = bottom - ratio * (bottom - top)
        parts.extend([
            f'<path d="M{left},{y} H{right}" stroke="#dce3ec"/>',
            f'<text x="80" y="{y + 4}" text-anchor="end">{high_y * ratio:.3g}</text>',
            f'<text x="{x}" y="341" text-anchor="middle">{low_x + ratio * (high_x - low_x):.3g}</text>',
        ])
    for column, color in enumerate(("#0b62af", "#ac4c14"), start=1):
        points = " ".join(
            f"{left + (r[0] - low_x) / (high_x - low_x) * (right - left):.2f},"
            f"{bottom - r[column] / high_y * (bottom - top):.2f}" for r in rows
        )
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3"/>')
        parts.append(
            f'<text x="{88 + (column - 1) * 245}" y="400" fill="{color}">'
            f'{escape(labels[column - 1])}</text>'
        )
    parts.append(f'<text x="384" y="366" text-anchor="middle">{escape(x_label)}</text></g></svg>')
    return "\n".join(parts)


def main():
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(exist_ok=True)
    gallery = ["# Model curves", "", "Analytical scenarios and seeded toy outputs.", ""]
    for name, x_label, y_label, rows, labels in scenarios():
        with (output / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow((x_label, *labels))
            writer.writerows(rows)
        (output / f"{name}.svg").write_text(
            chart(name, x_label, y_label, rows, labels), encoding="utf-8"
        )
        gallery.extend([f"## {name}", "", f"![{y_label} vs {x_label}]({name}.svg)",
                        "", f"[CSV data]({name}.csv)", ""])
    (output / "README.md").write_text("\n".join(gallery), encoding="utf-8")
    print(f"Generated {len(scenarios())} curves")
    print(f"Late replay without fence: {replay_effects(compact=True, fence=False)} effects")
    print(f"Late replay with fence: {replay_effects(compact=True, fence=True)} effect")


if __name__ == "__main__":
    main()
