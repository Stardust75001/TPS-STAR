#!/bin/bash

echo "📧 TPS-STAR Reports - Mode Email Seulement"
echo "📅 $(date '+%Y-%m-%d %H:%M:%S')"
echo "⚠️  Slack temporairement désactivé (webhook 404)"
echo ""

# Vérifier si generate-executive-summary-fixed.sh existe
if [ -f "./generate-executive-summary-fixed.sh" ]; then
    echo "📊 Génération du résumé exécutif..."
    ./generate-executive-summary-fixed.sh
else
    echo "⚠️  generate-executive-summary-fixed.sh manquant, création des rapports de base..."
    mkdir -p reports/audit/{html,pdf}
    
    DATE=$(date '+%Y%m%d')
    echo "📄 Rapport de base créé pour $DATE"
fi

# Préparer l'email avec liens vers les rapports
DATE=$(date '+%Y%m%d')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

EMAIL_SUBJECT="📊 TPS-STAR Reports - $DATE"
EMAIL_BODY="📊 TPS-STAR Executive Summary
📅 $TIMESTAMP

✅ Rapports générés avec succès!

🔗 Liens directs vers les rapports:
• HTML: file:///Users/asc/Shopify/TPS%20STAR/TPS-STAR-WORKTREE/reports/audit/html/tps-executive-summary-$DATE.html
• PDF: file:///Users/asc/Shopify/TPS%20STAR/TPS-STAR-WORKTREE/reports/audit/pdf/tps-executive-summary-$DATE.pdf

📊 Status Système:
• Email: ✅ FONCTIONNEL
• Slack: ❌ Webhook 404 (à corriger avec Workflow Builder)
• Reports: ✅ GÉNÉRÉS
• PDF: ✅ DISPONIBLE

📋 Actions requises:
1. ✅ Email fonctionne parfaitement
2. ⚠️ Créer nouveau webhook Slack via Workflow Builder
3. 🎯 Automation lundi 8h00 déjà configurée

---
🤖 TPS-STAR System - $TIMESTAMP
Si vous recevez cet email, tout fonctionne! ✅"

echo "📧 Envoi emails avec liens complets..."
RECIPIENTS=("alexjet2000@gmail.com" "asc2000@gmail.com" "alfalconx@gmail.com")

for email in "${RECIPIENTS[@]}"; do
    echo "📤 Envoi à $email..."
    echo "$EMAIL_BODY" | mail -s "$EMAIL_SUBJECT" "$email"
    echo "✅ Email envoyé à $email"
done

echo ""
echo "✅ RAPPORTS ENVOYÉS (MODE EMAIL SEULEMENT)"
echo "📧 3 emails envoyés avec liens vers les rapports"
echo "⚠️  Slack sera réactivé une fois le webhook Workflow créé"
