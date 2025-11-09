# SMTP test and safety notes

This repository includes `scripts/test_smtp_send.sh`, a small script to test SMTP credentials and send a debugged test email from your local environment.

Important safety rules
- Never commit real credentials to the repository.
- Keep a `.env` file (not committed) with your secrets. Add `.env` to `.gitignore`.
- Use GitHub Actions Secrets for CI usage; do not store secrets in workflow files.

Quick steps
1. Copy `.env.example` -> `.env` and fill in `SMTP_PASSWORD`.
2. Add `.env` to your local `.gitignore` if not already ignored.
3. Make the test script executable and run it:

```bash
chmod +x scripts/test_smtp_send.sh
./scripts/test_smtp_send.sh
```

What the script does
- Loads `.env` (if present) and exports variables.
- Uses a tiny inline Python snippet to connect to the SMTP server with STARTTLS, logs in, and sends a simple test email.
- Prints SMTP debug conversation to stdout to help diagnose TLS/auth/DNS issues.

If you want me to add `.env` to `.gitignore` automatically, say so and I will update the repo (I won't commit any secrets).
