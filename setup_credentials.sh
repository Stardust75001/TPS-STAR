#!/bin/bash
"""
TPS-STAR Analytics Credentials Setup Script
===========================================

This script helps you configure all the necessary API credentials
for the weekly analytics reporting system.

Run this script to set up:
- GitHub repository secrets
- Local environment variables
- API credential files
- Service account configurations

Usage:
    chmod +x setup_credentials.sh
    ./setup_credentials.sh
"""

echo "🚀 TPS-STAR Analytics Credentials Setup"
echo "======================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check required tools
echo "🔍 Checking required tools..."
if ! command_exists gh; then
    echo -e "${RED}❌ GitHub CLI (gh) is not installed. Please install it first.${NC}"
    echo "   Install: brew install gh"
    exit 1
fi

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed. Please install it first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All required tools are available${NC}"
echo ""

# Create directories
echo "📁 Creating necessary directories..."
mkdir -p credentials
mkdir -p reports
mkdir -p reports/charts
mkdir -p reports/data

echo -e "${GREEN}✅ Directories created${NC}"
echo ""

# GitHub Secrets Setup
echo "🔐 Setting up GitHub repository secrets..."
echo "Please provide the following information for GitHub secrets:"
echo ""

read -p "🌐 TPS Domain (e.g., tps-star.com): " TPS_DOMAIN
read -p "📊 GA4 Property ID: " GA4_PROPERTY_ID
read -p "📈 Amplitude API Key: " AMPLITUDE_API_KEY
read -s -p "🔑 Amplitude Secret Key: " AMPLITUDE_SECRET_KEY
echo ""
read -p "🔥 Hotjar API Key: " HOTJAR_API_KEY
read -p "🔍 Microsoft Clarity API Key: " CLARITY_API_KEY
read -p "🚨 Sentry Auth Token: " SENTRY_AUTH_TOKEN
read -p "🏢 Sentry Organization: " SENTRY_ORG
read -p "📦 Sentry Project: " SENTRY_PROJECT
read -p "🛒 Shopify Store Name (without .myshopify.com): " SHOPIFY_STORE
read -s -p "🔐 Shopify Access Token: " SHOPIFY_ACCESS_TOKEN
echo ""
read -p "💬 Slack Webhook URL (optional): " SLACK_WEBHOOK_URL

# Set GitHub secrets
echo ""
echo "🔄 Setting GitHub repository secrets..."

gh secret set TPS_DOMAIN --body="$TPS_DOMAIN"
gh secret set GA4_PROPERTY_ID --body="$GA4_PROPERTY_ID"
gh secret set AMPLITUDE_API_KEY --body="$AMPLITUDE_API_KEY"
gh secret set AMPLITUDE_SECRET_KEY --body="$AMPLITUDE_SECRET_KEY"
gh secret set HOTJAR_API_KEY --body="$HOTJAR_API_KEY"
gh secret set CLARITY_API_KEY --body="$CLARITY_API_KEY"
gh secret set SENTRY_AUTH_TOKEN --body="$SENTRY_AUTH_TOKEN"
gh secret set SENTRY_ORG --body="$SENTRY_ORG"
gh secret set SENTRY_PROJECT --body="$SENTRY_PROJECT"
gh secret set SHOPIFY_STORE_URL --body="https://$SHOPIFY_STORE.myshopify.com"
gh secret set SHOPIFY_ACCESS_TOKEN --body="$SHOPIFY_ACCESS_TOKEN"

if [ ! -z "$SLACK_WEBHOOK_URL" ]; then
    gh secret set SLACK_WEBHOOK_URL --body="$SLACK_WEBHOOK_URL"
fi

echo -e "${GREEN}✅ GitHub secrets configured${NC}"
echo ""

# Create local environment file
echo "📝 Creating local environment file..."
cat > .env << EOF
# TPS-STAR Analytics Environment Variables
# =======================================
# Generated on $(date)

# Basic Configuration
TPS_DOMAIN=$TPS_DOMAIN
WEEK_OFFSET=0

# Google Analytics 4
GA4_PROPERTY_ID=$GA4_PROPERTY_ID

# Amplitude Product Analytics
AMPLITUDE_API_KEY=$AMPLITUDE_API_KEY
AMPLITUDE_SECRET_KEY=$AMPLITUDE_SECRET_KEY

# Hotjar User Behavior
HOTJAR_API_KEY=$HOTJAR_API_KEY

# Microsoft Clarity
CLARITY_API_KEY=$CLARITY_API_KEY

