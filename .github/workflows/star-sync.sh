#!/bin/zsh
# ============================================================
# 🦅 TPS STAR SYNC (v3)
# Sync "TPS STAR" → branch DEV (+ optional Shopify push)
# Options:
#   --dry-run        : does not write (rsync/commit/push simulated)
#   --no-delete      : does not delete missing files on repo side

set -e

DRY_RUN=0
NO_DELETE=0

for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=1 ;;
    --no-delete) NO_DELETE=1 ;;
  esac
done

REPO_DIR="/Users/asc/Shopify/TPS STAR/TPS-STAR-WORKTREE"
SRC_DIR="/Users/asc/Shopify/TPS STAR/TPS-STAR-SOURCE"

echo "🦅 TPS STAR SYNC"
echo "Source: $SRC_DIR"
echo "Repo:   $REPO_DIR"
echo "Options: dry-run=$DRY_RUN, no-delete=$NO_DELETE"

RSYNC_OPTS="-avh --exclude='.git' --exclude='node_modules'"
if [[ $NO_DELETE -eq 0 ]]; then
  RSYNC_OPTS="$RSYNC_OPTS --delete"
fi
if [[ $DRY_RUN -eq 1 ]]; then
  RSYNC_OPTS="$RSYNC_OPTS --dry-run"
fi

echo "🔄 Rsync files..."
rsync $RSYNC_OPTS "$SRC_DIR/" "$REPO_DIR/"

if [[ $DRY_RUN -eq 1 ]]; then
  echo "✅ Dry run complete. No files written."
  exit 0
fi

cd "$REPO_DIR"

echo "🔄 Git add/commit/push to DEV branch..."
git checkout DEV
git add .
git commit -m "🔄 Sync from TPS STAR source"
git push origin DEV

echo "✅ Repo sync complete."

# Optional: Shopify theme push (uncomment if needed)
# echo "🚀 Pushing theme to Shopify..."
# shopify theme push

echo "🎉 TPS STAR sync finished."
