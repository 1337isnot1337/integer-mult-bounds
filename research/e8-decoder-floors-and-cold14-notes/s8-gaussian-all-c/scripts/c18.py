"""S8: no 18-total Gaussian-E8 decoder costs <= 42.  Input hits_table.pkl (see facets.py).

Argument.  e_j := 128 beta_j + 128 - hit_j >= 0 for every total (facet2), and
   sum_j e_j + E = 128 cost + 128 c - 7680,   E = sum_C (N_C - 12) >= 0   (N_C = #totals hitting clique C on both sides).
At c = 18 and cost <= 42 the right side is <= 0, so cost = 42, E = 0 (every clique hit EXACTLY 12 times) and every total
is tight: hit(R_j,A_j) = 128 beta_j + 128.  Since hit(R,A) <= hit(X,Y) <= 128 R(X,Y) + 128 <= 128 beta + 128 for the spans
(X,Y), the span pair is a tight flat pair and the cliques hit by total j are exactly those hit by (X_j,Y_j).
Checked below: for every tight flat pair t the set of cliques NOT hit is {C : C meets x_t} for a set x_t of pairwise
orthogonal lines (so that 1 - h_t = M x_t, M = 640 x 60 clique/line incidence).  Then
   12 * 1 = N = sum_j h_j = 18 * 1 - M mu,   mu = sum_j x_{t(j)} in Z_{>=0}^60,   i.e.  M mu = 6 * 1.
M has rank 60 (checked, exact) and M (1/2 * 1) = 6 * 1 (every clique has 12 lines), so mu = 1/2 * 1: not integral.
Contradiction.
Same argument on the tight face for any c (cost = 60 - c, needs c <= 20 since cost >= 40): M mu = (c-12) 1, mu = (c-12)/12;
for c = 19 (cost 41) and c = 20 (cost 40) this is non-integral, so c = 19 needs cost >= 42 and c = 20 cost >= 41."""
import pickle, numpy as np, sympy
from lines import views
S = views()['Gauss']; NO = S.NO
d = pickle.load(open('hits_table.pkl', 'rb')); fl = d['fl']; R = d['R']; H = d['hits']; C = d['C']
M = np.zeros((640, 60), np.int64)
for k, c in enumerate(C): M[k, c] = 1
assert (M.sum(1) == 12).all()
assert sympy.Matrix(M).rank() == 60
print('PASS clique/line incidence M (640 x 60) has exact rank 60; M(1/2) = 6')
L = [set(f) for f, dd in fl]
tight = np.argwhere(H == 128 * R + 128)
from collections import Counter
kinds = Counter()
for a, b in tight:
    X, Y = L[a], L[b]
    h = np.array([bool(X & set(c)) and bool(Y & set(c)) for c in C])
    x = sorted(T for T in range(60) if all(not h[k] for k, c in enumerate(C) if T in c))   # lines all of whose cliques are missed
    assert all(not NO[s, t] for s in x for t in x if s != t)            # pairwise orthogonal => cliques meet x at most once
    assert ((M[:, x].sum(1) if x else np.zeros(640, int)) == (~h).astype(int)).all()   # 1 - h = M x exactly
    kinds[(len(L[a]), len(L[b]), int(R[a, b]), len(x))] += 1
print('PASS every tight flat pair t has 1 - h_t = M x_t with x_t pairwise-orthogonal lines:', sorted(kinds.items()))
print('RESULT c18: M mu = 6*1 has the unique rational solution mu = 1/2 (non-integral) => no 18-total decoder costs <= 42')
# Tight face in general: cost = 60 - c forces the same structure with M mu = (c - 12) * 1, mu = (c - 12)/12 * 1.
for c in (19, 20):
    from fractions import Fraction as Fr
    mu = Fr(c - 12, 12)
    print('RESULT tight c=%d: cost = %d would need mu = %s (non-integral) => cost >= %d' % (c, 60 - c, mu, 61 - c if 61 - c > 40 else 41))
