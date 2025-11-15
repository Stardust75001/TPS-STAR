# ============================================================
#  A. Imports & Configuration globale
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

# --- Entrées CLI ---
csv_input = sys.argv[1]       # ex: report_data/metrics_report.csv
pdf_output = sys.argv[2]      # ex: TPS-Executive-Business-Report.pdf

# --- Palette consulting (dégradé bleu / gris) ---
BLUE_DEEP = colors.HexColor("#1F3B73")
BLUE_GREY = colors.HexColor("#4A5F78")
GREY_LIGHT = colors.HexColor("#E8ECF1")
BLACK = colors.HexColor("#1A1A1A")
WHITE = colors.white

# --- Logo TPS (téléchargé ou local) ---
LOGO_URL = (
    "https://cdn.shopify.com/s/files/1/0861/3180/2460/files/"
    "LOGO_ARRONDI_NT12052025_-_1200x628.jpg-removebg-preview.png?v=1747069835"
)
LOGO_FILENAME = "tps_logo.png"


# ============================================================
#  B. Gestion des polices & styles
# ============================================================

def register_fonts():
    """
    Essaie d'enregistrer SF Pro Rounded si les fichiers sont présents.
    Sinon fallback vers Helvetica.
    Tu peux déposer tes fichiers fonts dans ./fonts et adapter les noms.
    """
    global FONT_BODY, FONT_BODY_BOLD

    FONT_BODY = "Helvetica"
    FONT_BODY_BOLD = "Helvetica-Bold"

    # Exemple : si tu ajoutes SF Pro Rounded dans ./fonts, décommente et adapte :
    # try:
    #     pdfmetrics.registerFont(TTFont("SFProRounded", "fonts/SF-Pro-Rounded-Regular.ttf"))
    #     pdfmetrics.registerFont(TTFont("SFProRounded-Bold", "fonts/SF-Pro-Rounded-Bold.ttf"))
    #     FONT_BODY = "SFProRounded"
    #     FONT_BODY_BOLD = "SFProRounded-Bold"
    # except Exception:
    #     # Fallback silencieux vers Helvetica
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
#  C. Helpers génériques (footer, logo, charts, tables, CSV)
# ============================================================

def footer(canvas: Canvas, doc):
    """Footer bas droite avec numéro de page + date."""
    page_num = canvas.getPageNumber()
    footer_text = (
        f"Page {page_num} • Rapport généré le "
        f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    )
    canvas.setFont(FONT_BODY, 8)
    canvas.setFillColor(BLUE_GREY)
    canvas.drawRightString(A4[0] - 30, 20, footer_text)


def ensure_logo_local():
    """
    Télécharge le logo si non présent et renvoie le chemin.
    """
    if os.path.exists(LOGO_FILENAME):
        return LOGO_FILENAME

    try:
        import urllib.request

        urllib.request.urlretrieve(LOGO_URL, LOGO_FILENAME)
        return LOGO_FILENAME
    except Exception:
        # Si le téléchargement échoue, on continue sans logo.
        return None


def section_title(text: str):
    """Crée un titre de section (Paragraph) avec espacement."""
    return [
        Paragraph(f"<b>{text}</b>", title_style),
        Spacer(1, 12),
    ]


def build_kpi_table(rows, header_bg=BLUE_DEEP):
    """
    Construit un tableau KPI centré, 2 colonnes.
    rows = [[header1, header2], [val1, val2], ...]
    """
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
    """
    Génère un bar chart de la répartition des statuts.
    Retourne le chemin de l'image ou None.
    """
    if df.empty or "Status" not in df.columns:
        return None

    counts = df["Status"].value_counts()
    labels = list(counts.index)
    values = list(counts.values)

    plt.figure(figsize=(5, 3))
    bars = plt.bar(labels, values, color="#1F3B73")

    # Ajouter les valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(height),
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
    """
    Charge un CSV optionnel de type metric/value.
    Retourne {metric: value} ou {} si absent/incompatible.
    """
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


# ============================================================
#  D. Chargement des données
# ============================================================

df_health = pd.read_csv(csv_input)

base_dir = os.path.dirname(csv_input)

shopify_metrics = load_optional_metrics_csv(
    os.path.join(base_dir, "shopify_metrics.csv")
)
ga4_metrics = load_optional_metrics_csv(
    os.path.join(base_dir, "ga4_metrics.csv")
)
meta_metrics = load_optional_metrics_csv(
    os.path.join(base_dir, "meta_metrics.csv")
)
gsc_metrics = load_optional_metrics_csv(
    os.path.join(base_dir, "gsc_metrics.csv")
)
ahrefs_metrics = load_optional_metrics_csv(
    os.path.join(base_dir, "ahrefs_metrics.csv")
)
social_metrics = load_optional_metrics_csv(
    os.path.join(base_dir, "social_metrics.csv")
)


