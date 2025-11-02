#!/usr/bin/env bash
set -euo pipefail
echo "🔄 Synchronisation de la branche MAIN avec GitHub..."

# 1️⃣ Sauvegarde locale temporaire
echo "🧳 Sauvegarde temporaire des modifications locales..."
git add -A >/dev/null 2>&1 || true
git stash push -m "🧩 sauvegarde auto avant sync MAIN" >/dev/null 2>&1 || echo "ℹ️ Rien à sauvegarder."

# 2️⃣ Récupération distante
echo "📥 Récupération de origin/main..."
git fetch origin

# 3️⃣ Rebase pour garder l’historique propre
echo "🧠 Rebase sur origin/main..."
git rebase origin/main || {
  echo "⚠️ Conflits détectés — résous-les puis fais : git rebase --continue"
  exit 1
}

# 4️⃣ Restauration du stash
echo "📦 Restauration des changements sauvegardés..."
git stash pop >/dev/null 2>&1 || echo "✅ Aucun stash à restaurer."

# 5️⃣ Validation finale
echo "📝 Commit des fichiers restants..."
git add -A
git commit -m "sync: alignement complet avec origin/main ($(date '+%Y-%m-%d %H:%M'))" || echo "ℹ️ Rien à commit."

# 6️⃣ Push final
echo "🚀 Push vers GitHub..."
git push origin main

echo "✅ Synchronisation MAIN terminée sans conflit 🎉"
