from pathlib import Path
import contextlib
import csv
import io
import runpy
import statistics

HERE = Path(__file__).resolve().parent
SEEDS = (123456, 234567, 345678)
METRICS = (
    "TX", "Delivered", "PDR (%)", "Undelivered",
    "Mean delay (ms)", "Goodput (bit/s)", "UDP throughput (bit/s)"
)

with contextlib.redirect_stdout(io.StringIO()):
    module = runpy.run_path(
        str(HERE.parent / "fixed-vs-adaptive" / "analyze.py")
    )

rows = []
for policy in ("fixed", "adaptive"):
    for radio in ("ideal", "rx90"):
        for seed in SEEDS:
            name = f"{policy}-{radio}-seed{seed}.txt"
            values = module["analyze"](HERE / "logs" / name)
            rows.append((policy, radio, seed, *values))

with (HERE / "results.csv").open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(("Policy", "Radio", "Seed", *METRICS))
    writer.writerows(rows)

lines = [
    "# Multi-seed experiment results",
    "",
    "Three seeds per policy and radio setting; 12 runs total.",
    "Ideal: TX=1.0, RX=1.0. RX90: TX=1.0, RX=0.9.",
    "",
    "TX cohort: 120 <= t < 600 s; delivery deadline: 610 s.",
    "Rates use unique first receptions in 120 <= t < 600 s.",
    "UDP throughput counts payload plus an 8-byte UDP header only.",
    "",
    "## Individual runs",
    "",
    "| Policy | Radio | Seed | " + " | ".join(METRICS) + " |",
    "|" + "---|" * 10,
]

for row in rows:
    cells = [
        f"{value:.3f}" if isinstance(value, float) else str(value)
        for value in row
    ]
    lines.append("| " + " | ".join(cells) + " |")

lines += [
    "",
    "## Across-seed summary",
    "",
    "Values are mean ± sample standard deviation across three runs.",
    "These describe run-to-run variation, not confidence intervals.",
    "",
    "| Policy | Radio | " + " | ".join(METRICS) + " |",
    "|" + "---|" * 9,
]

for policy in ("fixed", "adaptive"):
    for radio in ("ideal", "rx90"):
        group = [r for r in rows if r[:2] == (policy, radio)]
        cells = [policy, radio]
        for index in range(3, 10):
            values = [r[index] for r in group]
            cells.append(
                f"{statistics.mean(values):.3f} ± "
                f"{statistics.stdev(values):.3f}"
            )
        lines.append("| " + " | ".join(cells) + " |")

lines += [
    "",
    "These experiments use the earlier time-based filling model.",
    "They are separate from the enhanced deposit-and-collection demo.",
    "No energy consumption or battery lifetime was measured.",
]
(HERE / "RESULTS.md").write_text("\n".join(lines) + "\n")
print("Created results.csv and RESULTS.md from all 12 logs.")
