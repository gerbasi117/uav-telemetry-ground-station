from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from telemetry_parser import TelemetryFrame


UNSAFE_WARNINGS = {
    "CRITICAL_BATTERY",
    "HIGH_CURRENT_DRAW",
    "ARMED_WITH_BAD_GPS",
    "SENSOR_FAULT",
    "TELEMETRY_TIMEOUT",
    "STALE_TELEMETRY",
}

CAUTION_WARNINGS = {
    "LOW_BATTERY",
    "GPS_LOST",
    "LOW_SATELLITE_COUNT",
    "LOW_LINK_QUALITY",
    "RANGEFINDER_TOO_CLOSE",
}


class FlightReportRecorder:
    """Collects telemetry frames and warning states, then produces a flight summary.

    This is intentionally simple and explainable for interviews. The goal is not
    to replace a production ground station; it is to demonstrate telemetry
    analysis, warning aggregation, and safety-focused reporting.
    """

    def __init__(self, scenario: str = "unknown", source: str = "simulate") -> None:
        self.scenario = scenario
        self.source = source
        self.frames: List[TelemetryFrame] = []
        self.warning_counts: Counter[str] = Counter()
        self.first_warning_timestamp: Optional[float] = None

    def add_sample(self, frame: TelemetryFrame, warnings: Iterable[str]) -> None:
        self.frames.append(frame)
        warning_list = [w for w in warnings if w and w != "None"]
        if warning_list and self.first_warning_timestamp is None:
            self.first_warning_timestamp = frame.timestamp
        self.warning_counts.update(warning_list)

    def safety_status(self) -> str:
        if not self.frames:
            return "NO_DATA"
        if any(self.warning_counts.get(w, 0) > 0 for w in UNSAFE_WARNINGS):
            return "UNSAFE"
        if any(self.warning_counts.get(w, 0) > 0 for w in CAUTION_WARNINGS):
            return "CAUTION"
        return "NOMINAL"

    def recommended_actions(self) -> List[str]:
        actions: List[str] = []
        counts = self.warning_counts

        if counts.get("CRITICAL_BATTERY", 0) or counts.get("LOW_BATTERY", 0):
            actions.append("Inspect battery state, capacity assumptions, and voltage/current calibration.")
        if counts.get("GPS_LOST", 0) or counts.get("LOW_SATELLITE_COUNT", 0):
            actions.append("Verify GPS placement, antenna visibility, wiring, and pre-flight GPS lock requirements.")
        if counts.get("ARMED_WITH_BAD_GPS", 0):
            actions.append("Review arming checks and block autonomous/GPS-dependent modes until GPS health is acceptable.")
        if counts.get("HIGH_CURRENT_DRAW", 0):
            actions.append("Inspect propulsion load, prop selection, motor/ESC behavior, wiring resistance, and battery sag.")
        if counts.get("LOW_LINK_QUALITY", 0):
            actions.append("Check telemetry-radio placement, antenna orientation, RF interference, and link budget.")
        if counts.get("RANGEFINDER_TOO_CLOSE", 0):
            actions.append("Validate rangefinder mounting, filtering, and obstacle/landing safety thresholds.")
        if counts.get("SENSOR_FAULT", 0):
            actions.append("Check IMU/sensor health, calibration, vibration isolation, and wiring.")
        if counts.get("TELEMETRY_TIMEOUT", 0) or counts.get("STALE_TELEMETRY", 0):
            actions.append("Investigate telemetry dropouts, timestamps, serial/transport settings, and ground-station timeout handling.")

        if not actions:
            actions.append("No warnings detected. Continue with normal post-flight inspection and log review.")
        return actions

    def summary(self) -> Dict[str, Any]:
        if not self.frames:
            return {
                "scenario": self.scenario,
                "source": self.source,
                "sample_count": 0,
                "duration_s": 0.0,
                "final_safety_status": "NO_DATA",
                "warning_counts": {},
                "recommended_actions": ["No telemetry samples were recorded."],
            }

        start = self.frames[0].timestamp
        end = self.frames[-1].timestamp
        min_battery_percent = min(f.battery_percent for f in self.frames)
        min_battery_voltage = min(f.battery_voltage for f in self.frames)
        max_current = max(f.current_draw_a for f in self.frames)
        max_altitude = max(f.altitude_m for f in self.frames)
        min_rangefinder = min(f.rangefinder_distance_m for f in self.frames)
        gps_loss_samples = sum(1 for f in self.frames if f.gps_fix.upper() not in {"3D", "3D_FIX", "RTK", "DGPS"})
        armed_samples = sum(1 for f in self.frames if f.armed)

        return {
            "scenario": self.scenario,
            "source": self.source,
            "sample_count": len(self.frames),
            "start_timestamp": start,
            "end_timestamp": end,
            "duration_s": round(max(0.0, end - start), 3),
            "min_battery_percent": round(min_battery_percent, 2),
            "min_battery_voltage": round(min_battery_voltage, 2),
            "max_current_draw_a": round(max_current, 2),
            "max_altitude_m": round(max_altitude, 2),
            "min_rangefinder_distance_m": round(min_rangefinder, 2),
            "gps_loss_samples": gps_loss_samples,
            "armed_samples": armed_samples,
            "warning_counts": dict(sorted(self.warning_counts.items())),
            "first_warning_timestamp": self.first_warning_timestamp,
            "final_safety_status": self.safety_status(),
            "recommended_actions": self.recommended_actions(),
        }

    def to_markdown(self) -> str:
        s = self.summary()
        warning_counts = s.get("warning_counts", {})
        actions = s.get("recommended_actions", [])

        lines = [
            "# Flight Summary Report",
            "",
            f"**Scenario:** `{s.get('scenario', 'unknown')}`",
            f"**Source:** `{s.get('source', 'unknown')}`",
            f"**Final safety status:** **{s.get('final_safety_status', 'UNKNOWN')}**",
            "",
            "## Summary",
            "",
            f"- Samples: {s.get('sample_count', 0)}",
            f"- Duration: {s.get('duration_s', 0.0)} seconds",
            f"- Minimum battery: {s.get('min_battery_percent', 'n/a')}% / {s.get('min_battery_voltage', 'n/a')} V",
            f"- Maximum current draw: {s.get('max_current_draw_a', 'n/a')} A",
            f"- Maximum altitude: {s.get('max_altitude_m', 'n/a')} m",
            f"- Minimum rangefinder distance: {s.get('min_rangefinder_distance_m', 'n/a')} m",
            f"- GPS-loss samples: {s.get('gps_loss_samples', 0)}",
            f"- Armed samples: {s.get('armed_samples', 0)}",
            "",
            "## Warning Counts",
            "",
        ]

        if warning_counts:
            lines.extend(["| Warning | Count |", "|---|---:|"])
            for warning, count in warning_counts.items():
                lines.append(f"| {warning} | {count} |")
        else:
            lines.append("No warnings detected.")

        lines.extend(["", "## Recommended Actions", ""])
        for action in actions:
            lines.append(f"- {action}")

        lines.extend([
            "",
            "## Portfolio Note",
            "",
            "This report is generated from simulated/replayed telemetry to demonstrate UAV log analysis, warning aggregation, and operator-facing safety summaries. Future versions can connect this workflow to MAVLink/PX4/ArduPilot telemetry and real field-test logs.",
            "",
        ])
        return "\n".join(lines)

    def write_json(self, path: str) -> None:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(self.summary(), indent=2), encoding="utf-8")

    def write_markdown(self, path: str) -> None:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_markdown(), encoding="utf-8")
