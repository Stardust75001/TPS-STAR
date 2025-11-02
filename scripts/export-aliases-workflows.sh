#!/usr/bin/env bash
set -euo pipefail
LC_ALL=C

STAR="$HOME/Shopify/TPS-STAR-WORKTREE"
CSV1="$STAR/exports/aliases_workflows.csv"
CSV2="$STAR/exports/apis_secrets_metrics.csv"
mkdir -p "$STAR/exports"

tmp_aliases="$(mktemp)"
tmp_wf="$(mktemp)"

esc() { sed -e 's/"/""/g' -e 's/\r//g' -e 's/\n/ /g'; }

# -- Déterminer le repo (owner/name) pour gh
get_repo() {
  local url
  url="$(git -C "$STAR" remote get-url origin 2>/dev/null || true)"
  if [[ "$url" =~ github.com[:/]+([^/]+)/([^/.]+) ]]; then
    echo "${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
  else
    gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true
  fi
}
REPO="$(get_repo || true)"

echo "🔎 Génération du CSV principal…"

# --- Aliases : ~/.aliases + ~/.aliases_tps_docs (on exclut DOCSCSV)
for f in "$HOME/.aliases" "$HOME/.aliases_tps_docs"; do
  [[ -f "$f" ]] || continue
  awk '
    /^[[:space:]]*#/ {next}
    /^[[:space:]]*alias[[:space:]]+[A-Za-z0-9_+-]+=/ {
      line=$0
      sub(/^[[:space:]]*alias[[:space:]]+/,"",line)
      name=line; sub(/=.*/,"",name)
      if (name=="DOCSCSV") next
      cmd=$0
      sub(/^[[:space:]]*alias[[:space:]]+[A-Za-z0-9_+-]+=[\"\047]?/,"",cmd)
      sub(/[\"\047][[:space:]]*$/,"",cmd)
      print name "\t" cmd
    }' "$f"
done > "$tmp_aliases"

# --- Workflows : .github/workflows/*.yml
wfdir="$STAR/.github/workflows"
if [ -d "$wfdir" ] && ls "$wfdir"/*.yml >/dev/null 2>&1; then
  for f in "$wfdir"/*.yml; do
    base="$(basename "$f")"
    # nom de workflow
    name="$(grep -m1 '^[[:space:]]*name:' "$f" | sed 's/^[[:space:]]*name:[[:space:]]*//')"
    [ -z "${name:-}" ] && name="$base"

    # description "humaine" : job: X → Step1, Step2 ; job: Y → …
    desc="$(
      awk 'f||/^jobs:/{f=1;print}' "$f" \
      | awk '
          /^[[:space:]]{2}[A-Za-z0-9_-]+:[[:space:]]*$/{
            if (job!=""){ print job"|"steps; steps="" }
            job=$1; sub(":","",job); next
          }
          /- +name:[[:space:]]*/{
            s=$0; sub(/^.*- +name:[[:space:]]*/,"",s)
            steps=(steps?steps", ":steps) s
          }
          END{ if(job!=""){ print job"|"steps } }' \
      | awk -F'|' '
          BEGIN{ sep="" }
          {
            steps=$2; if (steps=="") steps="(no steps)"
            printf "%sjob: %s → %s", sep, $1, steps
            sep=" ; "
          }'
    )"

    # statut du dernier run (si gh auth et REPO dispo)
    status="—"
    if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 && [ -n "${REPO:-}" ]; then
      status="$(gh run list -R "$REPO" --workflow "$name" --limit 1 --json status,conclusion \
                -q '.[0].conclusion // .[0].status' 2>/dev/null || echo '—')"
    fi

    printf '%s\t%s\t%s\n' "$name" "$desc" "$status" >> "$tmp_wf"
  done
fi

# --- CSV #1 : aliases + workflows (+ statut)
{
  echo '"name","description","last_run_status"'
  if [ -s "$tmp_aliases" ]; then
    while IFS=$'\t' read -r n c; do
      printf '"%s","%s",""\n' "$(printf '%s' "$n" | esc)" "$(printf '%s' "$c" | esc)"
    done < "$tmp_aliases"
  fi
  if [ -s "$tmp_wf" ]; then
    while IFS=$'\t' read -r n d s; do
      printf '"%s","%s","%s"\n' \
        "$(printf '%s' "$n" | esc)" \
        "$(printf '%s' "$d" | esc)" \
        "$(printf '%s' "$s" | esc)"
    done < "$tmp_wf"
  fi
} > "$CSV1"
rm -f "$tmp_aliases" "$tmp_wf"
echo "✅ CSV principal généré : $CSV1"

# -------------------------------------------------------------------
# CSV #2 : APIs / secrets / variables / apps Shopify (valeurs masquées)
# -------------------------------------------------------------------
mask_val() {
  local v="$1" len=${#1}
  if [ "$len" -le 4 ]; then
    printf '%s' "$v"
  else
    printf '%s… (len %d)' "${v:0:4}" "$len"
  fi
}

echo "🔎 Génération du CSV API & secrets…"
{
  echo '"type","key","value_preview","source"'

  # GitHub secrets & vars (noms uniquement)
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 && [ -n "${REPO:-}" ]; then
    gh secret list  -R "$REPO" --json name,visibility \
      | jq -r '.[] | ["GitHub Secret", .name, "(hidden)", "GitHub"] | @csv' || true
    gh variable list -R "$REPO" --json name,value \
      | jq -r '.[] | ["GitHub Variable", .name, (.value//""), "GitHub"] | @csv' \
      | awk -F, 'BEGIN{OFS=","} { $3="\"\""; print }' || true
  fi

  # Shopify apps (si CLI loguée)
  if command -v shopify >/dev/null 2>&1; then
    shopify app list --json 2>/dev/null \
      | jq -r '.[] | ["Shopify App", (.title//.handle//"unknown"), "(api key hidden)", "Shopify"] | @csv' || true
  fi

  # Fichiers .env et *secrets* (BSD find, profondeur <= 3 via prune)
  while IFS= read -r -d '' f; do
    while IFS='=' read -r k v; do
      [ -z "$k" ] && continue
      vp="$(mask_val "${v:-}")"
      printf '"%s","%s","%s","%s"\n' \
        "Local Secret" "$(printf '%s' "$k" | esc)" \
        "$(printf '%s' "$vp" | esc)" "$(printf '%s' "$f" | esc)"
    done < <(grep -E '^[A-Z0-9_]+=' "$f" | sed 's/\r$//')
  done < <(
    find "$HOME/Shopify" "$STAR" \
      -type d -mindepth 4 -prune -o \
      -type f \( -name '.env*' -o -iname '*secrets*' \) -print0 2>/dev/null
  )

  # Variables d’environnement utiles (aperçu masqué)
  for k in GA_MEASUREMENT_ID GA4_MEASUREMENT_ID GTM_ID SENTRY_DSN AHREFS_API_KEY \
           DATADOG_API_KEY META_PIXEL_ID GOOGLE_API_KEY OPENAI_API_KEY; do
    v="${!k-}"; [ -z "${v:-}" ] && continue
    vp="$(mask_val "$v")"
    printf '"%s","%s","%s","%s"\n' "Env Var" "$k" "$vp" "ENV"
  done
} > "$CSV2"

echo "✅ CSV API/secrets généré : $CSV2"
