#!/bin/zsh
cd ~/Shopify/TPS\ STAR/PRODUCTS/STOCK\ -\ CATALOG\ MANAGEMENT/
# Activer ou créer l’environnement
source .venv/bin/activate 2>/dev/null || python3 -m venv .venv && source .venv/bin/activate
# Installation silencieuse des dépendances essentielles
pip install -q pandas openpyxl requests
# Exécution du script de calculs et génération Excel
python3 update_dashboard_v2.py
