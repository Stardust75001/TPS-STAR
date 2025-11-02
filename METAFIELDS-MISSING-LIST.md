# 📋 METAFIELDS MANQUANTS - SHOPIFY ADMIN CONFIGURATION

## 🎯 NAMESPACE: `custom_integrations`

Allez dans **Shopify Admin → Settings → Custom data → Shop**

---

## ✅ METAFIELDS PRIORITAIRES (À configurer IMMÉDIATEMENT)

### 🔥 1. Microsoft Clarity
```
Nom: clarity_id
Type: Single line text
Valeur: tzvd9w6rjs
Description: Microsoft Clarity Project ID (alexjet2000@gmail.com)
```

### 📊 2. Hotjar
```
Nom: hotjar_id  
Type: Single line text
Valeur: 6564192
Description: Hotjar Site ID (alfalconx@gmail.com)
```

### 📈 3. Google Analytics 4
```
Nom: ga4_token
Type: Single line text  
Valeur: G-E4NPI2ZZM3
Description: Google Analytics 4 Measurement ID
```

### 📘 4. Meta Business (Facebook/Instagram)
```
Nom: meta_pixel_id
Type: Single line text
Valeur: 1973238620087976  
Description: Meta Pixel ID for Facebook/Instagram tracking
```

### 💬 5. Slack Webhook
```
Nom: slack_webhook_url
Type: Single line text
Valeur: https://hooks.slack.com/services/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
Description: Slack webhook for notifications
```

---

## 🔧 METAFIELDS OPTIONNELS (Selon vos besoins)

### 🚨 6. Sentry (Error Tracking)
```
Nom: sentry_dsn
Type: Single line text
Valeur: [À obtenir de sentry.io]
Description: Sentry DSN for error tracking
```

### ⚡ 7. Cloudflare Analytics
```
Nom: cloudflare_beacon_token
Type: Single line text
Valeur: [À obtenir de Cloudflare]
Description: Cloudflare Web Analytics token
```

### 🔍 8. Ahrefs SEO
```
Nom: ahrefs_api_key
Type: Single line text
Valeur: [Votre clé API Ahrefs]
Description: Ahrefs API key for SEO monitoring
```

### 🏷️ 9. Google Tag Manager (si utilisé)
```
Nom: gtm_id
Type: Single line text
Valeur: GTM-XXXXXXX
Description: Google Tag Manager Container ID
```

### 🔍 10. Google Search Console
```
Nom: gsc_verification
Type: Single line text
Valeur: [Code de vérification GSC]
Description: Google Search Console verification code
```

### 🌐 11. Domaine Principal
```
Nom: domain
Type: Single line text
Valeur: thepetsociety.paris
Description: Domaine principal du site
```

---

## 🎯 PLATEFORMES SUPPLÉMENTAIRES (Si nécessaires)

### 📊 Analytics Avancé
```
# Amplitude (Analytics gratuit)
amplitude_key: [Clé Amplitude]

# Mixpanel (Analytics payant)  
mixpanel_token: [Token Mixpanel]
```

### 📱 Social Media Pixels
```
# TikTok Pixel
tiktok_pixel: [TikTok Pixel ID]

# Snapchat Pixel
snapchat_pixel: [Snapchat Pixel ID]

# Pinterest Tag
pinterest_tag: [Pinterest Tag ID]
```

### 🛍️ E-commerce Tracking
```
# Shopify Pixel (si différent)
shopify_pixel: [Shopify Pixel ID]
```

---

## 🚀 INSTRUCTIONS DE CONFIGURATION

1. **Allez dans Shopify Admin**
2. **Settings → Custom data → Shop**
3. **Cliquez sur "Add definition"**
4. **Namespace**: `custom_integrations` 
5. **Ajoutez chaque metafield** avec le nom exact (sensible à la casse)
6. **Type**: "Single line text" pour tous
7. **Sauvegardez** chaque metafield

## ⚠️ NOTES IMPORTANTES

- **Respectez exactement** les noms de metafields (clarity_id, hotjar_id, etc.)
- **TPS-STAR supporte les deux formats** : `clarity_id` ET `Clarity_ID` (fallback)
- **Priorité 1** : clarity_id, hotjar_id, ga4_token, meta_pixel_id
- **Les valeurs vides** sont ignorées automatiquement

## 🧪 TEST APRÈS CONFIGURATION

Après avoir configuré les metafields, testez sur votre site :

```javascript
// Console test (F12 sur thepetsociety.paris)
TPS.debug.enable()
console.log('Config:', TPS.integrations)
```

Vous devriez voir vos IDs configurés s'afficher ! ✅
