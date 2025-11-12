#!/bin/bash
set -euo pipefail

# === CHARGEMENT VARIABLES ===
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "❌ Fichier .env introuvable."
  exit 1
fi

# === OBTENTION NOUVEAU ACCESS TOKEN ===
echo "🔄 Rafraîchissement du token..."
RESPONSE=$(curl -s -X POST https://oauth2.googleapis.com/token \
  -d client_id="$CLIENT_ID" \
  -d client_secret="$CLIENT_SECRET" \
  -d refresh_token="$REFRESH_TOKEN" \
  -d grant_type=refresh_token)

echo "🔍 Réponse brute : $RESPONSE"

ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r .access_token)

if [ "$ACCESS_TOKEN" == "null" ] || [ -z "$ACCESS_TOKEN" ]; then
  echo "❌ Échec de récupération du token."
  exit 1
fi

echo "✅ Token récupéré avec succès."

# === APPEL API GA4 ===
echo "📊 Récupération des données GA4..."
curl -s -X POST "https://analyticsdata.googleapis.com/v1beta/properties/${GA4_PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
    "metrics": [{"name": "activeUsers"}],
    "dimensions": [{"name": "date"}]
  }' > report_ga4.json

echo "✅ Données enregistrées dans report_ga4.json"
