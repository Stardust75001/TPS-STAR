#!/usr/bin/env python3
"""
generate_weekly_report.py

Minimal weekly report generator for TPS-STAR.
Collects (placeholder) data for several trackers, draws simple graphs,
produces a PDF and emails it to a configured recipient.

Notes:
- This is a scaffold: replace the placeholder data-fetching functions with
  real API calls (Sentry, Cloudflare, Meta, Search Console, GA4, Ahrefs)
  and provide the corresponding secrets as environment variables.
- The script is defensive: if no API keys are present it generates sample data
  so the report still runs.
"""
import os
import smtplib
import json
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from email.message import EmailMessage
from email.utils import formatdate
from email.utils import make_msgid
import base64
from pathlib import Path
import requests
import warnings

# Optional visualization libs
try:
    import seaborn as sns
    _HAS_SEABORN = True
except Exception:
    sns = None
    _HAS_SEABORN = False
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    _HAS_PLOTLY = True
except Exception:
    go = None
    px = None
    make_subplots = None
    _HAS_PLOTLY = False

warnings.filterwarnings('ignore')

# Set up styling (apply once)
if _HAS_SEABORN:
    try:
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    except Exception:
        plt.style.use('default')
else:
    plt.style.use('default')

from typing import Dict, List, Any


def _save_delivery_response(payload: dict):
    """Save a small JSON file with delivery provider response for debugging.

    Writes to reports/delivery-response-<timestamp>.json. Non-fatal on failure.
    """
    try:
        os.makedirs('reports', exist_ok=True)
        ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        fn = f'reports/delivery-response-{ts}.json'
        with open(fn, 'w', encoding='utf-8') as fh:
            json.dump(payload, fh, indent=2, default=str)
        print('Saved delivery response to', fn)
    except Exception as e:
        print('Warning: failed to save delivery response:', e)


# Auto-load .env if present so local runs don't require manual `source .env`.
def _load_dotenv_if_exists(filenames=None):
    """Load simple KEY=VALUE pairs from the first existing .env file found.

    Search order (first match wins):
      - CWD/.env
      - script directory/.env
      - repository root (script dir parent)/.env

    Does not overwrite existing environment variables.
    """
    try:
        if filenames is None:
            filenames = [
                Path(os.getcwd()) / '.env',
                Path(__file__).resolve().parent / '.env',
                Path(__file__).resolve().parent.parent / '.env'
            ]
        for p in filenames:
            if p.exists():
                loaded = 0
                with p.open('r', encoding='utf-8') as fh:
                    for raw in fh:
                        line = raw.strip()
                        if not line or line.startswith('#'):
                            continue
                        if '=' not in line:
                            continue
                        k, v = line.split('=', 1)
                        k = k.strip()
                        v = v.strip()
                        # remove surrounding quotes
                        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                            v = v[1:-1]
                        if k and k not in os.environ:
                            os.environ[k] = v
                            loaded += 1
                print(f'Loaded {loaded} vars from {p}')
                return
    except Exception as e:
        print('Warning: failed to read .env file:', e)


# Try to load .env automatically for local dev convenience
_load_dotenv_if_exists()


def sample_timeseries(days=14, base=100, noise=0.15):
    dates = [datetime.utcnow().date() - timedelta(days=(days-1-i)) for i in range(days)]
    values = np.maximum(0, (base * (1 + noise * np.random.randn(days))).astype(int))
    return pd.Series(values, index=pd.to_datetime(dates))


def fetch_sentry_errors():
    # Placeholder: replace with Sentry API call
    return sample_timeseries(days=14, base=25, noise=0.3)


def fetch_cloudflare_metrics():
    # Placeholder: replace with Cloudflare API call
    return sample_timeseries(days=14, base=2000, noise=0.2)


def fetch_meta_metrics():
    # Placeholder: replace with Meta/FB/IG API calls
    return sample_timeseries(days=14, base=350, noise=0.25)


def fetch_search_console():
    # Placeholder: replace with Google Search Console API
    return sample_timeseries(days=14, base=120, noise=0.3)


def fetch_ga4():
    # Placeholder: replace with GA4 API
    return sample_timeseries(days=14, base=900, noise=0.18)


def fetch_ahrefs():
    # Placeholder: replace with Ahrefs API call
    return sample_timeseries(days=14, base=40, noise=0.2)


def analyze_series(s: pd.Series, name: str):
    latest = int(s.iloc[-1])
    prev = int(s.iloc[-2]) if len(s) > 1 else latest
    delta = latest - prev
    pct = (delta / prev * 100) if prev != 0 else 0
    trend = 'up' if delta > 0 else ('down' if delta < 0 else 'stable')
    analysis = f"Latest: {latest}. Change vs previous: {delta} ({pct:.1f}%). Trend: {trend}."
    critical = False
    # simple critical rules (examples)
    if name == 'Sentry (Error Tracking)' and latest > 100:
        critical = True
    if name == 'Cloudflare (Performance/Security)' and latest < 500:
        # assume this metric is throughput; arbitrary threshold
        critical = False
    return analysis, critical


def plot_series(ax, s: pd.Series, title: str, ylabel: str = ''):
    ax.plot(s.index, s.values, marker='o', linestyle='-')
    ax.set_title(title, pad=20)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    ax.margins(y=0.15)


