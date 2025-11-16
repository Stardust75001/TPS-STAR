#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os
import tempfile

# === PATHS ===
DATA_CSV   = "/Users/asc/Shopify/TPS STAR/PRODUCTS/STOCK - CATALOG MANAGEMENT/TPS_DROPSHIP_DECISION_DATA_v7_COMPUTED.csv"
PDF_OUTPUT = "/Users/asc/Shopify/TPS STAR/PRODUCTS/STOCK - CATALOG MANAGEMENT/TPS_DASHBOARD_REPORT.pdf"
LOG_FILE   = "/var/log/tps/dashboard.log"

# Logo TPS
LOGO_URL = "https://cdn.shopify.com/s/files/1/0861/3180/2460/files/LOGO_ARRONDI_NT12052025_-_1200x628.jpg-removebg-preview.png?v=1747069835"

# Palette inspirée de ton thème (footer bleu + bande taupe)
PRIMARY   = colors.HexColor("#3c5665")   # bleu footer
ACCENT    = colors.HexColor("#b58a74")   # taupe / gold
TEXT_DARK = colors.HexColor("#222222")
BG_LIGHT  = colors.HexColor("#f5f1eb")


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass
    print(msg)


def find_column(possible, df):
    for name in possible:
        if name in df.columns:
            return name
    return None


def build_charts(df, revenue_col, margin_col, stock_col, category_col):
    """Génère quelques graphs PNG et renvoie leurs chemins."""
    images = []

    # 1) Top produits par marge
    if margin_col:
        top_margin = df.sort_values(margin_col, ascending=False).head(8)
        plt.figure(figsize=(8, 4))
        title_col = find_column(["title", "Title", "product_title"], df) or df.columns[0]
        labels = [str(v)[:25] + ("…" if len(str(v)) > 25 else "") for v in top_margin[title_col]]
        plt.bar(labels, top_margin[margin_col])
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Marge (€)")
        plt.title("Top produits par marge")
        plt.tight_layout()
        path = os.path.join(tempfile.gettempdir(), "tps_top_margin.png")
        plt.savefig(path, dpi=150)
        plt.close()
        images.append(path)

    # 2) CA par catégorie
    if revenue_col and category_col:
        cat = (
            df.groupby(category_col)[revenue_col]
            .sum()
            .sort_values(ascending=False)
            .head(8)
        )
        plt.figure(figsize=(8, 4))
        plt.bar(cat.index.astype(str), cat.values)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("CA (€)")
        plt.title("Top catégories par CA")
        plt.tight_layout()
        path = os.path.join(tempfile.gettempdir(), "tps_ca_categories.png")
        plt.savefig(path, dpi=150)
        plt.close()
        images.append(path)

    # 3) Distribution des stocks
    if stock_col:
        plt.figure(figsize=(6, 4))
        df[stock_col].clip(lower=0).hist(bins=30)
        plt.xlabel("Stock")
        plt.ylabel("Nombre de variantes")
        plt.title("Distribution des niveaux de stock")
        plt.tight_layout()
        path = os.path.join(tempfile.gettempdir(), "tps_stock_dist.png")
        plt.savefig(path, dpi=150)
        plt.close()
        images.append(path)

    return images


