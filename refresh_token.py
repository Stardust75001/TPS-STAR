import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("GA4_CLIENT_ID")
CLIENT_SECRET = os.getenv("GA4_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("GA4_REFRESH_TOKEN")
PROPERTY_ID = os.getenv("GA4_PROPERTY_ID")

token_url = "https://oauth2.googleapis.com/token"
payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "refresh_token": REFRESH_TOKEN,
    "grant_type": "refresh_token"
}

res = requests.post(token_url, data=payload)
access_token = res.json().get("access_token")

if access_token:
    print("✅ Access token récupéré :")
    print(access_token)
else:
    print("❌ Échec de récupération du token :")
    print(res.json())
