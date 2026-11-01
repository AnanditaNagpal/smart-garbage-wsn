# Fixed versus adaptive reporting

These earlier experiments use a synthetic time-based filling model.
They are separate from the enhanced deposit and collection demonstration.

## Scenarios
- Fixed: nominal 5-second reporting with jitter.
- Adaptive: nominal 15 seconds below 60% fill, 5 seconds at 60–79%, and 2 seconds at 80% or higher, with jitter.

## Reproduce
Run from the repository root:

    python3 experiments/fixed-vs-adaptive/analyze.py

See [generated results](RESULTS.md) and the supplied raw logs.

## Measurement definitions
- TX cohort: 120 <= t < 600 simulated seconds.
- Delivery deadline: 610 seconds.
- Packet identity: sender node ID and sequence number.
- PDR: delivered cohort packets divided by cohort transmissions.
- Delay: first matching reception minus send-log time, using Cooja timestamps.
- Goodput: unique first-received payload bits in 120 <= t < 600, divided by 480 seconds.
- Reconstructed UDP throughput: received payload plus an 8-byte UDP header per unique packet, divided by 480 seconds.
- This excludes IP/MAC overhead, routing traffic, acknowledgements and retransmissions.

## Interpretation
Fixed reporting produced 1,444 cohort transmissions; adaptive produced
1,180, a reduction of 18.28%. Both recorded 100% cohort PDR.

Lower goodput reflects fewer readings, not necessarily lower capacity.
These are individual runs, not a multi-seed statistical study.
Energy savings, battery lifetime and superior alert latency are unverified.

## Archived source and rerunning

The `source/` folder preserves the archived experiment files.

The supplied configuration references:
- `examples/smart-garbage/udp-client.c`
- `examples/smart-garbage/udp-server.c`

To rerun in a separate Contiki-NG checkout:
1. Create `examples/smart-garbage/`.
2. Copy the archived Makefile and udp-server.c into that folder.
3. Copy either udp-client-fixed.c or udp-client-adaptive.c there,
   renaming the chosen copy to udp-client.c.
4. Copy smart-garbage-working.csc into the same folder.
5. Compile both applications with TARGET=cooja.
6. Open the configuration in Cooja and run from time zero.
7. Record each scenario in a separate log through at least 610 seconds.

Use the same topology, seed and radio settings for both scenarios.
Reload the simulation after changing and compiling the client.
Preserve the supplied evidence logs; save new recordings separately.

The archived configuration retains its original paths and may contain
an old output-log destination. Check that destination before rerunning.
The nested source folder is an archive, not a standalone build directory.
