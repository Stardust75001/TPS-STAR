#!/usr/bin/env python3
"""
generate_tps_executive_onepager.py

Usage:
  python generate_tps_executive_onepager.py report_data/metrics_full_report.csv TPS-Executive-1pager.pdf
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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
import requests


LOGO_URL = (
    "https://cdn.shopify.com/s/files/1/0861/3180/2460/files/"
    "LOGO_ARRONDI_NT12052025_-_1200x628.jpg-removebg-preview.png?v=1747069835"
)

ACCENT = colors.HexColor("#1F3B57")
LIGHT_BG = colors.HexColor("#F4F5F7")


def fig_to_image():
    buf = io.BytesIO()
    plt.gcf().set_size_inches(12 / 2.54, 5 / 2.54)
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    img = Image(buf, width=14 * cm, height=None)
    img.hAlign = "CENTER"
    return img


def styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(
        name="Title",
        parent=s["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=ACCENT,
        alignment=TA_CENTER,
        spaceAfter=8,
    ))
    s.add(ParagraphStyle(
        name="Body",
        parent=s["Normal"],
        fontSize=9,
        leading=12,
        alignment=TA_LEFT,
    ))
    s.add(ParagraphStyle(
        name="KPI",
        parent=s["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        alignment=TA_CENTER,
        textColor=ACCENT,
    ))
    return s


def kpi(df, src, metric_name):
    sub = df[df["source"] == src]
    row = sub[sub["metric"] == metric_name]
    if row.empty:
        return "-"
    try:
        v = float(row["value"].iloc[0])
        if abs(v) >= 1000:
            return f"{v:,.0f}".replace(",", " ")
        return f"{v:,.2f}"
    except Exception:
        return str(row["value"].iloc[0])


def build_onepager(input_csv, output_pdf):
    base_dir = os.path.dirname(input_csv)
    metrics = pd.read_csv(input_csv)
    ga4_ts_path = os.path.join(base_dir, "ga4_timeseries.csv")

    st = styles()
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.4 * cm,
    )
    story = []

    # Logo + titre
    try:
        resp = requests.get(LOGO_URL, timeout=10)
        resp.raise_for_status()
        buf = io.BytesIO(resp.content)
        logo = Image(buf, width=4.5 * cm, height=None)
        logo.hAlign = "CENTER"
        story.append(logo)
        story.append(Spacer(1, 0.3 * cm))
    except Exception:
        pass

    story.append(Paragraph("TPS — Executive Weekly Snapshot", st["Title"]))
    story.append(Paragraph(
        f"Vue synthétique business & trafic — généré le {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        st["Body"],
    ))
    story.append(Spacer(1, 0.4 * cm))

    # KPI grid 2x3
    data = [
        [
            Paragraph("Revenue Shopify (7j)", st["KPI"]),
            Paragraph(kpi(metrics, "shopify", "Revenue (7d)"), st["KPI"]),
            Paragraph("Revenue GA4 (7j)", st["KPI"]),
            Paragraph(kpi(metrics, "ga4", "Revenue (7d)"), st["KPI"]),
        ],
        [
            Paragraph("AOV Shopify (7j)", st["KPI"]),
            Paragraph(kpi(metrics, "shopify", "AOV (7d)"), st["KPI"]),
            Paragraph("Sessions GA4 (7j)", st["KPI"]),
            Paragraph(kpi(metrics, "ga4", "Sessions (7d)"), st["KPI"]),
        ],
        [
            Paragraph("Conversions Shopify (7j)", st["KPI"]),
            Paragraph(kpi(metrics, "shopify", "Conversions (7d)"), st["KPI"]),
            Paragraph("Conversions GA4 (7j)", st["KPI"]),
            Paragraph(kpi(metrics, "ga4", "Conversions (7d)"), st["KPI"]),
        ],
    ]
    table = Table(data, colWidths=[4.2 * cm, 2.8 * cm, 4.2 * cm, 2.8 * cm], hAlign="CENTER")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 0.7, ACCENT),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.4 * cm))

    # Mini-timeseries GA4 revenue/sessions
    if os.path.exists(ga4_ts_path):
        ga4_ts = pd.read_csv(ga4_ts_path)
        ga4_ts["date"] = pd.to_datetime(ga4_ts["date"])

        plt.figure()
        ax1 = plt.gca()
        ax1.plot(ga4_ts["date"], ga4_ts["revenue"], marker="o", label="Revenue (€)")
        ax1.set_ylabel("€", color="black")
        plt.xticks(rotation=45, ha="right")

        ax2 = ax1.twinx()
        ax2.plot(ga4_ts["date"], ga4_ts["sessions"], marker="o", linestyle="--", label="Sessions", color="grey")
        ax2.set_ylabel("Sessions", color="grey")

        plt.title("Revenus & Sessions (GA4, 7 derniers jours)")
        img = fig_to_image()
        story.append(img)
        story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph(
        "💡 **Lecture rapide** : "
        "si la courbe des revenus et celle des sessions se décorrèlent, il faut vérifier le mix de canaux, "
        "la qualité du trafic paid et d’éventuels problèmes de conversion (UX, produit, prix).",
        st["Body"],
    ))

    doc.build(story)
    print(f"✅ Executive one-pager généré : {output_pdf}")
