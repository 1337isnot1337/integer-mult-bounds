"""Triple family T_h (upstream 03-motifs.tex, the Alon-type unit): decoder, copy cost and certified ceiling.

Bit side.  Lines t_T (T a 3-subset of [h]) in Q^h with the form I - J/9: G_ST = |S n T| - 1.  Pattern: B_TS = 0 where
|S n T| in {0, 2}, free where |S n T| = 1.  Label decoder B0 = M M^T mod 2 (M = incidence; the h centres C_i of the
paper): B0_ST = |S n T| mod 2.
Complex side.  Lines t_T in F_2^h with the dot product (t_T . t_T = 1).  Pattern: B_TS = 0 where |S n T| = 1 (odd),
free where |S n T| in {0, 2}.  Decoder over a field of characteristic 0: the paper's h + 1 centres C_i, C_*, with
B_ST = (|S n T| - 1)/2.

Per h the script computes, exactly:
  window      rank of the form on span{t_T}                    (Q for bit, F_2 for complex)
  c           totals of the centre decoder; for bit also rank_F2(B0) and the clique lower bound 4*floor(h/4)
              (4 triples inside a 4-set are pairwise at even intersection; odd-weight pairwise-orthogonal vectors of
              F_2^h are independent, so the clique number is <= h)
  cst_att     star cost of the centre decoder = sum_i dim span(gathered lines)    (attained: copy f = V -> 0)
  cst_thmC    #446 Theorem C floor of the centre decoder = sum_i rank of the pairing span(gathered) x span(readers)
  X*(att)     certified #595 ceiling skel.X at x = cst_att / v, best odd s in 3..15
For small h (bit, h <= MAXEXACT) also:
  minrank     exact F_2 minrank of the pattern (SAT, #595's encoder), and
  lab_min     min over nonzero p in F_2^h of dim_Q span{t_T : |T n supp p| odd}  (every label decoder on the B0 labels
              has each total gathering such a set, so cst >= c * lab_min for those decoders)
Usage: python triple.py REPO_ROOT HMIN HMAX [--exact MAXEXACT] [--json out]
"""
import itertools
import json
import sys
from fractions import Fraction as Fr
from math import comb

import numpy as np

REPO = sys.argv[1]
sys.path.insert(0, REPO + '/research/format-limits/scripts')
sys.dont_write_bytecode = True
from skel import X                      # noqa: E402
from minrank_sat import solve_asym      # noqa: E402

import units as U                       # noqa: E402

S_RANGE = range(3, 17, 2)


def xstar(h, x):
    best = None
    for s in S_RANGE:
        r = X(s, h, 1, Fr(x))
        if r and (best is None or r['hi'] > best[1]):
            best = (s, r['hi'])
    return best


