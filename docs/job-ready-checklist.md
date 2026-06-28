# Job-Ready Checklist - UAV Telemetry Ground Station

Use this checklist before linking this repo on a resume, LinkedIn, or recruiter message.

## Required

- [ ] Unit tests pass with `python3 -m unittest discover -s tests`
- [ ] Normal scenario runs
- [ ] Unsafe armed scenario runs
- [ ] Mixed-fault scenario runs
- [ ] CSV log generation works
- [ ] JSON flight report generation works
- [ ] Markdown flight report generation works
- [ ] README has quick-start commands
- [ ] Demo output or screenshots are included
- [ ] Resume bullets are included in README

## Demo commands

```bash
python3 src/main.py --mode simulate --scenario normal --duration 5 --rate 2 --no-dashboard --report reports/normal.json --report-md reports/normal.md
python3 src/main.py --mode simulate --scenario unsafe_armed --duration 5 --rate 2 --no-dashboard --report reports/unsafe_armed.json --report-md reports/unsafe_armed.md
python3 src/main.py --mode simulate --scenario mixed_faults --duration 8 --rate 2 --no-dashboard --log logs/mixed_faults.csv --report reports/mixed_faults.json --report-md reports/mixed_faults.md
python3 src/main.py --mode replay --replay data/sample_flight_log.csv --rate 5 --no-dashboard --report reports/replay_sample.json --report-md reports/replay_sample.md
```

## Interview explanation

This project demonstrates how I would approach UAV/robotics field telemetry: collect frames, evaluate warning states, log data, replay logs, and produce operator-facing reports. It is intentionally simulated first so the warning logic and reporting workflow can be tested before connecting to live MAVLink/PX4/ArduPilot telemetry.
