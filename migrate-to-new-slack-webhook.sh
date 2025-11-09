#!/bin/bash

echo "🔧 TPS-STAR Slack Webhook Migration - Automatic"
echo "==============================================="
echo ""

# Nouveau webhook URL
NEW_WEBHOOK_URL="https://hooks.slack.com/services/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"
OLD_WEBHOOK="https://hooks.slack.com/services/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"

echo "🔄 Updating webhook URL in scripts..."
echo "📤 Ancien: ...B09PQBYPV7W/xLgY..."
echo "📥 Nouveau: ...B09QS5Z0EDC/xW1I..."
echo ""

# Files to update
FILES=(
    "debug-email-slack.sh"
    "tps-production-ready.sh" 
    "tps-send-working.sh"
    "complete-tracker-audit.sh"
    "send-tps-reports-now.sh"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        # Backup
        cp "$file" "$file.pre-migration-backup"
        
        # Replace webhook URL
        sed -i.tmp "s|$OLD_WEBHOOK|$NEW_WEBHOOK_URL|g" "$file"
        rm -f "$file.tmp"
        
        echo "✅ Updated: $file"
    else
        echo "⚠️ File not found: $file"
    fi
done

echo ""
echo "🧪 Testing new webhook..."

TEST_PAYLOAD='{"text":"🎉 TPS-STAR Migration Complete! New webhook working perfectly ✅"}'

RESPONSE=$(curl -X POST -H 'Content-type: application/json' \
   --data "$TEST_PAYLOAD" \
   "$NEW_WEBHOOK_URL" \
   --write-out "HTTPSTATUS:%{http_code}" \
   --silent --output /tmp/slack_test.txt)

HTTP_STATUS=$(echo $RESPONSE | grep -o "HTTPSTATUS:.*" | cut -d: -f2)

if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ New webhook working perfectly!"
    echo "🎉 Migration successful - check your Slack channel!"
    echo ""
    echo "📊 Running updated diagnostic..."
    ./debug-email-slack.sh
else
    echo "❌ New webhook test failed (Status: $HTTP_STATUS)"
    echo "Response: $(cat /tmp/slack_test.txt 2>/dev/null)"
fi

rm -f /tmp/slack_test.txt
echo ""
echo "🚀 TPS-STAR is now ready with new Slack webhook!"
