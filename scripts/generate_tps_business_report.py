#!/usr/bin/env python3
"""
generate_tps_business_report.py (PRO / KPMG style)

Input:
  - metrics_full_report.csv   (source,metric,value)
  - report_data/shopify_timeseries.csv
  - report_data/ga4_timeseries.csv
  - report_data/ga4_sources.csv

Output:
  - TPS-Business-Weekly.pdf  (rapport multi-pages)
"""

import sys
import os
import io
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
)
from reportlab.lib import colors

import requests


LOGO_URL = (
    "https://cdn.shopify.com/s/files/1/0861/3180/2460/files/"
    "LOGO_ARRONDI_NT12052025_-_1200x628.jpg-removebg-preview.png?v=1747069835"
)

ACCENT = colors.HexColor("#1F3B57")   # bleu "consulting"
LIGHT_BG = colors.HexColor("#F4F5F7")


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def load_csv_safe(path, **kwargs):
    if not os.path.exists(path):
        return None
    return pd.read_csv(path, **kwargs)


def fig_to_image(width_cm=16, height_cm=7):
    """Convert current matplotlib fig to a centered ReportLab Image."""
    buf = io.BytesIO()
    plt.gcf().set_size_inches(width_cm / 2.54, height_cm / 2.54)
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    img = Image(buf, width=width_cm * cm, height=None)
    img.hAlign = "CENTER"
    return img


def make_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="TitleTPS",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        textColor=ACCENT,
        spaceAfter=12,
    ))

    styles.add(ParagraphStyle(
        name="H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=ACCENT,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name="H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=ACCENT,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        spaceAfter=6,
        alignment=TA_LEFT,
    ))

    styles.add(ParagraphStyle(
        name="KPI",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=ACCENT,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        name="SmallLabel",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_LEFT,
    ))

    return styles


def footer(canvas, doc):
    page_num = canvas.getPageNumber()
    text = (
        f"Page {page_num}  •  Rapport généré le "
        f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    )
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(A4[0] - 1.5 * cm, 1 * cm, text)


def kpi_value(df, metric_name):
    row = df[df["metric"] == metric_name]
    if row.empty:
        return "-"
    try:
        v = float(row["value"].iloc[0])
        if abs(v) >= 1000:
            return f"{v:,.0f}".replace(",", " ")
        return f"{v:,.2f}"
    except Exception:
        return str(row["value"].iloc[0])


