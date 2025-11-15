#!/usr/bin/env python3
"""
export_ga4_metrics.py
Exports GA4 KPIs and timeseries using the GA4 Data API.

Generates:
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

# ----------------------------------------------------------
# LOAD SECRETS
# ----------------------------------------------------------
GA4_PROPERTY_ID = os.getenv("GA4_PROPERTY_ID")
GA4_TOKEN = os.getenv("GA4_TOKEN")   # Access token refreshed daily

if not GA4_TOKEN:
    raise SystemExit("❌ GA4_TOKEN missing. Make sure refresh workflow ran.")

if not GA4_PROPERTY_ID:
    raise SystemExit("❌ GA4_PROPERTY_ID missing in GitHub secrets.")


# ----------------------------------------------------------
# GA4 API WRAPPER
# ----------------------------------------------------------
API_URL = f"https://analyticsdata.googleapis.com/v1beta/properties/{GA4_PROPERTY_ID}:runReport"
HEADERS = {"Authorization": f"Bearer {GA4_TOKEN}"}


def ga4_request(body):
    resp = requests.post(API_URL, headers=HEADERS, json=body)
    if resp.status_code != 200:
        print("❌ GA4 API ERROR:", resp.text)
        resp.raise_for_status()
    return resp.json()


# ----------------------------------------------------------
# 1 — Main KPIs (last 7 days)
# ----------------------------------------------------------
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

kpi = ga4_request(body_kpi)
values = [float(r["metricValues"][0]["value"]) for r in kpi.get("rows", [])]

sessions = float(kpi["rows"][0]["metricValues"][0]["value"])
users = float(kpi["rows"][0]["metricValues"][1]["value"])
conversions = float(kpi["rows"][0]["metricValues"][2]["value"])
revenue = float(kpi["rows"][0]["metricValues"][3]["value"])
avg_duration = float(kpi["rows"][0]["metricValues"][4]["value"])
bounce = float(kpi["rows"][0]["metricValues"][5]["value"])

# WRITE ga4_metrics.csv
metrics_path = os.path.join(BASE_DIR, "ga4_metrics.csv")
with open(metrics_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["metric", "value"])
    w.writerow(["Sessions (7d)", sessions])
    w.writerow(["Users (7d)", users])
    w.writerow(["Conversions (7d)", conversions])
    w.writerow(["Revenue (7d)", revenue])
    w.writerow(["Avg Session Duration (sec)", avg_duration])
    w.writerow(["Bounce Rate (%)", bounce])

print(f"✅ Generated: {metrics_path}")


# ----------------------------------------------------------
# 2 — Timeseries (sessions, conversions, revenue)
# ----------------------------------------------------------
body_timeseries = {
    "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
    "dimensions": [{"name": "date"}],
    "metrics": [
        {"name": "sessions"},
        {"name": "conversions"},
        {"name": "purchaseRevenue"}
    ]
}

ts = ga4_request(body_timeseries)

ts_path = os.path.join(BASE_DIR, "ga4_timeseries.csv")
with open(ts_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "sessions", "conversions", "revenue"])
    for row in ts.get("rows", []):
        date = row["dimensionValues"][0]["value"]
        s = row["metricValues"][0]["value"]
        c = row["metricValues"][1]["value"]
        r = row["metricValues"][2]["value"]
        w.writerow([date, s, c, r])

print(f"📈 Generated: {ts_path}")


# ----------------------------------------------------------
# 3 — Acquisition sources (channel groups)
# ----------------------------------------------------------
body_sources = {
    "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
    "dimensions": [
        {"name": "sessionDefaultChannelGroup"},
        {"name": "medium"},
        {"name": "source"},
    ],
    "metrics": [{"name": "sessions"}, {"name": "conversions"}, {"name": "purchaseRevenue"}],
    "orderBys": [{
        "metric": {
            "metricName": "sessions"
        },
        "desc": True
    }],
    "limit": 50
}

sources = ga4_request(body_sources)

src_path = os.path.join(BASE_DIR, "ga4_sources.csv")
with open(src_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["channel", "medium", "source", "sessions", "conversions", "revenue"])
    for row in sources.get("rows", []):
        ch = row["dimensionValues"][0]["value"]
        md = row["dimensionValues"][1]["value"]
        so = row["dimensionValues"][2]["value"]
        s = row["metricValues"][0]["value"]
        c = row["metricValues"][1]["value"]
        r = row["metricValues"][2]["value"]
        w.writerow([ch, md, so, s, c, r])

print(f"🌐 Generated: {src_path}")
print("🔥 GA4 export completed.")
