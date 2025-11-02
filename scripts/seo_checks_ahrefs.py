#!/usr/bin/env python3
import os, sys, json, csv, time
import urllib.request as r

API = "https://api.ahrefs.com/v3"

def call(path_query):
    key = os.environ["AHREFS_API_KEY"]
    req = r.Request(f"{API}{path_query}", headers={"Authorization": f"Bearer {key}"})
    try:
        with r.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"ERR {path_query}: {e}")
        sys.exit(2)

domain = os.environ.get("TPS_DOMAIN","").replace("https://","").replace("http://","").strip("/")
mode = "domain"

# 1) Metrics (DR, backlinks…) — endpoint Ahrefs v3 Site Explorer
data = call(f"/site-explorer/metrics?target={domain}&mode={mode}")

# 2) (Optionnel) Top backlinks
# top_bls = call(f"/site-explorer/backlinks?target={domain}&mode={mode}&limit=50")

out = {
    "target": domain,
    "fetched_at": int(time.time()),
    "metrics": data,
    # "top_backlinks": top_bls,
}

# Sauvegarde JSON + CSV rapide si métriques basiques présentes
os.makedirs("out", exist_ok=True)
with open("out/ahrefs_metrics.json","w") as f: json.dump(out, f, indent=2)

# Exemple de CSV si la réponse contient ces champs (adapter aux clés réelles renvoyées par v3)
row = {
    "domain": domain,
    "domain_rating": data.get("domain_rating"),
    "backlinks": data.get("backlinks"),
    "ref_domains": data.get("ref_domains"),
}
with open("out/ahrefs_metrics.csv","w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=row.keys()); w.writeheader(); w.writerow(row)

print("OK: out/ahrefs_metrics.json, out/ahrefs_metrics.csv")
