# 📊 TPS Tracking Events Documentation

## Vue d'ensemble

Le système de tracking TPS-STAR capture automatiquement les interactions utilisateur importantes et les transmet vers Google Analytics 4 (GA4) et Meta Pixel de manière unifiée.

## 🎯 Événements Globaux Automatiques

Ces événements sont capturés automatiquement par `snippets/tps-events.liquid` sans configuration supplémentaire :

### E-commerce Core
| Événement | Déclencheur | Propriétés |
|-----------|-------------|------------|
| `Add to Cart` | Ajout produit au panier via formulaire ou fetch | `product_id`, `product_name`, `price`, `quantity` |
| `Begin Checkout` | Clic sur bouton checkout | Aucune propriété spécifique |
| `Product View` | Chargement page produit | `product_id`, `product_name`, `product_type`, `price`, `vendor` |

### Engagement
| Événement | Déclencheur | Propriétés |
|-----------|-------------|------------|
| `Search` | Soumission formulaire de recherche | `query` |
| `Newsletter Signup` | Soumission formulaire newsletter | `email`, `location` |
| `Blog Post Read` | Scroll 75% sur article blog | `article_title`, `read_percentage` |

## 🎨 Événements Spécifiques par Section

### Product Recommendations
**Événement :** `Product Recommended Click`
**Déclencheur :** Clic sur produit recommandé
**Propriétés :**
```javascript
{
  product_handle: "premium-collar",
  product_name: "Premium Dog Collar", 
  position: 2,
  recommended_from: "product_page",
  recommendation_type: "related",
  source_product_id: "123456789",
  total_recommendations: 4
}
```

### Blog Articles
**Événement :** `Blog Post Read`
**Déclencheur :** Scroll 75% de l'article
**Propriétés :**
```javascript
{
  article_title: "Pet Care Tips",
  article_author: "John Doe", 
  read_percentage: 75,
  time_on_page: 180,
  word_count: 850
}
```

## 🔧 API du Système

### Fonction Principale
```javascript
TPS.trackEvent(eventName, properties)
```

**Paramètres :**
- `eventName` (string) : Nom de l'événement en anglais, format "Verb Noun"
- `properties` (object) : Objet avec les propriétés de l'événement

**Exemple :**
```javascript
TPS.trackEvent('Add to Cart', {
  product_id: '123456789',
  product_name: 'Premium Dog Collar',
  price: 29.99,
  quantity: 1,
  source: 'hero_button'
});
```

## 📋 Standards de Nommage

### Noms d'Événements
- **Format :** "Verb Noun" (ex: "Add to Cart", "View Product")
- **Langue :** Anglais uniquement
- **Casse :** Title Case (première lettre de chaque mot en majuscule)
- **Cohérence :** Utilisez les noms standardisés ci-dessous

### Propriétés
- **Format :** snake_case (ex: `product_id`, `user_email`)
- **Types :** Utilisez les types appropriés (string, number, boolean)
- **Cohérence :** Utilisez les mêmes noms de propriétés pour des données similaires

## 📊 Événements Standardisés

### E-commerce
```javascript
// Ajout au panier
TPS.trackEvent('Add to Cart', {
  product_id: string,
  product_name: string,
  price: number,
  quantity: number,
  variant_id: string,
  category: string,
  source: string // 'product_page', 'collection', 'recommendation'
});

// Vue produit
TPS.trackEvent('Product View', {
  product_id: string,
  product_name: string,
  product_type: string,
  price: number,
  vendor: string
});

// Début de checkout
TPS.trackEvent('Begin Checkout', {
  currency: string,
  value: number,
  num_items: number
});
```

### Engagement Utilisateur
```javascript
// Recherche
TPS.trackEvent('Search', {
  query: string,
  source: string, // 'header', 'sidebar', 'mobile'
  results_count: number
});

// Newsletter
TPS.trackEvent('Newsletter Signup', {
  email: string,
  location: string, // 'footer', 'popup', 'article'
  source_page: string
});

// Lecture article
TPS.trackEvent('Blog Post Read', {
  article_title: string,
  article_author: string,
  read_percentage: number,
  time_on_page: number
});
```

