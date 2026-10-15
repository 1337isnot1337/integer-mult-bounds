#!/bin/sh
# S8 verification (~6 min, 1 process; prints PASS/RESULT lines identical to expected.txt): rebuild the S5 flat-pair table (exact hits, certified ranks), then check
# the two counting facets (cost >= max(40, 60 - c)) and the c = 18 parity argument.  Compare with expected.txt.
# Needs python 3.11 with numpy, scipy, sympy, networkx on PATH.
set -e
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
HERE=$(cd "$(dirname "$0")" && pwd); W=${WORK:-$(mktemp -d)}
cp "$HERE"/scripts/*.py "$W"/
cd "$W"
python hits_table.py | grep -E '^(PASS|RESULT)'
python facets.py
python c18.py
python check_c21cover.py
echo "work dir: $W"
