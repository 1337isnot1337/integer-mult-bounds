"""S7 step 2c: cost-aware refinement of the 3-flat level search ("dumbbells").

Per total j (X_j = span R_j, Y_j = span A_j, Hermitian definite form on K^4, beta_j = dim X - dim(X cap Y^perp)):
  full   (4,4)                    beta = 4
  'a'    a side of dim <= 2       beta >= 0      (at most 2 such totals: 2-flat level search, lev_c16_d2.pkl)
  'p'    (3,3), beta = 2          both X_j, Y_j are 3-flats containing a side, X_j != Y_j  -> a DUMBBELL
  'q'    otherwise cheap          beta >= 3      (one 3-flat side; also (3,3) with beta = 3)
cost <= 42 with 16 totals:  4f + 2p + 3q <= 42, f = 16 - a - p - q   <=>   3a + p >= 22 - k,  k = a + p + q.
Every transversal (one 3-flat per cheap total: for p-totals either X_j or Y_j; for a-totals any 3-flat containing the
small side) is a valid level-k set (all hyperplanes distinct since one 3-flat cannot host two totals).
So a <= 42 decoder needs a level-k rep T (k = 9..15) and a choice of p members with partners Y (beta(t, Y) = 2) such that
all 2^p transversals are level-k sets, with 3*min(2, k-p) + p >= 22 - k.
This script computes, for every level-k rep, the maximum number p* of simultaneously doubled members."""
import sys, time, pickle, itertools
sys.path.insert(0, sys.path[0])
import numpy as np
from levels2 import load_flats, canon_many, canon
from lines import views

S = views()['Gauss']
J = S.ops[1]


def hyperplane_bases(fl):
    out = []
    for d, f in fl:
        rows = np.array([v for T in f for v in (S.reps[T], J @ S.reps[T])], float)
        u, s, vt = np.linalg.svd(rows)
        r = int((s > 1e-9 * s[0]).sum()); assert r == 2 * d
        out.append(vt[:r])
    return np.array(out)  # NF x 6 x 8 orthonormal real bases


def beta_matrix(Bs):
    """beta(X,Y) = real rank(Bx By^T)/2 for all pairs, by SVD; true rank-2 (real rank 4) pairs have sigma_5 ~ 1e-15."""
    NF = len(Bs); beta = np.zeros((NF, NF), np.int8)
    for i in range(NF):
        M = np.einsum('ik,njk->nij', Bs[i], Bs)
        s = np.linalg.svd(M, compute_uv=False)
        r = (s > 1e-7).sum(1)
        amb = ((s > 1e-11) & (s < 1e-3)).any(1)
        assert not amb.any(), 'ambiguous rank'
        assert (r % 2 == 0).all()
        beta[i] = r // 2
    return beta


def main():
    G, fl, P = load_flats('3')
    NF = len(fl)
    good = pickle.load(open(sys.argv[1], 'rb'))['good']
    t0 = time.time()
    beta = beta_matrix(hyperplane_bases(fl))
    print('beta histogram over ordered pairs', np.bincount(beta.flatten()).tolist(), '(%.0fs)' % (time.time() - t0), flush=True)
    comp = np.zeros((NF, NF), bool)
    for (a, b) in good[2]:
        comp[P[:, a], P[:, b]] = True; comp[P[:, b], P[:, a]] = True
    feasible = []
    for k in range(9, 16):
        need_best = None
        stats = []
        for T in sorted(good[k]):
            T = list(T)
            partners = {}
            for idx, t in enumerate(T):
                rest = T[:idx] + T[idx + 1:]
                ys = [y for y in range(NF) if y not in T and beta[t, y] == 2 and comp[y, rest].all()]
                ok = []
                if ys:
                    cs = canon_many(P, rest, ys)
                    ok = [y for y, cf in zip(ys, cs) if cf in good[k]]
                if ok: partners[idx] = ok
            # max number of members doubled simultaneously, all transversals valid (backtracking)
            best = [0]
            mem = sorted(partners)

            def valid_all(choice):
                # choice: dict idx -> partner; check every transversal
                items = list(choice.items())
                for mask in range(1 << len(items)):
                    X = list(T)
                    for b, (idx, y) in enumerate(items):
                        if mask >> b & 1: X[idx] = y
                    if canon(P, X) not in good[k]: return False
                return True

            def rec(pos, choice):
                best[0] = max(best[0], len(choice))
                if len(choice) + (len(mem) - pos) <= best[0]: return
                for q in range(pos, len(mem)):
                    idx = mem[q]
                    for y in partners[idx]:
                        if y in choice.values(): continue
                        # newly added transversals: those using y
                        choice[idx] = y
                        if valid_all(choice): rec(q + 1, choice)
                        del choice[idx]
            rec(0, {})
            p = best[0]
            # feasibility: exists p' <= p, a' <= min(2, k - p') with 3a' + p' >= 22 - k
            feas = any(3 * min(2, k - pp) + pp >= 22 - k for pp in range(p + 1))
            stats.append((p, len(partners)))
            if feas: feasible.append((k, tuple(T), p))
        from collections import Counter
        print('k=%d reps %d  (p*, #doublable members) histogram %s  feasible %d  (%.0fs)' % (
            k, len(good[k]), sorted(Counter(stats).items()), sum(1 for f in feasible if f[0] == k), time.time() - t0), flush=True)
    pickle.dump({'feasible': feasible, 'beta': beta}, open('dumbbell_out.pkl', 'wb'))
    print('FEASIBLE CONFIGURATIONS:', len(feasible), flush=True)


if __name__ == '__main__':
    main()
