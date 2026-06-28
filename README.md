# UAV Telemetry Ground Station

Python telemetry dashboard for UAV/field-robotics monitoring, warning-state detection, and flight-log replay.

## Why this exists

UAV/robotics integration roles require the ability to monitor system state, analyze telemetry, detect unsafe conditions, log data, and debug field issues. This project demonstrates those skills with a simulated telemetry stream that can later be connected to MAVLink, PX4, ArduPilot, or serial telemetry.

## Features

- Simulated UAV telemetry stream
- Repeatable fault scenarios
- Live terminal dashboard
- Compact terminal output mode for demos
- Warning engine for safety/fault states
- CSV flight-log recording
- Flight-log replay mode
- Unit tests for warning logic

## Warning scenarios

```text
normal
low_battery
gps_loss
high_current
unsafe_armed
rangefinder_close
sensor_fault
link_loss
mixed_faults
```

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python src/main.py --mode simulate --scenario normal --duration 10 --rate 2 --log logs/normal.csv
python src/main.py --mode simulate --scenario unsafe_armed --duration 8 --rate 2 --no-dashboard
python src/main.py --mode simulate --scenario mixed_faults --duration 12 --rate 2 --no-dashboard
python src/main.py --mode replay --replay data/sample_flight_log.csv --rate 3
python -m unittest discover -s tests
```

## Telemetry fields

- Flight mode
- Armed/disarmed state
- GPS fix and satellite count
- Latitude/longitude
- Altitude
- Heading
- Battery voltage and percentage
- Current draw
- Telemetry link quality
- Rangefinder distance
- IMU status

## Example warning states

- LOW_BATTERY
- CRITICAL_BATTERY
- GPS_LOST
- LOW_SATELLITE_COUNT
- HIGH_CURRENT_DRAW
- LOW_LINK_QUALITY
- TELEMETRY_TIMEOUT
- RANGEFINDER_TOO_CLOSE
- ARMED_WITH_BAD_GPS
- SENSOR_FAULT

## Future work

- MAVLink input
- PX4/ArduPilot log import
- Web dashboard
- Map view
- Battery remaining estimate
- Integration with Otto robotics operator assistant

## Resume bullets

- Built a Python UAV telemetry ground station for monitoring GPS, altitude, battery, current draw, flight mode, arming state, rangefinder data, and communication health.
- Implemented repeatable fault scenarios and warning-state logic for low battery, GPS loss, high current draw, telemetry timeout, unsafe arming state, sensor faults, low link quality, and rangefinder proximity alerts.
- Added flight-log replay and structured CSV logging to support diagnostics, field testing, and future MAVLink/PX4 integration.
