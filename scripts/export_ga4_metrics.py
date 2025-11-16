import json
import os
from datetime import datetime
from utils.ga4_api import GA4Client

# TPS - Unified export for daily + weekly dashboards
# --------------------------------------------------

def export_ga4_metrics(out_path="report_data/ga4_metrics.json"):
    ga4 = GA4Client()

    metrics = {
        "timestamp": datetime.utcnow().isoformat(),
        "active_users": ga4.get_active_users(),
        "pageviews": ga4.get_pageviews(),
        "sessions": ga4.get_sessions(),
        "top_pages": ga4.get_top_pages(limit=20),
        "events": ga4.get_top_events(limit=20),
        "country_stats": ga4.get_country_stats(limit=20),
        "device_stats": ga4.get_device_stats(),
        "ecommerce": ga4.get_ecommerce_overview(),       # e-commerce overview complet
        "checkout_funnel": ga4.get_checkout_funnel(),     # entonnoir checkout complet
    }

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w") as f:
        json.dump(metrics, f, indent=2)

    return metrics


if __name__ == "__main__":
    export_ga4_metrics()
