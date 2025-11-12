# 🧠 TPS — Aliases ZSH (Référence)
_Généré automatiquement le 2025-11-12 01:49:22_

## 🔗 Fichier source
`~/.aliases`

## 📌 Aliases

```bash
alias TPSSTAR='cd ~/Shopify/TPS-STAR-WORKTREE && echo "📁 Projet THE PET SOCIETY ouvert."'
```
```bash
alias TPSRAW='cd ~/Shopify/TPS-RAW-V1-'
```
```bash
alias TPSBASE='cd ~/Shopify/TPS-BASE'
```
```bash
alias TPSGIT='cd ~/Shopify/TPS-STAR-WORKTREE/.git'
```
```bash
alias TPSBACKUPS='cd ~/Shopify/TPS-BACKUPS'
```
```bash
alias TPSALIASES='nano ~/Shopify/TPS-STAR-WORKTREE/docs/ALIASES-REFERENCE.md'
```
```bash
alias OPENGIT='open https://github.com/Stardust75001/TPS-STAR'
```
```bash
alias RUN_GA4_REPORT='python run_report.py'
```
```bash
alias REFRESH_GA4_TOKEN='python refresh_token.py'
```
```bash
alias OPEN_GA4_REPORTS='open rapports/'
```
```bash
alias PUSH_GA4_WORKFLOW="git add .github/workflows/run-ga4-report.yml && git commit -m '🚀 GA4 daily report workflow' && git push origin DEV"
```
```bash
alias PUSH_REFRESH_TOKEN_WORKFLOW="git add .github/workflows/refresh-ga4-token.yml && git commit -m '🔄 Refresh GA4 token workflow' && git push origin DEV"
```
```bash
alias GITMAIN='git checkout main && git pull'
```
```bash
alias GITDEV='git checkout DEV && git pull'
```
```bash
alias GITPUSH='git push origin DEV'
```
```bash
alias GITST='git status'
```
```bash
alias GITADD='git add . && git commit -m "⚙️ Quick commit"'
```
```bash
alias GITREBASE='git pull origin main --rebase'
```
```bash
alias GITFIX='grep -rl "<<<<<<< HEAD" . | xargs sed -i "" "/<<<<<<< HEAD/d; /=======/d; />>>>>>>/d/"'
```
```bash
alias PATCHLIQUID='git checkout -b fix/liquid-guards && git add . && git commit -m "fix: Liquid guards"'
```
```bash
alias SYNCDEV='bash ~/Shopify/TPS-STAR-WORKTREE/scripts/git-sync-dev.sh'
```
```bash
alias TPSCLEAN='find . -name ".DS_Store" -delete && git gc --prune=now && git repack -a -d'
```
```bash
alias TPSBACKUP='bash ~/Shopify/backup-top.sh'
```
```bash
alias CLEANALL='find ~/Shopify/TPS-STAR-WORKTREE -name ".DS_Store" -delete && echo "🧹 Nettoyage complet terminé."'
```
```bash
alias FIXPERM='chmod -R 755 ~/Shopify/TPS-STAR-WORKTREE && echo "🔐 Permissions corrigées."'
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
alias THEMEPUSH='cd ~/Shopify/TPS-STAR-WORKTREE && bash ~/Shopify/fix-liquid-json-theme.sh && shopify theme check && shopify theme validate && shopify theme push --store f6d72e-0f.myshopify.com'
```
```bash
alias THEMEDEPLOY='bash ~/Shopify/backup-top.sh && THEMEPUSH'
```
```bash
alias MAKE_ALIAS_CSV='bash scripts/export-aliases-workflows.sh'
```
```bash
alias OPEN_ALIAS_CSV='open exports/aliases_workflows.csv'
```
```bash
alias OPEN_APIS_CSV='open exports/apis_secrets_metrics.csv'
```
```bash
alias README='code README.md'
```
```bash
alias OPEN_SITEMAP='open public/sitemap.xml'
```
```bash
alias OPEN_DASHBOARD='open https://analytics.google.com/analytics/web/'
```

## ⚙️ Fonctions (signatures)

 - 60:syncall() 
 - 69:TPSREPORTS() 

<sub>© Falcon Trading Company — document généré.</sub>
