# Demonstration guide

## 1. Start the dashboard

From the repository folder, run:

    python3 Smart_Garbage_Neighbourhood_Routing.py

Open http://127.0.0.1:8767 in a browser.
Keep the dashboard Terminal process running.

## 2. Show recorded collection behaviour

Select Recorded replay and Collection demonstration.
Restart replay, then press Play. Use 5x playback for a shorter demonstration.

Explain:
- Node 1 is the gateway; nodes 2–16 represent 15 bins.
- Synthetic resident deposits increase local fill.
- Green means below 60%, amber 60–79%, and red at least 80%.
- The gateway panel shows received readings, which can lag local state.
- Scheduled visits begin around four simulated minutes.
- Eligible bins are emptied only at logged collection events.
- The truck animation illustrates these events; the gateway does not dispatch it.

## 3. Show routing observations

Select Routing demonstration and enable parent links.
Advance playback and select bin 16.

Explain the displayed parent chain and observation ages.
The chain combines the latest logged preferred-parent observations.
It is not a trace of one packet's actual journey.
The browser street layout differs from the Cooja radio topology.

## 4. Show a live simulation

Follow the main README to build and open the Cooja configuration.
Use a separate log for new runs, preserving the supplied recording.
Ensure Cooja writes to the log beside the dashboard Python file.
Select Connect live and start Cooja.

Confirm that received-reading counts and simulation time advance.
Pausing Cooja stops new simulation events; the dashboard server remains open.

## 5. Explain the measured comparison

Open experiments/fixed-vs-adaptive/RESULTS.md.

These earlier experiments use a different filling model from this demo.
Both recorded 100% cohort PDR under the documented measurement rule.
Adaptive reporting produced 18.28% fewer application transmissions.
This does not establish energy savings or statistical superiority.

Reproduce the table from the repository root:

    python3 experiments/fixed-vs-adaptive/analyze.py

## 6. Finish safely

Pause Cooja before ending the demonstration.
Save configuration changes through Cooja's File menu if needed.
A saved configuration does not preserve a running simulation's state.
Press Control+C in the dashboard server's Terminal tab to stop it.

## Troubleshooting

- Browser cannot connect: check that the Python server is running.
- Port 8767 occupied: stop the previous dashboard server in its own tab.
- Live view does not advance: check Cooja is running and the log path matches.
- Source file missing: check application placement and configuration paths.
- Java class-version error: use a Java runtime compatible with the Cooja build.
