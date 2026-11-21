#!/usr/bin/env python3
"""Check the dataset against criterion 1 and write output/data_quality.csv.

Usage: python data_quality.py [--data data/generated.csv] [--out output/data_quality.csv]
Exits 1 if any check fails.
"""
import argparse
import sys

import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/generated.csv")
    ap.add_argument("--out", default="output/data_quality.csv")
    args = ap.parse_args()

    df = pd.read_csv(args.data, parse_dates=["created_at", "resolved_at"])
    closed = df[df["status"] == "closed"]
    days = (df["created_at"].max() - df["created_at"].min()).days

    rows = [
        ("row_count", len(df), ">= 10000", len(df) >= 10000),
        ("first_created_at", df["created_at"].min(), "", True),
        ("last_created_at", df["created_at"].max(), "", True),
        ("days_covered", days, ">= 90", days >= 90),
        ("category_count", df["category"].nunique(), ">= 4", df["category"].nunique() >= 4),
        ("closed_rows", len(closed), "", True),
        ("open_or_in_progress_rows", len(df) - len(closed), "", True),
        ("closed_rows_missing_resolution", int(closed["resolution_hours"].isna().sum()), "0",
         closed["resolution_hours"].isna().sum() == 0),
        ("duplicate_ids", int(df["id"].duplicated().sum()), "0", df["id"].duplicated().sum() == 0),
    ]
    for col in df.columns:
        n = int(df[col].isna().sum())
        ok = True if col in ("resolved_at", "resolution_hours") else n == 0
        rows.append((f"nulls_{col}", n, "0" if col not in ("resolved_at", "resolution_hours") else "open rows only", ok))

    out = pd.DataFrame(rows, columns=["check", "value", "expected", "pass"])
    out.to_csv(args.out, index=False)
    print(out.to_string(index=False))
    if not out["pass"].all():
        print("\nSome checks FAILED.")
        sys.exit(1)
    print("\nAll data quality checks passed.")


if __name__ == "__main__":
    main()
