#!/usr/bin/env bash
set -euo pipefail

PROD_BASE="https://rfam.org"
LOCAL_BASE="http://127.0.0.1:8888"

ENDPOINTS=(
  "/family/RF00360?content-type=application/json"
  "/family/RF00360?content-type=text/xml"
  "/family/snoZ107_R87?content-type=application/json"
  "/family/snoZ107_R87/acc"
  "/family/RF00360/id"
  "/family/snoZ107_R87/image/norm"
  "/family/RF00360/image/cov"
  "/family/RF00360/image/rscape"
  "/family/RF00360/image/rscape-cyk"
  "/family/snoZ107_R87/image/cons"
  "/family/RF00360/image/fcbp"
  "/family/RF00360/image/ent"
  "/family/RF00360/image/maxcm"
  "/family/snoZ107_R87/regions"
  "/family/RF00360/regions?content-type=text%2Fxml"
  "/family/RF00360/tree/"
  "/family/RF00360/tree/label/species/image"
  "/family/RF00360/tree/label/acc/image"
  "/family/RF00360/tree/label/acc/map"
  "/family/RF00360/tree/label/species/map"
  "/family/RF00002/structures?content-type=application/json"
  "/family/RF00002/structures?content-type=text/xml"
  "/family/RF00360/alignment"
  "/family/RF00360/alignment?gzip=1"
  "/family/RF00360/alignment/stockholm"
  "/family/RF00360/alignment/pfam"
  "/family/RF00360/alignment/fasta"
  "/family/snoZ107_R87/alignment/fastau"
)

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

compare() {
  local ep="$1"
  local prod_body="$TMPDIR/prod"
  local local_body="$TMPDIR/local"
  local prod_norm="$TMPDIR/prod_norm"
  local local_norm="$TMPDIR/local_norm"

  prod_status=$(curl -sS -L -o "$prod_body" -w "%{http_code}" "$PROD_BASE$ep")
  local_status=$(curl -sS -L -o "$local_body" -w "%{http_code}" "$LOCAL_BASE$ep")

  if [[ "$prod_status" != "$local_status" ]]; then
    printf "DIFFERENT (status) %-60s %s vs %s\n" "$ep" "$prod_status" "$local_status"
    return
  fi

  # For JSON responses, normalize by sorting keys before comparison
  if [[ "$ep" == *"application/json"* ]]; then
    python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(json.dumps(d,sort_keys=True))" "$prod_body" > "$prod_norm" 2>/dev/null || cp "$prod_body" "$prod_norm"
    python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(json.dumps(d,sort_keys=True))" "$local_body" > "$local_norm" 2>/dev/null || cp "$local_body" "$local_norm"

    if cmp -s "$prod_norm" "$local_norm"; then
      printf "IDENTICAL           %-60s\n" "$ep"
    else
      printf "DIFFERENT (body)    %-60s\n" "$ep"
    fi
  # For XML responses with timestamps, normalize timestamps before comparison
  elif [[ "$ep" == *"text/xml"* ]] || [[ "$ep" == *"text%2Fxml"* ]]; then
    # Remove timestamp lines from XML for comparison (handles various timestamp formats)
    sed -E 's/file built [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{2}-[A-Za-z]+-[0-9]{4}/file built TIMESTAMP/g' "$prod_body" > "$prod_norm"
    sed -E 's/file built [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{2}-[A-Za-z]+-[0-9]{4}/file built TIMESTAMP/g' "$local_body" > "$local_norm"

    if cmp -s "$prod_norm" "$local_norm"; then
      printf "IDENTICAL           %-60s\n" "$ep"
    else
      printf "DIFFERENT (body)    %-60s\n" "$ep"
    fi
  # For regions endpoint (plain text with timestamps)
  elif [[ "$ep" == *"/regions"* ]]; then
    # Remove timestamp lines from text for comparison
    sed -E 's/file built [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{2}-[A-Za-z]+-[0-9]{4}/file built TIMESTAMP/g' "$prod_body" > "$prod_norm"
    sed -E 's/file built [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{2}-[A-Za-z]+-[0-9]{4}/file built TIMESTAMP/g' "$local_body" > "$local_norm"

    if cmp -s "$prod_norm" "$local_norm"; then
      printf "IDENTICAL           %-60s\n" "$ep"
    else
      printf "DIFFERENT (body)    %-60s\n" "$ep"
    fi
  else
    if cmp -s "$prod_body" "$local_body"; then
      printf "IDENTICAL           %-60s\n" "$ep"
    else
      printf "DIFFERENT (body)    %-60s\n" "$ep"
    fi
  fi
}

for ep in "${ENDPOINTS[@]}"; do
  compare "$ep"
done
