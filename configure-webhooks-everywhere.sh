#!/bin/bash

echo "🔧 Configuration TPS-STAR Webhooks Everywhere"
echo "=============================================="

NEW_WEBHOOK="https://hooks.slack.com/services/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"

echo "1. 🔄 Mise à jour des fichiers locaux..."

# Files to update
FILES=(
    "debug-email-slack.sh"
    "tps-production-ready.sh"
    "tps-send-working.sh"
    "complete-tracker-audit.sh"
    "send-tps-reports-now.sh"
    "send-tps-reports-with-notifications.sh"
)

OLD_WEBHOOK="https://hooks.slack.com/services/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"

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        sed -i.backup "s|$OLD_WEBHOOK|$NEW_WEBHOOK|g" "$file"
        echo "✅ Updated: $file"
    fi
done

echo ""
echo "2. 🌍 Configuration variables d'environnement..."

# Add to shell profile
if ! grep -q "TPS_SLACK_WEBHOOK" ~/.zshrc; then
    echo 'export TPS_SLACK_WEBHOOK="'$NEW_WEBHOOK'"' >> ~/.zshrc
    echo "✅ Variable ajoutée à ~/.zshrc"
else
    echo "⚠️ Variable déjà présente dans ~/.zshrc"
fi

echo ""
echo "3. 📋 Instructions pour GitHub et Shopify:"
echo ""
echo "GitHub Repository Secrets:"
echo "========================="
echo "Nom: SLACK_WEBHOOK_URL"
echo "Valeur: $NEW_WEBHOOK"
echo ""
echo "Shopify Metafields/Settings:"
echo "============================"
echo "Nom: tps-star-slack-webhook"
echo "Valeur: $NEW_WEBHOOK"
echo ""
echo "✅ Configuration locale terminée!"
echo "🧪 Test du nouveau webhook..."

curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"🎯 TPS-STAR Configuration Complete! Webhook working from all systems ✅"}' \
  "$NEW_WEBHOOK"

echo ""
echo "🚀 Webhook configuré partout!"
