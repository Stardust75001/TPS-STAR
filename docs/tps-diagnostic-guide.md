# 🔧 TPS Tracking - Guide de Diagnostic

## Problèmes Fréquents et Solutions

### ❌ **Erreur 1: `ReferenceError: Can't find variable: TPS`**

**Cause :** Le SDK TPS n'est pas chargé ou pas encore disponible.

**Solutions :**

#### ✅ Vérification 1: Script dans theme.liquid
Vérifiez que le script est présent dans `layout/theme.liquid` avant `</body>` :
```liquid
{%- comment -%} TPS — Core tracking (namespace TPS) {%- endcomment -%}
<script src="{{ 'tps-tracking.js' | asset_url }}" defer></script>
```

#### ✅ Vérification 2: Fichier assets/tps-tracking.js existe
Le fichier `assets/tps-tracking.js` doit exister et contenir au minimum :
```javascript
window.TPS = window.TPS || {};
TPS.trackEvent = function(name, data) {
  if (!name) return;
  console.log("🧩 TPS.trackEvent →", name, data);
  
  // Envoi GA4
  if (window.gtag) gtag('event', name, data);
  // Envoi Meta Pixel
  if (window.fbq) fbq('trackCustom', name, data);
};

TPS.debug = {
  enable() { localStorage.setItem('TPS_DEBUG', '1'); location.reload(); },
  disable() { localStorage.removeItem('TPS_DEBUG'); location.reload(); },
  test(n='Test Event', d={foo:'bar'}) { TPS.trackEvent(n, d); }
};
```

#### ✅ Test de vérification
Dans la console du navigateur :
```javascript
// Test basique
typeof TPS !== 'undefined' // Doit retourner true

// Test des fonctions
TPS.debug.status() // Affiche l'état de configuration
```

---

### ❌ **Erreur 2: `Failed integrity metadata check` (Sentry)**

**Cause :** Shopify bloque le chargement du script Sentry à cause du hash d'intégrité SRI.

**Solution :** Utiliser la version sans intégrité

Dans `snippets/integrations.liquid`, remplacez :
```liquid
❌ AVANT:
loadScript('https://browser.sentry-cdn.com/7.120.1/bundle.tracing.replay.min.js', 'sentry-sdk')

✅ APRÈS:
loadScript('https://browser.sentry-cdn.com/8.36.0/bundle.tracing.replay.min.js', 'sentry-sdk')
```

#### Configuration Sentry recommandée :
```javascript
Sentry.init({
  dsn: "{{ shop.metafields.custom_integrations.sentry_dsn }}",
  integrations: [
    new Sentry.BrowserTracing(), 
    new Sentry.Replay()
  ],
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
});
```

---

### ❌ **Erreur 3: `Invalid PixelID: null` (Meta Pixel)**

**Cause :** Le Meta Pixel ID n'est pas configuré dans les métafields.

**Solutions :**

#### ✅ Configuration Métafield
1. Aller dans **Shopify Admin**
2. **Paramètres → Métadonnées → Boutique**
3. Créer/modifier métafield :
   - **Namespace :** `custom_integrations`
   - **Clé :** `Meta_Pixel_ID`
   - **Valeur :** `1973238620087976`

#### ✅ Vérification Code
Dans `snippets/integrations.liquid`, vérifier :
```liquid
{%- liquid
  assign meta_pixel_id = shop.metafields.custom_integrations.Meta_Pixel_ID | strip
-%}

<script>
  // Configuration debug
  const meta_pixel = "{{ meta_pixel_id | escape }}";
  console.log('Meta Pixel ID:', meta_pixel);
  
  if (meta_pixel && meta_pixel !== 'null' && meta_pixel !== '') {
    // Initialisation Meta Pixel
    fbq('init', meta_pixel);
  } else {
    console.warn('Meta Pixel ID not configured');
  }
</script>
```

---

## 🧪 Tests et Diagnostic

