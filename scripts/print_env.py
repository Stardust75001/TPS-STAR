#!/usr/bin/env python3
"""Utility: load .env (non-destructively) and print selected variables.

This is useful to verify which .env file would be used by
`scripts/generate_weekly_report.py` without modifying your shell environment.
"""
from pathlib import Path
import os
import sys


def load_dotenv_like(files=None):
    if files is None:
        files = [
            Path(os.getcwd()) / '.env',
            Path(__file__).resolve().parent / '.env',
            Path(__file__).resolve().parent.parent / '.env'
        ]
    for p in files:
        if p.exists():
            loaded = 0
            with p.open('r', encoding='utf-8') as fh:
                for raw in fh:
                    line = raw.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip()
                    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                        v = v[1:-1]
                    if k and k not in os.environ:
                        os.environ[k] = v
                        loaded += 1
            print(f'Loaded {loaded} vars from {p}')
            return p
    print('No .env file found in standard locations')
    return None


if __name__ == '__main__':
    p = load_dotenv_like()
    keys = ['SMTP_SERVER', 'SMTP_PORT', 'SMTP_USERNAME', 'SMTP_USER', 'SMTP_PASSWORD', 'EMAIL_RECIPIENT', 'SLACK_BOT_TOKEN', 'SLACK_CHANNEL']
    for k in keys:
        print(f"{k} = {os.environ.get(k)!r}")
    if p is None:
        sys.exit(2)
