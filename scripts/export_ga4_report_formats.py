import json
import pandas as pd
from fpdf import FPDF

output_path = "rapports/ga4-report-20251109.json"  # ⚠️ adapte dynamiquement si besoin

# Charger les données JSON
with open(output_path, "r") as f:
    data = json.load(f)

# Convertir en DataFrame
df = pd.DataFrame(data.get("rows", []))

# Export CSV
csv_path = output_path.replace('.json', '.csv')
df.to_csv(csv_path, index=False)

# Export PDF
pdf_path = output_path.replace('.json', '.pdf')
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=10)
for index, row in df.iterrows():
    row_data = ", ".join(f"{k}: {v}" for k, v in row.items())
    pdf.multi_cell(0, 10, txt=row_data)
pdf.output(pdf_path)
