"""Can a puncture of at most k lines bring the F2 minrank of the I_{n,1} pattern down to n - 1?
Variables: live selectors y_t, sink/source labels W, U (v x c over F2), B = W U^T.  Constraints: live t => B_tt = 1;
live s, t with G_st != 0 => B_ts = 0; at most k lines dead.  Gauge U_K = W_K = [I|0] on one fixed maximum clique K that
is forced live (WLOG while k is below the clique hitting number, see clique_hit.py, and S_n is transitive on maximum
cliques).  CaDiCaL 1.5.3 via python-sat, no proof log.
Usage: python punct_sat.py n c k [timeout_s [orbits.json orbit_index]]"""
import sys, time, itertools
import numpy as np
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
sys.dont_write_bytecode = True
import units as U


def build(n, c, k, K=None):
    L, G, lab = U.lorentz_family(n)
    v = len(L)
    if K is None:
        K = U.nonorth_clique(G)
    pool = IDPool(); cl = []
    nv = lambda: pool.id()
    y = [nv() for _ in range(v)]
    Uv = [[nv() for _ in range(c)] for _ in range(v)]
    Wv = [[nv() for _ in range(c)] for _ in range(v)]

    def AND(a, b):
        z = nv(); cl.extend([[-z, a], [-z, b], [z, -a, -b]]); return z

    def XOR(a, b):
        z = nv(); cl.extend([[-z, a, b], [-z, -a, -b], [z, -a, b], [z, a, -b]]); return z

    def B(T, S):
        lits = [AND(Wv[T][j], Uv[S][j]) for j in range(c)]
        z = lits[0]
        for l in lits[1:]:
            z = XOR(z, l)
        return z
    for T in range(v):
        cl.append([-y[T], B(T, T)])
    for T in range(v):
        for S in range(v):
            if S != T and G[T, S] != 0:
                cl.append([-y[T], -y[S], -B(T, S)])
    for i, T in enumerate(K):
        cl.append([y[T]])
        for j in range(c):
            cl.append([Uv[T][j]] if j == i else [-Uv[T][j]])
            cl.append([Wv[T][j]] if j == i else [-Wv[T][j]])
    card = CardEnc.atmost(lits=[-x for x in y], bound=k, vpool=pool, encoding=EncType.seqcounter)
    cl.extend(card.clauses)
    return cl, y, Uv, Wv, L, G, lab, K


if __name__ == '__main__':
    n, c, k = map(int, sys.argv[1:4])
    T = float(sys.argv[4]) if len(sys.argv) > 4 else 3600
    K = None
    if len(sys.argv) > 6:          # clique orbit json, orbit index
        import json
        K = json.load(open(sys.argv[5]))['orbits'][int(sys.argv[6])]['rep']
    cl, y, Uv, Wv, L, G, lab, K = build(n, c, k, K)
    print('n=%d c=%d k=%d clauses=%d clique=%s' % (n, c, k, len(cl), K), flush=True)
    s = Cadical153(bootstrap_with=cl)
    import threading
    tm = threading.Timer(T, lambda: s.interrupt()); tm.start()
    t0 = time.time()
    r = s.solve_limited(expect_interrupt=True)
    tm.cancel()
    res = {True: 'SAT', False: 'UNSAT', None: 'TIMEOUT'}[r]
    print('result', res, 'sec %.1f' % (time.time() - t0), flush=True)
    if r:
        m = set(x for x in s.get_model() if x > 0)
        dead = [t for t in range(len(L)) if y[t] not in m]
        print('dead', dead, flush=True)
