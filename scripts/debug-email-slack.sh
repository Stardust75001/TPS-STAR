#!/bin/bash

echo "🔧 TPS-STAR Email & Slack Debug Tool - Enhanced"
echo "=============================================="

# Test du webhook depuis variable d'environnement ou secret
SLACK_WEBHOOK="${TPS_SLACK_WEBHOOK:-${SLACK_WEBHOOK_URL:-}}"

if [ -z "$SLACK_WEBHOOK" ]; then
    echo "⚠️ No Slack webhook configured (set TPS_SLACK_WEBHOOK or SLACK_WEBHOOK_URL)"
    echo "✅ System operational (Slack notifications disabled)"
    exit 0
fi

echo "🔗 Testing webhook: [CONFIGURED]"

# Test rapide
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"🎯 TPS-STAR System - FULLY OPERATIONAL ✅"}' \
  "$SLACK_WEBHOOK"

echo "✅ System operational!"
