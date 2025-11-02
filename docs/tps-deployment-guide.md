# 🚀 TPS Tracking v1.0 - Guide d'Implémentation

## 📁 Déploiement des Fichiers

### ✅ **Étape 1: Déployer `assets/tps-tracking.js`**

Le fichier `assets/tps-tracking.js` est **prêt à déployer** avec la nouvelle version robuste et idempotente.

**📍 Dans Shopify Admin :**
1. Aller dans **Actions en ligne → Modifier le code**
2. **Assets → Add a new asset → Create a blank file**
3. Nommer le fichier : `tps-tracking.js`
4. Copier-coller le contenu complet du fichier
5. **Sauvegarder**

### ✅ **Étape 2: Vérifier l'inclusion dans `theme.liquid`**

**Le script est déjà inclus** dans `layout/theme.liquid` ligne 204:
```liquid
<script src="{{ 'tps-tracking.js' | asset_url }}" defer></script>
```

### ✅ **Étape 3: Configuration des Métafields**

**📍 Dans Shopify Admin → Paramètres → Métadonnées → Boutique :**

**Namespace : `custom_integrations`**
- `GA4_Token` = Votre ID GA4 (ex: `G-XXXXXXXXXX`)
- `Meta_Pixel_ID` = `1973238620087976`
- `Sentry_DSN` = Votre DSN Sentry (optionnel)
- `Cloudflare_Token` = Votre token Cloudflare (optionnel)

---

## 🧪 **Test et Validation**

### **1. Test de Base (Console du Navigateur)**
```javascript
// Vérifier que TPS est chargé
typeof TPS !== 'undefined'  // Doit retourner true

// Activer le debug
TPS.debug.enable()  // Recharge la page automatiquement
```

### **2. Test d'Événement**
```javascript
// Tester un événement simple
TPS.debug.test('Page View', {
  page: location.pathname,
  timestamp: Date.now()
});

// Événement personnalisé
TPS.trackEvent('Button Click', {
  button_name: 'hero_cta',
  section: 'homepage',
  user_type: 'new_visitor'
});
```

### **3. Diagnostic de Configuration**
En mode développement, inclure le diagnostic :
```liquid
{% if request.host contains 'preview' %}
  {% render 'tps-config-checker' %}
{% endif %}
```

---

## 🎯 **Événements Automatiques Inclus**

### **1. Newsletter Signup**
```html
<form data-newsletter data-location="footer">
  <input type="email" name="email" required>
  <button type="submit">Subscribe</button>
</form>
```
→ Génère automatiquement : `TPS.trackEvent('Newsletter Signup', {...})`

### **2. Product Recommendations**
```html
<a href="{{ product.url }}"
   data-rec-product-id="{{ product.id }}"
   data-rec-position="{{ forloop.index }}"
   data-rec-source="homepage">
   {{ product.title }}
</a>
```
→ Génère automatiquement : `TPS.trackEvent('Product Recommended Click', {...})`

### **3. Add to Cart (Opt-in)**
```html
<button data-track-add 
        data-product-id="{{ product.selected_or_first_available_variant.id }}"
        data-product-name="{{ product.title | escape }}"
        data-price="{{ product.selected_or_first_available_variant.price | money_without_currency | replace: ',', '.' }}"
        data-source="product_page">
  Ajouter au Panier
</button>
```
→ Génère automatiquement : `TPS.trackEvent('Add to Cart', {...})`

### **4. Page View Automatique**
Chaque page charge génère automatiquement :
```javascript
TPS.trackEvent('Page View', {
  path: location.pathname,
  title: document.title
});
```

---

## 🔧 **Événements Manuels**

### **Exemple : Bouton Héros**
```html
<button id="btn-hero" class="hero-cta">
  Découvrir nos Produits
</button>

<script>
  document.getElementById('btn-hero').addEventListener('click', function() {
    TPS.trackEvent('Hero CTA Click', {
      button_text: 'Découvrir nos Produits',
      section: 'homepage_hero',
      user_session_id: Date.now(),
      page_scroll_position: window.pageYOffset
    });
  });
</script>
```

