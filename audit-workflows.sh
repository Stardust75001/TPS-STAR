#!/bin/bash
set -euo pipefail

# === CONFIGURATION ===
WORKDIR="$HOME/Shopify/TPS-STAR-WORKTREE"
REPORT_DIR="$WORKDIR/rapports/Workflows"
mkdir -p "$REPORT_DIR"

TIMESTAMP=$(date "+%Y-%m-%d_%H-%M-%S")
REPORT_FILE="$REPORT_DIR/audit-workflows-$TIMESTAMP.csv"

echo "🔎 Checking all workflows in $WORKDIR/.github/workflows..."
cd "$WORKDIR/.github/workflows"

# === STEP 1 — Launch all workflows with 'workflow_dispatch' ===
for wf in *.yml; do
  if grep -q "workflow_dispatch" "$wf"; then
    echo "🚀 Dispatching $wf..."
    gh workflow run "$wf" --ref DEV >/dev/null 2>&1 || echo "⚠️ Failed to start $wf"
  else
    echo "⛔ Skipping $wf (no workflow_dispatch trigger)"
  fi
done

# === STEP 2 — Wait for GitHub Actions to queue ===
echo "⏳ Waiting 90 seconds for runs to start..."
sleep 90

# === STEP 3 — Fetch run status summary ===
echo "📋 Compiling results..."
{
  echo "Workflow Name,Status,Conclusion"
  gh run list --limit 50 --json name,status,conclusion,workflowName \
  | jq -r '.[] | "\(.workflowName),\(.status),\(.conclusion)"'
} > "$REPORT_FILE"

# === STEP 4 — Pretty print summary in terminal ===
echo -e "\n📊 Summary of latest runs:\n"
awk -F',' 'NR>1 {
  emoji = ($3=="success"?"✅":($3=="failure"?"❌":($3=="neutral"?"⚪":"⚙️")))
  printf "%-50s → %s %s\n", $1, emoji, $3
}' "$REPORT_FILE"

echo -e "\n✅ Résumé exporté → $REPORT_FILE"