def build_pdf(out_path: str):
    # Collect data
    sentry = fetch_sentry_errors()
    cloud = fetch_cloudflare_metrics()
    meta = fetch_meta_metrics()
    gsc = fetch_search_console()
    ga4 = fetch_ga4()
    ahrefs = fetch_ahrefs()

    sections = [
        ("Sentry (Error Tracking)", "Errors per day", sentry),
        ("Cloudflare (Performance/Security)", "Requests / day", cloud),
        ("Meta Business (Facebook/Instagram Analytics)", "Engagements / day", meta),
        ("Google Search Console (Search)", "Search clicks / day", gsc),
        ("Google Analytics (GA4)", "Sessions / day", ga4),
        ("Ahrefs (SEO)", "Estimated organic visits / day", ahrefs),
    ]

    with PdfPages(out_path) as pdf:
        # Cover page
        fig = plt.figure(figsize=(11.7, 10))
        plt.axis('off')
        title = "TPS-STAR — Weekly Analytics Report"
        date_str = datetime.utcnow().strftime('%Y-%m-%d')
        plt.text(0.5, 0.6, title, ha='center', va='center', fontsize=24)
        plt.text(0.5, 0.48, f"Generated: {date_str} UTC", ha='center', va='center', fontsize=10)
        plt.text(0.5, 0.38, "Summary: weekly snapshot of trackers and suggested next steps.", ha='center', va='center')
        pdf.savefig()
        plt.close()

        critical_points = []

        # One section per tracker
        for name, ylabel, series in sections:
            fig, ax = plt.subplots(figsize=(11.7, 10))
            plot_series(ax, series, name, ylabel)
            # analysis
            analysis, critical = analyze_series(series, name)
            text = f"\nAnalysis:\n{analysis}\n\nSuggested next steps:\n"
            # heuristic suggestions
            if name.startswith('Sentry'):
                text += "- Investigate recent error spikes, attach stack traces, assign to owner.\n- Add rate-limiting or retry logic where appropriate."
            elif name.startswith('Cloudflare'):
                text += "- Verify cache hit ratio; review firewall rules for false positives.\n- Monitor latency and DDoS alerts."
            elif name.startswith('Meta'):
                text += "- Review recent campaign changes; verify pixel events and dedupe.\n- Validate audiences and compare organic vs paid."
            elif 'Search Console' in name:
                text += "- Inspect queries with dropping impressions; check indexing issues.\n- Compare top pages vs Ahrefs backlinks."
            elif 'Google Analytics' in name:
                text += "- Verify session attribution changes; check GA4 events mapping.\n- Validate conversions and funnel steps."
            elif 'Ahrefs' in name:
                text += "- Account plan insufficient for v3 Site Explorer if you see errors.\n- Review backlinks/ref-domains and prioritize high-authority links."

            plt.figtext(0.1, 0.05, text, 
                        fontsize=10, 
                        wrap=True, 
                        verticalalignment='bottom', 
                        bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
            plt.subplots_adjust(bottom=0.35, top=0.92)
            pdf.savefig()
            plt.close()

            if critical:
                critical_points.append((name, analysis))

        # Conclusion page
        plt.figure(figsize=(11.7, 10))
        plt.axis('off')
        plt.text(0.02, 0.88, "Conclusion & Strategy", fontsize=18, weight='bold')
        y = 0.82
        if critical_points:
            plt.text(0.02, y, "Critical points detected:", fontsize=12, color='red')
            y -= 0.04
            for name, anal in critical_points:
                plt.text(0.04, y, f"- {name}: {anal}", fontsize=10)
                y -= 0.035
        else:
            plt.text(0.02, y, "No critical alerts detected this week.", fontsize=12)
            y -= 0.04

        strategy = (
            "Recommended strategy:\n"
            "1) Prioritize fixing critical errors (Sentry).\n"
            "2) Ensure tracking pixels & tags are validated (Meta / GA4).\n"
            "3) For SEO: upgrade/enable Ahrefs API or schedule manual exports until enabled.\n"
            "4) Keep monitoring thresholds and set automated alerts for regressions."
        )
        plt.text(0.02, y, strategy, fontsize=10)
        pdf.savefig()
        plt.close()

    return out_path


def send_email(smtp_server, smtp_port, username, password, recipient, subject, body, attachment_path):
    msg = EmailMessage()
    msg['From'] = username
    msg['To'] = recipient
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    # Ensure we have a Message-ID for tracking bounces
    try:
        msg_id = make_msgid()
        msg['Message-ID'] = msg_id
    except Exception:
        msg_id = None
    msg.set_content(body)

    with open(attachment_path, 'rb') as f:
        data = f.read()
    msg.add_attachment(data, maintype='application', subtype='pdf', filename=os.path.basename(attachment_path))
    # Try to send the email but handle common network/SMTP errors gracefully.
    try:
        # Save raw MIME for support/traceability before sending
        try:
            out_dir = os.path.join('reports', 'sent-messages')
            os.makedirs(out_dir, exist_ok=True)
            if msg_id:
                safe_id = msg_id.strip('<>')
            else:
                safe_id = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            eml_path = os.path.join(out_dir, f'message-{safe_id}.eml')
            with open(eml_path, 'wb') as ef:
                ef.write(msg.as_bytes())
            print('Saved outgoing message to', eml_path)
        except Exception as e:
            print('Warning: failed to save outgoing MIME:', e)
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as s:
            s.starttls()
            s.login(username, password)
            s.send_message(msg)
        # Save a small delivery response JSON for tracing (no provider id available for plain SMTP)
        try:
            resp = {
                'provider': 'smtp',
                'status': 'sent',
                'recipient': recipient,
                'message_id': msg_id,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
            _save_delivery_response(resp)
        except Exception:
            pass
        return True
    except Exception as e:
        # Print a clear, actionable message for diagnostics but do not raise.
        print('Email send failed:', repr(e))
        print('Check SMTP_SERVER/SMTP_PORT/SMTP_USERNAME/SMTP_PASSWORD and network connectivity.')
        try:
            resp = {
                'provider': 'smtp',
                'status': 'error',
                'error': repr(e),
                'recipient': recipient,
                'message_id': msg_id,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
            _save_delivery_response(resp)
        except Exception:
            pass
        return False


def upload_file_to_slack(token: str, channel: str, file_path: str, title: str = None) -> bool:
    """Upload a file to Slack using the Web API (files.upload). Returns True on success."""
    if not token or not channel:
        print('Slack token or channel not provided')
        return False
    url = 'https://slack.com/api/files.upload'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'channels': channel}
    if title:
        data['title'] = title
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'application/pdf')}
            r = requests.post(url, headers=headers, data=data, files=files, timeout=120)
        j = r.json()
        if not j.get('ok'):
            print('Slack files.upload failed:', j.get('error'))
            return False
        print('Uploaded report to Slack, file id:', j.get('file', {}).get('id'))
        return True
    except Exception as e:
        print('Slack upload error:', repr(e))
        return False


def upload_to_transfersh(file_path: str) -> str | None:
    """Upload a file to transfer.sh and return a public URL, or None on failure."""
    dest = f"https://transfer.sh/{os.path.basename(file_path)}"
    try:
        with open(file_path, 'rb') as f:
            r = requests.put(dest, data=f, timeout=120)
        if r.status_code in (200, 201):
            return r.text.strip()
        print('transfer.sh upload failed:', r.status_code, r.text[:200])
        return None
    except Exception as e:
        print('transfer.sh upload error:', repr(e))
        return None


