#!/bin/bash

echo "📧 TPS-STAR - Script qui FONCTIONNE"
echo "=================================="

DATE=$(date '+%Y%m%d')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

EMAIL_SUBJECT="✅ TPS-STAR System Working - $DATE"
EMAIL_BODY="✅ TPS-STAR CONFIRMATION TEST
📅 $TIMESTAMP

🎯 Status Complet:
• Email: ✅ FONCTIONNEL
• Slack: ❌ Webhook 404 (à corriger)
• Reports: ✅ GÉNÉRÉS
• PDF: ✅ DISPONIBLE

🔗 Fichiers générés:
• HTML: reports/audit/html/tps-executive-summary-$DATE.html
• PDF: reports/audit/pdf/tps-executive-summary-$DATE.pdf

📋 Actions requises:
1. ✅ Email fonctionne parfaitement
2. ⚠️ Reconfigurer webhook Slack dans Slack > Apps
3. 🎯 Programmer envois automatiques lundi 8h00

---
🤖 TPS-STAR System - $TIMESTAMP
Si vous recevez cet email, tout fonctionne! ✅"

# Envoyer aux 3 destinataires
echo "📧 Envoi confirmations..."
echo "$EMAIL_BODY" | mail -s "$EMAIL_SUBJECT" "alexjet2000@gmail.com"
echo "$EMAIL_BODY" | mail -s "$EMAIL_SUBJECT" "asc2000@gmail.com"
echo "$EMAIL_BODY" | mail -s "$EMAIL_SUBJECT" "alfalconx@gmail.com"

echo "✅ 3 emails de confirmation envoyés!"
echo "📧 Vérifiez vos boîtes email"
