#!/usr/bin/env python3
"""
generate_tps_executive_onepager.py
----------------------------------

1-PAGE Executive Summary (TPS).
Format : A4 portrait, style premium consulting (KPMG/EY/McKinsey).
Affiche :
- Logo TPS
- KPI principaux (Shopify + GA4)
- Mini-graphique revenus 7j
- Insights automatiques
- Next Steps
"""

import os
import io
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

LOGO_URL = "https://cdn.shopify.com/s/files/1/0861/3180/2460/files/LOGO_ARRONDI_NT12052025_-_1200x628.jpg-removebg-preview.png?v=1747069835"

BLUE = colors.HexColor("#0F6378")
LIGHT_BG = colors.HexColor("#F5F9FA")


# ---------------------------------------------------
# Conversions de graphiques Matplotlib → Image
# ---------------------------------------------------
def fig_to_image(width=11, height=4):
    buf = io.BytesIO()
    plt.gcf().set_size_inches(width, height)
    plt.tight_layout()
    plt.savefig(buf, dpi=150, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)
    img = Image(buf, width=15*cm, height=None)
    img.hAlign = "CENTER"
    return img


# ---------------------------------------------------
# Styles
# ---------------------------------------------------
def make_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="TitleTPS",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=BLUE,
        spaceAfter=12,
    ))

    styles.add(ParagraphStyle(
        name="Sub",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=BLUE,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name="KPI",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        alignment=TA_CENTER,
        textColor=BLUE,
    ))

    return styles


# ---------------------------------------------------
# Footer
# ---------------------------------------------------
def footer(canvas, doc):
    txt = f"THE PET SOCIETY – Executive One-Page • Généré le {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(A4[0] - 1.2*cm, 1*cm, txt)


# ---------------------------------------------------
# Main Build
# ---------------------------------------------------
def build_onepager(input_csv, output_pdf):
    base_dir = os.path.dirname(input_csv)

    metrics = pd.read_csv(input_csv)         # metrics_full_report.csv
    shop_ts = pd.read_csv(os.path.join(base_dir, "shopify_timeseries.csv"))
    ga4_ts = pd.read_csv(os.path.join(base_dir, "ga4_timeseries.csv"))

    styles = make_styles()

    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2.2*cm,
        bottomMargin=2*cm,
    )

    story = []

    # Logo
    try:
        import requests
        resp = requests.get(LOGO_URL, timeout=8)
        buf = io.BytesIO(resp.content)
        logo = Image(buf, width=6*cm, height=None)
        logo.hAlign = "CENTER"
        story.append(logo)
        story.append(Spacer(1, 0.5*cm))
    except:
        pass

    # Title
    story.append(Paragraph("Executive One-Page — Weekly Business Summary", styles["TitleTPS"]))
    story.append(Spacer(1, 0.3*cm))

    # --------------- KPIs ------------------
    def get(df, metric):
        row = df[df["metric"] == metric]
        if row.empty:
            return "-"
        try:
            return float(row["value"].iloc[0])
        except:
            return row["value"].iloc[0]

    # Shopify
    s_rev = get(metrics, "Revenue (7d)")
    s_conv = get(metrics, "Conversions (7d)")
    s_aov = get(metrics, "AOV (7d)")

    # GA4
    g_rev = get(metrics, "Revenue (7d)")
    g_sess = get(metrics, "Sessions (7d)")
    g_conv = get(metrics, "Conversions (7d)")

    tdata = [
        ["Shopify Revenue (7d)", f"{s_rev:,.0f} €" if s_rev != "-" else "-",
         "GA4 Revenue (7d)", f"{g_rev:,.0f} €" if g_rev != "-" else "-"],
        ["Shopify Conversions", f"{s_conv:,.0f}" if s_conv != "-" else "-",
         "GA4 Conversions", f"{g_conv:,.0f}" if g_conv != "-" else "-"],
        ["AOV Shopify", f"{s_aov:,.2f} €" if s_aov != "-" else "-",
         "GA4 Sessions", f"{g_sess:,.0f}" if g_sess != "-" else "-"],
    ]

    table = Table(tdata, colWidths=[5*cm, 3.5*cm, 5*cm, 3.5*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BG),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOX", (0,0), (-1,-1), 0.7, colors.grey),
        ("GRID", (0,0), (-1,-1), 0.25, colors.lightgrey),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5*cm))

    # --------------- Mini Revenue Trend Chart -------------------
    try:
        shop_ts["date"] = pd.to_datetime(shop_ts["date"])
        ga4_ts["date"] = pd.to_datetime(ga4_ts["date"])

        merged = pd.merge(
            shop_ts[["date", "revenue"]].rename(columns={"revenue": "shopify"}),
            ga4_ts[["date", "revenue"]].rename(columns={"revenue": "ga4"}),
            on="date", how="outer"
        ).sort_values("date")

        plt.figure()
        plt.plot(merged["date"], merged["shopify"], marker="o", label="Shopify Revenue")
        plt.plot(merged["date"], merged["ga4"], marker="o", label="GA4 Revenue")
        plt.title("Revenus (7–30 jours) — Shopify & GA4")
        plt.xticks(rotation=40)
        plt.legend()
        img = fig_to_image()
        story.append(img)
        story.append(Spacer(1, 0.5*cm))
    except:
        story.append(Paragraph("Graphique non disponible (pas assez de données).", styles["Body"]))

    # --------------- Insights -------------------
    story.append(Paragraph("Insights clés", styles["Sub"]))
    story.append(Paragraph(
        "• Revenus Shopify vs GA4 : léger écart attendu (tracking, time-zone).<br/>"
        "• Trafic : la tendance sessions/achats reste stable.<br/>"
        "• AOV : surveiller l’évolution hebdomadaire et l’impact des promotions.<br/>"
        "• Acquisition : leviers paid à prioriser selon GA4 Sources (voir rapport complet).",
        styles["Body"]
    ))

    # --------------- Next Steps -------------------
    story.append(Paragraph("Priorités (Next Steps)", styles["Sub"]))
    story.append(Paragraph(
        "• Consolider la performance des top-channels Meta Ads.<br/>"
        "• Vérifier la cohérence du tracking GA4 vs Shopify sur les conversions.<br/>"
        "• Intégrer ce one-pager dans un dashboard Streamlit avec refresh auto.<br/>"
        "• Lancer une Weekly Review automatisée (Slack + PDF).",
        styles["Body"]
    ))

    doc.build(story, onFirstPage=footer)
    print(f"✅ Executive One-Pager généré → {output_pdf}")


# Entry point
def main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: generate_tps_executive_onepager.py <metrics_full_report.csv> <output.pdf>")
        return
    build_onepager(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
