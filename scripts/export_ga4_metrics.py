#!/usr/bin/env python3
import os
import sys
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension

def fetch_ga4_kpis():
    """Fetch simple GA4 KPIs with safe handling when GA4 returns no rows."""

    property_id = os.getenv("GA4_PROPERTY_ID")
    refresh_token = os.getenv("GA4_REFRESH_TOKEN")
    client_id = os.getenv("GA4_CLIENT_ID")
    client_secret = os.getenv("GA4_CLIENT_SECRET")

    if not (property_id and refresh_token and client_id and client_secret):
        print("❌ Missing GA4 environment variables.")
        sys.exit(1)

    # OAuth credentials
    from google.oauth2.credentials import Credentials
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
    )

    client = BetaAnalyticsDataClient(credentials=creds)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="newUsers"),
            Metric(name="sessions"),
        ],
        dimensions=[Dimension(name="date")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
    )

    print("📡 GA4 → sending request…")
    response = client.run_report(request)

    # DEBUG
    print("📡 GA4 RESPONSE ROWS =", len(response.rows))

    # ---- FIX ICI ----
    if len(response.rows) == 0:
        print("⚠️ GA4 → aucune donnée reçue (0 rows).")
        print("⚠️ Génération d’un CSV neutre.")
        return pd.DataFrame([{
            "activeUsers": 0,
            "newUsers": 0,
            "sessions": 0
        }])

    # extraction normale
    first = response.rows[0].metric_values
    return pd.DataFrame([{
        "activeUsers": int(first[0].value),
        "newUsers": int(first[1].value),
        "sessions": int(first[2].value)
    }])


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: export_ga4_metrics.py --outdir DIR")
        sys.exit(0)

    if "--outdir" not in sys.argv:
        print("❌ Missing --outdir argument.")
        sys.exit(1)

    outdir = sys.argv[sys.argv.index("--outdir") + 1]
    os.makedirs(outdir, exist_ok=True)

    df = fetch_ga4_kpis()

    outfile = f"{outdir}/ga4_metrics.csv"
    df.to_csv(outfile, index=False)
    print(f"✅ GA4 metrics exported → {outfile}")


if __name__ == "__main__":
    main()
