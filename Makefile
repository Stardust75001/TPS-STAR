# TPS-STAR Makefile - Management des workflows et audits
# Automatisation des tâches de développement et d'audit

.PHONY: audit test deploy clean setup

# === AUDIT ET VALIDATION ===
audit:
	@echo "🔎 Lancement de l'audit des trackers TPS-STAR..."
	@gh workflow run "🧩 Audit Trackers (GA4 / Meta / Ahrefs / Cloudflare / Sentry)" -f path="/"
	@echo "✅ Workflow lancé. Ouvre l'onglet Actions du repo pour voir les résultats."
	@echo "📊 Tableaux de bord à vérifier :"
	@echo "   - GA4: https://analytics.google.com/"
	@echo "   - Meta Business: https://business.facebook.com/events_manager"
	@echo "   - Microsoft Clarity: https://clarity.microsoft.com/"
	@echo "   - Hotjar: https://insights.hotjar.com/"
	@echo "   - Sentry: https://sentry.io/"

# === TESTS LOCAUX ===
test:
	@echo "🧪 Tests locaux TPS-STAR..."
	@if [ -f "./test-clarity-integration.sh" ]; then \
		chmod +x ./test-clarity-integration.sh && ./test-clarity-integration.sh; \
	else \
		echo "❌ Fichier test-clarity-integration.sh non trouvé"; \
	fi
	@if [ -f "./validate_credentials.py" ]; then \
		python3 ./validate_credentials.py; \
	else \
		echo "❌ Fichier validate_credentials.py non trouvé"; \
	fi

# === GÉNÉRATION DE RAPPORTS ===
report:
	@echo "📋 Génération du rapport PDF TPS-STAR..."
	@if [ -f "./generate_pdf.sh" ]; then \
		chmod +x ./generate_pdf.sh && ./generate_pdf.sh; \
	else \
		echo "❌ Générateur PDF non trouvé"; \
	fi

# === SETUP ET CONFIGURATION ===
setup:
	@echo "⚙️ Configuration initiale TPS-STAR..."
	@if [ -f "./setup_credentials.sh" ]; then \
		chmod +x ./setup_credentials.sh && ./setup_credentials.sh; \
	else \
		echo "❌ Script de setup non trouvé"; \
	fi
	@echo "📝 Vérifiez les metafields Shopify (namespace: custom_integrations)"

# === DÉPLOIEMENT ===
deploy:
	@echo "🚀 Déploiement des fichiers vers Shopify..."
	@echo "⚠️  Assurez-vous que Shopify CLI est configuré"
	@echo "📁 Fichiers à déployer :"
	@echo "   - snippets/integrations.liquid"
	@echo "   - snippets/tracking-analytics.liquid"
	@echo "   - assets/tps-tracking.js"
	@echo "   - layout/theme.liquid"

# === NETTOYAGE ===
clean:
	@echo "🧹 Nettoyage des fichiers temporaires..."
	@rm -f *.tmp *.log
	@rm -rf __pycache__/
	@echo "✅ Nettoyage terminé"

# === AIDE ===
help:
	@echo "📚 TPS-STAR Makefile - Commandes disponibles :"
	@echo ""
	@echo "  make audit    - Lance l'audit complet des trackers"
	@echo "  make test     - Execute les tests locaux"
	@echo "  make report   - Génère le rapport PDF"
	@echo "  make setup    - Configuration initiale"
	@echo "  make deploy   - Guide de déploiement"
	@echo "  make clean    - Nettoie les fichiers temporaires"
	@echo "  make help     - Affiche cette aide"
	@echo ""
	@echo "🔗 Liens utiles :"
	@echo "   - Repo: https://github.com/Stardust75001/TPS-STAR"
	@echo "   - Docs: ./docs/"
	@echo "   - Tests: ./test-*.html"

# Par défaut, afficher l'aide
.DEFAULT_GOAL := help
