#!/bin/bash

# TPS-STAR PDF Report Generator - Installation et Génération
# Usage: ./generate_pdf.sh

echo "🚀 TPS-STAR PDF Report Generator"
echo "=================================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Installez Python3 d'abord."
    exit 1
fi

# Vérifier si wkhtmltopdf est installé (requis pour pdfkit)
if ! command -v wkhtmltopdf &> /dev/null; then
    echo "📦 Installation de wkhtmltopdf..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install wkhtmltopdf
        else
            echo "❌ Homebrew n'est pas installé. Installez-le d'abord : https://brew.sh"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update && sudo apt-get install -y wkhtmltopdf
    else
        echo "❌ OS non supporté. Installez wkhtmltopdf manuellement."
        exit 1
    fi
fi

# Créer un environnement virtuel si il n'existe pas
if [ ! -d "venv_pdf" ]; then
    echo "🔧 Création de l'environnement virtuel..."
    python3 -m venv venv_pdf
fi

# Activer l'environnement virtuel
echo "⚡ Activation de l'environnement virtuel..."
source venv_pdf/bin/activate

# Installer les dépendances
echo "📦 Installation des dépendances Python..."
pip install --upgrade pip
pip install -r requirements_pdf.txt

# Générer le rapport PDF
echo "📊 Génération du rapport PDF..."
python3 generate_pdf_report.py

# Vérifier si le PDF a été généré
if [ -f "TPS-STAR-Implementation-Report.pdf" ]; then
    echo ""
    echo "🎉 SUCCÈS ! Rapport PDF généré avec succès !"
    echo "📁 Fichier : TPS-STAR-Implementation-Report.pdf"
    echo "📊 Le rapport contient :"
    echo "   • Analyse détaillée de l'implémentation"
    echo "   • Graphiques et visualisations colorées"
    echo "   • ROI et analyse coût-bénéfice"
    echo "   • Recommandations stratégiques"
    echo "   • Timeline de déploiement"
    echo ""
    echo "💡 Le rapport est prêt pour présentation !"

    # Ouvrir le PDF (optionnel)
    read -p "Voulez-vous ouvrir le PDF maintenant ? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            open "TPS-STAR-Implementation-Report.pdf"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            xdg-open "TPS-STAR-Implementation-Report.pdf"
        fi
    fi
else
    echo "❌ Erreur lors de la génération du PDF"
    echo "💡 Vérifiez les messages d'erreur ci-dessus"
fi

# Désactiver l'environnement virtuel
deactivate

echo ""
echo "✨ Script terminé !"
