"""Regenerate analytical scenarios for Software Research Lab studies 11–20."""
import csv
from pathlib import Path

from experiments import chart


def scenarios():
    return [
        ("11-routing", "Cheap-model share (%)", "Cost per 1,000 tasks ($)",
         [(p, (1-p/100)*12 + p/100*(2 + 0.15*12), 12) for p in range(0,101,5)],
         ("Routing scenario", "Strong only")),
        ("12-compression", "Evidence kept (%)", "Input tokens",
         [(p, 1000*p/100 + 7000*0.4, 8000) for p in range(0,101,5)],
         ("Protected spans + compression", "Full context")),
        ("13-prefix", "Prefix hit rate (%)", "Prefill tokens per request",
         [(p, 2000-1500*p/100, 2000) for p in range(0,101,5)],
         ("Expected uncached tokens", "No reuse")),
        ("14-offload", "Bytes transferred per step (MB)", "Transfer time floor (ms)",
         [(n, n/8, n/16) for n in range(8,129,8)],
         ("8 GB/s effective", "16 GB/s effective")),
        ("15-migration", "Backfill rate (rows/s)", "Completion floor (min)",
         [(n, 1e6/n/60, 2e6/n/60) for n in range(500,5500,500)],
         ("One million rows", "Two million rows")),
        ("16-api-fuzz", "Sequence depth", "Candidate prefixes",
         [(d, 4**d, 2**d) for d in range(1,8)],
         ("Four choices per step", "Two choices per step")),
        ("17-diff", "Grouped edit share (%)", "Illustrative review time (min)",
         [(p, 60*(1-p/100)+20*p/100,60) for p in range(0,101,5)],
         ("Grouped view", "Line-by-line")),
        ("18-traces", "Sampling probability (%)", "Chance of retaining an incident (%)",
         [(p, 100*(1-(1-p/100)**5),p) for p in range(0,101,5)],
         ("Five traces", "One trace")),
        ("19-reconcile", "Difference size (keys)", "Estimated wire payload (KiB)",
         [(d, (2*d*32+d*16)/1024,10000*16/1024) for d in range(100,3100,100)],
         ("Sketch plus changed IDs", "Full inventory")),
        ("20-overload", "Timeout probability (%)", "Attempts per original request",
         [(p, 1+p/100+(p/100)**2, min(1.2,1+p/100+(p/100)**2)) for p in range(0,101,5)],
         ("Up to 3 attempts", "Budgeted ceiling")),
    ]


def main():
    output = Path(__file__).resolve().parent / "wave2-results"
    output.mkdir(exist_ok=True)
    for name, x_label, y_label, rows, labels in scenarios():
        with (output / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow((x_label, *labels))
            writer.writerows(rows)
        (output / f"{name}.svg").write_text(
            chart(name, x_label, y_label, rows, labels), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
