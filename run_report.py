import os
import json
import csv
from datetime import date
from fpdf import FPDF, XPos, YPos
import subprocess

# Création du dossier rapports
os.makedirs("rapports", exist_ok=True)

today = date.today().strftime("%Y%m%d")

# Exemple de données GA4
data = {"users": 123, "sessions": 456, "bounce_rate": 78.9}

# --- Génération JSON ---
json_file = f"rapports/ga4-report-{today}.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# --- Génération CSV ---
csv_file = f"rapports/ga4-report-{today}.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=data.keys())
    writer.writeheader()
    writer.writerow(data)

# --- Génération PDF ---
pdf_file = f"rapports/ga4-report-{today}.pdf"
pdf = FPDF()
pdf.add_page()

# Charger une police TTF Unicode (DejaVuSans.ttf dans le dossier)
FONT_PATH = "DejaVuSans.ttf"
if not os.path.isfile(FONT_PATH):
    raise FileNotFoundError(f"Font file not found: {FONT_PATH}")

pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
pdf.set_font("DejaVu", size=12)

pdf.cell(0, 10, f"GA4 Daily Report – {today}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 10, f"Users: {data['users']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 10, f"Sessions: {data['sessions']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 10, f"Bounce rate: {data['bounce_rate']}%", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.output(pdf_file)

print(f"✅ GA4 reports generated: {json_file}, {csv_file}, {pdf_file}")

# --- Envoi sur Slack ---
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")
if SLACK_WEBHOOK:
    if os.path.isfile(pdf_file):
        print(f"📤 Sending report {pdf_file} to Slack…")
        subprocess.run([
            "curl",
            "-F", f"file=@{pdf_file}",
            "-F", f"initial_comment=📊 GA4 Daily Report – {today}",
            "-F", "channels=#general",
            SLACK_WEBHOOK
        ])
        print("✅ Report sent to Slack.")
    else:
        print(f"❌ PDF not found: {pdf_file}")
else:
    print("⚠️ SLACK_WEBHOOK not defined. Skipping Slack upload.")
