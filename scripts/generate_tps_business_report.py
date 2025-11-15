#!/usr/bin/env python3
"""
generate_tps_business_report.py

Full multi-section BUSINESS report for THE PET SOCIETY.
Input:
  - metrics_full_report.csv (columns: source,metric,value)
  - report_data/shopify_timeseries.csv
  - report_data/ga4_timeseries.csv
  - report_data/ga4_sources.csv

Output:
  - PDF A4 multi-pages (portrait), with centered charts and TPS logo.
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


LOGO_URL = "https://cdn.shopify.com/s/files/1/0861/3180/2460/files/LOGO_ARRONDI_NT12052025_-_1200x628.jpg-removebg-preview.png?v=1747069835"


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def load_csv_safe(path, **kwargs):
    if not os.path.exists(path):
        return None
    return pd.read_csv(path, **kwargs)


def fig_to_image(width=14, height=6):
    """Convert current matplotlib fig to a ReportLab Image, centered."""
    buf = io.BytesIO()
    plt.gcf().set_size_inches(width, height)
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    img = Image(buf, width=16*cm, height=None)  # 16cm wide, height auto
    img.hAlign = "CENTER"
    return img


def make_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="TitleTPS",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name="H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="KPI",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        alignment=TA_CENTER,
    ))
    return styles


def footer(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}  •  Rapport généré le {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(A4[0] - 1.5*cm, 1*cm, text)


# --------------------------------------------------
# Build Report
# --------------------------------------------------
def build_report(input_csv, output_pdf):
    base_dir = os.path.dirname(input_csv)
    metrics = pd.read_csv(input_csv)  # columns: source,metric,value

    shopify = metrics[metrics["source"] == "shopify"].copy()
    ga4 = metrics[metrics["source"] == "ga4"].copy()

    shopify_ts = load_csv_safe(os.path.join(base_dir, "shopify_timeseries.csv"))
    ga4_ts = load_csv_safe(os.path.join(base_dir, "ga4_timeseries.csv"))
    ga4_sources = load_csv_safe(os.path.join(base_dir, "ga4_sources.csv"))

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

    # -------------------------
    # Cover / Executive header
    # -------------------------
    # Logo
    try:
        import requests
        resp = requests.get(LOGO_URL, timeout=10)
        resp.raise_for_status()
        buf = io.BytesIO(resp.content)
        logo = Image(buf, width=6*cm, height=None)
        logo.hAlign = "CENTER"
        story.append(logo)
        story.append(Spacer(1, 0.8*cm))
    except Exception:
        pass

    story.append(Paragraph("THE PET SOCIETY — Weekly Business Report", styles["TitleTPS"]))
    story.append(Spacer(1, 0.5*cm))

    # Quick KPIs table
    def kpi_val(df, metric_name):
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

    kpis_data = [
        ["Revenue Shopify (7j)", kpi_val(shopify, "Revenue (7d)"),
         "Revenue GA4 (7j)", kpi_val(ga4, "Revenue (7d)")],
        ["Conversions Shopify (7j)", kpi_val(shopify, "Conversions (7d)"),
         "Conversions GA4 (7j)", kpi_val(ga4, "Conversions (7d)")],
        ["AOV Shopify (7j)", kpi_val(shopify, "AOV (7d)"),
         "Sessions GA4 (7j)", kpi_val(ga4, "Sessions (7d)")],
    ]
    table = Table(kpis_data, colWidths=[5*cm, 3*cm, 5*cm, 3*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.8*cm))

    story.append(Paragraph("1. Executive Summary", styles["H1"]))
    story.append(Paragraph(
        "Ce rapport consolide les performances business, marketing et techniques de THE PET SOCIETY "
        "sur les 7 derniers jours. Il met en avant les revenus, les conversions, le trafic et les canaux "
        "d'acquisition principaux, afin de guider les décisions marketing et produit.",
        styles["Body"],
    ))
    story.append(PageBreak())

    # -------------------------
    # Section 2 — Business Revenue
    # -------------------------
    story.append(Paragraph("2. Business Revenue & Conversions", styles["H1"]))
    story.append(Spacer(1, 0.3*cm))

    # Revenue comparison bar chart
    if not shopify.empty or not ga4.empty:
        rev_shopify = float(shopify[shopify["metric"] == "Revenue (7d)"]["value"].iloc[0]) if not shopify.empty and "Revenue (7d)" in shopify["metric"].values else 0
        rev_ga4 = float(ga4[ga4["metric"] == "Revenue (7d)"]["value"].iloc[0]) if not ga4.empty and "Revenue (7d)" in ga4["metric"].values else 0

        plt.figure()
        labels = ["Shopify", "GA4"]
        values = [rev_shopify, rev_ga4]
        plt.bar(labels, values)
        plt.title("Revenus (7 derniers jours)")
        plt.ylabel("€")
        img = fig_to_image()
        story.append(img)
        story.append(Spacer(1, 0.5*cm))

    # Timeseries revenue (Shopify vs GA4)
    if shopify_ts is not None and ga4_ts is not None:
        st = shopify_ts.copy()
        gt = ga4_ts.copy()
        st["date"] = pd.to_datetime(st["date"])
        gt["date"] = pd.to_datetime(gt["date"])

        merged = pd.merge(st[["date", "revenue"]], gt[["date", "revenue"]], on="date", how="outer", suffixes=("_shopify", "_ga4"))
        merged = merged.sort_values("date")

        plt.figure()
        plt.plot(merged["date"], merged["revenue_shopify"], marker="o", label="Shopify Revenue")
        plt.plot(merged["date"], merged["revenue_ga4"], marker="o", label="GA4 Revenue")
        plt.title("Revenus journaliers (7j)")
        plt.xlabel("Date")
        plt.ylabel("€")
        plt.xticks(rotation=45)
        plt.legend()
        img = fig_to_image()
        story.append(img)
        story.append(Spacer(1, 0.5*cm))

    story.append(PageBreak())

    # -------------------------
    # Section 3 — Traffic & Acquisition
    # -------------------------
    story.append(Paragraph("3. Traffic & Acquisition (GA4)", styles["H1"]))
    story.append(Spacer(1, 0.3*cm))

    if ga4_sources is not None and not ga4_sources.empty:
        # Top channels
        top_channels = ga4_sources.groupby("channel", as_index=False)[["sessions", "conversions", "revenue"]].sum()
        top_channels = top_channels.sort_values("sessions", ascending=False).head(8)

        # Table
        tdata = [["Channel", "Sessions", "Conversions", "Revenue"]]
        for _, row in top_channels.iterrows():
            tdata.append([
                row["channel"],
                f"{int(row['sessions']):,}".replace(",", " "),
                f"{int(float(row['conversions'])):,}".replace(",", " "),
                f"{float(row['revenue']):,.0f}".replace(",", " "),
            ])

        table = Table(tdata, colWidths=[6*cm, 3*cm, 3*cm, 3*cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.5*cm))

        # Bar chart sessions by channel
        plt.figure()
        plt.bar(top_channels["channel"], top_channels["sessions"])
        plt.title("Sessions par canal (Top 8)")
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Sessions")
        img = fig_to_image()
        story.append(img)

    story.append(PageBreak())

    # -------------------------
    # Section 4 — Next Steps
    # -------------------------
    story.append(Paragraph("4. Next Steps & Recommandations", styles["H1"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "• Surveiller l'évolution des revenus et du panier moyen sur Shopify et vérifier l'écart avec GA4 "
        "pour détecter d'éventuels problèmes de tracking.<br/>"
        "• Identifier les canaux d'acquisition les plus rentables (sessions vs revenue) et ajuster les budgets "
        "Meta Ads / Google Ads en conséquence.<br/>"
        "• Intégrer ce rapport dans un dashboard Streamlit / Notion pour suivre la trajectoire semaine par semaine.",
        styles["Body"],
    ))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"✅ PDF généré : {output_pdf}")


def main():
    if len(sys.argv) != 3:
        print("Usage: generate_tps_business_report.py <metrics_full_report.csv> <output.pdf>")
        sys.exit(1)
    input_csv = sys.argv[1]
    output_pdf = sys.argv[2]
    build_report(input_csv, output_pdf)


if __name__ == "__main__":
    main()
