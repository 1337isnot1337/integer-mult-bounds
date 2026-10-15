"""S8 counting lemma.  Input: hits_table.pkl (from hits_table.py = S5 gauss_bound40.py + dump): for all 2271^2 flat pairs
(X, Y): exact clique hits h(X,Y) (number of the 640 twelve-cliques meeting both X and Y) and a certified LOWER bound
R(X,Y) on the Theorem-C pairing rank.

Checks:  h <= 192 R  (S5)   and   h <= 128 R + 128  (new)   on every pair.
Since a total j with spans X_j, Y_j has hit_j <= h(X_j, Y_j) and beta_j >= R(X_j, Y_j), and every clique is hit >= 12
times, 7680 <= sum_j hit_j <= sum_j min(192 beta_j, 128 beta_j + 128)  =>  cost >= 40 and cost >= 60 - c.
Also prints the tight pairs (h = 128 R + 128) and the deficit facts used for c = 18."""
import pickle, numpy as np
from collections import Counter
d = pickle.load(open('hits_table.pkl', 'rb')); fl = d['fl']; R = d['R']; H = d['hits']
assert len(fl) == 2271 and len(d['C']) == 640
assert (H <= 192 * R).all()
print('PASS facet1: hits <= 192*rank on all %d flat pairs' % H.size)
assert (H <= 128 * R + 128).all()
print('PASS facet2: hits <= 128*rank + 128 on all %d flat pairs' % H.size)
print('max hits by certified rank:', {int(r): int(H[R == r].max()) for r in range(5)})
desc = lambda i: 'dim%d/%dlines' % (fl[i][1], len(fl[i][0]))
tight = np.argwhere(H == 128 * R + 128)
print('tight pairs (hits = 128 rank + 128):', sorted(Counter((desc(a), desc(b), int(R[a, b])) for a, b in tight).items()))
for c in range(15, 20):
    lb = max(40, -(-(7680 - 128 * c) // 128))
    print('c = %d: cost >= %d%s' % (c, lb, '  (> 42: excluded)' if lb > 42 else ''))
