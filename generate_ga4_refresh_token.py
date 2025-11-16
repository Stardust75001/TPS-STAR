from google_auth_oauthlib.flow import InstalledAppFlow

client_id = input("CLIENT_ID: ")
client_secret = input("CLIENT_SECRET: ")

flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    },
    scopes=["https://www.googleapis.com/auth/analytics.readonly"]
)

creds = flow.run_local_server(port=8080)

print("\nACCESS TOKEN:\n", creds.token)
print("\nREFRESH TOKEN:\n", creds.refresh_token)
print("\nCLIENT ID:\n", client_id)
print("\nCLIENT SECRET:\n", client_secret)
