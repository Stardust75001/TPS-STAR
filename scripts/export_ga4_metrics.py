#!/usr/bin/env python3
"""
export_ga4_metrics.py — THE PET SOCIETY
GA4 Data API Exporter (sessions, revenue, conversions, timeseries, acquisition)

Outputs:
 - report_data/ga4_metrics.csv
 - report_data/ga4_timeseries.csv
 - report_data/ga4_sources.csv
"""

import os
import csv
import requests
from datetime import datetime, timedelta


BASE_DIR = "report_data"
os.makedirs(BASE_DIR, exist_ok=True)

GA4_PROPERTY_ID = os.getenv("GA4_PROPERTY_ID")
GA4_TOKEN = os.getenv("GA4_TOKEN")  # Generated daily by refresh workflow

if not GA4_PROPERTY_ID:
    raise SystemExit("❌ Missing GA4_PROPERTY_ID in GitHub Secrets.")

if not GA4_TOKEN:
    raise SystemExit("❌ Missing GA4_TOKEN (refresh workflow must run).")


API_URL = f"https://analyticsdata.googleapis.com/v1beta/properties/{GA4_PROPERTY_ID}:runReport"
HEADERS = {"Authorization": f"Bearer {GA4_TOKEN}"}


def ga4_query(body):
    resp = requests.post(API_URL, headers=HEADERS, json=body)
    if resp.status_code != 200:
        print("❌ GA4 ERROR:", resp.text)
        resp.raise_for_status()
    return resp.json()


# ================================
# 1. MAIN KPIS
# ================================
body_kpi = {
    "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
    "metrics": [
        {"name": "sessions"},
        {"name": "totalUsers"},
        {"name": "conversions"},
        {"name": "purchaseRevenue"},
        {"name": "avgSessionDuration"},
        {"name": "bounceRate"}
    ]
}

data = ga4_query(body_kpi)
values = data["rows"][0]["metricValues"]

sessions = float(values[0]["value"])
users = float(values[1]["value"])
convs = float(values[2]["value"])
revenue = float(values[3]["value"])
avg_duration = float(values[4]["value"])
bounce = float(values[5]["value"])


# Write file
metrics_path = os.path.join(BASE_DIR, "ga4_metrics.csv")
with open(metrics_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["metric", "value"])
    w.writerow(["Sessions (7d)", sessions])
    w.writerow(["Users (7d)", users])
    w.writerow(["Conversions (7d)", convs])
    w.writerow(["Revenue (7d)", revenue])
    w.writerow(["Avg Session Duration (s)", avg_duration])
    w.writerow(["Bounce Rate (%)", bounce])

print(f"✅ GA4 KPIs exported → {metrics_path}")


# ================================
# 2. TIMESERIES (sessions, conv, revenue)
# ================================
body_ts = {
    "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
    "dimensions": [{"name": "date"}],
    "metrics": [
        {"name": "sessions"},
        {"name": "conversions"},
        {"name": "purchaseRevenue"},
    ]
}

ts = ga4_query(body_ts)

ts_path = os.path.join(BASE_DIR, "ga4_timeseries.csv")
with open(ts_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "sessions", "conversions", "revenue"])
    for row in ts["rows"]:
        date = row["dimensionValues"][0]["value"]
        s = row["metricValues"][0]["value"]
        c = row["metricValues"][1]["value"]
        r = row["metricValues"][2]["value"]
        w.writerow([date, s, c, r])

print(f"📈 GA4 Timeseries exported → {ts_path}")


# ================================
# 3. ACQUISITION CHANNELS
# ================================
body_src = {
    "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
    "dimensions": [
        {"name": "sessionDefaultChannelGroup"},
        {"name": "medium"},
        {"name": "source"},
    ],
    "metrics": [
        {"name": "sessions"},
        {"name": "conversions"},
        {"name": "purchaseRevenue"},
    ],
    "orderBys": [{
        "metric": {"metricName": "sessions"},
        "desc": True
    }],
    "limit": 50
}

src = ga4_query(body_src)

src_path = os.path.join(BASE_DIR, "ga4_sources.csv")
with open(src_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["channel", "medium", "source", "sessions", "conversions", "revenue"])
    for row in src["rows"]:
        ch = row["dimensionValues"][0]["value"]
        md = row["dimensionValues"][1]["value"]
        so = row["dimensionValues"][2]["value"]
        s = row["metricValues"][0]["value"]
        c = row["metricValues"][1]["value"]
        r = row["metricValues"][2]["value"]
        w.writerow([ch, md, so, s, c, r])

print(f"🌐 GA4 Sources exported → {src_path}")
print("🔥 GA4 export complete.")
