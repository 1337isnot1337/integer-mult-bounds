"""Continuation of levels2.py (same definitions) with two exact speedups:
 (1) extension flats f must be pair-compatible with every member (pair {Z_i, f} is a 2-subset, so it must be a level-2 set);
 (2) canonicalisation and subset-closure checks run in the worker pool.
argv: c dims infile startlevel maxlevel nproc tag.   Loads good[] from infile (written by levels2.py) and continues."""
import sys, time, pickle, itertools
sys.path.insert(0, sys.path[0])
import numpy as np
from multiprocessing import Pool
from levels2 import load_flats, canon_many, canon, sat_job

c = int(sys.argv[1]); dims = sys.argv[2]
G, fl, P = load_flats(dims)
NF = len(fl)
lines_of = [set(f) for d, f in fl]
good = pickle.load(open(sys.argv[3], 'rb'))['good']
# pair compatibility matrix from level-2 orbit reps
comp = np.zeros((NF, NF), bool)
for (a, b) in good[2]:
    comp[P[:, a], P[:, b]] = True; comp[P[:, b], P[:, a]] = True


def compl(X):
    U = set().union(*(lines_of[f] for f in X))
    return [T for T in range(60) if T not in U]


def gen(R):
    """canonical (m+1)-sets extending rep R that pass the full (m)-subset closure test, given global PREV."""
    fs = [f for f in range(NF) if f not in R and comp[f, list(R)].all()]
    out = []
    for X in set(canon_many(P, R, fs)) if fs else []:
        if all(canon(P, Y) in PREV for Y in itertools.combinations(X, len(X) - 1)):
            out.append(X)
    return out


def init(prev):
    global PREV
    PREV = prev


if __name__ == '__main__':
    start = int(sys.argv[4]); maxlev = int(sys.argv[5]); npr = int(sys.argv[6]); tag = sys.argv[7]
    t0 = time.time()
    for m in range(start, maxlev + 1):
        with Pool(npr, initializer=init, initargs=(good[m - 1],)) as pool:
            cand = set()
            for out in pool.imap_unordered(gen, sorted(good[m - 1]), chunksize=4):
                cand.update(out)
            jobs = [(X, compl(X), c - m) for X in sorted(cand)]
            print('level %d: subset-closed candidates %d; testing minrank <= %d   (%.0fs)' % (m, len(jobs), c - m, time.time() - t0), flush=True)
            good[m] = set()
            for X, r, t in pool.imap_unordered(sat_job, jobs, chunksize=1):
                if r: good[m].add(X)
        pickle.dump({'good': good, 'flats': fl}, open('lev_%s.pkl' % tag, 'wb'))
        hist = {}
        for X in good[m]:
            k = len(compl(X)); hist[k] = hist.get(k, 0) + 1
        print('LEVEL %d: %d good orbit reps (%.0fs); |O| hist %s' % (m, len(good[m]), time.time() - t0, sorted(hist.items())), flush=True)
        if not good[m]:
            print('EMPTY at level %d => at most %d such flats/totals for c=%d, dims %s' % (m, m - 1, c, dims), flush=True)
            break
