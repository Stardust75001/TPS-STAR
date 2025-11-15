#!/usr/bin/env python3
"""
merge_all_metrics.py

Usage:
  python merge_all_metrics.py report_data report_data/metrics_full_report.csv

Lit :
  <base>/shopify_metrics.csv
  <base>/ga4_metrics.csv

Produit :
  metrics_full_report.csv  (source,metric,value)
"""

import sys
import os
import pandas as pd


def load_or_empty(path, source_name):
    if not os.path.exists(path):
        return pd.DataFrame(columns=["metric", "value", "source"])
    df = pd.read_csv(path)
    df["source"] = source_name
    return df[["source", "metric", "value"]]


def main():
    if len(sys.argv) != 3:
        print("Usage: merge_all_metrics.py <base_dir> <output_csv>")
        raise SystemExit(1)

    base_dir = sys.argv[1]
    out_path = sys.argv[2]

    shopify_path = os.path.join(base_dir, "shopify_metrics.csv")
    ga4_path = os.path.join(base_dir, "ga4_metrics.csv")

    shopify_df = load_or_empty(shopify_path, "shopify")
    ga4_df = load_or_empty(ga4_path, "ga4")

    full = pd.concat([shopify_df, ga4_df], ignore_index=True)
    full.to_csv(out_path, index=False)

    print(f"✅ Merged metrics written to: {out_path}")


if __name__ == "__main__":
    main()
