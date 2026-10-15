"""S7 step 3: full decoder SAT on all 60 lines with c totals, where for each flat Z_i of a configuration (i = 0..k-1),
total i has a whole side inside Z_i:  sigma_i -> W[T,i] = 0 for T outside Z_i;  not sigma_i -> U[T,i] = 0 for T outside Z_i.
Totals k..c-1 are free.  sigma_0 = 1 by the global transpose symmetry (W,U) -> (U,W) (the pattern is symmetric).
No GL gauge (columns are distinguished).  Free columns: lexicographic order is NOT imposed (keeps the encoding simple).
argv: c pkl level nproc [solver] [limit]: runs every orbit rep of good[level] in pkl."""
import sys, time, pickle
sys.path.insert(0, sys.path[0])
from multiprocessing import Pool
from pysat.formula import IDPool
from pysat.solvers import Solver
from lines import views

S = views()['Gauss']


def encode(Zs, c):
    pool = IDPool(); cl = []
    W = [[pool.id(('w', T, j)) for j in range(c)] for T in range(60)]
    U = [[pool.id(('u', T, j)) for j in range(c)] for T in range(60)]
    sig = [pool.id(('s', i)) for i in range(len(Zs))]
    def AND(a, b):
        z = pool.id(('and', a, b)); cl.extend([[-z, a], [-z, b], [z, -a, -b]]); return z
    def XOR(a, b):
        z = pool.id(('xor', a, b)); cl.extend([[-z, a, b], [-z, -a, -b], [z, -a, b], [z, a, -b]]); return z
    for T in range(60):
        for S_ in range(60):
            if T == S_ or S.NO[T, S_]:
                acc = AND(W[T][0], U[S_][0])
                for j in range(1, c): acc = XOR(acc, AND(W[T][j], U[S_][j]))
                cl.append([acc] if T == S_ else [-acc])
    for i, Z in enumerate(Zs):
        Zs_ = set(Z)
        for T in range(60):
            if T not in Zs_:
                cl.append([-sig[i], -W[T][i]]); cl.append([sig[i], -U[T][i]])
    if Zs: cl.append([sig[0]])
    return cl, pool


def job(args):
    X, Zs, c, solver = args
    cl, pool = encode(Zs, c)
    t = time.time()
    with Solver(name=solver, bootstrap_with=cl) as s:
        r = s.solve()
    return X, r, time.time() - t


if __name__ == '__main__':
    c = int(sys.argv[1]); d = pickle.load(open(sys.argv[2], 'rb')); lev = int(sys.argv[3]); npr = int(sys.argv[4])
    solver = sys.argv[5] if len(sys.argv) > 5 else 'cadical153'
    lim = int(sys.argv[6]) if len(sys.argv) > 6 else None
    fl = d['flats']; reps = sorted(d['good'][lev])[:lim]
    jobs = [(X, [fl[f][1] for f in X], c, solver) for X in reps]
    nsat = 0; t0 = time.time()
    with Pool(npr) as p:
        for k, (X, r, t) in enumerate(p.imap_unordered(job, jobs)):
            nsat += bool(r)
            print('%s sizes %s %s %.1fs [%d/%d] (%.0fs)' % (X, [len(fl[f][1]) for f in X], 'SAT' if r else 'UNSAT', t, k + 1, len(jobs), time.time() - t0), flush=True)
    print('level %d c=%d %s: %d SAT of %d' % (lev, c, solver, nsat, len(jobs)), flush=True)
