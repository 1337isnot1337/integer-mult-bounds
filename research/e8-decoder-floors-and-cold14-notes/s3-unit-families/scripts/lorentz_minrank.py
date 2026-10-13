"""F_2 minrank of the #595 pattern on I_{n,1} (n = 11: is it 10 = omega or 11 = c0?).  SAT with the clique gauge,
time-limited; prints the outcome per c.  Usage: python lorentz_minrank.py REPO_ROOT n timeout_s [--json out]"""
import sys
REPO = sys.argv[1]
sys.path.insert(0, REPO + '/research/format-limits/scripts')
sys.dont_write_bytecode = True
from minrank_sat import solve_asym   # noqa: E402
import units as U                    # noqa: E402

n, T = int(sys.argv[2]), int(sys.argv[3])
L, G, lab = U.lorentz_family(n)
om = U.nonorth_clique(G)
c0 = U.f2_rank(lab)
print('I_{%d,1}: omega=%d c0=%d' % (n, len(om), c0), flush=True)
lo, hi, log = U.minrank_f2(G, om, c0, solve_asym, timeout=T)
print(lo, hi, log, flush=True)
if '--json' in sys.argv:
    import json
    json.dump([dict(n=n, omega=len(om), c0=c0, lo=lo, hi=hi, log={k: v[0] for k, v in log.items()})],
              open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