# Sentry Error Tracking
SENTRY_AUTH_TOKEN=$SENTRY_AUTH_TOKEN
SENTRY_ORG=$SENTRY_ORG
SENTRY_PROJECT=$SENTRY_PROJECT

# Shopify Store Data
SHOPIFY_STORE_URL=https://$SHOPIFY_STORE.myshopify.com
SHOPIFY_ACCESS_TOKEN=$SHOPIFY_ACCESS_TOKEN

# Slack Notifications (optional)
SLACK_WEBHOOK_URL=$SLACK_WEBHOOK_URL
EOF

echo -e "${GREEN}✅ Environment file created: .env${NC}"
echo ""

# Google Analytics Service Account Setup
echo "🔑 Google Analytics Service Account Setup"
echo "========================================="
echo ""
echo "To complete GA4 integration, you need to:"
echo "1. 🌐 Visit: https://console.cloud.google.com/"
echo "2. 📊 Enable Google Analytics Reporting API"
echo "3. 🔐 Create a service account"
echo "4. 📥 Download the JSON credentials file"
echo "5. 📂 Save it as 'credentials/ga4-service-account.json'"
echo ""
read -p "Have you downloaded the GA4 service account JSON file? (y/n): " ga4_ready

if [ "$ga4_ready" = "y" ] || [ "$ga4_ready" = "Y" ]; then
    echo "📂 Please place your GA4 service account JSON file at:"
    echo "   📁 credentials/ga4-service-account.json"
    echo ""
    echo "🔧 Then add the service account email to your GA4 property with Viewer permissions"
    echo ""
fi

# Test API connections
echo "🧪 Testing API connections..."
echo ""

# Create test script
cat > test_connections.py << 'EOF'
#!/usr/bin/env python3
import os
import requests
import json
from datetime import datetime

def test_amplitude():
    api_key = os.getenv('AMPLITUDE_API_KEY')
    if not api_key:
        return "❌ API key not found"

    # Test endpoint (you may need to adjust this)
    url = "https://amplitude.com/api/2/users"
    headers = {'Authorization': f'Bearer {api_key}'}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return "✅ Connected successfully"
        else:
            return f"⚠️ HTTP {response.status_code}"
    except Exception as e:
        return f"❌ Connection failed: {str(e)}"

def test_sentry():
    auth_token = os.getenv('SENTRY_AUTH_TOKEN')
    org = os.getenv('SENTRY_ORG')

    if not auth_token or not org:
        return "❌ Credentials not found"

    url = f"https://sentry.io/api/0/organizations/{org}/"
    headers = {'Authorization': f'Bearer {auth_token}'}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return "✅ Connected successfully"
        else:
            return f"⚠️ HTTP {response.status_code}"
    except Exception as e:
        return f"❌ Connection failed: {str(e)}"

def test_shopify():
    store_url = os.getenv('SHOPIFY_STORE_URL')
    access_token = os.getenv('SHOPIFY_ACCESS_TOKEN')

    if not store_url or not access_token:
        return "❌ Credentials not found"

    url = f"{store_url}/admin/api/2023-07/shop.json"
    headers = {'X-Shopify-Access-Token': access_token}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return "✅ Connected successfully"
        else:
            return f"⚠️ HTTP {response.status_code}"
    except Exception as e:
        return f"❌ Connection failed: {str(e)}"

if __name__ == "__main__":
    print("🧪 Testing API Connections")
    print("=" * 30)
    print(f"📈 Amplitude: {test_amplitude()}")
    print(f"🚨 Sentry: {test_sentry()}")
    print(f"🛒 Shopify: {test_shopify()}")
    print("")
    print("Note: GA4, Hotjar, and Clarity require additional setup")
EOF

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Run connection tests
python3 test_connections.py

# Cleanup test script
rm test_connections.py

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "✅ What's been configured:"
echo "   🔐 GitHub repository secrets"
echo "   📝 Local environment file (.env)"
echo "   📁 Directory structure"
echo ""
echo "🔄 Next steps:"
echo "   1. 📊 Complete GA4 service account setup"
echo "   2. 🧪 Test the report generator: python3 scripts/generate_weekly_report.py"
echo "   3. ⚡ Trigger the workflow: gh workflow run weekly-analytics-report.yml"
echo ""
echo "📚 Documentation: Check scripts/README.md for detailed setup guides"
echo ""
echo -e "${GREEN}🚀 Your analytics system is ready to go!${NC}"
