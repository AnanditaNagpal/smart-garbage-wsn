from pathlib import Path
import csv
import statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with (HERE / "results.csv").open(newline="") as file:
    rows = list(csv.DictReader(file))

panels = (
    ("TX", "Application transmissions", "Packets in TX cohort"),
    ("Mean delay (ms)", "Mean application delay", "ms"),
    ("Goodput (bit/s)", "Payload goodput", "bit/s"),
    ("UDP throughput (bit/s)", "Reconstructed UDP throughput", "bit/s"),
)
colors = {"fixed": "#245745", "adaptive": "#B18438"}
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
fig.set_facecolor("#F7F5EF")

for ax, (metric, title, unit) in zip(axes.flat, panels):
    for policy, offset in (("fixed", -0.19), ("adaptive", 0.19)):
        for x, radio in enumerate(("ideal", "rx90")):
            group = sorted(
                (r for r in rows
                 if r["Policy"] == policy and r["Radio"] == radio),
                key=lambda r: int(r["Seed"]),
            )
            assert len(group) == 3, "Expected three seeds per group."
            values = [float(r[metric]) for r in group]
            mean = statistics.mean(values)
            sd = statistics.stdev(values)
            position = x + offset
            ax.bar(
                position, mean, width=0.34, yerr=sd, capsize=5,
                color=colors[policy], alpha=0.9,
                label=policy.capitalize() if x == 0 else None,
                zorder=2,
            )
            ax.scatter(
                [position - 0.055, position, position + 0.055],
                values, s=24, color="#222222", zorder=4,
            )
            label = f"{mean:.1f}" if metric == "TX" else f"{mean:.3f}"
            ax.annotate(
                label, (position, mean + sd),
                xytext=(0, 8), textcoords="offset points",
                ha="center", fontsize=9,
            )
    ax.set_title(title, fontsize=13, pad=12)
    ax.set_ylabel(unit)
    ax.set_xticks((0, 1), ("Ideal: RX=1.0", "RX90: RX=0.9"))
    ax.set_ylim(bottom=0)
    ax.margins(y=0.18)
    ax.grid(axis="y", alpha=0.2, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)

axes[0, 0].legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.12), ncol=2)
fig.suptitle(
    "Fixed versus adaptive reporting across three random seeds",
    fontsize=18, y=0.97,
)
fig.text(
    0.5, 0.035,
    "Bars: mean; error bars: sample SD; dots: individual seeds. "
    "All 12 runs recorded 100% cohort PDR.\n"
    "TX window: 120–600 s (end excluded); delivery deadline: 610 s. "
    "UDP accounting: payload + 8-byte header.\n"
    "Earlier time-based filling model; separate from the enhanced collection demo.",
    ha="center", fontsize=9,
)
fig.tight_layout(rect=(0, 0.12, 1, 0.93))
output = HERE / "results-comparison.png"
fig.savefig(output, dpi=180, facecolor=fig.get_facecolor())
plt.close(fig)
print("Created:", output.name)
