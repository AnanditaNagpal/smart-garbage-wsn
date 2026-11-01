TX cohort: 120 <= t < 600 s; delivery deadline: 610 s.
Rates: unique first receptions in 120 <= t < 600 s.
UDP throughput includes payload + 8-byte UDP header only.
It excludes IP/MAC headers, control traffic and retransmissions.

| Scenario | TX | Delivered | PDR (%) | Lost | Mean delay (ms) | Goodput (bit/s) | UDP throughput (bit/s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| fixed-timebased-5s.txt | 1444 | 1444 | 100.00 | 0 | 75.242 | 437.017 | 629.283 |
| adaptive-full.txt | 1180 | 1180 | 100.00 | 0 | 66.532 | 360.667 | 518.000 |
