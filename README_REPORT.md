Weekly Analytics Report (TPS-STAR)
=================================
![GA4 Daily Report](https://github.com/Stardust75001/TPS-STAR/actions/workflows/run-ga4-report.yml/badge.svg)

This folder contains a simple report generator and a scheduled workflow that produces a weekly PDF and emails it.

What it does
- Runs every Monday (08:00 UTC / 09:00 Europe/Paris) by default.
- Generates a multi-page PDF with one section per tracker (Sentry, Cloudflare, Meta, Search Console, GA4, Ahrefs).
- Creates simple charts and text analysis. When SMTP credentials are present, emails the PDF to the recipient.

Quick setup
1. Add required GitHub Secrets (Repository -> Settings -> Secrets and variables -> Actions):
   - SMTP_SERVER (e.g. smtp.gmail.com)
   - SMTP_PORT (e.g. 587)
   - SMTP_USERNAME (email used to send)
   - SMTP_PASSWORD (SMTP password or app password)
   - EMAIL_RECIPIENT (e.g. hello@thepetsociety.fr)
   - AHREFS_API_KEY (optional)
   - GA4_PROPERTY_ID (optional)
   - SENTRY_DSN (optional)

2. The workflow `/.github/workflows/weekly-analytics-report.yml` will run and create an artifact `weekly-report` (contains the PDF) and will also email it when SMTP secrets are set.

Customize
- Replace the placeholder fetch_* functions in `scripts/generate_weekly_report.py` with real API calls.
- Adjust the schedule cron in the workflow if you need a different timezone/time.

Notes
- Do not commit API keys or passwords to the repo. Use GitHub Secrets.
- The provided script includes heuristics for analysis and sample critical thresholds; tune these to your business needs.
Export formats
- `.json`, `.csv`, and `.pdf` versions of the GA4 report are stored in `/rapports/`
- Each run creates `ga4-report-YYYYMMDD.*` files
- Notes
- Do not commit API keys or passwords to the repo. Use GitHub Secrets.
- The provided script includes heuristics for analysis and sample critical thresholds; tune these to your business needs.

Export formats
- `.json`, `.csv`, and `.pdf` versions of the GA4 report are stored in `/rapports/`
- Each run creates `ga4-report-YYYYMMDD.*` files
