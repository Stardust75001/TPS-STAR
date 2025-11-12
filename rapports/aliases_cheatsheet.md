
---

## 🧠 Workflow Automation & Slack — TPS-STAR

| Alias | Description | Commande |
|:------|:-------------|:----------|
| **TPSRUNVERIFY** | Lancer le workflow complet (Verify + Resume + PDF + Slack) | `gh workflow run '🧠 Verify + Resume + PDF + Slack' --repo Stardust75001/TPS-STAR --ref DEV` |
| **TPSWATCH** | Suivre en direct le statut du dernier run | `gh run watch --repo Stardust75001/TPS-STAR` |
| **TPSLIST** | Afficher les 3 derniers runs de la chaîne | `gh run list --workflow='verify-all-final.yml' --limit 3 --repo Stardust75001/TPS-STAR` |
| **TPSLIGHT** | Activer le mode Slack clair (TPS-STAR 🪶) | `gh variable set SLACK_MODE --body "light" --repo Stardust75001/TPS-STAR` |
| **TPSDARK** | Activer le mode Slack sombre (THE PET SOCIETY 🐾) | `gh variable set SLACK_MODE --body "dark" --repo Stardust75001/TPS-STAR` |
| **TPSCHAIN** | Relancer la chaîne complète (mode sombre + run + watch) | `TPSDARK && TPSRUNVERIFY && TPSWATCH` |
| **TPSCHEAT** | Régénérer le PDF Cheatsheet et l’ouvrir dans Preview | `bash ~/Shopify/TPS-STAR-WORKTREE/scripts/build-cheatsheet.sh && open ~/Shopify/TPS-STAR-WORKTREE/CheatSheet/TPS_STAR_Cheatsheet_Aliases.pdf` |
| **TPSCLEAN** | Nettoyer les rapports CSV et relancer la chaîne | `rm -f ~/Shopify/TPS-STAR-WORKTREE/rapports/Workflows/*.csv && TPSCHAIN` |

---

