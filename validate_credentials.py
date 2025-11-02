#!/usr/bin/env python3
"""
Quick Validation Script for TPS-STAR Analytics Credentials
==========================================================

This script validates that all API credentials are properly configured
and can establish connections to the analytics platforms.

Usage:
    python3 validate_credentials.py
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List, Tuple

class CredentialValidator:
    def __init__(self):
        self.results = []
        self.load_environment()

    def load_environment(self):
        """Load environment variables from .env file if it exists"""
        env_file = '.env'
        if os.path.exists(env_file):
            print("📝 Loading environment from .env file...")
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
        else:
            print("⚠️  No .env file found, using system environment variables")

    def test_amplitude(self) -> Tuple[str, str, str]:
        """Test Amplitude API connection"""
        api_key = os.getenv('AMPLITUDE_API_KEY')
        secret_key = os.getenv('AMPLITUDE_SECRET_KEY')

        if not api_key or not secret_key:
            return "❌", "Missing credentials", "Set AMPLITUDE_API_KEY and AMPLITUDE_SECRET_KEY"

        try:
            # Test with Amplitude's export API
            import base64
            credentials = f"{api_key}:{secret_key}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()

            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }

            # Use a simple endpoint that should return project info
            url = "https://amplitude.com/api/2/export"
            params = {
                'start': '20241101',
                'end': '20241101'
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                return "✅", "Connected successfully", "API credentials valid"
            elif response.status_code == 401:
                return "❌", "Authentication failed", "Check API key and secret"
            elif response.status_code == 403:
                return "⚠️", "Access denied", "Verify account permissions"
            else:
                return "⚠️", f"HTTP {response.status_code}", "Check API documentation"

        except requests.exceptions.Timeout:
            return "⚠️", "Connection timeout", "Network or API issue"
        except Exception as e:
            return "❌", f"Connection failed", str(e)

    def test_sentry(self) -> Tuple[str, str, str]:
        """Test Sentry API connection"""
        auth_token = os.getenv('SENTRY_AUTH_TOKEN')
        org = os.getenv('SENTRY_ORG')
        project = os.getenv('SENTRY_PROJECT')

        if not auth_token or not org:
            return "❌", "Missing credentials", "Set SENTRY_AUTH_TOKEN and SENTRY_ORG"

        try:
            headers = {'Authorization': f'Bearer {auth_token}'}
            url = f"https://sentry.io/api/0/organizations/{org}/"

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                org_data = response.json()
                return "✅", "Connected successfully", f"Organization: {org_data.get('name', org)}"
            elif response.status_code == 401:
                return "❌", "Authentication failed", "Check auth token"
            elif response.status_code == 404:
                return "❌", "Organization not found", f"Verify organization slug: {org}"
            else:
                return "⚠️", f"HTTP {response.status_code}", "Check Sentry API status"

        except Exception as e:
            return "❌", "Connection failed", str(e)

    def test_shopify(self) -> Tuple[str, str, str]:
        """Test Shopify API connection"""
        store_url = os.getenv('SHOPIFY_STORE_URL')
        access_token = os.getenv('SHOPIFY_ACCESS_TOKEN')

        if not store_url or not access_token:
            return "❌", "Missing credentials", "Set SHOPIFY_STORE_URL and SHOPIFY_ACCESS_TOKEN"

        try:
            headers = {'X-Shopify-Access-Token': access_token}
            url = f"{store_url}/admin/api/2023-07/shop.json"

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                shop_data = response.json()
                shop_name = shop_data.get('shop', {}).get('name', 'Unknown')
                return "✅", "Connected successfully", f"Store: {shop_name}"
            elif response.status_code == 401:
                return "❌", "Authentication failed", "Check access token"
            elif response.status_code == 404:
                return "❌", "Store not found", "Verify store URL"
            else:
                return "⚠️", f"HTTP {response.status_code}", "Check Shopify API status"

        except Exception as e:
            return "❌", "Connection failed", str(e)

    def test_ga4_credentials(self) -> Tuple[str, str, str]:
        """Test GA4 service account credentials"""
        property_id = os.getenv('GA4_PROPERTY_ID')
        credentials_file = 'credentials/ga4-service-account.json'

        if not property_id:
            return "❌", "Missing property ID", "Set GA4_PROPERTY_ID"

        if not os.path.exists(credentials_file):
            return "❌", "Missing credentials file", f"Create {credentials_file}"

        try:
            with open(credentials_file, 'r') as f:
                credentials = json.load(f)

            required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
            missing_fields = [field for field in required_fields if field not in credentials]

            if missing_fields:
                return "❌", "Invalid credentials file", f"Missing: {', '.join(missing_fields)}"

            if credentials['type'] != 'service_account':
                return "❌", "Wrong credential type", "Expected service_account"

            return "✅", "Credentials file valid", f"Service account: {credentials['client_email']}"

        except json.JSONDecodeError:
            return "❌", "Invalid JSON format", "Check credentials file syntax"
        except Exception as e:
            return "❌", "File access error", str(e)

    def test_github_secrets(self) -> Tuple[str, str, str]:
        """Test if we're running in GitHub Actions with secrets"""
        if os.getenv('GITHUB_ACTIONS'):
            secrets_found = []
            secrets_missing = []

            expected_secrets = [
                'TPS_DOMAIN', 'GA4_PROPERTY_ID', 'AMPLITUDE_API_KEY',
                'SENTRY_AUTH_TOKEN', 'SHOPIFY_STORE_URL'
            ]

            for secret in expected_secrets:
                if os.getenv(secret):
                    secrets_found.append(secret)
                else:
                    secrets_missing.append(secret)

            if secrets_missing:
                return "⚠️", f"Missing {len(secrets_missing)} secrets", f"Missing: {', '.join(secrets_missing)}"
            else:
                return "✅", f"All {len(secrets_found)} secrets found", "GitHub Actions ready"
        else:
            return "ℹ️", "Not in GitHub Actions", "Local environment detected"

    def run_validation(self):
        """Run all validation tests"""
        print("🧪 TPS-STAR Analytics Credentials Validation")
        print("=" * 50)
        print("")

        tests = [
            ("🏢 GitHub Secrets", self.test_github_secrets),
            ("📊 GA4 Credentials", self.test_ga4_credentials),
            ("📈 Amplitude API", self.test_amplitude),
            ("🚨 Sentry API", self.test_sentry),
            ("🛒 Shopify API", self.test_shopify),
        ]

        results = []
        for test_name, test_func in tests:
            print(f"Testing {test_name}...")
            status, message, details = test_func()
            results.append((test_name, status, message, details))
            print(f"  {status} {message}")
            if details:
                print(f"     {details}")
            print("")

        # Summary
        print("📋 Validation Summary")
        print("=" * 20)

        success_count = sum(1 for _, status, _, _ in results if status == "✅")
        total_count = len(results)

        for test_name, status, message, _ in results:
            print(f"{status} {test_name}: {message}")

        print("")
        print(f"🎯 Overall Status: {success_count}/{total_count} tests passed")

        if success_count == total_count:
            print("🎉 All systems ready! Your analytics reporting is fully configured.")
            return True
        else:
            print("⚠️  Some issues found. Check the details above and resolve before running reports.")
            return False

def main():
    validator = CredentialValidator()
    success = validator.run_validation()

    if not success:
        print("")
        print("🔧 Quick fixes:")
        print("   • Run: ./setup_credentials.sh")
        print("   • Check: CREDENTIALS_SETUP.md")
        print("   • Verify: GitHub repository secrets")

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