def main():
    log("=== TPS PDF REPORT — START ===")

    if not os.path.exists(DATA_CSV):
        log(f"❌ CSV introuvable : {DATA_CSV}")
        return

    df = pd.read_csv(DATA_CSV)

    # Détection souple des colonnes (FR / EN)
    revenue_col     = find_column(["total_revenue", "revenue", "CA_total", "ca_total", "sales_revenue", "revenue_eur"], df)
    margin_col      = find_column(["total_margin", "margin", "marge", "profit", "profit_eur"], df)
    margin_rate_col = find_column(["margin_rate", "margin_pct", "marge_pct"], df)
    stock_col       = find_column(["stock", "inventory_quantity", "available", "Stock", "stock_total"], df)
    category_col    = find_column(["category", "categorie", "collection", "category_name"], df)
    title_col       = find_column(["title", "Title", "product_title"], df) or df.columns[0]

    # === KPI principaux ===
    ca_total     = float(df[revenue_col].sum()) if revenue_col else 0.0
    marge_totale = float(df[margin_col].sum()) if margin_col else 0.0
    if margin_rate_col:
        marge_pct = float(df[margin_rate_col].mean())
    else:
        marge_pct = (marge_totale / ca_total * 100) if ca_total else 0.0

    # Stock faible : quartile bas
    low_stock_count = 0
    low_stock_sample = []
    if stock_col:
        low_mask = df[stock_col] > 0
        low_mask &= df[stock_col] <= df[stock_col].quantile(0.25)
        low_df = df[low_mask]
        low_stock_count = int(low_df.shape[0])
        for _, row in low_df.head(10).iterrows():
            low_stock_sample.append(
                (str(row[title_col])[:40], int(row[stock_col]))
            )

    # Top produits par marge
    top_products = []
    if margin_col:
        for _, row in df.sort_values(margin_col, ascending=False).head(5).iterrows():
            top_products.append(
                (
                    str(row[title_col])[:40],
                    float(row[margin_col]),
                    int(row[stock_col]) if stock_col else None,
                )
            )

    # === Construction du PDF ===
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
        title="TPS Daily Business KPI Report",
        author="TPS Automation Bot",
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitleTPS",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=PRIMARY,
        alignment=1,
        spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=ACCENT,
        spaceBefore=12,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK,
    ))

    story = []

    # Logo + titre
    try:
        logo = Image(LOGO_URL, width=4 * cm, height=2.2 * cm)
        logo.hAlign = "CENTER"
        story.append(logo)
        story.append(Spacer(1, 0.3 * cm))
    except Exception:
        pass

    story.append(Paragraph("TPS — Daily Business KPI Report", styles["TitleTPS"]))
    story.append(Paragraph(
        datetime.now().strftime("Report generated on %d %B %Y — %H:%M"),
        styles["Body"],
    ))
    story.append(Spacer(1, 0.4 * cm))

    # === Executive summary ===
    story.append(Paragraph("Executive Summary", styles["SectionHeader"]))

    bullets = [
        f"<b>Revenu total</b> : {ca_total:,.2f} €",
        f"<b>Marge totale</b> : {marge_totale:,.2f} €",
        f"<b>Taux de marge moyen</b> : {marge_pct:,.1f} %",
    ]
    if low_stock_count:
        bullets.append(f"<b>Produits avec stock sensible</b> : {low_stock_count}")
    if top_products:
        bullets.append(f"<b>Top performer marge</b> : {top_products[0][0]}")

    for b in bullets:
        story.append(Paragraph(f"• {b}", styles["Body"]))
    story.append(Spacer(1, 0.4 * cm))

    # Tableau KPI
    kpi_data = [
        ["KPI", "Valeur"],
        ["Revenu total", f"{ca_total:,.2f} €"],
        ["Marge totale", f"{marge_totale:,.2f} €"],
        ["Taux de marge moyen", f"{marge_pct:,.1f} %"],
        ["Nb produits stock sensible", str(low_stock_count)],
    ]
    kpi_table = Table(kpi_data, colWidths=[8 * cm, 6 * cm], hAlign="LEFT")
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("BACKGROUND", (0, 1), (-1, -1), BG_LIGHT),
        ("TEXTCOLOR", (0, 1), (-1, -1), TEXT_DARK),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.5 * cm))

    # === Top produits par marge ===
    if top_products:
        story.append(Paragraph("Top Products by Margin", styles["SectionHeader"]))
        tp_data = [["Produit", "Marge (€)", "Stock"]]
        for name, margin_value, stock_value in top_products:
            tp_data.append([name, f"{margin_value:,.2f}", "" if stock_value is None else str(stock_value)])

        tp_table = Table(tp_data, colWidths=[9 * cm, 4 * cm, 1.5 * cm])
        tp_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("TEXTCOLOR", (0, 1), (-1, -1), TEXT_DARK),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(tp_table)
        story.append(Spacer(1, 0.5 * cm))

    # === Watchlist stock faible ===
    if low_stock_sample:
        story.append(Paragraph("Low Stock Watchlist", styles["SectionHeader"]))
        ls_data = [["Produit", "Stock"]]
        for name, stk in low_stock_sample:
            ls_data.append([name, str(stk)])

        ls_table = Table(ls_data, colWidths=[11 * cm, 3 * cm])
        ls_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#b8403b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("TEXTCOLOR", (0, 1), (-1, -1), TEXT_DARK),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(ls_table)
        story.append(PageBreak())

    # === Graphiques ===
    story.append(Paragraph("Visual KPIs", styles["SectionHeader"]))
    chart_paths = build_charts(df, revenue_col, margin_col, stock_col, category_col)
    for path in chart_paths:
        img = Image(path, width=15 * cm, height=7 * cm)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 0.4 * cm))

    # === Conclusions et Next Steps ===
    story.append(PageBreak())
    story.append(Paragraph("Conclusions & Next Steps", styles["SectionHeader"]))

    # Insights
    insights = []
    if ca_total > 0:
        insights.append(
            f"Current cumulative revenue reaches <b>{ca_total:,.0f} €</b> "
            f"with an average margin of <b>{marge_pct:,.1f} %</b>."
        )
    if low_stock_count > 0:
        insights.append(
            f"<b>{low_stock_count}</b> variants are in a low stock zone — "
            "risk of lost sales on best-performing items."
        )
    if top_products:
        insights.append(
            f"Top-margin products are strong profit drivers; "
            f"<b>{top_products[0][0]}</b> should stay in focus for campaigns."
        )

    story.append(Paragraph("<b>Key Insights</b>", styles["Body"]))
    for c in insights:
        story.append(Paragraph(f"• {c}", styles["Body"]))
    story.append(Spacer(1, 0.3 * cm))

    # Next steps
    steps = [
        "Review and confirm replenishment orders for low-stock best-sellers in the next 24–48 hours.",
        "Push top-margin products into Meta / Google Ads and highlight them on the homepage & hero banner.",
        "Monitor margin by category to detect pricing / sourcing optimisation opportunities.",
    ]
    story.append(Paragraph("<b>Recommended Next Steps</b>", styles["Body"]))
    for s in steps:
        story.append(Paragraph(f"• {s}", styles["Body"]))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph(
        "Official TPS Automation Report — crafted for precision, performance & storytelling 🐾",
        styles["Body"],
    ))

    # Build final PDF
    doc.build(story)

    log(f"✔ PDF généré : {PDF_OUTPUT}")
    log("=== TPS PDF REPORT — END ===")


if __name__ == "__main__":
    main()
