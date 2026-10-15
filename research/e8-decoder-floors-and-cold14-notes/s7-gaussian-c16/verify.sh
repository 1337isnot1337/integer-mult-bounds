#!/bin/sh
# S7 verification: rebuild the 3-flat level tables from scratch, then check the theorem. ~15-25 min, 8 processes.
# Needs python with numpy, networkx, python-sat on PATH.  CROSS=1 adds the glucose4 re-solve of all UNSAT prunings (~15 min).
set -e
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
HERE=$(cd "$(dirname "$0")" && pwd); W=${WORK:-$(mktemp -d)}
cp "$HERE"/scripts/*.py "$HERE"/data/flats_Gauss.pkl "$HERE"/data/orbits.pkl "$HERE"/data/pair_orbits.pkl "$W"/
cd "$W"
python lines.py | head -1
python levels2.py 16 3 3 8 vf | grep -E '^(LEVEL|EMPTY)'
python levels3.py 16 3 lev_vf.pkl 4 16 8 vf2 | grep -E '^(LEVEL|EMPTY)' | sed 's/ (.*//'
cp lev_vf2.pkl lev_c16_d3_hi.pkl
python prove_c16.py lev_vf2.pkl | sed 's/  (.*s)$//'
python price16.py
python levels2.py 15 3 1 1 calib15 | grep -E '^(LEVEL|EMPTY)' | sed 's/ (.*//'
if [ -n "$CROSS" ]; then python crosscheck.py 16 3 lev_vf2.pkl 8 glucose4 8 | grep CROSSCHECK | sed 's/ (.*//'; fi
echo "work dir: $W"
