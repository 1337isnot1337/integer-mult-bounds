"""Heuristic (model-free, exploratory) search for punctures of I_{n,1} that lower the star label-decoder ratio
x = C_star(P)/v (window kept) or raise X*(h, x).  Float ranks; every reported point is re-evaluated exactly by punct.py.
Usage: python anneal.py n seed steps [objective: x|X]"""
import sys, math, random, itertools
import numpy as np
sys.dont_write_bytecode = True
import units as U

n, seed, steps = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
obj = sys.argv[4] if len(sys.argv) > 4 else 'x'
rng = random.Random(seed)
L, G, lab = U.lorentz_family(n)
v = len(L)
Q = np.diag([1.0] * n + [-1.0])
Lf = L.astype(float)
F = [np.array([(p >> j) & 1 for j in range(n)]) for p in range(1, 1 << n)]
RM = np.array([(lab @ f) % 2 for f in F], dtype=bool)          # functional x line


def cost(live):
    lv = np.nonzero(live)[0]
    Ll = Lf[lv]
    h = np.linalg.matrix_rank(Ll @ Q @ Ll.T)
    rad = np.linalg.matrix_rank(Ll) - h
    items = []
    for i in range(len(F)):
        R = lv[RM[i, lv]]
        if len(R) == 0:
            continue
        sp = np.linalg.matrix_rank(Lf[R] @ Q @ Ll.T) if rad else np.linalg.matrix_rank(Lf[R])
        w = 0
        for t in R:
            w |= 1 << int(t)
        items.append((sp, w))
    items.sort(key=lambda t: t[0])
    basis, tot, seen = {}, 0, set()
    for sp, w in items:
        if w in seen:
            continue
        seen.add(w)
        x = w
        while x:
            hb = x.bit_length() - 1
            if hb in basis:
                x ^= basis[hb]
            else:
                basis[hb] = x; break
        if x:
            tot += sp
    return tot, h


def score(live):
    c, h = cost(live)
    x = c / live.sum()
    if obj == 'x':
        return x - 0.0 * h, (c, int(live.sum()), h)
    # proxy for X*: X ~ (2 - 3x)/... use D/Cost-like proxy at s = 3: (2 - 3x)/(h) as monotone stand-in
    return -(2 - 3 * x) / h, (c, int(live.sum()), h)


live = np.ones(v, dtype=bool)
cur, info = score(live)
best = (cur, info, live.copy())
T0 = 0.01
for it in range(steps):
    T = T0 * (1 - it / steps) + 1e-5
    nl = live.copy()
    for _ in range(rng.choice([1, 1, 1, 2, 3])):
        t = rng.randrange(v); nl[t] = not nl[t]
    if nl.sum() < v // 3:
        continue
    s, inf = score(nl)
    if s <= cur or rng.random() < math.exp(-(s - cur) / T):
        live, cur, info = nl, s, inf
        if s < best[0]:
            best = (s, inf, live.copy())
            print('it %d best %.5f (C=%d v=%d h=%d) dead=%s' % (it, s, inf[0], inf[1], inf[2],
                  list(np.nonzero(~live)[0]) if (~live).sum() < 40 else '%d lines' % (~live).sum()), flush=True)
print('final best', best[0], best[1], 'dead', list(np.nonzero(~best[2])[0]))
