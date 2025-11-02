#!/usr/bin/env bash
set -euo pipefail
echo "🔄 Synchronisation de la branche DEV avec GitHub..."

# 1️⃣ Sauvegarde locale temporaire
echo "🧳 Sauvegarde temporaire des modifications locales..."
git add -A >/dev/null 2>&1 || true
git stash push -m "🧩 sauvegarde auto avant sync DEV" >/dev/null 2>&1 || echo "ℹ️ Rien à sauvegarder."

# 2️⃣ Récupération distante
echo "📥 Récupération de origin/DEV..."
git fetch origin

# 3️⃣ Rebase pour garder l’historique propre
echo "🧠 Rebase sur origin/DEV..."
git rebase origin/DEV || {
  echo "⚠️ Conflits détectés — résous-les puis fais : git rebase --continue"
  exit 1
}

# 4️⃣ Restauration du stash
echo "📦 Restauration des changements sauvegardés..."
git stash pop >/dev/null 2>&1 || echo "✅ Aucun stash à restaurer."

# 5️⃣ Validation finale
echo "📝 Commit des fichiers restants..."
git add -A
git commit -m "sync: alignement complet avec origin/DEV ($(date '+%Y-%m-%d %H:%M'))" || echo "ℹ️ Rien à commit."

# 6️⃣ Push final
echo "🚀 Push vers GitHub..."
git push origin DEV

echo "✅ Synchronisation DEV terminée sans conflit 🎉"
