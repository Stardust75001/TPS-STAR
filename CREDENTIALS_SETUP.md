# 🔐 API Credentials Setup Guide
# =============================

This guide walks you through setting up all API credentials needed for the TPS-STAR weekly analytics reporting system.

## 🚀 Quick Setup

### Option 1: Automated Setup Script
```bash
# Make script executable and run
chmod +x setup_credentials.sh
./setup_credentials.sh
```

### Option 2: Manual Setup
Follow the platform-specific guides below.

---

## 📊 Google Analytics 4 (GA4) Setup

### Step 1: Create Service Account
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing one
3. Enable **Google Analytics Reporting API**
4. Go to **IAM & Admin > Service Accounts**
5. Click **Create Service Account**
6. Name: `tps-star-analytics`
7. Click **Create and Continue**

### Step 2: Generate Credentials
1. In Service Accounts, click on your new account
2. Go to **Keys** tab
3. Click **Add Key > Create New Key**
4. Select **JSON** format
5. Download and save as `credentials/ga4-service-account.json`

### Step 3: Grant Access
1. Copy the service account email (ends with @...gserviceaccount.com)
2. Go to [Google Analytics](https://analytics.google.com/)
3. Select your property
4. Go to **Admin > Property Access Management**
5. Click **+** and add the service account email
6. Grant **Viewer** permissions

### Step 4: Get Property ID
1. In GA4, go to **Admin > Property Settings**
2. Copy the **Property ID** (format: 123456789)
3. Set as `GA4_PROPERTY_ID` secret

---

## 📈 Amplitude Setup

### Step 1: Get API Credentials
1. Login to [Amplitude](https://analytics.amplitude.com/)
2. Go to **Settings > Projects**
3. Select your project
4. Click **General** tab
5. Copy **API Key** and **Secret Key**

### Step 2: Configure Permissions
1. Ensure your account has **Admin** or **Analyst** role
2. Verify **Export Data** permission is enabled

### Environment Variables:
```bash
AMPLITUDE_API_KEY=your_api_key_here
AMPLITUDE_SECRET_KEY=your_secret_key_here
```

---

## 🔥 Hotjar Setup

### Step 1: Generate API Key
1. Login to [Hotjar](https://insights.hotjar.com/)
2. Go to **Account Settings > API**
3. Click **Generate API Token**
4. Copy the token and your Site ID

### Step 2: Get Site ID
1. In Hotjar dashboard, check the URL
2. Format: `https://insights.hotjar.com/site/SITE_ID/dashboard`
3. Extract the numeric Site ID

### Environment Variables:
```bash
HOTJAR_API_KEY=your_api_token_here
HOTJAR_SITE_ID=your_site_id_here
```

---

## 🔍 Microsoft Clarity Setup

### Step 1: Get Project Details
1. Login to [Microsoft Clarity](https://clarity.microsoft.com/)
2. Select your project
3. Go to **Settings > Setup**
4. Copy **Project ID** from the tracking code

### Step 2: API Access
1. Go to **Settings > API**
2. Generate **API Key**
3. Note: Clarity API access may be limited

### Environment Variables:
```bash
CLARITY_API_KEY=your_api_key_here
CLARITY_PROJECT_ID=your_project_id_here
```

---

## 🚨 Sentry Setup

### Step 1: Create Auth Token
1. Login to [Sentry](https://sentry.io/)
2. Go to **Settings > Account > API**
3. Click **Create New Token**
4. Name: `tps-star-analytics`
5. Scopes: `project:read`, `org:read`, `event:read`
6. Copy the token

### Step 2: Get Organization & Project Details
1. In Sentry dashboard, check URL format:
   `https://sentry.io/organizations/YOUR_ORG/projects/YOUR_PROJECT/`
2. Extract organization slug and project slug

### Environment Variables:
```bash
SENTRY_AUTH_TOKEN=your_auth_token_here
SENTRY_ORG=your_organization_slug
SENTRY_PROJECT=your_project_slug
```

---

## 🛒 Shopify Setup

### Step 1: Create Private App
1. Go to **Shopify Admin > Apps > App and sales channel settings**
2. Click **Develop apps for your store**
3. Click **Create an app**
4. Name: `TPS Analytics Reporter`

### Step 2: Configure Permissions
**Admin API access scopes needed:**
- `read_orders` - Order data
- `read_products` - Product information  
- `read_customers` - Customer analytics
- `read_analytics` - Store analytics
- `read_reports` - Sales reports

### Step 3: Generate Access Token
1. Click **API credentials** tab
2. Click **Install app**
3. Copy **Admin API access token**

### Environment Variables:
```bash
SHOPIFY_STORE_URL=https://your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_access_token_here
```

---

## 💬 Slack Notifications Setup (Optional)

### Step 1: Create Webhook
1. Go to your Slack workspace
2. Visit [Slack API](https://api.slack.com/apps)
3. Click **Create New App > From scratch**name: `TPS Analytics Bot`
4. Select your workspace

### Step 2: Configure Incoming Webhooks
1. Go to **Incoming Webhooks**
2. Toggle **Activate Incoming Webhooks**
3. Click **Add New Webhook to Workspace**
4. Select channel for notifications
5. Copy the webhook URL

### Environment Variables:
```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

---

## 🔐 GitHub Secrets Configuration

After collecting all credentials, set them as GitHub repository secrets:

```bash
# Using GitHub CLI
gh secret set TPS_DOMAIN --body="your-domain.com"
gh secret set GA4_PROPERTY_ID --body="123456789"
gh secret set AMPLITUDE_API_KEY --body="your_amplitude_key"
gh secret set AMPLITUDE_SECRET_KEY --body="your_amplitude_secret"
gh secret set HOTJAR_API_KEY --body="your_hotjar_key"
gh secret set CLARITY_API_KEY --body="your_clarity_key"
gh secret set SENTRY_AUTH_TOKEN --body="your_sentry_token"
gh secret set SENTRY_ORG --body="your_sentry_org"
gh secret set SENTRY_PROJECT --body="your_sentry_project"
gh secret set SHOPIFY_STORE_URL --body="https://your-store.myshopify.com"
gh secret set SHOPIFY_ACCESS_TOKEN --body="your_shopify_token"
gh secret set SLACK_WEBHOOK_URL --body="your_slack_webhook"
```

Or manually in GitHub:
1. Go to **Repository > Settings > Secrets and variables > Actions**
2. Click **New repository secret**
3. Add each credential with the names above

---

## 🧪 Testing Your Setup

### Test Report Generation
```bash
# Local test with environment variables
python3 scripts/generate_weekly_report.py

# GitHub workflow test
gh workflow run weekly-analytics-report.yml
```

### Verify API Connections
```bash
# Check workflow logs
gh run list --workflow=weekly-analytics-report.yml

# View specific run
gh run view [RUN_ID]
```

### Debug Common Issues

**"Authentication failed"**
- Verify API keys are correct
- Check token permissions and scopes
- Ensure service account has proper access

**"Rate limit exceeded"**
- APIs have different rate limits
- Add delays between requests
- Consider caching data

**"Module not found"**
- Install requirements: `pip install -r scripts/requirements.txt`
- Check Python version compatibility

---

## 📋 Credentials Checklist

Use this checklist to verify all credentials are configured:

### Required Credentials
- [ ] GA4 Property ID
- [ ] GA4 Service Account JSON file
- [ ] Amplitude API Key & Secret
- [ ] Hotjar API Key & Site ID
- [ ] Sentry Auth Token, Org & Project
- [ ] Shopify Store URL & Access Token

### Optional Credentials  
- [ ] Microsoft Clarity API Key & Project ID
- [ ] Slack Webhook URL for notifications

### GitHub Configuration
- [ ] All secrets added to repository
- [ ] Service account JSON uploaded as secret
- [ ] Workflow permissions configured

### Local Development
- [ ] `.env` file created with all variables
- [ ] `credentials/` directory with GA4 JSON
- [ ] Python dependencies installed

---

## 🔄 Maintenance

### Regular Tasks
- **Monthly**: Rotate API tokens for security
- **Quarterly**: Review API permissions and access
- **Annually**: Update service account credentials

### Monitoring
- **GitHub Actions**: Check workflow runs weekly
- **API Limits**: Monitor usage across all platforms  
- **Error Logs**: Review Sentry for authentication issues

---

## 🆘 Support

If you encounter issues:

1. **Check logs**: GitHub Actions > Workflow runs
2. **Verify credentials**: Test each API individually
3. **Review permissions**: Ensure proper access levels
4. **Update documentation**: Keep this guide current

For platform-specific help:
- [GA4 Reporting API Docs](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [Amplitude API Docs](https://developers.amplitude.com/docs/analytics-api)
- [Hotjar API Docs](https://help.hotjar.com/hc/en-us/articles/115011867948)
- [Sentry API Docs](https://docs.sentry.io/api/)
- [Shopify API Docs](https://shopify.dev/api/admin-rest)

---

**🎉 Once configured, your analytics system will automatically generate beautiful weekly reports every Monday at 8:00 AM UTC!**
