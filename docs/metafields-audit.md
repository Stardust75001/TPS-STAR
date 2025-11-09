# 🔍 TPS Tracking - Audit des Métafields Shopify

## ✅ **Métafields PRÉSENTS** (d'après les captures)

| Nom dans Shopify Admin | Nom dans le Code | Status |
|------------------------|------------------|---------|
| `cloudflare_beacon_token` | `cloudflare_beacon_token` | ✅ Match |
| `sentry_dsn` | `sentry_dsn` | ✅ Match |
| `Slack Webhook URL` | `slack_webhook_url` | ⚠️ Casse différente |
| `AHREFS_API_KEY` | `ahrefs_api_key` | ⚠️ Casse différente |
| `Cloudflare Token` | `cloudflare_beacon_token` | ⚠️ Nom différent |
| `Sentry DSN` | `sentry_dsn` | ⚠️ Casse différente |
| `Meta Pixel ID` | `meta_pixel_id` | ⚠️ Casse différente |
| `GA4 Token` | `ga4_token` | ⚠️ Casse différente |
| `Domaine principal` | `domain_principal` | ⚠️ Nom différent |

## ❌ **Métafields MANQUANTS** (requis par le code)

### Analytics Gratuits (PRIORITÉ HAUTE)
- [ ] **`Clarity_ID`** - Microsoft Clarity (analytics gratuit, zéro coût)
- [ ] **`Hotjar_ID`** - Hotjar (heatmaps utilisateur, plan gratuit disponible)
- [ ] **`Amplitude_Key`** - Amplitude (analytics événements, plan gratuit 10M events/mois)

### Plateformes Publicitaires (OPTIONNEL)
- [ ] **`gtm_id`** - Google Tag Manager (gestion centralisée des tags)
- [ ] **`tiktok_pixel`** - TikTok Pixel (si pub TikTok)
- [ ] **`snapchat_pixel`** - Snapchat Pixel (si pub Snapchat)
- [ ] **`pinterest_tag`** - Pinterest Tag (si pub Pinterest)
- [ ] **`mixpanel_token`** - Mixpanel (analytics avancé)
- [ ] **`shopify_pixel`** - Shopify Pixel (analytics natif Shopify)

## 🔧 **ACTIONS REQUISES**

### 1. **Ajouter les Métafields Manquants**

**Dans Shopify Admin → Paramètres → Métadonnées → Boutique**

```
Namespace: custom_integrations
Type: Single line text (pour tous)

PRIORITÉ 1 - Analytics Gratuits:
✅ Clarity_ID = [Votre ID Microsoft Clarity]
✅ Hotjar_ID = [Votre ID Hotjar] 
✅ Amplitude_Key = [Votre clé API Amplitude]

PRIORITÉ 2 - Tag Management:
✅ gtm_id = [Votre ID Google Tag Manager] (ex: GTM-XXXXXXX)

PRIORITÉ 3 - Plateformes Publicitaires:
✅ tiktok_pixel = [Votre TikTok Pixel ID]
✅ snapchat_pixel = [Votre Snapchat Pixel ID]
✅ pinterest_tag = [Votre Pinterest Tag ID]
✅ mixpanel_token = [Votre token Mixpanel]
✅ shopify_pixel = [Votre Shopify Pixel ID]
```

### 2. **Corriger les Incohérences de Noms**

Les métafields dans Shopify utilisent des majuscules, mais le code attend des minuscules.

**Options :**
1. **Renommer dans Shopify** (recommandé) - Plus simple
2. **Adapter le code** pour gérer les deux formats

### 3. **Configuration Minimale Fonctionnelle**

Pour que TPS fonctionne immédiatement :

```
REQUIS ABSOLU:
✅ GA4_Token = G-XXXXXXXXXX
✅ Meta_Pixel_ID = 1973238620087976

RECOMMANDÉ (gratuit):
✅ Clarity_ID = [ID Microsoft Clarity]
✅ Hotjar_ID = [ID Hotjar]
✅ Amplitude_Key = [Clé Amplitude]

OPTIONNEL:
✅ Sentry_DSN = [DSN Sentry pour erreurs]
✅ Cloudflare_Token = [Token Cloudflare Analytics]
```

## 📊 **Valeurs d'Exemple pour Tests**

```
Microsoft Clarity_ID: Format typique "abc123def456"
Hotjar_ID: Format typique "1234567" 
Amplitude_Key: Format typique "ab12cd34ef56gh78ij90kl12mn34op56"
Google Tag Manager: Format "GTM-XXXXXXX"
TikTok Pixel: Format "C1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6"
```

## 🚀 **Prochaines Étapes**

1. **Ajouter** les métafields manquants dans Shopify Admin
2. **Configurer** au minimum GA4_Token et Meta_Pixel_ID  
3. **Tester** avec `TPS.debug.enable()` dans la console
4. **Valider** les événements dans GA4 DebugView et Meta Events Manager
5. **Ajouter progressivement** les autres plateformes selon les besoins

---

**💡 TIP :** Commencez par les analytics gratuits (Clarity, Hotjar, Amplitude) qui donnent un maximum d'insights sans coût supplémentaire !
