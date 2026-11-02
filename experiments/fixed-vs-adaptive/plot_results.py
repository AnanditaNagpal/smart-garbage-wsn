"""Plot the earlier fixed/adaptive experiment from recorded logs."""
from pathlib import Path
import contextlib
import io
import runpy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    analysis = runpy.run_path(str(HERE / "analyze.py"))

names = ("fixed-timebased-5s.txt", "adaptive-full.txt")
results = [analysis["analyze"](HERE / name) for name in names]
labels = ["Fixed 5 s", "Adaptive"]
colours = ["#245745", "#B18438"]

panels = [
    ("Application transmissions", "Packets in TX cohort", 0),
    ("Payload goodput", "bit/s", 5),
    ("Reconstructed UDP throughput", "bit/s", 6),
    ("Mean application delay", "ms", 4),
]

fig, axes = plt.subplots(2, 2, figsize=(10, 7))
fig.patch.set_facecolor("#F7F5EF")

for ax, (title, unit, index) in zip(axes.flat, panels):
    values = [row[index] for row in results]
    bars = ax.bar(labels, values, color=colours, width=0.55)
    ax.set_title(title, fontsize=12, pad=12)
    ax.set_ylabel(unit)
    ax.set_ylim(0, max(values) * 1.22)
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.18)
    ax.spines[["top", "right"]].set_visible(False)
    for bar, value in zip(bars, values):
        label = f"{value:.0f}" if index == 0 else f"{value:.3f}"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + max(values) * 0.035,
            label, ha="center", fontsize=10
        )

fig.suptitle(
    "Fixed versus adaptive reporting\nEarlier time-based filling experiment",
    fontsize=15, y=0.98
)
fig.text(
    0.5, 0.035,
    "One recorded run per scenario. TX cohort: 120–600 s; delivery deadline: 610 s.\n"
    "Rates use first receptions in 120–600 s. UDP accounting includes payload + 8-byte header.\n"
    "These results are separate from the enhanced collection demonstration.",
    ha="center", fontsize=9
)
fig.tight_layout(rect=(0, 0.13, 1, 0.91))
output = HERE / "results-comparison.png"
fig.savefig(output, dpi=180, facecolor=fig.get_facecolor())
plt.close(fig)
print("Created:", output)
