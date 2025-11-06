#!/bin/bash

echo "🔗 Connexion Pantone aux Produits - TPS-STAR"
echo "=============================================="

echo "📋 ÉTAPES SHOPIFY ADMIN :"
echo ""
echo "1. 🎨 CRÉER LE METAFIELD PRODUIT :"
echo "   • Aller dans : Settings > Metafields and metaobjects"
echo "   • Onglet : Products"
echo "   • Click : Add definition"
echo "   • Nom : Product Color Variants"
echo "   • Namespace : custom.color_variants"  
echo "   • Type : List of metaobjects"
echo "   • Metaobject type : Pantone Color"
echo "   • Cocher : Storefront API access"
echo ""
echo "2. 📦 ASSIGNER AUX PRODUITS :"
echo "   • Aller sur chaque produit"
echo "   • Scroll vers : Metafields"
echo "   • Product Color Variants : Sélectionner les couleurs Pantone"
echo ""
echo "3. 🏷️ NOMMER LES VARIANTES :"
echo "   • Dans les variantes du produit"
echo "   • Option name : 'Color' ou 'Couleur'"
echo "   • Values : Utiliser exactement les mêmes noms que dans Pantone Color > Name"
echo ""
echo "4. 📁 INSTALLER LE TEMPLATE :"
echo "   • Upload : snippets/product-variant-color-selector.liquid"
echo "   • Modifier : sections/product-form.liquid ou templates/product.liquid"
echo ""
echo "✅ VÉRIFICATIONS :"
echo "   • Noms des couleurs identiques : Pantone.Name = Variant.Option"
echo "   • Codes Hex valides dans Pantone metaobject"
echo "   • Metafield correctement assigné aux produits"

# Créer un fichier d'aide pour le mapping
cat > pantone-variant-mapping-example.json << 'JSON'
{
  "exemple_mapping": {
    "pantone_metaobject": {
      "name": "Midnight Black",
      "code": "19-3911 TPX", 
      "hex": "#2B2B2B"
    },
    "product_variant": {
      "option1": "Color",
      "option1_value": "Midnight Black",
      "option2": "Size", 
      "option2_value": "M"
    }
  },
  "important": "Le 'name' du metaobject doit être identique à 'option1_value' de la variante"
}
JSON

echo ""
echo "📄 Fichier créé : pantone-variant-mapping-example.json"
echo "🎯 Template créé : snippets/product-variant-color-selector.liquid"
