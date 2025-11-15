#!/usr/bin/env python3
"""
generate_tps_exec_summary.py

1-page Executive Summary based on metrics_full_report.csv
"""

import sys
import os
from datetime import datetime

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib import colors
import io
import requests


LOGO_URL = "https://cdn.shopify.com/s/files/1/0861/3180/2460/files/LOGO_ARRONDI_NT12052025_-_1200x628.jpg-removebg-preview.png?v=1747069835"


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitleTPS",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
    ))
    return styles


def get_metric(df, source, name):
    sub = df[(df["source"] == source) & (df["metric"] == name)]
    if sub.empty:
        return "-"
    try:
        v = float(sub["value"].iloc[0])
        if abs(v) >= 1000:
            return f"{v:,.0f}".replace(",", " ")
        return f"{v:,.2f}"
    except Exception:
        return str(sub["value"].iloc[0])


def build_exec(input_csv, output_pdf):
    df = pd.read_csv(input_csv)
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
        resp = requests.get(LOGO_URL, timeout=10)
        resp.raise_for_status()
        buf = io.BytesIO(resp.content)
        logo = Image(buf, width=5*cm, height=None)
        logo.hAlign = "CENTER"
        story.append(logo)
        story.append(Spacer(1, 0.5*cm))
    except Exception:
        pass

    story.append(Paragraph("THE PET SOCIETY — Executive Summary (7 jours)", styles["TitleTPS"]))
    story.append(Spacer(1, 0.7*cm))

    # KPI grid
    data = [
        ["Revenus Shopify (7j)", get_metric(df, "shopify", "Revenue (7d)"),
         "Revenus GA4 (7j)", get_metric(df, "ga4", "Revenue (7d)")],
        ["Conversions Shopify (7j)", get_metric(df, "shopify", "Conversions (7d)"),
         "Conversions GA4 (7j)", get_metric(df, "ga4", "Conversions (7d)")],
        ["AOV Shopify (7j)", get_metric(df, "shopify", "AOV (7d)"),
         "Sessions GA4 (7j)", get_metric(df, "ga4", "Sessions (7d)")],
        ["Users GA4 (7j)", get_metric(df, "ga4", "Users (7d)"),
         "Taux de rebond GA4", get_metric(df, "ga4", "Bounce Rate (%)") + " %"],
    ]

    table = Table(data, colWidths=[5*cm, 3*cm, 5*cm, 3*cm])
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

    txt = (
        "• Vue consolidée des performances business et marketing sur les 7 derniers jours.<br/>"
        "• Shopify = source vérité sur le revenu et le panier moyen ; GA4 = vue trafic et attribution.<br/>"
        "• Utiliser ces chiffres comme base pour ajuster les budgets d'acquisition (Meta Ads, Google Ads) "
        "et prioriser les chantiers UX / performance."
    )
    story.append(Paragraph(txt, styles["Body"]))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        f"Rapport généré le {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        styles["Body"],
    ))

    doc.build(story)
    print(f"✅ Executive 1-page PDF généré : {output_pdf}")


def main():
    if len(sys.argv) != 3:
        print("Usage: generate_tps_exec_summary.py <metrics_full_report.csv> <output.pdf>")
        sys.exit(1)
    build_exec(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
