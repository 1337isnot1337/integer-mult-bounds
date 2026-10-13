"""Matroid-partition certificate for the centre decoder of I_{n,1} under every puncture.

Claim: for every live set L of lines,  sum_i rank(R(e_i) & L) >= |L| / 2.
Certificate: a partition of all v lines into 2n sets I_{i,1}, I_{i,2}, each linearly independent and contained in
R(e_i) (the readers of centre i).  Then 2 rank(R(e_i) & L) >= |L & I_{i,1}| + |L & I_{i,2}| and summing gives the
claim.  For n = 11, 13: v = 2 n (n - 1) / 2 ... (220 = 22 x 10, 364 = 26 x 14 ... see output).
Found by Edmonds/Knuth matroid partitioning (shortest augmenting paths, float rank oracle); the final partition is
verified with exact rational ranks.  Usage: python partition.py n copies mult [--json out]
(copies of each line = mult, slots per centre = copies: proves sum_i rank >= (mult/copies)|L|)"""
import sys, json, random
from collections import deque
import numpy as np
sys.dont_write_bytecode = True
import units as U


def run(n, copies=2, seed=0, mult=1):
    L0, G, lab0 = U.lorentz_family(n)
    L = np.repeat(L0, mult, axis=0); lab = np.repeat(lab0, mult, axis=0)   # each line mult times
    v = len(L)
    Lf = L.astype(float)
    allowed = [[i for i in range(n) if lab[t, i]] for t in range(v)]       # t in R(e_i)  <=>  label_t[i] = 1
    slots = [(i, c) for i in range(n) for c in range(copies)]
    S = [set() for _ in slots]
    where = {}
    indep = lambda ss: len(ss) == 0 or np.linalg.matrix_rank(Lf[sorted(ss)]) == len(ss)
    rng = random.Random(seed)
    order = list(range(v)); rng.shuffle(order)
    for x in order:
        # BFS: nodes are elements; edge y -> slot s: y can enter s (allowed) and S_s + y indep  => done
        # else y -> z for z in S_s with S_s - z + y independent (z then must move)
        prev = {x: None}
        q = deque([x]); found = None
        while q and found is None:
            y = q.popleft()
            for si, (i, c) in enumerate(slots):
                if i not in allowed[y] or where.get(y) == si:
                    continue
                if indep(S[si] | {y}):
                    found = (y, si); break
                for z in S[si]:
                    if z not in prev and indep((S[si] - {z}) | {y}):
                        prev[z] = (y, si); q.append(z)
        if found is None:
            return None, x
        y, si = found
        # augment along the path: y goes into si; then walk back
        while True:
            old = where.get(y)
            if old is not None:
                S[old].discard(y)
            S[si].add(y); where[y] = si
            if prev[y] is None:
                break
            y, si = prev[y][0], prev[y][1]
            # prev[z] = (y', si'): y' entered si' displacing z -- here z is the element we just moved; walk on
        # sanity
    return (S, slots, L, lab), None


def verify(S, slots, L, lab):
    for (i, c), ss in zip(slots, S):
        ss = sorted(ss)
        assert all(lab[t, i] for t in ss)
        assert U.rank_q(L[ss].tolist()) == len(ss), 'dependent slot'
    allv = sorted(t for ss in S for t in ss)
    assert allv == list(range(len(L))), 'not a partition'
    return True


if __name__ == '__main__':
    n = int(sys.argv[1]); copies = int(sys.argv[2]); mult = int(sys.argv[3])
    for seed in range(5):
        res, fail = run(n, copies, seed, mult)
        if res:
            S, slots, L, lab = res
            verify(S, slots, L, lab)
            print('n=%d: %d copies of each of the %d lines partitioned into %d independent slots (%d per centre) VERIFIED exactly'
                  ' => sum_i rank(R(e_i) & L) >= (%d/%d)|L| for every live set L; slot sizes %s' % (
                n, mult, len(L) // mult, len(slots), copies, mult, copies, sorted(set(len(s) for s in S))))
            if '--json' in sys.argv:
                json.dump(dict(n=n, copies=copies, slots=[dict(centre=i, copy=c, lines=sorted(int(t) for t in s))
                                                           for (i, c), s in zip(slots, S)]),
                          open(sys.argv[sys.argv.index('--json') + 1], 'w'))
            break
        print('seed %d: no augmenting path for element %d (a set violating |S| <= copies*rank exists)' % (seed, fail))
