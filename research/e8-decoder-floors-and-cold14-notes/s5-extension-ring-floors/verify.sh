#!/bin/sh
# Re-run the checked claims and compare PASS/RESULT lines with expected.txt.  Usage: PY=python3.11 sh verify.sh
set -e
PY=${PY:-python3}
D=$(cd "$(dirname "$0")" && pwd)
OUT=$(mktemp -d)
cd "$D/scripts"
for s in lines eisen_floor hurwitz_floor gauss_pi gauss_bound40; do
  echo "== $s" >&2
  "$PY" -B "$s.py" | grep -E '^(PASS|FAIL|RESULT|Gauss|Eisen|Hurwitz) ' | sed 's/np\.int64(\([0-9]*\))/\1/g' >> "$OUT/got.txt"
done
"$PY" -B gauss_c15.py calib >> "$OUT/got.txt"
sed -E 's/ [0-9.]+ s$//' "$OUT/got.txt" > "$OUT/got2.txt"
if diff -u "$D/expected.txt" "$OUT/got2.txt"; then echo "ALL MATCH ($(grep -c '^PASS' "$OUT/got2.txt") PASS lines)"; else echo "MISMATCH"; exit 1; fi
