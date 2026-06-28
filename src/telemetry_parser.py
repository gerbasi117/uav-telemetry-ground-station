from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class TelemetryFrame:
    timestamp: float
    flight_mode: str
    armed: bool
    latitude: float
    longitude: float
    altitude_m: float
    heading_deg: float
    battery_voltage: float
    battery_percent: float
    current_draw_a: float
    gps_fix: str
    satellite_count: int
    link_quality: float
    imu_status: str
    rangefinder_distance_m: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TelemetryFrame":
        return cls(
            timestamp=float(data["timestamp"]),
            flight_mode=str(data["flight_mode"]),
            armed=str(data["armed"]).lower() in {"true", "1", "yes"} if not isinstance(data["armed"], bool) else data["armed"],
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            altitude_m=float(data["altitude_m"]),
            heading_deg=float(data["heading_deg"]),
            battery_voltage=float(data["battery_voltage"]),
            battery_percent=float(data["battery_percent"]),
            current_draw_a=float(data["current_draw_a"]),
            gps_fix=str(data["gps_fix"]),
            satellite_count=int(float(data["satellite_count"])),
            link_quality=float(data["link_quality"]),
            imu_status=str(data["imu_status"]),
            rangefinder_distance_m=float(data["rangefinder_distance_m"]),
        )
