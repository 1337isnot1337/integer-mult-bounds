"""Gaussian E8 (60 lines, w = 4): every decoder with exactly c = minrank = 15 totals costs exactly 60 (Theorem C).

B = W U^T with W, U in F2^{60x15}; rank B >= 15 (minrank, S1: c = 14 UNSAT) so W, U have full column rank and every
total j has w_j = W e_j != 0, u_j != 0.  If every nonzero vector of col(W) and of col(U) has a support spanning K^4,
then every total pairs span(R_j) = span(A_j) = K^4 with rank 4 (positive definite), so sum_j beta_j = 15 * 4 = 60.
SAT question (asymmetric decoders, clique gauge): exists a valid 15-total decoder and x != 0 with supp(W x) inside a
3-dim flat?  (Every proper flat lies in one of the 1500 3-flats.)  The U side follows by transposition (B^T is valid
for the transposed decoder, the pattern being symmetric).  argv: [optional 'calib'] -> drop the flat constraint."""
import sys, time, pickle, itertools; sys.path.insert(0, sys.path[0])
from lines import *
from flats import flats
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
import networkx as nx

def main(calib=False, c=15):
    S = views()['Gauss']; v = S.v
    F = flats(S)
    hyp = [sorted(f) for f, d in F.items() if d == 3]
    assert len(hyp) == 1500
    g = nx.Graph([(i, j) for i in range(v) for j in range(i + 1, v) if S.NO[i, j]])
    K = sorted(max(nx.find_cliques(g), key=len)); assert len(K) == 12
    pool = IDPool(); cl = []
    U = [[pool.id(('u', T, j)) for j in range(c)] for T in range(v)]
    W = [[pool.id(('w', T, j)) for j in range(c)] for T in range(v)]
    def AND(a, b):
        z = pool.id(('and', a, b)); cl.extend([[-z, a], [-z, b], [z, -a, -b]]); return z
    def XOR(a, b):
        z = pool.id(('xor', a, b)); cl.extend([[-z, a, b], [-z, -a, -b], [z, -a, b], [z, a, -b]]); return z
    def xorlist(ls):
        acc = ls[0]
        for l in ls[1:]: acc = XOR(acc, l)
        return acc
    for T in range(v):
        for S_ in range(v):
            if T == S_ or S.NO[T, S_]:
                b = xorlist([AND(W[T][j], U[S_][j]) for j in range(c)])
                cl.append([b] if T == S_ else [-b])
    for i, T in enumerate(K):
        for j in range(c):
            cl.append([U[T][j]] if j == i else [-U[T][j]]); cl.append([W[T][j]] if j == i else [-W[T][j]])
    if not calib:
        x = [pool.id(('x', j)) for j in range(c)]; cl.append(x)
        y = [xorlist([AND(W[T][j], x[j]) for j in range(c)]) for T in range(v)]
        sel = [pool.id(('s', h)) for h in range(len(hyp))]; cl.append(sel)
        for h, H in enumerate(hyp):
            Hs = set(H)
            for T in range(v):
                if T not in Hs: cl.append([-sel[h], -y[T]])
    s = Cadical153(bootstrap_with=cl); t = time.time(); r = s.solve()
    print(('calibration (no flat constraint) ' if calib else 'support-in-a-3-flat ') + ('SAT' if r else 'UNSAT'), round(time.time() - t, 1), 's', flush=True)
    return r

if __name__ == '__main__':
    main(calib=len(sys.argv) > 1 and sys.argv[1] == 'calib')
