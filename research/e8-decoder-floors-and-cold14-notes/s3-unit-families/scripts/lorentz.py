"""Lorentzian I_{n,1} units (#634 note 3: triples e_A + e_{n+1} and pairs e_i - e_j, n odd) as bit units.

Per n, exactly: v; window = rank of the Lorentz Gram (#634 proves the fitting minrank over char != 2 is n for n = 11, 13,
i.e. no rank-(n-1) labelling as for E8 = I_{9,1}); the binary labels (3-set / complement of a pair) satisfy
<u_S, u_T> = 1 + G_ST mod 2 (checked), so B0 = U U^T is a decoder of the #595 pattern with c0 = rank_F2(U) totals;
omega (pairwise non-orthogonal clique, exact) is a lower bound on the F_2 minrank; z = orthogonal neighbours per line;
cst_lab = attainable star cost of the label decoders on these labels (matroid-greedy over the 2^n - 1 functionals);
X* certified (skel.X) at x = cst_lab / v.  n = 9 is the E8 control (window 8 after the isotropic quotient).
Usage: python lorentz.py REPO_ROOT [n ...] [--json out]
"""
import sys
from fractions import Fraction as Fr

import numpy as np

REPO = sys.argv[1]
sys.path.insert(0, REPO + '/research/format-limits/scripts')
sys.dont_write_bytecode = True
from skel import X                      # noqa: E402

import units as U                       # noqa: E402


def greedy_cost(L, lab, rad=None):
    """rad: isotropic radical vector (n = 9); spans are then measured in the quotient by <rad>."""
    n = lab.shape[1]
    costs = []
    for p in range(1, 1 << n):
        pv = np.array([(p >> j) & 1 for j in range(n)])
        R = np.nonzero((lab @ pv) % 2)[0]
        costs.append(((U.rank_q(L[R].tolist() + ([rad] if rad is not None else [])) - (1 if rad is not None else 0)) if len(R) else 0, p))
    costs.sort()
    basis, tot, used = {}, 0, []
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
            tot += cst; used.append(cst)
        if len(basis) == n:
            break
    return tot, sorted(used)


def main():
    args = sys.argv[2:]
    jout = None
    if '--json' in args:
        jout = args[args.index('--json') + 1]
        args = args[:args.index('--json')]
    ns = [int(a) for a in args] or [9, 11, 13]
    rows = []
    for n in ns:
        L, G, lab = U.lorentz_family(n)
        v = len(L)
        assert (((lab @ lab.T) % 2) == ((1 + G) % 2)).all(), 'labels do not fit the pattern'
        h = U.rank_q(G.tolist())
        c0 = U.f2_rank(lab)
        om = U.nonorth_clique(G)
        z = sorted(set(int((G[i] == 0).sum()) for i in range(v)))
        rad = [1] * n + [3] if n == 9 else None
        cst, used = greedy_cost(L, lab, rad)
        # for n = 9 the label space is degenerate (w = (1,..,1,3) is isotropic): ranks of spans include the radical,
        # the quotient (E8) costs dim span - 1 per total that contains the radical; report the Gram ranks too
        x = Fr(cst, v)
        best = None
        for s in range(3, 17, 2):
            r = X(s, h, 1, x)
            if r and (best is None or r['hi'] > best[1]):
                best = (s, r['hi'])
        print('I_{%d,1}: v=%d window(Gram rank)=%d c0=rank_F2(labels)=%d omega=%d z=%s cst_lab=%d (per total %s) x=%s=%.4f X*=%s'
              % (n, v, h, c0, len(om), z, cst, used, x, float(x),
                 ('%.5e@s%d' % (float(best[1]), best[0])) if best else 'D<=0'), flush=True)
        rows.append(dict(n=n, v=v, window=h, c0=c0, omega=len(om), z=z, cst_lab=cst, per_total=used, x=str(x),
                         Xstar=None if best is None else dict(s=best[0], hi=str(best[1]))))
    if jout:
        import json
        json.dump(rows, open(jout, 'w'), indent=1)


if __name__ == '__main__':
    main()
