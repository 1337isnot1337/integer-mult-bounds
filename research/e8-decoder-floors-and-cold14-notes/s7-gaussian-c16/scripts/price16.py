"""Calibration: a SAT-found 16-total decoder (S6 clique-gauge encoding, no cost cap) is valid and costs >= 43 (here: its exact
Theorem-C cost, with the number of cheap totals)."""
import sys; sys.path.insert(0, sys.path[0])
import numpy as np
from lines import views
from sub_minrank import encode
from pysat.solvers import Solver
S = views()['Gauss']; c = 16
cl, pool, _ = encode(S, range(60), c)
with Solver(name='cadical153', bootstrap_with=cl) as s:
    assert s.solve(); m = set(l for l in s.get_model() if l > 0)
W = np.array([[pool.id(('w', T, j)) in m for j in range(c)] for T in range(60)], int)
U = np.array([[pool.id(('u', T, j)) in m for j in range(c)] for T in range(60)], int)
B = W @ U.T % 2
assert all(B[T, T] == 1 for T in range(60)) and not (B[S.NO] != 0).any(), 'invalid decoder'
beta = [S.pair_rank([T for T in range(60) if W[T, j]], [T for T in range(60) if U[T, j]]) for j in range(c)]
print('c=16 decoder valid; betas', beta, 'sum', sum(beta), 'cheap totals', sum(b < 4 for b in beta))
assert sum(beta) >= 43
