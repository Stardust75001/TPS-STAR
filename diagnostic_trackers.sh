#!/usr/bin/env bash

echo "🔍 TPS-STAR DIAGNOSTIC COMPLET"
echo "================================"
echo ""

echo "📋 PROBLÈME IDENTIFIÉ :"
echo "   Votre test sur 'test-tps-debug.html' montre ❌ pour tous les trackers"
echo "   C'est NORMAL car ce fichier ne charge QUE l'initialisation TPS"
echo "   Il ne charge PAS les vrais trackers (gtag, fbq, clarity, hj)"
echo ""

echo "🧪 TESTS À EFFECTUER :"
echo ""

echo "1. 📁 TEST AVEC LE FICHIER COMPLET :"
echo "   - Ouvrez : test-tps-complete.html (vient d'être créé)"
echo "   - Celui-ci charge TOUS les trackers réels"
echo "   - Vous devriez voir 4/4 trackers ✅"
echo ""

echo "2. 🌐 TEST SUR VOTRE VRAI SITE SHOPIFY :"
echo "   - Allez sur votre site Shopify en production"
echo "   - Ouvrez la console (F12)"
echo "   - Tapez exactement :"
echo ""
echo "   TPS.debug.enable()"
echo "   puis :"
echo "   console.log('Clarity:', typeof clarity === 'function' ? '✅' : '❌');"
echo "   console.log('Hotjar:', typeof hj === 'function' ? '✅' : '❌');"
echo "   console.log('GA4:', typeof gtag === 'function' ? '✅' : '❌');"
echo "   console.log('Meta:', typeof fbq === 'function' ? '✅' : '❌');"
echo ""

echo "3. 🔧 SI TOUJOURS ❌ SUR LE SITE SHOPIFY :"
echo "   Vérifiez vos metafields Shopify :"
echo ""

# Script pour vérifier les metafields
cat << 'EOF'
// DIAGNOSTIC AVANCÉ - Dans la console de votre site Shopify :

console.group('🔍 TPS-STAR Metafields Diagnostic');

// Vérifier la configuration TPS
console.log('TPS Config:', window.tpsConfig || 'MISSING');

// Vérifier chaque metafield individuellement
const expectedFields = {
  'clarity_id': 'tzvd9w6rjs',
  'hotjar_id': '6564192',
  'ga4_token': 'G-E4NPI2ZZM3',
  'meta_pixel_id': '1973238620087976'
};

Object.entries(expectedFields).forEach(([field, expectedValue]) => {
  const actualValue = window.tpsConfig?.[field];
  const status = actualValue === expectedValue ? '✅' : '❌';
  console.log(`${status} ${field}:`, actualValue, `(expected: ${expectedValue})`);
});

console.groupEnd();

// Test de chargement des scripts
console.group('🔍 Script Loading Status');
console.log('Scripts loaded in head/body:');
Array.from(document.querySelectorAll('script[src]')).forEach(script => {
  const src = script.src.toLowerCase();
  if (src.includes('gtag') || src.includes('facebook') || src.includes('clarity') || src.includes('hotjar')) {
    console.log('✅ Found:', src);
  }
});
console.groupEnd();
EOF

echo ""
echo "4. 📝 VÉRIFICATION DES METAFIELDS SHOPIFY :"
echo "   Dans votre admin Shopify :"
echo "   Settings → Custom data → Metafields"
echo "   Namespace: 'custom_integrations'"
echo "   Vérifiez que vous avez :"
echo "   - clarity_id = tzvd9w6rjs"
echo "   - hotjar_id = 6564192"
echo "   - ga4_token = G-E4NPI2ZZM3"
echo "   - meta_pixel_id = 1973238620087976"
echo ""

echo "5. 🎯 SOLUTION PROBABLE :"
echo "   Si le test-tps-complete.html fonctionne (4/4 ✅)"
echo "   Mais votre site Shopify montre ❌"
echo "   → Le problème est dans vos metafields Shopify"
echo "   → Ils ne sont pas configurés ou mal nommés"
echo ""

echo "📞 PROCHAINES ÉTAPES :"
echo "   1. Testez test-tps-complete.html en premier"
echo "   2. Si ça marche, vérifiez vos metafields Shopify"
echo "   3. Assurez-vous que Storefront API access est activé"
echo "   4. Testez à nouveau sur votre site Shopify"
echo ""

echo "🚀 Une fois tous les metafields corrects, votre site montrera 4/4 ✅ !"
