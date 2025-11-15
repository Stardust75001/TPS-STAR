#!/usr/bin/env python3
import os
import pandas as pd
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

PROPERTY_ID = os.environ.get("GA4_PROPERTY_ID")
CLIENT_ID = os.environ.get("GA4_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GA4_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("GA4_REFRESH_TOKEN")

OUT_METRICS = "report_data/ga4_metrics.csv"
OUT_TS = "report_data/ga4_timeseries.csv"
OUT_SRC = "report_data/ga4_sources.csv"

def get_service():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/analytics.readonly"]
    )
    return build("analyticsdata", "v1beta", credentials=creds)

def run_report(service, start, end, dims, metrics):
    return service.properties().runReport(
        property=f"properties/{PROPERTY_ID}",
        body={
            "dateRanges": [{"startDate": start, "endDate": end}],
            "dimensions": [{"name": d} for d in dims],
            "metrics": [{"name": m} for m in metrics],
        }
    ).execute()

def main():
    service = get_service()

    # --- 7j KPIs
    r = run_report(service, "7daysAgo", "today",
                   dims=[],
                   metrics=["sessions", "conversions", "purchaseRevenue"])
    totals = r["rows"][0]["metricValues"]
    metrics_df = pd.DataFrame({
        "metric": ["Sessions (7d)", "Conversions (7d)", "Revenue (7d)"],
        "value": [float(totals[0]["value"]), float(totals[1]["value"]), float(totals[2]["value"])],
        "source": "ga4",
    })
    metrics_df.to_csv(OUT_METRICS, index=False)

    # --- 30j timeseries
    r = run_report(service, "30daysAgo", "today",
                   dims=["date"],
                   metrics=["purchaseRevenue"])
    rows = []
    for row in r.get("rows", []):
        rows.append({"date": row["dimensionValues"][0]["value"],
                     "revenue": float(row["metricValues"][0]["value"])})
    pd.DataFrame(rows).to_csv(OUT_TS, index=False)

    # --- Channels
    r = run_report(service, "7daysAgo", "today",
                   dims=["sessionDefaultChannelGroup"],
                   metrics=["sessions", "conversions", "purchaseRevenue"])
    out = []
    for row in r.get("rows", []):
        out.append({
            "channel": row["dimensionValues"][0]["value"],
            "sessions": float(row["metricValues"][0]["value"]),
            "conversions": float(row["metricValues"][1]["value"]),
            "revenue": float(row["metricValues"][2]["value"]),
        })
    pd.DataFrame(out).to_csv(OUT_SRC, index=False)

    print("✅ GA4 export OK")

if __name__ == "__main__":
    main()
