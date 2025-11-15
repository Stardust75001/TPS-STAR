import sys
import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen.canvas import Canvas

# ---------------------------------------------------
# Entrées
# ---------------------------------------------------
csv_input = sys.argv[1]       # metrics_report.csv
pdf_output = sys.argv[2]      # ex: TPS-Executive-Business-Report.pdf

df_health = pd.read_csv(csv_input)

# ---------------------------------------------------
# Styles & couleurs TPS
# ---------------------------------------------------
TAUPE = colors.HexColor("#BA986E")
BLACK = colors.HexColor("#1A1A1A")
WHITE = colors.white

styles = getSampleStyleSheet()
title_style = styles["Title"]
subtitle_style = styles["Heading2"]
text_style = styles["BodyText"]

# Footer avec n° page + date
def footer(canvas: Canvas, doc):
    page_num = canvas.getPageNumber()
    footer_text = f"Page {page_num} — Rapport généré le {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(570, 20, footer_text)

# Document PDF
doc = SimpleDocTemplate(
    pdf_output,
    pagesize=A4,
    title="TPS Executive Business Report",
    author="The Pet Society Paris",
)

elements = []

# ---------------------------------------------------
# Helpers
# ---------------------------------------------------
def section(title: str):
    """Ajoute un titre de section + espace."""
    elements.append(Paragraph(f"<b>{title}</b>", title_style))
    elements.append(Spacer(1, 12))

def load_optional_metrics_csv(filename: str):
    """Charge un CSV optionnel de type metric/value. Retourne dict(metric -> value) ou dict vide."""
    if not os.path.exists(filename):
        return {}
    try:
        df = pd.read_csv(filename)
        # On tolère "metric" ou "Metric"
        metric_col = "metric" if "metric" in df.columns else ("Metric" if "Metric" in df.columns else None)
        value_col = "value" if "value" in df.columns else ("Value" if "Value" in df.columns else None)
        if not metric_col or not value_col:
            return {}
        return dict(zip(df[metric_col], df[value_col]))
    except Exception:
        return {}

def build_kpi_table(rows):
    """Construit un tableau simple KPI à deux colonnes."""
    table = Table(rows, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), TAUPE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("GRID", (0,0), (-1,-1), 0.5, BLACK),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    return table

def generate_health_chart(df):
    """Génère un petit bar chart sur la santé des services (OK / INVALID / MISSING etc.)."""
    if df.empty or "Status" not in df.columns:
        return None
    counts = df["Status"].value_counts()
    labels = list(counts.index)
    values = list(counts.values)

    plt.figure(figsize=(5, 3))
    plt.bar(labels, values, color="#BA986E")
    plt.title("Répartition des statuts des services")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    chart_path = "temp_health_chart.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path

# ---------------------------------------------------
# Chargement des CSV métier optionnels (étapes futures)
# ---------------------------------------------------
shopify_metrics = load_optional_metrics_csv(os.path.join(os.path.dirname(csv_input), "shopify_metrics.csv"))
ga4_metrics     = load_optional_metrics_csv(os.path.join(os.path.dirname(csv_input), "ga4_metrics.csv"))
meta_metrics    = load_optional_metrics_csv(os.path.join(os.path.dirname(csv_input), "meta_metrics.csv"))
gsc_metrics     = load_optional_metrics_csv(os.path.join(os.path.dirname(csv_input), "gsc_metrics.csv"))
ahrefs_metrics  = load_optional_metrics_csv(os.path.join(os.path.dirname(csv_input), "ahrefs_metrics.csv"))
social_metrics  = load_optional_metrics_csv(os.path.join(os.path.dirname(csv_input), "social_metrics.csv"))

# ---------------------------------------------------
# PAGE 1+ : EXECUTIVE SUMMARY
# ---------------------------------------------------
section("📌 Executive Summary")

# Calcul TPS Health Score (basé sur metrics_report.csv)
ok_count = (df_health["Status"] == "OK").sum()
total = len(df_health)
score = int((ok_count / total) * 100) if total > 0 else 0

elements.append(Paragraph(
    f"<b>TPS Health Score global :</b> {score} / 100",
    subtitle_style
))
elements.append(Spacer(1, 8))

elements.append(Paragraph(
    f"<b>Services OK :</b> {ok_count} / {total}",
    text_style
))
elements.append(Spacer(1, 8))

# Si on a quelques données métier déjà branchées, on les met ici en résumé
summary_lines = []

if "Conversions (7d)" in shopify_metrics:
    summary_lines.append(f"• Conversions Shopify (7j) : {shopify_metrics['Conversions (7d)']}")
if "Revenue (7d)" in shopify_metrics:
    summary_lines.append(f"• Chiffre d'affaires (7j) : {shopify_metrics['Revenue (7d)']}")
if "AOV (7d)" in shopify_metrics:
    summary_lines.append(f"• Panier moyen (7j) : {shopify_metrics['AOV (7d)']}")

