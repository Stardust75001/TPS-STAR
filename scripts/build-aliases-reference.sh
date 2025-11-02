#!/usr/bin/env bash
set -euo pipefail
OUT="$HOME/Shopify/TPS-STAR-WORKTREE/docs/ALIASES-REFERENCE.md"
TS="$(date +'%Y-%m-%d %H:%M:%S')"
mkdir -p "$(dirname "$OUT")"

{
  echo "# 🧠 TPS — Aliases ZSH (Référence)"
  echo "_Généré automatiquement le ${TS}_"
  echo
  echo "## 🔗 Fichier source"
  echo "\`~/.aliases\`"
  echo

  echo "## 📌 Aliases"
  echo
  if [ -f "$HOME/.aliases" ]; then
    grep -E "^[[:space:]]*alias[[:space:]]+[A-Za-z0-9_+-]+=" "$HOME/.aliases" \
      | sed 's/^/```bash\n/; s/$/\n```/' || true
  else
    echo "_~/.aliases introuvable._"
  fi

  echo
  echo "## ⚙️ Fonctions (signatures)"
  echo
  if [ -f "$HOME/.aliases" ]; then
    grep -nE "^[[:space:]]*[A-Za-z0-9_+-]+[[:space:]]*\(\)[[:space:]]*\{" "$HOME/.aliases" \
      | sed -E 's/^/ - /; s/\{.*$//' || true
  fi

  echo
  echo "<sub>© Falcon Trading Company — document généré.</sub>"
} > "$OUT"

echo "✅ Aliases Reference générée : $OUT"
