#!/usr/bin/env python3
import argparse
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="CSV produced by log_to_csv.py")
    ap.add_argument("--out", required=True, help="Output summary CSV")
    args = ap.parse_args()

    df = pd.read_csv(args.csv)
    # dt_ms here is inter-command interval, not true network latency
    df["dt_ms"] = pd.to_numeric(df["dt_ms"], errors="coerce")

    summary = df.groupby("cmd").agg(
        n=("cmd", "count"),
        lin_mean=("lin", "mean"),
        ang_mean=("ang", "mean"),
        dt_ms_mean=("dt_ms", "mean"),
        dt_ms_p95=("dt_ms", lambda x: x.dropna().quantile(0.95) if x.dropna().size else float("nan")),
    ).reset_index()

    summary.to_csv(args.out, index=False)
    print(f"Wrote summary -> {args.out}")

if __name__ == "__main__":
    main()
