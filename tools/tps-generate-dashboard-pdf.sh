#!/bin/zsh
set -e

############################################
# 🔧 CONFIG
############################################
SLACK_TOKEN="${SLACK_TOKEN}"

PDF_PATH="/Users/asc/Shopify/TPS STAR/PRODUCTS/STOCK - CATALOG MANAGEMENT/TPS_DASHBOARD_REPORT.pdf"
PY_SCRIPT="/Users/asc/Shopify/TPS STAR/TPS-STAR-WORKTREE/tools/tps_generate_pdf.py"

# Virtualenv TPS
VENV="/Users/asc/Shopify/TPS STAR/TPS-STAR-WORKTREE/.venv/bin/activate"

# Channel Slack (reports)
CHANNEL_ID="C09QS5VMFAA"


############################################
# 🔒 CONFIRMATION SCREEN
############################################
echo "==========================================="
echo "   ⚠️  CONFIRMATION REQUISE — TPS Automation"
echo "Cette action va :"
echo " • Calculer les KPI"
echo " • Générer le PDF Business Corporate + Luxe"
echo " • Envoyer vers Slack (#reports)"
echo " • Logger l’opération"
echo "==========================================="
echo ""

read "CONFIRM?Confirmer ? (yes/no) : "

if [[ "$CONFIRM" != "yes" && "$CONFIRM" != "y" ]]; then
    echo "❌ Annulé."
    exit 0
fi


############################################
# 🧪 Activation du Virtualenv
############################################
if [[ -f "$VENV" ]]; then
    echo "🐍 Activation venv TPS…"
    source "$VENV"
else
    echo "⚠️ Virtualenv introuvable : $VENV"
    echo "   Le script continue avec python3 global."
fi


############################################
# 📄 GÉNÉRATION DU PDF
############################################
echo "📄 Génération du PDF Business KPI…"
python3 "$PY_SCRIPT"


############################################
# 📤 UPLOAD PDF VERS SLACK (nouvelle API)
############################################
if [ -f "$PDF_PATH" ]; then
  echo "📤 Upload du PDF sur Slack (API externe)…"

  # Taille du fichier
  FILE_SIZE=$(stat -f%z "$PDF_PATH")

  # 1) Init upload externe
  INIT_RESP=$(curl -s -X POST https://slack.com/api/files.getUploadURLExternal \
    -H "Content-Type: application/x-www-form-urlencoded" \
    --data-urlencode "token=$SLACK_TOKEN" \
    --data-urlencode "filename=$(basename "$PDF_PATH")" \
    --data-urlencode "length=$FILE_SIZE")

  echo "🔎 Slack getUploadURLExternal → $INIT_RESP"

  UPLOAD_URL=$(echo "$INIT_RESP" | python3 -c 'import sys, json; d=json.load(sys.stdin); print(d.get("upload_url",""))')
  FILE_ID=$(echo "$INIT_RESP" | python3 -c 'import sys, json; d=json.load(sys.stdin); print(d.get("file_id",""))')

  if [ -z "$UPLOAD_URL" ] || [ -z "$FILE_ID" ]; then
    echo "❌ Erreur init upload Slack. Abandon."
    exit 1
  fi

  # 2) Upload binaire
  curl -s -X POST "$UPLOAD_URL" \
    -H "Content-Type: application/octet-stream" \
    --data-binary @"$PDF_PATH" >/dev/null

  # 3) Finalisation → rattachement dans Slack #reports
  COMPLETE_RESP=$(curl -s -X POST https://slack.com/api/files.completeUploadExternal \
    -H "Content-Type: application/json; charset=utf-8" \
    -H "Authorization: Bearer $SLACK_TOKEN" \
    --data "{
      \"files\": [{
        \"id\": \"$FILE_ID\",
        \"title\": \"TPS Daily KPI Dashboard\"
      }],
      \"channel_id\": \"$CHANNEL_ID\"
    }")

  echo "✅ Slack completeUploadExternal → $COMPLETE_RESP"

else
  echo "❌ PDF introuvable, upload Slack impossible."
fi


############################################
# 💬 Message Slack complémentaire
############################################
curl -s -X POST \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  --data "{
      \"channel\": \"reports\",
      \"text\": \"🐾 *TPS Automation – Daily KPI Report Dispatched* 📊🚀\nLe PDF vient d’être envoyé.\n\n*Insights clés :*\n• Revenu total / Marge totale\n• Taux de marge\n• Analyse du stock sensible\n• Top performers & recommandations\n\n_Powered by TPS Automation Bot_ 🤖\"
  }" \
  https://slack.com/api/chat.postMessage >/dev/null


############################################
# 📝 LOGGING FINAL
############################################
echo "$(date '+%Y-%m-%d %H:%M:%S') – Dashboard PDF + Slack OK" >> /var/log/tps/dashboard.log
echo "✅ Fin du script TPS Automation."
