# 📊 TPS Tracking SDK - Guide d'implémentation

## Vue d'ensemble

Le SDK TPS Tracking (`tps-tracking.js`) fournit un système unifié de tracking d'événements qui route automatiquement vers :
- **Google Analytics 4** (gtag)
- **Meta Pixel** (fbq)  
- **Événements DOM personnalisés** (pour autres intégrations)

## 🚀 Installation

### 1. Chargement du SDK
Le SDK est automatiquement chargé dans `layout/theme.liquid` :
```liquid
{%- comment -%} TPS — Core tracking (namespace TPS) {%- endcomment -%}
<script src="{{ 'tps-tracking.js' | asset_url }}" defer></script>
```

### 2. API Principale
```javascript
TPS.trackEvent(eventName, properties);
```

## 🎯 Événements Automatiques

Ces événements sont capturés automatiquement sans configuration :

### E-commerce
- **Page View** - Chaque page visitée
- **Add to Cart** - Via interception fetch `/cart/add.js`
- **Begin Checkout** - Clics sur boutons checkout

### Engagement
- **Newsletter Signup** - Formulaires avec `data-newsletter`
- **Search** - Formulaires de recherche

### Exemple de formulaire newsletter :
```liquid
<form data-newsletter data-location="footer">
  <input type="email" name="contact[email]" required>
  <button type="submit">Subscribe</button>
</form>
```

## 🎨 Événements avec Data-Attributes

### Recommandations Produits
Automatiquement trackées via data-attributes sur les liens produits :

```liquid
<a href="{{ product.url }}"
   data-rec-product-id="{{ product.id }}"
   data-rec-position="{{ forloop.index }}"
   data-rec-source="homepage">
  {{ product.title }}
</a>
```

**Événement généré :** `Product Recommendation Click`

### Boutons Checkout
```liquid
<button data-checkout data-source="cart_drawer">
  Checkout
</button>
```

**Événement généré :** `Begin Checkout`

## 🛠️ Événements Manuels

### Bouton Add to Cart Spécifique
```liquid
<button id="btn-add-hero">Add to Cart</button>

<script>
document.getElementById('btn-add-hero')?.addEventListener('click', function(){
  if (!window.TPS || !TPS.trackEvent) return;
  
  TPS.trackEvent('Add to Cart', {
    product_id: '{{ product.selected_or_first_available_variant.id }}',
    product_name: {{ product.title | json }},
    price: {{ product.selected_or_first_available_variant.price | money_without_currency | replace: ',', '.' }},
    source: 'hero_button'
  });
});
</script>
```

### Lecture d'Article (Scroll 75%)
```liquid
<script>
(function(){
  let sent = false;
  window.addEventListener('scroll', function(){
    if(sent) return;
    const p = (window.scrollY + window.innerHeight) / document.body.scrollHeight * 100;
    if(p >= 75){
      sent = true;
      if (window.TPS && TPS.trackEvent) {
        TPS.trackEvent('Blog Post Read', {
          article_title: {{ article.title | json }},
          read_percentage: 75
        });
      }
    }
  }, {passive:true});
})();
</script>
```

## 📋 Format des Événements

### Noms d'Événements
- **Format :** "Verb Noun" (ex: "Add to Cart", "Product Recommendation Click")
- **Langue :** Anglais
- **Casse :** Title Case

### Propriétés Standards
```javascript
// E-commerce
{
  product_id: string,      // ID du produit
  product_name: string,    // Nom du produit
  price: number,          // Prix en décimal
  quantity: number,       // Quantité
  source: string         // Source du clic
}

// Navigation
{
  position: number,       // Position dans la liste
  recommended_from: string, // Page source
  page_type: string      // Type de page
}
```

## 🧪 Debug et Test

### Activation du Debug
```javascript
// Dans la console du navigateur
localStorage.setItem('TPS_DEBUG', '1');
location.reload();

// Ou utiliser l'helper (si debug déjà activé)
TPS.debug.enable();
```

### Désactivation
```javascript
localStorage.removeItem('TPS_DEBUG');
location.reload();

// Ou
TPS.debug.disable();
```

