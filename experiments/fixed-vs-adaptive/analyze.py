"""Analyze the earlier fixed/adaptive experiment logs, not the collection demo."""
from pathlib import Path
import ipaddress
import re
import statistics

START, END, DRAIN = 120.0, 600.0, 610.0
HERE = Path(__file__).resolve().parent
prefix = re.compile(r"^(\d+):(\d+(?:\.\d+)?)\s+ID:(\d+)")
tx_pattern = re.compile(r"BIN_TX BIN seq=(\d+) fill=(\d+) bytes=(\d+)")
rx_pattern = re.compile(
    r"BIN_RX bytes=(\d+) payload='BIN seq=(\d+) fill=(\d+)' from (\S+)"
)

def analyze(path):
    tx, rx = {}, {}
    previous = -1.0
    last = 0.0
    for line in path.read_text().splitlines():
        stamp = prefix.search(line)
        if not stamp:
            continue
        minutes, seconds, mote = stamp.groups()
        time = int(minutes) * 60 + float(seconds)
        if time < previous - 1:
            raise ValueError(f"{path.name}: multiple runs detected; isolate one run.")
        previous = last = time
        match = tx_pattern.search(line)
        if match:
            seq, fill, size = map(int, match.groups())
            key = (int(mote), seq)
            if key in tx:
                raise ValueError(f"Repeated transmission key: {key}")
            tx[key] = (time, size)
        match = rx_pattern.search(line)
        if match:
            size, seq, fill, address = match.groups()
            sender = int(ipaddress.IPv6Address(address)) & 0xffff
            key = (sender, int(seq))
            rx.setdefault(key, []).append((time, int(size)))

    if last < DRAIN:
        raise ValueError(f"{path.name}: recording must reach {DRAIN} seconds.")

    cohort = {k: v for k, v in tx.items() if START <= v[0] < END}
    delays = []
    for key, (sent, size) in cohort.items():
        arrivals = [t for t, n in rx.get(key, [])
                    if sent <= t <= DRAIN and n == size]
        if arrivals:
            delays.append((min(arrivals) - sent) * 1000)

    received_in_window = [
        events[0][1] for events in rx.values()
        if START <= events[0][0] < END
    ]
    duration = END - START
    count = len(cohort)
    delivered = len(delays)
    if not count:
        raise ValueError("No transmissions in measurement window.")

    return (
        count, delivered, 100 * delivered / count,
        count - delivered,
        statistics.mean(delays) if delays else float("nan"),
        8 * sum(received_in_window) / duration,
        8 * sum(n + 8 for n in received_in_window) / duration,
    )

print("TX cohort: 120 <= t < 600 s; delivery deadline: 610 s.")
print("Rates: unique first receptions in 120 <= t < 600 s.")
print("UDP throughput includes payload + 8-byte UDP header only.")
print("It excludes IP/MAC headers, control traffic and retransmissions.\n")
print("| Scenario | TX | Delivered | PDR (%) | Lost | Mean delay (ms) | Goodput (bit/s) | UDP throughput (bit/s) |")
print("|---|---:|---:|---:|---:|---:|---:|---:|")
for name in ("fixed-timebased-5s.txt", "adaptive-full.txt"):
    tx, delivered, pdr, lost, delay, goodput, throughput = analyze(HERE / name)
    print(f"| {name} | {tx} | {delivered} | {pdr:.2f} | {lost} | {delay:.3f} | {goodput:.3f} | {throughput:.3f} |")
