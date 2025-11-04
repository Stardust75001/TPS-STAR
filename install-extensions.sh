#!/usr/bin/env bash
set -euo pipefail

# Tentatives avec fallback pour quelques extensions dont l'ID peut varier
code --list-extensions >/dev/null 2>&1 || { echo "Le CLI 'code' n'est pas disponible dans le PATH. Ouvre VS Code et active 'Install code command in PATH'."; exit 1; }

# installe avec fallback pour GitLens
code --install-extension eamodio.gitlens || code --install-extension gitkraken.gitlens || echo "GitLens not found on marketplace"

# installations simples
code --install-extension mhutchie.git-graph
code --install-extension GitHub.vscode-pull-request-github
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension christian-kohler.path-intellisense
code --install-extension humao.rest-client || echo "humao.rest-client failed"

# Theme Check (fallback name variants)
code --install-extension Shopify.theme-check || code --install-extension shopify.theme-check || echo "Shopify Theme Check not found"

# Liquid syntax (fallbacks)
code --install-extension neild3r.liquid || code --install-extension sissel.shopify-liquid || echo "Liquid extension not found"

echo "Done. Vérifie les extensions installées avec: code --list-extensions"
