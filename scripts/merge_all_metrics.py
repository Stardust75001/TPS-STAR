#!/usr/bin/env python3
import pandas as pd
import sys

def merge_metrics(shopify_csv, ga4_csv, output_csv):
    shop = pd.read_csv(shopify_csv)
    ga4 = pd.read_csv(ga4_csv)

    merged = pd.concat([shop, ga4], axis=1)
    merged.to_csv(output_csv, index=False)

    print(f"✅ Full metrics exported → {output_csv}")

def main():
    merge_metrics(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
