from __future__ import annotations

import math
import random
import time
from typing import Iterator

from telemetry_parser import TelemetryFrame


class TelemetryGenerator:
    """Generates simulated UAV telemetry for local testing."""

    def __init__(self, seed: int = 117) -> None:
        self.random = random.Random(seed)
        self.start_time = time.time()
        self.base_lat = 30.2672
        self.base_lon = -97.7431

    def frames(self, duration_s: float, rate_hz: float) -> Iterator[TelemetryFrame]:
        total_frames = int(duration_s * rate_hz)
        delay = 1.0 / rate_hz if rate_hz > 0 else 0.5

        for i in range(total_frames):
            t = time.time()
            elapsed = t - self.start_time
            battery_percent = max(5.0, 100.0 - elapsed * 0.85)
            voltage = 25.2 * (battery_percent / 100.0) + 19.0 * (1.0 - battery_percent / 100.0)
            altitude = max(0.0, 15.0 + 8.0 * math.sin(i / 12.0))
            current = 12.0 + 8.0 * abs(math.sin(i / 7.0))

            # Inject occasional warning scenarios for demo purposes.
            gps_fix = "3D"
            satellites = 14
            link_quality = 95.0
            imu_status = "OK"
            rangefinder = max(0.2, 3.5 + math.sin(i / 5.0))

            if 35 <= i <= 42:
                satellites = 5
            if 60 <= i <= 65:
                gps_fix = "NO_FIX"
            if 80 <= i <= 85:
                current = 72.0
            if 95 <= i <= 99:
                link_quality = 20.0
            if 110 <= i <= 114:
                rangefinder = 0.45
            if 125 <= i <= 128:
                imu_status = "FAULT"

            yield TelemetryFrame(
                timestamp=t,
                flight_mode="LOITER" if i % 50 < 35 else "STABILIZE",
                armed=i > 10,
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
