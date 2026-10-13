#!/bin/sh
# Recompute every number of this package and compare with expected.json.
# Usage: sh verify.sh REPO_ROOT OUT_DIR
#   REPO_ROOT: a checkout of CrocSwap/integer-mult-bounds main (reads research/format-limits/scripts: skel.py, cert.py,
#              minrank_sat.py, e8units.py of #595); OUT_DIR: fresh output directory.
# Python >= 3.11 with numpy, networkx, python-sat on PATH as `python3` (or set PY).  About 40 min on 10 cores
# (the steps run in parallel; the ADE step spends up to 600 s in each of its two SAT timeouts).
set -eu
REPO=$(cd "$1" && pwd); OUT=$2
PY=${PY:-python3}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
cd "$HERE/scripts"
$PY -B ade_screen_fixed.py "$REPO" --json "$OUT/ade.json"          > "$OUT/ade.log" 2>&1 &
$PY -B triple.py "$REPO" 6 32 --exact 11 --json "$OUT/triple.json"  > "$OUT/triple.log" 2>&1 &
$PY -B lorentz.py "$REPO" 9 11 13 --json "$OUT/lorentz.json"        > "$OUT/lorentz.log" 2>&1 &
$PY -B lorentz_minrank.py "$REPO" 11 600 --json "$OUT/lorentz_minrank.json" > "$OUT/lorentz_minrank.log" 2>&1 &
$PY -B cover.py "$REPO" E8,T8,T10,T12,T16,T20,T24,L11,L13 20000 --json "$OUT/cover.json" > "$OUT/cover.log" 2>&1 &
$PY -B rank.py "$REPO" --json "$OUT/rank.json"                      > "$OUT/rank.log" 2>&1 &
wait
$PY -B check.py "$OUT" "$HERE/expected.json"
