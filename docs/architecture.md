# Architecture

```text
Telemetry source
   |-- simulated generator
   |-- CSV replay
   |-- future MAVLink input
          |
          v
TelemetryFrame parser
          |
          +--> WarningEngine
          |        |-- battery warnings
          |        |-- GPS warnings
          |        |-- link warnings
          |        |-- sensor warnings
          |
          +--> Dashboard renderer
          |
          +--> CSV logger
```

## Future MAVLink plan

A future `mavlink_input.py` module can translate MAVLink heartbeat, GPS, battery, attitude, rangefinder, and status messages into the same `TelemetryFrame` dataclass used by the current dashboard.
