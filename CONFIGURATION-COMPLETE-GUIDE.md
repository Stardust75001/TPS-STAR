# 🎯 GUIDE COMPLET DE CONFIGURATION TPS-STAR
# Configuration de tous les trackers avec vos IDs officiels

## 📋 ÉTAPE 1: CONFIGURATION SHOPIFY METAFIELDS

Allez dans **Shopify Admin → Settings → Custom data → Shop**
Namespace: `custom_integrations`

### ✅ TRACKERS PRIORITAIRES (À configurer immédiatement)

```
1. clarity_id = "tzvd9w6rjs"
   📧 Compte: alexjet2000@gmail.com
   🔗 Dashboard: https://clarity.microsoft.com

2. hotjar_id = "6564192" 
   📧 Compte: alfalconx@gmail.com  
   🔗 Dashboard: https://insights.hotjar.com

3. ga4_token = "G-E4NPI2ZZM3"
   📧 Compte: [votre compte GA4]
   🔗 Dashboard: https://analytics.google.com

4. meta_pixel_id = "1973238620087976"
   📧 Compte: [votre compte Meta Business]
   🔗 Dashboard: https://business.facebook.com

5. slack_webhook_url = "https://hooks.slack.com/services/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"
   💬 Notifications en temps réel
```

### 🔧 TRACKERS OPTIONNELS (À configurer selon vos besoins)

```
6. sentry_dsn = "[À obtenir de sentry.io]"
   🚨 Monitoring des erreurs

7. cloudflare_beacon_token = "[À obtenir de Cloudflare]"
   ⚡ Analytics de performance

8. ahrefs_api_key = "[À obtenir d'Ahrefs]"
   🔍 Monitoring SEO

9. gtm_id = "GTM-XXXXXXX" (si vous utilisez GTM)
   🏷️ Google Tag Manager

10. gsc_verification = "[Code de vérification Google Search Console]"
    🔍 Vérification Search Console
```

## 📋 ÉTAPE 2: FINALISER HOTJAR

### Problem identifié: Hotjar non finalisé dans le dashboard

1. **Allez sur https://insights.hotjar.com**
2. **Connectez-vous avec alfalconx@gmail.com**
3. **Terminez l'installation** en suivant l'assistant
4. **Confirmez** que le code de tracking est détecté

## 📋 ÉTAPE 3: TEST COMPLET

### Test dans la console navigateur (thepetsociety.paris):

```javascript
// Copier-coller ce code complet dans la console
console.log('🎯 TPS-STAR - Test de tous les trackers');

// 1. Vérifier la configuration
if (typeof TPS !== 'undefined' && TPS.integrations) {
    console.log('✅ TPS configuré');
    console.log('Config:', TPS.integrations);
} else {
    console.log('❌ TPS non configuré');
}

// 2. Vérifier le chargement
const trackers = {
    'Clarity': typeof clarity !== 'undefined',
    'Hotjar': typeof hj !== 'undefined',
    'GA4': typeof gtag !== 'undefined', 
    'Meta': typeof fbq !== 'undefined',
    'Sentry': typeof Sentry !== 'undefined'
};

console.log('\n📊 Status des trackers:');
Object.entries(trackers).forEach(([name, loaded]) => {
    console.log(`${loaded ? '✅' : '❌'} ${name}`);
});

// 3. Tests fonctionnels
setTimeout(() => {
    console.log('\n🧪 Tests fonctionnels...');
    
    if (typeof clarity !== 'undefined') {
        clarity('set', 'test_user', 'tps_config_check');
        console.log('✅ Clarity: Event test envoyé');
    }
    
    if (typeof hj !== 'undefined') {
        hj('event', 'tps_config_check');
        console.log('✅ Hotjar: Event test envoyé');
    }
    
    if (typeof gtag !== 'undefined') {
        gtag('event', 'tps_config_check', {source: 'manual_test'});
        console.log('✅ GA4: Event test envoyé');
    }
    
    if (typeof fbq !== 'undefined') {
        fbq('trackCustom', 'TPS_Config_Check');
        console.log('✅ Meta: Event test envoyé');
    }
    
}, 2000);
```

## 📋 ÉTAPE 4: VÉRIFICATION DASHBOARDS

### Vérifiez que les données arrivent dans:

1. **Microsoft Clarity** → https://clarity.microsoft.com (alexjet2000@gmail.com)
2. **Hotjar** → https://insights.hotjar.com (alfalconx@gmail.com)  
3. **Google Analytics** → https://analytics.google.com
4. **Meta Business** → https://business.facebook.com
5. **Google Ads** → https://ads.google.com (asc2000@gmail.com - 100-529-5680)

## 🚨 PROBLÈMES FRÉQUENTS

### Si Clarity ne fonctionne pas:
- Vérifiez que `clarity_id = "tzvd9w6rjs"` est bien configuré
- Le compte alexjet2000@gmail.com doit avoir accès au projet

### Si Hotjar ne fonctionne pas:
- Terminez l'installation dans le dashboard Hotjar
- Vérifiez que `hotjar_id = "6564192"` est configuré
- Le compte alfalconx@gmail.com doit être actif

### Si aucun tracker ne fonctionne:
- Vérifiez que `{%- render 'integrations' -%}` est dans theme.liquid
- Rechargez la page après configuration des metafields
- Attendez 2-3 minutes pour la propagation

## ✅ RÉSULTAT ATTENDU

Après configuration complète:
- **4 trackers gratuits** actifs (Clarity, Hotjar, GA4, Meta)
- **Dashboards** recevant des données en temps réel
- **Console** montrant ✅ pour tous les trackers
- **Notifications Slack** pour les événements importants
