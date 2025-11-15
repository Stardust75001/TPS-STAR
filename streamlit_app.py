#!/usr/bin/env python3
"""
streamlit_app.py — TPS Business Dashboard

Usage:
  streamlit run streamlit_app.py
"""

import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TPS — Business Dashboard",
    layout="wide",
)

DATA_DIR = "report_data"


def load_csv(name):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)


shopify_metrics = load_csv("shopify_metrics.csv")
shopify_ts = load_csv("shopify_timeseries.csv")
ga4_metrics = load_csv("ga4_metrics.csv")
ga4_ts = load_csv("ga4_timeseries.csv")
ga4_sources = load_csv("ga4_sources.csv")

st.title("🐾 THE PET SOCIETY — Business Dashboard")

st.markdown("Vue synthétique des KPIs Shopify + GA4 sur les 7 derniers jours.")

# ---------------- KPIs ROW ----------------
col1, col2, col3, col4 = st.columns(4)

def get_metric(df, name):
    if df is None:
        return None
    row = df[df["metric"] == name]
    if row.empty:
        return None
    try:
        return float(row["value"].iloc[0])
    except Exception:
        return row["value"].iloc[0]

with col1:
    rev = get_metric(shopify_metrics, "Revenue (7d)")
    st.metric("Revenus Shopify (7j)", f"{rev:,.0f} €" if rev is not None else "—")

with col2:
    conv = get_metric(shopify_metrics, "Conversions (7d)")
    st.metric("Conversions Shopify (7j)", f"{conv:,.0f}" if conv is not None else "—")

with col3:
    aov = get_metric(shopify_metrics, "AOV (7d)")
    st.metric("Panier moyen Shopify", f"{aov:,.2f} €" if aov is not None else "—")

with col4:
    sess = get_metric(ga4_metrics, "Sessions (7d)")
    st.metric("Sessions GA4 (7j)", f"{sess:,.0f}" if sess is not None else "—")

st.markdown("---")

# ---------------- REVENUE TIMESERIES ----------------
st.subheader("Revenus quotidiens (Shopify vs GA4)")

if shopify_ts is not None and ga4_ts is not None:
    st_ts = shopify_ts.copy()
    ga_ts = ga4_ts.copy()
    st_ts["date"] = pd.to_datetime(st_ts["date"])
    ga_ts["date"] = pd.to_datetime(ga_ts["date"])

    merged = pd.merge(
        st_ts[["date", "revenue"]],
        ga_ts[["date", "revenue"]],
        on="date",
        how="outer",
        suffixes=("_shopify", "_ga4"),
    ).sort_values("date")

    merged.set_index("date", inplace=True)
    st.line_chart(merged)
else:
    st.info("Timeseries non disponible (CSV manquants).")

st.markdown("---")

# ---------------- ACQUISITION ----------------
st.subheader("Top canaux d'acquisition (GA4)")

if ga4_sources is not None and not ga4_sources.empty:
    df = ga4_sources.copy()
    df["sessions"] = pd.to_numeric(df["sessions"], errors="coerce")
    df["conversions"] = pd.to_numeric(df["conversions"], errors="coerce")
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

    top = df.groupby("channel", as_index=False)[["sessions", "conversions", "revenue"]].sum()
    top = top.sort_values("sessions", ascending=False).head(10)

    c1, c2 = st.columns(2)
    with c1:
        st.bar_chart(top.set_index("channel")["sessions"])
    with c2:
        st.bar_chart(top.set_index("channel")["revenue"])
else:
    st.info("Données GA4 sources non disponibles.")

st.markdown("---")
st.caption("Dashboard alimenté automatiquement par le workflow Weekly Business Report.")