# ============================================================
#  E. Construction du document PDF
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
# Page 1 — Logo + Executive Summary
# ------------------------------------------------------------

# Logo centré
logo_path = ensure_logo_local()
if logo_path:
    logo = Image(logo_path, width=180, height=90)
    logo.hAlign = "CENTER"
    elements.append(logo)
    elements.append(Spacer(1, 16))

# Titre section
elements += section_title("📌 Executive Summary")

ok_count = (df_health["Status"] == "OK").sum()
total = len(df_health)
score = int((ok_count / total) * 100) if total > 0 else 0

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

# Résumé business si métriques disponibles
summary_lines = []

# Shopify
if "Conversions (7d)" in shopify_metrics:
    summary_lines.append(
        f"• Conversions Shopify (7j) : {shopify_metrics['Conversions (7d)']}"
    )
if "Revenue (7d)" in shopify_metrics:
    summary_lines.append(
        f"• Chiffre d'affaires (7j) : {shopify_metrics['Revenue (7d)']}"
    )
if "AOV (7d)" in shopify_metrics:
    summary_lines.append(
        f"• Panier moyen (7j) : {shopify_metrics['AOV (7d)']}"
    )

# GA4
if "Sessions (7d)" in ga4_metrics:
    summary_lines.append(
        f"• Sessions GA4 (7j) : {ga4_metrics['Sessions (7d)']}"
    )
if "ConvRate (7d)" in ga4_metrics:
    summary_lines.append(
        f"• Taux de conversion Analytics (7j) : {ga4_metrics['ConvRate (7d)']}"
    )

# Meta
if "ROAS (7d)" in meta_metrics:
    summary_lines.append(
        f"• ROAS Meta Ads (7j) : {meta_metrics['ROAS (7d)']}"
    )

if not summary_lines:
    summary_text = (
        "Les données business détaillées (CA, conversions, ROAS, SEO) "
        "seront enrichies dès que les exports CSV Shopify / GA4 / Meta "
        "seront branchés sur ce rapport."
    )
else:
    summary_text = "<br/>".join(summary_lines)

elements.append(Paragraph(summary_text, text_style))
elements.append(Spacer(1, 16))

# Graphique santé des services (centré)
chart_path = generate_health_chart(df_health)
if chart_path and os.path.exists(chart_path):
    chart_img = Image(chart_path, width=400, height=240)
    chart_img.hAlign = "CENTER"
    elements.append(chart_img)

elements.append(PageBreak())

# ------------------------------------------------------------
# Page 2 — Business Revenue
# ------------------------------------------------------------
elements += section_title("📈 Business Revenue")

business_rows = [["KPI", "Valeur"]]

# Shopify
business_rows.append([
    "Conversions Shopify (7j)",
    shopify_metrics.get("Conversions (7d)", "N/A"),
])
business_rows.append([
    "Chiffre d'affaires (7j)",
    shopify_metrics.get("Revenue (7d)", "N/A"),
])
business_rows.append([
    "Panier moyen (7j)",
    shopify_metrics.get("AOV (7d)", "N/A"),
])

# GA4
business_rows.append([
    "Sessions (7j)",
    ga4_metrics.get("Sessions (7d)", "N/A"),
])
business_rows.append([
    "Taux conversion Analytics (7j)",
    ga4_metrics.get("ConvRate (7d)", "N/A"),
])

# Meta
business_rows.append([
    "ROAS Meta (7j)",
    meta_metrics.get("ROAS (7d)", "N/A"),
])
business_rows.append([
    "Budget Meta (7j)",
    meta_metrics.get("Spend (7d)", "N/A"),
])

business_table = build_kpi_table(business_rows)
elements.append(business_table)
elements.append(PageBreak())

# ------------------------------------------------------------
# Page 3 — Tech Stability / Ops
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# Page 4 — Marketing / SEO
# ------------------------------------------------------------
elements += section_title("👁️ Marketing & SEO")

seo_rows = [["KPI", "Valeur"]]

# GSC
seo_rows.append(["Clics SEO (7j)", gsc_metrics.get("Clicks (7d)", "N/A")])
seo_rows.append([
    "Impressions SEO (7j)",
    gsc_metrics.get("Impressions (7d)", "N/A"),
])
seo_rows.append(["Pages indexées", gsc_metrics.get("Valid Pages", "N/A")])

# Ahrefs
seo_rows.append(["Domain Rating", ahrefs_metrics.get("Domain Rating", "N/A")])
seo_rows.append(["Backlinks", ahrefs_metrics.get("Backlinks", "N/A")])

