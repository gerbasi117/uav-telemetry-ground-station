from __future__ import annotations

import argparse
import time
from pathlib import Path

from dashboard import render_dashboard
from flight_report import FlightReportRecorder
from logger import CsvTelemetryLogger, replay_csv, replay_jsonl
from telemetry_generator import SCENARIOS, TelemetryGenerator
from warning_engine import WarningEngine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="UAV telemetry ground station MVP")
    parser.add_argument("--mode", choices=["simulate", "replay"], default="simulate")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="normal", help="Simulation warning scenario")
    parser.add_argument("--duration", type=float, default=60.0, help="Simulation duration in seconds")
    parser.add_argument("--rate", type=float, default=2.0, help="Frames per second")
    parser.add_argument("--log", type=str, default="", help="Optional CSV log output path")
    parser.add_argument("--replay", type=str, default="data/sample_flight_log.csv", help="CSV or JSONL log to replay")
    parser.add_argument("--no-dashboard", action="store_true", help="Print compact output instead of dashboard")
    parser.add_argument("--report", type=str, default="", help="Optional JSON flight-summary report output path")
    parser.add_argument("--report-md", type=str, default="", help="Optional Markdown flight-summary report output path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    engine = WarningEngine()
    logger = CsvTelemetryLogger(args.log) if args.log else None
    source = args.mode
    scenario = args.scenario if args.mode == "simulate" else Path(args.replay).name
    report = FlightReportRecorder(scenario=scenario, source=source)

    if args.mode == "simulate":
        frames = TelemetryGenerator(scenario=args.scenario).frames(duration_s=args.duration, rate_hz=args.rate)
    else:
        replay_path = Path(args.replay)
        if replay_path.suffix.lower() == ".jsonl":
            frames = replay_jsonl(str(replay_path))
        else:
            frames = replay_csv(str(replay_path))

    try:
        for frame in frames:
            warnings = engine.evaluate(frame)
            report.add_sample(frame, warnings)

            if logger:
                logger.write(frame)

            if args.no_dashboard:
                print(
                    f"mode={frame.flight_mode:<9} armed={str(frame.armed):<5} "
                    f"alt={frame.altitude_m:>5.1f}m batt={frame.battery_percent:>5.1f}% "
                    f"gps={frame.gps_fix}/{frame.satellite_count} current={frame.current_draw_a:>5.1f}A "
                    f"link={frame.link_quality:>5.1f}% warnings={warnings or ['None']}"
                )
            else:
                render_dashboard(frame, warnings)

            if args.mode == "replay":
                time.sleep(1.0 / args.rate if args.rate > 0 else 0.5)
    finally:
        if logger:
            logger.close()

        wrote_report = False
        if args.report:
            report.write_json(args.report)
            print(f"JSON report written: {args.report}")
            wrote_report = True
        if args.report_md:
            report.write_markdown(args.report_md)
            print(f"Markdown report written: {args.report_md}")
            wrote_report = True

        if wrote_report:
            summary = report.summary()
            print(
                "Flight summary: "
                f"samples={summary.get('sample_count')} "
                f"status={summary.get('final_safety_status')} "
                f"warnings={summary.get('warning_counts', {})}"
            )


if __name__ == "__main__":
    main()
