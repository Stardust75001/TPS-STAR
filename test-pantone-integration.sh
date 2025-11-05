#!/bin/bash

echo "🧪 Test Integration Pantone - TPS-STAR"
echo "====================================="

echo "✅ CHECKLIST INTÉGRATION :"
echo ""
echo "1. 📁 Fichier snippet créé :"
if [ -f "snippets/product-variant-color-selector.liquid" ]; then
    echo "   ✅ snippets/product-variant-color-selector.liquid existe"
else
    echo "   ❌ snippets/product-variant-color-selector.liquid manquant"
fi

echo ""
echo "2. 📝 Template modifié :"
if grep -q "product-variant-color-selector" "sections/template-product.liquid"; then
    echo "   ✅ Render ajouté dans template-product.liquid"
else
    echo "   ❌ Render non trouvé dans template-product.liquid"
fi

echo ""
echo "3. 🔧 PROCHAINES ÉTAPES SHOPIFY :"
echo "   • Uploader snippets/product-variant-color-selector.liquid"
echo "   • Créer metafield 'Product Color Variants'"
echo "   • Assigner couleurs Pantone aux produits"
echo "   • Vérifier noms des variantes = noms Pantone"
echo ""
echo "4. 🎨 TEST PRODUIT :"
echo "   • Aller sur un produit avec variantes couleur"
echo "   • Vérifier affichage du sélecteur Pantone"
echo "   • Tester changement de couleur"
