import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Étape 1 : récupérer un nouveau access_token via refresh_token
def get_access_token():
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": os.getenv("GA4_CLIENT_ID"),
        "client_secret": os.getenv("GA4_CLIENT_SECRET"),
        "refresh_token": os.getenv("GA4_REFRESH_TOKEN"),
        "grant_type": "refresh_token"
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        print("❌ Échec récupération token :", response.status_code, response.text)
        return None

# Étape 2 : lancer le runReport
def run_report(access_token):
    property_id = os.getenv("GA4_PROPERTY_ID")
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "dateRanges": [{"startDate": "2024-11-01", "endDate": "2024-11-08"}],
        "dimensions": [{"name": "country"}],
        "metrics": [{"name": "activeUsers"}]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ Rapport GA4 récupéré :\n")
        print(response.json())
    else:
        print("❌ Échec du runReport :", response.status_code, response.text)

if __name__ == "__main__":
    token = get_access_token()
    if token:
        run_report(token)
