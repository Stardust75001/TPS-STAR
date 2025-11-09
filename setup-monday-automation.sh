#!/bin/bash

echo "📅 TPS-STAR Monday Morning Automation Setup"
echo "=========================================="
echo ""

# Chemin absolu vers le dossier de travail
WORK_DIR="/Users/asc/Shopify/TPS STAR/TPS-STAR-WORKTREE"

echo "📂 Working directory: $WORK_DIR"
echo ""

# Créer les tâches cron pour lundi matin
echo "⏰ Configuration des tâches automatiques..."

# Tâche 1: Rapport de production complet à 8h00
CRON_PRODUCTION="0 8 * * 1 cd '$WORK_DIR' && ./tps-production-ready.sh >> /tmp/tps-monday-production.log 2>&1"

# Tâche 2: Email de confirmation à 8h05 
CRON_CONFIRMATION="5 8 * * 1 cd '$WORK_DIR' && ./tps-send-working.sh >> /tmp/tps-monday-confirmation.log 2>&1"

# Nettoyer les anciennes tâches TPS
echo "🧹 Nettoyage des anciennes tâches..."
crontab -l 2>/dev/null | grep -v "tps-" | grep -v "TPS" | crontab -

# Ajouter les nouvelles tâches
echo "➕ Ajout des nouvelles tâches..."
(crontab -l 2>/dev/null; echo "$CRON_PRODUCTION"; echo "$CRON_CONFIRMATION") | crontab -

echo ""
echo "✅ AUTOMATION CONFIGURÉE!"
echo ""
echo "📋 Tâches programmées pour chaque lundi:"
echo "   🎯 8:00 AM - Rapport de production complet (TPSPROD)"
echo "   ✅ 8:05 AM - Email de confirmation (TPSWORKING)"
echo ""
echo "📧 Destinataires:"
echo "   • alexjet2000@gmail.com"  
echo "   • asc2000@gmail.com"
echo "   • alfalconx@gmail.com"
echo ""
echo "📁 Logs disponibles dans:"
echo "   • /tmp/tps-monday-production.log"
echo "   • /tmp/tps-monday-confirmation.log"
echo ""
echo "📋 Configuration cron actuelle:"
crontab -l | grep -E "(tps-|TPS)" || echo "Aucune tâche TPS trouvée"
