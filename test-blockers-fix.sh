#!/bin/bash

# TPS-STAR Blockers Fix Validation
# Teste les 4 corrections critiques appliquées

echo "🔧 TPS-STAR - Validation des corrections des 4 blockers"
echo "====================================================="

echo ""
echo "1. 🔍 Métafields Keys (lowercase + fallback)"
echo "   Vérification de la nouvelle syntaxe robust..."

# Test 1: Vérifier la nouvelle syntaxe des metafields
if grep -q "integ.ga4_token.*default.*integ.GA4_Token" snippets/integrations.liquid; then
    echo "   ✅ ga4_token: lowercase → CamelCase fallback"
else
    echo "   ❌ ga4_token: syntaxe manquante"
fi

if grep -q "integ.meta_pixel_id.*default.*integ.Meta_Pixel_ID" snippets/integrations.liquid; then
    echo "   ✅ meta_pixel_id: lowercase → CamelCase fallback"
else
    echo "   ❌ meta_pixel_id: syntaxe manquante"
fi

if grep -q "integ.clarity_id.*default.*integ.Clarity_ID" snippets/integrations.liquid; then
    echo "   ✅ clarity_id: lowercase → CamelCase fallback"
else
    echo "   ❌ clarity_id: syntaxe manquante"
fi

echo ""
echo "2. 🛡️ Sentry (syntaxe + SRI)"
echo "   Vérification du bloc Sentry corrigé..."

# Test 2: Vérifier que Sentry n'a plus d'erreur de syntaxe
if grep -q "Sentry.init({" snippets/integrations.liquid && ! grep -q "integrity" snippets/integrations.liquid; then
    echo "   ✅ Sentry: syntaxe corrigée, plus de SRI integrity"
else
    echo "   ❌ Sentry: problème de syntaxe ou SRI encore présent"
fi

if grep -q ".catch(function(){" snippets/integrations.liquid; then
    echo "   ✅ Sentry: error handling proper"
else
    echo "   ❌ Sentry: error handling manquant"
fi

echo ""
echo "3. 📊 Amplitude (SRI supprimé)"
echo "   Vérification que l'integrity est supprimée..."

# Test 3: Vérifier qu'Amplitude n'a plus d'integrity
if grep -q "amplitude" snippets/integrations.liquid && ! grep -q "r.integrity=" snippets/integrations.liquid; then
    echo "   ✅ Amplitude: SRI integrity supprimée"
else
    echo "   ❌ Amplitude: SRI integrity encore présente"
fi

echo ""
echo "4. 🎯 GTM vs GA4 (priorité GTM)"
echo "   Vérification de la logique de priorité..."

# Test 4: Vérifier la logique GTM prioritaire
if grep -q "if (cfg.gtm_id.*!window.dataLayer)" snippets/integrations.liquid; then
    echo "   ✅ GTM: chargé en priorité"
else
    echo "   ❌ GTM: logique de priorité incorrecte"
fi

if grep -q "else if (cfg.ga4_token.*!cfg.gtm_id)" snippets/integrations.liquid; then
    echo "   ✅ GA4: chargé seulement si pas de GTM"
else
    echo "   ❌ GA4: logique de fallback incorrecte"
fi

echo ""
echo "📋 RÉSUMÉ DES CORRECTIONS"
echo "========================"
echo ""
echo "Après déploiement, vous devriez voir en console :"
echo ""
echo "✅ Résolutions attendues :"
echo "   - Plus d'erreur 'integrity metadata check' (Sentry + Amplitude)"
echo "   - Plus de 'ReferenceError: Sentry is not defined'"
echo "   - Plus de 'Invalid PixelID: null' (si metafields configurés)"
echo "   - Logs: '[TPS-STAR] Sentry initialized'"
echo "   - Logs: '🪟 Clarity loaded: tzvd9w6rjs'"
echo "   - Logs: '🔥 Hotjar loaded: 6564192'"
echo ""
echo "🔧 METAFIELDS SHOPIFY REQUIS :"
echo "   Namespace: custom_integrations"
echo "   Type: Single line text, Storefront API access: Active"
echo ""
echo "   Clés lowercase (recommandées) :"
echo "   ├── ga4_token → 'G-E4NPI2ZZM3'"
echo "   ├── meta_pixel_id → '1973238620087976'"
echo "   ├── sentry_dsn → 'https://your-dsn@sentry.io'"
echo "   ├── cloudflare_beacon_token → '21fd2470...'"
echo "   ├── clarity_id → 'tzvd9w6rjs'"
echo "   └── hotjar_id → '6564192'"
echo ""
echo "   ⚠️  Vos anciennes clés CamelCase (GA4_Token, etc.) continuent"
echo "       de fonctionner grâce au fallback automatique"
echo ""
echo "🧪 Test final : Déployez → Console → TPS.debug.enable()"
