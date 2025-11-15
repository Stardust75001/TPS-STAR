import sys
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
import matplotlib.pyplot as plt
import numpy as np
import os

# ----------------------------------------
# Inputs
# ----------------------------------------
csv_input = sys.argv[1]
pdf_output = sys.argv[2]

df = pd.read_csv(csv_input)

# ----------------------------------------
# PDF Setup
# ----------------------------------------
styles = getSampleStyleSheet()
title_style = styles["Title"]
subtitle_style = styles["Heading2"]
text_style = styles["BodyText"]

TAUPE = colors.HexColor("#BA986E")
BLACK = colors.HexColor("#1A1A1A")

# Footer with page number
def footer(canvas: Canvas, doc):
    page_num = canvas.getPageNumber()
    footer_text = f"Page {page_num} — Rapport généré le {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(570, 20, footer_text)

# Document
doc = SimpleDocTemplate(
    pdf_output,
    pagesize=A4,
    title="TPS Executive Business Report",
    author="The Pet Society Paris",
)

elements = []

# ----------------------------------------
# Helper: Section Title
# ----------------------------------------
def section(title):
    elements.append(Paragraph(f"<b>{title}</b>", title_style))
    elements.append(Spacer(1, 12))

# ----------------------------------------
# Helper: generate chart
# ----------------------------------------
def chart(values, labels, title, filename="temp_chart.png"):
    plt.figure(figsize=(5,3))
    plt.bar(labels, values, color="#BA986E")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename

# ----------------------------------------
# PAGE 1 — EXECUTIVE SUMMARY
# ----------------------------------------
section("📌 Executive Summary")

elements.append(Paragraph(
    "Résumé global des performances Business, Tech, SEO et Data.",
    text_style
))
elements.append(Spacer(1, 20))

# Compute global score
ok_count = (df['Status'] == "OK").sum()
total = len(df)
score = int((ok_count / total) * 100)

elements.append(Paragraph(
    f"<b>TPS Health Score :</b> {score} / 100",
    subtitle_style
))

elements.append(Paragraph(
    "<b>Systems OK :</b> {} / {}".format(ok_count, total),
    text_style
))

elements.append(PageBreak())

# ----------------------------------------
# PAGE 2 — BUSINESS KPIs
# ----------------------------------------
section("📈 Business Revenue")

# Placeholder KPIs (replace by API data later)
business_kpis = [
    ["Conversions Shopify", "N/A"],
    ["Panier Moyen", "N/A"],
    ["Traffic organique / paid", "N/A"],
    ["Performance Meta Ads (ROAS / CTR / CPC)", "N/A"],
]

table = Table(business_kpis)
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), TAUPE),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("GRID", (0,0), (-1,-1), 0.5, BLACK)
]))
elements.append(table)
elements.append(PageBreak())

# ----------------------------------------
# PAGE 3 — TECH STABILITY
# ----------------------------------------
section("🛠 Tech Stability / Ops")

tech_table = df.values.tolist()
tech_table.insert(0, ["Service", "Status"])

table = Table(tech_table)
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), TAUPE),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("GRID", (0,0), (-1,-1), 0.5, BLACK)
]))

elements.append(table)
elements.append(PageBreak())

# ----------------------------------------
# PAGE 4 — MARKETING & SEO
# ----------------------------------------
section("👁️ Marketing & SEO")

seo_kpis = [
    ["Indexation GSC", "N/A"],
    ["Domain Health (Ahrefs)", "N/A"],
    ["Instagram Engagement", "N/A"],
    ["TikTok KPIs", "N/A"],
]

table = Table(seo_kpis)
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), TAUPE),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("GRID", (0,0), (-1,-1), 0.5, BLACK)
]))

elements.append(table)
elements.append(PageBreak())

# ----------------------------------------
# PAGE 5 — DATA QUALITY & MONITORING
# ----------------------------------------
section("🧩 Data Quality & Monitoring")

dq = [
    ["Qualité tracking (GA4 / GTM / Pixel)", "N/A"],
    ["Exhaustivité métriques", "N/A"],
    ["Historique erreurs système", "N/A"],
]

table = Table(dq)
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), TAUPE),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("GRID", (0,0), (-1,-1), 0.5, BLACK)
]))

elements.append(table)
elements.append(PageBreak())

# ----------------------------------------
# PAGE 6 — ANALYSE AUTOMATIQUE
# ----------------------------------------
section("🔍 Analyse (Business + Tech + SEO + Data)")

analysis_text = """
<b>Analyse automatique :</b><br/><br/>
• Les systèmes critiques semblent globalement stables.<br/>
• Risques potentiels détectés sur certaines APIs externes.<br/>
• Absence temporaire de données business (à connecter aux APIs).<br/>
• Opportunités : tracking, SEO, campagnes Meta Ads.<br/>
"""

elements.append(Paragraph(analysis_text, text_style))
elements.append(PageBreak())

# ----------------------------------------
# PAGE 7 — RECOMMANDATIONS
# ----------------------------------------
section("⭐ Recommandations Actionnables")

recos = """
<b>48 heures :</b><br/>
• Vérifier GTM / GA4 / Pixel Meta<br/>
• Valider tokens expirés (si existants)<br/><br/>

<b>7 jours :</b><br/>
• Activer reporting Shopify API automatisé<br/>
• Connecter Meta Ads Reporting API<br/><br/>

<b>30 jours :</b><br/>
• Mettre en place tableau de bord Streamlit<br/>
• Historiser données business + SEO + tech<br/>
"""

elements.append(Paragraph(recos, text_style))
elements.append(PageBreak())

# ----------------------------------------
# PAGE 8 — ANNEXE
# ----------------------------------------
section("📎 Annexe — Données Brutes")

table = Table(df.values.tolist())
table.setStyle(TableStyle([
    ("GRID", (0,0), (-1,-1), 0.25, BLACK)
]))
elements.append(table)

# ----------------------------------------
# Build PDF
# ----------------------------------------
doc.build(elements, onLaterPages=footer, onFirstPage=footer)
