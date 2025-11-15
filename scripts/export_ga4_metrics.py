#!/usr/bin/env python3
"""
export_ga4_metrics.py

Usage:
  python export_ga4_metrics.py ga4_metrics.csv ga4_timeseries.csv ga4_sources.csv

Sortie 1 (résumé 7j) : ga4_metrics.csv
  metric,value
  Revenue (7d),1234.50
  Sessions (7d),987
  Conversions (7d),42

Sortie 2 (timeseries) : ga4_timeseries.csv
  date,revenue,sessions,conversions

Sortie 3 (sources) : ga4_sources.csv
  channel,sessions,conversions,revenue
"""

import os
import sys
import csv
from typing import List, Dict

import requests


def get_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise SystemExit(f"❌ Missing env var: {name}")
    return val


def get_access_token() -> str:
    """Rafraîchit un access token à partir du refresh token."""
    refresh_token = get_env("GA4_REFRESH_TOKEN")
    client_id = get_env("GA4_CLIENT_ID")
    client_secret = get_env("GA4_CLIENT_SECRET")

    resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    if resp.status_code != 200:
        raise SystemExit(f"❌ OAuth token error {resp.status_code}: {resp.text}")

    access_token = resp.json().get("access_token")
    if not access_token:
        raise SystemExit("❌ No access_token in OAuth response")
    return access_token


def run_report(property_id: str, body: Dict) -> Dict:
    token = get_access_token()
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(url, json=body, headers=headers)
    if resp.status_code != 200:
        raise SystemExit(f"❌ GA4 API error {resp.status_code}: {resp.text}")
    return resp.json()


def rows_to_dicts(resp: Dict, dims: List[str], mets: List[str]) -> List[Dict]:
    out = []
    for row in resp.get("rows", []):
        dvals = [d.get("value") for d in row.get("dimensionValues", [])]
        mvals = [m.get("value") for m in row.get("metricValues", [])]
        entry = {dims[i]: dvals[i] for i in range(len(dims))}
        for i, m in enumerate(mets):
            entry[m] = float(mvals[i]) if mvals[i] not in (None, "") else 0.0
        out.append(entry)
    return out


def export_ga4(property_id: str, summary_path: str, ts_path: str, sources_path: str):
    # --- 1) Timeseries (date)
    body_ts = {
        "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "date"}],
        "metrics": [
            {"name": "totalRevenue"},
            {"name": "sessions"},
            {"name": "conversions"},
        ],
    }
    resp_ts = run_report(property_id, body_ts)
    ts_rows = rows_to_dicts(resp_ts, ["date"], ["totalRevenue", "sessions", "conversions"])

    # --- 2) Channels
    body_channels = {
        "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "sessionDefaultChannelGroup"}],
        "metrics": [
            {"name": "sessions"},
            {"name": "conversions"},
            {"name": "totalRevenue"},
        ],
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
    }
    resp_ch = run_report(property_id, body_channels)
    ch_rows = rows_to_dicts(
        resp_ch,
        ["sessionDefaultChannelGroup"],
        ["sessions", "conversions", "totalRevenue"],
    )

    # --- 3) Résumé 7 jours – on somme la timeseries
    total_rev = sum(r["totalRevenue"] for r in ts_rows)
    total_sessions = sum(r["sessions"] for r in ts_rows)
    total_conv = sum(r["conversions"] for r in ts_rows)

    # --- Write summary
    with open(summary_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        w.writerow(["Revenue (7d)", f"{total_rev:.2f}"])
        w.writerow(["Sessions (7d)", int(total_sessions)])
        w.writerow(["Conversions (7d)", int(total_conv)])

    # --- Write timeseries
    with open(ts_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "revenue", "sessions", "conversions"])
        for r in ts_rows:
            # GA4 date -> YYYYMMDD
            d = r["date"]
            date_iso = f"{d[0:4]}-{d[4:6]}-{d[6:8]}"
            w.writerow([
                date_iso,
                f"{r['totalRevenue']:.2f}",
                int(r["sessions"]),
                int(r["conversions"]),
            ])

    # --- Write channels
    with open(sources_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["channel", "sessions", "conversions", "revenue"])
        for r in ch_rows:
            w.writerow([
                r["sessionDefaultChannelGroup"],
                int(r["sessions"]),
                int(r["conversions"]),
                f"{r['totalRevenue']:.2f}",
            ])

    print(f"✅ GA4 summary     -> {summary_path}")
    print(f"✅ GA4 timeseries  -> {ts_path}")
    print(f"✅ GA4 sources     -> {sources_path}")


def main():
    if len(sys.argv) != 4:
        print("Usage: export_ga4_metrics.py ga4_metrics.csv ga4_timeseries.csv ga4_sources.csv")
        raise SystemExit(1)

    summary_path = sys.argv[1]
    ts_path = sys.argv[2]
    sources_path = sys.argv[3]
    prop_id = get_env("GA4_PROPERTY_ID")

    export_ga4(prop_id, summary_path, ts_path, sources_path)


if __name__ == "__main__":
    main()
