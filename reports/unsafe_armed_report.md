# Flight Summary Report

**Scenario:** `unsafe_armed`
**Source:** `simulate`
**Final safety status:** **UNSAFE**

## Summary

- Samples: 4
- Duration: 1.5 seconds
- Minimum battery: 98.7% / 25.12 V
- Maximum current draw: 15.3 A
- Maximum altitude: 16.98 m
- Minimum rangefinder distance: 3.5 m
- GPS-loss samples: 4
- Armed samples: 4

## Warning Counts

| Warning | Count |
|---|---:|
| ARMED_WITH_BAD_GPS | 4 |
| GPS_LOST | 4 |
| LOW_SATELLITE_COUNT | 4 |

## Recommended Actions

- Verify GPS placement, antenna visibility, wiring, and pre-flight GPS lock requirements.
- Review arming checks and block autonomous/GPS-dependent modes until GPS health is acceptable.

## Portfolio Note

This report is generated from simulated/replayed telemetry to demonstrate UAV log analysis, warning aggregation, and operator-facing safety summaries. Future versions can connect this workflow to MAVLink/PX4/ArduPilot telemetry and real field-test logs.
