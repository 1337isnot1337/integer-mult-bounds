"""Corrected ADE unit screen (replaces #620's ade_screen.py; erratum found by #630).

Per unit (real root lines, window h = Gram rank, k = 1):
  v, h                 exact
  c0 = rank_F2(J + G)  the label decoder B0 used by #620 (an UPPER bound on the F2 minrank of the pattern)
  omega                largest pairwise non-orthogonal set (identity block of the pattern) -> minrank >= omega
  c = minrank          exact F2 minrank of the pattern (asymmetric decoders allowed, SAT; c-1 UNSAT, c SAT)
  x_proxy = c*h/v      #620's full-rank-totals premise (each total charged the window), now with the exact minrank
  cst_lab              star cost attainable by label decoders on the B0 labels: min over bases {p_j} of F2^c0 of
                       sum_j dim_Q span{lines T : u_T . p_j = 1} (matroid greedy, exact); an UPPER bound on cst_min
  X*                   certified ceiling of #595 (skel.X, rational intervals) maximised over odd s in 3..15

What changed against #620:
  * E6 was built as the complement of two ORTHOGONAL roots (= D6, 30 lines); it is now the complement of an A2 (36 lines).
  * the column 'c' was rank_F2(J+G) of one decoder; it is now the exact minrank (both are printed).
  * an attainable label-decoder star cost is added next to the proxy.
Usage: python ade_screen_fixed.py REPO_ROOT [--json out.json]
"""
import json
import sys
import time
from fractions import Fraction as Fr

import numpy as np

REPO = sys.argv[1]
sys.path.insert(0, REPO + '/research/format-limits/scripts')
sys.dont_write_bytecode = True
from skel import X, profile             # noqa: E402  (#595, certified ceiling)
from cert import cost_iv                # noqa: E402
from minrank_sat import solve_asym      # noqa: E402  (#595 SAT encoding, GL(c) gauge on a clique)
from e8units import sym_factor_f2       # noqa: E402

import units as U                       # noqa: E402

S_RANGE = range(3, 17, 2)
TIMEOUT = 600                           # seconds per SAT query (A8, D9 hit it: minrank left as a range)


def xstar(h, x):
    best = None
    for s in S_RANGE:
        r = X(s, h, 1, Fr(x))
        if r and (best is None or r['hi'] > best[1]):
            best = (s, r['hi'], r['lo'])
    return best


def minrank(G, omega_set, c0):
    lo, hi, log = U.minrank_f2(G, omega_set, c0, solve_asym, timeout=TIMEOUT)
    return (lo if lo == hi else '%d..%d' % (lo, hi)), log, lo


def label_cost(L, G):
    B0 = (1 + G) % 2
    Uf = sym_factor_f2(B0).astype(np.int64)
    c0 = Uf.shape[1]
    costs = []
    for p in range(1, 1 << c0):
        pv = np.array([(p >> j) & 1 for j in range(c0)])
        R = np.nonzero((Uf @ pv) % 2)[0]
        costs.append((U.rank_q(L[R].tolist()), p))
    costs.sort()
    basis, tot = {}, 0
    for cst, p in costs:
        x = p
        while x:
            hb = x.bit_length() - 1
            if hb in basis:
                x ^= basis[hb]
            else:
                basis[hb] = x
                break
        if x:
            tot += cst
        if len(basis) == c0:
            break
    return tot, c0


def unit(name, L, G=None):
    if G is None:
        G = U.gram_doubled(L)
    v = len(L)
    h = U.rank_q(G.tolist())
    c0 = U.f2_rank((1 + G) % 2)
    om = U.nonorth_clique(G)
    c, log, clo = minrank(G, om, c0)
    cst_lab, _ = label_cost(L, G)
    xp = Fr(clo * h, v)                 # proxy at the certified lower end of the minrank
    xl = Fr(cst_lab, v)
    row = dict(unit=name, v=v, h=h, c0=c0, omega=len(om), minrank=c, sat_log={k: v_ for k, v_ in log.items()},
               x_proxy=str(xp), cst_lab=cst_lab, x_lab=str(xl))
    for key, x in (('proxy', xp), ('lab', xl)):
        b = xstar(h, x)
        row['Xstar_' + key] = None if b is None else dict(s=b[0], hi=str(b[1]), hi_float=float(b[1]))
    if row['Xstar_lab'] is None and xl < 1:
        # positive deficit only at s > 1/(1 - x): bound the ceiling by D_s / Cost_s (#595 A.2) for odd s up to 801
        best = None
        for s_ in range(3, 802, 2):
            prof, m, D = profile(s_, h, 1, xl)
            if D <= 0:
                continue
            b = D / cost_iv(prof, m)[0]
            if best is None or b > best[1]:
                best = (s_, b)
        row['DoverCost_lab'] = dict(s=best[0], hi=str(best[1]), hi_float=float(best[1]))
        print('   %s: x_lab < 1, deficit > 0 only for s > %s; max over odd s <= 801 of D_s/Cost_s = %.4e at s = %d'
              % (name, 1 / (1 - xl), float(best[1]), best[0]))
    return row


def main():
    rows = []
    cases = [('A%d' % n, U.roots_A(n)) for n in (4, 5, 6, 7, 8)]
    cases += [('D%d' % n, U.roots_D(n)) for n in (4, 5, 6, 7, 8, 9, 10, 12)]
    cases += [('D6(archived "E6")', U.roots_D6_archived()), ('E6', U.roots_E6()), ('E7', U.roots_E7()), ('E8', U.roots_E8())]
    for name, L in cases:
        t = time.time()
        r = unit(name, L)
        rows.append(r)
        f = lambda k: ('%.4e@s%d' % (r[k]['hi_float'], r[k]['s'])) if r[k] else 'D<=0'
        print('%-18s v=%4d h=%2d c0=%2d omega=%2d minrank=%-5s x_proxy=%-7s cst_lab=%4d x_lab=%-8s X*proxy=%-14s X*lab=%-14s (%.0fs)'
              % (name, r['v'], r['h'], r['c0'], r['omega'], r['minrank'], r['x_proxy'], r['cst_lab'], r['x_lab'],
                 f('Xstar_proxy'), f('Xstar_lab'), time.time() - t), flush=True)
    if '--json' in sys.argv:
        json.dump(rows, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
