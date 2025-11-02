# TPS-STAR Analytics Configuration Guide
# Configuration des IDs pour Microsoft Clarity et Hotjar

## 🎯 IDs Officiels TPS-STAR

### Microsoft Clarity
- **ID**: `tzvd9w6rjs`
- **Site ID**: `6564192` (pour référence)
- **Dashboard**: https://clarity.microsoft.com

### Hotjar
- **ID**: `6564192`
- **Dashboard**: https://insights.hotjar.com

## 📝 Configuration dans Shopify

### Étape 1: Ajouter les Métafields
Dans **Shopify Admin** → **Paramètres** → **Métadonnées** → **Boutique**:

**Namespace**: `custom_integrations`

1. **Clarity_ID**
   - Type: Single line text
   - Valeur: `tzvd9w6rjs`

2. **Hotjar_ID**  
   - Type: Single line text
   - Valeur: `6564192`

### Étape 2: Vérification
Une fois configuré, testez avec :

```javascript
// Dans la console du navigateur
TPS.debug.enable()
console.log('Clarity ID:', TPS.integrations.clarity_id)
console.log('Hotjar ID:', TPS.integrations.hotjar_id)
```

## 🧪 Test des Plateformes

### Microsoft Clarity
1. Allez dans https://clarity.microsoft.com
2. Sélectionnez votre projet (ID: tzvd9w6rjs)
3. Vérifiez que les données arrivent en temps réel

### Hotjar  
1. Allez dans https://insights.hotjar.com
2. Sélectionnez votre site (ID: 6564192)
3. Vérifiez les heatmaps et recordings

## 💡 Validation Technique

### Code Clarity Injecté:
```html
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "tzvd9w6rjs");
</script>
```

### Code Hotjar Injecté:
```html
<script>
    (function (c, s, q, u, a, r, e) {
        c.hj=c.hj||function(){(c.hj.q=c.hj.q||[]).push(arguments)};
        c._hjSettings = { hjid: a };
        r = s.getElementsByTagName('head')[0];
        e = s.createElement('script');
        e.async = true;
        e.src = q + c._hjSettings.hjid + u;
        r.appendChild(e);
    })(window, document, 'https://static.hj.contentsquare.net/c/csq-', '.js', 6564192);
</script>
```

## 🚀 Prochaines Étapes

1. **Configurez les métafields** avec les IDs ci-dessus
2. **Testez le chargement** avec `TPS.debug.enable()`
3. **Vérifiez les dashboards** Clarity et Hotjar
4. **Commencez l'analyse** des données utilisateur !

Les codes sont déjà intégrés dans le système TPS-STAR et se chargeront automatiquement une fois les métafields configurés.
