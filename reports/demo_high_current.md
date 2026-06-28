# Flight Summary Report

**Scenario:** `high_current`
**Source:** `simulate`
**Final safety status:** **UNSAFE**

## Summary

- Samples: 8
- Duration: 3.501 seconds
- Minimum battery: 97.0% / 25.02 V
- Maximum current draw: 72.0 A
- Maximum altitude: 19.41 m
- Minimum rangefinder distance: 3.5 m
- GPS-loss samples: 0
- Armed samples: 5

## Warning Counts

| Warning | Count |
|---|---:|
| HIGH_CURRENT_DRAW | 8 |

## Recommended Actions

- Inspect propulsion load, prop selection, motor/ESC behavior, wiring resistance, and battery sag.

## Portfolio Note

This report is generated from simulated/replayed telemetry to demonstrate UAV log analysis, warning aggregation, and operator-facing safety summaries. Future versions can connect this workflow to MAVLink/PX4/ArduPilot telemetry and real field-test logs.
