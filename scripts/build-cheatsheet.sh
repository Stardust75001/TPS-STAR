#!/bin/zsh
set -e

TARGET_DIR="$HOME/Shopify/TPS-STAR-WORKTREE/CheatSheet"
OUTPUT_MD="$TARGET_DIR/tps_alias_cheatsheet.md"
OUTPUT_HTML="$TARGET_DIR/tps_alias_cheatsheet.html"
OUTPUT_PDF="$TARGET_DIR/TPS_STAR_Cheatsheet_Aliases.pdf"
WORKFLOWS_DIR="$HOME/Shopify/TPS-STAR-WORKTREE/.github/workflows"

mkdir -p "$TARGET_DIR"

echo "📘 Génération du PDF Cheatsheet TPS (WeasyPrint)..."

# === CONTENU MARKDOWN ===
cat <<'MARKDOWN' > "$OUTPUT_MD"
# 🧭 TPS STAR — Cheatsheet CLI & Workflows  
**Auteur :** THE PET SOCIETY  
**Date :** $(date '+%d %B %Y à %Hh%M')

---

## 🚀 Raccourcis CLI

| **Alias** | **Description** |
|------------|----------------|
| TPSSTAR | Ouvre le projet THE PET SOCIETY |
| TPSDEV | Bascule sur la branche DEV et met à jour |
| TPSBATCHWORKFLOW | Lance tous les workflows GitHub avec audit |
| TPSSYNC | Synchronise tous les fichiers de langue Shopify |
| TPSDOCS | Ouvre la documentation locale des alias |
| TPSREPORTS | Ouvre le dossier des rapports GitHub Actions |
| TPSGIT | Affiche l’état Git actuel du worktree |
| TPSFIX | Force la resynchronisation complète du thème |

---
MARKDOWN

# === WORKFLOWS ===
echo "## ⚙️ Workflows GitHub actifs\n" >> "$OUTPUT_MD"

if [ -d "$WORKFLOWS_DIR" ]; then
  WORKFLOWS=$(ls "$WORKFLOWS_DIR"/*.yml 2>/dev/null || true)
  if [ -n "$WORKFLOWS" ]; then
    echo "| **Fichier** | **Dernière modification** | **Description (auto)** |" >> "$OUTPUT_MD"
    echo "|-------------|----------------------------|--------------------------|" >> "$OUTPUT_MD"
    for wf in $WORKFLOWS; do
      name=$(basename "$wf")
      mod_date=$(date -r "$wf" "+%d/%m/%Y %H:%M")
      desc=$(grep -m1 '^#' "$wf" | sed 's/^# *//;s/|/\\|/g')
      [ -z "$desc" ] && desc="(Aucune description trouvée)"
      echo "| $name | $mod_date | $desc |" >> "$OUTPUT_MD"
    done
  else
    echo "_Aucun workflow trouvé._" >> "$OUTPUT_MD"
  fi
else
  echo "_Dossier workflows introuvable._" >> "$OUTPUT_MD"
fi

# === PIED DE PAGE ===
cat <<FOOT >> "$OUTPUT_MD"

---

**Généré automatiquement le $(date '+%d %B %Y à %Hh%M')**  
**THE PET SOCIETY — Workflow & DevOps Aliases**
FOOT

# === CONVERSION MARKDOWN → HTML → PDF ===
python3 - <<PYCODE
import markdown, weasyprint, pathlib
md_file = pathlib.Path("$OUTPUT_MD")
html_file = pathlib.Path("$OUTPUT_HTML")
pdf_file = pathlib.Path("$OUTPUT_PDF")

html = markdown.markdown(md_file.read_text(encoding="utf-8"), extensions=["tables"])
html_content = f"""
<html>
<head>
<meta charset="utf-8">
<style>
body {{
  font-family: "Helvetica", sans-serif;
  margin: 2cm;
}}
h1, h2, h3 {{ color: #0f6378; }}
table {{
  width: 100%;
  border-collapse: collapse;
  margin-top: 1em;
}}
th, td {{
  border: 1px solid #ccc;
  padding: 6px 10px;
  font-size: 12px;
}}
th {{ background: #eaeaea; }}
footer {{
  margin-top: 2em;
  text-align: center;
  font-size: 10px;
  color: #666;
}}
</style>
</head>
<body class="markdown-body">{html}</body>
</html>
"""
html_file.write_text(html_content, encoding="utf-8")
weasyprint.HTML(string=html_content).write_pdf(pdf_file)
print(f"✅ Cheatsheet PDF générée : {pdf_file}")
print(f"📂 Ouvrir : open {pdf_file}")
PYCODE