def q_pair_rank(rows, Qform):
    """rank over Q of the Gram matrix of span(rows) under Qform (integer)."""
    idx = []
    red = []
    import math
    for i, r in enumerate(rows):
        rr0 = [int(x) for x in r]
        rr = rr0
        for pc, b in red:
            if rr[pc]:
                f, g = rr[pc], b[pc]
                rr = [g * x - f * y for x, y in zip(rr, b)]
                c = math.gcd(*rr)
                if c > 1:
                    rr = [x // c for x in rr]
        pc = next((j for j, x in enumerate(rr) if x), None)
        if pc is not None:
            red.append((pc, rr)); idx.append(i)
    B = np.array([rows[i] for i in idx], dtype=object)
    Gm = B.dot(np.array(Qform, dtype=object)).dot(B.T)
    return len(idx), U.rank_q(Gm.tolist())


def f2_dim(rows):
    return U.f2_rank(np.array(rows))


def f2_pair_rank(rows):
    """dim and dot-product rank of span(rows) over F_2."""
    rows = np.array(rows, dtype=np.int64) % 2
    # basis
    basis = []
    for r in rows:
        x = int(''.join(str(int(b)) for b in r[::-1]), 2)
        for b in basis:
            x = min(x, x ^ b)
        if x:
            basis.append(x)
    n = rows.shape[1]
    Bm = np.array([[(b >> j) & 1 for j in range(n)] for b in basis], dtype=np.int64)
    return len(basis), U.f2_rank((Bm @ Bm.T) % 2)


def bit_row(h, exact):
    M, G, T = U.triple_family(h)
    v = len(T)
    Qf = 9 * np.eye(h, dtype=np.int64) - 1            # 9 (I - J/9); ranks are unchanged by the factor 9
    dimall, window = q_pair_rank(M.tolist(), Qf.tolist())
    c0 = U.f2_rank(M @ M.T % 2)
    att, thm = 0, 0
    per = []
    for i in range(h):
        R = [k for k, t in enumerate(T) if i in t]
        d, pr = q_pair_rank(M[R].tolist(), Qf.tolist())
        att += d; thm += pr; per.append((d, pr))
    row = dict(side='bit', h=h, v=v, window=window, span=dimall, c_centre=h, c0=c0, clique_lb=4 * (h // 4),
               z=3 * comb(h - 3, 2), cst_att=att, cst_thmC=thm, per_total=sorted(set(per)))
    if exact and h <= exact:
        off = [(i, j) for i in range(v) for j in range(i + 1, v) if G[i, j] != 0]
        # explicit clique: disjoint 4-sets' triples
        cl = []
        for b in range(h // 4):
            pts = range(4 * b, 4 * b + 4)
            cl += [T.index(tuple(t)) for t in itertools.combinations(pts, 3)]
        lo, hi, log = U.minrank_f2(G, cl, c0, solve_asym, timeout=600)
        c = lo if lo == hi else '%d..%d' % (lo, hi)
        row['minrank'] = c
        row['minrank_log'] = log
        lab = None
        for p in range(1, 1 << h):
            P = [j for j in range(h) if p >> j & 1]
            R = [k for k, t in enumerate(T) if len(set(t) & set(P)) % 2]
            d = U.rank_q(M[R].tolist())
            lab = d if lab is None else min(lab, d)
        row['lab_min'] = lab
    return row


def cx_row(h):
    M, G, T = U.triple_family(h)
    v = len(T)
    dimall, window = f2_pair_rank(M.tolist())
    # centre decoder rank over Q of (M M^T - J)/2  = rank of [M | 1] (Gram-type), exact
    Bc = (M @ M.T - 1)
    cdec = U.rank_q(np.hstack([M, np.ones((v, 1), dtype=np.int64)]).tolist())
    att, thm = 0, 0
    per = []
    for i in range(h):
        R = [k for k, t in enumerate(T) if i in t]
        d, pr = f2_pair_rank(M[R].tolist())
        att += d; thm += pr; per.append((d, pr))
    d, pr = f2_pair_rank(M.tolist())                   # C_* gathers every line
    att += d; thm += pr; per.append((d, pr))
    return dict(side='complex', h=h, v=v, window=window, span=dimall, c_centre=h + 1, rank_centre_matrix=cdec,
                z=comb(h - 3, 3) + 3 * (h - 3), cst_att=att, cst_thmC=thm, per_total=sorted(set(per)))


def main():
    hmin, hmax = int(sys.argv[2]), int(sys.argv[3])
    exact = int(sys.argv[sys.argv.index('--exact') + 1]) if '--exact' in sys.argv else 0
    rows = []
    for h in range(hmin, hmax + 1):
        for r in (bit_row(h, exact), cx_row(h)):
            x_att, x_thm = Fr(r['cst_att'], r['v']), Fr(r['cst_thmC'], r['v'])
            wnd = r['window']
            # the window entering skel.X is the rank of the label space (Theorem B uses the window form)
            for key, x in (('att', x_att), ('thmC', x_thm)):
                b = xstar(wnd, x)
                r['X_' + key] = None if b is None else dict(s=b[0], hi=str(b[1]), f=float(b[1]))
            r['x_att'], r['x_thmC'] = str(x_att), str(x_thm)
            rows.append(r)
            fx = lambda k: ('%.5e@s%d' % (r[k]['f'], r[k]['s'])) if r[k] else 'D<=0'
            extra = (' minrank=%s lab_min=%s' % (r.get('minrank'), r.get('lab_min'))) if 'minrank' in r else ''
            print('%-7s h=%2d v=%5d window=%2d c=%2d cst_att=%4d cst_thmC=%4d x_att=%.4f X*att=%s X*thmC=%s z=%d per=%s%s'
                  % (r['side'], h, r['v'], wnd, r['c_centre'], r['cst_att'], r['cst_thmC'], float(x_att), fx('X_att'),
                     fx('X_thmC'), r['z'], r['per_total'], extra), flush=True)
    if '--json' in sys.argv:
        json.dump(rows, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
