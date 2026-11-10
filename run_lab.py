"""Run one or every model and optionally generate a self-contained report."""

import argparse
from html import escape
import json
from pathlib import Path
import re

from lab_demos import DEMOS


ROOT = Path(__file__).resolve().parent
PROTOCOLS = ("PROTOCOLS.md", "PROTOCOLS_11_20.md", "PROTOCOLS_21_30.md")


def run(study=None):
    reports = []
    for file in PROTOCOLS:
        for match in re.finditer(r"^## (\d+)\. (.+)$",
                                 (ROOT / file).read_text(encoding="utf-8-sig"), re.M):
            number = int(match[1])
            if study is None or number == study:
                title = match[2]
                if number == 16:
                    title = "Defensive API lifecycle contract checks"
                reports.append({"study": number, "title": title,
                                "model": DEMOS[number - 1].__name__,
                                "observations": DEMOS[number - 1]()})
    return reports


def html_report(reports):
    cards = []
    for report in reports:
        title = escape(report["title"])
        observations = escape(json.dumps(report["observations"], indent=2, ensure_ascii=False))
        cards.append(f'<details><summary>{report["study"]:02d} · {title}</summary>'
                     f"<pre>{observations}</pre></details>")
    return """<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Software Research Lab · Demo results</title>
<style>
body{max-width:960px;margin:3rem auto;padding:0 1rem;font:16px system-ui;color:#142638;background:#f3f6fb}
details{background:white;border:1px solid #ccd9e7;border-radius:.5rem;padding:1rem;margin:.6rem 0}
summary{cursor:pointer;font-weight:650}pre{overflow:auto;background:#edf3fa;padding:1rem}
</style>
<h1>Software Research Lab</h1>
<p>Marouane Mouhajar · Deterministic teaching models</p>
<p>Expand a study to inspect its output. These are synthetic demonstrations, not benchmarks.</p>
""" + "\n".join(cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", type=int, choices=range(1, len(DEMOS) + 1))
    parser.add_argument("--html", type=Path, help="write an offline report to this path")
    args = parser.parse_args()
    reports = run(args.study)
    if args.html:
        args.html.write_text(html_report(reports), encoding="utf-8")
    else:
        print(json.dumps(reports, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
