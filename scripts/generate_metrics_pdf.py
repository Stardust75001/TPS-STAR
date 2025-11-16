import sys
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

input_csv = sys.argv[1]
output_pdf = sys.argv[2]

df = pd.read_csv(input_csv)

# PDF styling — TPS branding
TAUPE = colors.HexColor("#BA986E")
BLACK = colors.HexColor("#1A1A1A")
WHITE = colors.white

doc = SimpleDocTemplate(
    output_pdf,
    pagesize=A4,
    title="TPS Metrics Report"
)

styles = getSampleStyleSheet()
style_header = styles["Title"]
style_header.textColor = BLACK

style_footer = styles["Normal"]
style_footer.textColor = colors.grey

style_table = styles["BodyText"]

elements = []

# Header
elements.append(Paragraph("🐾 THE PET SOCIETY PARIS", style_header))
elements.append(Paragraph("TPS Metrics Health Report — " + datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"), styles["Heading2"]))

# Table
table_data = [df.columns.tolist()] + df.values.tolist()

table = Table(table_data)
table_style = TableStyle([
    ("BACKGROUND", (0,0), (-1,0), TAUPE),
    ("TEXTCOLOR", (0,0), (-1,0), WHITE),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 10),
    ("GRID", (0,0), (-1,-1), 0.25, BLACK),
])

table.setStyle(table_style)
elements.append(table)

# Footer
elements.append(Paragraph("<br/><br/><i>The Pet Society — Parisian Smart Pet Living</i>", style_footer))

doc.build(elements)
