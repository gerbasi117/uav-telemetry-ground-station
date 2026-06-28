# Flight Summary Report

**Scenario:** `mixed_faults`
**Source:** `simulate`
**Final safety status:** **UNSAFE**

## Summary

- Samples: 8
- Duration: 3.501 seconds
- Minimum battery: 97.0% / 25.02 V
- Maximum current draw: 72.0 A
- Maximum altitude: 19.41 m
- Minimum rangefinder distance: 3.5 m
- GPS-loss samples: 2
- Armed samples: 5

## Warning Counts

| Warning | Count |
|---|---:|
| ARMED_WITH_BAD_GPS | 3 |
| GPS_LOST | 2 |
| HIGH_CURRENT_DRAW | 2 |
| LOW_LINK_QUALITY | 2 |
| LOW_SATELLITE_COUNT | 6 |

## Recommended Actions

- Verify GPS placement, antenna visibility, wiring, and pre-flight GPS lock requirements.
- Review arming checks and block autonomous/GPS-dependent modes until GPS health is acceptable.
- Inspect propulsion load, prop selection, motor/ESC behavior, wiring resistance, and battery sag.
- Check telemetry-radio placement, antenna orientation, RF interference, and link budget.

## Portfolio Note

This report is generated from simulated/replayed telemetry to demonstrate UAV log analysis, warning aggregation, and operator-facing safety summaries. Future versions can connect this workflow to MAVLink/PX4/ArduPilot telemetry and real field-test logs.
