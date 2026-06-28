from __future__ import annotations

import argparse
import time
from pathlib import Path

from dashboard import render_dashboard
from logger import CsvTelemetryLogger, replay_csv, replay_jsonl
from telemetry_generator import TelemetryGenerator
from warning_engine import WarningEngine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="UAV telemetry ground station MVP")
    parser.add_argument("--mode", choices=["simulate", "replay"], default="simulate")
    parser.add_argument("--duration", type=float, default=60.0, help="Simulation duration in seconds")
    parser.add_argument("--rate", type=float, default=2.0, help="Frames per second")
    parser.add_argument("--log", type=str, default="", help="Optional CSV log output path")
    parser.add_argument("--replay", type=str, default="data/sample_flight_log.csv", help="CSV or JSONL log to replay")
    parser.add_argument("--no-dashboard", action="store_true", help="Print compact output instead of dashboard")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    engine = WarningEngine()
    logger = CsvTelemetryLogger(args.log) if args.log else None

    if args.mode == "simulate":
        frames = TelemetryGenerator().frames(duration_s=args.duration, rate_hz=args.rate)
    else:
        replay_path = Path(args.replay)
        if replay_path.suffix.lower() == ".jsonl":
            frames = replay_jsonl(str(replay_path))
        else:
            frames = replay_csv(str(replay_path))

    try:
        for frame in frames:
            warnings = engine.evaluate(frame)
            if logger:
                logger.write(frame)

            if args.no_dashboard:
                print(f"{frame.flight_mode} armed={frame.armed} alt={frame.altitude_m:.1f}m batt={frame.battery_percent:.1f}% warnings={warnings or ['None']}")
            else:
                render_dashboard(frame, warnings)

            if args.mode == "replay":
                time.sleep(1.0 / args.rate if args.rate > 0 else 0.5)
    finally:
        if logger:
            logger.close()


if __name__ == "__main__":
    main()
