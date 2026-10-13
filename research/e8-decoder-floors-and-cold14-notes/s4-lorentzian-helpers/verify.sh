#!/bin/sh
# S4 package: punctures of I_{11,1}/I_{13,1}, E8-skeleton features, calibrated model.  No kappa claim.
# Usage: sh verify.sh /path/to/integer-mult-bounds-main /fresh/out   [PY=python3.11]   (~30-40 min on 10 cores)
set -eu
REPO=$1; OUT=$2; PY=${PY:-python3}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"; cd "$HERE/scripts"
run() { name=$1; shift; "$PY" -B "$@" > "$OUT/$name.log" 2>&1; }
# exact certificates and exact computations (fast)
run census       census.py 11 13
run partition11  partition.py 11 2 1
run partition13  partition.py 13 7 3
run twocover8    twocover.py 8
run twocover11   twocover.py 11
run twocover13   twocover.py 13
run cellcover8   cellcover.py 8
run cellcover11  cellcover.py 11
run cellcover13  cellcover.py 13
run orbits11     clique_orbits.py 11 "$OUT/clique_orbits11.json"
"$PY" -B -c "import clique_orbits as C; print(C.survival_bound(11))" > "$OUT/survival11.log"
# slower steps in parallel
run packbases11  packbases.py 11 &
run packbases13  packbases.py 13 &
run punct11      punct.py "$REPO" 11 &
run example      example_pairlabel.py "$REPO" &
run frames8      frames.py 8 &
run frames11     frames.py 11 &
run model3       model3.py "$REPO" --json "$OUT/model3.json" &
for o in 0 1 2 3 4; do run sat19_o$o punct_sat.py 11 10 19 7200 "$OUT/clique_orbits11.json" $o & done
wait
"$PY" -B check.py "$HERE/expected" "$OUT"
