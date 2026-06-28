from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Iterator

from telemetry_parser import TelemetryFrame


FIELDNAMES = [
    "timestamp",
    "flight_mode",
    "armed",
    "latitude",
    "longitude",
    "altitude_m",
    "heading_deg",
    "battery_voltage",
    "battery_percent",
    "current_draw_a",
    "gps_fix",
    "satellite_count",
    "link_quality",
    "imu_status",
    "rangefinder_distance_m",
]


class CsvTelemetryLogger:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.file = self.path.open("w", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(self.file, fieldnames=FIELDNAMES)
        self.writer.writeheader()

    def write(self, frame: TelemetryFrame) -> None:
        self.writer.writerow(frame.to_dict())
        self.file.flush()

    def close(self) -> None:
        self.file.close()


def replay_csv(path: str) -> Iterator[TelemetryFrame]:
    with Path(path).open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield TelemetryFrame.from_dict(row)


def replay_jsonl(path: str) -> Iterator[TelemetryFrame]:
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield TelemetryFrame.from_dict(json.loads(line))
