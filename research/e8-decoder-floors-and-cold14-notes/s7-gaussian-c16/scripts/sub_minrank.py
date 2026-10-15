"""F2 minrank test of the Gaussian-E8 decoder pattern induced on a line subset O (asymmetric B = W U^T, clique gauge)."""
import sys, time, pickle
sys.path.insert(0, sys.path[0])
from lines import views
from pysat.formula import IDPool
from pysat.solvers import Solver
import networkx as nx

def encode(S, O, c, gauge=True):
    O = list(O); pool = IDPool(); cl = []
    U = {T: [pool.id(('u', T, j)) for j in range(c)] for T in O}
    W = {T: [pool.id(('w', T, j)) for j in range(c)] for T in O}
    def AND(a, b):
        z = pool.id(('and', a, b)); cl.extend([[-z, a], [-z, b], [z, -a, -b]]); return z
    def XOR(a, b):
        z = pool.id(('xor', a, b)); cl.extend([[-z, a, b], [-z, -a, -b], [z, -a, b], [z, a, -b]]); return z
    def xorlist(ls):
        acc = ls[0]
        for l in ls[1:]: acc = XOR(acc, l)
        return acc
    for T in O:
        for S_ in O:
            if T == S_ or S.NO[T, S_]:
                b = xorlist([AND(W[T][j], U[S_][j]) for j in range(c)])
                cl.append([b] if T == S_ else [-b])
    K = []
    if gauge:
        g = nx.Graph([(i, j) for i in O for j in O if i < j and S.NO[i, j]]); g.add_nodes_from(O)  # S7: isolated lines too
        K = sorted(max(nx.find_cliques(g), key=len))[:c]
        for i, T in enumerate(K):
            for j in range(c):
                cl.append([U[T][j]] if j == i else [-U[T][j]]); cl.append([W[T][j]] if j == i else [-W[T][j]])
    return cl, pool, len(K)

def run(S, O, c, solver='cadical153'):
    cl, pool, k = encode(S, O, c)
    t = time.time()
    with Solver(name=solver, bootstrap_with=cl) as s: r = s.solve()
    return r, time.time() - t, k

if __name__ == '__main__':
    S = views()['Gauss']
    F = pickle.load(open('flats_Gauss.pkl', 'rb'))
    hyp = [sorted(f) for f, d in F.items() if d == 3]
    c = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    print('full 60, c', c, run(S, range(60), c), flush=True)
    for size in (15, 6, 4):
        H = next(h for h in hyp if len(h) == size)
        O = [T for T in range(60) if T not in H]
        print('|H|', size, '|O|', len(O), 'c', c, run(S, O, c), flush=True)
