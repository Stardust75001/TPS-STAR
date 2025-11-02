#!/bin/bash

# TPS-STAR Quick Integration Test
# Vérifie rapidement les corrections appliquées

echo "🔧 TPS-STAR Quick Integration Test"
echo "=================================="

# Test 1: Vérifier que le debug metafields est présent
echo "1. 🔍 Vérification debug metafields dans theme.liquid..."
if grep -q "console.log('TPS mf:'" layout/theme.liquid; then
    echo "   ✅ Debug metafields ajouté"
else
    echo "   ❌ Debug metafields manquant"
fi

# Test 2: Vérifier que Sentry statique est supprimé
echo "2. 🧹 Vérification suppression Sentry statique..."
if ! grep -q "sentry-init.js" layout/theme.liquid; then
    echo "   ✅ Sentry statique supprimé"
else
    echo "   ❌ Sentry statique encore présent"
fi

# Test 3: Vérifier les logs Clarity et Hotjar
echo "3. 📊 Vérification logs Clarity et Hotjar..."
if grep -q "🪟 Clarity loaded:" snippets/integrations.liquid; then
    echo "   ✅ Log Clarity ajouté"
else
    echo "   ❌ Log Clarity manquant"
fi

if grep -q "🔥 Hotjar loaded:" snippets/integrations.liquid; then
    echo "   ✅ Log Hotjar ajouté"
else
    echo "   ❌ Log Hotjar manquant"
fi

# Test 4: Vérifier le debug Meta Pixel
echo "4. 🎯 Vérification debug Meta Pixel..."
if grep -q "console.log('\[TPS\] meta id:'" snippets/integrations.liquid; then
    echo "   ✅ Debug Meta Pixel ajouté"
else
    echo "   ❌ Debug Meta Pixel manquant"
fi

# Test 5: Vérifier le Makefile
echo "5. ⚙️ Vérification Makefile audit..."
if [ -f "Makefile" ] && grep -q "audit:" Makefile; then
    echo "   ✅ Makefile avec règle audit créé"
else
    echo "   ❌ Makefile audit manquant"
fi

# Test 6: Corriger l'URL Hotjar dans integrations.liquid
echo "6. 🔥 Correction URL Hotjar..."
if grep -q "https://static.hotjar.com/c/hotjar-" snippets/integrations.liquid; then
    echo "   ✅ URL Hotjar corrigée"
else
    echo "   ❌ URL Hotjar à corriger"
fi

echo ""
echo "🎯 Tests terminés. Prochaines étapes :"
echo "   1. Configurer les metafields Shopify (namespace: custom_integrations)"
echo "   2. Déployer les fichiers modifiés vers le thème"
echo "   3. Tester avec TPS.debug.enable() dans la console"
echo "   4. Vérifier les dashboards des plateformes"
echo ""
echo "📋 Metafields requis :"
echo "   - ga4_token: G-E4NPI2ZZM3"
echo "   - meta_pixel_id: 1973238620087976"
echo "   - sentry_dsn: votre DSN complet"
echo "   - cloudflare_beacon_token: 21fd2470..."
echo "   - clarity_id: tzvd9w6rjs"
echo "   - hotjar_id: 6564192"
