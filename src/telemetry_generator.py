from __future__ import annotations

import math
import random
import time
from typing import Iterator

from telemetry_parser import TelemetryFrame


SCENARIOS = {
    "normal",
    "low_battery",
    "gps_loss",
    "high_current",
    "unsafe_armed",
    "rangefinder_close",
    "sensor_fault",
    "link_loss",
    "mixed_faults",
}


class TelemetryGenerator:
    """Generates simulated UAV telemetry for local testing.

    The scenario argument makes demos/replay repeatable for recruiters and
    interview conversations. It also gives unit-test-style coverage for warning
    states without needing a real vehicle connected.
    """

    def __init__(self, seed: int = 117, scenario: str = "normal") -> None:
        if scenario not in SCENARIOS:
            raise ValueError(f"Unknown scenario '{scenario}'. Options: {sorted(SCENARIOS)}")
        self.random = random.Random(seed)
        self.start_time = time.time()
        self.base_lat = 30.2672
        self.base_lon = -97.7431
        self.scenario = scenario

    def frames(self, duration_s: float, rate_hz: float) -> Iterator[TelemetryFrame]:
        total_frames = max(1, int(duration_s * rate_hz))
        delay = 1.0 / rate_hz if rate_hz > 0 else 0.5

        for i in range(total_frames):
            t = time.time()
            elapsed = t - self.start_time

            battery_percent = max(5.0, 100.0 - elapsed * 0.85)
            voltage = 25.2 * (battery_percent / 100.0) + 19.0 * (1.0 - battery_percent / 100.0)
            altitude = max(0.0, 15.0 + 8.0 * math.sin(i / 12.0))
            current = 12.0 + 8.0 * abs(math.sin(i / 7.0))
            gps_fix = "3D"
            satellites = 14
            link_quality = 95.0
            imu_status = "OK"
            rangefinder = max(0.2, 3.5 + math.sin(i / 5.0))
            armed = i > 2
            flight_mode = "LOITER" if i % 50 < 35 else "STABILIZE"

            if self.scenario == "low_battery":
                battery_percent = max(8.0, 24.0 - i * 0.8)
                voltage = 21.4 if battery_percent > 15 else 20.2
            elif self.scenario == "gps_loss":
                gps_fix = "NO_FIX"
                satellites = 3
            elif self.scenario == "high_current":
                current = 72.0
            elif self.scenario == "unsafe_armed":
                armed = True
                gps_fix = "NO_FIX"
                satellites = 3
                flight_mode = "ALT_HOLD"
            elif self.scenario == "rangefinder_close":
                rangefinder = 0.42
            elif self.scenario == "sensor_fault":
                imu_status = "FAULT"
            elif self.scenario == "link_loss":
                link_quality = 20.0
            elif self.scenario == "mixed_faults":
                if i % 6 in {0, 1}:
                    satellites = 5
                if i % 10 in {2, 3}:
                    gps_fix = "NO_FIX"
                    satellites = 3
                if i % 12 in {4, 5}:
                    current = 72.0
                if i % 14 in {6, 7}:
                    link_quality = 22.0
                if i % 16 in {8, 9}:
                    rangefinder = 0.45
                if i % 18 in {10, 11}:
                    imu_status = "FAULT"

            yield TelemetryFrame(
                timestamp=t,
                flight_mode=flight_mode,
                armed=armed,
                latitude=self.base_lat + 0.00001 * i,
                longitude=self.base_lon - 0.00001 * i,
                altitude_m=round(altitude, 2),
                heading_deg=round((i * 4.0) % 360, 1),
                battery_voltage=round(voltage, 2),
                battery_percent=round(battery_percent, 1),
                current_draw_a=round(current, 1),
                gps_fix=gps_fix,
                satellite_count=satellites,
                link_quality=round(link_quality, 1),
                imu_status=imu_status,
                rangefinder_distance_m=round(rangefinder, 2),
            )

            time.sleep(delay)
