#!/usr/bin/env python3
import requests
import pandas as pd
from datetime import datetime, UTC
import argparse
import os

def fetch_shopify_metrics(domain, token):
    base = f"https://{domain}/admin/api/2025-01"
    headers = {"X-Shopify-Access-Token": token}

    # Orders
    orders_url = f"{base}/orders.json?status=any&limit=250"
    orders = requests.get(orders_url, headers=headers).json().get("orders", [])

    total_orders = len(orders)
    total_revenue = sum(float(o.get("total_price", 0)) for o in orders)

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "generated_at": datetime.now(UTC).isoformat()
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    metrics = fetch_shopify_metrics(args.domain, args.token)
    df = pd.DataFrame([metrics])
    df.to_csv(f"{args.outdir}/shopify_metrics.csv", index=False)

    print("✅ Shopify metrics exported → report_data/shopify_metrics.csv")

if __name__ == "__main__":
    main()
