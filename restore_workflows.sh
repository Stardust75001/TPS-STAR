#!/usr/bin/env bash
set -euo pipefail

# Se placer dans le worktree
cd ~/Shopify/TPS-STAR-WORKTREE

echo "📦 Restauration des workflows GitHub..."

# Liste des commits à restaurer (du plus récent au plus ancien)
declare -a commits=(
    "f400ad42"
    "3c55766b"
    "b2c7a81c"
    "2bb6f50f"
    "2de3d64b"
    "952a4dc8"
    "dc664d69"
    "7479255e"
    "19b3cc8f"
    "da726a51"
    "497bb01e"
    "73cf78d5"
    "3b30d72f"
    "31e57694"
    "50bf236e"
    "e6379345"
    "c81f9f9d"
    "315efd76"
    "1595e127"
    "07c6e2f7"
    "2dd74224"
    "61a6d6a5"
    "4e95c223"
    "7fd7329b"
    "45506f98"
    "964e017b"
    "8f6feecd"
    "36a627cc"
    "2f407709"
    "f5821eed"
    "0b001736"
    "244cd3a4"
    "13798c8a"
    "c5098cd3"
    "aba2a0b7"
    "89732234"
)

# Pour chaque commit, restaurer tous les fichiers workflows du commit
for c in "${commits[@]}"; do
    echo "⏳ Restauration depuis commit $c ..."
    git checkout "$c" -- .github/workflows/
done

echo "✅ Tous les workflows ont été restaurés depuis les commits listés."
echo "💡 N'oublie pas de vérifier avec 'git status' et de faire un 'git add' + 'git commit' pour enregistrer les fichiers restaurés."
