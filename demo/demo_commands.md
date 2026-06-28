# Demo Commands

Run unit tests:

```bash
python3 -m unittest discover -s tests
```

Run a normal flight scenario:

```bash
python3 src/main.py --mode simulate --scenario normal --duration 5 --rate 2 --no-dashboard
```

Run an unsafe armed-state scenario and generate reports:

```bash
python3 src/main.py --mode simulate --scenario unsafe_armed --duration 5 --rate 2 --no-dashboard --report reports/unsafe_armed.json --report-md reports/unsafe_armed.md
```

Run a mixed-fault scenario:

```bash
python3 src/main.py --mode simulate --scenario mixed_faults --duration 8 --rate 2 --no-dashboard --log logs/mixed_faults.csv --report reports/mixed_faults.json --report-md reports/mixed_faults.md
```

Replay a saved log:

```bash
python3 src/main.py --mode replay --replay logs/demo_mixed_faults.csv --rate 5 --no-dashboard --report reports/replay_mixed_faults.json --report-md reports/replay_mixed_faults.md
```
