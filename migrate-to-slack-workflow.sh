#!/bin/bash

echo "🔄 Migration vers Slack Workflow"
echo "================================"
echo ""

# Demander le nouveau webhook URL
read -p "🔗 Entrez votre nouveau webhook URL Slack Workflow: " NEW_WEBHOOK_URL

if [ -z "$NEW_WEBHOOK_URL" ]; then
    echo "❌ URL requise pour continuer"
    exit 1
fi

# Tester le nouveau webhook
echo "🧪 Test du nouveau webhook..."
TEST_RESULT=$(curl -X POST \
  -H "Content-type: application/json" \
  -d '{
    "text": "🎯 Migration TPS-STAR - Test webhook workflow"
  }' \
  "$NEW_WEBHOOK_URL" \
  --write-out "%{http_code}" \
  --silent --output /dev/null)

if [ "$TEST_RESULT" = "200" ]; then
    echo "✅ Nouveau webhook fonctionne!"
    
    # Backup et mise à jour
    echo "💾 Sauvegarde des fichiers originaux..."
    
    OLD_WEBHOOK="https://hooks.slack.com/services/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"
    
    # Fichiers à mettre à jour
    FILES=(
        "debug-email-slack.sh"
        "tps-production-ready.sh"
        "tps-dashboard.sh"
    )
    
    for file in "${FILES[@]}"; do
        if [ -f "$file" ]; then
            # Backup
            cp "$file" "$file.pre-workflow-backup"
            
            # Remplacer l'URL
            sed -i.tmp "s|$OLD_WEBHOOK|$NEW_WEBHOOK_URL|g" "$file"
            rm -f "$file.tmp"
            
            echo "✅ Mis à jour: $file"
        fi
    done
    
    echo ""
    echo "🎉 MIGRATION RÉUSSIE!"
    echo "🧪 Test avec: TPSDEBUG"
    
else
    echo "❌ Nouveau webhook ne fonctionne pas (status: $TEST_RESULT)"
fi
