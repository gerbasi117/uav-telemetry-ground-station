# Demo Output

## Normal scenario

```bash
python src/main.py --mode simulate --scenario normal --duration 5 --rate 2 --no-dashboard
```

Expected output includes stable GPS, battery, current draw, and no warning states.

## Unsafe armed scenario

```bash
python src/main.py --mode simulate --scenario unsafe_armed --duration 5 --rate 2 --no-dashboard
```

Expected warning states:

- GPS_LOST
- LOW_SATELLITE_COUNT
- ARMED_WITH_BAD_GPS

## High-current scenario

```bash
python src/main.py --mode simulate --scenario high_current --duration 5 --rate 2 --no-dashboard
```

Expected warning state:

- HIGH_CURRENT_DRAW

## Mixed-fault scenario

```bash
python src/main.py --mode simulate --scenario mixed_faults --duration 10 --rate 2 --no-dashboard
```

Expected output rotates through GPS, current, link, rangefinder, and sensor warnings.

## Report generation

```bash
python3 src/main.py --mode simulate --scenario mixed_faults --duration 8 --rate 2 --no-dashboard --log logs/mixed_faults.csv --report reports/mixed_faults_report.json --report-md reports/mixed_faults_report.md
```

Expected final line:

```text
Flight summary: samples=16 status=UNSAFE warnings={...}
```

Open the generated Markdown report:

```bash
less reports/mixed_faults_report.md
```