### Debug Mode
```javascript
// Activer le debug
localStorage.setItem('TPS_DEBUG', '1');
location.reload();

// Vérifier le statut
TPS.debug.status();

// Tester un événement
TPS.debug.test('Test Event', {test: true});
```

### Vérification Automatique
Ajoutez le checker de config (en mode développement uniquement) :
```liquid
{% comment %} En développement seulement {% endcomment %}
{% if request.host contains 'preview' or request.host contains 'dev' %}
  {% render 'tps-config-checker' %}
{% endif %}
```

### Console Commands Utiles
```javascript
// Vérifier TPS
typeof TPS !== 'undefined'

// Vérifier GA4  
typeof gtag === 'function'

// Vérifier Meta Pixel
typeof fbq === 'function'

// Vérifier Sentry
typeof Sentry !== 'undefined'

// Test événement complet
TPS.trackEvent('Debug Test', {
  test_property: 'test_value',
  timestamp: Date.now()
});
```

---

## 📋 Checklist de Configuration

### ✅ Fichiers Requis
- [ ] `assets/tps-tracking.js` existe et est correct
- [ ] `snippets/integrations.liquid` configuré
- [ ] Script TPS chargé dans `layout/theme.liquid`

### ✅ Métafields Shopify
- [ ] `custom_integrations.GA4_Token` configuré
- [ ] `custom_integrations.Meta_Pixel_ID` = `1973238620087976`
- [ ] `custom_integrations.Sentry_DSN` configuré

### ✅ Tests Fonctionnels
- [ ] `TPS.trackEvent()` fonctionne
- [ ] `TPS.debug.test()` fonctionne
- [ ] Événements visibles dans GA4 DebugView
- [ ] Événements visibles dans Meta Events Manager

---

## 🚀 Configuration Minimale Fonctionnelle

Si vous voulez une version minimale qui fonctionne, voici le code essentiel :

### assets/tps-tracking.js (version minimale)
```javascript
window.TPS = window.TPS || {};

TPS.trackEvent = function(name, data) {
  if (!name) return;
  
  const payload = Object.assign({ event: name, timestamp: Date.now() }, data || {});
  console.log("🧩 TPS.trackEvent →", payload);

  // GA4
  if (window.gtag) {
    gtag('event', name.toLowerCase().replace(/\s+/g, '_'), payload);
  }
  
  // Meta Pixel
  if (window.fbq) {
    fbq('trackCustom', name, payload);
  }

  // Debug
  if (localStorage.getItem('TPS_DEBUG') === '1') {
    console.debug("[TPS_DEBUG]", name, payload);
  }
};

TPS.debug = {
  enable() { 
    localStorage.setItem('TPS_DEBUG', '1'); 
    location.reload(); 
  },
  disable() { 
    localStorage.removeItem('TPS_DEBUG'); 
    location.reload(); 
  },
  test(n='Test Event', d={foo:'bar'}) { 
    TPS.trackEvent(n, d); 
  },
  status() {
    console.group('[TPS] Status');
    console.log('TPS loaded:', typeof TPS !== 'undefined');
    console.log('GA4 available:', typeof gtag === 'function');
    console.log('Meta available:', typeof fbq === 'function');
    console.log('Debug mode:', localStorage.getItem('TPS_DEBUG') === '1');
    console.groupEnd();
  }
};

console.log('[TPS] SDK loaded successfully');
```

### Test de Validation
```javascript
// Dans la console du navigateur
TPS.debug.status();
TPS.debug.test();
```

---

## 📞 Support et Monitoring

### GitHub Actions
Les workflows automatiques vérifient :
- Présence du script TPS
- Configuration des métafields
- Intégration GA4/Meta Pixel

### Monitoring Continue
```javascript
// Ajouter à vos pages pour monitoring
window.addEventListener('error', function(e) {
  if (e.message.includes('TPS')) {
    console.error('[TPS] Runtime Error:', e);
    // Optionnel : envoyer à Sentry
  }
});
```
