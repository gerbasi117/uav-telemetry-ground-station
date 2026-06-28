import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from flight_report import FlightReportRecorder
from telemetry_parser import TelemetryFrame


def frame(**overrides):
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


class FlightReportTests(unittest.TestCase):
    def test_nominal_report(self):
        recorder = FlightReportRecorder(scenario="normal", source="unit-test")
        recorder.add_sample(frame(timestamp=1000.0), [])
        recorder.add_sample(frame(timestamp=1001.0, battery_percent=79.0), [])
        summary = recorder.summary()
        self.assertEqual(summary["sample_count"], 2)
        self.assertEqual(summary["final_safety_status"], "NOMINAL")
        self.assertEqual(summary["min_battery_percent"], 79.0)

    def test_unsafe_report(self):
        recorder = FlightReportRecorder(scenario="unsafe", source="unit-test")
        recorder.add_sample(frame(timestamp=1000.0, armed=True, gps_fix="NO_FIX", satellite_count=3), ["GPS_LOST", "ARMED_WITH_BAD_GPS"])
        summary = recorder.summary()
        self.assertEqual(summary["final_safety_status"], "UNSAFE")
        self.assertEqual(summary["warning_counts"]["ARMED_WITH_BAD_GPS"], 1)
        self.assertTrue(any("GPS" in action or "arming" in action.lower() for action in summary["recommended_actions"]))

    def test_write_json_and_markdown(self):
        recorder = FlightReportRecorder(scenario="test", source="unit-test")
        recorder.add_sample(frame(timestamp=1000.0), [])
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "report.json"
            md_path = Path(tmp) / "report.md"
            recorder.write_json(str(json_path))
            recorder.write_markdown(str(md_path))
            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())
            self.assertEqual(json.loads(json_path.read_text())["final_safety_status"], "NOMINAL")
            self.assertIn("Flight Summary Report", md_path.read_text())


if __name__ == "__main__":
    unittest.main()