# Social
seo_rows.append([
    "Instagram Engagement (7j)",
    social_metrics.get("Instagram Engagement (7d)", "N/A"),
])
seo_rows.append([
    "TikTok Views (7j)",
    social_metrics.get("TikTok Views (7d)", "N/A"),
])

seo_table = build_kpi_table(seo_rows, header_bg=BLUE_GREY)
elements.append(seo_table)
elements.append(PageBreak())

# ------------------------------------------------------------
# Page 5 — Data Quality & Monitoring
# ------------------------------------------------------------
elements += section_title("🧩 Data Quality & Monitoring")

dq_rows = [
    ["Indicateur", "Statut / Commentaire"],
    [
        "Qualité tracking (GTM / GA4 / Pixel)",
        "À dériver des statuts GTM_ID, GA4_TOKEN, META_TOKEN, SHOPIFY_API_KEY, etc.",
    ],
    [
        "Exhaustivité métriques",
        "À préciser lorsque les CSV Shopify / GA4 / Meta seront branchés.",
    ],
    [
        "Historique erreurs système",
        "À enrichir avec des logs / statistiques supplémentaires (Sentry, JS errors…).",
    ],
]

dq_table = build_kpi_table(dq_rows, header_bg=BLUE_DEEP)
elements.append(dq_table)
elements.append(PageBreak())

# ------------------------------------------------------------
# Page 6 — Analyse & Recommandations
# ------------------------------------------------------------
elements += section_title("🔍 Analyse & Recommandations")

analysis_lines = []

# Analyse score global
if score == 100:
    analysis_lines.append(
        "• L’ensemble des services monitorés est actuellement opérationnel (100% OK)."
    )
elif score >= 80:
    analysis_lines.append(
        "• La majorité des services est opérationnelle. Quelques intégrations sont à surveiller."
    )
else:
    analysis_lines.append(
        "• Plusieurs services clés présentent des anomalies. Prioriser la remédiation sur les intégrations critiques."
    )

# Points critiques
def append_if_status_not_ok(service_key, label):
    if service_key in df_health["Service"].values:
        status = df_health.loc[
            df_health["Service"] == service_key, "Status"
        ].iloc[0]
        if status != "OK":
            analysis_lines.append(f"• {label} : statut {status} → action requise.")

append_if_status_not_ok("SHOPIFY_API_KEY", "Shopify API Key (données produits / commandes)")
append_if_status_not_ok("GA4_TOKEN", "GA4 Token (Analytics / funnels)")
append_if_status_not_ok("META_TOKEN", "Meta Token (Meta Ads / Pixel)")
append_if_status_not_ok("GSC_CREDENTIALS", "GSC Credentials (Search Console SEO)")
append_if_status_not_ok("CLOUDFLARE_TOKEN", "Cloudflare Token (DNS / edge security)")

if not analysis_lines:
    analysis_lines.append(
        "• Les données actuelles ne permettent pas encore une analyse détaillée des KPI business. "
        "Brancher Shopify / GA4 / Meta / Ahrefs pour enrichir ce rapport."
    )

analysis_text = "<br/>".join(analysis_lines)
elements.append(Paragraph(analysis_text, text_style))
elements.append(Spacer(1, 16))

recos = """
<b>À 48 heures :</b><br/>
• Corriger en priorité les secrets en statut MISSING / INVALID (Shopify, GA4, Meta, GSC, Slack, SMTP…).<br/>
• Vérifier que GTM, GA4 et le Pixel Meta remontent correctement les évènements clés (page_view, view_item, add_to_cart, purchase).<br/><br/>

<b>À 7 jours :</b><br/>
• Brancher les exports automatisés Shopify (commandes, CA, AOV) dans <i>shopify_metrics.csv</i> utilisé par ce rapport.<br/>
• Brancher un rapport GA4 (sessions, conversion rate, top sources) dans <i>ga4_metrics.csv</i>.<br/>
• Brancher un résumé Meta Ads (ROAS, spend, CPA) dans <i>meta_metrics.csv</i>.<br/><br/>

<b>À 30 jours :</b><br/>
• Mettre en place un dashboard interactif (Notion / Data Studio / Streamlit) alimenté par les mêmes sources que ce PDF.<br/>
• Historiser les rapports (hebdomadaire) pour suivre les tendances et anticiper les risques.<br/>
• Ajouter des alertes Slack dès qu’un service clé passe en statut INVALID / MISSING.<br/>
"""
elements.append(Paragraph(recos, text_style))
elements.append(PageBreak())

# ------------------------------------------------------------
# Page 7 — Annexe : données brutes
# ------------------------------------------------------------
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

# ============================================================
#  F. Génération du PDF
# ============================================================

doc.build(elements, onFirstPage=footer, onLaterPages=footer)
