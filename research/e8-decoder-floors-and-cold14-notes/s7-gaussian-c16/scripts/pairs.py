"""S7 step 2a: orbits of unordered pairs of distinct 3-flats under the line group (order 11520), and the minrank test
minrank(pattern on O) <= c - 2 with O = lines outside H1 u H2 (c = 16 -> test 14).

Reduction (argued): a total j is 'cheap' (beta_j < 4) iff R_j or A_j lies in a 3-flat H_j.  For any m cheap totals,
on O = complement of H_1 u ... u H_m those m columns of W (or U) vanish, so B[O,O] = W[O] U[O]^T has rank <= c - m.
Output: pairs.pkl {'pair_reps': [(H1, H2, orbit_size, minrank_le_14: bool)]}."""
import sys, time, pickle
sys.path.insert(0, sys.path[0])
from multiprocessing import Pool
from lines import views
from sub_minrank import run

S = views()['Gauss']


def load():
    G = pickle.load(open('orbits.pkl', 'rb'))['G']
    F = pickle.load(open('flats_Gauss.pkl', 'rb'))
    hyp = sorted(tuple(sorted(f)) for f, d in F.items() if d == 3)
    assert len(hyp) == 1500
    return G, hyp


def act(g, h):
    return tuple(sorted(g[i] for i in h))


def pair_orbits(G, hyp):
    """canonical orbit reps of unordered pairs {H1,H2}, by brute force: canonical form = min over G of sorted image pair."""
    hid = {h: k for k, h in enumerate(hyp)}
    # permutation of flats induced by each group element
    P = [[hid[act(g, h)] for h in hyp] for g in G]
    seen = set(); reps = []
    n = len(hyp)
    for a in range(n):
        for b in range(a + 1, n):
            if (a, b) in seen: continue
            orb = set()
            for p in P:
                x, y = p[a], p[b]
                orb.add((x, y) if x < y else (y, x))
            seen |= orb
            reps.append((a, b, len(orb)))
    assert sum(r[2] for r in reps) == n * (n - 1) // 2
    return reps, P


def job(args):
    H, c, solver = args
    Hs = set(H)
    O = [T for T in range(60) if T not in Hs]
    r, t, k = run(S, O, c, solver)
    return H, c, solver, r, t, len(O)


if __name__ == '__main__':
    G, hyp = load()
    t = time.time()
    reps, P = pair_orbits(G, hyp)
    print('pair orbits', len(reps), 'time %.0fs' % (time.time() - t), flush=True)
    pickle.dump({'reps': reps}, open('pair_orbits.pkl', 'wb'))
