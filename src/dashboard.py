from __future__ import annotations

import os
from typing import List

from telemetry_parser import TelemetryFrame


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def render_dashboard(frame: TelemetryFrame, warnings: List[str]) -> None:
    clear_screen()
    warning_text = ", ".join(warnings) if warnings else "None"
    print("=" * 64)
    print("UAV TELEMETRY GROUND STATION")
    print("=" * 64)
    print(f"Time:               {frame.timestamp:.2f}")
    print(f"Flight mode:        {frame.flight_mode}")
    print(f"Armed:              {frame.armed}")
    print(f"GPS:                {frame.gps_fix} / {frame.satellite_count} satellites")
    print(f"Position:           {frame.latitude:.6f}, {frame.longitude:.6f}")
    print(f"Altitude:           {frame.altitude_m:.2f} m")
    print(f"Heading:            {frame.heading_deg:.1f} deg")
    print(f"Battery:            {frame.battery_voltage:.2f} V / {frame.battery_percent:.1f}%")
    print(f"Current draw:       {frame.current_draw_a:.1f} A")
    print(f"Link quality:       {frame.link_quality:.1f}%")
    print(f"IMU status:         {frame.imu_status}")
    print(f"Rangefinder:        {frame.rangefinder_distance_m:.2f} m")
    print("-" * 64)
    print(f"WARNINGS:           {warning_text}")
    print("=" * 64)
