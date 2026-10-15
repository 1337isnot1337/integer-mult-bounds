"""S7 step 2b: level search over sets of distinct 3-flats {H_1..H_m} (up to the line group, order 11520) such that EVERY
subset J satisfies minrank(pattern on lines outside U_{i in J} H_i) <= c - |J|   (c = number of totals, default 16).

A decoder with c totals and k cheap totals (beta_j < 4) gives such a set of size k (one 3-flat containing a deficient side
of each cheap total; S6 single-flat lemma => distinct).  Level m+1 candidates: extend each level-m rep by a flat that is
pair-compatible with all members; keep if all m-subsets are level-m sets; then SAT-test the full union at c-(m+1).
argv: c maxlevel nproc.  Writes levels_c{c}.pkl and prints per-level counts."""
import sys, time, pickle, itertools
sys.path.insert(0, sys.path[0])
import numpy as np
from multiprocessing import Pool
from lines import views
from sub_minrank import run
from pairs import load

S = views()['Gauss']


def sat_job(args):
    key, O, cc = args
    if cc < 0:
        return key, False, 0.0
    if len(O) == 0:
        return key, True, 0.0
    if cc == 0:
        return key, False, 0.0   # nonempty O needs rank >= 1 (B_TT = 1)
    r, t, _ = run(S, O, cc, 'cadical153')
    return key, r, t


if __name__ == '__main__':
    c = int(sys.argv[1]); maxlev = int(sys.argv[2]); npr = int(sys.argv[3])
    G, hyp = load()
    hid = {h: k for k, h in enumerate(hyp)}
    P = np.array([[hid[tuple(sorted(g[i] for i in h))] for h in hyp] for g in G], dtype=np.int32)  # |G| x 1500
    NF = len(hyp)
    lines_of = [set(h) for h in hyp]

    def canon(fs):
        A = np.sort(P[:, list(fs)], axis=1)
        k = np.lexsort(A.T[::-1])[0]
        return tuple(int(x) for x in A[k])

    def compl(fs):
        U = set().union(*(lines_of[f] for f in fs))
        return [T for T in range(60) if T not in U]

    # level 1: the 3 orbit reps, minrank 15 on complement (S6) -> valid iff 15 <= c-1
    reps1 = sorted({canon([f]) for f in range(NF)})
    good = {1: set(reps1) if 15 <= c - 1 else set()}
    print('level 1 reps', len(good[1]), flush=True)
    # level 2: from pairs.py orbit results (c=14 test) only valid for c=16; recompute generically via SAT
    union_cache = {}
    t0 = time.time()
    with Pool(npr) as pool:
        for m in range(2, maxlev + 1):
            cand = set()
            for R in good[m - 1]:
                for f in range(NF):
                    if f in R: continue
                    cand.add(canon(list(R) + [f]))
            # subset closure
            cand2 = []
            for X in cand:
                if all(canon(list(Y)) in good[m - 1] for Y in itertools.combinations(X, m - 1)):
                    cand2.append(X)
            jobs = []
            for X in cand2:
                O = compl(X)
                jobs.append((X, O, c - m))
            print('level %d: candidates %d, after subset closure %d; SAT tests at rank <= %d' % (m, len(cand), len(jobs), c - m), flush=True)
            good[m] = set(); n = 0
            for X, r, t in pool.imap_unordered(sat_job, jobs, chunksize=1):
                n += 1
                if r: good[m].add(X)
                if n % 50 == 0 or n == len(jobs):
                    print('  level %d progress %d/%d  good %d  (%.0fs)' % (m, n, len(jobs), len(good[m]), time.time() - t0), flush=True)
            pickle.dump(good, open('levels_c%d.pkl' % c, 'wb'))
            sizes = {}
            for X in good[m]:
                k = len(compl(X)); sizes[k] = sizes.get(k, 0) + 1
            print('LEVEL %d: %d good orbit reps; |O| histogram %s' % (m, len(good[m]), sorted(sizes.items())), flush=True)
            if not good[m]:
                print('EMPTY at level %d => at most %d cheap totals for c=%d' % (m, m - 1, c), flush=True)
                break