def send_via_sendgrid(api_key: str, sender: str, recipient: str, subject: str, body: str, attachment_path: str) -> bool:
    """Send an email with attachment using SendGrid v3 API as a fallback.

    Returns True on success.
    """
    if not api_key:
        print('SendGrid API key not provided')
        return False
    url = 'https://api.sendgrid.com/v3/mail/send'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    attachments = []
    try:
        with open(attachment_path, 'rb') as f:
            b = f.read()
        attachments.append({
            'content': base64.b64encode(b).decode('ascii'),
            'filename': os.path.basename(attachment_path),
            'type': 'application/pdf',
            'disposition': 'attachment'
        })
    except Exception as e:
        print('Failed to read attachment for SendGrid:', e)
        return False

    payload = {
        'personalizations': [{'to': [{'email': recipient}], 'subject': subject}],
        'from': {'email': sender},
        'content': [{'type': 'text/plain', 'value': body}],
        'attachments': attachments
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        # Persist provider response for debugging
        try:
            resp = {
                'provider': 'sendgrid',
                'status_code': r.status_code,
                'text_snippet': (r.text[:1000] if r.text else None),
                'recipient': recipient,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
            _save_delivery_response(resp)
        except Exception:
            pass

        if r.status_code in (200, 202):
            print('SendGrid accepted the message (status)', r.status_code)
            return True
        else:
            print('SendGrid send failed:', r.status_code, r.text[:500])
            return False
    except Exception as e:
        print('SendGrid request error:', repr(e))
        try:
            resp = {
                'provider': 'sendgrid',
                'status': 'error',
                'error': repr(e),
                'recipient': recipient,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
            _save_delivery_response(resp)
        except Exception:
            pass
        return False


def post_webhook_message(webhook_url: str, text: str) -> bool:
    try:
        r = requests.post(webhook_url, json={'text': text}, timeout=10)
        if r.status_code >= 200 and r.status_code < 300:
            return True
        print('Webhook post failed:', r.status_code, r.text[:200])
        return False
    except Exception as e:
        print('Webhook post error:', repr(e))
        return False


def main():
    out_dir = os.environ.get('REPORT_OUT_DIR', 'out')
    os.makedirs(out_dir, exist_ok=True)
    date_str = datetime.utcnow().strftime('%Y%m%d')
    out_pdf = os.path.join(out_dir, f'tps-weekly-report-{date_str}.pdf')

    print('Building PDF report...')
    pdf_path = build_pdf(out_pdf)
    print('PDF generated at', pdf_path)

    # Email settings from env / GitHub secrets
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = os.environ.get('SMTP_USERNAME')
    smtp_pass = os.environ.get('SMTP_PASSWORD')
    recipient = os.environ.get('EMAIL_RECIPIENT', 'hello@thepetsociety.fr')

    # Prefer SendGrid in CI when available (more reliable / less DNS dependency)
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    sendgrid_sender = os.environ.get('SENDGRID_SENDER')

    subject = f"TPS-STAR Weekly Analytics Report — {datetime.utcnow().strftime('%Y-%m-%d')}"
    body = "Attached: weekly analytics report (PDF). See attached for graphs, analysis and recommended next steps."

    emailed = False
    # Try SendGrid first when configured
    if sendgrid_key and sendgrid_sender and pdf_path:
        try:
            print('Attempting SendGrid delivery to', recipient)
            sg_ok = send_via_sendgrid(sendgrid_key, sendgrid_sender, recipient, subject, body, pdf_path)
            if sg_ok:
                print('SendGrid delivered the message')
                emailed = True
            else:
                print('SendGrid attempt returned failure; will try SMTP if configured')
        except Exception as e:
            print('SendGrid attempt raised an exception:', repr(e))

    # If SendGrid not used or failed, try SMTP when configured
    if not emailed and smtp_server and smtp_user and smtp_pass and pdf_path:
        try:
            print('Attempting SMTP delivery to', recipient)
            ok = send_email(smtp_server, smtp_port, smtp_user, smtp_pass, recipient, subject, body, pdf_path)
            if ok:
                print('Email sent via SMTP')
                emailed = True
            else:
                print('SMTP send failed; check credentials and network. Report generation succeeded.')
        except Exception as e:
            print('SMTP send raised an exception:', repr(e))

    if not emailed:
        print('No successful email delivery. Report available at:', pdf_path)
    # Slack delivery (optional)
    slack_token = os.environ.get('SLACK_BOT_TOKEN')
    slack_channel = os.environ.get('SLACK_CHANNEL')
    slack_webhook = os.environ.get('SLACK_WEBHOOK_URL')
    if slack_token and slack_channel:
        print('Uploading PDF to Slack channel', slack_channel)
        ok = upload_file_to_slack(slack_token, slack_channel, pdf_path, title=f'TPS-STAR Weekly Report {datetime.utcnow().strftime("%Y-%m-%d")}')
        if ok:
            print('Report uploaded to Slack')
        else:
            print('Failed to upload report to Slack via files.upload')
    elif slack_webhook:
        print('Uploading PDF to transfer.sh for webhook delivery')
        url = upload_to_transfersh(pdf_path)
        if url:
            text = f"TPS-STAR Weekly report generated: {url} (expires per transfer.sh policy)"
            posted = post_webhook_message(slack_webhook, text)
            if posted:
                print('Posted report link to Slack via webhook')
            else:
                print('Failed to post report link to Slack webhook')
        else:
            print('Failed to upload report to transfer.sh; cannot post webhook link')
    else:
        print('SMTP credentials not found in env; skipping email send. Report available at:', pdf_path)

# Disabled duplicate procedural entrypoint. Use the class-based
# TPSAnalyticsReporter at the end of this file as the single entrypoint.

class TPSAnalyticsReporter:
    def __init__(self):
        self.week_offset = int(os.getenv('WEEK_OFFSET', '0'))
        self.end_date = datetime.now() - timedelta(days=self.week_offset * 7)
        self.start_date = self.end_date - timedelta(days=7)

        # Create output directories
        os.makedirs('reports', exist_ok=True)
        os.makedirs('reports/charts', exist_ok=True)
        os.makedirs('reports/data', exist_ok=True)

        self.report_data = {}

    def fetch_ga4_data(self) -> Dict[str, Any]:
        """Fetch Google Analytics 4 data"""
        print("📊 Fetching GA4 data...")

        # Simulated GA4 data structure (replace with actual GA4 API calls)
        ga4_data = {
            'sessions': np.random.randint(1200, 2500),
            'users': np.random.randint(800, 1800),
            'pageviews': np.random.randint(3500, 8000),
            'bounce_rate': round(np.random.uniform(0.35, 0.65), 3),
            'avg_session_duration': round(np.random.uniform(120, 300), 2),
            'conversion_rate': round(np.random.uniform(0.02, 0.08), 4),
            'revenue': round(np.random.uniform(2500, 12000), 2),
            'transactions': np.random.randint(15, 85),
            'new_users_percentage': round(np.random.uniform(0.60, 0.85), 3),
            'mobile_percentage': round(np.random.uniform(0.55, 0.75), 3),
            'top_pages': [
                {'page': '/', 'views': np.random.randint(800, 1500)},
                {'page': '/collections/all', 'views': np.random.randint(400, 800)},
                {'page': '/products/premium-collar', 'views': np.random.randint(200, 600)},
                {'page': '/pages/about', 'views': np.random.randint(100, 300)},
                {'page': '/cart', 'views': np.random.randint(150, 400)}
            ],
            'traffic_sources': {
                'organic': round(np.random.uniform(0.35, 0.55), 3),
                'direct': round(np.random.uniform(0.20, 0.35), 3),
                'social': round(np.random.uniform(0.15, 0.25), 3),
                'paid': round(np.random.uniform(0.05, 0.15), 3),
                'email': round(np.random.uniform(0.03, 0.10), 3),
                'referral': round(np.random.uniform(0.02, 0.08), 3)
            },
            'daily_sessions': [
                np.random.randint(150, 400) for _ in range(7)
            ]
        }

        return ga4_data

    def fetch_amplitude_data(self) -> Dict[str, Any]:
        """Fetch Amplitude product analytics data"""
        print("📈 Fetching Amplitude data...")

        amplitude_data = {
            'events_tracked': np.random.randint(8000, 25000),
            'unique_users': np.random.randint(600, 1200),
            'user_retention': {
                'day_1': round(np.random.uniform(0.40, 0.70), 3),
                'day_7': round(np.random.uniform(0.15, 0.35), 3),
                'day_30': round(np.random.uniform(0.05, 0.20), 3)
            },
            'top_events': [
                {'event': 'Product View', 'count': np.random.randint(2000, 5000)},
                {'event': 'Add to Cart', 'count': np.random.randint(300, 800)},
                {'event': 'Page Ready', 'count': np.random.randint(1500, 3500)},
                {'event': 'Add to Wishlist', 'count': np.random.randint(100, 350)},
                {'event': 'Remove from Cart', 'count': np.random.randint(50, 200)}
            ],
            'conversion_funnel': {
                'product_views': 2847,
                'add_to_cart': 456,
                'begin_checkout': 198,
                'purchase': 67
            },
            'user_segments': {
                'new_visitors': round(np.random.uniform(0.60, 0.80), 3),
                'returning_customers': round(np.random.uniform(0.15, 0.30), 3),
                'power_users': round(np.random.uniform(0.05, 0.15), 3)
            }
        }

        return amplitude_data

    def fetch_hotjar_data(self) -> Dict[str, Any]:
        """Fetch Hotjar user behavior data"""
        print("🔥 Fetching Hotjar data...")

        hotjar_data = {
            'sessions_recorded': np.random.randint(150, 350),
            'heatmaps_generated': np.random.randint(12, 25),
            'avg_session_length': round(np.random.uniform(180, 420), 2),
            'rage_clicks': np.random.randint(8, 25),
            'form_abandonment_rate': round(np.random.uniform(0.25, 0.55), 3),
            'scroll_depth': {
                '25%': round(np.random.uniform(0.80, 0.95), 3),
                '50%': round(np.random.uniform(0.60, 0.80), 3),
                '75%': round(np.random.uniform(0.40, 0.65), 3),
                '100%': round(np.random.uniform(0.20, 0.45), 3)
            },
            'top_clicked_elements': [
                {'element': 'Add to Cart Button', 'clicks': np.random.randint(400, 800)},
                {'element': 'Product Images', 'clicks': np.random.randint(600, 1200)},
                {'element': 'Navigation Menu', 'clicks': np.random.randint(300, 600)},
                {'element': 'Search Bar', 'clicks': np.random.randint(150, 400)},
                {'element': 'Wishlist Icon', 'clicks': np.random.randint(80, 200)}
            ]
        }

        return hotjar_data

    def fetch_sentry_data(self) -> Dict[str, Any]:
        """Fetch Sentry error tracking data"""
        print("🚨 Fetching Sentry data...")

        sentry_data = {
            'total_errors': np.random.randint(15, 85),
            'unique_errors': np.random.randint(8, 25),
            'crash_free_sessions': round(np.random.uniform(0.96, 0.998), 4),
            'performance_score': round(np.random.uniform(85, 98), 1),
            'top_errors': [
                {'error': 'NetworkError: Failed to fetch', 'count': np.random.randint(5, 20)},
                {'error': 'TypeError: Cannot read property', 'count': np.random.randint(3, 15)},
                {'error': 'ReferenceError: gtag is not defined', 'count': np.random.randint(2, 10)},
                {'error': 'ChunkLoadError: Loading chunk failed', 'count': np.random.randint(1, 8)}
            ],
            'browser_performance': {
                'avg_load_time': round(np.random.uniform(1.2, 3.5), 2),
                'lcp': round(np.random.uniform(1.5, 4.0), 2),
                'fid': round(np.random.uniform(50, 200), 1),
                'cls': round(np.random.uniform(0.05, 0.25), 3)
            }
        }

        return sentry_data

    def create_kpi_overview_chart(self):
        """Create KPI overview dashboard"""
        print("📊 Creating KPI overview chart...")
        # If plotly is available, use interactive dashboards; otherwise fall back to matplotlib
        if _HAS_PLOTLY and make_subplots is not None and go is not None:
            try:
                fig = make_subplots(
                    rows=2, cols=3,
                    subplot_titles=('Sessions Trend', 'Revenue Growth', 'Conversion Funnel',
                                  'Traffic Sources', 'User Retention', 'Error Rate'),
                    specs=[[{"secondary_y": True}, {"secondary_y": True}, {}],
                           [{"type": "domain"}, {}, {"secondary_y": True}]]
                )

                # Sessions trend
                days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                sessions = self.report_data['ga4']['daily_sessions']
                fig.add_trace(
                    go.Scatter(x=days, y=sessions, mode='lines+markers',
                              name='Sessions', line=dict(color='#2E86C1', width=3)),
                    row=1, col=1
                )

                # Revenue growth (mock week-over-week)
                revenue_data = [2800, 3200, 2900, 3800, 4200, 3600, 4100]
                fig.add_trace(
                    go.Bar(x=days, y=revenue_data, name='Revenue (€)',
                           marker_color='#28B463'),
                    row=1, col=2
                )

                # Conversion funnel
                funnel_data = self.report_data['amplitude']['conversion_funnel']
                funnel_labels = list(funnel_data.keys())
                funnel_values = list(funnel_data.values())

                fig.add_trace(
                    go.Funnel(
                        y=funnel_labels,
                        x=funnel_values,
                        textinfo="value+percent initial",
                        marker={"color": ["#3498DB", "#E74C3C", "#F39C12", "#27AE60"]}
                    ),
                    row=1, col=3
                )

                # Traffic sources pie chart
                sources = list(self.report_data['ga4']['traffic_sources'].keys())
                values = list(self.report_data['ga4']['traffic_sources'].values())

                fig.add_trace(
                    go.Pie(labels=sources, values=values, name="Traffic Sources",
                           marker_colors=['#3498DB', '#E74C3C', '#F39C12', '#27AE60', '#9B59B6', '#E67E22']),
                    row=2, col=1
                )

                # User retention
                retention = self.report_data['amplitude']['user_retention']
                fig.add_trace(
                    go.Bar(x=list(retention.keys()), y=list(retention.values()),
                           name='Retention Rate', marker_color='#8E44AD'),
                    row=2, col=2
                )

                # Error rate trend
                error_days = days
                error_rates = [np.random.uniform(0.01, 0.05) for _ in range(7)]
                fig.add_trace(
                    go.Scatter(x=error_days, y=error_rates, mode='lines+markers',
                              name='Error Rate', line=dict(color='#E74C3C', width=2)),
                    row=2, col=3
                )

                fig.update_layout(
                    title_text="🎯 TPS-STAR Weekly KPI Dashboard",
                    title_x=0.5,
                    height=800,
                    showlegend=False,
                    template="plotly_white",
                    font=dict(size=12)
                )

                fig.write_html("reports/charts/kpi_dashboard.html")
                try:
                    fig.write_image("reports/charts/kpi_dashboard.png", width=1400, height=800)
                except Exception:
                    # If kaleido/engine not available, write only html
                    pass
            except Exception as e:
                print('Plotly KPI dashboard build failed; falling back to matplotlib:', repr(e))
                # Matplotlib fallback: simple 2x3 grid
                days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                sessions = self.report_data['ga4']['daily_sessions']
                revenue_data = [2800, 3200, 2900, 3800, 4200, 3600, 4100]
                funnel_data = self.report_data['amplitude']['conversion_funnel']
                sources = list(self.report_data['ga4']['traffic_sources'].keys())
                values = list(self.report_data['ga4']['traffic_sources'].values())
                retention = self.report_data['amplitude']['user_retention']
                error_rates = [np.random.uniform(0.01, 0.05) for _ in range(7)]

                fig, axes = plt.subplots(2, 3, figsize=(14, 9))
                # Sessions
                axes[0, 0].plot(days, sessions, marker='o')
                axes[0, 0].set_title('Sessions Trend')

                # Revenue
                axes[0, 1].bar(days, revenue_data, color='#28B463')
                axes[0, 1].set_title('Revenue Growth')

                # Funnel (horizontal bar)
                labels = list(funnel_data.keys())
                vals = list(funnel_data.values())
                axes[0, 2].barh(labels, vals, color=['#3498DB', '#E74C3C', '#F39C12', '#27AE60'])
                axes[0, 2].set_title('Conversion Funnel')

                # Traffic sources (pie)
                axes[1, 0].pie(values, labels=sources, autopct='%1.1f%%')
                axes[1, 0].set_title('Traffic Sources')

                # Retention
                axes[1, 1].bar(list(retention.keys()), list(retention.values()), color='#8E44AD')
                axes[1, 1].set_title('User Retention')

                # Error rate
                axes[1, 2].plot(days, error_rates, marker='o', color='#E74C3C')
                axes[1, 2].set_title('Error Rate')

                plt.tight_layout()
                png_path = 'reports/charts/kpi_dashboard.png'
                html_path = 'reports/charts/kpi_dashboard.html'
                fig.savefig(png_path, dpi=150)
                plt.close(fig)
                # Simple HTML wrapper embedding the PNG
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write("<html><body><img src='kpi_dashboard.png' style='max-width:100%' /></body></html>")
        else:
            # Matplotlib fallback: simple 2x3 grid
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            sessions = self.report_data['ga4']['daily_sessions']
            revenue_data = [2800, 3200, 2900, 3800, 4200, 3600, 4100]
            funnel_data = self.report_data['amplitude']['conversion_funnel']
            sources = list(self.report_data['ga4']['traffic_sources'].keys())
            values = list(self.report_data['ga4']['traffic_sources'].values())
            retention = self.report_data['amplitude']['user_retention']
            error_rates = [np.random.uniform(0.01, 0.05) for _ in range(7)]

            fig, axes = plt.subplots(2, 3, figsize=(14, 9))
            # Sessions
            axes[0, 0].plot(days, sessions, marker='o')
            axes[0, 0].set_title('Sessions Trend')

            # Revenue
            axes[0, 1].bar(days, revenue_data, color='#28B463')
            axes[0, 1].set_title('Revenue Growth')

            # Funnel (horizontal bar)
            labels = list(funnel_data.keys())
            vals = list(funnel_data.values())
            axes[0, 2].barh(labels, vals, color=['#3498DB', '#E74C3C', '#F39C12', '#27AE60'])
            axes[0, 2].set_title('Conversion Funnel')

            # Traffic sources (pie)
            axes[1, 0].pie(values, labels=sources, autopct='%1.1f%%')
            axes[1, 0].set_title('Traffic Sources')

            # Retention
            axes[1, 1].bar(list(retention.keys()), list(retention.values()), color='#8E44AD')
            axes[1, 1].set_title('User Retention')

            # Error rate
            axes[1, 2].plot(days, error_rates, marker='o', color='#E74C3C')
            axes[1, 2].set_title('Error Rate')

            plt.tight_layout()
            png_path = 'reports/charts/kpi_dashboard.png'
            html_path = 'reports/charts/kpi_dashboard.html'
            fig.savefig(png_path, dpi=150)
            plt.close(fig)
            # Simple HTML wrapper embedding the PNG
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write("<html><body><img src='kpi_dashboard.png' style='max-width:100%' /></body></html>")

    def create_user_behavior_analysis(self):
        """Create detailed user behavior analysis"""
        print("👥 Creating user behavior analysis...")
        if _HAS_PLOTLY and make_subplots is not None and go is not None:
            try:
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Page Scroll Depth', 'Top Clicked Elements',
                                  'Session Duration Distribution', 'Device Usage'),
                    # device usage (bottom-right) is a pie -> use 'domain' type there
                    specs=[[{}, {}], [{}, {"type": "domain"}]]
                )

                # Scroll depth
                scroll_data = self.report_data['hotjar']['scroll_depth']
                scroll_depths = list(scroll_data.keys())
                scroll_percentages = [v * 100 for v in scroll_data.values()]

                fig.add_trace(
                    go.Bar(x=scroll_depths, y=scroll_percentages,
                           name='Scroll Depth', marker_color='#3498DB'),
                    row=1, col=1
                )

                # Top clicked elements
                clicked_elements = self.report_data['hotjar']['top_clicked_elements']
                element_names = [item['element'] for item in clicked_elements]
                click_counts = [item['clicks'] for item in clicked_elements]

                fig.add_trace(
                    go.Bar(x=click_counts, y=element_names, orientation='h',
                           name='Clicks', marker_color='#E74C3C'),
                    row=1, col=2
                )

                # Session duration distribution
                durations = np.random.normal(200, 80, 1000)
                durations = durations[durations > 0]

                fig.add_trace(
                    go.Histogram(x=durations, nbinsx=20, name='Session Duration',
                                marker_color='#27AE60'),
                    row=2, col=1
                )

                # Device usage (pie chart)
                devices = ['Mobile', 'Desktop', 'Tablet']
                device_percentages = [65, 30, 5]

                fig.add_trace(
                    go.Pie(labels=devices, values=device_percentages, name="Devices",
                           marker_colors=['#F39C12', '#9B59B6', '#E67E22']),
                    row=2, col=2
                )

                fig.update_layout(
                    title_text="👥 User Behavior Deep Dive",
                    title_x=0.5,
                    height=700,
                    showlegend=False,
                    template="plotly_white"
                )

                fig.write_html("reports/charts/user_behavior.html")
                try:
                    fig.write_image("reports/charts/user_behavior.png", width=1200, height=700)
                except Exception:
                    pass
            except Exception as e:
                print('Plotly user behavior chart failed; falling back to matplotlib:', repr(e))
                # Matplotlib fallback
                scroll_data = self.report_data['hotjar']['scroll_depth']
                scroll_depths = list(scroll_data.keys())
                scroll_percentages = [v * 100 for v in scroll_data.values()]

                clicked_elements = self.report_data['hotjar']['top_clicked_elements']
                element_names = [item['element'] for item in clicked_elements]
                click_counts = [item['clicks'] for item in clicked_elements]

                durations = np.random.normal(200, 80, 1000)
                durations = durations[durations > 0]

                devices = ['Mobile', 'Desktop', 'Tablet']
                device_percentages = [65, 30, 5]

                fig, axes = plt.subplots(2, 2, figsize=(12, 8))
                axes[0, 0].bar(scroll_depths, scroll_percentages, color='#3498DB')
                axes[0, 0].set_title('Page Scroll Depth')

                axes[0, 1].barh(element_names, click_counts, color='#E74C3C')
                axes[0, 1].set_title('Top Clicked Elements')

                axes[1, 0].hist(durations, bins=20, color='#27AE60')
                axes[1, 0].set_title('Session Duration Distribution')

                axes[1, 1].pie(device_percentages, labels=devices, autopct='%1.0f%%')
                axes[1, 1].set_title('Device Usage')

                plt.tight_layout()
                png_path = 'reports/charts/user_behavior.png'
                html_path = 'reports/charts/user_behavior.html'
                fig.savefig(png_path, dpi=150)
                plt.close(fig)
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write("<html><body><img src='user_behavior.png' style='max-width:100%' /></body></html>")
        else:
            # Matplotlib fallback
            scroll_data = self.report_data['hotjar']['scroll_depth']
            scroll_depths = list(scroll_data.keys())
            scroll_percentages = [v * 100 for v in scroll_data.values()]

            clicked_elements = self.report_data['hotjar']['top_clicked_elements']
            element_names = [item['element'] for item in clicked_elements]
            click_counts = [item['clicks'] for item in clicked_elements]

            durations = np.random.normal(200, 80, 1000)
            durations = durations[durations > 0]

            devices = ['Mobile', 'Desktop', 'Tablet']
            device_percentages = [65, 30, 5]

            fig, axes = plt.subplots(2, 2, figsize=(12, 8))
            axes[0, 0].bar(scroll_depths, scroll_percentages, color='#3498DB')
            axes[0, 0].set_title('Page Scroll Depth')

            axes[0, 1].barh(element_names, click_counts, color='#E74C3C')
            axes[0, 1].set_title('Top Clicked Elements')

            axes[1, 0].hist(durations, bins=20, color='#27AE60')
            axes[1, 0].set_title('Session Duration Distribution')

            axes[1, 1].pie(device_percentages, labels=devices, autopct='%1.0f%%')
            axes[1, 1].set_title('Device Usage')

            plt.tight_layout()
            png_path = 'reports/charts/user_behavior.png'
            html_path = 'reports/charts/user_behavior.html'
            fig.savefig(png_path, dpi=150)
            plt.close(fig)
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write("<html><body><img src='user_behavior.png' style='max-width:100%' /></body></html>")

    def create_ecommerce_performance_chart(self):
        """Create e-commerce performance analysis"""
        print("🛒 Creating e-commerce performance chart...")
        if _HAS_PLOTLY and make_subplots is not None and go is not None:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Revenue by Day', 'Product Performance',
                              'Cart Abandonment Analysis', 'Customer Segments'),
                # Customer Segments (bottom-right) is a pie chart -> 'domain'
                specs=[[{"secondary_y": True}, {}], [{}, {"type": "domain"}]]
            )

            # Revenue by day with transactions
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            revenue = [2800, 3200, 2900, 3800, 4200, 3600, 4100]
            transactions = [12, 15, 11, 18, 22, 17, 19]

            fig.add_trace(
                go.Bar(x=days, y=revenue, name='Revenue (€)',
                       marker_color='#27AE60'),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(x=days, y=transactions, mode='lines+markers',
                          name='Transactions', line=dict(color='#E74C3C', width=3)),
                row=1, col=1, secondary_y=True
            )

            # Product performance
            products = ['Premium Collar', 'Dog Leash', 'Pet Treats', 'Cat Toy', 'Pet Bed']
            product_revenue = [1200, 800, 600, 400, 350]

            fig.add_trace(
                go.Bar(x=products, y=product_revenue, name='Product Revenue',
                       marker_color='#3498DB'),
                row=1, col=2
            )

            # Cart abandonment funnel
            cart_funnel = ['Add to Cart', 'View Cart', 'Begin Checkout', 'Complete Purchase']
            cart_values = [456, 298, 198, 67]

            fig.add_trace(
                go.Funnel(
                    y=cart_funnel,
                    x=cart_values,
                    textinfo="value+percent initial",
                    marker={"color": ["#F39C12", "#E67E22", "#D35400", "#E74C3C"]}
                ),
                row=2, col=1
            )

            # Customer segments
            segments = ['New Customers', 'Returning', 'VIP Customers']
            segment_values = [65, 28, 7]

            fig.add_trace(
                go.Pie(labels=segments, values=segment_values, name="Customer Segments",
                       marker_colors=['#3498DB', '#E74C3C', '#F1C40F']),
                row=2, col=2
            )

            fig.update_layout(
                title_text="🛒 E-commerce Performance Analytics",
                title_x=0.5,
                height=700,
                showlegend=False,
                template="plotly_white"
            )

            fig.write_html("reports/charts/ecommerce_performance.html")
            try:
                fig.write_image("reports/charts/ecommerce_performance.png", width=1200, height=700)
            except Exception:
                pass
        else:
            # Matplotlib fallback
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            revenue = [2800, 3200, 2900, 3800, 4200, 3600, 4100]
            transactions = [12, 15, 11, 18, 22, 17, 19]

            products = ['Premium Collar', 'Dog Leash', 'Pet Treats', 'Cat Toy', 'Pet Bed']
            product_revenue = [1200, 800, 600, 400, 350]

            cart_funnel = ['Add to Cart', 'View Cart', 'Begin Checkout', 'Complete Purchase']
            cart_values = [456, 298, 198, 67]

            segments = ['New Customers', 'Returning', 'VIP Customers']
            segment_values = [65, 28, 7]

            fig, axes = plt.subplots(2, 2, figsize=(12, 8))
            axes[0, 0].bar(days, revenue, color='#27AE60')
            axes[0, 0].set_title('Revenue by Day')

            axes[0, 0].plot(days, transactions, marker='o', color='#E74C3C')

            axes[0, 1].bar(products, product_revenue, color='#3498DB')
            axes[0, 1].set_title('Product Performance')

            axes[1, 0].barh(cart_funnel, cart_values, color=['#F39C12', '#E67E22', '#D35400', '#E74C3C'])
            axes[1, 0].set_title('Cart Abandonment Funnel')

            axes[1, 1].pie(segment_values, labels=segments, autopct='%1.0f%%')
            axes[1, 1].set_title('Customer Segments')

            plt.tight_layout()
            png_path = 'reports/charts/ecommerce_performance.png'
            html_path = 'reports/charts/ecommerce_performance.html'
            fig.savefig(png_path, dpi=150)
            plt.close(fig)
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write("<html><body><img src='ecommerce_performance.png' style='max-width:100%' /></body></html>")

    def generate_insights_and_recommendations(self) -> List[Dict[str, str]]:
        """Generate AI-powered insights and recommendations"""
        print("🧠 Generating insights and recommendations...")

        ga4 = self.report_data['ga4']
        amplitude = self.report_data['amplitude']
        hotjar = self.report_data['hotjar']
        sentry = self.report_data['sentry']

        insights = []

        # Traffic insights
        if ga4['bounce_rate'] > 0.5:
            insights.append({
                'type': 'warning',
                'category': 'Traffic Quality',
                'insight': f"Bounce rate is {ga4['bounce_rate']:.1%}, which is above the recommended 50% threshold.",
                'recommendation': "Improve page load speed, enhance content relevance, and optimize mobile experience.",
                'priority': 'High'
            })

        # Conversion insights
        if ga4['conversion_rate'] < 0.03:
            insights.append({
                'type': 'opportunity',
                'category': 'Conversion Optimization',
                'insight': f"Conversion rate is {ga4['conversion_rate']:.2%}, below industry average of 3%.",
                'recommendation': "A/B test checkout flow, add social proof, and implement exit-intent popups.",
                'priority': 'High'
            })

        # User experience insights
        if hotjar['rage_clicks'] > 15:
            insights.append({
                'type': 'warning',
                'category': 'User Experience',
                'insight': f"High rage click count ({hotjar['rage_clicks']}) indicates user frustration.",
                'recommendation': "Review heatmaps to identify problematic elements and improve UI/UX design.",
                'priority': 'Medium'
            })

        # Performance insights
        if sentry['crash_free_sessions'] < 0.98:
            insights.append({
                'type': 'critical',
                'category': 'Technical Health',
                'insight': f"Crash-free session rate is {sentry['crash_free_sessions']:.1%}, below 98% target.",
                'recommendation': "Prioritize fixing top errors and implement better error handling.",
                'priority': 'Critical'
            })

        # Positive insights
        if amplitude['user_retention']['day_7'] > 0.25:
            insights.append({
                'type': 'success',
                'category': 'User Engagement',
                'insight': f"Excellent 7-day retention rate of {amplitude['user_retention']['day_7']:.1%}.",
                'recommendation': "Leverage this strength by implementing referral programs and user-generated content.",
                'priority': 'Low'
            })

        return insights

    def create_html_report(self, insights: List[Dict[str, str]]):
        """Generate comprehensive HTML report"""
        print("📄 Creating HTML report...")

        report_date = self.end_date.strftime("%Y-%m-%d")

        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TPS-STAR Weekly Analytics Report - {report_date}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #2E86C1;
            --success-color: #27AE60;
            --warning-color: #F39C12;
            --danger-color: #E74C3C;
            --info-color: #3498DB;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px 0;
        }}

        .main-container {{
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .header {{
            background: linear-gradient(135deg, var(--primary-color), #1B4F72);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            margin: 0;
            font-size: 2.5rem;
            font-weight: 300;
        }}

        .header .subtitle {{
            margin-top: 10px;
            opacity: 0.9;
            font-size: 1.1rem;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}

        .kpi-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-5px);
        }}

        .kpi-number {{
            font-size: 2.2rem;
            font-weight: 700;
            margin: 10px 0;
        }}

        .kpi-label {{
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .kpi-change {{
            font-size: 0.85rem;
            margin-top: 5px;
        }}

        .positive {{ color: var(--success-color); }}
        .negative {{ color: var(--danger-color); }}
        .neutral {{ color: var(--info-color); }}

        .chart-container {{
            margin: 30px;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .chart-title {{
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: #2c3e50;
            text-align: center;
        }}

        .insights-section {{
            margin: 30px;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .insight-card {{
            margin: 15px 0;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid;
        }}

        .insight-critical {{
            background: #fdeaea;
            border-left-color: var(--danger-color);
        }}
        .insight-warning {{
            background: #fef9e7;
            border-left-color: var(--warning-color);
        }}
        .insight-opportunity {{
            background: #eaf4fd;
            border-left-color: var(--info-color);
        }}
        .insight-success {{
            background: #eafaf1;
            border-left-color: var(--success-color);
        }}

        .insight-title {{
            font-weight: 600;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .priority-badge {{
            font-size: 0.75rem;
            padding: 3px 8px;
            border-radius: 12px;
            text-transform: uppercase;
            font-weight: 600;
        }}

        .priority-critical {{ background: var(--danger-color); color: white; }}
        .priority-high {{ background: var(--warning-color); color: white; }}
        .priority-medium {{ background: var(--info-color); color: white; }}
        .priority-low {{ background: var(--success-color); color: white; }}

        .footer {{
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }}

        .chart-embed {{
            width: 100%;
            height: 600px;
            border: none;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <!-- Header -->
        <div class="header">
            <h1><i class="fas fa-chart-line"></i> TPS-STAR Analytics Report</h1>
            <div class="subtitle">
                Weekly Business Intelligence Report<br>
                Period: {self.start_date.strftime("%B %d")} - {self.end_date.strftime("%B %d, %Y")}
            </div>
        </div>

        <!-- KPI Overview -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Sessions</div>
                <div class="kpi-number" style="color: var(--primary-color);">
                    {self.report_data['ga4']['sessions']:,}
                </div>
                <div class="kpi-change positive">
                    <i class="fas fa-arrow-up"></i> +12.3% vs last week
                </div>
            </div>

            <div class="kpi-card">
                <div class="kpi-label">Revenue</div>
                <div class="kpi-number" style="color: var(--success-color);">
                    €{self.report_data['ga4']['revenue']:,.0f}
                </div>
                <div class="kpi-change positive">
                    <i class="fas fa-arrow-up"></i> +8.7% vs last week
                </div>
            </div>

            <div class="kpi-card">
                <div class="kpi-label">Conversion Rate</div>
                <div class="kpi-number" style="color: var(--info-color);">
                    {self.report_data['ga4']['conversion_rate']:.2%}
                </div>
                <div class="kpi-change negative">
                    <i class="fas fa-arrow-down"></i> -2.1% vs last week
                </div>
            </div>

            <div class="kpi-card">
                <div class="kpi-label">Avg Order Value</div>
                <div class="kpi-number" style="color: var(--warning-color);">
                    €{(self.report_data['ga4']['revenue'] / self.report_data['ga4']['transactions']):.0f}
                </div>
                <div class="kpi-change positive">
                    <i class="fas fa-arrow-up"></i> +5.4% vs last week
                </div>
            </div>

            <div class="kpi-card">
                <div class="kpi-label">Crash-Free Sessions</div>
                <div class="kpi-number" style="color: var(--success-color);">
                    {self.report_data['sentry']['crash_free_sessions']:.1%}
                </div>
                <div class="kpi-change positive">
                    <i class="fas fa-arrow-up"></i> +0.3% vs last week
                </div>
            </div>

            <div class="kpi-card">
                <div class="kpi-label">User Retention (7d)</div>
                <div class="kpi-number" style="color: var(--info-color);">
                    {self.report_data['amplitude']['user_retention']['day_7']:.1%}
                </div>
                <div class="kpi-change positive">
                    <i class="fas fa-arrow-up"></i> +4.2% vs last week
                </div>
            </div>
        </div>

        <!-- Charts -->
        <div class="chart-container">
            <div class="chart-title">📊 KPI Dashboard Overview</div>
            <iframe src="charts/kpi_dashboard.html" class="chart-embed"></iframe>
        </div>

        <div class="chart-container">
            <div class="chart-title">👥 User Behavior Analysis</div>
            <iframe src="charts/user_behavior.html" class="chart-embed"></iframe>
        </div>

        <div class="chart-container">
            <div class="chart-title">🛒 E-commerce Performance</div>
            <iframe src="charts/ecommerce_performance.html" class="chart-embed"></iframe>
        </div>

        <!-- Insights and Recommendations -->
        <div class="insights-section">
            <h2><i class="fas fa-lightbulb"></i> Key Insights & Recommendations</h2>
"""

        # Add insights
        for insight in insights:
            priority_class = f"priority-{insight['priority'].lower()}"
            insight_class = f"insight-{insight['type']}"

            icon_map = {
                'critical': 'fas fa-exclamation-triangle',
                'warning': 'fas fa-exclamation-circle',
                'opportunity': 'fas fa-chart-line',
                'success': 'fas fa-check-circle'
            }

            html_template += f"""
            <div class="insight-card {insight_class}">
                <div class="insight-title">
                    <i class="{icon_map[insight['type']]}"></i>
                    {insight['category']}
                    <span class="priority-badge {priority_class}">{insight['priority']}</span>
                </div>
                <div class="insight-content">
                    <strong>Insight:</strong> {insight['insight']}<br>
                    <strong>Recommendation:</strong> {insight['recommendation']}
                </div>
            </div>
"""

        html_template += f"""
        </div>

        <!-- Footer -->
        <div class="footer">
            <p><i class="fas fa-robot"></i> Generated automatically by TPS-STAR Analytics System</p>
            <p>Report generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p UTC")}</p>
            <p><i class="fas fa-github"></i> <a href="https://github.com/Stardust75001/TPS-STAR" style="color: #3498db;">View on GitHub</a></p>
        </div>
    </div>
</body>
</html>
"""

        with open(f"reports/weekly-report-{report_date}.html", "w", encoding="utf-8") as f:
            f.write(html_template)

    def save_data_json(self):
        """Save all collected data as JSON for future reference"""
        report_date = self.end_date.strftime("%Y-%m-%d")

        with open(f"reports/data/analytics-data-{report_date}.json", "w") as f:
            json.dump(self.report_data, f, indent=2, default=str)

    def run(self):
        """Main execution method"""
        print("🚀 Starting TPS-STAR Weekly Analytics Report Generation...")
        print(f"📅 Analyzing period: {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")

        # Collect data from all sources
        self.report_data['ga4'] = self.fetch_ga4_data()
        self.report_data['amplitude'] = self.fetch_amplitude_data()
        self.report_data['hotjar'] = self.fetch_hotjar_data()
        self.report_data['sentry'] = self.fetch_sentry_data()

        # Generate visualizations
        self.create_kpi_overview_chart()
        self.create_user_behavior_analysis()
        self.create_ecommerce_performance_chart()

