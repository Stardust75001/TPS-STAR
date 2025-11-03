#!/usr/bin/env bash
set -euo pipefail

# Lightweight SMTP test script for TPS-STAR
# Usage:
# 1) Create a `.env` file in the repo root (see .env.example) and DO NOT commit it.
# 2) Run: chmod +x scripts/test_smtp_send.sh && ./scripts/test_smtp_send.sh

# Load .env if present (export variables)
if [ -f ".env" ]; then
  # shellcheck disable=SC1091
  set -o allexport
  # shellcheck disable=SC1091
  source ".env"
  set +o allexport
fi

# Required env vars (will fail if missing)
: "${SMTP_SERVER:?Need to set SMTP_SERVER (e.g. smtpout.secureserver.net)}"
: "${SMTP_PORT:=587}"
: "${SMTP_USERNAME:?Need to set SMTP_USERNAME}"
: "${SMTP_PASSWORD:?Need to set SMTP_PASSWORD}"
: "${EMAIL_RECIPIENT:?Need to set EMAIL_RECIPIENT}"

echo "Testing SMTP connection to $SMTP_SERVER:$SMTP_PORT -> $EMAIL_RECIPIENT"

python3 - <<'PY'
import os, smtplib, sys
from email.message import EmailMessage

smtp_server = os.environ['SMTP_SERVER']
smtp_port = int(os.environ.get('SMTP_PORT', '587'))
smtp_user = os.environ['SMTP_USERNAME']
smtp_pass = os.environ['SMTP_PASSWORD']
recipient = os.environ['EMAIL_RECIPIENT']

msg = EmailMessage()
msg['Subject'] = 'TPS-STAR Test Email'
msg['From'] = smtp_user
msg['To'] = recipient
msg.set_content('Ceci est un email de test envoyé par scripts/test_smtp_send.sh (TPS-STAR).')

try:
    with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as s:
        # Print SMTP conversation to stdout for debugging
        s.set_debuglevel(1)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(smtp_user, smtp_pass)
        s.send_message(msg)
    print('\nEmail sent successfully to:', recipient)
    sys.exit(0)
except Exception as e:
    print('\nFailed to send email:', repr(e))
    print('Check: SMTP host/port, username/password, network (outbound 587), or provider-specific app-passwords/allowlisting.')
    sys.exit(2)
PY
