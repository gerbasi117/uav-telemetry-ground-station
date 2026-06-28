# Testing Strategy

The project uses repeatable simulated scenarios to test telemetry and safety behavior before connecting to real hardware.

## Test layers

| Layer | Purpose |
|---|---|
| Unit tests | Validate warning logic and report generation. |
| Scenario smoke tests | Run known fault scenarios and inspect compact terminal output. |
| Report checks | Generate JSON/Markdown reports and confirm expected safety status. |
| Replay tests | Replay CSV/JSONL logs through the same warning/report pipeline. |

## Current scenarios

- `normal`
- `low_battery`
- `gps_loss`
- `high_current`
- `unsafe_armed`
- `rangefinder_close`
- `sensor_fault`
- `link_loss`
- `mixed_faults`

## Why simulated testing first?

Simulated testing makes the warning logic repeatable and safe. Once the software behavior is validated, the same pipeline can accept live telemetry or real flight logs.
