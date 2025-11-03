#!/bin/bash
REPORTS_DIR="/Users/asc/Shopify/TPS STAR/TPS-STAR-WORKTREE/reports - metrics"
DATETIME=$(date +%Y%m%d-%H%M)
mkdir -p "$REPORTS_DIR/$DATETIME"

echo "🔍 Finding latest successful workflow run..."
RUN_ID=$(gh run list --workflow="weekly-analytics-report.yml" --status completed --limit 5 --json databaseId,conclusion | jq -r '.[] | select(.conclusion == "success") | .databaseId' | head -1)

if [ -z "$RUN_ID" ]; then
    echo "❌ No successful workflow runs found"
    exit 1
fi

echo "📋 Available artifacts for run $RUN_ID:"
gh api repos/Stardust75001/TPS-STAR/actions/runs/$RUN_ID/artifacts --jq '.artifacts[] | "\(.name) (expires: \(.expires_at))"'

echo "📥 Downloading all artifacts from run $RUN_ID..."
gh run download "$RUN_ID" --dir "$REPORTS_DIR/$DATETIME"

echo "✅ Downloaded files:"
find "$REPORTS_DIR/$DATETIME" -type f | head -10

# Prioritize weekly/TPS report PDFs over guides
PDF_FILE=$(find "$REPORTS_DIR/$DATETIME" -name "*weekly*report*.pdf" -o -name "*tps*report*.pdf" | head -1)
if [ -z "$PDF_FILE" ]; then
    PDF_FILE=$(find "$REPORTS_DIR/$DATETIME" -name "*.pdf" | head -1)
fi

if [ -n "$PDF_FILE" ]; then
    echo "�� Opening: $PDF_FILE"
    open "$PDF_FILE"
else
    echo "⚠️  No PDF found, but other files are available"
fi
