import os
import pandas as pd
import streamlit as st

BASE_DIR = "report_data"

def load_kv(name):
    path = os.path.join(BASE_DIR, name)
    if not os.path.exists(path):
        return {}
    df = pd.read_csv(path)
    if "metric" in df.columns and "value" in df.columns:
        return dict(zip(df["metric"], df["value"]))
    if "Metric" in df.columns and "Value" in df.columns:
        return dict(zip(df["Metric"], df["Value"]))
    return {}

def main():
    st.set_page_config(page_title="TPS Business Dashboard", layout="wide")

    st.title("🐾 THE PET SOCIETY — Business & Tech Dashboard")
    st.caption("Basé sur les mêmes CSV que le rapport PDF exécutif.")

    health_path = os.path.join(BASE_DIR, "metrics_report.csv")
    if os.path.exists(health_path):
        df_health = pd.read_csv(health_path)
    else:
        df_health = pd.DataFrame()

    shopify = load_kv("shopify_metrics.csv")
    ga4 = load_kv("ga4_metrics.csv")
    meta = load_kv("meta_metrics.csv")
    gsc = load_kv("gsc_metrics.csv")
    social = load_kv("social_metrics.csv")

    # Ligne KPI principale
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("CA Shopify (7j)", shopify.get("Revenue (7d)", "N/A"))
    with c2:
        st.metric("Conversions (7j)", shopify.get("Conversions (7d)", "N/A"))
    with c3:
        st.metric("Sessions GA4 (7j)", ga4.get("Sessions (7d)", "N/A"))
    with c4:
        st.metric("ROAS Meta (7j)", meta.get("ROAS (7d)", "N/A"))

    st.markdown("---")

    colA, colB = st.columns(2)

    with colA:
        st.subheader("Santé des services")
        if not df_health.empty:
            st.dataframe(df_health)
            st.bar_chart(df_health["Status"].value_counts())
        else:
            st.info("metrics_report.csv introuvable ou vide.")

    with colB:
        st.subheader("SEO & Social")
        st.write("SEO (GSC)")
        st.json(gsc)
        st.write("Social")
        st.json(social)

    st.markdown("---")
    st.subheader("Brut : Shopify / GA4 / Meta")
    st.write("Shopify")
    st.json(shopify)
    st.write("GA4")
    st.json(ga4)
    st.write("Meta")
    st.json(meta)

if __name__ == "__main__":
    main()
