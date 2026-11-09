"""Regenerate the analytical SVG and CSV scenarios for studies 21–30."""
import csv
from pathlib import Path
from experiments import chart


def scenarios():
    return [
        ("21-ai", "Independent zero-error audit size", "Upper error bound (%)",
         [(n, 100*(1-0.05**(1/n)), 1) for n in range(50, 1050, 50)],
         ("95% zero-error bound", "1% target")),
        ("22-ai", "Claims selected for repair (%)", "Illustrative request cost (units)",
         [(p, 25+p*0.4, 65) for p in range(0,101,5)],
         ("Selective repair", "Full repair")),
        ("23-ai", "Gold branch retained (%)", "Two-stage recall (%)",
         [(p, 100*p/100*0.9, 90) for p in range(0,101,5)],
         ("90% conditional leaf recall", "Perfect branch routing")),
        ("24-ai", "Per-sample disagreement probability (%)", "Chance of seeing disagreement (%)",
         [(p, 100*(1-(1-p/100)**5),100*(1-(1-p/100)**10)) for p in range(0,101,5)],
         ("Five independent samples", "Ten independent samples")),
        ("25-ai", "Uniform rank", "Trainable parameters (millions)",
         [(r, 32*r*8192/1e6, 32*16*8192/1e6) for r in range(4,65,4)],
         ("One projection per layer", "Rank 16 reference")),
        ("26-ai", "Symmetric label flips (%)", "Retained signed label signal (%)",
         [(p, 100-2*p, 100) for p in range(0,51,5)],
         ("Symmetric flip model", "Clean labels")),
        ("27-ai", "Conditional acceptance (%)", "Expected emitted tokens per verification",
         [(p, sum((p/100)**i for i in range(5)),sum((p/100)**i for i in range(9))) for p in range(0,101,5)],
         ("Four drafted tokens", "Eight drafted tokens")),
        ("28-ai", "Per-test defect detection (%)", "Defective patches missed (%)",
         [(p, 100*(1-p/100)**3, 100*(1-p/100)) for p in range(0,101,5)],
         ("Three independent tests", "One test")),
        ("29-ai", "Audit precision (%)", "Expected corrected labels",
         [(p, 500*p/100,500*0.10) for p in range(0,101,5)],
         ("Targeted audit", "Random audit at 10% noise")),
        ("30-ai", "Retained examples", "Illustrative payload (MB)",
         [(n, n*512*4/1e6,n*512*4*32/1e6) for n in range(100,2100,100)],
         ("Token IDs only", "32 float32 values per token")),
    ]


def main():
    directory = Path(__file__).resolve().parent / "ai-results"
    directory.mkdir(exist_ok=True)
    for name, x, y, rows, labels in scenarios():
        with (directory / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow((x, *labels))
            writer.writerows(rows)
        (directory / f"{name}.svg").write_text(
            chart(name, x, y, rows, labels), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
