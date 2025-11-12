#!/bin/bash
set -euo pipefail

ZSHRC="$HOME/.zshrc"

echo "🔧 Installation des alias TPS dans $ZSHRC ..."

# Supprime les anciens blocs si présents
sed -i '' '/# === TPS STAR ALIASES ===/,/# =========================/d' "$ZSHRC"

# Ajoute le bloc d’alias complet
cat <<'ALIASES' >> "$ZSHRC"

# === TPS STAR ALIASES ===
alias TPSSTAR='cd ~/Shopify/TPS-STAR-WORKTREE && echo "📁 Projet THE PET SOCIETY ouvert."'
alias TPSDEV='cd ~/Shopify/TPS-STAR-WORKTREE && git fetch origin DEV && git checkout DEV && echo "🚧 Branche DEV active pour TPS-STAR."'
alias TPSBATCHWORKFLOW='bash ~/Shopify/TPS-STAR-WORKTREE/audit-workflows.sh'
alias TPSSYNC='bash ~/Shopify/TPS-STAR-WORKTREE/scripts/sync-locales.sh'
alias TPSDOCS='open ~/Shopify/TPS-STAR-WORKTREE/docs/ALIASES-REFERENCE.md'
alias TPSREPORTS='open ~/Shopify/TPS-STAR-WORKTREE/rapports/Workflows'
alias TPSGIT='cd ~/Shopify/TPS-STAR-WORKTREE && git status'
alias TPSFIX='cd ~/Shopify/TPS-STAR-WORKTREE && git fetch origin DEV && git reset --hard origin/DEV && git clean -fd && echo "✅ Worktree parfaitement synchronisé."'
# =========================
ALIASES

echo "✅ Aliases TPS ajoutés à ton .zshrc"
echo "💡 Recharge maintenant avec : source ~/.zshrc"

# =============================
# 🧠 TPS-STAR WORKFLOW ALIASES
# =============================

alias TPSRUNVERIFY="gh workflow run '🧠 Verify + Resume + PDF + Slack' --repo Stardust75001/TPS-STAR --ref DEV"
alias TPSWATCH="gh run watch --repo Stardust75001/TPS-STAR"
alias TPSLIST="gh run list --workflow='verify-all-final.yml' --limit 3 --repo Stardust75001/TPS-STAR"
alias TPSLIGHT='gh variable set SLACK_MODE --body "light" --repo Stardust75001/TPS-STAR && echo "🪶 Slack mode: Light (TPS-STAR)"'
alias TPSDARK='gh variable set SLACK_MODE --body "dark" --repo Stardust75001/TPS-STAR && echo "🐾 Slack mode: Dark (TPS)"'
alias TPSCHAIN='TPSDARK && TPSRUNVERIFY && TPSWATCH'
alias TPSCHEAT='bash ~/Shopify/TPS-STAR-WORKTREE/scripts/build-cheatsheet.sh && open ~/Shopify/TPS-STAR-WORKTREE/CheatSheet/TPS_STAR_Cheatsheet_Aliases.pdf'
alias TPSCLEAN='rm -f ~/Shopify/TPS-STAR-WORKTREE/rapports/Workflows/*.csv && echo "🧹 Rapports nettoyés." && TPSCHAIN'

cat >> scripts/register-aliases.sh <<'EOF'

# =============================
# 🧠 TPS-STAR WORKFLOW ALIASES
# =============================

alias TPSRUNVERIFY="gh workflow run '🧠 Verify + Resume + PDF + Slack' --repo Stardust75001/TPS-STAR --ref DEV"
alias TPSWATCH="gh run watch --repo Stardust75001/TPS-STAR"
alias TPSLIST="gh run list --workflow='verify-all-final.yml' --limit 3 --repo Stardust75001/TPS-STAR"
alias TPSLIGHT='gh variable set SLACK_MODE --body "light" --repo Stardust75001/TPS-STAR && echo \"🪶 Slack mode: Light (TPS-STAR)\"'
alias TPSDARK='gh variable set SLACK_MODE --body "dark" --repo Stardust75001/TPS-STAR && echo \"�� Slack mode: Dark (TPS)\"'
alias TPSCHAIN='TPSDARK && TPSRUNVERIFY && TPSWATCH'
alias TPSCHEAT='bash ~/Shopify/TPS-STAR-WORKTREE/scripts/build-cheatsheet.sh && open ~/Shopify/TPS-STAR-WORKTREE/CheatSheet/TPS_STAR_Cheatsheet_Aliases.pdf'
alias TPSCLEAN='rm -f ~/Shopify/TPS-STAR-WORKTREE/rapports/Workflows/*.csv && echo \"🧹 Rapports nettoyés.\" && TPSCHAIN'

# =============================
# 🧠 TPS-STAR WORKFLOW ALIASES
# =============================

alias TPSRUNVERIFY="gh workflow run '🧠 Verify + Resume + PDF + Slack' --repo Stardust75001/TPS-STAR --ref DEV"
alias TPSWATCH="gh run watch --repo Stardust75001/TPS-STAR"
alias TPSLIST="gh run list --workflow='verify-all-final.yml' --limit 3 --repo Stardust75001/TPS-STAR"
alias TPSLIGHT='gh variable set SLACK_MODE --body "light" --repo Stardust75001/TPS-STAR && echo \"🪶 Slack mode: Light (TPS-STAR)\"'
alias TPSDARK='gh variable set SLACK_MODE --body "dark" --repo Stardust75001/TPS-STAR && echo \"�� Slack mode: Dark (TPS)\"'
alias TPSCHAIN='TPSDARK && TPSRUNVERIFY && TPSWATCH'
alias TPSCHEAT='bash ~/Shopify/TPS-STAR-WORKTREE/scripts/build-cheatsheet.sh && open ~/Shopify/TPS-STAR-WORKTREE/CheatSheet/TPS_STAR_Cheatsheet_Aliases.pdf'
alias TPSCLEAN='rm -f ~/Shopify/TPS-STAR-WORKTREE/rapports/Workflows/*.csv && echo \"🧹 Rapports nettoyés.\" && TPSCHAIN'
