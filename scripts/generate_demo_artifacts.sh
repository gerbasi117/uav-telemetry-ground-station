#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p demo logs reports

PYTHON_BIN="${PYTHON_BIN:-python3}"

run_demo() {
  local scenario="$1"
  local duration="$2"
  local rate="$3"
  local output="demo/${scenario}_terminal_output.txt"
  local log="logs/demo_${scenario}.csv"
  local report_json="reports/demo_${scenario}.json"
  local report_md="reports/demo_${scenario}.md"

  echo "Generating demo for scenario: $scenario"
  "$PYTHON_BIN" src/main.py \
    --mode simulate \
    --scenario "$scenario" \
    --duration "$duration" \
    --rate "$rate" \
    --no-dashboard \
    --log "$log" \
    --report "$report_json" \
    --report-md "$report_md" \
    > "$output"
}

run_demo normal 4 2
run_demo unsafe_armed 4 2
run_demo high_current 4 2
run_demo mixed_faults 5 2

# Replay a generated log to demonstrate post-test log analysis.
"$PYTHON_BIN" src/main.py \
  --mode replay \
  --replay logs/demo_mixed_faults.csv \
  --rate 5 \
  --no-dashboard \
  --report reports/demo_replay_mixed_faults.json \
  --report-md reports/demo_replay_mixed_faults.md \
  > demo/replay_mixed_faults_terminal_output.txt

"$PYTHON_BIN" -m unittest discover -s tests > demo/unit_test_output.txt

cat > demo/demo_commands.md <<'CMDS'
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
CMDS

echo "Demo artifacts generated in demo/, logs/, and reports/."
