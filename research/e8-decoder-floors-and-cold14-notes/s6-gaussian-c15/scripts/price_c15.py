"""Sanity: a 15-total decoder found by SAT (calibration) has Theorem-C cost sum_j beta_j = 60, as the G2 theorem forces."""
import sys
sys.path.insert(0, sys.path[0])
import numpy as np
from lines import views
from sub_minrank import encode
from pysat.solvers import Solver

S = views()['Gauss']; c = 15
cl, pool, _ = encode(S, range(60), c)
with Solver(name='cadical153', bootstrap_with=cl) as s:
    assert s.solve(); m = set(l for l in s.get_model() if l > 0)
W = np.array([[pool.id(('w', T, j)) in m for j in range(c)] for T in range(60)], int)
U = np.array([[pool.id(('u', T, j)) in m for j in range(c)] for T in range(60)], int)
B = W @ U.T % 2
assert all(B[T, T] == 1 for T in range(60)) and not (B[S.NO] != 0).any(), 'invalid decoder'
beta = [S.pair_rank([T for T in range(60) if W[T, j]], [T for T in range(60) if U[T, j]]) for j in range(c)]
print('rank_F2 check: W,U columns', c, ' betas', beta, ' sum', sum(beta))
assert sum(beta) == 60
