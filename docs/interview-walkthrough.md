# Interview Walkthrough: UAV Telemetry Ground Station

## 30-second explanation

I built a Python UAV telemetry ground-station prototype that simulates and replays drone telemetry, evaluates warning states, logs data, and generates post-run safety reports. The goal was to demonstrate how I would approach field robotics testing: monitor vehicle health, detect unsafe states, preserve logs, and produce a concise report for debugging.

## What problem it solves

During UAV and robotics field testing, operators need to know whether the vehicle is safe, what warnings occurred, and what should be inspected after a test. This project simulates that workflow using repeatable fault scenarios and automatic report generation.

## What I built

- Telemetry generator with repeatable scenarios.
- Terminal dashboard for live status.
- Warning engine for battery, GPS, link, current, sensor, and arming faults.
- CSV logging and replay mode.
- JSON and Markdown flight summary reports.
- Unit tests for warning logic and report generation.

## Example scenario

The `mixed_faults` scenario intentionally produces multiple issues, including GPS loss, high current draw, low link quality, and unsafe armed state. The system classifies the final report as `UNSAFE` and recommends follow-up actions.

## Why this matters for UAV/Robotics Systems Integration

This project demonstrates the same workflow used in real integration/test work:

1. Collect telemetry.
2. Detect unhealthy states.
3. Preserve logs.
4. Reproduce the issue.
5. Generate a summary.
6. Recommend next debugging steps.

## What I would improve next

- Add live MAVLink input.
- Add configurable warning thresholds.
- Add web dashboard UI.
- Add real flight-log replay.
- Add plots for battery/current/altitude over time.
- Add integration with Otto as an operator assistant for summarizing reports.
