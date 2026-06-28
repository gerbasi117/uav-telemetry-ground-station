# Flight Summary Report

**Scenario:** `unsafe_armed`
**Source:** `simulate`
**Final safety status:** **UNSAFE**

## Summary

- Samples: 8
- Duration: 3.501 seconds
- Minimum battery: 97.0% / 25.02 V
- Maximum current draw: 18.7 A
- Maximum altitude: 19.41 m
- Minimum rangefinder distance: 3.5 m
- GPS-loss samples: 8
- Armed samples: 8

## Warning Counts

| Warning | Count |
|---|---:|
| ARMED_WITH_BAD_GPS | 8 |
| GPS_LOST | 8 |
| LOW_SATELLITE_COUNT | 8 |

## Recommended Actions

- Verify GPS placement, antenna visibility, wiring, and pre-flight GPS lock requirements.
- Review arming checks and block autonomous/GPS-dependent modes until GPS health is acceptable.

## Portfolio Note

This report is generated from simulated/replayed telemetry to demonstrate UAV log analysis, warning aggregation, and operator-facing safety summaries. Future versions can connect this workflow to MAVLink/PX4/ArduPilot telemetry and real field-test logs.
