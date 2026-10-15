"""S7 step 2 (fast, general): level search over sets Z = {Z_1..Z_m} of distinct flats (dims chosen by argv), up to the
line group (order 11520), such that EVERY subset J of Z satisfies

        minrank(decoder pattern on O_J) <= c - |J|,     O_J = lines outside U_{i in J} Z_i.

Why: if a decoder B = W U^T has c totals and Z_i contains a whole side (R_j or A_j) of total j_i (distinct totals), then
those |J| columns of W (or U) vanish on O_J, so B[O_J, O_J] has rank <= c - |J| (and obeys the pattern on O_J).
minrank is monotone under taking sub-line-sets, and Z = 3-flats is a relaxation of any proper flat.

argv: c dims(e.g. '3' or '2' or '23') maxlevel nproc [tag]
Writes lev_<tag>.pkl = {m: set of canonical sets (tuples of flat ids into the 'flats' list)} and prints counts."""
import sys, time, pickle, itertools
sys.path.insert(0, sys.path[0])
import numpy as np
from multiprocessing import Pool
from lines import views
from sub_minrank import run

S = views()['Gauss']
B = 12  # bits per flat id (< 4096)


def load_flats(dims):
    G = pickle.load(open('orbits.pkl', 'rb'))['G']
    F = pickle.load(open('flats_Gauss.pkl', 'rb'))
    fl = sorted((d, tuple(sorted(f))) for f, d in F.items() if str(d) in dims)
    fid = {f: k for k, (d, f) in enumerate(fl)}
    P = np.array([[fid[tuple(sorted(g[i] for i in f))] for d, f in fl] for g in G], dtype=np.int64)
    return G, fl, P


def keys(A):
    """A: (..., |G|, m) sorted ids -> lexicographic key pair (k1, k2), 5 ids per key."""
    m = A.shape[-1]
    k1 = np.zeros(A.shape[:-1], np.int64); k2 = np.zeros(A.shape[:-1], np.int64)
    for i in range(m):
        if i < 5: k1 = (k1 << B) | A[..., i]
        else: k2 = (k2 << B) | A[..., i]
    return k1, k2


def canon_many(P, R, fs):
    """canonical forms of R u {f} for each f in fs (vectorised).  Canonical = lexicographically least sorted image."""
    out = []
    PR = P[:, list(R)]  # |G| x m
    for s in range(0, len(fs), 64):
        ch = fs[s:s + 64]
        A = np.concatenate([np.broadcast_to(PR, (len(ch),) + PR.shape), P[:, ch].T[:, :, None]], axis=2)
        A = np.sort(A, axis=2)
        k1, k2 = keys(A)
        m1 = k1.min(1, keepdims=True)
        k2m = np.where(k1 == m1, k2, np.iinfo(np.int64).max)
        g = k2m.argmin(1)
        for t in range(len(ch)):
            out.append(tuple(int(x) for x in A[t, g[t]]))
    return out


def canon(P, X):
    X = list(X)
    return canon_many(P, X[:-1], [X[-1]])[0]


def sat_job(args):
    key, O, cc = args
    if len(O) == 0: return key, True, 0.0
    if cc <= 0: return key, False, 0.0  # nonempty O has rank >= 1
    r, t, _ = run(S, O, cc, 'cadical153')
    return key, r, t


def main():
    c = int(sys.argv[1]); dims = sys.argv[2]; maxlev = int(sys.argv[3]); npr = int(sys.argv[4])
    tag = sys.argv[5] if len(sys.argv) > 5 else 'c%d_d%s' % (c, dims)
    G, fl, P = load_flats(dims)
    NF = len(fl); assert NF < (1 << B)
    lines_of = [set(f) for d, f in fl]
    compl = lambda X: [T for T in range(60) if T not in set().union(*(lines_of[f] for f in X))]
    t0 = time.time()
    good = {0: {()}}
    with Pool(npr) as pool:
        for m in range(1, maxlev + 1):
            cand = set()
            for R in good[m - 1]:
                fs = [f for f in range(NF) if f not in R]
                cand.update(canon_many(P, R, fs) if R else [canon(P, [f]) for f in fs])
            cand2 = [X for X in cand
                     if m == 1 or all(canon(P, Y) in good[m - 1] for Y in itertools.combinations(X, m - 1))]
            jobs = [(X, compl(X), c - m) for X in cand2]
            print('level %d: candidates %d, subset-closed %d; testing minrank <= %d   (%.0fs)' % (
                m, len(cand), len(jobs), c - m, time.time() - t0), flush=True)
            good[m] = set(); n = 0
            for X, r, t in pool.imap_unordered(sat_job, jobs, chunksize=1):
                n += 1
                if r: good[m].add(X)
                if n % 100 == 0: print('  %d/%d good %d (%.0fs)' % (n, len(jobs), len(good[m]), time.time() - t0), flush=True)
            pickle.dump({'good': good, 'flats': fl}, open('lev_%s.pkl' % tag, 'wb'))
            hist = {}
            for X in good[m]:
                key = (tuple(sorted(len(fl[f][1]) for f in X)), len(compl(X)))
                hist[key] = hist.get(key, 0) + 1
            print('LEVEL %d: %d good orbit reps (%.0fs)' % (m, len(good[m]), time.time() - t0), flush=True)
            if len(hist) < 40: print('   (flat sizes, |O|) histogram:', sorted(hist.items()), flush=True)
            if not good[m]:
                print('EMPTY at level %d => at most %d such flats/totals for c=%d, dims %s' % (m, m - 1, c, dims), flush=True)
                break


if __name__ == '__main__':
    main()
