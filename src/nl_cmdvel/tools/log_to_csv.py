#!/usr/bin/env python3
import argparse
import csv
import re

# Parses log lines like:
# [INFO] ... cmd='forward' -> lin=0.15, ang=0.00, dt_ms=123.4
PAT = re.compile(r"cmd='(?P<cmd>[^']+)'\s*->\s*lin=(?P<lin>-?\d+\.\d+),\s*ang=(?P<ang>-?\d+\.\d+)(?:,\s*dt_ms=(?P<dt>\d+\.\d+))?")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True, help="Path to run_log.txt (captured with tee)")
    ap.add_argument("--csv", required=True, help="Output CSV path")
    args = ap.parse_args()

    rows = []
    with open(args.log, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = PAT.search(line)
            if not m:
                continue
            rows.append({
                "cmd": m.group("cmd"),
                "lin": float(m.group("lin")),
                "ang": float(m.group("ang")),
                "dt_ms": float(m.group("dt")) if m.group("dt") else "",
            })

    with open(args.csv, "w", newline="", encoding="utf-8") as out:
        w = csv.DictWriter(out, fieldnames=["cmd", "lin", "ang", "dt_ms"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"Wrote {len(rows)} rows -> {args.csv}")

if __name__ == "__main__":
    main()
