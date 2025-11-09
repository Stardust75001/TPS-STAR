# 🔐 TPS-STAR API Keys & Secrets Management
## Guide de Configuration Sécurisée

### 📋 **APIs à Conserver dans Shopify**

#### ✅ **ESSENTIELS - À GARDER** :
1. **SHOPIFY_API_KEY** : `shpat_1a4d9f469967266533...`
   - Usage : Admin API access, metafields, orders
   - Permissions : read_products, read_orders, read_customers

2. **SHOPIFY_CLI_AUTH_TOKEN** : `shpat_246b03fff5ae13abf7...`
   - Usage : Shopify CLI theme deployments
   - Permissions : theme management

#### 🗑️ **À SUPPRIMER - Doublons/Obsolètes** :
- ❌ CLI Exports (doublon)
- ❌ CLI Themes (doublon)
- ❌ GitHub Theme Deploy (ancien système)
- ❌ SHOPIFY_CATALOG_IMPORT_API_KEY (usage unique terminé)
- ❌ SyncScript (remplacé par TPS-STAR)
- ❌ Theme Kit Deploy (remplacé par CLI)

---

### 🔗 **GitHub-Shopify Connection**

**API Utilisée** : Shopify CLI + Admin API
**Documentation** : https://shopify.dev/docs/api/admin

#### Configuration Actuelle :
```bash
# Dans GitHub Secrets
SHOPIFY_STORE_URL=https://f6d72e-0f.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_your_admin_api_token
SHOPIFY_CLI_AUTH_TOKEN=shpat_your_cli_token
```

#### Permissions Requises :
- `read_themes` / `write_themes` : Pour deployments
- `read_metafields` / `write_metafields` : Pour TPS-STAR config
- `read_products` : Pour analytics

---

### 🎯 **TPS-STAR Metafields - Configuration Prioritaire**

#### Shopify Admin → Settings → Custom data → Shop

| Namespace | Key | Type | Valeur |
|-----------|-----|------|--------|
| `custom_integrations` | `clarity_id` | Single line text | `tzvd9w6rjs` |
| `custom_integrations` | `hotjar_id` | Single line text | `6564192` |
| `custom_integrations` | `ga4_token` | Single line text | `G-E4NPI2ZZM3` |
| `custom_integrations` | `meta_pixel_id` | Single line text | `1973238620087976` |
| `custom_integrations` | `slack_webhook_url` | Single line text | `[Votre URL Slack]` |

---

### 🔒 **Sécurité des APIs**

#### ✅ **Bonnes Pratiques** :
1. **Shopify Metafields** : Pour les IDs de tracking (sécurisé, pas dans le code)
2. **GitHub Secrets** : Pour les tokens d'API sensibles
3. **Variables d'environnement** : Pour le développement local (.env)

#### ❌ **À ÉVITER** :
- Tokens en dur dans le code
- APIs dans les fichiers publics
- Permissions trop larges

---

### 🧹 **Plan de Cleanup**

#### Étape 1 : Supprimer les Apps Obsolètes
```bash
# Dans Shopify Admin → Apps → App and sales channel settings
# Supprimer :
- CLI Exports
- CLI Themes  
- GitHub Theme Deploy
- SyncScript
- Theme Kit Deploy
```

#### Étape 2 : Configurer les 5 Metafields Prioritaires
```bash
# Utiliser les valeurs officielles TPS-STAR
clarity_id: "tzvd9w6rjs"
hotjar_id: "6564192"
ga4_token: "G-E4NPI2ZZM3"
meta_pixel_id: "1973238620087976"
slack_webhook_url: "[À compléter]"
```

#### Étape 3 : Test Final
```javascript
// Console navigateur sur votre site
TPS.debug.enable()
// Vérifier que les 4 trackers sont actifs
```

---

### 📞 **APIs à Ajouter (Optionnelles)**

Si vous souhaitez les APIs complètes pour le reporting :

#### Analytics APIs :
- **Amplitude** : API Key + Secret (analytics gratuit)
- **Hotjar** : API Token (pour extraire les données)
- **Sentry** : Auth Token (pour les rapports d'erreurs)

#### Configuration :
```bash
# Ajouter dans GitHub Secrets
AMPLITUDE_API_KEY=your_key
HOTJAR_API_TOKEN=your_token
SENTRY_AUTH_TOKEN=your_token
```

Ces APIs sont **optionnelles** - les trackers fonctionnent sans elles.

---

**🎯 PRIORITÉ IMMÉDIATE** : Configurer les 5 metafields Shopify pour activer tous les trackers !
