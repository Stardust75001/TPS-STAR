# 🧠 TPS — Aliases ZSH (Référence)
_Généré automatiquement le 2025-11-02 02:13:29_

## 🔗 Fichier source
`~/.aliases`

## 📌 Aliases

```bash
alias STAR='cd ~/Shopify/TPS-STAR-WORKTREE && echo "📁 Projet THE PET SOCIETY ouvert."'
```
```bash
alias SHOPIFY='cd ~/Shopify'
```
```bash
alias BACKUPS='cd ~/Shopify/TPS-BACKUPS && echo "🗂️ Dossier de sauvegardes ouvert."'
```
```bash
alias GITMAIN='git checkout main && git pull'
```
```bash
alias GITFIX='git add -A && git commit -m "quick fix: $(date +%Y-%m-%d_%H:%M:%S)" && git push'
```
```bash
alias PATCHLIQUID='git checkout -b fix/liquid-guards && git add . && git commit -m "fix: Liquid guards"'
```
```bash
alias SYNCALL='cd ~/Shopify/TPS-STAR-WORKTREE && bash ~/Shopify/backup-top.sh && git add -A && git commit -m "sync: $(date +%Y-%m-%d_%H:%M:%S)" && git push && echo "✅ Backup + Push GitHub terminés."'
```
```bash
alias OPENGIT='open https://github.com/Stardust75001/TPS-STAR'
```
```bash
alias CLEANALL='find ~/Shopify/TPS-STAR-WORKTREE -name ".DS_Store" -delete && echo "🧹 Nettoyage complet terminé."'
```
```bash
alias FIXPERM='chmod -R 755 ~/Shopify/TPS-STAR-WORKTREE && echo "🔐 Permissions corrigées."'
```
```bash
alias BACKUP='bash ~/Shopify/backup-top.sh'
```
```bash
alias SANITY='shopify theme check && echo "✅ Sanity check terminé"'
```
```bash
alias SERVE='shopify theme serve'
```
```bash
alias THEMECHECK='cd ~/Shopify/TPS-STAR-WORKTREE && shopify theme check && shopify theme validate && echo "🧠 Vérification complète du thème terminée."'
```
```bash
alias THEMEFIX='cd ~/Shopify/TPS-STAR-WORKTREE && bash ~/Shopify/fix-liquid-json-theme.sh && echo "🧩 Liquid/JSON vérifiés et réparés (si besoin)."'
```
```bash
alias THEMEPUSH='cd ~/Shopify/TPS-STAR-WORKTREE && bash ~/Shopify/fix-liquid-json-theme.sh && shopify theme check && shopify theme validate && shopify theme push --store f6d72e-0f.myshopify.com && echo "🚀 Thème corrigé, validé et poussé."'
```
```bash
alias THEMEDEPLOY='bash ~/Shopify/backup-top.sh && THEMEPUSH'
```
```bash
alias mk='make -C ~/Shopify/TPS-STAR-WORKTREE'
```
```bash
alias SYNCDEV='bash ~/Shopify/TPS-STAR-WORKTREE/scripts/git-sync-dev.sh'
```
```bash
alias SYNCDEV='bash ~/Shopify/TPS-STAR-WORKTREE/scripts/git-sync-dev.sh'
```
```bash
alias SYNCMAIN='bash ~/Shopify/TPS-STAR-WORKTREE/scripts/git-sync-main.sh'
```

## ⚙️ Fonctions (signatures)


<sub>© Falcon Trading Company — document généré.</sub>
