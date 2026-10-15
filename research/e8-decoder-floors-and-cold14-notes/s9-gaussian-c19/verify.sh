#!/bin/sh
# S9 verification.  Rebuilds every input from scratch (exact lines/flats/cliques, certified ranks), then
#  (1) the mu-packing optima f(k) (HiGHS) + CP-SAT cross-checks,
#  (2) the type catalog (58,340 types), its 27 orbits and the lifting data,
#  (3) calibrations of the case ILP (must be FEASIBLE) and the F2 confinement checks of the c = 21 counting covers,
#  (4) [FULL=1] every case ILP of Theorems 1-2 (HiGHS; hours; PAR parallel jobs, default 6).
# Lines printed (times stripped) should match expected.txt (FULL part: expected_full.txt).
# Needs python 3.11 + numpy scipy sympy networkx python-sat ortools on PATH.
set -e
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
HERE=$(cd "$(dirname "$0")" && pwd); W=${WORK:-$(mktemp -d)}; PAR=${PAR:-6}
cp "$HERE"/scripts/*.py "$W"/; cd "$W"
strip() { sed -E 's/ [0-9]+s$//'; }
python flats.py Gauss > /dev/null
python orbits.py
python hits_table.py | grep -E '^(PASS|RESULT)'
python types_e.py 256 | head -1
python dom.py | head -2
python lift_prep.py > /dev/null && echo "lift.pkl built"
for cap in 6 7 8 9 10 11 12; do python mu_ilp.py $cap 600 | head -1 | awk '{printf "mu-packing: cap %s  max |mu| = %d  (LP %d)\n",$1,int($(NF-3)+0.5),5*$1}'; done
python mu_cpsat.py 7 33 2 | strip
python mu_cpsat.py 8 37 2 | strip
echo "calibrations (must be FEASIBLE):"
python branch1.py 21 42 -1 600 feas | head -1 | strip
python branch1.py 19 44 -1 600 feas | head -1 | strip
python pairkinds.py | head -1
python f2check.py
python check_c21cover.py
python try_cand.py "[(1,54),(3,4),(5,59),(6,18),(7,19),(8,57),(20,32),(21,31),(23,24),(25,51),(28,58),(29,52),(33,56),(35,48),(36,50),(38,53),(39,46),(40,55),(41,47),(42,44),(43,45)]" | strip
python core.py "[(1,54),(3,4),(5,59),(6,18),(7,19),(8,57),(20,32),(21,31),(23,24),(25,51),(28,58),(29,52),(33,56),(35,48),(36,50),(38,53),(39,46),(40,55),(41,47),(42,44),(43,45)]"
if [ -n "$FULL" ]; then
  for cc in "19 42" "20 41" "20 42"; do
    set -- $cc
    CASES=$(python -c "
import pickle; T=pickle.load(open('types_e256.pkl','rb')); L=pickle.load(open('lift.pkl','rb')); d=pickle.load(open('dom.pkl','rb'))
s=128*($2+$1)-7680
print(' '.join(['-1']+[str(k) for k,r in enumerate(d['reps']) if L[r][1]>0 and T[r][3]<=s]))")
    echo "$CASES" | tr ' ' '\n' | xargs -P $PAR -I{} python branch1.py $1 $2 {} ${TL:-14400} $MODE | strip | sort -t' ' -k4,4n
  done
fi
echo "work dir: $W"
