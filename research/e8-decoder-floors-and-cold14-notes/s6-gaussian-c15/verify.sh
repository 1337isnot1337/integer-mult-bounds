#!/bin/sh
# Usage: PATH=<venv>/bin:$PATH sh verify.sh   (python3.11 + numpy, networkx, python-sat). ~3 min (orbit mode), 3 processes.
# Optional: FULL=1 also runs the group-free sweep over all 1500 3-flats (~45 min with 3 processes).
set -e
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
cd "$(dirname "$0")/scripts"
python -B flats.py Gauss                                   # writes flats_Gauss.pkl
python -B orbits.py                                        # group of order 11520, orbits on 3-flats
python -B prove_c15.py orbits cadical153,glucose4,maplechrono | sed 's/ [0-9.]*s / Ts /; s/\[[0-9]*\/18\]//' | sort
python -B price_c15.py
if [ -n "$FULL" ]; then python -B prove_c15.py all | tail -1; fi
