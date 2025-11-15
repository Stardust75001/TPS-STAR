#!/usr/bin/env python3
import pandas as pd

shop = pd.read_csv("report_data/shopify_metrics.csv")
ga4 = pd.read_csv("report_data/ga4_metrics.csv")

merged = pd.concat([shop, ga4], ignore_index=True)
merged.to_csv("report_data/metrics_full_report.csv", index=False)

print("✅ Merge OK → metrics_full_report.csv")
