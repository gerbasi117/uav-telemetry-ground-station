# MAVLink / PX4 / ArduPilot Integration Roadmap

This project currently uses simulated and replayed telemetry. The next major upgrade is live MAVLink support.

## Planned architecture

```mermaid
flowchart LR
    A[Flight Controller] --> B[Telemetry Radio / UDP]
    B --> C[MAVLink Listener]
    C --> D[TelemetryFrame Mapper]
    D --> E[Warning Engine]
    E --> F[Dashboard + Logger + Flight Report]
```

## Step-by-step plan

1. Add a MAVLink listener module.
2. Support serial telemetry radio input and UDP input.
3. Map GPS, battery, current, armed state, mode, heading, and range data into `TelemetryFrame`.
4. Preserve raw MAVLink logs for debugging.
5. Add configuration profiles for different airframes.
6. Replay real logs through the existing report generator.

## Why this matters

A systems integration engineer needs repeatable tooling for bring-up, field testing, and troubleshooting. This project is designed so the simulated pipeline can become a live telemetry pipeline without rewriting the warning/reporting logic.
