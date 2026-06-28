from __future__ import annotations

import time
from typing import List, Optional

from telemetry_parser import TelemetryFrame


class WarningEngine:
    """Evaluates telemetry frames and returns warning labels.

    Thresholds are intentionally simple for MVP. Future versions can load these
    from a config file and adjust thresholds by vehicle type/battery setup.
    """

    def __init__(self, telemetry_timeout_s: float = 3.0) -> None:
        self.telemetry_timeout_s = telemetry_timeout_s
        self.last_timestamp: Optional[float] = None

    def evaluate(self, frame: TelemetryFrame, now: Optional[float] = None) -> List[str]:
        warnings: List[str] = []
        now = time.time() if now is None else now

        if frame.battery_percent <= 15 or frame.battery_voltage <= 20.5:
            warnings.append("CRITICAL_BATTERY")
        elif frame.battery_percent <= 25 or frame.battery_voltage <= 21.5:
            warnings.append("LOW_BATTERY")

        if frame.gps_fix.upper() not in {"3D", "3D_FIX", "RTK", "DGPS"}:
            warnings.append("GPS_LOST")

        if frame.satellite_count < 8:
            warnings.append("LOW_SATELLITE_COUNT")

        if frame.current_draw_a >= 65:
            warnings.append("HIGH_CURRENT_DRAW")

        if frame.link_quality < 35:
            warnings.append("LOW_LINK_QUALITY")

        if frame.imu_status.upper() not in {"OK", "NOMINAL"}:
            warnings.append("SENSOR_FAULT")

        if 0 <= frame.rangefinder_distance_m < 0.75:
            warnings.append("RANGEFINDER_TOO_CLOSE")

        if frame.armed and ("GPS_LOST" in warnings or "LOW_SATELLITE_COUNT" in warnings):
            warnings.append("ARMED_WITH_BAD_GPS")

        if self.last_timestamp is not None:
            gap = frame.timestamp - self.last_timestamp
            if gap > self.telemetry_timeout_s:
                warnings.append("TELEMETRY_TIMEOUT")
        elif now - frame.timestamp > self.telemetry_timeout_s * 2:
            warnings.append("STALE_TELEMETRY")

        self.last_timestamp = frame.timestamp
        return warnings
