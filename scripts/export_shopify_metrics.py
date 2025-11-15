#!/usr/bin/env python3
"""
export_shopify_metrics.py

Usage:
  python export_shopify_metrics.py shopify_metrics.csv shopify_timeseries.csv

Sortie 1 (résumé 7j) : shopify_metrics.csv
  metric,value
  Revenue (7d),1234.50
  Conversions (7d),42
  AOV (7d),29.39

Sortie 2 (timeseries) : shopify_timeseries.csv
  date,revenue,orders,aov
  2025-11-08,123.45,3,41.15
  ...
"""

import os
import sys
import csv
from datetime import datetime, timedelta, timezone

import requests


def get_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise SystemExit(f"❌ Missing env var: {name}")
    return val


def fetch_orders_7d():
    store_domain = get_env("SHOPIFY_STORE_DOMAIN")
    token = get_env("SHOPIFY_ADMIN_API_ACCESS_TOKEN")

    base_url = f"https://{store_domain}/admin/api/2024-07/orders.json"

    end_dt = datetime.now(timezone.utc)
    start_dt = end_dt - timedelta(days=7)

    params = {
        "status": "any",
        "created_at_min": start_dt.isoformat(),
        "created_at_max": end_dt.isoformat(),
        "limit": 250,
        "fields": "id,total_price,created_at"
    }

    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    orders = []
    url = base_url

    while True:
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            raise SystemExit(f"❌ Shopify API error {resp.status_code}: {resp.text}")

        data = resp.json().get("orders", [])
        orders.extend(data)

        # Pagination via Link header (page_info)
        link = resp.headers.get("Link")
        if not link or 'rel="next"' not in link:
            break

        next_url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                # <https://..page_info=XXXX>; rel="next"
                start = part.find("<") + 1
                end = part.find(">")
                next_url = part[start:end]
                break

        if not next_url:
            break

        url = next_url
        params = {}  # déjà inclus dans next_url

    return orders


def aggregate_metrics(orders):
    # dict date -> [revenue_sum, order_count]
    by_date = {}

    for o in orders:
        created = datetime.fromisoformat(o["created_at"].replace("Z", "+00:00"))
        date_key = created.date().isoformat()
        total_price = float(o.get("total_price", 0.0))

        if date_key not in by_date:
            by_date[date_key] = {"revenue": 0.0, "orders": 0}

        by_date[date_key]["revenue"] += total_price
        by_date[date_key]["orders"] += 1

    # résumé global
    total_rev = sum(v["revenue"] for v in by_date.values())
    total_orders = sum(v["orders"] for v in by_date.values())
    aov = total_rev / total_orders if total_orders else 0.0

    return by_date, total_rev, total_orders, aov


def write_summary_csv(path, total_rev, total_orders, aov):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["Revenue (7d)", f"{total_rev:.2f}"])
        writer.writerow(["Conversions (7d)", total_orders])
        writer.writerow(["AOV (7d)", f"{aov:.2f}"])


def write_timeseries_csv(path, by_date):
    rows = []
    for d, vals in sorted(by_date.items()):
        rev = vals["revenue"]
        orders = vals["orders"]
        aov = rev / orders if orders else 0.0
        rows.append([d, f"{rev:.2f}", orders, f"{aov:.2f}"])

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "revenue", "orders", "aov"])
        writer.writerows(rows)


def main():
    if len(sys.argv) != 3:
        print("Usage: export_shopify_metrics.py shopify_metrics.csv shopify_timeseries.csv")
        raise SystemExit(1)

    summary_path = sys.argv[1]
    timeseries_path = sys.argv[2]

    print("📦 Fetching Shopify orders (last 7 days)...")
    orders = fetch_orders_7d()
    print(f"✅ {len(orders)} orders fetched")

    by_date, total_rev, total_orders, aov = aggregate_metrics(orders)

    write_summary_csv(summary_path, total_rev, total_orders, aov)
    write_timeseries_csv(timeseries_path, by_date)

    print(f"✅ Shopify summary  -> {summary_path}")
    print(f"✅ Shopify timeseries -> {timeseries_path}")


if __name__ == "__main__":
    main()
