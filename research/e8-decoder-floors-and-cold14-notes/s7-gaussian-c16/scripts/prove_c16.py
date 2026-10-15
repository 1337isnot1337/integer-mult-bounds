"""S7 theorem: every Gaussian-E8 decoder with exactly 16 totals has Theorem-C cost >= 43.

Inputs: lev_c16_d3_hi.pkl (3-flat level tables good[k], k = 1..16, from levels2.py / levels3.py; a level-k set is a set of
k distinct 3-flats every subset J of which has minrank(pattern on lines outside the union of J) <= 16 - |J|).

Argument (see README):
  k = #cheap totals (beta < 4).  Each cheap total has a side in a proper flat, hence in a 3-flat; one 3-flat per cheap
  total gives a level-k set (S6 lemma for distinctness), and any legal choice of 3-flats does.  Types:
    a: a side of dim <= 2 (inside a 2-flat Z): every 3-flat through Z is a legal choice;   beta >= 0
    p: (3,3) with beta = 2: both X_j != Y_j legal (dumbbell);                              beta = 2
    q: rest (beta >= 3).
  cost <= 42  <=>  3a + p >= 22 - k.
  (A) a = 0 whenever k >= 5: no level-k rep (k >= 5) has an 'a-capable' member.            [checked below]
  (B) for k >= 11 the maximum number p* of jointly doubled members is < 22 - k.            [checked below]
  Arithmetic: k <= 4: 3a + p <= 3k < 22 - k.  5 <= k <= 10: a = 0, p <= k < 22 - k.  k = 16: good[16] empty.
"""
import sys, time, pickle, itertools
sys.path.insert(0, sys.path[0])
import numpy as np
from levels2 import load_flats, canon, canon_many
from dumbbell import hyperplane_bases, beta_matrix

G, fl3, P = load_flats('3')
_, fl2, _ = load_flats('2')
NF = len(fl3)
good = pickle.load(open(sys.argv[1] if len(sys.argv) > 1 else 'lev_c16_d3_hi.pkl', 'rb'))['good']
set3 = [set(f) for d, f in fl3]; set2 = [set(f) for d, f in fl2]
through = [[h for h in range(NF) if set2[z] <= set3[h]] for z in range(len(fl2))]
inside = [[z for z in range(len(fl2)) if set2[z] <= set3[h]] for h in range(NF)]
cache = {}


def ok(X):
    X = tuple(sorted(X))
    if len(set(X)) < len(X): return False
    if X not in cache: cache[X] = canon(P, X) in good[len(X)]
    return cache[X]


def a_capable(T, i):
    return any(all(h == T[i] or (h not in T and ok(T[:i] + [h] + T[i + 1:])) for h in through[z]) for z in inside[T[i]])


def pstar(T, beta, cap):
    k = len(T)
    part = {i: [y for y in range(NF) if y not in T and beta[T[i], y] == 2 and ok(T[:i] + [y] + T[i + 1:])] for i in range(k)}
    mem = sorted(i for i in part if part[i]); best = [0]

    def valid(choice):
        items = list(choice.items())
        for mask in range(1 << len(items)):
            X = list(T)
            for b, (i, y) in enumerate(items):
                if mask >> b & 1: X[i] = y
            if not ok(X): return False
        return True

    def rec(pos, choice):
        best[0] = max(best[0], len(choice))
        if best[0] >= cap or len(choice) + len(mem) - pos <= best[0]: return
        for q in range(pos, len(mem)):
            i = mem[q]
            for y in part[i]:
                if y in choice.values(): continue
                choice[i] = y
                if valid(choice): rec(q + 1, choice)
                del choice[i]
    rec(0, {})
    return best[0]


if __name__ == '__main__':
    t0 = time.time()
    assert len(good[1]) == 3 and not good[16]
    print('level sizes:', {k: len(good[k]) for k in sorted(good) if k}, flush=True)
    for k in range(1, 16):
        n = sum(1 for T in good[k] if any(a_capable(list(T), i) for i in range(k)))
        print('(A) k=%2d: %4d of %4d reps have an a-capable member' % (k, n, len(good[k])), flush=True)
        if k >= 5: assert n == 0
    beta = beta_matrix(hyperplane_bases(fl3))
    for k in range(11, 16):
        ps = [pstar(list(T), beta, 22 - k) for T in sorted(good[k])]
        print('(B) k=%2d: max p* = %d (need >= %d for cost <= 42)' % (k, max(ps), 22 - k), flush=True)
        assert max(ps) < 22 - k
    for k in range(0, 17):
        if k <= 4: assert 3 * k < 22 - k
        elif k <= 10: assert k < 22 - k
    print('THEOREM: no Gaussian-E8 decoder with exactly 16 totals has sum beta_j <= 42  (%.0fs)' % (time.time() - t0), flush=True)
