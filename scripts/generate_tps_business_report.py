# ============================================================
#  TPS Executive Business Report
#  - Mode "full"      : rapport complet multi-pages
#  - Mode "executive" : one-page résumé
#
#  Usage :
#    python3 scripts/generate_tps_business_report.py \
#        report_data/metrics_report.csv \
#        TPS-Executive-Business-Report.pdf \
#        full
#
#    python3 scripts/generate_tps_business_report.py \
#        report_data/metrics_report.csv \
#        TPS-Executive-OnePager.pdf \
#        executive
# ============================================================

import sys
import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ------------------------------------------------------------
# Entrées CLI
# ------------------------------------------------------------
if len(sys.argv) < 3:
    print("Usage: generate_tps_business_report.py <metrics_report.csv> <output.pdf> [full|executive]")
    sys.exit(1)

csv_input = sys.argv[1]          # ex: report_data/metrics_report.csv
pdf_output = sys.argv[2]         # ex: TPS-Executive-Business-Report.pdf
mode = sys.argv[3] if len(sys.argv) > 3 else "full"
mode = mode.lower()

# ------------------------------------------------------------
# Palette consulting (dégradé bleu / gris)
# ------------------------------------------------------------
BLUE_DEEP = colors.HexColor("#1F3B73")
BLUE_GREY = colors.HexColor("#4A5F78")
GREY_LIGHT = colors.HexColor("#E8ECF1")
BLACK = colors.HexColor("#1A1A1A")
WHITE = colors.white

# ------------------------------------------------------------
# Logo TPS
# ------------------------------------------------------------
LOGO_URL = (
    "https://cdn.shopify.com/s/files/1/0861/3180/2460/files/"
    "LOGO_ARRONDI_NT12052025_-_1200x628.jpg-removebg-preview.png?v=1747069835"
)
LOGO_FILENAME = "tps_logo.png"


# ============================================================
#  A. Fonts & Styles
# ============================================================

def register_fonts():
    """
    Essaie SF Pro Rounded si dispo localement, sinon Helvetica.
    Dépose éventuellement tes fichiers dans ./fonts et adapte.
    """
    global FONT_BODY, FONT_BODY_BOLD
    FONT_BODY = "Helvetica"
    FONT_BODY_BOLD = "Helvetica-Bold"

    # Exemple si tu ajoutes SF Pro Rounded :
    # try:
    #     pdfmetrics.registerFont(TTFont("SFProRounded", "fonts/SF-Pro-Rounded-Regular.ttf"))
    #     pdfmetrics.registerFont(TTFont("SFProRounded-Bold", "fonts/SF-Pro-Rounded-Bold.ttf"))
    #     FONT_BODY = "SFProRounded"
    #     FONT_BODY_BOLD = "SFProRounded-Bold"
    # except Exception:
    #     pass


register_fonts()
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TPS-Title",
    parent=styles["Title"],
    fontName=FONT_BODY_BOLD,
    fontSize=14,
    textColor=BLUE_DEEP,
    alignment=1,  # CENTER
    spaceAfter=12,
)

subtitle_style = ParagraphStyle(
    "TPS-Subtitle",
    parent=styles["Heading2"],
    fontName=FONT_BODY_BOLD,
    fontSize=12,
    textColor=BLUE_GREY,
    spaceAfter=8,
)

text_style = ParagraphStyle(
    "TPS-Body",
    parent=styles["BodyText"],
    fontName=FONT_BODY,
    fontSize=11,
    textColor=BLACK,
    leading=14,
)


# ============================================================
#  B. Helpers génériques
# ============================================================

def footer(canvas: Canvas, doc):
    """Footer : numéro de page + date UTC."""
    page_num = canvas.getPageNumber()
    footer_text = (
        f"Page {page_num} • Rapport généré le "
        f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    )
    canvas.setFont(FONT_BODY, 8)
    canvas.setFillColor(BLUE_GREY)
    canvas.drawRightString(A4[0] - 30, 20, footer_text)


def ensure_logo_local():
    """Télécharge le logo si besoin et renvoie le chemin local."""
    if os.path.exists(LOGO_FILENAME):
        return LOGO_FILENAME
    try:
        import urllib.request
        urllib.request.urlretrieve(LOGO_URL, LOGO_FILENAME)
        return LOGO_FILENAME
    except Exception:
        return None


def section_title(text: str):
    """Titre de section standard."""
    return [
        Paragraph(f"<b>{text}</b>", title_style),
        Spacer(1, 12),
    ]


