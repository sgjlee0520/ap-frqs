#!/usr/bin/env bash
# AP FRQ Bulk Downloader
# Downloads all 7,483 PDFs from apfrqs.com organized by course/year.
# Usage: bash download.sh
# Resume-safe: skips already-downloaded files.

set -euo pipefail

MANIFEST="manifest.json"
OUTPUT="files"
SLEEP=0.05
ERRORS=0
DOWNLOADED=0
SKIPPED=0

if ! command -v jq &>/dev/null; then
  echo "Error: jq is required. Install with: brew install jq  OR  sudo apt install jq"
  exit 1
fi

if [ ! -f "$MANIFEST" ]; then
  echo "Error: manifest.json not found. Run from repo root."
  exit 1
fi

TOTAL=$(jq 'length' "$MANIFEST")
echo "Starting download of $TOTAL files..."
echo ""

i=0
while IFS= read -r entry; do
  course=$(echo "$entry" | jq -r '.course')
  year=$(echo "$entry"   | jq -r '.year')
  name=$(echo "$entry"   | jq -r '.name')
  url=$(echo "$entry"    | jq -r '.url')

  # Sanitize course name for filesystem
  safe_course=$(echo "$course" | tr '/:' '--')
  dest="$OUTPUT/$safe_course/$year/$name"

  i=$((i + 1))

  if [ -f "$dest" ]; then
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  mkdir -p "$(dirname "$dest")"

  if curl -fsSL --retry 3 --retry-delay 2 -o "$dest" "$url"; then
    DOWNLOADED=$((DOWNLOADED + 1))
    echo "[$i/$TOTAL] ✓ $course / $year / $name"
  else
    ERRORS=$((ERRORS + 1))
    echo "[$i/$TOTAL] ✗ FAILED: $course / $year / $name"
    rm -f "$dest"
  fi

  sleep "$SLEEP"

done < <(jq -c '.[]' "$MANIFEST")

echo ""
echo "============================================================"
echo "Done. Downloaded: $DOWNLOADED | Skipped: $SKIPPED | Errors: $ERRORS"
