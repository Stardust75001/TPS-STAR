#!/bin/bash
# Download weekly reports to reports-metrics folder

REPORTS_DIR="/Users/asc/Shopify/TPS STAR/TPS-STAR-WORKTREE/reports - metrics"
DATE=$(date +%Y%m%d)
DATETIME=$(date +%Y%m%d-%H%M)

# Create date-specific folder
mkdir -p "$REPORTS_DIR/$DATETIME"

# Get the latest workflow run ID for the weekly analytics report
echo "🔍 Finding latest workflow run..."
RUN_ID=$(gh run list --workflow="weekly-analytics-report.yml" --limit 1 --json databaseId --jq '.[0].databaseId')

if [ -z "$RUN_ID" ]; then
    echo "❌ No workflow runs found"
    exit 1
fi

echo "📥 Downloading artifacts from run $RUN_ID to $REPORTS_DIR/$DATETIME"

# Try both artifact naming patterns
gh run download "$RUN_ID" --name "weekly-report-metrics-*" --dir "$REPORTS_DIR/$DATETIME" 2>/dev/null || \
gh run download "$RUN_ID" --name "weekly-report-artifacts" --dir "$REPORTS_DIR/$DATETIME" || \
gh run download "$RUN_ID" --dir "$REPORTS_DIR/$DATETIME"

echo "✅ Download complete. Files available in: $REPORTS_DIR/$DATETIME"
find "$REPORTS_DIR/$DATETIME" -type f -name "*.pdf" -o -name "*.html" -o -name "*.png" | head -10

# Open the main PDF if it exists
PDF_FILE=$(find "$REPORTS_DIR/$DATETIME" -name "*.pdf" | head -1)
if [ -n "$PDF_FILE" ]; then
    echo "📖 Opening PDF: $PDF_FILE"
    open "$PDF_FILE"
fi