if "Sessions (7d)" in ga4_metrics:
    summary_lines.append(f"• Sessions GA4 (7j) : {ga4_metrics['Sessions (7d)']}")
if "ConvRate (7d)" in ga4_metrics:
    summary_lines.append(f"• Taux de conversion Analytics (7j) : {ga4_metrics['ConvRate (7d)']}")

if "ROAS (7d)" in meta_metrics:
    summary_lines.append(f"• ROAS Meta Ads (7j) : {meta_metrics['ROAS (7d)']}")

if not summary_lines:
    summary_text = "Données business détaillées non encore branchées (Shopify / GA4 / Meta). Le rapport utilise pour l’instant principalement l’état des intégrations techniques."
else:
    summary_text = "<br/>".join(summary_lines)

elements.append(Paragraph(summary_text, text_style))
elements.append(Spacer(1, 12))

# Graphique de répartition des statuts (OK/INVALID/MISSING…)
chart_path = generate_health_chart(df_health)
if chart_path and os.path.exists(chart_path):
    elements.append(Spacer(1, 12))
    elements.append(Image(chart_path, width=400, height=240))

# Fin Executive Summary → nouvelle section sur nouvelle page
elements.append(PageBreak())

# ---------------------------------------------------
# SECTION BUSINESS — PAGE SUIVANTE
# ---------------------------------------------------
section("📈 Business Revenue")

# Construire un bloc KPI Business
business_rows = [["KPI", "Valeur"]]

# Shopify
business_rows.append(["Conversions Shopify (7j)", shopify_metrics.get("Conversions (7d)", "N/A")])
business_rows.append(["Chiffre d'affaires (7j)", shopify_metrics.get("Revenue (7d)", "N/A")])
business_rows.append(["Panier moyen (7j)", shopify_metrics.get("AOV (7d)", "N/A")])

# GA4
business_rows.append(["Sessions (7j)", ga4_metrics.get("Sessions (7d)", "N/A")])
business_rows.append(["Taux conversion Analytics (7j)", ga4_metrics.get("ConvRate (7d)", "N/A")])

# Meta
business_rows.append(["ROAS Meta (7j)", meta_metrics.get("ROAS (7d)", "N/A")])
business_rows.append(["Budget Meta (7j)", meta_metrics.get("Spend (7d)", "N/A")])

business_table = build_kpi_table(business_rows)
elements.append(business_table)
elements.append(PageBreak())

# ---------------------------------------------------
# SECTION TECH STABILITY / OPS — PAGE SUIVANTE
# ---------------------------------------------------
section("🛠 Tech Stability / Ops")

elements.append(Paragraph(
    "Vue d’ensemble de la santé des intégrations (Cloudflare, Meta, Sentry, GA4, Ahrefs, GTM, Zik, GSC, Slack, SMTP, Shopify, Amplitude…).",
    text_style
))
elements.append(Spacer(1, 8))

