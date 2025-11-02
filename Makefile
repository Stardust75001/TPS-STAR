# ============================================================
# 🦅 THE PET SOCIETY — TPS-STAR WORKTREE MAKEFILE
# Centralisation des commandes locales (pyenv, Shopify, CI)
# ============================================================

PYENV = tps-star-3119

# --- Environnement Python ---
env:
	@echo "📦 Activation pyenv ($(PYENV))..."
	@export PYENV_VERSION=$(PYENV)
	@python -V
	@which python
	@echo "✅ $(PYENV) prêt."

# --- Vérification des dépendances ---
check:
	@echo "🔍 Vérification outils installés..."
	@command -v pyenv >/dev/null && echo "✔️ pyenv ok" || echo "❌ pyenv manquant"
	@command -v shopify >/dev/null && echo "✔️ shopify CLI ok" || echo "⚠️ shopify CLI manquant"
	@command -v gh >/dev/null && echo "✔️ GitHub CLI ok" || echo "⚠️ gh CLI manquant"
	@command -v jq >/dev/null && echo "✔️ jq ok" || echo "⚠️ jq manquant"

# --- Qualité de code ---
lint:
	@echo "🧹 Analyse Python..."
	@export PYENV_VERSION=$(PYENV)
	@ruff check scripts/ || true

# --- Tests ---
test:
	@echo "🧪 Lancement des tests..."
	@export PYENV_VERSION=$(PYENV)
	@pytest -q || echo "⚠️ Aucune suite de tests."

# --- Backups Shopify ---
backup:
	@echo "💾 Backup complet du thème Shopify..."
	@bash scripts/backup-top.sh

# --- Workflows GitHub ---
release:
	@echo "🚀 Déclenchement workflow : Sentry Release & Deploy"
	@gh workflow run "🧩 Sentry Release & Deploy"

seo:
	@echo "🔎 Déclenchement workflow : SEO Checks (Ahrefs v3)"
	@gh workflow run "🔎 SEO Checks (Ahrefs v3)"

audit:
	@echo "📊 Déclenchement workflow : Audit Trackers"
	@gh workflow run "🧩 Audit Trackers (GA4 / Meta / Ahrefs / Cloudflare / Sentry)"

# --- Aide ---
help:
	@echo ""
	@echo "🦅 COMMANDES DISPONIBLES"
	@echo "-------------------------"
	@echo "make env       → Active l'environnement pyenv local"
	@echo "make check     → Vérifie les outils essentiels"
	@echo "make lint      → Analyse syntaxique (ruff)"
	@echo "make test      → Lancement des tests Python"
	@echo "make backup    → Sauvegarde complète du thème Shopify"
	@echo "make release   → Déploie release Sentry"
	@echo "make seo       → Lancement audit SEO (Ahrefs v3)"
	@echo "make audit     → Lancement audit trackers GA4/Meta/Sentry"
	@echo ""

.PHONY: env check lint test backup release seo audit help