### Test Manuel
```javascript
// Tester un événement
TPS.debug.test('Test Event', {
  test_property: 'test_value'
});
```

### Logs Debug
Quand le debug est activé, vous verrez dans la console :
```
[TPS] Tracking: Add to Cart
  Properties: {product_id: "123", price: 29.99}
  Available vendors: {ga4: true, meta: true}
  → GA4: add_to_cart {item_id: "123", value: 29.99, currency: "EUR"}
  → Meta: Add to Cart {content_ids: ["123"], value: 29.99, currency: "EUR"}
```

## 🎯 Événements Standards Prédéfinis

### E-commerce Core
| Événement | Propriétés | Déclencheur |
|-----------|------------|-------------|
| `Page View` | `page_type`, `product_id` | Chargement page |
| `Add to Cart` | `product_id`, `price`, `quantity` | Ajout panier |
| `Begin Checkout` | `source` | Clic checkout |

### Engagement
| Événement | Propriétés | Déclencheur |
|-----------|------------|-------------|
| `Product Recommendation Click` | `product_id`, `position`, `recommended_from` | Clic recommandation |
| `Newsletter Signup` | `email`, `location` | Soumission newsletter |
| `Search` | `query`, `source` | Recherche |
| `Blog Post Read` | `article_title`, `read_percentage` | Scroll 75% |

## 🔄 Intégration avec Analytics

### Google Analytics 4
Les événements sont automatiquement convertis au format GA4 :
- `Add to Cart` → `add_to_cart`
- `product_id` → `item_id`
- `product_name` → `item_name`
- `price` → `value` + `currency: "EUR"`

### Meta Pixel
Les événements sont envoyés comme événements custom :
- Propriétés `product_id` → `content_ids: [id]`
- Propriétés `price` → `value` + `currency`
- Type de contenu automatique : `product`

## 📁 Structure des Fichiers

```
assets/
├── tps-tracking.js          # SDK principal
└── ...

snippets/
├── recommended-products.liquid  # Snippet recommandations
├── tps-examples.liquid         # Exemples copy-paste
└── ...

templates/
├── article.liquid              # Template blog avec tracking
└── ...

layout/
└── theme.liquid               # Chargement SDK
```

## ⚡ Bonnes Pratiques

### Performance
- ✅ Utilisez `{passive: true}` sur les event listeners
- ✅ Vérifiez `window.TPS` avant utilisation
- ✅ Un seul listener global plutôt que multiples
- ❌ Évitez les listeners dans les boucles

### Sécurité
- ✅ Échappez les données Liquid avec `| json`
- ✅ Validez les données côté client
- ✅ Ne trackez pas d'informations sensibles

### Gouvernance
- ✅ Utilisez les noms d'événements standardisés
- ✅ Documentez les nouveaux événements
- ✅ Testez avec le mode debug activé

## 🔧 Exemple d'Intégration Complète

```liquid
{%- comment -%} Section avec produits recommandés {%- endcomment -%}
<div class="recommendations">
  {% for product in recommendations.products %}
    <a href="{{ product.url }}"
       data-rec-product-id="{{ product.id }}"
       data-rec-position="{{ forloop.index }}"
       data-rec-source="product_page">
      {{ product.title }} - {{ product.price | money }}
    </a>
  {% endfor %}
</div>

{%- comment -%} Bouton spécial avec tracking inline {%- endcomment -%}
<button id="special-add-btn">Add to Cart (Special)</button>

<script>
document.getElementById('special-add-btn')?.addEventListener('click', function(){
  if (!window.TPS || !TPS.trackEvent) return;
  
  TPS.trackEvent('Add to Cart', {
    product_id: '{{ product.id }}',
    product_name: {{ product.title | json }},
    price: {{ product.price | divided_by: 100.0 }},
    source: 'special_button'
  });
}, {passive: true});
</script>
```

## 📞 Support

Le tracking est automatiquement testé via les workflows GitHub Actions :
- **Audit Trackers** - Vérifie la présence des scripts
- **SEO Checks** - Valide l'intégration analytics

Pour debug local :
1. Activez `TPS_DEBUG`
2. Ouvrez la console navigateur
3. Déclenchez les interactions
4. Vérifiez les logs TPS et GA4/Meta
