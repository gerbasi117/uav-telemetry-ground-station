import unittest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from telemetry_parser import TelemetryFrame
from warning_engine import WarningEngine


def base_frame(**overrides):
    data = dict(
        timestamp=1000.0,
        flight_mode="LOITER",
        armed=False,
        latitude=30.0,
        longitude=-97.0,
        altitude_m=10.0,
        heading_deg=90.0,
        battery_voltage=24.0,
        battery_percent=80.0,
        current_draw_a=15.0,
        gps_fix="3D",
        satellite_count=12,
        link_quality=95.0,
        imu_status="OK",
        rangefinder_distance_m=3.0,
    )
    data.update(overrides)
    return TelemetryFrame(**data)


class WarningEngineTests(unittest.TestCase):
    def test_low_battery(self):
        warnings = WarningEngine().evaluate(base_frame(battery_percent=20.0, battery_voltage=21.3), now=1000.0)
        self.assertIn("LOW_BATTERY", warnings)

    def test_critical_battery(self):
        warnings = WarningEngine().evaluate(base_frame(battery_percent=10.0, battery_voltage=20.2), now=1000.0)
        self.assertIn("CRITICAL_BATTERY", warnings)

    def test_armed_with_bad_gps(self):
        warnings = WarningEngine().evaluate(base_frame(armed=True, gps_fix="NO_FIX", satellite_count=3), now=1000.0)
        self.assertIn("GPS_LOST", warnings)
        self.assertIn("ARMED_WITH_BAD_GPS", warnings)

    def test_rangefinder_too_close(self):
        warnings = WarningEngine().evaluate(base_frame(rangefinder_distance_m=0.4), now=1000.0)
        self.assertIn("RANGEFINDER_TOO_CLOSE", warnings)

    def test_sensor_fault(self):
        warnings = WarningEngine().evaluate(base_frame(imu_status="FAULT"), now=1000.0)
        self.assertIn("SENSOR_FAULT", warnings)


if __name__ == "__main__":
    unittest.main()
