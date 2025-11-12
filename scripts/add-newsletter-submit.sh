#!/usr/bin/env bash
# add-newsletter-submit.sh
# Add .general.newsletter.submit to all locale JSON files under ./locales
# Requires: jq

set -euo pipefail

LOCALES_DIR="${1:-locales}"
FORCE="${FORCE:-false}"   # set FORCE=true to overwrite existing values

DEFAULT_EN="Subscribe"

translate() {
  case "$1" in
    en|en.default) echo "Subscribe" ;;
    fr)            echo "S’abonner" ;;
    de)            echo "Abonnieren" ;;
    es)            echo "Suscribirse" ;;
    it)            echo "Iscriviti" ;;
    nl)            echo "Abonneren" ;;
    pl)            echo "Subskrybuj" ;;
    pt)            echo "Subscrever" ;;
    da)            echo "Abonner" ;;
    sv)            echo "Prenumerera" ;;
    *)             echo "$DEFAULT_EN" ;;
  esac
}

update_file() {
  local file="$1"
  local base="$(basename "$file")"
  local stem="${base%.*}"
  local lang="${stem%%.*}"

  local value
  value="$(translate "$lang")"

  if [[ "$FORCE" == "true" ]]; then
    jq --arg v "$value" '
      (.general //= {}) |
      (.general.newsletter //= {}) |
      (.general.newsletter.submit = $v)
    ' "$file" > "$file.tmp"
  else
    jq --arg v "$value" '
      if (.general and .general.newsletter and .general.newsletter.submit) then
        .
      else
        (.general //= {}) |
        (.general.newsletter //= {}) |
        (.general.newsletter.submit = $v)
      end
    ' "$file" > "$file.tmp"
  fi

  mv "$file.tmp" "$file"
  echo "✔ Updated: $file  → general.newsletter.submit = \"$value\"${FORCE:+ (forced)}"
}

if ! command -v jq >/dev/null 2>&1; then
  echo "❌ jq not found. Install it first (e.g., brew install jq, apt-get install jq)." >&2
  exit 1
fi

shopt -s nullglob
files=( "$LOCALES_DIR"/*.json )
if (( ${#files[@]} == 0 )); then
  echo "❌ No JSON files found in $LOCALES_DIR"
  exit 1
fi

for f in "${files[@]}"; do
  update_file "$f"
done

echo "✅ Done."
