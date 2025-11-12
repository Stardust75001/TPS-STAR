#!/bin/bash

SCRIPTS_DIR="/Users/asc/Shopify/TPS STAR/TPS-STAR-WORKTREE/scripts"
RAPPORTS_DIR="/Users/asc/Shopify/TPS STAR/TPS-STAR-WORKTREE/rapports"

mkdir -p "$RAPPORTS_DIR/Scripts"
mkdir -p "$RAPPORTS_DIR/Ahrefs"
mkdir -p "$RAPPORTS_DIR/Workflows"

for script in "$SCRIPTS_DIR"/*; do
  base=$(basename "$script")
  ext="${base##*.}"
  name="${base%.*}"

  if [[ "$base" == *ahrefs* ]]; then
    outdir="$RAPPORTS_DIR/Ahrefs"
  elif [[ "$base" == *workflow* || "$base" == *ci* || "$base" == *sync* ]]; then
    outdir="$RAPPORTS_DIR/Workflows"
  else
    outdir="$RAPPORTS_DIR/Scripts"
  fi

  if [[ "$ext" == "csv" ]]; then
    cp "$script" "$outdir/$base"
  elif [[ "$ext" == "md" || "$ext" == "sh" || "$ext" == "py" || "$ext" == "js" ]]; then
    pandoc "$script" -o "$outdir/$name.pdf" --pdf-engine=tectonic
  fi
done

echo "✅ All scripts converted and organized in $RAPPORTS_DIR"
