#!/usr/bin/env bash
set -euo pipefail

LC_ALL=C
STAR="$HOME/Shopify/TPS-STAR-WORKTREE"
EXPORT_DIR="$STAR/exports"
mkdir -p "$EXPORT_DIR"

timestamp="$(date +"%Y%m%d-%H%M")"
report="$EXPORT_DIR/branch-cleaner-$timestamp.csv"

# Header du CSV
echo "branch,status,reason,last_commit,date" > "$report"

echo "🧹 TPS-STAR — Branch Cleaner (mode interactif)"
echo "──────────────────────────────────────────────"
echo ""

# Branches protégées (jamais supprimées)
PROTECTED=(
  "main"
  "DEV"
  "SANDBOX"
)

# Fonction pour vérifier protection
is_protected() {
  local b="$1"
  for p in "${PROTECTED[@]}"; do
    [[ "$b" == "$p" ]] && return 0
  done
  return 1
}

# Récupérer toutes les branches locales
branches=$(git for-each-ref --format="%(refname:short)" refs/heads/)

for branch in $branches; do
  # Protection
  if is_protected "$branch"; then
    echo "🔒 $branch — protégé (ignoré)"
    continue
  fi

  # Dernier commit
  commit="$(git rev-parse "$branch")"
  info="$(git log -1 --pretty="%h|%ci|%s" "$branch" 2>/dev/null || echo "none|none|none")"

  hash="$(echo "$info" | cut -d'|' -f1)"
  date="$(echo "$info" | cut -d'|' -f2)"
  msg="$(echo "$info" | cut -d'|' -f3)"

  # Détecter remote tracking
  if git rev-parse --symbolic-full-name "$branch@{upstream}" >/dev/null 2>&1; then
    remote="yes"
  else
    remote="no"
  fi

  # Détecter si c'est une branche backup/fantôme
  reason="active"
  if [[ "$branch" == backup-* ]] \
     || [[ "$branch" == save/* ]] \
     || [[ "$branch" == *before-forcepush* ]] \
     || [[ "$remote" == "no" ]]; then
    reason="cleanup_candidate"
  fi

  if [[ "$reason" != "cleanup_candidate" ]]; then
    echo "✔️  $branch — active"
    continue
  fi

  echo ""
  echo "⚠️  Branche trouvée : $branch"
  echo "    Dernier commit : $hash"
  echo "    Date           : $date"
  echo "    Message        : $msg"
  echo "    Remote         : $remote"
  echo ""

  # Confirmation
  read -rp "Supprimer cette branche ? (y/N) " confirm

  if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
    git branch -D "$branch"
    echo "🗑️  $branch supprimée"
    echo "$branch,deleted,$reason,$hash,$date" >> "$report"
  else
    echo "⏭️  $branch conservée"
    echo "$branch,kept,$reason,$hash,$date" >> "$report"
  fi
done

echo ""
echo "📄 Rapport CSV généré : $report"
echo "✨ Nettoyage terminé."
