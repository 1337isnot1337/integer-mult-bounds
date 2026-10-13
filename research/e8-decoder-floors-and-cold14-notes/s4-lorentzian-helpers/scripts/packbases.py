"""Disjoint spanning sets inside reader sets: a puncture-robustness certificate.
For a functional p (Hamming weight k, S_n orbit representative) we pack q pairwise disjoint bases of span R(p) inside
R(p) (matroid union by augmenting paths; every packed basis is re-verified with exact rational rank).
If R(p) holds q disjoint bases, deleting any P leaves rank(R(p) - P) >= rank R(p) - floor(|P| / q): some basis loses
at most floor(|P|/q) lines.  Usage: python packbases.py n"""
import sys
from collections import deque
import numpy as np
sys.dont_write_bytecode = True
import units as U


def pack(Lsub, q, seed=0):
    Lf = Lsub.astype(float)
    m = len(Lsub)
    S = [set() for _ in range(q)]
    where = {}
    ind = lambda ss: len(ss) == 0 or np.linalg.matrix_rank(Lf[sorted(ss)]) == len(ss)
    for x in range(m):
        prev = {x: None}; dq = deque([x]); found = None
        while dq and found is None:
            y = dq.popleft()
            for si in range(q):
                if where.get(y) == si:
                    continue
                if ind(S[si] | {y}):
                    found = (y, si); break
                for z in S[si]:
                    if z not in prev and ind((S[si] - {z}) | {y}):
                        prev[z] = (y, si); dq.append(z)
        if found is None:
            continue
        y, si = found
        while True:
            old = where.get(y)
            if old is not None:
                S[old].discard(y)
            S[si].add(y); where[y] = si
            if prev[y] is None:
                break
            y, si = prev[y]
    return S


if __name__ == '__main__':
    n = int(sys.argv[1])
    L, G, lab = U.lorentz_family(n)
    for k in range(1, n + 1):
        p = np.array([1] * k + [0] * (n - k))
        R = np.nonzero((lab @ p) % 2)[0]
        r0 = U.rank_q(L[R].tolist())
        # strip coloops (lines outside the span of the rest of R): deleting one drops the rank by one
        col = [t for t in R if U.rank_q(L[[u for u in R if u != t]].tolist()) < r0]
        R = np.array([t for t in R if t not in col])
        r = U.rank_q(L[R].tolist())
        assert r == r0 - len(col)
        q = len(R) // r
        while q > 0:
            S = pack(L[R], q)
            if all(len(s) == r for s in S):
                break
            q -= 1
        for s in S:
            assert U.rank_q(L[R[sorted(s)]].tolist()) == r
        assert len(set().union(*S)) == q * r
        print('n=%d k=%d: |R|=%d rank=%d coloops=%d %s; rest rank %d holds %d disjoint bases (verified exactly)'
              ' -> rank(R - P) >= %d - floor(|P|/%d)' % (n, k, len(R) + len(col), r0, len(col), [int(c) for c in col], r, q, r, q), flush=True)
