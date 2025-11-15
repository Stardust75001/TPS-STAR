#!/usr/bin/env python3
import os
import requests
import pandas as pd
from datetime import datetime, timedelta

SHOPIFY_STORE = os.environ.get("SHOPIFY_STORE_DOMAIN")
API_KEY = os.environ.get("SHOPIFY_API_KEY")
API_PASS = os.environ.get("SHOPIFY_API_PASSWORD")

BASE_URL = f"https://{API_KEY}:{API_PASS}@{SHOPIFY_STORE}/admin/api/2024-10"

OUT_METRICS = "report_data/shopify_metrics.csv"
OUT_TS = "report_data/shopify_timeseries.csv"

def get_orders_last_7_days():
    since = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT00:00:00Z")
    url = f"{BASE_URL}/orders.json?status=any&created_at_min={since}&limit=250"
    r = requests.get(url)
    data = r.json().get("orders", [])
    return pd.DataFrame(data)

def get_orders_last_30_days():
    since = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%dT00:00:00Z")
    url = f"{BASE_URL}/orders.json?status=any&created_at_min={since}&limit=250"
    r = requests.get(url)
    data = r.json().get("orders", [])
    df = pd.DataFrame(data)
    if df.empty:
        return df
    df["day"] = pd.to_datetime(df["created_at"]).dt.date
    return df.groupby("day")["total_price"].sum().reset_index()

def main():
    df7 = get_orders_last_7_days()
    revenue = df7["total_price"].astype(float).sum() if not df7.empty else 0
    conv = len(df7)
    aov = (revenue / conv) if conv else 0

    pd.DataFrame({
        "metric": ["Revenue (7d)", "Conversions (7d)", "AOV (7d)"],
        "value": [revenue, conv, aov],
        "source": "shopify",
    }).to_csv(OUT_METRICS, index=False)

    df30 = get_orders_last_30_days()
    if not df30.empty:
        df30.rename(columns={"day": "date", "total_price": "revenue"}, inplace=True)
    df30.to_csv(OUT_TS, index=False)

    print("✅ Shopify export OK")

if __name__ == "__main__":
