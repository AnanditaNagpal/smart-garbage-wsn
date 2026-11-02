# Multi-seed experiment results

Three seeds per policy and radio setting; 12 runs total.
Ideal: TX=1.0, RX=1.0. RX90: TX=1.0, RX=0.9.

TX cohort: 120 <= t < 600 s; delivery deadline: 610 s.
Rates use unique first receptions in 120 <= t < 600 s.
UDP throughput counts payload plus an 8-byte UDP header only.

## Individual runs

| Policy | Radio | Seed | TX | Delivered | PDR (%) | Undelivered | Mean delay (ms) | Goodput (bit/s) | UDP throughput (bit/s) |
|---|---|---|---|---|---|---|---|---|---|
| fixed | ideal | 123456 | 1444 | 1444 | 100.000 | 0 | 75.242 | 437.017 | 629.283 |
| fixed | ideal | 234567 | 1442 | 1442 | 100.000 | 0 | 75.139 | 436.850 | 628.983 |
| fixed | ideal | 345678 | 1429 | 1429 | 100.000 | 0 | 74.505 | 433.100 | 623.633 |
| fixed | rx90 | 123456 | 1438 | 1438 | 100.000 | 0 | 80.930 | 436.033 | 627.767 |
| fixed | rx90 | 234567 | 1442 | 1442 | 100.000 | 0 | 81.658 | 437.167 | 629.433 |
| fixed | rx90 | 345678 | 1439 | 1439 | 100.000 | 0 | 83.551 | 436.333 | 628.200 |
| adaptive | ideal | 123456 | 1180 | 1180 | 100.000 | 0 | 66.532 | 360.667 | 518.000 |
| adaptive | ideal | 234567 | 1181 | 1181 | 100.000 | 0 | 68.483 | 360.667 | 518.000 |
| adaptive | ideal | 345678 | 1189 | 1189 | 100.000 | 0 | 66.683 | 363.217 | 521.617 |
| adaptive | rx90 | 123456 | 1186 | 1186 | 100.000 | 0 | 72.299 | 362.517 | 520.650 |
| adaptive | rx90 | 234567 | 1189 | 1189 | 100.000 | 0 | 73.749 | 363.700 | 522.233 |
| adaptive | rx90 | 345678 | 1192 | 1192 | 100.000 | 0 | 72.586 | 364.683 | 523.617 |

## Across-seed summary

Values are mean ± sample standard deviation across three runs.
These describe run-to-run variation, not confidence intervals.

| Policy | Radio | TX | Delivered | PDR (%) | Undelivered | Mean delay (ms) | Goodput (bit/s) | UDP throughput (bit/s) |
|---|---|---|---|---|---|---|---|---|
| fixed | ideal | 1438.333 ± 8.145 | 1438.333 ± 8.145 | 100.000 ± 0.000 | 0.000 ± 0.000 | 74.962 ± 0.399 | 435.656 ± 2.215 | 627.300 ± 3.179 |
| fixed | rx90 | 1439.667 ± 2.082 | 1439.667 ± 2.082 | 100.000 ± 0.000 | 0.000 ± 0.000 | 82.046 ± 1.353 | 436.511 ± 0.587 | 628.467 ± 0.865 |
| adaptive | ideal | 1183.333 ± 4.933 | 1183.333 ± 4.933 | 100.000 ± 0.000 | 0.000 ± 0.000 | 67.233 ± 1.085 | 361.517 ± 1.472 | 519.206 ± 2.088 |
| adaptive | rx90 | 1189.000 ± 3.000 | 1189.000 ± 3.000 | 100.000 ± 0.000 | 0.000 ± 0.000 | 72.878 ± 0.768 | 363.633 ± 1.085 | 522.167 ± 1.484 |

These experiments use the earlier time-based filling model.
They are separate from the enhanced deposit-and-collection demo.
No energy consumption or battery lifetime was measured.