### Navigation et Recommendations
```javascript
// Clic recommandation
TPS.trackEvent('Product Recommended Click', {
  product_id: string,
  product_name: string,
  position: number,
  recommended_from: string, // 'product_page', 'homepage', 'cart'
  recommendation_type: string // 'related', 'trending', 'bestsellers'
});

// Clic collection
TPS.trackEvent('Product Collection Click', {
  product_id: string,
  collection_handle: string,
  position: number,
  total_products: number
});
```

## 🛠️ Implémentation

### 1. Événements Globaux
Automatiquement capturés via `snippets/tps-events.liquid` inclus dans `layout/theme.liquid`.

### 2. Événements Spécifiques
Ajoutés directement dans les sections concernées avec des scripts inline.

**Exemple dans une section :**
```liquid
<script>
document.querySelector('.special-button')?.addEventListener('click', function() {
  TPS.trackEvent('Special Action', {
    button_location: 'hero_section',
    page_type: '{{ template.name }}'
  });
});
</script>
```

### 3. Validation des Données
```liquid
{%- comment -%} Utilisation des filtres Liquid appropriés {%- endcomment -%}
TPS.trackEvent('Add to Cart', {
  product_name: {{ product.title | json }}, // Échappe les guillemets
  price: {{ product.price | divided_by: 100.0 }}, // Prix en décimal
  category: {{ product.type | json }}
});
```

## 🧪 Debug et Test

### Mode Debug
```javascript
// Activer les logs console
localStorage.setItem('TPS_DEBUG', '1');

// Désactiver
localStorage.removeItem('TPS_DEBUG');
```

### Validation GA4
1. Ouvrir Google Analytics 4
2. Aller dans **Admin > DebugView**
3. Déclencher les événements sur le site
4. Vérifier que les événements apparaissent en temps réel

### Validation Meta Pixel
1. Installer **Meta Pixel Helper** (extension Chrome)
2. Naviguer sur le site
3. Vérifier que les événements custom sont détectés

## 📈 Reporting et Analyse

### Google Analytics 4
Les événements TPS apparaissent dans :
- **Reports > Engagement > Events**
- **Admin > DebugView** (temps réel)
- **Explore** pour analyses personnalisées

### Meta Pixel
Les événements sont visibles dans :
- **Events Manager**
- **Ads Manager > Audiences** (pour retargeting)

## 🔄 Maintenance

### Ajout d'un Nouvel Événement
1. Définir le nom et les propriétés selon les standards
2. Documenter dans cette section
3. Implémenter dans la section appropriée
4. Tester avec le mode debug
5. Valider dans GA4 et Meta Pixel

### Modification d'un Événement Existant
1. Vérifier l'impact sur les rapports existants
2. Maintenir la rétrocompatibilité si possible
3. Mettre à jour la documentation
4. Communiquer les changements à l'équipe

## 🚨 Bonnes Pratiques

### Performance
- ✅ Utiliser `addEventListener` sur des éléments stables
- ✅ Éviter les listeners dans les boucles
- ✅ Préférer l'event delegation pour les éléments dynamiques
- ❌ Ne pas surcharger avec trop d'événements

### Données
- ✅ Inclure les informations essentielles (ID, nom, prix)
- ✅ Utiliser des types de données cohérents
- ✅ Valider les données côté client si nécessaire
- ❌ Ne pas inclure d'informations sensibles (emails complets, etc.)

### Gouvernance
- ✅ Documenter chaque nouvel événement
- ✅ Suivre les conventions de nommage
- ✅ Tester avant mise en production
- ✅ Monitorer les performances et erreurs

## 📞 Support

Pour questions ou problèmes :
1. Vérifier cette documentation
2. Activer le mode debug (`TPS_DEBUG`)
3. Consulter les logs dans la console
4. Vérifier les workflow GitHub Actions pour les audits automatiques
