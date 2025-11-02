#!/bin/bash

# TPS-STAR - Configuration Rapide Clarity & Hotjar
# Ce script vous guide pour configurer les métafields Shopify

echo "🎯 TPS-STAR - Configuration Clarity & Hotjar"
echo "============================================="

echo ""
echo "📋 IDs à configurer dans Shopify Admin:"
echo ""
echo "✅ Microsoft Clarity ID: tzvd9w6rjs"
echo "✅ Hotjar ID: 6564192"
echo ""

echo "🔧 Étapes de configuration:"
echo ""
echo "1. Allez dans Shopify Admin"
echo "2. Paramètres → Métadonnées → Boutique"
echo "3. Cliquez sur 'Ajouter une définition'"
echo ""

echo "📝 Première métafield - Microsoft Clarity:"
echo "   • Namespace: custom_integrations"
echo "   • Clé: Clarity_ID"
echo "   • Type: Single line text"
echo "   • Valeur: tzvd9w6rjs"
echo ""

echo "📝 Deuxième métafield - Hotjar:"
echo "   • Namespace: custom_integrations"
echo "   • Clé: Hotjar_ID"
echo "   • Type: Single line text"
echo "   • Valeur: 6564192"
echo ""

echo "🧪 Test après configuration:"
echo "1. Ouvrez votre site Shopify"
echo "2. Console navigateur (F12)"
echo "3. Tapez: TPS.debug.enable()"
echo "4. Vérifiez les logs pour Clarity et Hotjar"
echo ""

echo "📊 Dashboards à surveiller:"
echo "• Microsoft Clarity: https://clarity.microsoft.com"
echo "• Hotjar: https://insights.hotjar.com"
echo ""

echo "💡 Test local:"
echo "Ouvrez test-clarity-hotjar.html dans votre navigateur"
echo "pour tester les codes avant déploiement."
echo ""

# Demander si l'utilisateur veut ouvrir le fichier de test
read -p "Voulez-vous ouvrir le fichier de test maintenant ? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "test-clarity-hotjar.html"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "test-clarity-hotjar.html"
    else
        echo "Ouvrez manuellement: test-clarity-hotjar.html"
    fi
fi

echo ""
echo "✅ Configuration terminée !"
echo "🚀 Vos codes Clarity et Hotjar sont prêts à être déployés !"
