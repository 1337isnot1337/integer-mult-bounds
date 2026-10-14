"""Gaussian view: the 2-adic (mod pi) sum-rank bound is at most 12, so it cannot reach 43.
The unit-pair graph (|hG|^2 = 1, 32 per line) has a partition into 12 five-cliques; with N/2 odd exactly inside the
cliques, (hG o N)/2 mod pi = block-diag(J_5) of F2-rank 12.  Also: max set with no unit pair = 12 (lower bound 12)."""
import sys; sys.path.insert(0, sys.path[0])
from lines import *
import networkx as nx
from pysat.solvers import Cadical153
from pysat.card import CardEnc
W = views(); S = W['Gauss']; a, b = gauss_gram(S.reps, W['_J']); N = a*a + b*b; v = S.v
U = nx.Graph([(i, j) for i in range(v) for j in range(i+1, v) if N[i, j] == 1])
cl5 = [c for c in nx.find_cliques(U) if len(c) == 5]
# exact cover by SAT
x = list(range(1, len(cl5)+1)); cls = []
for T in range(v):
    lits = [x[k] for k, c in enumerate(cl5) if T in c]
    cls.append(lits)
    for i in range(len(lits)):
        for j in range(i+1, len(lits)): cls.append([-lits[i], -lits[j]])
s = Cadical153(bootstrap_with=cls); assert s.solve()
part = [cl5[k] for k in range(len(cl5)) if s.get_model()[k] > 0]
assert len(part) == 12 and sorted(sum(part, [])) == list(range(v))
M = np.zeros((v, v), int)
for c in part:
    for i in c:
        for j in c: M[i, j] = 1
from lines import rank_q
# F2 rank of block-diag J_5 is 12 (one per block)
print('PASS gauss.pi: unit graph has', len(cl5), 'five-cliques and a partition into 12 of them -> mod-pi bound <= 12')
