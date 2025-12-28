#!/usr/bin/env python3
"""
Quick CSV report: rows/cols, missing values, basic numeric stats, top categories.

Example:
  python3 src/csv_summary.py --file "data/sample.csv" --out "outputs/report.txt"
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a quick summary report for a CSV file.")
    p.add_argument("--file", required=True, help="Path to CSV file")
    p.add_argument("--out", default="", help="Optional output path for report (txt). If omitted, prints to console.")
    p.add_argument("--top-n", type=int, default=5, help="Top N categories for non-numeric columns")
    return p.parse_args()


def build_report(df: pd.DataFrame, top_n: int = 5) -> str:
    lines: list[str] = []
    lines.append("CSV QUICK SUMMARY")
    lines.append("=" * 60)
    lines.append(f"Rows: {len(df)}")
    lines.append(f"Columns: {df.shape[1]}")
    lines.append("")
    lines.append("Columns:")
    lines.append(", ".join(df.columns))
    lines.append("")

    # Missing values
    missing = df.isna().sum().sort_values(ascending=False)
    lines.append("Missing values (per column):")
    for col, cnt in missing.items():
        lines.append(f"  {col}: {cnt}")
    lines.append("")

    # Numeric stats
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if num_cols:
        lines.append("Numeric columns summary:")
        desc = df[num_cols].describe().T
        for col in num_cols:
            row = desc.loc[col]
            lines.append(
                f"  {col}: mean={row['mean']:.2f}, std={row['std']:.2f}, min={row['min']:.2f}, max={row['max']:.2f}"
            )
        lines.append("")
    else:
        lines.append("No numeric columns detected.\n")

    # Categorical top values
    cat_cols = [c for c in df.columns if c not in num_cols]
    if cat_cols:
        lines.append("Top categories (non-numeric columns):")
        for col in cat_cols:
            lines.append(f"\n{col}:")
            vc = df[col].astype(str).value_counts().head(top_n)
            for k, v in vc.items():
                lines.append(f"  {k}: {v}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    path = Path(args.file).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Error: file not found: {path}")

    df = pd.read_csv(path)
    report = build_report(df, top_n=args.top_n)

    if args.out:
        out = Path(args.out).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="_
