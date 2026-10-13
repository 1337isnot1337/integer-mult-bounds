"""Punctures of the Lorentzian units I_{n,1} (#634 note 3), star label decoders and Theorem C floors.

A puncture keeps a set of live lines.  For a live set:
  h      = Gram rank of the live lines (stage window, after the Lemma Q quotient by the radical),
  c0     = F2 rank of the live labels,
  star   = min over bases of the live label space of sum_j dim_Q span(R(p_j) & live)        (matroid greedy, exact)
  thmC   = the same with the Gram rank of the block G[R,R] (#446 Theorem C pairing floor of a label total)
  x      = star / v_live.
Spans are measured modulo the radical of the live Gram matrix (Lemma Q, #595 C.4), so that n = 9 gives E8 (8 per total)."""
import itertools, sys
from fractions import Fraction as Fr
import numpy as np
sys.dont_write_bytecode = True
import units as U


def family(n):
    L, G, lab = U.lorentz_family(n)
    return L, G, lab


def _rank_f(M):
    if len(M) == 0:
        return 0
    return int(np.linalg.matrix_rank(np.asarray(M, dtype=float)))


def evaluate(n, live, exact=True, fam=None):
    L, G, lab = fam or family(n)
    live = np.asarray(sorted(live))
    Ll, Gl, labl = L[live], G[np.ix_(live, live)], lab[live]
    rk = U.rank_q if exact else _rank_f
    span_all = rk(Ll.tolist())
    h = rk(Gl.tolist())
    rad = span_all - h                         # dimension of the radical of the live span
    # radical basis: vectors in span(Ll) orthogonal (Lorentz) to every live line
    Q = np.diag([1] * n + [-1])
    costs = []
    for pint in range(1, 1 << n):
        pv = np.array([(pint >> j) & 1 for j in range(n)])
        R = np.nonzero((labl @ pv) % 2)[0]
        if len(R) == 0:
            continue
        sp = rk(Ll[R].tolist())
        if rad:
            # dim of image in span/radical: rank of Gram pairing of R against all live lines
            sp = rk((Ll[R] @ Q @ Ll.T).tolist())
        gr = rk(Gl[np.ix_(R, R)].tolist())
        word = sum(1 << int(i) for i in R)          # reader word over the live lines
        costs.append((sp, gr, word, pint))
    star, used = _greedy(costs, 0, n)
    thc, usedc = _greedy(costs, 1, n)
    c0 = U.f2_rank(labl)
    return dict(n=n, v=len(live), h=h, rad=rad, c0=c0, star=star, star_totals=used, thmC=thc, thmC_totals=usedc,
                x=Fr(star, len(live)))


def _greedy(costs, key, n):
    cs = sorted(costs, key=lambda t: (t[key], t[3]))
    basis, tot, used = {}, 0, []
    seen = set()
    for t in cs:
        if t[2] in seen:
            continue
        seen.add(t[2])
        x = t[2]
        while x:
            hb = x.bit_length() - 1
            if hb in basis:
                x ^= basis[hb]
            else:
                basis[hb] = x
                break
        if x:
            tot += t[key]; used.append((t[key], t[3]))
    return tot, used


def coord_puncture(n, S):
    """live = lines not involving any coordinate in S (triples A with A & S empty, pairs disjoint from S)."""
    T = list(itertools.combinations(range(n), 3)); P = list(itertools.combinations(range(n), 2))
    lines = T + P
    return [i for i, l in enumerate(lines) if not set(l) & set(S)]


def Xstar(h, x, smax=15):
    sys.path.insert(0, _REPO + '/research/format-limits/scripts')
    from skel import X
    best = None
    for s in range(3, smax + 1, 2):
        r = X(s, h, 1, Fr(x))
        if r and (best is None or r['hi'] > best[1]):
            best = (s, r['hi'])
    return best


_REPO = None
if __name__ == '__main__':
    _REPO = sys.argv[1]
    for n in map(int, sys.argv[2:]):
        for k in range(0, n - 7):
            live = coord_puncture(n, range(n - k, n))
            r = evaluate(n, live)
            xs = Xstar(r['h'], r['x'])
            print('I_{%d,1} minus coords %s: v=%d h=%d rad=%d c0=%d star=%d %s thmC=%d x=%s=%.4f X*=%s' % (
                n, list(range(n - k, n)), r['v'], r['h'], r['rad'], r['c0'], r['star'], sorted(c for c, _ in r['star_totals']),
                r['thmC'], r['x'], float(r['x']), ('%.5e@s%d' % (float(xs[1]), xs[0])) if xs else 'D<=0'), flush=True)