def build_kpi_table(rows, header_bg=BLUE_DEEP):
    """Tableau KPI centré 2 colonnes."""
    table = Table(rows, hAlign="CENTER")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BODY_BOLD),
        ("FONTNAME", (0, 1), (-1, -1), FONT_BODY),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.3, BLUE_GREY),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.whitesmoke, GREY_LIGHT]),
    ]))
    return table


def generate_health_chart(df, output_path="temp_health_chart.png"):
    """Bar chart de la répartition des statuts et retour du chemin image."""
    if df.empty or "Status" not in df.columns:
        return None
    counts = df["Status"].value_counts()
    labels = list(counts.index)
    values = list(counts.values)

    plt.figure(figsize=(5, 3))
    bars = plt.bar(labels, values, color="#1F3B73")

    for bar in bars:
        h = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            h,
            str(h),
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.title("Répartition des statuts des services", fontsize=11)
    plt.xticks(rotation=30, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path


def load_optional_metrics_csv(filename: str):
    """Charge un CSV metric/value → dict, ou {} si non dispo."""
    if not os.path.exists(filename):
        return {}
    try:
        df = pd.read_csv(filename)
        metric_col = None
        value_col = None
        for c in df.columns:
            if c.lower() == "metric":
                metric_col = c
            if c.lower() == "value":
                value_col = c
        if not metric_col or not value_col:
            return {}
        return dict(zip(df[metric_col], df[value_col]))
    except Exception:
        return {}


def generate_timeseries_chart(csv_path, metric_col, title, output_path):
    """
    Génère un line chart simple à partir d'un CSV time-series :
    colonnes attendues : date, <metric_col>
    """
    if not os.path.exists(csv_path):
        return None
    try:
        df = pd.read_csv(csv_path)
        if "date" not in df.columns or metric_col not in df.columns:
            return None
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        plt.figure(figsize=(5.5, 3))
        plt.plot(df["date"], df[metric_col], marker="o", linewidth=1.8, color="#1F3B73")
        plt.title(title, fontsize=11)
        plt.xticks(rotation=30, ha="right", fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
        return output_path
    except Exception:
        return None


# ============================================================
#  C. Chargement des données
# ============================================================

df_health = pd.read_csv(csv_input)
base_dir = os.path.dirname(csv_input)

shopify_metrics = load_optional_metrics_csv(os.path.join(base_dir, "shopify_metrics.csv"))
ga4_metrics = load_optional_metrics_csv(os.path.join(base_dir, "ga4_metrics.csv"))
meta_metrics = load_optional_metrics_csv(os.path.join(base_dir, "meta_metrics.csv"))
gsc_metrics = load_optional_metrics_csv(os.path.join(base_dir, "gsc_metrics.csv"))
ahrefs_metrics = load_optional_metrics_csv(os.path.join(base_dir, "ahrefs_metrics.csv"))
social_metrics = load_optional_metrics_csv(os.path.join(base_dir, "social_metrics.csv"))

# timeseries optionnelles pour graphes business
shopify_ts = os.path.join(base_dir, "shopify_timeseries.csv")
ga4_ts = os.path.join(base_dir, "ga4_timeseries.csv")
meta_ts = os.path.join(base_dir, "meta_timeseries.csv")

ok_count = (df_health["Status"] == "OK").sum()
total = len(df_health)
score = int((ok_count / total) * 100) if total > 0 else 0

# ============================================================
#  D. Construction du document
# ============================================================

doc = SimpleDocTemplate(
    pdf_output,
    pagesize=A4,
    title="TPS Executive Business Report",
    author="The Pet Society Paris",
    leftMargin=36,
    rightMargin=36,
    topMargin=40,
    bottomMargin=40,
)

elements = []

# ------------------------------------------------------------
# Logo (pour tous les modes)
# ------------------------------------------------------------
logo_path = ensure_logo_local()
if logo_path:
    logo = Image(logo_path, width=180, height=90)
    logo.hAlign = "CENTER"
    elements.append(logo)
    elements.append(Spacer(1, 16))


# ============================================================
#  E. Mode EXECUTIVE (one-page)
# ============================================================
if mode == "executive":
    elements += section_title("📌 Executive One-Page Summary")

    # Score global
    elements.append(Paragraph(
        f"<b>TPS Health Score global :</b> {score} / 100",
        subtitle_style,
    ))
    elements.append(Spacer(1, 8))

    # Tableau KPI synthétique
    kpi_rows = [["KPI", "Valeur"]]

    # Shopify
    kpi_rows.append(["Conversions Shopify (7j)", shopify_metrics.get("Conversions (7d)", "N/A")])
    kpi_rows.append(["CA Shopify (7j)", shopify_metrics.get("Revenue (7d)", "N/A")])
    kpi_rows.append(["Panier moyen (7j)", shopify_metrics.get("AOV (7d)", "N/A")])

    # GA4
    kpi_rows.append(["Sessions (7j)", ga4_metrics.get("Sessions (7d)", "N/A")])
    kpi_rows.append(["Taux de conversion (7j)", ga4_metrics.get("ConvRate (7d)", "N/A")])

    # Meta
    kpi_rows.append(["ROAS Meta (7j)", meta_metrics.get("ROAS (7d)", "N/A")])
    kpi_rows.append(["Spend Meta (7j)", meta_metrics.get("Spend (7d)", "N/A")])

    # SEO
    kpi_rows.append(["Clics SEO (7j)", gsc_metrics.get("Clicks (7d)", "N/A")])
    kpi_rows.append(["Impressions SEO (7j)", gsc_metrics.get("Impressions (7d)", "N/A")])

    # Social
    kpi_rows.append(["Instagram Eng. (7j)", social_metrics.get("Instagram Engagement (7d)", "N/A")])
    kpi_rows.append(["TikTok Views (7j)", social_metrics.get("TikTok Views (7d)", "N/A")])

    kpi_table = build_kpi_table(kpi_rows)
    elements.append(kpi_table)
    elements.append(Spacer(1, 12))

    # Graph santé services (si dispo)
    chart_path = generate_health_chart(df_health, "temp_health_chart_exec.png")
    if chart_path and os.path.exists(chart_path):
        img = Image(chart_path, width=380, height=220)
        img.hAlign = "CENTER"
        elements.append(img)
        elements.append(Spacer(1, 12))

    # 3–5 points d'analyse rapide
    bullets = []
    if score == 100:
        bullets.append("• Tous les services critiques sont opérationnels. Maintenir la configuration actuelle.")
    elif score >= 80:
        bullets.append("• La majorité des services est OK. Quelques intégrations doivent être réalignées.")
    else:
        bullets.append("• Plusieurs services sont en anomalie : prioriser les secrets / API les plus critiques.")

    if "Revenue (7d)" in shopify_metrics:
        bullets.append(f"• CA 7j : {shopify_metrics['Revenue (7d)']} (à suivre vs semaine précédente).")
    if "ROAS (7d)" in meta_metrics:
        bullets.append(f"• ROAS Meta 7j : {meta_metrics['ROAS (7d)']} (optimiser les campagnes sous-performantes).")
    if "Sessions (7d)" in ga4_metrics and "ConvRate (7d)" in ga4_metrics:
        bullets.append(
            f"• {ga4_metrics['Sessions (7d)']} sessions / Taux de conversion {ga4_metrics['ConvRate (7d)']}."
        )

    analysis_text = "<br/>".join(bullets)
    elements.append(Paragraph(analysis_text, text_style))

    # Build
    doc.build(elements, onFirstPage=footer, onLaterPages=footer)
    sys.exit(0)


# ============================================================
#  F. Mode FULL (rapport complet)
# ============================================================

# Page 1 — Executive Summary
elements += section_title("📌 Executive Summary")

elements.append(Paragraph(
    f"<b>TPS Health Score global :</b> {score} / 100",
    subtitle_style,
))
elements.append(Spacer(1, 8))
elements.append(Paragraph(
    f"<b>Services OK :</b> {ok_count} / {total}",
    text_style,
))
elements.append(Spacer(1, 10))

summary_lines = []

if "Conversions (7d)" in shopify_metrics:
    summary_lines.append(f"• Conversions Shopify (7j) : {shopify_metrics['Conversions (7d)']}")
if "Revenue (7d)" in shopify_metrics:
    summary_lines.append(f"• CA Shopify (7j) : {shopify_metrics['Revenue (7d)']}")
if "AOV (7d)" in shopify_metrics:
    summary_lines.append(f"• Panier moyen (7j) : {shopify_metrics['AOV (7d)']}")
if "Sessions (7d)" in ga4_metrics:
    summary_lines.append(f"• Sessions GA4 (7j) : {ga4_metrics['Sessions (7d)']}")
if "ConvRate (7d)" in ga4_metrics:
    summary_lines.append(f"• Taux de conversion Analytics (7j) : {ga4_metrics['ConvRate (7d)']}")
if "ROAS (7d)" in meta_metrics:
    summary_lines.append(f"• ROAS Meta Ads (7j) : {meta_metrics['ROAS (7d)']}")

if not summary_lines:
    summary_text = (
        "Les données business (CA, conversions, ROAS, SEO) seront enrichies dès que "
        "les exports automatisés Shopify / GA4 / Meta seront branchés dans ce rapport."
    )
else:
    summary_text = "<br/>".join(summary_lines)

elements.append(Paragraph(summary_text, text_style))
elements.append(Spacer(1, 16))

chart_path = generate_health_chart(df_health, "temp_health_chart.png")
if chart_path and os.path.exists(chart_path):
    img = Image(chart_path, width=400, height=240)
    img.hAlign = "CENTER"
    elements.append(img)

elements.append(PageBreak())

# Page 2 — Business Revenue
elements += section_title("📈 Business Revenue")

business_rows = [["KPI", "Valeur"]]
business_rows.append(["Conversions Shopify (7j)", shopify_metrics.get("Conversions (7d)", "N/A")])
business_rows.append(["CA Shopify (7j)", shopify_metrics.get("Revenue (7d)", "N/A")])
business_rows.append(["Panier moyen (7j)", shopify_metrics.get("AOV (7d)", "N/A")])
business_rows.append(["Sessions (7j)", ga4_metrics.get("Sessions (7d)", "N/A")])
business_rows.append(["Taux conversion Analytics (7j)", ga4_metrics.get("ConvRate (7d)", "N/A")])
business_rows.append(["ROAS Meta (7j)", meta_metrics.get("ROAS (7d)", "N/A")])
business_rows.append(["Budget Meta (7j)", meta_metrics.get("Spend (7d)", "N/A")])

business_table = build_kpi_table(business_rows)
elements.append(business_table)
elements.append(PageBreak())

# Page 3 — Business Dashboards (si timeseries dispo)
ts_charts = []

c1 = generate_timeseries_chart(shopify_ts, "revenue", "CA Shopify - 7/14 jours", "temp_shopify_revenue.png")
if c1:
    ts_charts.append(("CA Shopify", c1))

c2 = generate_timeseries_chart(ga4_ts, "sessions", "Sessions GA4 - 7/14 jours", "temp_ga4_sessions.png")
if c2:
    ts_charts.append(("Sessions GA4", c2))

c3 = generate_timeseries_chart(meta_ts, "roas", "ROAS Meta Ads - 7/14 jours", "temp_meta_roas.png")
if c3:
    ts_charts.append(("ROAS Meta", c3))

if ts_charts:
    elements += section_title("📊 Business Dashboards (Vue temporelle)")
    for label, path in ts_charts:
        img = Image(path, width=420, height=260)
        img.hAlign = "CENTER"
        elements.append(img)
        elements.append(Spacer(1, 12))
    elements.append(PageBreak())

# Page 4 — Tech Stability / Ops
elements += section_title("🛠 Tech Stability / Ops")

elements.append(Paragraph(
    "Vue d’ensemble des intégrations techniques clés : Cloudflare, Meta, "
    "Sentry, GA4, Ahrefs, GTM, Zik, GSC, Slack, SMTP, Shopify, Amplitude…",
    text_style,
))
elements.append(Spacer(1, 10))

health_rows = [list(df_health.columns)] + df_health.values.tolist()
health_table = Table(health_rows, hAlign="CENTER")
health_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BLUE_DEEP),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("FONTNAME", (0, 0), (-1, 0), FONT_BODY_BOLD),
    ("FONTNAME", (0, 1), (-1, -1), FONT_BODY),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("GRID", (0, 0), (-1, -1), 0.25, BLUE_GREY),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
elements.append(health_table)
elements.append(PageBreak())

# Page 5 — Marketing & SEO
elements += section_title("👁️ Marketing & SEO")

seo_rows = [["KPI", "Valeur"]]
seo_rows.append(["Clics SEO (7j)", gsc_metrics.get("Clicks (7d)", "N/A")])
seo_rows.append(["Impressions SEO (7j)", gsc_metrics.get("Impressions (7d)", "N/A")])
seo_rows.append(["Pages indexées", gsc_metrics.get("Valid Pages", "N/A")])
seo_rows.append(["Domain Rating", ahrefs_metrics.get("Domain Rating", "N/A")])
seo_rows.append(["Backlinks", ahrefs_metrics.get("Backlinks", "N/A")])
seo_rows.append(["Instagram Engagement (7j)", social_metrics.get("Instagram Engagement (7d)", "N/A")])
seo_rows.append(["TikTok Views (7j)", social_metrics.get("TikTok Views (7d)", "N/A")])

seo_table = build_kpi_table(seo_rows, header_bg=BLUE_GREY)
elements.append(seo_table)
elements.append(PageBreak())

# Page 6 — Data Quality & Monitoring
elements += section_title("🧩 Data Quality & Monitoring")

dq_rows = [
    ["Indicateur", "Statut / Commentaire"],
    [
        "Qualité tracking (GTM / GA4 / Pixel)",
        "Synthèse à dériver des statuts GTM_ID, GA4_TOKEN, META_TOKEN, SHOPIFY_API_KEY, etc.",
    ],
    [
        "Exhaustivité métriques",
        "À préciser lorsque les CSV Shopify / GA4 / Meta seront branchés.",
    ],
    [
        "Historique erreurs système",
        "À enrichir avec Sentry / logs JS pour suivi des erreurs applicatives.",
    ],
]
dq_table = build_kpi_table(dq_rows, header_bg=BLUE_DEEP)
elements.append(dq_table)
elements.append(PageBreak())

# Page 7 — Analyse & Recommandations
elements += section_title("🔍 Analyse & Recommandations")

analysis_lines = []
if score == 100:
    analysis_lines.append("• Tous les services monitorés sont opérationnels (100% OK).")
elif score >= 80:
    analysis_lines.append("• La majorité des services est OK. Quelques intégrations restent à sécuriser.")
else:
    analysis_lines.append("• Plusieurs services critiques sont en anomalie. Prioriser secrets & APIs clés.")

def append_if_status_not_ok(service_key, label):
    if service_key in df_health["Service"].values:
        status = df_health.loc[df_health["Service"] == service_key, "Status"].iloc[0]
        if status != "OK":
            analysis_lines.append(f"• {label} : statut {status} → action requise.")

append_if_status_not_ok("SHOPIFY_API_KEY", "Shopify API (backend boutique)")
append_if_status_not_ok("GA4_TOKEN", "GA4 (mesure Analytics)")
append_if_status_not_ok("META_TOKEN", "Meta Ads / Pixel")
append_if_status_not_ok("GSC_CREDENTIALS", "Google Search Console")
append_if_status_not_ok("CLOUDFLARE_TOKEN", "Cloudflare (DNS / CDN)")

if not analysis_lines:
    analysis_lines.append(
        "• Les données actuelles ne permettent pas une analyse business détaillée. "
        "Brancher Shopify / GA4 / Meta / Ahrefs pour activer le plein potentiel du rapport."
    )

analysis_text = "<br/>".join(analysis_lines)
elements.append(Paragraph(analysis_text, text_style))
elements.append(Spacer(1, 16))

recos = """
<b>À 48 heures :</b><br/>
• Corriger les secrets/API en statut MISSING / INVALID (Shopify, GA4, Meta, GSC, Slack, SMTP…).<br/>
• Vérifier que GTM, GA4 et le Pixel Meta remontent les évènements clés (page_view, view_item, add_to_cart, purchase).<br/><br/>

<b>À 7 jours :</b><br/>
• Brancher les exports Shopify (CA, commandes, AOV) dans <i>shopify_metrics.csv</i> et <i>shopify_timeseries.csv</i>.<br/>
• Brancher les exports GA4 (sessions, conversions, sources) dans <i>ga4_metrics.csv</i> et <i>ga4_timeseries.csv</i>.<br/>
• Brancher les exports Meta Ads (ROAS, spend) dans <i>meta_metrics.csv</i> et <i>meta_timeseries.csv</i>.<br/><br/>

<b>À 30 jours :</b><br/>
• Mettre en place un dashboard interactif (Streamlit / Notion / Looker) alimenté par ces mêmes CSV.<br/>
• Historiser les rapports hebdo dans un dossier /reports et notifier #reports sur Slack.<br/>
• Ajouter des alertes Slack dès qu’un service passe en statut INVALID / MISSING.<br/>
"""
elements.append(Paragraph(recos, text_style))
elements.append(PageBreak())

# Page 8 — Annexe
elements += section_title("📎 Annexe — Données brutes des services")
annex_rows = [list(df_health.columns)] + df_health.values.tolist()
annex_table = Table(annex_rows, hAlign="CENTER")
annex_table.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), FONT_BODY),
    ("FONTSIZE", (0, 0), (-1, -1), 7),
    ("GRID", (0, 0), (-1, -1), 0.25, BLUE_GREY),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
elements.append(annex_table)

# Build final
doc.build(elements, onFirstPage=footer, onLaterPages=footer)
