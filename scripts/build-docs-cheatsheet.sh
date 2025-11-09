#!/usr/bin/env bash
set -euo pipefail
steps=()

OUT="$HOME/Shopify/TPS-STAR-WORKTREE/docs/WORKFLOWS-CHEATSHEET.md"
TS="$(date '+%Y-%m-%d %H:%M:%S')"
mkdir -p "$(dirname "$OUT")"

# Détecte le repo "owner/name"
detect_repo() {
  local nwo=""
  if command -v gh >/dev/null 2>&1; then
    nwo="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
  fi
  if [ -z "$nwo" ]; then
    # fallback via git remote
    local url
    url="$(git -C "$HOME/Shopify/TPS-STAR-WORKTREE" config --get remote.origin.url 2>/dev/null || true)"
    # ssh -> git@github.com:owner/repo.git | https -> https://github.com/owner/repo(.git)
    nwo="$(printf '%s\n' "$url" | sed -E 's#(git@github\.com:|https://github\.com/)##; s#\.git$##')"
  fi
  printf '%s' "$nwo"
}
NWO="$(detect_repo)"

{
  echo "# 🚀 TPS — Workflows & Pipelines (Cheat Sheet)"
  echo "_Généré automatiquement le ${TS}_"
  echo

  WF_DIR="$HOME/Shopify/TPS-STAR-WORKTREE/.github/workflows"
  if [ -d "$WF_DIR" ]; then
    find "$WF_DIR" -type f \( -name '*.yml' -o -name '*.yaml' \) | sort | while IFS= read -r f; do
      # Nom du workflow (clé 'name:' ou nom de fichier)
      name="$(awk '/^[[:space:]]*name:[[:space:]]*/{sub(/^[[:space:]]*name:[[:space:]]*/,""); print; exit}' "$f")"
      [ -z "$name" ] && name="$(basename "$f")"

      echo "## $name"
      echo
      echo "- Fichier : \`$(basename "$f")\`"

      # Dernier statut via gh (si auth OK)
      status_str="—"
      if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 && [ -n "$NWO" ]; then
        status_str="$(gh run list -R "$NWO" --workflow "$name" --json status,conclusion,updatedAt --limit 1 2>/dev/null \
          | awk -F'"' '/status/ {st=$4} /conclusion/ {co=$4} /updatedAt/ {ts=$4} END{ if (st!="") printf("%s/%s @ %s", st, co, ts); }')"
        [ -z "$status_str" ] && status_str="—"
      fi
      echo "- Dernier run : $status_str"

      echo
      echo "### Jobs"

      # Jobs + steps (robuste sans mapfile)
      awk 'f||/^jobs:/{f=1;print}' "$f" \
      | awk '
        /^[[:space:]]{2}[A-Za-z0-9_-]+:[[:space:]]*$/{
          if (job!=""){ print "JOB_END"; }
          job=$1; sub(":","",job); print "JOB="job; next
        }
        /- +name:[[:space:]]*/{
          s=$0; sub(/^.*- +name:[[:space:]]*/,"",s); print "STEP="s
        }
        END{ if (job!="") print "JOB_END" }' \
      | awk '
        BEGIN{ prev=""; acc="" }
        /^JOB=/{ 
          if (prev!=""){ print "OUT "prev"|"acc }
          prev=substr($0,5); acc=""; next
        }
        /^STEP=/{ s=substr($0,6); acc=(acc?acc", ":acc) s; next }
        /^JOB_END$/{ 
          if (prev!=""){ print "OUT "prev"|"acc }
          prev=""; acc=""; next
        }
        END{ if (prev!="") print "OUT "prev"|"acc }' \
      | while IFS='|' read -r tag payload; do
          job="${tag#OUT }"
          echo "  - **$job**"
          IFS=',' read -r -a steps <<<"$payload"
          for s in "${steps[@]}"; do
            s="$(echo "$s" | sed 's/^ *//')"
            [ -n "$s" ] && echo "    - $s"
          done
        done

      echo
      echo "---"
      echo
    done
  else
    echo "_Aucun dossier .github/workflows trouvé._"
    echo
  fi

  echo "<sub>© Falcon Trading Company — document généré.</sub>"
} > "$OUT"

echo "✅ Cheat Sheet enrichie : $OUT"
