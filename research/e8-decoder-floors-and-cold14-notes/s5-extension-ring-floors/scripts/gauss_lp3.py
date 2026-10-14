import sys, itertools; sys.path.insert(0, sys.path[0])
from lines import *
import networkx as nx
from scipy.optimize import linprog
d = np.load('rankmat.npz'); R = d['R'].astype(float); L = d['lines_of'].astype(np.float32)
S = views()['Gauss']; v = S.v
g = nx.Graph([(i, j) for i in range(v) for j in range(i+1, v) if S.NO[i, j]])
fams = {}
for c in nx.find_cliques(g): fams.setdefault('max%d' % len(c), []).append(c)
fams['single'] = [[T] for T in range(v)]
fams['nopair'] = [[a, b] for a in range(v) for b in range(a+1, v) if S.NO[a, b]]
fams['all'] = [list(range(v))]
mval = {k: (15 if k == 'all' else len(fams[k][0])) for k in fams}
names = sorted(fams); H = []
for k in names:
    inc = np.zeros((v, len(fams[k])), np.float32)
    for j, c in enumerate(fams[k]): inc[c, j] = 1
    meet = (L @ inc > 0).astype(np.float32); H.append(meet @ meet.T)
H = np.stack(H, -1).reshape(-1, len(names)); Rf = R.reshape(-1)
rows = np.unique(np.concatenate([H, Rf[:, None]], 1), axis=0); rows = rows[rows[:, :-1].sum(1) > 0]
c = -np.array([mval[k] * len(fams[k]) for k in names], float)
res = linprog(c, A_ub=rows[:, :-1], b_ub=rows[:, -1], bounds=[(0, None)]*len(names), method='highs')
print('LP bound', -res.fun, {k: round(x*len(fams[k]), 4) for k, x in zip(names, res.x) if x > 1e-12})