### **Exemple : Ajout au Panier Personnalisé**
```html
<button id="add-to-cart-hero" data-variant-id="{{ product.selected_or_first_available_variant.id }}">
  Ajouter - {{ product.selected_or_first_available_variant.price | money }}
</button>

<script>
  document.getElementById('add-to-cart-hero').addEventListener('click', function() {
    const variantId = this.getAttribute('data-variant-id');
    
    TPS.trackEvent('Add to Cart', {
      product_id: '{{ product.id }}',
      variant_id: variantId,
      product_name: '{{ product.title | escape }}',
      price: {{ product.selected_or_first_available_variant.price | money_without_currency | replace: ',', '.' }},
      currency: '{{ cart.currency.iso_code }}',
      source: 'hero_button',
      collection: '{{ collection.title | escape }}',
      page_type: 'product'
    });
    
    // Votre logique d'ajout au panier existante
    // fetch('/cart/add.js', {...})
  });
</script>
```

### **Exemple : Événement de Conversion**
```javascript
// Après un achat réussi (page de remerciement)
TPS.trackEvent('Purchase', {
  transaction_id: '{{ order.number }}',
  value: {{ order.total_price | money_without_currency | replace: ',', '.' }},
  currency: '{{ order.currency }}',
  items_count: {{ order.line_items.size }},
  shipping_method: '{{ order.shipping_method.title }}',
  discount_amount: {{ order.total_discounts | money_without_currency | replace: ',', '.' }},
  customer_type: '{% if customer.orders_count == 1 %}new{% else %}returning{% endif %}'
});
```

---

## 📊 **Validation dans les Plateformes**

### **Google Analytics 4**
1. Ouvrir **GA4 → Configure → DebugView**
2. Naviguer sur votre site avec debug activé
3. Les événements `TPS.trackEvent()` apparaissent en temps réel

### **Meta Pixel (Events Manager)**
1. Ouvrir **Meta Business → Events Manager**
2. Sélectionner votre Pixel `1973238620087976`
3. **Test Events** → Voir les événements custom en direct

### **Sentry (Error Tracking)**
1. Les événements TPS apparaissent comme **Breadcrumbs**
2. Dans **Issues → Event Details → Breadcrumbs**
3. Catégorie : `tps.event`

---

## 🚀 **Prochaines Étapes**

1. **Déployer** `assets/tps-tracking.js` sur le thème
2. **Configurer** les métafields dans Shopify Admin
3. **Tester** avec `TPS.debug.enable()` et `TPS.debug.test()`
4. **Valider** les événements dans GA4 DebugView
5. **Implémenter** les événements personnalisés selon vos besoins
6. **Activer** les rapports hebdomadaires automatiques

---

## 💡 **Tips d'Optimisation**

### **Debug Conditionnel**
```liquid
{% if request.host contains 'preview' or request.host contains 'dev' %}
  <script>TPS.debug.enable();</script>
{% endif %}
```

### **Événements Conditionnels**
```javascript
// Seulement si l'utilisateur a scrollé plus de 50%
if (window.pageYOffset > document.body.scrollHeight * 0.5) {
  TPS.trackEvent('Deep Page Engagement', {
    scroll_depth: Math.round((window.pageYOffset / document.body.scrollHeight) * 100)
  });
}
```

### **Queue d'Événements**
Le SDK gère automatiquement la queue d'événements si GA4/Meta Pixel se chargent après TPS. Aucune action requise.

---

**🎉 TPS Tracking v1.0 est prêt à déployer !**

Toutes les fonctionnalités sont incluses :
- ✅ Tracking universel GA4 + Meta Pixel
- ✅ Événements automatiques (Newsletter, Recommandations, Add to Cart)
- ✅ Debug mode complet
- ✅ Configuration via métafields Shopify
- ✅ Queue system pour chargement asynchrone
- ✅ Protection contre double-chargement
- ✅ Compatible avec tous les thèmes Shopify
