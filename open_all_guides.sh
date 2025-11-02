#!/usr/bin/env bash

echo "📖 Ouverture de tous les guides PDF TPS-STAR..."
echo ""

# Ouvrir tous les guides PDF dans l'ordre de recommandation
if [ -f "TPS-STAR-Master-Dashboard-Guide.pdf" ]; then
    echo "🎯 Ouverture du GUIDE MAÎTRE (recommandé)..."
    open "TPS-STAR-Master-Dashboard-Guide.pdf"
    sleep 1
fi

if [ -f "TPS-STAR-Actions-Rapides-Guide.pdf" ]; then
    echo "⚡ Ouverture du Guide d'Actions Rapides..."
    open "TPS-STAR-Actions-Rapides-Guide.pdf"
    sleep 1
fi

if [ -f "TPS-STAR-Dashboard-Verification-Guide.pdf" ]; then
    echo "📋 Ouverture du Guide de Vérification..."
    open "TPS-STAR-Dashboard-Verification-Guide.pdf"
    sleep 1
fi

echo ""
echo "📚 Tous les guides PDF sont maintenant ouverts !"
echo ""
echo "🎯 GUIDE RECOMMANDÉ : Commencez par le GUIDE MAÎTRE"
echo "   → Il contient TOUT ce dont vous avez besoin"
echo "   → 9 sections complètes avec scripts de test"
echo "   → Solutions de dépannage intégrées"
echo ""
echo "🚀 Bonne vérification de vos dashboards TPS-STAR !"