# --------------------------------------------------
# Build Report
# --------------------------------------------------
def build_report(input_csv, output_pdf):
    base_dir = os.path.dirname(input_csv)

    metrics = pd.read_csv(input_csv)  # source,metric,value
    shopify = metrics[metrics["source"] == "shopify"].copy()
    ga4 = metrics[metrics["source"] == "ga4"].copy()

    shopify_ts = load_csv_safe(os.path.join(base_dir, "shopify_timeseries.csv"))
    ga4_ts = load_csv_safe(os.path.join(base_dir, "ga4_timeseries.csv"))
    ga4_sources = load_csv_safe(os.path.join(base_dir, "ga4_sources.csv"))

    styles = make_styles()
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2 * cm,
    )
    story = []

    # ----------------- COVER / EXEC SUMMARY HEADER -----------------
    # Logo
    try:
        resp = requests.get(LOGO_URL, timeout=10)
        resp.raise_for_status()
        buf = io.BytesIO(resp.content)
        logo = Image(buf, width=6 * cm, height=None)
        logo.hAlign = "CENTER"
        story.append(logo)
        story.append(Spacer(1, 0.6 * cm))
    except Exception:
        pass

    story.append(Paragraph("THE PET SOCIETY — Weekly Business Report", styles["TitleTPS"]))
    story.append(Paragraph("Vue consolidée Shopify / GA4 — horizon 7 jours", styles["SmallLabel"]))
    story.append(Spacer(1, 0.5 * cm))

    # KPI GRID (style consulting)
    kpi_rows = [
        [
            Paragraph("Revenue Shopify (7j)", styles["KPI"]),
            Paragraph(kpi_value(shopify, "Revenue (7d)"), styles["KPI"]),
            Paragraph("Revenue GA4 (7j)", styles["KPI"]),
            Paragraph(kpi_value(ga4, "Revenue (7d)"), styles["KPI"]),
        ],
        [
            Paragraph("Conversions Shopify (7j)", styles["KPI"]),
            Paragraph(kpi_value(shopify, "Conversions (7d)"), styles["KPI"]),
            Paragraph("Sessions GA4 (7j)", styles["KPI"]),
            Paragraph(kpi_value(ga4, "Sessions (7d)"), styles["KPI"]),
        ],
        [
            Paragraph("AOV Shopify (7j)", styles["KPI"]),
            Paragraph(kpi_value(shopify, "AOV (7d)"), styles["KPI"]),
            Paragraph("Conversions GA4 (7j)", styles["KPI"]),
            Paragraph(kpi_value(ga4, "Conversions (7d)"), styles["KPI"]),
        ],
    ]

    kpi_table = Table(
        kpi_rows,
        colWidths=[4.5 * cm, 3 * cm, 4.5 * cm, 3 * cm],
        hAlign="CENTER",
    )
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 0.7, ACCENT),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.8 * cm))

    story.append(Paragraph("1. Executive Summary", styles["H1"]))
    story.append(Paragraph(
        "Ce rapport synthétise la performance business de THE PET SOCIETY sur la dernière semaine : "
        "revenus, conversions, trafic et mix de canaux. L’objectif est de fournir une base factuelle "
        "pour les décisions marketing (budget paid), produit (offre) et expérience client.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "Les sections suivantes détaillent les revenus, la dynamique de trafic et le poids relatif des "
        "canaux d’acquisition (organique, paid, social…), avec des recommandations actionnables en fin de rapport.",
        styles["Body"],
    ))
    story.append(PageBreak())

    # ----------------- SECTION 2 — BUSINESS REVENUE -----------------
    story.append(Paragraph("2. Business Revenue & Conversions", styles["H1"]))
    story.append(Spacer(1, 0.2 * cm))

    # Bar chart comparatif revenus Shopify / GA4
    if not shopify.empty or not ga4.empty:
        rev_shopify = float(shopify[shopify["metric"] == "Revenue (7d)"]["value"].iloc[0]) \
            if not shopify.empty and "Revenue (7d)" in shopify["metric"].values else 0
        rev_ga4 = float(ga4[ga4["metric"] == "Revenue (7d)"]["value"].iloc[0]) \
            if not ga4.empty and "Revenue (7d)" in ga4["metric"].values else 0

        plt.figure()
        bars = plt.bar(["Shopify", "GA4"], [rev_shopify, rev_ga4])
        plt.title("Revenus totaux 7 derniers jours")
        plt.ylabel("€")
        for b in bars:
            h = b.get_height()
            plt.text(b.get_x() + b.get_width() / 2, h, f"{h:,.0f}".replace(",", " "),
                     ha="center", va="bottom", fontsize=8)
        img = fig_to_image()
        story.append(img)
        story.append(Spacer(1, 0.3 * cm))

    # Timeseries revenus (Shopify vs GA4)
    if shopify_ts is not None and ga4_ts is not None:
        st = shopify_ts.copy()
        gt = ga4_ts.copy()
        st["date"] = pd.to_datetime(st["date"])
        gt["date"] = pd.to_datetime(gt["date"])

        merged = pd.merge(
            st[["date", "revenue"]],
            gt[["date", "revenue"]],
            on="date",
            how="outer",
            suffixes=("_shopify", "_ga4"),
        ).sort_values("date")

        plt.figure()
        plt.plot(merged["date"], merged["revenue_shopify"], marker="o", label="Shopify")
        plt.plot(merged["date"], merged["revenue_ga4"], marker="o", label="GA4")
        plt.title("Revenus journaliers (7 jours)")
        plt.xlabel("Date")
        plt.ylabel("€")
        plt.xticks(rotation=45, ha="right")
        plt.legend()
        img = fig_to_image()
        story.append(img)

    story.append(PageBreak())

    # ----------------- SECTION 3 — TRAFFIC & ACQUISITION ------------
    story.append(Paragraph("3. Traffic & Acquisition (GA4)", styles["H1"]))
    story.append(Spacer(1, 0.2 * cm))

    if ga4_sources is not None and not ga4_sources.empty:
        top_channels = ga4_sources.groupby("channel", as_index=False)[
            ["sessions", "conversions", "revenue"]
        ].sum()
        top_channels = top_channels.sort_values("sessions", ascending=False).head(8)

        # Tableau comparatif
        tdata = [["Canal", "Sessions", "Conversions", "Revenus (€)"]]
        for _, row in top_channels.iterrows():
            tdata.append([
                row["channel"],
                f"{int(row['sessions']):,}".replace(",", " "),
                f"{int(row['conversions']):,}".replace(",", " "),
                f"{float(row['revenue']):,.0f}".replace(",", " "),
            ])

        table = Table(tdata, colWidths=[6 * cm, 3 * cm, 3 * cm, 3 * cm], hAlign="CENTER")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BG),
            ("TEXTCOLOR", (0, 0), (-1, 0), ACCENT),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.4 * cm))

        # Bar chart sessions par canal
        plt.figure()
        plt.bar(top_channels["channel"], top_channels["sessions"])
        plt.title("Sessions par canal (Top 8)")
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Sessions")
        img = fig_to_image()
        story.append(img)

    story.append(PageBreak())

    # ----------------- SECTION 4 — NEXT STEPS -----------------------
    story.append(Paragraph("4. Next Steps & Recommandations", styles["H1"]))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "• **Alignement Shopify vs GA4** — contrôler régulièrement l’écart de revenus et de conversions. "
        "Un écart > 5–10 % doit déclencher une revue du tracking (GTM, balises GA4, events d’achat).<br/>"
        "• **Budget Paid Media** — concentrer les investissements sur les canaux dont le ratio "
        "revenue/sessions est le plus élevé (ROAS implicite), tout en surveillant la contribution "
        "du trafic organique (SEO / social).<br/>"
        "• **Dashboarding** — exposer ces indicateurs dans un dashboard Streamlit ou BI (hebdomadaire) "
        "pour suivre la trajectoire du lancement et documenter les décisions marketing.",
        styles["Body"],
    ))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"✅ PDF généré : {output_pdf}")
    print("   Style : PRO / consulting (TPS Business Weekly)")


def main():
    if len(sys.argv) != 3:
        print("Usage: generate_tps_business_report.py <metrics_full_report.csv> <output.pdf>")
        raise SystemExit(1)
    input_csv = sys.argv[1]
    output_pdf = sys.argv[2]
    build_report(input_csv, output_pdf)


if __name__ == "__main__":
    main()