# Tableau complet de metrics_report.csv
health_rows = [list(df_health.columns)] + df_health.values.tolist()
health_table = Table(health_rows, hAlign="LEFT")
health_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), TAUPE),
    ("TEXTCOLOR", (0,0), (-1,0), WHITE),
    ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 8),
    ("GRID", (0,0), (-1,-1), 0.25, BLACK),
    ("ALIGN", (0,0), (-1,-1), "LEFT"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
elements.append(health_table)
elements.append(PageBreak())

# ---------------------------------------------------
# SECTION MARKETING / SEO — PAGE SUIVANTE
# ---------------------------------------------------
section("👁️ Marketing / SEO")

seo_rows = [["KPI", "Valeur"]]

# GSC
seo_rows.append(["Clics SEO (7j)", gsc_metrics.get("Clicks (7d)", "N/A")])
seo_rows.append(["Impressions SEO (7j)", gsc_metrics.get("Impressions (7d)", "N/A")])
seo_rows.append(["Pages indexées", gsc_metrics.get("Valid Pages", "N/A")])

# Ahrefs
seo_rows.append(["Domain Rating", ahrefs_metrics.get("Domain Rating", "N/A")])
seo_rows.append(["Backlinks", ahrefs_metrics.get("Backlinks", "N/A")])

# Social
seo_rows.append(["Instagram Engagement (7j)", social_metrics.get("Instagram Engagement (7d)", "N/A")])
seo_rows.append(["TikTok Views (7j)", social_metrics.get("TikTok Views (7d)", "N/A")])

seo_table = build_kpi_table(seo_rows)
elements.append(seo_table)
elements.append(PageBreak())

# ---------------------------------------------------
# SECTION DATA & MONITORING — PAGE SUIVANTE
# ---------------------------------------------------
section("🧩 Data Quality & Monitoring")

dq_rows = [
    ["Indicateur", "Statut / Commentaire"],
    ["Qualité tracking (GTM / GA4 / Pixel)", "À dériver des statuts GTM_ID, GA4_TOKEN, META_TOKEN, SHOPIFY_API_KEY, etc."],
    ["Exhaustivité métriques", "À préciser lorsque les CSV Shopify/GA4/Meta seront branchés."],
    ["Historique erreurs système", "À enrichir avec un log d’erreurs ou des stats supplémentaires."],
]

dq_table = build_kpi_table(dq_rows)
elements.append(dq_table)
elements.append(PageBreak())

# ---------------------------------------------------
# SECTION ANALYSE — PAGE SUIVANTE
# ---------------------------------------------------
section("🔍 Analyse Croisée (Business / Tech / SEO / Data)")

# Analyse simple basée sur le score et les statuts
analysis_lines = []

if score == 100:
    analysis_lines.append("• L’ensemble des services monitorés est actuellement opérationnel (100% OK).")
elif score >= 80:
    analysis_lines.append("• La majorité des services est opérationnelle. Quelques intégrations sont à surveiller.")
else:
    analysis_lines.append("• Plusieurs services clés présentent des anomalies. Il est recommandé de prioriser la remédiation.")

if "SHOPIFY_API_KEY" in df_health["Service"].values:
    shopify_status = df_health.loc[df_health["Service"] == "SHOPIFY_API_KEY", "Status"].iloc[0]
    if shopify_status != "OK":
        analysis_lines.append("• Shopify API Key n’est pas en statut OK → risque direct sur l’accès aux données business.")
if "GA4_TOKEN" in df_health["Service"].values:
    ga4_status = df_health.loc[df_health["Service"] == "GA4_TOKEN", "Status"].iloc[0]
    if ga4_status != "OK":
        analysis_lines.append("• GA4 Token invalide ou manquant → les analyses Analytics ne seront pas complètes.")
if "META_TOKEN" in df_health["Service"].values:
    meta_status = df_health.loc[df_health["Service"] == "META_TOKEN", "Status"].iloc[0]
    if meta_status != "OK":
        analysis_lines.append("• Meta Token à corriger → impact sur Meta Ads & Pixel Debugging.")
if "GSC_CREDENTIALS" in df_health["Service"].values:
    gsc_status = df_health.loc[df_health["Service"] == "GSC_CREDENTIALS", "Status"].iloc[0]
    if gsc_status != "OK":
        analysis_lines.append("• GSC Credentials non valides → pas de vision SEO Search Console fiable.")

if not analysis_lines:
    analysis_lines.append("• Les données actuelles ne permettent pas encore une analyse détaillée des KPI business. Brancher Shopify / GA4 / Meta pour enrichir ce rapport.")

analysis_text = "<br/>".join(analysis_lines)
elements.append(Paragraph(analysis_text, text_style))
elements.append(PageBreak())

# ---------------------------------------------------
# SECTION RECOMMANDATIONS — PAGE SUIVANTE
# ---------------------------------------------------
section("⭐ Recommandations Actionnables")

recos = """
<b>À 48 heures :</b><br/>
• Vérifier et corriger les secrets en statut MISSING / INVALID (Shopify, GA4, Meta, GSC, Slack, SMTP…).<br/>
• S’assurer que GTM, GA4 et Pixel Meta remontent correctement les évènements clés (page_view, view_item, add_to_cart, purchase).<br/><br/>

<b>À 7 jours :</b><br/>
• Brancher les exports automatisés Shopify (commandes, CA, AOV) dans un CSV <i>shopify_metrics.csv</i> utilisé par ce rapport.<br/>
• Brancher un rapport GA4 (sessions, conv rate, sources) dans <i>ga4_metrics.csv</i>.<br/>
• Brancher un résumé Meta Ads (ROAS, spend, CPA) dans <i>meta_metrics.csv</i>.<br/><br/>

<b>À 30 jours :</b><br/>
• Mettre en place un dashboard interactif (Streamlit / Notion / Data Studio) alimenté par les mêmes sources que ce rapport PDF.<br/>
• Historiser les rapports (journalier / hebdo) pour suivre les tendances et anticiper les risques.<br/>
• Ajouter des alertes Slack dès qu’un service clé passe en statut INVALID / MISSING.<br/>
"""
elements.append(Paragraph(recos, text_style))
elements.append(PageBreak())

# ---------------------------------------------------
# SECTION ANNEXE — PAGE SUIVANTE
# ---------------------------------------------------
section("📎 Annexe — Données brutes des services")

annex_rows = [list(df_health.columns)] + df_health.values.tolist()
annex_table = Table(annex_rows, hAlign="LEFT")
annex_table.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 7),
    ("GRID", (0,0), (-1,-1), 0.25, BLACK),
    ("ALIGN", (0,0), (-1,-1), "LEFT"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
elements.append(annex_table)

# ---------------------------------------------------
# Génération du PDF
# ---------------------------------------------------
doc.build(elements, onFirstPage=footer, onLaterPages=footer)
