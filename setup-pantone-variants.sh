#!/bin/bash

echo "🎨 Configuration Pantone Variants - TPS-STAR"
echo "=============================================="

echo "1. 📋 Configuration Shopify requise :"
echo ""
echo "A. Créer un nouveau Metafield pour les PRODUITS :"
echo "   Nom: Product Color Variants"
echo "   Namespace: custom.color_variants"
echo "   Type: List of metaobjects"
echo "   Metaobject: Pantone Color"
echo ""
echo "B. Liquid Template pour variant selector :"
echo "   Fichier: snippets/product-variant-color-selector.liquid"
echo ""
echo "🔧 Générations des fichiers..."
