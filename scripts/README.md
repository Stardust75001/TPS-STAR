# TPS-STAR Weekly Analytics Report System
# =======================================

## Overview
This directory contains the automated weekly analytics reporting system that generates comprehensive business intelligence reports every Monday morning.

## 🎯 Features

### 📊 **Comprehensive Data Collection**
- **Google Analytics 4**: Traffic, conversions, user behavior
- **Amplitude**: Product analytics, user retention, event tracking  
- **Hotjar**: User behavior, heatmaps, session recordings
- **Microsoft Clarity**: Additional user insights, scroll patterns
- **Sentry**: Error tracking, performance monitoring, crash reports
- **Shopify**: E-commerce metrics, orders, revenue data

### 📈 **Beautiful Visualizations**
- Interactive charts and graphs using Plotly
- KPI dashboard with key performance indicators
- User behavior analysis with heatmaps and funnels
- E-commerce performance tracking
- Colorful, well-structured visual design

### 🧠 **AI-Powered Insights**
- Automated analysis of performance trends
- Actionable recommendations based on data
- Priority-based insight categorization
- Week-over-week comparison analysis

### 📄 **Professional Reports**
- Beautiful HTML reports with modern design
- Mobile-responsive layout
- Executive summary with key takeaways
- Detailed charts and data visualizations
- Downloadable artifacts for sharing

## 🚀 Quick Start

### Prerequisites
```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables (see Configuration section)
export GA4_PROPERTY_ID="your-ga4-property-id"
export AMPLITUDE_API_KEY="your-amplitude-key"
# ... other API keys
```

### Manual Execution
```bash
# Generate current week report
python generate_weekly_report.py

# Generate report for specific week offset
WEEK_OFFSET=1 python generate_weekly_report.py  # Last week
WEEK_OFFSET=2 python generate_weekly_report.py  # Two weeks ago
```

### Automated Execution
The system runs automatically via GitHub Actions every Monday at 8:00 AM UTC. Reports are generated and uploaded as artifacts.

## 📁 File Structure

```
scripts/
├── generate_weekly_report.py     # Main report generator
├── analytics_connectors.py       # API connectors for all platforms
├── requirements.txt              # Python dependencies
└── README.md                    # This file

Generated Reports:
reports/
├── weekly-report-YYYY-MM-DD.html    # Main HTML report
├── charts/
│   ├── kpi_dashboard.html           # Interactive KPI dashboard
│   ├── user_behavior.html           # User behavior analysis
│   ├── ecommerce_performance.html   # E-commerce metrics
│   ├── kpi_dashboard.png            # Static chart exports
│   ├── user_behavior.png
│   └── ecommerce_performance.png
└── data/
    └── analytics-data-YYYY-MM-DD.json  # Raw data backup
```

## ⚙️ Configuration

### Environment Variables
Set these in your environment or GitHub Secrets:

```bash
# Google Analytics 4
export GA4_PROPERTY_ID="123456789"
export GA4_ACCESS_TOKEN="your-oauth-token"

# Amplitude Product Analytics  
export AMPLITUDE_API_KEY="your-amplitude-api-key"
export AMPLITUDE_SECRET_KEY="your-amplitude-secret"

# Hotjar User Behavior
export HOTJAR_API_TOKEN="your-hotjar-token" 
export HOTJAR_SITE_ID="your-site-id"

# Microsoft Clarity
export CLARITY_API_KEY="your-clarity-key"
export CLARITY_PROJECT_ID="your-project-id"

# Sentry Error Tracking
export SENTRY_AUTH_TOKEN="your-sentry-token"
export SENTRY_ORG="your-organization"
export SENTRY_PROJECT="your-project"

# Shopify Store Data
export SHOPIFY_STORE="your-store-name"
export SHOPIFY_ACCESS_TOKEN="your-admin-api-token"

# Slack Notifications (optional)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
```

### API Credentials Setup

#### Google Analytics 4
1. Create a service account in Google Cloud Console
2. Enable Google Analytics Reporting API
3. Download credentials JSON file as `ga4-credentials.json`
4. Add service account email to GA4 property with Viewer permissions

#### Amplitude
1. Go to Amplitude Settings > Projects
2. Generate API Key and Secret Key
3. Ensure proper permissions for analytics data

#### Hotjar
1. Visit Hotjar Account Settings > API
2. Generate API token
3. Note your Site ID from the dashboard

#### Sentry
1. Go to Sentry Settings > Account > API
2. Create new auth token with project:read scope
3. Note your organization and project slugs

## 📊 Report Contents

### KPI Dashboard
- **Sessions & Users**: Traffic volume and unique visitors
- **Revenue & Transactions**: E-commerce performance
- **Conversion Rates**: Funnel optimization metrics
- **User Retention**: Long-term engagement tracking
- **Technical Health**: Error rates and performance

### User Behavior Analysis
- **Scroll Depth**: How far users scroll on pages
- **Click Heatmaps**: Most interacted elements
- **Session Duration**: Time spent on site
- **Device Breakdown**: Mobile vs desktop usage

### E-commerce Performance
- **Revenue Trends**: Daily and weekly patterns
- **Product Performance**: Top selling items
- **Cart Abandonment**: Checkout funnel analysis
- **Customer Segments**: New vs returning customers

### Insights & Recommendations
- **Automated Analysis**: AI-generated insights from data
- **Priority Rankings**: Critical, High, Medium, Low priorities
- **Actionable Items**: Specific recommendations for improvement
- **Performance Alerts**: Issues requiring immediate attention

## 🔧 Customization

### Adding New Data Sources
1. Create new connector class in `analytics_connectors.py`
2. Implement required fetch methods
3. Add to `get_all_connectors()` function
4. Update report generator to use new data

### Modifying Visualizations
Edit the chart creation methods in `generate_weekly_report.py`:
- `create_kpi_overview_chart()`
- `create_user_behavior_analysis()`
- `create_ecommerce_performance_chart()`

### Custom Insights
Modify `generate_insights_and_recommendations()` to add:
- New business rules
- Custom thresholds
- Industry-specific recommendations

## 🚨 Troubleshooting

### Common Issues

**"No module named 'plotly'"**
```bash
pip install -r requirements.txt
```

**"API Authentication Failed"**
- Check environment variables are set correctly
- Verify API keys have proper permissions
- Ensure credentials files are in correct location

**"Charts not displaying"**
- Install kaleido for static image generation: `pip install kaleido`
- Check that reports directory has write permissions

**"Missing data for platform X"**
- Verify API credentials for that platform
- Check connector implementation in `analytics_connectors.py`
- Review API rate limits and quotas

### Debug Mode
Enable detailed logging:
```bash
DEBUG=1 python generate_weekly_report.py
```

## 📈 Performance Optimization

### For Large Datasets
- Implement data caching between runs
- Use incremental data fetching
- Add database storage for historical data
- Implement parallel API calls

### Chart Optimization  
- Reduce data points for large time series
- Use sampling for detailed datasets
- Implement lazy loading for interactive charts

## 🔐 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for all credentials  
3. **Rotate API tokens** regularly
4. **Limit API permissions** to minimum required
5. **Use HTTPS** for all API calls
6. **Implement rate limiting** to respect API quotas

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review GitHub Actions logs for automated runs
3. Verify API documentation for any platform changes
4. Create issue in TPS-STAR repository with detailed error logs

## 🎉 Contributing

To improve the analytics system:
1. Fork the repository
2. Create feature branch
3. Add new connectors or visualizations
4. Test with sample data
5. Submit pull request with documentation

---

**Generated by TPS-STAR Analytics Team** 📊✨
