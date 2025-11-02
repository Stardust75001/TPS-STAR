# 🔍 GUIDE D'INTERPRÉTATION - TPS.debug.enable()

## 📊 **Résultats Attendus dans la Console**

Après avoir tapé `TPS.debug.enable()` dans la console de votre site, vous devriez voir :

### ✅ **SUCCÈS - Résultat Optimal :**
```
🔍 TPS-STAR Debug Info
├─ 📊 Config loaded: {
│    ga4: "G-E4NPI2ZZM3",
│    meta_pixel_id: "1973238620087976", 
│    sentry_dsn: "https://your-dsn@sentry.io",
│    cloudflare_beacon_token: "21fd2470...",
│    clarity_id: "tzvd9w6rjs",
│    hotjar_id: "6564192",
│    domain: "your-shop.myshopify.com"
│  }
├─ 🎯 Active platforms: ["ga4", "meta_pixel_id", "clarity_id", "hotjar_id", "cloudflare_beacon_token"]
└─ 🔗 TPS object: {integrations: {...}, debug: {...}}
```

### ⚠️ **PROBLÈMES POSSIBLES :**

#### 1. **Métafields Vides/Manquants :**
```
🔍 TPS-STAR Debug Info
├─ 📊 Config loaded: {
│    ga4: "",
│    meta_pixel_id: "",
│    clarity_id: "",
│    hotjar_id: ""
│  }
├─ 🎯 Active platforms: []
└─ 🔗 TPS object: {...}
```
**➜ SOLUTION** : Configurez les metafields dans Shopify Admin

#### 2. **Erreur ReferenceError :**
```
❌ ReferenceError: Can't find variable: TPS
```
**➜ SOLUTION** : Redéployez le fichier `snippets/integrations.liquid` mis à jour

#### 3. **Certains Champs "null" :**
```
🔍 TPS-STAR Debug Info
├─ 📊 Config loaded: {
│    ga4: "G-E4NPI2ZZM3",        ✅ OK
│    meta_pixel_id: null,        ❌ PROBLÈME
│    clarity_id: "tzvd9w6rjs",   ✅ OK
│    hotjar_id: null             ❌ PROBLÈME
│  }
```
**➜ SOLUTION** : Vérifiez les metafields avec des valeurs `null`

---

## 🛠️ **DIAGNOSTIC DÉTAILLÉ**

### **Étape 1 : Vérifier que TPS existe**
```javascript
console.log(window.TPS);
```
**Attendu :** `{integrations: {...}, debug: {...}}`

### **Étape 2 : Vérifier la configuration JSON**
```javascript
console.log(document.getElementById('tps-integrations').textContent);
```
**Attendu :** JSON avec vos valeurs de metafields

### **Étape 3 : Vérifier les logs de chargement**
Dans la console, vous devriez voir :
```
[TPS-STAR] System initialized
🪟 Clarity loaded: tzvd9w6rjs
🔥 Hotjar loaded: 6564192
[TPS] meta id: 1973238620087976 string
[TPS-STAR] Meta Pixel initialized: 1973238620087976
[TPS-STAR] Sentry initialized
```

### **Étape 4 : Tests Fonctionnels**
```javascript
// Test Meta Pixel
console.log(typeof fbq); // Devrait être "function"

// Test Clarity  
console.log(typeof clarity); // Devrait être "function"

// Test Hotjar
console.log(typeof hj); // Devrait être "function"
```

---

## 🎯 **ACTIONS CORRECTIVES**

### **Si Config est Vide :**
1. **Vérifiez les Metafields Shopify :**
   - Admin → Settings → Metafields → Shop
   - Namespace : `custom_integrations`
   - Activez `Storefront API access` pour CHAQUE champ

2. **Métafields Requis :**
   ```
   ga4_token = "G-E4NPI2ZZM3"
   meta_pixel_id = "1973238620087976" 
   sentry_dsn = "votre-dsn-complet"
   clarity_id = "tzvd9w6rjs"
   hotjar_id = "6564192"
   cloudflare_beacon_token = "21fd2470..."
   ```

### **Si TPS n'existe pas :**
1. Redéployez `snippets/integrations.liquid`
2. Vérifiez que `{% render 'integrations' %}` est dans `layout/theme.liquid`

### **Si Certains Trackers ne se Chargent pas :**
1. Vérifiez les erreurs console
2. Testez en navigation privée (pas d'ad-blocker)
3. Vérifiez les dashboards des plateformes

---

## 📋 **CHECKLIST DE VALIDATION**

- [ ] `TPS.debug.enable()` fonctionne sans erreur
- [ ] Config JSON contient vos valeurs réelles (pas "null" ou "")
- [ ] Active platforms liste au moins 3-4 plateformes
- [ ] Logs de chargement visibles pour Clarity/Hotjar
- [ ] Meta Pixel ne dit plus "Invalid PixelID: null"
- [ ] Aucune erreur "integrity metadata check"
- [ ] Dashboards reçoivent les données (5-10 min)

---

## 🚨 **Si Vous Voyez Encore des Erreurs**

Copiez-collez EXACTEMENT ce que vous voyez dans la console et je vous aiderai à diagnostiquer le problème spécifique !

**Common Issues:**
- Metafields mal configurés
- `Storefront API access` non activé  
- Ancienne version du fichier déployée
- Ad-blocker qui bloque les trackers
- Configuration DNS/proxy qui interfère
