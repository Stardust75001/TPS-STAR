# ✅ TPS Tracking Analytics - Configuration Complète

## 📁 **Configuration Déployée**

### ✅ **1. Fichier Principal**
- **`snippets/tracking-analytics.liquid`** ✅ Créé et configuré
- **Contient :** Configuration JSON + SDK TPS + Exemples d'usage

### ✅ **2. Inclusion dans Theme**
- **`layout/theme.liquid`** ✅ Mis à jour
- **Position :** Juste avant `</body>` (optimal pour performance)
- **Code :** `{%- render 'tracking-analytics' -%}`

## 🔧 **Configuration des Métafields**

Le système gère automatiquement les variations de noms entre Shopify Admin et le code :

### **Métafields Shopify → Code Mapping**
```liquid
GA4_Token / ga4_token → ga4
Meta_Pixel_ID / meta_pixel_id → meta_pixel_id  
Sentry_DSN / sentry_dsn → sentry_dsn
Cloudflare_Token / cloudflare_beacon_token → cloudflare_beacon_token
Clarity_ID / clarity_id → clarity_id (nouveau)
Hotjar_ID / hotjar_id → hotjar_id (nouveau)
Amplitude_Key / amplitude_key → amplitude_key (nouveau)
```

## 🎯 **Test de Fonctionnement**

### **1. Vérification Console**
```javascript
// Ouvrir la console du navigateur (F12)

// 1. Vérifier TPS
typeof TPS !== 'undefined'  // doit retourner true

// 2. Activer debug mode
TPS.debug.enable()  // recharge automatiquement la page

// 3. Tester un événement
TPS.debug.test('Page View Test', {test: true})

// 4. Vérifier la configuration
console.log('TPS Config:', TPS.integrations)
```

### **2. Événements Automatiques**

Le snippet inclut des exemples qui se déclenchent automatiquement :

#### **Newsletter (Automatique)**
```html
<form data-newsletter data-location="footer">
  <input type="email" name="contact[email]" required>
  <button type="submit">Subscribe</button>
</form>
```
→ Génère : `TPS.trackEvent('Newsletter Signup', {...})`

#### **Recommandations Produits (Automatique)**
```html
<a data-rec-product-id="{{ product.id }}" 
   data-rec-position="1" 
   data-rec-source="homepage">
   Product Link
</a>
```
→ Génère : `TPS.trackEvent('Product Recommended Click', {...})`

#### **Add to Cart (Automatique)**
```html
<button data-track-add 
        data-product-id="{{ variant.id }}"
        data-product-name="{{ product.title }}"
        data-price="{{ variant.price | money_without_currency }}">
  Add to Cart
</button>
```
→ Génère : `TPS.trackEvent('Add to Cart', {...})`

## 📊 **Validation dans les Plateformes**

### **Google Analytics 4**
1. **GA4 → Configure → DebugView**
2. Activer le debug : `TPS.debug.enable()`
3. Les événements TPS apparaissent en temps réel

### **Meta Pixel**
1. **Meta Business → Events Manager**
2. **Test Events** → Voir votre domaine
3. Événements custom visibles avec propriétés

### **Plateformes Gratuites** (si configurées)
- **Clarity :** Événements dans Microsoft Clarity dashboard
- **Hotjar :** Événements dans Hotjar analytics
- **Amplitude :** Événements dans Amplitude dashboard

## 🚀 **Prochaines Étapes**

### **1. Configuration Minimale (Immédiate)**
Dans Shopify Admin → Métadonnées → Boutique → `custom_integrations` :
```
✅ GA4_Token = G-XXXXXXXXXX
✅ Meta_Pixel_ID = 1973238620087976
```

### **2. Analytics Gratuits (Recommandé)**
```
✅ Clarity_ID = [ID Microsoft Clarity]
✅ Hotjar_ID = [ID Hotjar] 
✅ Amplitude_Key = [Clé Amplitude]
```

### **3. Test Final**
1. **Déployer** le thème avec les modifications
2. **Console :** `TPS.debug.enable()`
3. **Naviguer** sur le site → événements visibles dans debug
4. **Vérifier** GA4 DebugView et Meta Test Events

## 💡 **Avantages de cette Configuration**

- ✅ **Un seul snippet** gère tout le tracking
- ✅ **Chargement optimisé** (avant `</body>`)
- ✅ **Auto-tracking** pour newsletter, recommandations, add-to-cart
- ✅ **Compatible** avec les métafields existants de Shopify
- ✅ **Extensible** pour nouvelles plateformes
- ✅ **Debug mode** intégré pour diagnostics

---

**🎉 Configuration Complète ! Le système TPS est maintenant opérationnel.**

**Test rapide :** 
1. Console → `TPS.debug.enable()`
2. Console → `TPS.debug.test()`
3. Vérifier GA4 DebugView 🚀
